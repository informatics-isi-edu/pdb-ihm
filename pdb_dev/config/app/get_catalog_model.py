#!/usr/bin/python3

import argparse
import sys
from deriva.core import ErmrestCatalog, get_credential, DerivaServer
from deriva.core.ermrest_model import tag as chaise_tags
import json

system_columns = ['RID', 'RCT', 'RMT', 'RCB', 'RMB', 'Owner']

parser = argparse.ArgumentParser()
parser.add_argument('hostname')
parser.add_argument('catalog_number')
parser.add_argument('action')
if len(sys.argv) == 5:
    parser.add_argument('target')
args = parser.parse_args()

def addVisibleConstraintAnnotations(value, visible_constraints):
    if type(value).__name__ == 'list':
        if len(value) == 2:
            if type(value[0]).__name__ == 'str' and type(value[1]).__name__ == 'str':
                """
                We suppose a Foreign Key constraint to be an array with 2 elements, each of "str" type
                """
                if value[0] not in visible_constraints.keys():
                    visible_constraints[value[0]] = []
                if value[1] not in visible_constraints[value[0]]:
                    visible_constraints[value[0]].append(value[1])
            else:
                """
                Traverse recursively the list
                """
                addVisibleConstraintAnnotations(value[0], visible_constraints)
                addVisibleConstraintAnnotations(value[1], visible_constraints)
        else:
            """
            Traverse recursively the list
            """
            for item in value:
                addVisibleConstraintAnnotations(item, visible_constraints)
    elif type(value).__name__ == 'dict':
        """
        Traverse recursively the dictionary
        """
        for key in value.keys():
            addVisibleConstraintAnnotations(value[key], visible_constraints)
    elif type(value).__name__ not in ['str', 'bool']:
        print ('Unhandled type: {}, {}'.format(type(value).__name__, value))
 
def getTableVisibleConstraints(table, tag):
    visible_constraints = {}
    """
    Search for Foreign Key constraints in the table annotations
    """
    if tag in table.annotations.keys():
        addVisibleConstraintAnnotations(table.annotations[tag], visible_constraints)
    return visible_constraints
    
def getSchemaVisibleConstraints(schema, tag):
    schema_visible_constraints = {}
    tables = schema.tables
    """
    Search for Foreign Key constraints in the tables annotations of the schema
    """
    for key in tables:
        table = tables[key]
        table_visible_constraints = getTableVisibleConstraints(table, tag)
        if len(table_visible_constraints) > 0:
            schema_visible_constraints[key] = table_visible_constraints
    return schema_visible_constraints

def getCatalogVisibleConstraints(model_root, tag):
    catalog_visible_constraints = {}
    schemas = model_root.schemas
    """
    Search for Foreign Key constraints in the tables annotations of the catalog
    """
    for key in schemas:
        schema = schemas[key]
        schema_visible_constraints = getSchemaVisibleConstraints(schema, tag)
        if len(schema_visible_constraints) > 0:
            catalog_visible_constraints[key] = schema_visible_constraints
    return catalog_visible_constraints

def getTableForeignKeys(table):
    """
    Get the Foreign Keys constraints names of the table
    """
    table_foreign_keys = {}
    foreign_keys = table.foreign_keys
    for fk in foreign_keys:
        fk_schema_name = fk.constraint_schema.name
        if fk_schema_name not in table_foreign_keys.keys():
            table_foreign_keys[fk_schema_name] = []
        table_foreign_keys[fk_schema_name].append(fk.constraint_name)
    return table_foreign_keys
    
def getSchemaForeignKeys(schema):
    """
    Get the Foreign Keys constraints names of the schema
    """
    schema_foreign_keys = {}
    tables = schema.tables
    for key in tables:
        table = tables[key]
        table_foreign_keys = getTableForeignKeys(table)
        if len(table_foreign_keys) > 0:
            schema_foreign_keys[key] = table_foreign_keys
    return schema_foreign_keys

def getCatalogForeignKeys(model_root):
    """
    Get the Foreign Keys constraints names of the catalog
    """
    catalog_foreign_keys = {}
    schemas = model_root.schemas
    for key in schemas:
        schema = schemas[key]
        schema_foreign_keys = getSchemaForeignKeys(schema)
        if len(schema_foreign_keys) > 0:
            catalog_foreign_keys[key] = schema_foreign_keys
    return catalog_foreign_keys

