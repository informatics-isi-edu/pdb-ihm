import sys
import json
from ast import literal_eval
from deriva.core import get_credential, DerivaServer

groups = {
 "https://auth.globus.org/0b98092c-3c41-11e9-a8c8-0ee7d80087ee": "pdb_admin",
 "https://auth.globus.org/176baec4-ed26-11e5-8e88-22000ab4b42b": "isrd_staff",
 "https://auth.globus.org/eef3e02a-3c40-11e9-9276-0edc9bdd56a6": "pdb_curator",
 "https://auth.globus.org/c94a1e5c-3c40-11e9-a5d1-0aacc65bfe9a": "pdb_writer",
 "https://auth.globus.org/99da042e-64a6-11ea-ad5f-0ef992ed7ca1": "pdb_submitter",
 "https://auth.globus.org/8875a770-3c40-11e9-a8c8-0ee7d80087ee": "pdb_reader"
}

def replace_group(object):
    object_string = json.dumps(object)
    for k,v in groups.items():
        object_string = object_string.replace(k, v)
    try:
        ret = literal_eval(object_string)
        return ret
    except:
        object_string = object_string.replace('false', 'False')
        ret = literal_eval(object_string)
        return ret
    
def get_catalog_introspection(model):
    new_object = {}
    if hasattr(model, 'acls'):
        new_object['acls'] = replace_group(model.acls)
    if hasattr(model, 'acl_bindings'):
        new_object['acl_bindings'] = replace_group(model.acl_bindings)
    schemas = {}
    new_object['schemas'] = schemas
    for schema_name in model.schemas:
        new_schema = {}
        schemas[schema_name] = new_schema
        schema = model.schemas[schema_name]
        if hasattr(schema, 'acls'):
            new_schema['acls'] = replace_group(schema.acls)
        if hasattr(schema, 'acl_bindings'):
            new_schema['acl_bindings'] = replace_group(schema.acl_bindings)
        new_tables = {}
        new_schema['tables'] = new_tables
        for table_name in schema.tables:
            new_table = {}
            new_tables[table_name] = new_table
            table = schema.tables[table_name]
            if hasattr(table, 'acls'):
                new_table['acls'] = replace_group(table.acls)
            if hasattr(table, 'acl_bindings'):
                new_table['acl_bindings'] = replace_group(table.acl_bindings)
            new_columns = {}
            new_table['columns'] = new_columns
            for column in table.columns:
                new_column = {}
                new_columns[column.name] = new_column
                if hasattr(column, 'acls'):
                    new_column['acls'] = replace_group(column.acls)
                if hasattr(column, 'acl_bindings'):
                    new_column['acl_bindings'] = replace_group(column.acl_bindings)
            new_foreign_keys = {}
            new_table['foreign_keys'] = new_foreign_keys
            for foreign_key in table.foreign_keys:
                new_foreign_key = {}
                new_foreign_keys[foreign_key.constraint_name] = new_foreign_key
                if hasattr(foreign_key, 'acls'):
                    new_foreign_key['acls'] = replace_group(foreign_key.acls)
                if hasattr(foreign_key, 'acl_bindings'):
                    new_foreign_key['acl_bindings'] = replace_group(foreign_key.acl_bindings)
        
    fw = open('catalog_acls.json', 'w')
    json.dump(new_object, fw, indent=4)
    fw.close()

def main(server_name, catalog_id, credentials):
    server = DerivaServer('https', server_name, credentials)
    catalog = server.connect_ermrest(catalog_id)
    catalog.dcctx['cid'] = 'oneoff/model'
    model = catalog.getCatalogModel()
    get_catalog_introspection(model)

if __name__ == '__main__':
    host = 'data.pdb-dev.org'
    catalog_id = 1
    credentials = get_credential(host)
    main(host, catalog_id, credentials)
