#!/usr/bin/python

import sys
import json
from deriva.core import ErmrestCatalog, AttrDict, get_credential, DEFAULT_CREDENTIAL_FILE, tag, urlquote, DerivaServer, get_credential, BaseCLI
from deriva.core.ermrest_model import builtin_types, Schema, Table, Column, Key, ForeignKey
from deriva.core import urlquote, urlunquote
from deriva.core import HatracStore
import requests.exceptions
from ... import utils
from ...utils import DCCTX, PDBDEV_CLI, cfg

'''
NOTE: Use cfg object to check for different deployment env 
'''

GROUPS = {
    "public" : ["*"],
    "pdb-admins" : ["https://auth.globus.org/0b98092c-3c41-11e9-a8c8-0ee7d80087ee"],
    "pdb-curators" : ["https://auth.globus.org/eef3e02a-3c40-11e9-9276-0edc9bdd56a6"],
    "pdb-submitters" : ["https://auth.globus.org/99da042e-64a6-11ea-ad5f-0ef992ed7ca1"],
    "pdb-writers" : ["https://auth.globus.org/c94a1e5c-3c40-11e9-a5d1-0aacc65bfe9a"],  # inactive    
    "pdb-readers" : ["https://auth.globus.org/8875a770-3c40-11e9-a8c8-0ee7d80087ee"],  # inactive
    "isrd-staff": ["https://auth.globus.org/176baec4-ed26-11e5-8e88-22000ab4b42b"],    
    "isrd-systems": ["https://auth.globus.org/3938e0d0-ed35-11e5-8641-22000ab4b42b"],
    "isrd-testers": ["https://auth.globus.org/9d596ac6-22b9-11e6-b519-22000aef184d"],
    "pdb-ihm": ["https://auth.globus.org/cfc89bb6-3d96-4f50-8f1d-f625ef400e40"], 
}
g = GROUPS
GROUPS["owners"] = g["isrd-systems"] + g["pdb-admins"] 
GROUPS["pdb-all"] = g["pdb-admins"] + g["pdb-submitters"] + g["pdb-curators"]
GROUPS["isrd-all"] = g["isrd-systems"] + g["isrd-staff"] + g["isrd-testers"]

# -- remove owners from the these groups, so the policy is easier to read, as owners can do anything already
# -- NOTE: ignore pdb-readers and pdb-writers for now
GROUPS["entry_creators"] = g["pdb-submitters"] + g["pdb-curators"] + g["isrd-staff"]
GROUPS["entry_updaters"] = g["pdb-curators"] + g["isrd-staff"]
#GROUPS["entry_readers"] = g["pdb-curators"] + g["isrd-staff"]   # to discuss, ignore for now

ERMREST_CATALOG_ACLS = {
    "owner" : g["owners"],
    "enumerate": g["public"], 
    "select": g["entry_updaters"],
    "insert": g["entry_updaters"],
    "update": g["entry_updaters"],
    "delete": g["entry_updaters"],
}

FKEY_ACLS = {
    "default": { "insert": ["*"], "update": ["*"] },
    "RCBRMB": None,
}

FKEY_ACL_BINDINGS = {
    # set Owner group only if user is a member of the group
    "set_owner_old": {
        "types": ["update", "insert"],
        "scope_acl": ["*"], 
        "projection": ["ID"],
        "projection_type": "acl"
    }
}



# -- ---------------------------------------------------------------------
# clear all the ACLs in the table and reset the fkey.acls to default
def clear_table_acls(table):

    if False: # to debug
        for fkey in table.foreign_keys:
            from_cols = {c.name for c in fkey.column_map.keys()}
            to_cols = {c.name for c in fkey.column_map.values()}
            pk_table = fkey.pk_table
            print("       B-- fk %s:%s (%s->%s:%s) acls: %s, acl_bindings: %s" % (table.name, fkey.constraint_name, from_cols, fkey.pk_table.name, to_cols, fkey.acls, fkey.acl_bindings))
            
    table.clear(clear_comment=False, clear_annotations=False, clear_acls=True, clear_acl_bindings=True)

    if False: # to debug
        for fkey in table.foreign_keys:
            from_cols = {c.name for c in fkey.column_map.keys()}
            to_cols = {c.name for c in fkey.column_map.values()}
            pk_table = fkey.pk_table
            print("       C-- fk %s:%s (%s->%s:%s) acls: %s, acl_bindings: %s" % (table.name, fkey.constraint_name, from_cols, fkey.pk_table.name, to_cols, fkey.acls, fkey.acl_bindings))

    # assign default to fkey acls
    for fkey in table.foreign_keys:
        fkey.acls = FKEY_ACLS["default"]
        if False: # to debug
            from_cols = {c.name for c in fkey.column_map.keys()}
            to_cols = {c.name for c in fkey.column_map.values()}
            pk_table = fkey.pk_table        
            print("       S-- fk %s:%s (%s->%s:%s) acls: %s, acl_bindings: %s" % (table.name, fkey.constraint_name, from_cols, fkey.pk_table.name, to_cols, fkey.acls, fkey.acl_bindings))        

