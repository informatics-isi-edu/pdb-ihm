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
from deriva.utils.extras.model import clear_schema_acls, print_schema_model_extras, print_table_model_extras, format_acls, format_acl_bindings, ermrest_groups, set_ermrest_groups

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
    "pdb-ihm-dev": [],     
    "pdb-ihm": ["https://auth.globus.org/cfc89bb6-3d96-4f50-8f1d-f625ef400e40"], 
}
g = GROUPS
GROUPS["owners"] = g["isrd-systems"] + g["pdb-admins"]
GROUPS["pdb-pipelines"] = g["pdb-ihm"]
GROUPS["pdb-all"] = g["pdb-admins"] + g["pdb-submitters"] + g["pdb-curators"]
GROUPS["isrd-internal"] = g["isrd-systems"] + g["isrd-staff"]
GROUPS["isrd-all"] = g["isrd-systems"] + g["isrd-staff"] + g["isrd-testers"]

# -- remove owners from the these groups, so the policy is easier to read, as owners can do anything already
# -- NOTE: ignore pdb-readers and pdb-writers for now
GROUPS["entry-creators"] = g["pdb-submitters"] + g["pdb-curators"] + g["isrd-staff"] 
GROUPS["entry-updaters"] = g["pdb-curators"] + g["isrd-staff"]
GROUPS["entry-readers"] = g["pdb-readers"]

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

ermrest_catalog_acls = {}
column_curator_enumerate_curator_read_curator_write = {}

