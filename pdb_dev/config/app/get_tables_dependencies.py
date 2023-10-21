#!/usr/bin/python3

from requests import HTTPError
from deriva.core import DerivaServer, ErmrestCatalog, get_credential
from deriva.core.ermrest_model import Table, Column, Key, builtin_types
import argparse
import sys
import json

parser = argparse.ArgumentParser()
parser.add_argument('hostname')
parser.add_argument('catalog_number')
parser.add_argument('schema_name')
parser.add_argument('filename')
args = parser.parse_args()


hostname = args.hostname
catalog_number = args.catalog_number
schema_name = args.schema_name
filename = args.filename

credential = get_credential(hostname)
server = DerivaServer('https', hostname, credential)
catalog = server.connect_ermrest(catalog_number)
model = catalog.getCatalogModel()
schema = model.schemas[schema_name]
tables = sorted(schema.tables.keys())
groups = {}
tables_dependencies = {}

def checkReferences(table_name):
    table_references = []
    table = model.schemas[schema_name].tables[table_name]
    
    foreign_keys = table.foreign_keys
    for foreign_key in foreign_keys:
        foreign_key_columns = foreign_key.foreign_key_columns
        referenced_columns = foreign_key.referenced_columns
        i = 0
        fk = []
        ref = []
        for foreign_key_column in foreign_key_columns:
            column_name = foreign_key_column.name
            names = foreign_key.names[0]
            if column_name not in ['Owner', 'RCB', 'RMB']:
                reference = referenced_columns[i]
                ref_schema = reference.table.schema.name
                ref_table = reference.table.name
                if table_name in ['Accession_Code'] or ref_table in ['Accession_Code']:
                    continue
                if ref_schema == schema_name and ref_table != table_name and ref_table not in table_references:
                    table_references.append(ref_table)
            i = i+1
    return table_references

def isResolved(tname):
    dependencies = tables_dependencies[tname]
    if len(dependencies) == 0:
        return True
    if len(groups) == 1:
        return False
    for dependency in dependencies:
        found = False
        for i in range(len(groups)-1):
            if dependency in groups[i]:
                found = True
                break
        if found == False:
            return False
    return True
                                    
            

for tname in tables:
    tables_dependencies[tname] = checkReferences(tname)
    
"""
f = open('/home/serban/pdb/fk_dependencies.json', 'w')
f.write(json.dumps(tables_dependencies, indent=4))
f.close()
"""
index = 0
unresolved_references = tables
while len(unresolved_references) > 0:
    unresolved_tables = []
    groups[index] = []
    for tname in unresolved_references:
        if isResolved(tname):
            groups[index].append(tname)
        else:
            unresolved_tables.append(tname)
    unresolved_references = unresolved_tables
    index = index+1
    
f = open(filename, 'w')
f.write(json.dumps(groups, indent=4))
f.close()

for tname in tables:
    found = False
    for key in groups.keys():
        if tname in groups[key]:
            found = True
            break
    if found == False:
        print('Table {} was not found in groups'.format(tname))

print('End of processing.') 
       