def getInvalidTableVisibleConstraints(table, schema, table_visible_constraints, tag):
    """
    Get the invalid constraints names referred in the visible columns or visible foreign keys of the table
    """
    invalid_table_visible_constraints = {}
    if tag == chaise_tags.visible_columns:
        constraints = table.foreign_keys
    elif tag == chaise_tags.visible_foreign_keys:
        constraints = table.referenced_by

    for constraint_schema_name in table_visible_constraints.keys():
        for constraint_name in table_visible_constraints[constraint_schema_name]:
            try:
                constraint = constraints.__getitem__((schema, constraint_name))
            except:
                if constraint_schema_name not in invalid_table_visible_constraints.keys():
                    invalid_table_visible_constraints[constraint_schema_name] = []
                invalid_constraints = invalid_table_visible_constraints[constraint_schema_name]
                if constraint_name not in invalid_constraints:
                    invalid_constraints.append(constraint_name)
    return invalid_table_visible_constraints
    
def getInvalidSchemaVisibleConstraints(schema, schema_visible_constraints, tag):
    """
    Get the invalid constraints names referred in the visible columns or visible foreign keys of the schema
    """
    invalid_schema_visible_constraints = {}
    tables = schema.tables
    for key in tables:
        if key in schema_visible_constraints.keys():
            table = tables[key]
            invalid_table_visible_constraints = getInvalidTableVisibleConstraints(table, schema, schema_visible_constraints[key], tag)
            if len(invalid_table_visible_constraints) > 0:
                invalid_schema_visible_constraints[key] = invalid_table_visible_constraints
    return invalid_schema_visible_constraints

def getInvalidCatalogVisibleConstraints(model_root, catalog_visible_constraints, tag):
    """
    Get the invalid constraints names referred in the visible columns or visible foreign keys of the catalog
    """
    invalid_catalog_visible_constraints = {}
    schemas = model_root.schemas
    for key in schemas:
        if key in catalog_visible_constraints.keys():
            schema = schemas[key]
            invalid_schema_visible_constraints = getInvalidSchemaVisibleConstraints(schema, catalog_visible_constraints[key], tag)
            if len(invalid_schema_visible_constraints) > 0:
                invalid_catalog_visible_constraints[key] = invalid_schema_visible_constraints
    return invalid_catalog_visible_constraints
    
def getColumnDefinition(column):
    """
    Get the JSON representation of a column definition
    """
    column_definition = {}
    column_definition['type'] = column.type.prejson()['typename']
    if column.nullok != None and column.nullok == False:
        column_definition['Nullable'] = 'NOT NULL'
    if column.default != None:
        column_definition['default'] = column.default
    if column.annotations != None and len(column.annotations) > 0:
        column_definition['annotations'] = column.annotations
    if column.comment != None and len(column.comment) > 0:
        column_definition['comment'] = column.comment
    if column.acls != None and len(column.acls) > 0:
        column_definition['acls'] = column.acls
    if column.acl_bindings != None and len(column.acl_bindings) > 0:
        column_definition['acl_bindings'] = column.acl_bindings
    return column_definition
                       
