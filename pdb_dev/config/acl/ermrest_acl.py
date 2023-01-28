#!/usr/bin/python

import sys
import json
from deriva.core import ErmrestCatalog, AttrDict, get_credential, DEFAULT_CREDENTIAL_FILE, tag, urlquote, DerivaServer, get_credential, BaseCLI
from deriva.core.ermrest_model import builtin_types, Schema, Table, Column, Key, ForeignKey
from deriva.core import urlquote, urlunquote
from deriva.core import HatracStore
import requests.exceptions

groups = {
    "public" : ["*"],
    "pdb-admins" : ["https://auth.globus.org/0b98092c-3c41-11e9-a8c8-0ee7d80087ee"],
    "pdb-curators" : ["https://auth.globus.org/eef3e02a-3c40-11e9-9276-0edc9bdd56a6"],
    "pdb-submitters" : ["https://auth.globus.org/99da042e-64a6-11ea-ad5f-0ef992ed7ca1"],
    "pdb-writers" : ["https://auth.globus.org/c94a1e5c-3c40-11e9-a5d1-0aacc65bfe9a"],  # inactive    
    "pdb-readers" : ["https://auth.globus.org/8875a770-3c40-11e9-a8c8-0ee7d80087ee"],  # inactive
    "isrd-staff": ["https://auth.globus.org/176baec4-ed26-11e5-8e88-22000ab4b42b"],    
    "isrd-systems": ["https://auth.globus.org/3938e0d0-ed35-11e5-8641-22000ab4b42b"],
    "isrd-testers": ["https://auth.globus.org/9d596ac6-22b9-11e6-b519-22000aef184d"],
}
g = groups
groups["owners"] = g["isrd-systems"] + g["pdb-admins"] 
groups["pdb-all"] = g["pdb-admins"] + g["pdb-submitters"] + g["pdb-curators"]
groups["isrd-all"] = g["isrd-systems"] + g["isrd-staff"] + g["isrd-testers"]
# -- remove admins from the these groups, so the policy is easier to read, as owners can do anything already
groups["entry_creators"] = g["pdb-submitters"] + g["pdb-curators"] + g["isrd-staff"],
groups["entry_updaters"] = g["pdb-curators"] + g["isrd-staff"]

ermrest_catalog_acl = {
    "owner" : g["owners"],
    "enumerate": g["public"], 
    "select": g["entry_updaters"],
    "insert": g["entry_updaters"],
    "update": g["entry_updaters"],
    "delete": g["entry_updaters"],
}


fkey_acls : {
    "default": { "insert": ["*"], "update": ["*"] },
    "RCBRMB": None,
}

fkey_acl_bindings = {
    # submitter can only choose entries with certain Workflow Status
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
            "RID"
        ],
        "projection_type": "notnull"
    },
    # set Owner group only if user is a member of the group
    "set_owner_old": {
        'types': ['update', 'insert'],
        'scope_acl': ['*'], 
        'projection': ['ID'],
        'projection_type': 'acl'
    }
    
}