# -- set different group members depending on deployment environment
def initialize_policies(catalog):
    global g, ermrest_catalog_acls, column_curator_enumerate_curator_read_curator_write
    if not ermrest_groups: set_ermrest_groups(catalog) # needed to use humanize groups in format_acls/acl_bindings 
    
    if cfg.is_dev:
        g["owners"] = g["owners"] + g["isrd-staff"]
        g["entry-updaters"] = g["entry-updaters"] + g["isrd-testers"]
        g["pdb-pipeline"] = g["pdb-ihm-dev"]

    ermrest_catalog_acls = {
        "owner" : g["owners"],
        "enumerate": g["public"], 
        "select": g["entry-updaters"] + g["entry-readers"],
        "insert": g["entry-updaters"],
        "update": g["entry-updaters"],
        "delete": g["entry-updaters"],
        "create": [],
        "write": [],
    }

    column_curator_enumerate_curator_read_curator_write = {
        "enumerate": g["entry-updaters"],
        "select": g["entry-updaters"],
        "insert": g["entry-updaters"],
        "update": g["entry-updaters"],
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
        fkey.acls.clear()
        fkey.acls.update(FKEY_ACLS["default"])
        if False: # to debug
            from_cols = {c.name for c in fkey.column_map.keys()}
            to_cols = {c.name for c in fkey.column_map.values()}
            pk_table = fkey.pk_table        
            print("       S-- fk %s:%s (%s->%s:%s) acls: %s, acl_bindings: %s" % (table.name, fkey.constraint_name, from_cols, fkey.pk_table.name, to_cols, fkey.acls, fkey.acl_bindings))        

# -- ---------------------------------------------------------------------
# clear all acls and acl_bindings under the schema
def x_clear_schema_acls(schema):
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
    
# -- ======================================================================
# schema policies
#    
# -- ---------------------------------------------------------------------
'''
  PDB schema Inherit catalog level policy. Overwrite the tables that submitters can insert in on individual tables.
  NOTE: Owner fkeys will be cleared through the clear statement
'''
def set_PDB_acl(model):
    schema = model.schemas["PDB"]
    print("set_PDB_acl")
    
    # -- set table level ACLs
    set_PDB_entry(model)
    set_PDB_entry_related(model)      # set appropriate Entry_Related_File
    set_PDB_entry_coordinates_related(model)
    set_PDB_Accession_Code(model) 
    set_PDB_Curation_Log(model)   
    set_PDB_entry_collection_related(model)
    set_PDB_entry_related_error_file_tables(model)
    set_PDB_entry_related_system_generated_tables(model)
    set_PDB_Entry_Related_File(model)
    set_PDB_Entry_Related_File_Templates(model)    
    set_tables_curators_access_only(model)
    set_tables_submitters_read(model)

    # -- apply add-on acls to all tables in schema
    # disable Owner columns
    for table in schema.tables.values():
        for col in table.columns:
            if col.name in ["Owner"]:
                col.acls.update({
                    "enumerate": [],                    
                    "select": [],
                    "insert": [],
                    "update": []
                    #"delete": [],
                })
    
    
# -- ---------------------------------------------------------------------
'''
  Allow entry-creators to read only. All changes will be done programmitically or by entry-updaters
'''
def set_Vocab_acl(model):
    schema = model.schemas["Vocab"]
    print("set_Vocab_acl")
    
    
    # Anyone can read. The rest follows catalog policy
    schema.acls.update({
        "select": g["entry-creators"],
    })

    # Block all access to ID, URI, Owner columns
    for table in schema.tables.values():
        for col in table.columns:
            if col.name in ["ID", "URI", "Owner"]:
                col.acls.update({
                    "enumerate": [],                    
                    "select": [],
                    "insert": [],
                    "update": []
                    #"delete": [],
                })

    
# -- ---------------------------------------------------------------------
'''
  Most of the tables in this schema should be created by the Deriva system.
  NOTE: We have Catalog_Group which is currently empty and is not system generated.
'''
def set_public_acl(model):
    schema = model.schemas["public"]
    print("set_public_acl")
    
    schema.acls.update({
        "select": g["entry-updaters"],
        "insert": [],
        "update": [],
        "delete": [],
    })
    
    # -- ERMrest_Client
    table = schema.tables["ERMrest_Client"]
    table.acl_bindings.update({
        "submitters_read_own_entries": {
            "types": ["select"],
            "scope_acl": g["pdb-submitters"],
            "projection": ["ID"],
            "projection_type": "acl"
        }
    })

    # -- ERMrest_Group inherit default policy

    # -- Catalog_Group: entry-updaters can modify for now
    table = schema.tables["Catalog_Group"]
    table.acls.update({
        "select" : g['entry-updaters'],
        "insert" : g['entry-updaters'],  
        "update": g["entry-updaters"],
        "delete": g["entry-updaters"],
    })
    

# -- ---------------------------------------------------------------------
'''
  Tables in this schema is not really being used. Inherit catalog level policy for now
'''
def set_WWW_acl(model):
    schema = model.schemas["WWW"]

    print("set_WWW_acl")
    
    # -- inherit policy from catalog e.g. only entry-updaters can do anything
    # -- Page
    
    # -- Page_Asset
    table = schema.tables["Page_Asset"]
    ''' # if only entry-updaters can create, no need for acl_bindings
    table.acl_bindings.update({
        "rcb_update_its_own_page": {
            "types": ["insert", "update"],
            "projection": ["RCB"],
            "projection_type": "acl",
            "scope_acl": ["*"]}
    })    
    '''

# -- ======================================================================
# table policies
#
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
                        { "filter": "Workflow_Status", "operator": "=", "operand": "RELEASE READY" },
                        { "filter": "Workflow_Status", "operator": "=", "operand": "HOLD" },
                    ]
                },
                "RID"
            ],
            "projection_type": "nonnull"
        },
    }
    
    # ==== table-level =====    
    # Policy: Submitter can create but can only see their own entries. They can't modify entries during a certain workflow status.
    table.acls.update({
        "insert": g["entry-creators"],
    })
    table.acl_bindings.update({
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
                        { "filter": "Process_Status", "operator": "=", "operand": "Error: generating mmCIF file", },
                        { "filter": "Process_Status", "operator": "=", "operand": "Error: processing uploaded mmCIF file", },
                        { "filter": "Process_Status", "operator": "=", "operand": "Error: processing uploaded restraint files", }
                    ]
                },
                "RCB"
            ],
            "projection_type": "acl"
        }
    })

    # ==== column-level =====
    # -- acl: no modification to these columns unless owner
    for cname in ["id"]:
        col = table.columns[cname]
        col.acls.update({
            "insert": [],
            "update": []
            #"delete": [],            
        })
    
    
    # -- acl: submitters can only see when the entry is HOLD or REL
    # -- cnames: Accession_Code, Release_Date
    for cname in ["Accession_Code", "Release_Date"]:
        col = table.columns[cname]
        col.acls.update({
            "insert": g["entry-updaters"],
        })
        col.acl_bindings.update({    
            "submitters_read_own_entries": False,
            "submitters_modify_based_on_workflow_status": False,
            "submitters_read_based_on_workflow_status": col_acl_bindings["submitters_read_based_on_workflow_status"],
        })
    
    # -- ACL: entry_creator can read, but only updater can insert
    # -- cnames: Deposit date, Submitter_Flag, Submitter_Flag_Date:
    cnames = ["Deposit_Date"]
    cnames += ["Submitter_Flag", "Submitter_Flag_Date"]
    for cname in cnames:
        col = table.columns[cname]
        col.acls.update({
            "select": g["entry-creators"],        
            "insert": g["entry-updaters"],
        })
        col.acl_bindings.update({
            "submitters_modify_based_on_workflow_status": False,
        })
    
    # -- ACL: only entry updaters can create and read:
    # -- cnames: Notes, Manual_Processing (TO-ADD)
    for cname in ["Notes", "Manual_Processing", "New_Chem_Comp_Pending"]:
        if not cname in table.columns.elements: continue
        col = table.columns[cname]
        col.acls.update(column_curator_enumerate_curator_read_curator_write)
        col.acl_bindings.update({
            "submitters_read_own_entries": False,        
            "submitters_modify_based_on_workflow_status": False,
        })

    # -- ACL: submiters can create but not edit
    cnames = ["Process_Status"]
    for cname in cnames:
        col = table.columns[cname]
        col.acls.update({
            "update": g["entry-updaters"],
        })
        col.acl_bindings.update({
            "submitters_modify_based_on_workflow_status": False,
        })
        
    # ==== foreign keys =====
    
    # -- Workflow_Status/Process_Status: submitters can only choose status that they are allowed
    status_related_fkeys = {
        "workflow_status": "entry_Workflow_Status_fkey",
        "process_status": "entry_Process_Status_fkey"
    }
    for status_name, constraint_name in status_related_fkeys.items():
        fkey = table.foreign_keys[(schema, constraint_name)]
        fkey.acls.update({
            "insert": g["entry-updaters"],
            "update": g["entry-updaters"],   # TODO: removed from Process_Status fkey
        })
        # set acl_binding policy name
        submitters_select_allowed = f"submitters_select_allowed_{status_name}" # eg submitters_select_allowed_workflow_status
        curators_select_allowed = f"curators_select_allowed_{status_name}"     # eg curators_select_allowed_workflow_status
        fkey.acl_bindings.update({
            # submitters can only selected workflow status that they are allowed: "File upload"
            # Note: Can't filter based on Entry_Related_File_Status column since submitters can't choose all those choices
            submitters_select_allowed: {
                "types": [ "insert", "update" ],
                "scope_acl": g["pdb-submitters"],
                "projection": [
                    { "filter": "Entry_Submitter_Select" if cfg.is_dev else "PDB_Submitter_Allow" , "operator": "=", "operand": "True"  },
                    "RID"
                ],
                "projection_type": "nonnull"
            },
        }) # end setting up fkey.acl_bindings
    # end for
    
    # -- Use default for the rest of fkeys
    #table.foreign_keys[(schema, "entry_Accession_Code_fkey")].acls = FKEY_ACLS["default"]
    #table.foreign_keys[(schema, "entry_Workflow_Status_fkey")].acls = FKEY_ACLS["default"]
    #table.foreign_keys[(schema, "entry_Owner_fkey")].acls = {}
    #table.foreign_keys[(schema, "entry_RCB_fkey")].acls = {}
    #table.foreign_keys[(schema, "entry_RMB_fkey")].acls = {}        


