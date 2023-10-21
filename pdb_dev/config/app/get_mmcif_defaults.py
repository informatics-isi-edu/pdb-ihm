#!/usr/bin/python3

import sys
import traceback
import json
import argparse
from deriva.core import ErmrestCatalog, get_credential
from deriva.core.ermrest_model import builtin_types as typ, Table, Key, ForeignKey

def describe(table):
    system_columns = ['RID', 'RCT', 'RMT', 'RCB', 'RMB']
    unique_columns = []
    foreign_key_columns = []
    not_null_columns = []
    keys = table.keys
    for key in keys:
        for col in key.unique_columns:
            if col.name not in (system_columns + unique_columns):
                unique_columns.append(col.name)
    keys = table.foreign_keys
    for key in keys:
        for col in key.foreign_key_columns:
            if col.name not in (system_columns + unique_columns + foreign_key_columns):
                foreign_key_columns.append(col.name)
    columns = table.column_definitions
    for column in columns:
        if column.nullok == False and column.default == None and column.type.typename == 'text' and column.type.is_domain == False and column.type.is_array == False and column.name not in (system_columns + unique_columns + foreign_key_columns):
            not_null_columns.append(column.name)
    return not_null_columns

parser = argparse.ArgumentParser()
parser.add_argument('hostname')
parser.add_argument('catalog_number')
parser.add_argument('schema_name')
args = parser.parse_args()


hostname = args.hostname
catalog_number = args.catalog_number
schema_name = args.schema_name

credential = get_credential(hostname)
catalog_ermrest = ErmrestCatalog('https', hostname, catalog_number, credentials=credential)
catalog_ermrest.dcctx['cid'] = 'model'
model_root = catalog_ermrest.getCatalogModel()
schema = model_root.schemas[schema_name]
tables = schema.tables

not_null_not_default_columns = {}
for table in tables:
    if table not in ['Entry_Related_File_Templates', 'entry']:
        ret = describe(tables[table])
        if len(ret) > 0:
            not_null_not_default_columns[table] = ret
print(json.dumps(not_null_not_default_columns, indent=4))