def getTableDefinition(table):
    """
    Get the JSON representation of a table definition
    """
    table_definition = {}
    
    """
    Get the table columns definitions
    """
    table_definition['columns'] = {}
    column_definitions = table_definition['columns']
    columns = table.column_definitions
    for column in columns:
        column_name = column.name
        if column_name not in system_columns:
            column_definition = getColumnDefinition(column)
            if len(column_definition) > 0:
                column_definitions[column_name] = column_definition
    
    """
    Get the table unique keys
    """
    keys_definitions = {}
    keys = table.keys
    for key in keys:
        key_definition = {}
        constraint_name = key.constraint_name
        columns_names = []
        for column in key.unique_columns:
            columns_names.append(column.name)
        if len(columns_names) == 1 and columns_names[0] == 'RID':
            continue
        key_definition['unique_columns'] = '({})'.format(','.join(columns_names))
        if key.annotations != None and len(key.annotations) > 0:
            key_definition['annotations'] = key.annotations
        keys_definitions[constraint_name] = key_definition
    if len(keys_definitions) > 0:
        table_definition['keys'] = keys_definitions
    
    """
    Get the table foreign keys
    """
    foreign_keys_definitions = {}
    foreign_keys = table.foreign_keys
    for foreign_key in foreign_keys:
        constraint_name = foreign_key.constraint_name
        columns_names = []
        for column in foreign_key.foreign_key_columns:
            columns_names.append(column.name)
        if len(columns_names) == 1 and columns_names[0] in ['Owner', 'RCB', 'RMB']:
            continue
        foreign_key_definition = {}
        foreign_key_definition['columns'] = '({})'.format(','.join(columns_names))
        
        referenced_columns_definition = {'schema': foreign_key.constraint_schema.name,
                                    'table': foreign_key.pk_table.name
                                    }
        referenced_columns_names = []
        for column in foreign_key.referenced_columns:
            referenced_columns_names.append(column.name)
        referenced_columns_definition['columns'] = '({})'.format(','.join(referenced_columns_names))
        foreign_key_definition['referenced_columns'] = referenced_columns_definition
        if foreign_key.annotations != None and len(foreign_key.annotations) > 0:
            foreign_key_definition['annotations'] = foreign_key.annotations
        foreign_keys_definitions[constraint_name] = foreign_key_definition
    if len(foreign_keys_definitions) > 0:
        table_definition['foreign_keys'] = foreign_keys_definitions
    
    """
    Get the table reference by
    """
    referenced_by_definitions = {}
    referenced_by = table.referenced_by
    for foreign_key in referenced_by:
        constraint_name = foreign_key.constraint_name
        columns_names = []
        for column in foreign_key.foreign_key_columns:
            columns_names.append(column.name)
        if len(columns_names) == 1 and columns_names[0] in ['Owner', 'RCB', 'RMB']:
            continue
        foreign_key_definition = {'schema': foreign_key.constraint_schema.name,
                                  'table': foreign_key.table.name
                                  }
        foreign_key_definition['columns'] = '({})'.format(','.join(columns_names))
        
        referenced_columns_names = []
        for column in foreign_key.referenced_columns:
            referenced_columns_names.append(column.name)
        foreign_key_definition['referenced_columns'] = '({})'.format(','.join(referenced_columns_names))
        if foreign_key.annotations != None and len(foreign_key.annotations) > 0:
            foreign_key_definition['annotations'] = foreign_key.annotations
        referenced_by_definitions[constraint_name] = foreign_key_definition
    if len(referenced_by_definitions) > 0:
        table_definition['referenced_by'] = referenced_by_definitions
    
    """
    Get the table attributes
    """
    if table.annotations != None and len(table.annotations) > 0:
        table_definition['annotations'] = table.annotations
    if table.comment != None and len(table.comment) > 0:
        table_definition['comment'] = table.comment
    if table.acls != None and len(table.acls) > 0:
        table_definition['acls'] = table.acls
    if table.acl_bindings != None and len(table.acl_bindings) > 0:
        table_definition['acl_bindings'] = table.acl_bindings
    return table_definition
                       
def getSchemaDefinition(schema):
    """
    Get the JSON representation of a schema definition
    """
    schema_definition = {}
    
    """
    Get the schema tables definitions
    """
    
    schema_definition['tables'] = {}
    table_definitions = schema_definition['tables']
    tables = schema.tables
    for key in tables:
        table = tables[key]
        table_definition = getTableDefinition(table)
        if len(table_definition) > 0:
            table_definitions[key] = table_definition
    """
    Get the schema attributes
    """
    if schema.annotations != None and len(schema.annotations) > 0:
        schema_definition['annotations'] = schema.annotations
    if schema.comment != None and len(schema.comment) > 0:
        schema_definition['comment'] = schema.comment
    if schema.acls != None and len(schema.acls) > 0:
        schema_definition['acls'] = schema.acls
    return schema_definition
                       
def getCatalogDefinition(model_root):
    """
    Get the JSON representation of a catalog definition
    """
    catalog_definition = {}
    
    """
    Get the catalog schema definitions
    """
    catalog_definition['schemas'] = {}
    schema_definitions = catalog_definition['schemas']
    schemas = model_root.schemas
    for key in schemas:
        schema = schemas[key]
        schema_definition = getSchemaDefinition(schema)
        if len(schema_definition) > 0:
            schema_definitions[key] = schema_definition

    """
    Get the catalog attributes
    """
    if model_root.annotations != None and len(model_root.annotations) > 0:
        catalog_definition['annotations'] = model_root.annotations
    if model_root.acls != None and len(model_root.acls) > 0:
        catalog_definition['acls'] = model_root.acls
    return catalog_definition
                       