# -- ---------------------------------------------------------------------
'''
  Include all entry related tables have direct fkey to entry.id (no tables that link to entry through assocation).
  A subset of these tables with different policies will be set later in different functions.
  This approach will allow the acl to better adapt to model changes related to mmCIF.
'''
# Apply the entry access control on these tables 
def set_PDB_entry_related(model):
    schema = model.schemas["PDB"]
    entry_table = schema.tables["entry"]
    entry_related_tables = []

    # Create entry_related_tables: any table that has a fkey pointing to the entry_table through entry.id.
    # There might be a small subset of these tables that have their own policies. In that case,
    # the script will just clean the table policy before setting a new one. 
    for table in schema.tables.values():
        # == exclude system generated tables that linked to entry
        for fkey in table.foreign_keys:
            from_cols = {c.name for c in fkey.column_map.keys()}
            to_cols = {c.name for c in fkey.column_map.values()}
            pk_table = fkey.pk_table
            # == these are entry related tables
            if pk_table.name == "entry" and to_cols == {"id"} :
                # == set fkey policies
                fkey.acls.update({
                    "insert": g["entry-updaters"],
                    "update": g["entry-updaters"],
                })
                fkey.acl_bindings.update({
                    # submitter can only choose their own entries with certain Workflow Status
                    "submitters_modify_based_on_entry_workflow_status": {
                        "types": ["insert", "update"],
                        "scope_acl": g["pdb-submitters"],
                        "projection": [
                            {
                                "or": [
                                    { "filter": "Workflow_Status", "operator": "=", "operand": "DRAFT",  },
                                    { "filter": "Workflow_Status", "operator": "=", "operand": "DEPO", },
                                    { "filter": "Workflow_Status", "operator": "=", "operand": "RECORD READY", },
                                    { "filter": "Process_Status", "operator": "=", "operand": "Error: generating mmCIF file", },
                                    { "filter": "Process_Status", "operator": "=", "operand": "Error: processing uploaded mmCIF file", },
                                    { "filter": "Process_Status", "operator": "=", "operand": "Error: processing uploaded restraint files", }
                                ]
                            },
                            "RCB"
                        ],
                        "projection_type": "acl"
                    },
                })
                # == table policies if haven't already set. Might not need to check if there is only 1 fkey.
                if table in entry_related_tables:
                    print("    x existed: entry_related policies: %s" % (table.name,))                    
                    continue
                print("  - set_entry_related policies: %s" % (table.name,))
                entry_related_tables.append(table)
                # set acls: no acl is needed. use default policy
                table.acls.update({
                    "insert" : g["entry-creators"]
                })
                # submitters can reads their own entries and update according to its entry's workflow status (e.g. follow the fkey to entry table)        
                table.acl_bindings.update({
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
                                { "filter": "Workflow_Status", "operator": "=", "operand": "DRAFT"  },
                                { "filter": "Workflow_Status", "operator": "=", "operand": "DEPO" },
                                { "filter": "Workflow_Status", "operator": "=", "operand": "RECORD READY" },
                                { "filter": "Process_Status", "operator": "=", "operand": "Error: generating mmCIF file", },
                                { "filter": "Process_Status", "operator": "=", "operand": "Error: processing uploaded mmCIF file", },
                                { "filter": "Process_Status", "operator": "=", "operand": "Error: processing uploaded restraint files", }
                            ]},
                            "RCB",
                        ],
                        "projection_type": "acl",
                    }
                })
                #print(table.acl_bindings)
            # -- end fkey that point to entry
        # -- end fkey
    # -- end table

    