# -- ---------------------------------------------------------------------
# clear all acls and acl_bindings under the schema
def clear_schema_acls(schema):
    # NOTE: There is a bug in the fkey clear. It doesn't set the fkey acls to default.
    # Uncomment and ignore the rest of the code when the bug is fixed
    #schema.clear(clear_comment=False, clear_annotations=False, clear_acls=True, clear_acl_bindings=True)
    
    schema.acls.clear()
    for table in schema.tables.values():
        clear_table_acls(table)

# -- ---------------------------------------------------------------------
def print_table_acls(table):

    print("  t: %s acls: %s acl_bindings: %s" % (table.name, table.acls, table.acl_bindings))
    for col in table.columns:
        if col.acls or col.acl_bindings:
            print("    c: %s.%s: acls=%s acl_bindings=%s" % (table.name, col.name, col.acls, col.acl_bindings))
    for fkey in table.foreign_keys:
        from_cols = {c.name for c in fkey.column_map.keys()}
        to_cols = {c.name for c in fkey.column_map.values()}
        pk_table = fkey.pk_table        
        print("      fk %s:%s (%s->%s:%s) acls: %s, acl_bindings: %s" % (table.name, fkey.constraint_name, from_cols, fkey.pk_table.name, to_cols, fkey.acls, fkey.acl_bindings))        
    
