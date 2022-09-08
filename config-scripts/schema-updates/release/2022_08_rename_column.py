import sys
import json
from deriva.core import ErmrestCatalog, AttrDict, get_credential, DEFAULT_CREDENTIAL_FILE, tag, urlquote, DerivaServer, get_credential, BaseCLI
from deriva.core.ermrest_model import builtin_types, Schema, Table, Column, Key, ForeignKey, DomainType, ArrayType
import utils
from utils import ApplicationClient

# ========================================================

# ============================================================

acl_bindings = {
  "released_reader": {
    "types": [
      "select"
    ],
    "scope_acl": [
      "https://auth.globus.org/99da042e-64a6-11ea-ad5f-0ef992ed7ca1"
    ],
    "projection": [
      "RCB"
    ],
    "projection_type": "acl"
  },
  "self_service_creator": {
    "types": [
      "update",
      "delete"
    ],
    "scope_acl": [
      "https://auth.globus.org/99da042e-64a6-11ea-ad5f-0ef992ed7ca1"
    ],
    "projection": [
      {
        "or": [
          {
            "filter": "Restraint_Workflow_Status",
            "operand": "DRAFT",
            "operator": "="
          },
          {
            "filter": "Restraint_Workflow_Status",
            "operand": "DEPO",
            "operator": "="
          },
          {
            "filter": "Restraint_Workflow_Status",
            "operand": "RECORD READY",
            "operator": "="
          },
          {
            "filter": "Restraint_Workflow_Status",
            "operand": "ERROR",
            "operator": "="
          }
        ]
      },
      "RCB"
    ],
    "projection_type": "acl"
  }
}

def main(server_name, catalog_id, credentials):
    server = DerivaServer('https', server_name, credentials)
    catalog = server.connect_ermrest(catalog_id)
    catalog.dcctx['cid'] = 'oneoff/model'
    model = catalog.getCatalogModel()

    utils.drop_fkey_if_exist(model, 'PDB', 'Entry_Related_File', 'Entry_Related_File_Process_Status_fkey')
    utils.drop_fkey_if_exist(model, 'PDB', 'Entry_Related_File', 'Entry_Related_File_Workflow_Status_fkey')

    utils.rename_column_if_exists(model, 'PDB', 'Entry_Related_File', 'Process_Status', 'Restraint_Process_Status')
    utils.rename_column_if_exists(model, 'PDB', 'Entry_Related_File', 'Workflow_Status', 'Restraint_Workflow_Status')
    
    model = catalog.getCatalogModel()
    utils.create_foreign_key_if_not_exists(model, 'PDB', 'Entry_Related_File', 'Entry_Related_File_Restraint_Process_Status_fkey', 
                                            ForeignKey.define(['Restraint_Process_Status'], 'Vocab', 'Process_Status', ['Name'],
                                                                                            constraint_names=[ ['PDB', 'Entry_Related_File_Restraint_Process_Status_fkey'] ],
                                                                                            on_update='CASCADE',
                                                                                            on_delete='SET NULL')
                                                )
    model = catalog.getCatalogModel()
    utils.create_foreign_key_if_not_exists(model, 'PDB', 'Entry_Related_File', 'Entry_Related_File_Restraint_Workflow_Status_fkey', 
                                            ForeignKey.define(['Restraint_Workflow_Status'], 'Vocab', 'Workflow_Status', ['Name'],
                                                                                            constraint_names=[ ['PDB', 'Entry_Related_File_Restraint_Workflow_Status_fkey'] ],
                                                                                            on_update='CASCADE',
                                                                                            on_delete='SET NULL')
                                                )
    utils.set_table_acl_bindings(catalog, 'PDB', 'Entry_Related_File', acl_bindings)

# ===================================================    

if __name__ == '__main__':
    args = ApplicationClient('ad-hoc table creation tool', None, 1).parse_cli()
    credentials = get_credential(args.host, args.credential_file)
    main(args.host, args.catalog_id, credentials)
