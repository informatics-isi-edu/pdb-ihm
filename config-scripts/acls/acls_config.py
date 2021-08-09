#!/usr/bin/python

from deriva.core import  get_credential, DerivaServer, BaseCLI
from ast import literal_eval
import json
import sys
from acls import pdb_submitter
from acls import table_acls_list, table_acl_bindings_list, table_acl_bindings_template_list
from acls import column_acls_list, column_acl_bindings_list
from acls import foreign_key_acls_list, foreign_key_acl_bindings_list
from acls import catalog_acls, table_acls, table_acl_bindings, column_acls, column_acl_bindings, foreign_key_acls, foreign_key_acl_bindings

"""
ACL Configuration Tool for PDB.

Usage:

    python3 acls_config.py  --host <hostname> --credential-file <credential-file>

"""


def setCatalogACL(model_root):
    changed = False
    if model_root.acls != catalog_acls:
        print('Catalog ACLs modified')
        print('Old: '.format(json.dumps(model_root.acls, indent=4)))
        print('New: '.format(json.dumps(catalog_acls, indent=4)))
        changed = True
    return changed

def getTableConfigACL(schema_name, table_name):
    for table_acl in table_acls:
        if table_acl["schema"] == schema_name:
            for table in table_acl["tables"]:
                if table == table_name:
                    return table_acls_list[table_acl["acls"]]
    return {}
                     
                     
def setTablesACL(model_root):
    changed = False
    for schema_name in model_root.schemas.keys():
        schema = model_root.schemas[schema_name];
        for table_name in schema.tables.keys():
            acls = schema.tables[table_name].acls
            if acls != getTableConfigACL(schema_name, table_name):
                print('Table {}:{} ACLs modified'.format(schema_name, table_name))
                print('Old: '.format(json.dumps(acls, indent=4)))
                print('New: '.format(json.dumps(getTableConfigACL(schema_name, table_name), indent=4)))
                changed = True
    return changed

def getTableACLBindindingTemplate(acl_bindings, fk):
    for key,value in table_acl_bindings_template_list.items():
        if literal_eval(value.replace('%FOREIGN_KEY%', fk).replace('pdb_submitter', pdb_submitter)) == acl_bindings:
            return key
    return None
    
def getTableConfigACLBindings(schema_name, table_name):
    for table_acl_binding in table_acl_bindings:
        if table_acl_binding["schema"] == schema_name:
            for table in table_acl_binding["tables"]:
                if table == table_name:
                    if 'foreign_keys' not in table_acl_binding:
                        return table_acl_bindings_list[table_acl_binding["acl_bindings"]]
                    else:
                        return literal_eval(table_acl_bindings_template_list[table_acl_binding["acl_bindings"]].replace('%FOREIGN_KEY%', table_acl_binding['foreign_keys'][table_name]).replace('pdb_submitter', pdb_submitter)) 
    return {}
                     
def setTablesACLBindings(model_root):
    changed = False
    for schema_name in model_root.schemas.keys():
        schema = model_root.schemas[schema_name];
        for table_name in schema.tables.keys():
            acl_bindings = schema.tables[table_name].acl_bindings
            if acl_bindings != getTableConfigACLBindings(schema_name, table_name):
                print('Table {}:{} ACL Bindings modified'.format(schema_name, table_name))
                print('Old: '.format(json.dumps(acl_bindings, indent=4)))
                print('New: '.format(json.dumps(getTableConfigACLBindings(schema_name, table_name), indent=4)))
                changed = True
    return changed
                     
def getColumnConfigACL(schema_name, table_name, column_name):
    for column_acl in column_acls:
        if column_acl["schema"] == schema_name and column_acl["table"] == table_name:
            if column_name in column_acl["columns"]:
                return column_acls_list[column_acl["acls"]]
    return {}
                     
def setColumnsACL(model_root):
    changed = False
    for schema_name in model_root.schemas.keys():
        schema = model_root.schemas[schema_name];
        for table_name in schema.tables.keys():
            table = schema.tables[table_name]
            for column in table.column_definitions:
                acls = column.acls
                if acls != getColumnConfigACL(schema_name, table_name, column.name):
                    print('Column {}:{}:{} ACLs modified'.format(schema_name, table_name, column.name))
                    print('Old: '.format(json.dumps(acls, indent=4)))
                    print('New: '.format(json.dumps(getColumnConfigACL(schema_name, table_name, column.name), indent=4)))
                    changed = True
    return changed

def getColumnConfigACLBindings(schema_name, table_name, column_name):
    for column_acl_binding in column_acl_bindings:
        if column_acl_binding["schema"] == schema_name and column_acl_binding["table"] == table_name:
            if column_name in column_acl_binding["columns"]:
                return column_acl_bindings_list[column_acl_binding["acl_bindings"]]
    return {}
                     