# -- ---------------------------------------------------------------------
# no acl and acl_bindings set in Vocab tables
# 
def print_acls(model, schema_names=["PDB"]):
    for sname in schema_names:
        schema = model.schemas[sname]
        for table in schema.tables.values():
            print("--- %s:%s ---" % (schema.name, table.name))
            # == print table acls
            if table.acls  == {
                    'owner': ['https://auth.globus.org/0b98092c-3c41-11e9-a8c8-0ee7d80087ee', 'https://auth.globus.org/176baec4-ed26-11e5-8e88-22000ab4b42b'],
                    'write': [],
                    'delete': ['https://auth.globus.org/eef3e02a-3c40-11e9-9276-0edc9bdd56a6'],
                    'insert': ['https://auth.globus.org/eef3e02a-3c40-11e9-9276-0edc9bdd56a6', 'https://auth.globus.org/c94a1e5c-3c40-11e9-a5d1-0aacc65bfe9a', 'https://auth.globus.org/99da042e-64a6-11ea-ad5f-0ef992ed7ca1'],
                    'select': ['https://auth.globus.org/c94a1e5c-3c40-11e9-a5d1-0aacc65bfe9a', 'https://auth.globus.org/8875a770-3c40-11e9-a8c8-0ee7d80087ee'],
                    'update': ['https://auth.globus.org/eef3e02a-3c40-11e9-9276-0edc9bdd56a6'],
                    'enumerate': ['*']
            }:
                #print("     %s: DEFAULT TABLE ACL 1" % (table.name))
                #continue
                pass
            elif table.acls == {
                    'delete': ['https://auth.globus.org/0b98092c-3c41-11e9-a8c8-0ee7d80087ee', 'https://auth.globus.org/176baec4-ed26-11e5-8e88-22000ab4b42b', 'https://auth.globus.org/eef3e02a-3c40-11e9-9276-0edc9bdd56a6'],
                    'insert': ['https://auth.globus.org/0b98092c-3c41-11e9-a8c8-0ee7d80087ee', 'https://auth.globus.org/176baec4-ed26-11e5-8e88-22000ab4b42b', 'https://auth.globus.org/eef3e02a-3c40-11e9-9276-0edc9bdd56a6'],
                    'select': ['*'],
                    'update': ['https://auth.globus.org/0b98092c-3c41-11e9-a8c8-0ee7d80087ee', 'https://auth.globus.org/176baec4-ed26-11e5-8e88-22000ab4b42b', 'https://auth.globus.org/eef3e02a-3c40-11e9-9276-0edc9bdd56a6'],
                    'enumerate': ['*'],
            }:
                #print("     %s: DEFAULT TABLE ACL 2" % (table.name))
                #continue
                pass
            elif table.acls == {
                    'delete': ['https://auth.globus.org/0b98092c-3c41-11e9-a8c8-0ee7d80087ee', 'https://auth.globus.org/176baec4-ed26-11e5-8e88-22000ab4b42b', 'https://auth.globus.org/eef3e02a-3c40-11e9-9276-0edc9bdd56a6'],
                    'insert': ['https://auth.globus.org/0b98092c-3c41-11e9-a8c8-0ee7d80087ee', 'https://auth.globus.org/eef3e02a-3c40-11e9-9276-0edc9bdd56a6', 'https://auth.globus.org/176baec4-ed26-11e5-8e88-22000ab4b42b'],
                    'select': ['https://auth.globus.org/0b98092c-3c41-11e9-a8c8-0ee7d80087ee', 'https://auth.globus.org/eef3e02a-3c40-11e9-9276-0edc9bdd56a6', 'https://auth.globus.org/176baec4-ed26-11e5-8e88-22000ab4b42b'],
                    'update': ['https://auth.globus.org/0b98092c-3c41-11e9-a8c8-0ee7d80087ee', 'https://auth.globus.org/eef3e02a-3c40-11e9-9276-0edc9bdd56a6', 'https://auth.globus.org/176baec4-ed26-11e5-8e88-22000ab4b42b'],
                    'enumerate': ['*']
            }:
                #print("     %s: DEFAULT TABLE ACL 3" % (table.name))
                #continue
                pass
            elif not table.acls:
                print("     %s: DEFAULT TABLE ACL 4: NO ACLS" % (table.name))
                pass
            elif table.acls or table.acl_bindings:
                print(" t: %s acls: %s acl_bindings: %s" % (table.name, table.acls, table.acl_bindings))
            else:
                print("     %s: NON DEFAULT" % (table.name))
                pass

            acl_bindings: {
                'released_reader': {
                    'types': ['select'],
                    'scope_acl': ['https://auth.globus.org/99da042e-64a6-11ea-ad5f-0ef992ed7ca1'],
                    'projection': [{'outbound': ['PDB', 'struct_ref_seq_structure_id_fkey']}, 'RCB'],
                    'projection_type': 'acl'
                },
                'self_service_creator': {
                    'types': ['update', 'delete'],
                    'scope_acl': ['https://auth.globus.org/99da042e-64a6-11ea-ad5f-0ef992ed7ca1'],
                    'projection': [{'outbound': ['PDB', 'struct_ref_seq_structure_id_fkey']},
                                   {'or': [{'filter': 'Workflow_Status', 'operand': 'DRAFT', 'operator': '='},
                                           {'filter': 'Workflow_Status', 'operand': 'DEPO', 'operator': '='},
                                           {'filter': 'Workflow_Status', 'operand': 'RECORD READY', 'operator': '='},
                                           {'filter': 'Workflow_Status', 'operand': 'ERROR', 'operator': '='}]},
                                   'RCB'],
                    'projection_type': 'acl'
                }
            }
            # == print column acls
            for col in table.columns:
                if col.acls or col.acl_bindings:
                    print("  c: %s.%s: acls=%s acl_bindings=%s" % (table.name, col.name, col.acls, col.acl_bindings))
                    
            # == print fkey acls
            for fkey in table.foreign_keys:
                from_cols = {c.name for c in fkey.column_map.keys()}
                to_cols = {c.name for c in fkey.column_map.values()}
                if from_cols == {"Owner"}:
                    #print("     OWNER: fk %s (%s) acls: %s, acl_bindings: %s" % (fkey.constraint_name, from_cols, fkey.acls, fkey.acl_bindings))
                    continue
                elif from_cols == {"RCB"} or from_cols == {"RMB"}:
                    # current policy: acls: {}, acl_bindings: {}                    
                    continue
                elif from_cols == {"Entry_Related_File"}:
                    # current policy: acls: {}, acl_bindings: {} and sometimes with default acls
                    #print("     ENTRY_RELATED_FILE: fk %s (%s) acls: %s, acl_bindings: %s" % (fkey.constraint_name, from_cols, fkey.acls, fkey.acl_bindings))                    
                    continue
                elif fkey.acls == {"insert": ["*"], "update": ["*"]} and not fkey.acl_bindings:
                    #print("     DEFAULT: fk %s (%s) acls: %s, acl_bindings: %s" % (fkey.constraint_name, from_cols, fkey.acls, fkey.acl_bindings))
                    continue  
                # if (from_cols == {"structure_id"} or from_cols == {"entry_id"}) or \                
                elif fkey.pk_table.name == "entry" and to_cols == {"id"} and fkey.acl_bindings == {
                        'unfrozen': {
                            'types': ['insert', 'update'],
                            'projection': [
                                {'or': [
                                    {'filter': 'Workflow_Status', 'operand': 'DRAFT', 'operator': '='},
                                    {'filter': 'Workflow_Status', 'operand': 'DEPO', 'operator': '='},
                                    {'filter': 'Workflow_Status', 'operand': 'RECORD READY', 'operator': '='},
                                    {'filter': 'Workflow_Status', 'operand': 'ERROR', 'operator': '='} ]
                                 },
                                'RID'
                            ],
                            'projection_type': 'nonnull',
                            'scope_acl': ['*']
                        }
                }:
                    #print("     ENTRY_STATUS: fk %s:%s (%s->%s:%s) acls: %s, acl_bindings: %s" % (table.name, fkey.constraint_name, from_cols, fkey.pk_table.name, to_cols, fkey.acls, fkey.acl_bindings))
                    continue
                else:
                    print("    fk: %s:%s (%s->%s:%s) acls: %s, acl_bindings: %s" % (table.name, fkey.constraint_name, from_cols, fkey.pk_table.name, to_cols, fkey.acls, fkey.acl_bindings))

        continue
    