# -- ---------------------------------------------------------------------
# overwrite general entry_related policies
# Policy: these tables rely on content stored in uploaded mmCIF files and cannot be changed through UI
# check policy docs: https://docs.google.com/document/d/1M5NtfwvpIsw5thcBoj7KzrCkRhNlNS3pOD8L-TQrKEg/edit
def set_PDB_entry_coordinates_related(model):
    schema = model.schemas["PDB"]

    curator_edit_exclusions = ["entity_poly_seq", "struct_asym"]
    user_edit_exclusions = ["chem_comp", "entity_poly", "atom_type", "ihm_model_list"]
    
    # exclude submitter from editing these tables
    for tname in curator_edit_exclusions + user_edit_exclusions:
        table = schema.tables[tname]
        clear_table_acls(table) # clear policies
        # -- user_edit_exclusion: uses default schema/catalog policies.  
        # -- curator_edit_exclusion: take away curator write access. Only pdb-pipelines can modify
        if tname in curator_edit_exclusions:
            table.acls.update({
                "insert": g["pdb-pipelines"],
                "update": g["pdb-pipelines"],
                "delete": g["pdb-pipelines"],
            })
        
        # -- submitters can only read their own entries, no editing
        entry_fkey = None
        for fkey in table.foreign_keys:
            to_cols = {c.name for c in fkey.column_map.values()}
            if fkey.pk_table.name == "entry" and to_cols == {"id"} :
                entry_fkey = fkey
                break
        if entry_fkey:
            table.acl_bindings.update({
                "submitter_read_own_entries" : {
                    "types": ["select"],
                    "scope_acl": g["pdb-submitters"],
                    "projection": [{"outbound": ["PDB", entry_fkey.constraint_name ]}, "RCB"],
                    "projection_type": "acl"
                },
            })
        else:
            raise Exception("ERROR: %s do not have proper foreign keys to entry table" % (tname))
            
    # -- for

    