def setColumnsACLBindings(model_root):
    changed = False
    for schema_name in model_root.schemas.keys():
        schema = model_root.schemas[schema_name];
        for table_name in schema.tables.keys():
            table = schema.tables[table_name]
            for column in table.column_definitions:
                acl_bindings = column.acl_bindings
                if acl_bindings != getColumnConfigACLBindings(schema_name, table_name, column.name):
                    print('Column {}:{}:{} ACL Bindings modified'.format(schema_name, table_name, column.name))
                    print('Old: '.format(json.dumps(acl_bindings, indent=4)))
                    print('New: '.format(json.dumps(getColumnConfigACLBindings(schema_name, table_name, column.name), indent=4)))
                    changed = True
    return changed

def getForeignKeyConfigACL(schema_name, table_name, foreign_key_name):
    for foreign_key_acl in foreign_key_acls:
        if foreign_key_acl["schema"] == schema_name and foreign_key_acl["table"] == table_name:
            if foreign_key_name in foreign_key_acl["foreign_keys"]:
                return foreign_key_acls_list[foreign_key_acl["acls"]]
    return {}
                     
def setForeignKeyACL(model_root):
    changed = False
    for schema_name in model_root.schemas.keys():
        schema = model_root.schemas[schema_name];
        for table_name in schema.tables.keys():
            table = schema.tables[table_name]
            for fk in table.foreign_keys:
                if fk.constraint_name[-8:] not in ['RCB_fkey', 'RMB_fkey'] and fk.constraint_name[-10:] != 'Owner_fkey':
                    acls = fk.acls
                    if acls != getForeignKeyConfigACL(schema_name, table_name, fk.constraint_name):
                        print('Foreign Key {}:{}:{} ACLs modified'.format(schema_name, table_name, fk.constraint_name))
                        print('Old: '.format(json.dumps(acls, indent=4)))
                        print('New: '.format(json.dumps(getForeignKeyConfigACL(schema_name, table_name, fk.constraint_name), indent=4)))
                        changed = True
    return changed

def getForeignKeyConfigACLBindings(schema_name, table_name, foreign_key_name):
    for foreign_key_acl_binding in foreign_key_acl_bindings:
        if foreign_key_acl_binding["schema"] == schema_name and foreign_key_acl_binding["table"] == table_name:
            if foreign_key_name in foreign_key_acl_binding["foreign_keys"]:
                return foreign_key_acl_bindings_list[foreign_key_acl_binding["acl_bindings"]]
    return {}
                     
def setForeignKeyACLBindings(model_root):
    changed = False
    for schema_name in model_root.schemas.keys():
        schema = model_root.schemas[schema_name];
        for table_name in schema.tables.keys():
            table = schema.tables[table_name]
            for fk in table.foreign_keys:
                if fk.constraint_name[-8:] not in ['RCB_fkey', 'RMB_fkey'] and fk.constraint_name[-10:] != 'Owner_fkey':
                    acl_bindings = fk.acl_bindings
                    if acl_bindings != getForeignKeyConfigACLBindings(schema_name, table_name, fk.constraint_name):
                        print('Foreign Key {}:{}:{} ACL Bindings modified'.format(schema_name, table_name, fk.constraint_name))
                        print('Old: '.format(json.dumps(acl_bindings, indent=4)))
                        print('New: '.format(json.dumps(getForeignKeyConfigACLBindings(schema_name, table_name, fk.constraint_name), indent=4)))
                        changed = True
    return changed

def setACLs(model_root):
    changed = setCatalogACL(model_root)
    changed = changed or setTablesACL(model_root)
    changed = changed or setTablesACLBindings(model_root)
    changed = changed or setColumnsACL(model_root)
    changed = changed or setColumnsACLBindings(model_root)
    changed = changed or setForeignKeyACL(model_root)
    changed = changed or setForeignKeyACLBindings(model_root)
    if changed == True:
        print('Applying ACLs changes...')
        model_root.apply()
    else:
        print('No ACLs changes detected.')

def main(server_name, catalog_id, credentials):
    server = DerivaServer('https', server_name, credentials)
    catalog = server.connect_ermrest(catalog_id)
    catalog.dcctx['cid'] = "ACL/model"
    model = catalog.getCatalogModel()
    setACLs(model)

if __name__ == '__main__':
    args = BaseCLI("ACL Configuration Tool", None, 1).parse_cli()
    credentials = get_credential(args.host, args.credential_file)

    main(args.host, 99, credentials)