# -- ---------------------------------------------------------------------
'''
  PDB schema Inherit catalog level policy. Overwrite the tables that submitters can insert in on individual tables.
  NOTE: Owner fkeys will be cleared through the clear statement
'''
def set_PDB_acl(model):
    schema = model.schemas["PDB"]
    print("set_PDB_acl")
    
    #schema.clear(clear_comment=False, clear_annotations=False, clear_acls=True, clear_acl_bindings=True)
    clear_schema_acls(schema)

    set_PDB_entry(model)
    set_PDB_entry_related(model)      # set appropriate Entry_Related_File
    set_PDB_entry_collection_related(model)
    set_PDB_entry_related_system_generated_tables(model)
    set_PDB_Accession_Code(model)
    set_PDB_Data_Dictionary_Related(model)
    set_PDB_Entry_Related_File_Templates(model)    

# -- ---------------------------------------------------------------------
'''
  Allow entry_creators to read only. All changes will be done programmitically or by entry_updaters
'''
def set_Vocab_acl(model):
    schema = model.schemas["Vocab"]
    print("set_Vocab_acl")
    
    #schema.clear(clear_comment=False, clear_annotations=False, clear_acls=True, clear_acl_bindings=True)
    clear_schema_acls(schema)
    
    # Anyone can read. The rest follows catalog policy
    schema.acls = {
        "select": g["entry_creators"],
    }

# -- ---------------------------------------------------------------------
'''
  Most of the tables in this schema should be created by the Deriva system.
  NOTE: We have Catalog_Group which is currently empty and is not system generated.
'''
def set_public_acl(model):
    schema = model.schemas["public"]
    print("set_public_acl")
    
    # -- reset policies
    # there is a bug in acl_binding.clear()
    #schema.clear(clear_comment=False, clear_annotations=False, clear_acls=True, clear_acl_bindings=True)
    clear_schema_acls(schema)    
    
    schema.acls = {
        "select": g["entry_updaters"],
        "insert": [],
        "update": [],
        "delete": [],
    }    
    
    # -- ERMrest_Client
    table = schema.tables["ERMrest_Client"]
    table.acl_bindings = {
        "submitters_read_own_entries": {
            "types": ["select"],
            "scope_acl": g["pdb-submitters"],
            "projection": ["ID"],
            "projection_type": "acl"
        }
    }

    # -- ERMrest_Group inherit default policy

    # -- Catalog_Group: entry_updaters can modify for now
    table = schema.tables["Catalog_Group"]
    table.acls = {
        "select" : g['entry_updaters'],
        "insert" : g['entry_updaters'],  
        "update": g["entry_updaters"],
        "delete": g["entry_updaters"],
    }
    