# -- ---------------------------------------------------------------------    
def set_PDB_Accession_Code(model):
    table = model.schemas["PDB"].tables["Accession_Code"]
    clear_table_acls(table)
    print("  - set_PDB_Accession_Code")
    
    # submitters can only read their entry Accession_Code
    table.acl_bindings.update({
        "submitters_read_own_entries": {
            "types": ["select"],
            "scope_acl": g["pdb-submitters"],
            "projection": [{"outbound": ["PDB", "Accession_Code_Entry_fkey"]}, "RCB"],
            "projection_type": "acl"
        }
    })
    
    cnames = ["Accession_Serial", "PDB_Extended_Code", "PDB_Code", "PDB_Accession_Code", "Notes"]
    for cname in cnames:
        col = table.columns[cname]
        col.acls.update(column_curator_enumerate_curator_read_curator_write)
        

# -- ---------------------------------------------------------------------
'''
  Policy: Submitters can't create and can only read entry created by submitters and if Submitter_Allow is True.
'''
def set_PDB_Curation_Log(model):
    if "Curation_Log" not in model.schemas["PDB"].tables:
        return
    
    schema = model.schemas["PDB"]
    table = schema.tables["Curation_Log"]
    clear_table_acls(table)

    # -- inherit catalog-level policy: e.g. Only entry-updaters can create/update.
    
    # -- find fkey to entry table
    for fkey in table.foreign_keys:
        if fkey.pk_table == schema.tables["entry"]:
            entry_fkey = fkey
    # this shouldn't happen
    if entry_fkey == None: 
        raise Exception("ERROR: PDB.Curation_Log do not have proper foreign keys to entry table")

    table.acl_bindings.update({
        "submitter_allow_and_own_entries": {
            "types": ["select"],
            "scope_acl": g["pdb-submitters"],
            "projection": [
                { "filter": "Submitter_Allow", "operator": "=", "operand": True},
                { "outbound": ["PDB", entry_fkey.constraint_name]},
                "RCB",
            ],
            "projection_type": "acl",
        }
    })

# -- ---------------------------------------------------------------------    
'''
  policy: pdb-ihm generated content, entry_updater can read, pdb_submitter can only read their own entry
'''
def set_PDB_entry_collection_related(model):
    schema = model.schemas["PDB"]
    collection_table = schema.tables["ihm_entry_collection"]
    mapping_table = schema.tables["ihm_entry_collection_mapping"]
    entry_table = schema.tables["entry"]    
    # -- clear table policies in case they were set by entry_related logic
    clear_table_acls(collection_table)
    clear_table_acls(mapping_table)
    
    entry_fkey = None
    collection_fkey = None
    
    # find 2 fkeys in mapping table
    for fkey in mapping_table.foreign_keys:
        pk_table = fkey.pk_table
        if pk_table == entry_table:
            entry_fkey = fkey
        if pk_table == collection_table:
            collection_fkey = fkey

    # this shouldn't happen
    if entry_fkey == None or collection_fkey == None:
        raise Exception("ERROR: ihm_entry_collection_mapping do not have proper foreign keys to entry and/or collection table")

    # == set policy on ihm_entry_collection table
    # -- acl: adopt schema level for acls e.g. only entry-updaters can read/write
    # -- acl_bindings: pdb_submitters can only see their entries
    collection_table.acl_bindings.update({
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
    })
        
    # == set policies for the mapping table: only curator can set up mapping table at any time
    # -- acl: adopts schema policy
    # -- acl_bindings: pdb_submitters can only see their entries
    mapping_table.acl_bindings.update({
        "submitter_read_own_entries" : {
            "types": ["select"],
            "scope_acl": g["pdb-submitters"],
            "projection": [ {"outbound": ["PDB", entry_fkey.constraint_name ]}, "RCB" ],
            "projection_type": "acl"
        }
    })
    