def getTableAttribute(table_list, attribute, column_name=None):
    """
    Extract the "attribute" value from the table definition
    """
    table_attributes = {}
    if column_name == None:
        if attribute == None:
            for key in table_list.keys():
                if key != 'columns':
                    table_attributes[key] = table_list[key]
        else:
            if attribute in table_list.keys():
                table_attributes[attribute] = table_list[attribute]
            elif attribute == 'constraints':
                if 'keys' in table_list.keys():
                    table_attributes['keys'] = table_list['keys']
                if 'foreign_keys' in table_list.keys():
                    table_attributes['foreign_keys'] = table_list['foreign_keys']
                if 'referenced_by' in table_list.keys():
                    table_attributes['referenced_by'] = table_list['referenced_by']
            return table_attributes
    if column_name == None:
        """
        Get the attribute for all the table columns
        """
        columns = table_list['columns'].keys()
    else:
        columns = [column_name]
    columns_attribute = {}
    for column in columns:
        column_attributes = table_list['columns'][column]
        if attribute != None:
            if attribute in column_attributes.keys():
                columns_attribute[column] = column_attributes[attribute]
        else:
            columns_attribute[column] = column_attributes
                
    if len(columns_attribute) > 0:
        table_attributes['columns'] = columns_attribute
    return table_attributes

def getSchemaAttribute(schema_list, attribute, table_name=None, column_name=None):
    """
    Extract the "attribute" value from the schema definition
    """
    schema_attributes = {}
    if table_name == None and column_name == None:
        if attribute == None:
            for key in schema_list.keys():
                if key != 'tables':
                    schema_attributes[key] = schema_list[key]
        else:
            if attribute in schema_list.keys():
                schema_attributes[attribute] = schema_list[attribute]
            if attribute != 'constraints':
                return schema_attributes
    if table_name == None:
        """
        Get the attribute for all the schema tables
        """
        tables = schema_list['tables'].keys()
    else:
        tables = [table_name]
    tables_attribute = {}
    for table in tables:
        table_attribute = getTableAttribute(schema_list['tables'][table], attribute, column_name)
        if len(table_attribute) > 0:
            tables_attribute[table] = table_attribute
    if len(tables_attribute) > 0:
        schema_attributes['tables'] = tables_attribute
    return schema_attributes

def getCatalogAttribute(catalog_list, attribute, schema_name=None, table_name=None, column_name=None):
    """
    Extract the "attribute" value from the catalog definition
    """
    catalog_attributes = {}
    if schema_name == None and table_name == None and column_name == None:
        if attribute == None:
            for key in catalog_list.keys():
                if key != 'schemas':
                    catalog_attributes[key] = catalog_list[key]
        else:
            if attribute in catalog_list.keys():
                catalog_attributes[attribute] = catalog_list[attribute]
            if attribute != 'constraints':
                return catalog_attributes
    schemas_attributes = {}
    if schema_name == None:
        """
        Get the attribute for all the catalog schemas
        """
        schemas = catalog_list['schemas'].keys()
    else:
        schemas = [schema_name]
    for schema in schemas:
        schema_attribute = getSchemaAttribute(catalog_list['schemas'][schema], attribute, table_name, column_name)
        if len(schema_attribute) > 0:
            schemas_attributes[schema] = schema_attribute
    if len(schemas_attributes) > 0:
        catalog_attributes['schemas'] = schemas_attributes
    return catalog_attributes
        
    
actions = ['annotations', 'display', 'fkeys', 'validate']
usage = """
usage: python3 validate_visible_columns.py hostname catalog_number action[:attribute] [target]

positional arguments:
    <hostname>        Fully qualified host name.
    <catalog_number>  The catalog ID.
    <action>          Can have one of the values:
                        annotations : Display the Foreign Keys referred in the tag:isrd.isi.edu,2016:visible-columns and tag:isrd.isi.edu,2016:visible-foreign-keys annotations.
                        display[:attribute] : Display the definition or the attribute only of a catalog, schema, table or column.
                            <attribute> : Can have one of the values:
                                            acls : Display only the "acls" of the target
                                            acl_bindings : Display only the "acl_bindings" of the target
                                            annotations : Display only the "annotations" of the target
                                            comment: Display only the "comment" of the target
                                            constraints : Display only the "constraints" ("keys", "foreign keys" or "referenced by") of the target
                        fkeys : Display the Foreign Keys.
                        validate : Display the invalid Foreign Keys referred in the annotations of all the tables of a catalog, of a schema or just to one table..

optional arguments:
    <target>          Can have one of the values:
                        - schema : The action will be applied only to the schema specified by the schema_name.
                        - table : The action will be applied only to the table specified in the format schema_name:table_name.
                        - column : The action will be applied only to the column specified in the format schema_name:table_name:column_name.
"""