# -- ---------------------------------------------------------------------
'''
  Tables in this schema is not really being used. Inherit catalog level policy for now
'''
def set_WWW_acl(model):
    schema = model.schemas["WWW"]

    print("set_WWW_acl")
    # There is a bug in schema.clear. Need to set fkey.acls to default
    #schema.clear(clear_comment=False, clear_annotations=False, clear_acls=True, clear_acl_bindings=True)
    clear_schema_acls(schema)

    # -- inherit policy from catalog e.g. only entry_updaters can do anything
    # -- Page
    
    # -- Page_Asset
    table = schema.tables["Page_Asset"]
    ''' # if only entry_updaters can create, no need for acl_bindings
    table.acl_bindings =  {
        "rcb_update_its_own_page": {
            "types": ["insert", "update"],
            "projection": ["RCB"],
            "projection_type": "acl",
            "scope_acl": ["*"]}
    }    
    '''
    
# -- ---------------------------------------------------------------------
def set_PDB_entry(model):
    schema = model.schemas["PDB"]    
    table = schema.tables["entry"]
    print("  - set_PDB_entry")
    # assuming that the table policy has been cleared.

    # == policy dict
    col_acl_bindings = {
        "submitters_read_based_on_workflow_status": {
            "types": [ "select" ],
            "scope_acl": g["pdb-submitters"],
            "projection": [
                {
                    "or": [
                        { "filter": "Workflow_Status", "operator": "=", "operand": "REL" },
                        { "filter": "Workflow_Status", "operator": "=", "operand": "HOLD" },
                    ]
                },
                "RID"
            ],
            "projection_type": "nonnull"
        },
    }
    
    # ==== table-level =====    
    # Policy: Submitter can create but can only see their own entries. They can't delete entries during a certain workflow status.
    table.acls = {
        "select": g["entry_updaters"],
        "insert": g["entry_creators"],
        "update": g["entry_updaters"],                    
        "delete": g["entry_updaters"],          
    }
    table.acl_bindings = {
        "submitters_read_own_entries": {
            "types": ["select"],
            "scope_acl": g["pdb-submitters"],
            "projection": ["RCB"],
            "projection_type": "acl"
        },
        "submitters_modify_based_on_workflow_status": {
            "types": ["update", "delete"],
            "scope_acl": g["pdb-submitters"],
            "projection": [
                {
                    "or": [
                        { "filter": "Workflow_Status", "operator": "=", "operand": "DRAFT",  },
                        { "filter": "Workflow_Status", "operator": "=", "operand": "DEPO", },
                        { "filter": "Workflow_Status", "operator": "=", "operand": "RECORD READY", },
                        { "filter": "Workflow_Status", "operator": "=", "operand": "ERROR", }
                    ]
                },
                "RCB"
            ],
            "projection_type": "acl"
        }
    }

    # ==== column-level =====
    # -- Accession_Code: submitters can only see when the entry is HOLD or REL
    table.columns["Accession_Code"].acls = {
        "insert": g["entry_updaters"],
    }
    table.columns["Accession_Code"].acl_bindings = {    
        "submitters_read_own_entries": False,
        "submitters_modify_based_on_workflow_status": False,
        "submitters_read_based_on_workflow_status": col_acl_bindings["submitters_read_based_on_workflow_status"],
    }

    # -- Release date: submitters can only see when the entry is HOLD or REL
    table.columns["Release_Date"].acls = {
        "select": g["entry_updaters"],        
    }
    table.columns["Release_Date"].acl_bindings = {
        "submitters_read_own_entries": False,
        "submitters_modify_based_on_workflow_status": False,
        "submitters_read_based_on_workflow_status": col_acl_bindings["submitters_read_based_on_workflow_status"],        
    }
    
    # -- Deposit date: entry_creator can read, but only updater can insert
    table.columns["Deposit_Date"].acls = {    
        "select": g["entry_creators"],        
        "insert": g["entry_updaters"],
    }

    # -- Notes: only entry updaters can create and read
    table.columns["Notes"].acls = {            
        "select": g["entry_updaters"],        
        "insert": g["entry_updaters"],
      }

    # ==== foreign keys =====

    # -- Workflow Status: submitters can only choose Workflow_Status that they are allowed
    table.foreign_keys[(schema, "entry_Workflow_Status_fkey")].acls = { 
        "insert": g["entry_updaters"],
        "update": g["entry_updaters"],
    }
    table.foreign_keys[(schema, "entry_Workflow_Status_fkey")].acl_bindings = {
        # submitters can only selected workflow status that they are allowed (PDB_Submitter_Allow)
        "submitters_select_allowed_workflow_status": {
            "types": [ "insert", "update" ],
            "scope_acl": g["pdb-submitters"],
            "projection": [
                { "filter": "PDB_Submitter_Allow", "operator": "=", "operand": "True",  },
                "RID"
            ],
            "projection_type": "nonnull"
        }
    }

    # -- Use default for the rest of fkeys
    #table.foreign_keys[(schema, "entry_Accession_Code_fkey")].acls = FKEY_ACLS["default"]
    #table.foreign_keys[(schema, "entry_Workflow_Status_fkey")].acls = FKEY_ACLS["default"]
    #table.foreign_keys[(schema, "entry_Owner_fkey")].acls = {}
    #table.foreign_keys[(schema, "entry_RCB_fkey")].acls = {}
    #table.foreign_keys[(schema, "entry_RMB_fkey")].acls = {}        