# -- ---------------------------------------------------------------------
'''
  policy: pdb-ihm generated content, entry_updater can read, pdb_submitter can only read their own entry
'''
def set_PDB_entry_related_error_file_tables(model):
    schema = model.schemas["PDB"]
    for tname in ["Entry_Error_File"]:
        print("  - set_entry_related_error_file_table: %s" % (tname,))        
        table = schema.tables[tname]
        clear_table_acls(table) 
        
        # == table policy
        # -- acl: only pdb-ihm can manipulate, entry-updaters can read (from schema acl)
        table.acls.update({
            "insert": g["pdb-pipelines"],
            "update": g["pdb-pipelines"],
            "delete": g["pdb-pipelines"],
        })
        # -- acl_bindings: submitters can read if it is linked to their entries (need to traverse fkey to entry)
        for fkey in table.foreign_keys:
            from_cols = {c.name for c in fkey.column_map.keys()}
            pk_table = fkey.pk_table
            if pk_table.name == "entry":  
                table.acl_bindings.update({
                    "submitter_read_own_entries" : {
                        "types": ["select"],
                        "scope_acl": g["pdb-submitters"],
                        "projection": [{"outbound": ["PDB", fkey.constraint_name ]}, "RCB"],
                        "projection_type": "acl"
                    }
                })
            # -- if the fkey to entry
        # -- end fkey
    # -- end tname
    
# -- ---------------------------------------------------------------------
'''
  policy: pdb-ihm generated content, entry_updater can read, pdb_submitter can only read their own entry.
  TODO: use entry_table.referenced_by:
'''
def set_PDB_entry_related_system_generated_tables(model):
    schema = model.schemas["PDB"]
    for tname in ["Entry_Generated_File"]:
        print("  - set_entry_related_system_generated_table: %s" % (tname,))        
        table = schema.tables[tname]
        clear_table_acls(table) 
        
        # == table policy
        # -- acl: only pdb-ihm can manipulate, entry-updaters can read and manipulate (from schema acl)
        table.acls.update({
            "insert": g["pdb-pipelines"] + g["entry-updaters"],
            "update": g["pdb-pipelines"] + g["entry-updaters"],
            "delete": g["pdb-pipelines"] + g["entry-updaters"],
        })
        # -- acl_bindings: submitters can read if it is linked to their entries (need to traverse fkey to entry)
        for fkey in table.foreign_keys:
            from_cols = {c.name for c in fkey.column_map.keys()}
            pk_table = fkey.pk_table
            if pk_table.name == "entry":
                # -- extend existing policy to filter certain file types
                table.acl_bindings.update({
                    "submitter_read_own_entries" : {
                        "types": ["select"],
                        "scope_acl": g["pdb-submitters"],
                        "projection": [
                            {
                                "or": [
                                    { "filter": "File_Type", "operator": "=", "operand": "mmCIF",  },
                                    { "filter": "File_Type", "operator": "=", "operand": "Validation: Full PDF", },
                                    { "filter": "File_Type", "operator": "=", "operand": "Validation: Summary PDF", }
                                ]
                            },
                            {"outbound": ["PDB", fkey.constraint_name ]}, 
                            "RCB"
                        ],
                        "projection_type": "acl"
                    }
                })
            # -- if the fkey to entry
        # -- end fkey
    # -- end tname
    
# -- ---------------------------------------------------------------------
# Data_Dictionary, Supported_Dictionary: only updater can read and do anything, submmitter can't read
# IHM_New_Chem_Comp: submitters can't read
def set_tables_curators_access_only(model):
    """
    Set ACLs for tables that only curators can access.
    """
    schema = model.schemas["PDB"]
    for table_name in ["Supported_Dictionary", "audit_conform", "IHM_New_Chem_Comp"]:
        if table_name not in schema.tables.keys(): continue
        print("  - set_tables_curators_access_only: %s" % (table_name))
        table = schema.tables[table_name]
        clear_table_acls(table)                
        # use default schema ACLs (only entry-updaters can do anything to these tables)

    
# -- ---------------------------------------------------------------------
# "Data_Dictionary" and "Conform_Dictionary" are needed for users to see Conform Dict associated with
# generated mmCIF files

def set_tables_submitters_read(model):
    """
    Set ACLs for tables that allow submitters to read the content (similar to vocab tables)
    """
    schema = model.schemas["PDB"]
    for table_name in ["Conform_Dictionary", "Data_Dictionary"]:
        if table_name not in schema.tables.keys(): continue
        print("  - set_tables_submitters_read: %s" % (table_name))
        table = schema.tables[table_name]
        clear_table_acls(table)
        table.acls.update({
            "select": g["entry-creators"],
        })


