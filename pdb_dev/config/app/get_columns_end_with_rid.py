#!/usr/bin/python3

import argparse
import sys
from deriva.core import ErmrestCatalog, get_credential, DerivaServer
from deriva.core.ermrest_model import tag as chaise_tags
import traceback
import json

"""
Usage:
    python3 get_columns_end_with_RID.py dev.pdb-dev.org 99
"""

parser = argparse.ArgumentParser()
parser.add_argument('hostname')
parser.add_argument('catalog_number')

args = parser.parse_args()

catalog_number = args.catalog_number
hostname = args.hostname
schema_name = 'PDB'

credential = get_credential(hostname)
catalog_ermrest = ErmrestCatalog('https', hostname, catalog_number, credentials=credential)
catalog_ermrest.dcctx['cid'] = 'model'
model_root = catalog_ermrest.getCatalogModel()
schema = model_root.schemas[schema_name]

combo1_columns = {}

def getForeignKeyColumns(fk):
    ret = {}
    i =0
    for fk_col in fk.foreign_key_columns:
        if not fk_col.name.endswith('_RID') and fk_col.name != 'structure_id':
            ret[fk_col.name] = fk.referenced_columns[i].name
        i += 1
    return ret
    
for table_name in schema.tables:
    table = schema.tables[table_name]
    for column in table.column_definitions:
        if column.name.endswith('_RID') and column.nullok == False:
            for fk in table.foreign_keys:
                i = 0
                for fk_col in fk.foreign_key_columns:
                    if fk_col.name == column.name:
                        if table_name not in combo1_columns.keys():
                            combo1_columns[table_name] = {}
                        combo1_columns[table_name][column.name] = {}
                        combo1_columns[table_name][column.name][fk.pk_table.name] = getForeignKeyColumns(fk)
                    i +=1

fw = open('combo1_columns.json', 'w')
json.dump(combo1_columns, fw, indent=4)
fw.write('\n')
fw.close()

pk_tables = []
for fk_table,fk_value in combo1_columns.items():
    for fk_col, value in fk_value.items():
        for k in value.keys():
            if k not in pk_tables:
                pk_tables.append(k)
#print(json.dumps(pk_tables, indent=4))
fk_tables = []
for fk_table in combo1_columns.keys():
    if fk_table not in fk_tables:
        fk_tables.append(fk_table)
#print(json.dumps(fk_tables, indent=4))

"""
with open('combo1_columns.json', 'r') as f:
    combo1_columns = json.load(f)

def setRID(fk_table, row, combo1_columns, memory_rows):
    entry = combo1_columns[fk_table]
    for col,value in entry.items():
        for pk_table,mappings in value.items():
            for pk_row in memory_rows[pk_table]
                found = True
                for fk_col, pk_col in mappings:
                    if row[fk_col] != pk_row[pk_col]:
                        found = False
                        break
                if found == True:
                    row[col] = pk_row['RID']
                    break
            
    "ihm_pseudo_site_feature": {
        "Pseudo_Site_RID": {
            "ihm_pseudo_site": {
                "pseudo_site_id": "id"
            }
        },
        "Feature_RID": {
            "ihm_feature_list": {
                "feature_id": "feature_id"
            }
        }
    },
    
if tname in pk_tables:
    memory_rows[tname] = rows
    
if tname in fk_tables:
    setRID(tname, row, combo1_columns, memory_rows)
"""