# -- ---------------------------------------------------------------------
'''
  Include all tables that has a forieng key pointed to entry.id excepted those in ENTRY_RELATED_SYSTEM_GENERATED_TABLE_NAMES
  All entry related tables have direct fkey to entry (no tables that link to entry through assocation)
  TODO: address fkey to entry that's not through id
'''
# Apply the entry access control on these tables 
def set_PDB_entry_related(model):
    schema = model.schemas["PDB"]
    entry_table = schema.tables["entry"]
    entry_related_tables = []

    # Create entry_related_tables: any table that has a fkey pointing to the entry_table.
    # There might be a small subset of these tables that have their own policies. In that case,
    # the script will just clean the table policy before setting a new one. 
    for table in schema.tables.values():
        # == exclude system generated tables that linked to entry
        if table.name in entry_related_exclusion:
            continue
        for fkey in table.foreign_keys:
            from_cols = {c.name for c in fkey.column_map.keys()}
            to_cols = {c.name for c in fkey.column_map.values()}
            pk_table = fkey.pk_table
            # == these are entry related tables
            if pk_table.name == "entry" and to_cols == {"id"} :
                # == set fkey policies
                fkey.acl = {
                    "insert": g["entry_updaters"],
                    "update": g["entry_updaters"],
                }
                fkey.acl_bindings = {
                    # submitter can only choose their own entries with certain Workflow Status
                    "submitters_modify_based_on_entry_workflow_status": {
                        "types": ["update", "delete"],
                        "scope_acl": g["pdb-submitters"],
                        "projection": [
                            {
                                "or": [
                                    { "filter": "Workflow_Status", "operator": "=", "operand": "DRAFT",  },
                                    { "filter": "Workflow_Status", "operator": "=", "operand": "DEPO", },
                                    { "filter": "Workflow_Status", "operator": "=", "operand": "RECORD READY", },
                                    { "filter": "Workflow_Status", "operator": "=", "operand": "ERROR", }
                                ]
                            },
                            "RCB"
                        ],
                        "projection_type": "acl"
                    },
                }
                # == table policies if haven't already set. Might not need to check if there is only 1 fkey.
                if table in entry_related_tables:
                    continue
                print("  - set_entry_related: %s" % (table.name,))
                entry_related_tables.append(table)
                # set acls to be the same as entry table
                table.acls = entry_table.acls
                # submitters can reads their own entries and update according to its entry's workflow status (e.g. follow the fkey to entry table)        
                table.acl_bindings = {
                    "submitter_read_own_entries" : {
                        "types": ["select"],
                        "scope_acl": g["pdb-submitters"],
                        "projection": [{"outbound": ["PDB", fkey.constraint_name ]}, "RCB"],
                        "projection_type": "acl"
                    },
                    # submitter can only choose their own entries with certain Workflow Status            
                    "submitter_update_based_on_workflow_status" : {
                        "types": ["update", "delete"],
                        "scope_acl": g["pdb-submitters"],
                        "projection": [
                            {"outbound": ["PDB", fkey.constraint_name]},           
                            {"or": [
                                { "filter": "Workflow_Status", "operator": "=", "operand": "DRAFT",  },
                                { "filter": "Workflow_Status", "operator": "=", "operand": "DEPO", },
                                { "filter": "Workflow_Status", "operator": "=", "operand": "RECORD READY", },
                                { "filter": "Workflow_Status", "operator": "=", "operand": "ERROR", }
                            ]},
                            "RCB",
                        ],
                        "projection_type": "acl",
                    }
                }
            # -- end fkey that point to entry
        # -- end fkey
    # -- end table