hostname = args.hostname
catalog_number = args.catalog_number
action = args.action

if len(action.split(':')) == 2:
    attribute = action.split(':')[1]
    action = action.split(':')[0]
elif len(action.split(':')) == 1:
    attribute = None
else:
    print ('Invalid value "{}" for the "action" parameter.'.format(action))
    print ('Valid parameters are:')
    for value in actions:
        print ('\t{}'.format(value))
    print (usage)
    sys.exit(1)

if len(sys.argv) == 5:
    target = args.target
else:
    target = None

if action not in actions:
    print ('Invalid value "{}" for the "action" parameter.'.format(action))
    print ('Valid parameters are:')
    for value in actions:
        print ('\t{}'.format(value))
    print (usage)
    sys.exit(1)
    
if target != None:
    if len(target.split(':')) == 1:
        schema_name = target
        table_name = None
        column_name = None
    elif len(target.split(':')) == 2:
        schema_name = target.split(':')[0]
        table_name = target.split(':')[1]
        column_name = None
    elif len(target.split(':')) == 3:
        schema_name = target.split(':')[0]
        table_name = target.split(':')[1]
        column_name = target.split(':')[2]
    else:
        print ('Invalid format for the "target" parameter.')
        print ('Valid format is: schema_name[:table_name[:column_name]]')
        print (usage)
        sys.exit(1)
else:
    schema_name = None
    table_name = None
    column_name = None

if column_name != None and action != 'display':
    print ('WARNING: column name "{}" ignored for action "{}".'.format(column_name, action))
    
credential = get_credential(hostname)
catalog_ermrest = ErmrestCatalog('https', hostname, catalog_number, credentials=credential)
model_root = catalog_ermrest.getCatalogModel()

catalog_foreign_keys = getCatalogForeignKeys(model_root)
catalog_visible_columns = getCatalogVisibleConstraints(model_root, chaise_tags.visible_columns)
catalog_visible_foreign_keys = getCatalogVisibleConstraints(model_root, chaise_tags.visible_foreign_keys)
invalid_visible_columns = getInvalidCatalogVisibleConstraints(model_root, catalog_visible_columns,chaise_tags.visible_columns )
invalid_visible_foreign_keys = getInvalidCatalogVisibleConstraints(model_root, catalog_visible_foreign_keys, chaise_tags.visible_foreign_keys)
invalid_constraints = {}
if len(invalid_visible_columns) > 0:
    if target == None:
        invalid_constraints['visible_columns'] = invalid_visible_columns
    elif schema_name in invalid_visible_columns.keys():
        if table_name == None:
            invalid_constraints['visible_columns'] = invalid_visible_columns[schema_name]
        elif table_name in invalid_visible_columns[schema_name].keys():
             invalid_constraints['visible_columns'] = invalid_visible_columns[schema_name][table_name]
           
if len(invalid_visible_foreign_keys) > 0:
    invalid_constraints['visible_foreign_keys'] = invalid_visible_foreign_keys
    
catalog_list = getCatalogDefinition(model_root)

if action == 'display':
    catalog_id = 'Catalog {}'.format(catalog_number)
    res = {catalog_id: {}}
    res[catalog_id] = getCatalogAttribute(catalog_list, attribute, schema_name=schema_name, table_name=table_name, column_name=column_name)
    if len(res[catalog_id]) == 0:
        res = {}
    print (json.dumps(res, indent=4))
elif action == 'fkeys':
    print (json.dumps(catalog_foreign_keys, indent=4))
elif action == 'annotations':
    print (json.dumps(catalog_visible_columns, indent=4))
    print (json.dumps(catalog_visible_foreign_keys, indent=4))
elif action == 'validate':
    print (json.dumps(invalid_constraints, indent=4))

sys.exit(1)

    

