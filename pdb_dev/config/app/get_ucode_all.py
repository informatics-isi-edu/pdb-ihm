#!/usr/bin/python3

import argparse
import sys
import json
import traceback
from deriva.core import ErmrestCatalog, get_credential
from deriva.core.ermrest_model import Type, builtin_types
import subprocess

debug = False

def column_is_fk(fkeys, table_name, column_name, model_root, indent, vocab_tables):
    is_fk = False
    for fkey in fkeys:
        foreign_key_columns = fkey.foreign_key_columns
        index = 0
        for column in foreign_key_columns:
            if column.name == column_name:
                if debug == True:
                    print('{}PDB.{}.{} references {}.{}.{}'.format(indent, table_name, column_name, fkey.pk_table.schema.name, fkey.pk_table.name, fkey.referenced_columns[index].name))
                is_fk = True
                if fkey.pk_table.schema.name == 'PDB':
                    column_is_fk(model_root.schemas['PDB'].tables[fkey.pk_table.name].foreign_keys, fkey.pk_table.name, fkey.referenced_columns[index].name, model_root, indent + '    ', vocab_tables)
                else:
                    if fkey.pk_table.name not in vocab_tables:
                        vocab_tables.append(fkey.pk_table.name)
            index +=1
    if is_fk == False:
        if debug == True:
            print('{}PDB.{}.{} is not a Foreign Key'.format(indent, table_name, column_name))

args = ['/usr/bin/python3', 'testGetUcode.py', 'ihm-extension.dic']
if debug == True:
    print('Running "{}"'.format(' '.join(args))) 
p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
stdoutdata, stderrdata = p.communicate()
returncode = p.returncode
if returncode != 0:
    print('Can not get Ucode for dictionary "%s".\nstdoutdata: %s\nstderrdata: %s\n' % ('ihm-extension.dic', stdoutdata, stderrdata)) 
    sys.exit(1)
fw = open('ucode_ihm.log', 'w')
fw.write(stdoutdata.decode('utf-8'))
fw.close()

args = ['/usr/bin/python3', 'testGetUcode.py', 'mmcif_v5.342_ihm_v1.17.dic']
if debug == True:
    print('Running "{}"'.format(' '.join(args))) 
p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
stdoutdata, stderrdata = p.communicate()
returncode = p.returncode
if returncode != 0:
    print('Can not get Ucode for dictionary "%s".\nstdoutdata: %s\nstderrdata: %s\n' % ('mmcif_pdbx_v50.dic', stdoutdata, stderrdata)) 
    sys.exit(1)
fw = open('ucode_mmCIF.log', 'w')
fw.write(stdoutdata.decode('utf-8'))
fw.close()

parser = argparse.ArgumentParser()
parser.add_argument('hostname')
parser.add_argument('catalog_number')
args = parser.parse_args()


hostname = args.hostname
catalog_number = args.catalog_number

schema_name= 'PDB'

ucode = {}

vocab_tables = []

missing_tables = []

for input in ['ucode_ihm.log', 'ucode_mmCIF.log']:
    fr = open(input, 'r')
    lines = fr.readlines()
    for line in lines:
        if line.startswith('Table:'):
            tokens = line.split()
            table = tokens[1]
            column = tokens[3]
            if table not in ucode.keys():
                ucode[table] = []
            if column in ucode[table]:
                if debug == True:
                    print('Duplicate column: {}.{}'.format(table, column))
            else:
                ucode[table].append(column)
            
    fr.close()

credential = get_credential(hostname)
catalog_ermrest = ErmrestCatalog('https', hostname, catalog_number, credentials=credential)
catalog_ermrest.dcctx['cid'] = 'model'
model_root = catalog_ermrest.getCatalogModel()

for table_name,columns in ucode.items():
    try:
        table = model_root.schemas[schema_name].tables[table_name]
        fkeys = table.foreign_keys
        for column_name in columns:
            column = table.column_definitions.__getitem__(column_name)
            column_is_fk(fkeys, table_name, column_name, model_root, '', vocab_tables)
    except:
        missing_tables.append(table_name)

if False:
    for vocab_table in vocab_tables:
        print('select count(*) as {} from "Vocab".{};'.format(vocab_table, vocab_table))
    print(len(vocab_tables))
    
ucode_tables = {}
schema = model_root.schemas['Vocab']
for table_name in vocab_tables:
    table = schema.tables[table_name]
    referenced_by = table.referenced_by
    if len(referenced_by) != 1:
        print('More than 1 table is referring Vocab.{}'.format(table_name))
    referenced_by = referenced_by[0]
    schema_name = referenced_by.constraint_schema.name
    tname = referenced_by.table.name
    fk_name = referenced_by.constraint_name
    foreign_key_columns = referenced_by.foreign_key_columns
    if len(foreign_key_columns) != 1:
        print('More than 1 column is referring Vocab.{}'.format(table_name))
    foreign_key_column_name = foreign_key_columns[0].name
    if tname not in ucode_tables.keys():
        ucode_tables[tname] = []
    ucode_tables[tname].append(foreign_key_column_name)

if 'chem_comp' not in ucode_tables.keys():
    ucode_tables['chem_comp'] = []
ucode_tables['chem_comp'].append('id')
fw = open('vocab_ucode.json', 'w')
json.dump(ucode_tables, fw, indent=4)
fw.close()