# -- ---------------------------------------------------------------------
'''
  policy: pdb-ihm generated content, entry_updater can read, pdb_submitter can only read their own entry
'''
def set_PDB_entry_collection_related(model):
    collection_table = schemas.tables["_ihm_entry_collection"]
    mapping_table = schemas.tables["_ihm_entry_collection_mapping"]
    # -- clear table policies in case they were set by entry_related logic
    clear_table_acls(collection_table)
    clear_table_acls(mapping_table)
    
    entry_fkey = None
    collection_fkey = None
    
    # find 2 fkeys in mapping table
    for fkey in mapping_table.foreign_keys:
        pk_table = fkey.pk_table
        if pk_table = entry_table:
            entry_fkey = fkey
        if pk_table = mapping_table:
            collection_fkey = fkey

    # this shouldn't happen
    if entry_fkey == None or collection_fkey == None:
        raise Exception("ERROR: _ihm_entry_collection_mappings do not have proper foreign keys to entry and/or collection table")

    # == set policy on _ihm_entry_collection table
    # -- acl: adopt schema levevl for acls e.g. only entry_updaters can read/write
    # -- acl_bindings: pdb_submitters can only see their entries
    collection_table.acl_bindings = {
        "submitter_read_own_entries" : {
            "types": ["select"],
            "scope_acl": g["pdb-submitters"],
            "projection": [
                {"inbound": ["PDB", collection_fkey.constraint_name ]},
                {"outbound": ["PDB", entry_fkey.constraint_name ]},
                "RCB"
            ],
            "projection_type": "acl"
        }
    }
        
    # == set policies for the mapping table: only curator can set up mapping table at any time
    # -- acl: adopts schema policy
    # -- acl_bindings: pdb_submitters can only see their entries
    mapping_table.acl_bindings = {
        "submitter_read_own_entries" : {
            "types": ["select"],
            "scope_acl": g["pdb-submitters"],
            "projection": [ {"outbound": ["PDB", entry_fkey.constraint_name ]}, "RCB" ],
            "projection_type": "acl"
        }
    }
    
    
# -- ---------------------------------------------------------------------
'''
  policy: pdb-ihm generated content, entry_updater can read, pdb_submitter can only read their own entry
'''
def set_PDB_entry_related_system_generated_tables(model):
    schema = model.schemas["PDB"]
    for tname in ["Entry_Error_File", "Entry_mmCIF_File"]
        print("  - set_entry_related_system_generated_table: %s" % (tname,))        
        table = schema.tables[tname]
        clear_table_acls(table) 
        
        # == table policy
        # -- acl: only pdb-ihm can manipulate, entry_updaters can read (from schema acl)
        table.acls = {
            "insert": g["pdb-ihm"],
            "update": g["pdb-ihm"],
            "delete": g["pdb-ihm"],
        }
        # -- acl_bindings: submitters can read if it is linked to their entries (need to traverse fkey to entry)
        for fkey in table.foreign_keys:
            from_cols = {c.name for c in fkey.column_map.keys()}
            to_cols = {c.name for c in fkey.column_map.values()}
            pk_table = fkey.pk_table
            if pk_table.name == "entry" and to_cols == {"id"} :
                table.acl_bindings = {
                    "submitter_read_own_entries" : {
                        "types": ["select"],
                        "scope_acl": g["pdb-submitters"],
                        "projection": [{"outbound": ["PDB", fkey.constraint_name ]}, "RCB"],
                        "projection_type": "acl"
                    }
                }
            # -- if the fkey to entry
        # -- end fkey
    # -- end tname
    