# -- ---------------------------------------------------------------------
def clear_Owner_fkeys(model):
    for schema in model.schemas.values():
        if schema.name in ["public", "WWW", "Vocab"]:
            continue
        for table in schema.tables.values():
            print("--- %s:%s ---" % (schema.name, table.name))
            if table.acls  == {
                    'owner': ['https://auth.globus.org/0b98092c-3c41-11e9-a8c8-0ee7d80087ee', 'https://auth.globus.org/176baec4-ed26-11e5-8e88-22000ab4b42b'],
                    'write': [],
                    'delete': ['https://auth.globus.org/eef3e02a-3c40-11e9-9276-0edc9bdd56a6'],
                    'insert': ['https://auth.globus.org/eef3e02a-3c40-11e9-9276-0edc9bdd56a6', 'https://auth.globus.org/c94a1e5c-3c40-11e9-a5d1-0aacc65bfe9a', 'https://auth.globus.org/99da042e-64a6-11ea-ad5f-0ef992ed7ca1'],
                    'select': ['https://auth.globus.org/c94a1e5c-3c40-11e9-a5d1-0aacc65bfe9a', 'https://auth.globus.org/8875a770-3c40-11e9-a8c8-0ee7d80087ee'],
                    'update': ['https://auth.globus.org/eef3e02a-3c40-11e9-9276-0edc9bdd56a6'],
                    'enumerate': ['*']
            }:
                print("     DEFAULT TABLE ACL 1")
                continue
            if table.acls == {
                    'delete': ['https://auth.globus.org/0b98092c-3c41-11e9-a8c8-0ee7d80087ee', 'https://auth.globus.org/176baec4-ed26-11e5-8e88-22000ab4b42b', 'https://auth.globus.org/eef3e02a-3c40-11e9-9276-0edc9bdd56a6'],
                    'insert': ['https://auth.globus.org/0b98092c-3c41-11e9-a8c8-0ee7d80087ee', 'https://auth.globus.org/176baec4-ed26-11e5-8e88-22000ab4b42b', 'https://auth.globus.org/eef3e02a-3c40-11e9-9276-0edc9bdd56a6'],
                    'select': ['*'],
                    'update': ['https://auth.globus.org/0b98092c-3c41-11e9-a8c8-0ee7d80087ee', 'https://auth.globus.org/176baec4-ed26-11e5-8e88-22000ab4b42b', 'https://auth.globus.org/eef3e02a-3c40-11e9-9276-0edc9bdd56a6'],
                    'enumerate': ['*'],
            }:
                print("     DEFAULT TABLE ACL 2")
                continue
            if table.acls == {
                    'delete': ['https://auth.globus.org/0b98092c-3c41-11e9-a8c8-0ee7d80087ee', 'https://auth.globus.org/176baec4-ed26-11e5-8e88-22000ab4b42b', 'https://auth.globus.org/eef3e02a-3c40-11e9-9276-0edc9bdd56a6'],
                    'insert': ['https://auth.globus.org/0b98092c-3c41-11e9-a8c8-0ee7d80087ee', 'https://auth.globus.org/eef3e02a-3c40-11e9-9276-0edc9bdd56a6', 'https://auth.globus.org/176baec4-ed26-11e5-8e88-22000ab4b42b'],
                    'select': ['https://auth.globus.org/0b98092c-3c41-11e9-a8c8-0ee7d80087ee', 'https://auth.globus.org/eef3e02a-3c40-11e9-9276-0edc9bdd56a6', 'https://auth.globus.org/176baec4-ed26-11e5-8e88-22000ab4b42b'],
                    'update': ['https://auth.globus.org/0b98092c-3c41-11e9-a8c8-0ee7d80087ee', 'https://auth.globus.org/eef3e02a-3c40-11e9-9276-0edc9bdd56a6', 'https://auth.globus.org/176baec4-ed26-11e5-8e88-22000ab4b42b'],
                    'enumerate': ['*']
            }:
                print("     DEFAULT TABLE ACL 3")
                continue
            if not table.acls:
                print("     DEFAULT TABLE ACL 4: NO ACLS")
                continue                

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

            if table.acls or table.acl_bindings:
                print(" t: %s acls: %s acl_bindings: %s" % (table.name, table.acls, table.acl_bindings))
            for fkey in table.foreign_keys:
                from_cols = {c.name for c in fkey.column_map.keys()}
                to_cols = {c.name for c in fkey.column_map.values()}
                if from_cols == {"Owner"}:
                    #print("     OWNER: fk %s (%s) acls: %s, acl_bindings: %s" % (fkey.constraint_name, from_cols, fkey.acls, fkey.acl_bindings))
                    continue
                if from_cols == {"RCB"} or from_cols == {"RMB"}:
                    # current policy: acls: {}, acl_bindings: {}                    
                    continue
                if from_cols == {"Entry_Related_File"}:
                    # current policy: acls: {}, acl_bindings: {} and sometimes with default acls
                    #print("     ENTRY_RELATED_FILE: fk %s (%s) acls: %s, acl_bindings: %s" % (fkey.constraint_name, from_cols, fkey.acls, fkey.acl_bindings))                    
                    continue
                if fkey.acls == {"insert": ["*"], "update": ["*"]} and not fkey.acl_bindings:
                    #print("     DEFAULT: fk %s (%s) acls: %s, acl_bindings: %s" % (fkey.constraint_name, from_cols, fkey.acls, fkey.acl_bindings))
                    continue  
                # if (from_cols == {"structure_id"} or from_cols == {"entry_id"}) or \                
                if fkey.pk_table.name == "entry" and to_cols == {"id"} and fkey.acl_bindings == {
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
                print("    -- fk %s:%s (%s->%s:%s) acls: %s, acl_bindings: %s" % (table.name, fkey.constraint_name, from_cols, fkey.pk_table.name, to_cols, fkey.acls, fkey.acl_bindings))

                #if fkey.acls or fkey.acl_bindings:
                #    print("non-empty")
        continue
                #if fkey.acl_bi
                #fkey.acls = { "insert": "*", "update": "*" }
                #fkey.acl_bindings = None
    
# -- ---------------------------------------------------------------------
def set_PDB_acl(model):
    schema = model.schemas["PDB"]

    # allowing entry creators to create anything in the PDB schema
    schema.acls = {
        "insert": g["entry_creators"],        
    }

    # clear up the Owner foreng keys

    
    # give entry_creator insert rights
    

# -- ---------------------------------------------------------------------
def set_Vocab_acl(model):
    schema = model.schemas["Vocab"]

    # Anyone can read. The rest follows catalog policy
    schema.acls = {
        "select": g["entry_creators"],
    }
    
# -- ---------------------------------------------------------------------
def set_PDB_entry_acl(model):
    table = model.tables["PDB"]

    # clear all the existing ACL associated with the table
    table.clear(clear_comment=False, clear_annotations=False, clear_acls=True, clear_acl_bindings=True)
    
    # ==== table-level =====    
    # Submitter can create but can only see their own entries. They can't delete entries during a certain workflow status.
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
        "submitters_read_own_entries": false,
        "submitters_modify_based_on_workflow_status": false,
        "submitters_read_based_on_workflow_status": {
            "types": [ "select" ],
            "scope_acl": g["pdb-submitters"],
            "projection": [
                {
                    "or": [
                        { "filter": "Workflow_Status", "operand": "REL" },
                        { "filter": "Workflow_Status", "operand": "HOLD" },
                    ]
                },
                "RID"
            ],
            "projection_type": "nonnull"
        },
    }

    # -- Release date: submitters can only see when the entry is HOLD or REL
    table.columns["Release_Date"].acls = {
        "select": g["entry_updaters"],        
    }
    table.columns["Release_Date"].acl_bindings = {
        "submitters_read_own_entries": false,
        "submitters_modify_based_on_workflow_status": false,
        "submitters_read_based_on_workflow_status": {
            "types": [ "select" ],
            "scope_acl": g["pdb-submitters"],
            "projection": [
                {
                    "or": [
                        { "filter": "Workflow_Status", "operand": "REL" },
                        { "filter": "Workflow_Status", "operand": "HOLD" },
                    ]
                },
                "RID"
            ],
            "projection_type": "nonnull"
        },
    }
    
    # -- Deposit date
    table.columns["Deposit_Date"].acls = {    
        "select": g["entry_creators"],        
        "insert": g["entry_updaters"],
    }

    # -- Notes: non-submitters can create
    table.columns["Notes"].acls = {            
        "select": g["entry_updaters"],        
        "insert": g["entry_updaters"],
      },


    # ==== foreign keys =====
    schema = model.schemas["PDB"]

    # -- Workflow Status: submitters can only choose Workflow_Status that they are allowed
    table.foreign_key[(schema, "entry_Workflow_Status_fkey")].acls = { 
        "insert": g["entry_updaters"],
        "update": g["entry_updaters"],
    }
    table.foreign_key[(schema, "entry_Workflow_Status_fkey")].acl_bindings = {     
        "submitters_modify_based_on_workflow_status": {
            "types": [ "insert", "update" ],
            "scope_acl": g["pdb-submitters"],
            "projection": [
                { "filter": "PDB_Submitter_Allow", "operator": "=", "operand": "True",  },
                "RID"
            ],
            "projection_type": "nonnull"
        }
    },

    # -- the rest of fkeys
    table.foreign_key[(schema, "entry_Accession_Code_fkey")].acls = { "insert": "*", "update": "*",}
    table.foreign_key[(schema, "entry_Workflow_Status_fkey")].acls = { "insert": "*", "update": "*",}
    # -- Owner fkey: the column is blank. Use default    
    table.foreign_key[(schema, "entry_Owner_fkey")].acls = {}
    # -- RCB, RMB fkeys: system generated. No need to set policy    
    table.foreign_key[(schema, "entry_RCB_fkey")].acls = {}
    table.foreign_key[(schema, "entry_RMB_fkey")].acls = {}        