# -- ---------------------------------------------------------------------
# Added on additional fkey policies in Entry_Related_File.
# Do not clear the table since the rest of the policies are set in set_PDB_entry_related()
def set_PDB_Entry_Related_File(model):
    schema = model.schemas["PDB"]
    table = schema.tables["Entry_Related_File"]

    # == table acl and entry_fkey are set in set_pdb_entry_related()

    # == column acl
    
    # -- ACL: submiters can create but not edit
    cnames = ["Restraint_Process_Status"]
    for cname in cnames:
        col = table.columns[cname]
        col.acls.update({
            "update": g["entry-updaters"],
        })
        col.acl_bindings.update({
            "submitters_modify_based_on_workflow_status": False,
        })

    # == update restraint_workflow_status fkey
    # ACL details is controlled through database columns Submitter_Select and Entry_Related_File_Status in
    # the Vocab.Workflow_Status and Vocab.Processing_Status
    status_related_fkeys = {
        "workflow_status": "Entry_Related_File_Restraint_Workflow_Status_fkey",
        "process_status": "Entry_Related_File_Restraint_Process_Status_fkey"
    }
    for status_name, constraint_name in status_related_fkeys.items():
        fkey = table.foreign_keys[(schema, constraint_name)]
        fkey.acls.update({
            "insert": [],
            "update": [],
        })
        # set acl_binding policy name
        submitters_select_allowed = f"submitters_select_allowed_{status_name}" # eg submitters_select_allowed_workflow_status
        curators_select_allowed = f"curators_select_allowed_{status_name}"     # eg curators_select_allowed_workflow_status
        fkey.acl_bindings.update({
            # submitters can only selected workflow status that they are allowed: "File upload"
            # Note: Can't filter based on Entry_Related_File_Status column since submitters can't choose all those choices
            submitters_select_allowed: {
                "types": [ "insert", "update" ],
                "scope_acl": g["pdb-submitters"],
                "projection": [
                    { "filter": "Restraint_Submitter_Select", "operator": "=", "operand": True, },
                    "RID"
                ],
                "projection_type": "nonnull"
            },
            curators_select_allowed: {
                "types": [ "insert", "update" ],
                "scope_acl": g["entry-updaters"],
                "projection": [
                    { "filter": "Restraint_Status", "operator": "=", "operand": True, },
                    "RID"
                ],
                "projection_type": "nonnull"
            }
        }) # end setting up fkey.acl_bindings
    # end for

    
    #print("set_PDB_entry_Related_Fiie: acl:%s --- acl_bindings:%s" % (fkey.acls, fkey.acl_bindings))    

# -- ---------------------------------------------------------------------
# submitters can always read
#
def set_PDB_Entry_Related_File_Templates(model):
    for tname in ["Entry_Related_File_Templates"]:
        print("  - set PDB_Entry_Related_File_Templates: %s" % (tname,))        
        table = model.schemas["PDB"].tables[tname]
        clear_table_acls(table)

        # allow entry-creators to read        
        table.acls.update({
            "select": g["entry-creators"],            
        })

# -- ---------------------------------------------------------------------
# 
def set_ermrest_acl(catalog):
    initialize_policies(catalog)    
    model = catalog.getCatalogModel()

    if False:
        print_acls(model, ["PDB"])
        #clear_table_acls(model.schemas["PDB"].tables["Entry_Related_File_Templates"])        
        set_PDB_Entry_Related_File_Templates(model)
        print_table_acls(model.schemas["PDB"].tables["Entry_Related_File_Templates"])
        
    model.clear(clear_comment=False, clear_annotations=False, clear_acls=True, clear_acl_bindings=True)

    # -- catalog
    model.acls.update(ermrest_catalog_acls)
    # -- schemas
    set_PDB_acl(model)
    set_Vocab_acl(model)        
    set_public_acl(model)
    set_WWW_acl(model)
    # -- apply 
    model.apply()

# -- =================================================================================
        
def main(server_name, catalog_id, credentials):
    server = DerivaServer("https", server_name, credentials)
    catalog = server.connect_ermrest(catalog_id)
    catalog.dcctx["cid"] = DCCTX["acl"]
    #store = HatracStore("https", server_name, credentials)

    set_ermrest_acl(catalog)
    
# -- =================================================================================
# Install the Python package:
#    From the protein-database directory, run: 
#        pip3 install --upgrade --no-deps .
#
# Running the script:
#    python3 -m pdb_dev.config.acl.ermrest_acl --host dev.pdb-dev.org --catalog-id 99 
#
if __name__ == "__main__":
    args = PDBDEV_CLI(DCCTX["acl"], None, 1).parse_cli()
    credentials = get_credential(args.host, args.credential_file)
    #print("credential: %s" % (credentials))
    main(args.host, args.catalog_id, credentials)