# -- ---------------------------------------------------------------------    
def set_PDB_Accession_Code(model):
    table = model.schemas["PDB"].tables["Accession_Code"]
    clear_table_acls(table)
    print("  - set_PDB_Accession_Code")
    
    # submitters can only read their entry Accession_Code
    table.acl_bindings = {
        "submitters_read_own_entries": {
            "types": ["select"],
            "scope_acl": g["pdb-submitters"],
            "projection": [{"outbound": ["PDB", "Accession_Code_Entry_fkey"]}, "RCB"],
            "projection_type": "acl"
        }
    }

# -- ---------------------------------------------------------------------
# Data_Dictionary, Supported_Dictionary: only updater can read and do anything
def set_PDB_Data_Dictionary_Related(model):
    for table_name in ["Data_Dictionary", "Supported_Dictionary"]:
        print("  - set PDB_Data_Dictionary_Related: %s" % (table_name))
        table = model.schemas["PDB"].tables[table_name]
        clear_table_acls(table)                
        # use default schema ACLs (only entry_updaters can do anything to these tables)


# -- ---------------------------------------------------------------------
# Any group members should be able to read?
# current acls:
#  - Entry_Related_File_Templates: DEFAULT TABLE ACL 4: NO ACLS
#  - c Entry_Related_File_Templates.File_URL: acls={'select': ['*']} acl_bindings={'no_binding': False}
#    -- fk Entry_Related_File_Templates:Entry_Template_File_File_Type_fkey ({'File_Type'}->File_Type:{'Name'}) acls: {'insert': ['*'], 'update': ['*']}, acl_bindings: {}
#    -- fk Entry_Related_File_Templates:Entry_Template_File_Owner_fkey ({'Owner'}->Catalog_Group:{'ID'}) acls: {'insert': ['https://auth.globus.org/eef3e02a-3c40-11e9-9276-0edc9bdd56a6'], 'update': ['https://auth.globus.org/eef3e02a-3c40-11e9-9276-0edc9bdd56a6']}, acl_bindings: {'set_owner': {'types': ['update', 'insert'], 'scope_acl': ['*'], 'projection': ['ID'], 'projection_type': 'acl'}}
#
def set_PDB_Entry_Related_File_Templates(model):
    for tname in ["Entry_Related_File_Templates"]:
        print("  - set PDB_Entry_Related_File_Templates: %s" % (tname,))        
        table = model.schemas["PDB"].tables[tname]
        clear_table_acls(table)

        # allow entry_creators to read        
        table.acls = {
            "select": g["entry_creators"],            
        }
                
# -- ---------------------------------------------------------------------
# 
def set_ermrest_acl(catalog):
    model = catalog.getCatalogModel()
    #response = catalog.get("/schema")
    #schema = response.json()
    #print(json.dumps(schema, indent=2))

    # test deriva-py clear function
    print_table_acls(model.schemas["PDB"].tables["entry"])    
    if False:
        print_acls(model, ["PDB"])
        #clear_table_acls(model.schemas["PDB"].tables["Entry_Related_File_Templates"])        
        set_PDB_Entry_Related_File_Templates(model)
        print_table_acls(model.schemas["PDB"].tables["Entry_Related_File_Templates"])

    '''
    # -- catalog
    model.acls = ERMREST_CATALOG_ACLS
    # -- schemas
    set_PDB_acl(model)
    set_Vocab_acl(model)        
    set_public_acl(model)
    set_WWW_acl(model)
    # -- apply 
    model.apply()
    '''
# -- =================================================================================
        
def main(server_name, catalog_id, credentials):
    server = DerivaServer("https", server_name, credentials)
    catalog = server.connect_ermrest(catalog_id)
    catalog.dcctx["cid"] = utils.DCCTX["acl"]
    #store = HatracStore("https", server_name, credentials)

    set_ermrest_acl(catalog)
    
# -- =================================================================================
#  python ermrest_acl.py --host dev.pdb-dev.org --catalog_id 99 
if __name__ == "__main__":
    args = PDBDEV_CLI(DCCTX["acl"], None, 1).parse_cli()
    credentials = get_credential(args.host, args.credential_file)
    print(credentials)
    main(args.host, args.catalog_id, credentials)