# -- ---------------------------------------------------------------------
def set_PDB_Accession_Code(model):
    table = model.schenas["PDB"].tables["Accession_Code"]

    # inherit table-leavel ACL
    table.acls = None
    
    # submitters can only read their entry Accession_Code
    table.acl_bindings = {
        "submitters_read_own_entries": {
            'types': ['select'],
            'scope_acl': g["pdb-submitters"],
            'projection': [{'outbound': ['PDB', 'Accession_Code_Entry_fkey']}, 'RCB'],
            'projection_type': 'acl'
        }
    }

# -- ---------------------------------------------------------------------
# set the same policies for Data_Dictionary and Supported_Dictionary
def set_PDB_Data_Dictionary_Related(model):
    for table_name in ["Data_Dictionary", "Supported_Dictionary"]:
        table = model.schenas["PDB"].tables[table_name]
    
        # allow all to read
        table.acls = {
            'select': ['entry_creators'],
        }
    
        table.acl_bindings = None

# -- ---------------------------------------------------------------------
def set_ermrest_acl(catalog):
    model = catalog.getCatalogModel()

    #response = catalog.get("/schema")
    #schema = response.json()
    #print(json.dumps(schema, indent=2))
    
    clear_Owner_fkeys(model)
    
    #model.acls.update(ermrest_catalog_acl)
    #set_PDB_acl(model)
    #set_PDB_entry_acl(model)
    #set_PDB_Accession_Code(model)
    #set_PDB_Data_Dictionary_Related(model)
    #model.apply()

# -- =================================================================================
        
def main(server_name, catalog_id, credentials):
    server = DerivaServer('https', server_name, credentials)
    catalog = server.connect_ermrest(catalog_id)
    catalog.dcctx['cid'] = "config/acl"
    #store = HatracStore('https', server_name, credentials)

    set_ermrest_acl(catalog)
    
# -- =================================================================================

if __name__ == '__main__':
    cli = BaseCLI("config/acl", None, 1)
    cli.parser.add_argument('--catalog_id', metavar='<id>', help="Deriva catalog ID (default=1)", default=1, required=True)
    args = cli.parse_cli()    
    credentials = get_credential(args.host, args.credential_file)

    main(args.host, args.catalog_id, credentials)

