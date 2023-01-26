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
    "pdb-admins" = ["https://auth.globus.org/0b98092c-3c41-11e9-a8c8-0ee7d80087ee"],
    "pdb-curators" = ["https://auth.globus.org/eef3e02a-3c40-11e9-9276-0edc9bdd56a6"],
    "pdb-writers" = ["https://auth.globus.org/c94a1e5c-3c40-11e9-a5d1-0aacc65bfe9a"],
    "pdb-submitters" = ["https://auth.globus.org/99da042e-64a6-11ea-ad5f-0ef992ed7ca1"]
    "isrd-staff": ["https://auth.globus.org/176baec4-ed26-11e5-8e88-22000ab4b42b"],    
    "isrd-systems": ["https://auth.globus.org/3938e0d0-ed35-11e5-8641-22000ab4b42b"],
    "isrd-testers": ["https://auth.globus.org/9d596ac6-22b9-11e6-b519-22000aef184d"],
}
g = groups
groups["owners"] = g["isrd-systems"] + g["pdb-admins"] 
groups["pdb-all"] = g["pdb-admins"] + g["pdb-submitters"] + g["pdb-curators"]
groups["pdb-updaters"] = g["pdb-admins"] + g["pdb-curators"]
groups["isrd-updaters"] = g["isrd-systems"] + g["isrd-staff"]
groups["isrd-all"] = g["isrd-systems"] + g["isrd-staff"] + g["isrd-testers"]
groups["pdb-entry-creators"] = g["pdb-admins"] + g["pdb-curators"] + g["pdb-submitters"]
groups["entry_creators"] = g["pdb-entry-creators"] + g["isrd-updaters"],
groups["entry_updaters"] = g["pdb-admins"] + g["pdb-curators"] + g["isrd-updaters"]

ermrest_catalog_acl = {
    "owner" : g["owners"]
    "enumerate": g["public"], # g["pdb-all"] + g["isrd-all"] 
    "select": g["entry_updaters"],
    "insert": g["entry_creators"],
    "update": g["entry_updaters"],
    "delete": g["entry_updaters"],
}

# -- ---------------------------------------------------------------------
def set_PDB_acl(model):
    schema = model.schemas["PDB"]
    

# -- ---------------------------------------------------------------------
def set_PDB_entry_acl(model):
    table = model.tables["PDB"]

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
        "submitters_modify_based_on_workflow_status": false        
        "submitters_read_based_on_workflow_status": {
            "types": [ "select" ],
            "scope_acl": g["pdb-submitters"]
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
        "submitters_modify_based_on_workflow_status": false
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
        "insert": g["entry_updaters"]
        "update": g["entry_updaters"]
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
def set_ermrest_acl(catalog):
    model = catalog.getCatalogModel()
    
    model.acls.update(ermrest_catalog_acl)
    set_PDB_entry_acl(catalog)


# -- =================================================================================
        
def main(server_name, catalog_id, credentials):
    server = DerivaServer('https', server_name, credentials)
    catalog = server.connect_ermrest(catalog_id)
    catalog.dcctx['cid'] = "config/acl"
    store = HatracStore('https', server_name, credentials)

    set_smite_acl(catalog, store)
    
# -- =================================================================================

if __name__ == '__main__':
    args = SmiteCLI("config/acl", None, 1).parse_cli()
    credentials = get_credential(args.host, args.credential_file)
    main(args.host, args.catalog_id, credentials)

