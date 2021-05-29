import sys
import json
from deriva.core import get_credential, DerivaServer, BaseCLI
from deriva.core.ermrest_model import Key

# Fix the following simple key inssues
# 1. entry: rename entry_id_unique_key to entry_id_primary_key 
# 2. struct: add struct_primary_key: [entry_id]
# 3. pdbx_entry_detail:
#  3.1. delete structure_id column and its fkey to entry table
#  3.2. create pdbx_entry_details_primary_key: [entry_id]

pdbx_entry_details_acl_binding = {
  "released_reader": {
    "types": [
      "select"
    ],
    "scope_acl": [
      "https://auth.globus.org/99da042e-64a6-11ea-ad5f-0ef992ed7ca1"
    ],
    "projection": [
      {
        "outbound": [
          "PDB",
          "pdbx_entry_details_entry_id_fkey"
        ]
      },
      "RCB"
    ],
    "projection_type": "acl"
  },
  "self_service_group": {
    "types": [
      "update",
      "delete"
    ],
    "scope_acl": [
      "*"
    ],
    "projection": [
      "Owner"
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
        "outbound": [
          "PDB",
          "pdbx_entry_details_entry_id_fkey"
        ]
      },
      {
        "or": [
          {
            "filter": "Workflow_Status",
            "operand": "DRAFT",
            "operator": "="
          },
          {
            "filter": "Workflow_Status",
            "operand": "DEPO",
            "operator": "="
          },
          {
            "filter": "Workflow_Status",
            "operand": "RECORD READY",
            "operator": "="
          },
          {
            "filter": "Workflow_Status",
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


def set_acl_binding(catalog, schema_name, table_name, acl_binding):
    model = catalog.getCatalogModel()
    schema = model.schemas[schema_name]
    table = model.schemas[schema_name].tables[table_name]
    table.acl_bindings = acl_binding
    model.apply()
    print('Set acl_bindings to {}:{}'.format(schema_name, table_name))

def drop_column(catalog, schema_name, table_name, column_name):
    model = catalog.getCatalogModel()
    schema = model.schemas[schema_name]
    table = model.schemas[schema_name].tables[table_name]
    column = table.column_definitions[column_name]
    column.drop()
    print('Dropped in {}:{} table the column {}'.format(schema_name, table_name, column_name))

def drop_fk(catalog, schema_name, table_name, constraint_name):
    model = catalog.getCatalogModel()
    schema = model.schemas[schema_name]
    table = model.schemas[schema_name].tables[table_name]
    fk = table.foreign_keys.__getitem__((schema, constraint_name))
    fk.drop()
    print('Dropped in {}:{} table the foreign key {}'.format(schema_name, table_name, constraint_name))

def create_pk(catalog, schema_name, table_name, columns, constraint_name):
    model = catalog.getCatalogModel()
    schema = model.schemas[schema_name]
    table = model.schemas[schema_name].tables[table_name]
    pkey_def = Key.define(columns, constraint_names=[ [schema_name, constraint_name] ])
    table.create_key(pkey_def)
    print('Created in {}:{} table the primary key {}'.format(schema_name, table_name, constraint_name))

def rename_pk(catalog, schema_name, table_name, old_name, new_name):
    model = catalog.getCatalogModel()
    schema = model.schemas[schema_name]
    table = model.schemas[schema_name].tables[table_name]
    pk = table.keys.__getitem__((schema, old_name))
    pk.alter(constraint_name=new_name)
    print('Renamed in {}:{} table the primary key {} to {}'.format(schema_name, table_name, old_name, new_name))

def main(server_name, catalog_id, credentials):
    server = DerivaServer('https', server_name, credentials)
    catalog = server.connect_ermrest(catalog_id)
    catalog.dcctx['cid'] = "oneoff/model"

    rename_pk(catalog, 'PDB', 'entry', 'entry_id_unique_key', 'entry_id_primary_key')
    create_pk(catalog, 'PDB', 'struct', ['entry_id'], 'struct_primary_key')
    drop_fk(catalog, 'PDB', 'pdbx_entry_details', 'pdbx_entry_details_structure_id_fkey')
    drop_column(catalog, 'PDB', 'pdbx_entry_details', 'structure_id')
    create_pk(catalog, 'PDB', 'pdbx_entry_details', ['entry_id'], 'pdbx_entry_details_primary_key')
    set_acl_binding(catalog, 'PDB', 'pdbx_entry_details', pdbx_entry_details_acl_binding)

if __name__ == '__main__':
    args = BaseCLI("ad-hoc table creation tool", None, 1).parse_cli()
    credentials = get_credential(args.host, args.credential_file)

    main(args.host, 99, credentials)
    
