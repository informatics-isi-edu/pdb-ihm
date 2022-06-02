#!/usr/bin/python3

import json
import python_jsonschema_objects as pjs
import deriva.core.ermrest_model as em
from collections import namedtuple
from deriva.core import ErmrestCatalog, get_credential, DerivaServer
from deriva.utils.catalog.components.configure_catalog import DerivaCatalogConfigure, DerivaTableConfigure
import deriva.utils.catalog.components.model_elements as model_elements
from deriva.core.ermrest_config import tag as chaise_tags
from requests import HTTPError
import csv
import pickle
import argparse
import sys
import os

parser = argparse.ArgumentParser()
parser.add_argument('hostname')
parser.add_argument('catalog_number')
parser.add_argument('schema_name')
parser.add_argument('term_schema_name')
parser.add_argument('files_dir')
parser.add_argument('pickle_file')
args = parser.parse_args()


vocab_list = []
term_data_map = {}
hostname = args.hostname
catalog_number = args.catalog_number
schema_name = args.schema_name
vocab_schema_name = args.term_schema_name
files_dir = args.files_dir
pickle_file = args.pickle_file

print ('hostname: {}'.format(hostname))
print ('catalog_number: {}'.format(catalog_number))
print ('schema_name: {}'.format(schema_name))
print ('term_schema_name: {}'.format(vocab_schema_name))
print ('files_dir: {}'.format(files_dir))
print ('pickle_file: {}'.format(pickle_file))

with open(pickle_file, 'rb') as pickle_file:
    vocab_list = pickle.load(pickle_file)

filename_list = os.listdir(files_dir)
filename_list.sort()

credential = get_credential(hostname)
server = DerivaServer('https', hostname, credential)
catalog = server.connect_ermrest(catalog_number)
pb = catalog.getPathBuilder()

map_term_value = {}

catalog_ermrest = ErmrestCatalog('https', hostname, catalog_number, credentials=credential)
model = catalog_ermrest.getCatalogModel()

# map to ID of Vocabulary table
for vocab_dict in vocab_list:
    for k, v in vocab_dict.items():
        vocab_table_name = '{}_{}_term'.format(k[0], k[1])
        vocab_table_name = vocab_table_name[-50:]
        vocab_table = pb.schemas[vocab_schema_name].tables[vocab_table_name]
        entities = vocab_table.path.entities()
        for entity in entities:
            term_data_map[(k[0], k[1], entity['Name'])] = entity['ID']

# schema = model.schemas[schema_name]
# for tab_name in schema.tables.keys():
#     table = model.table(schema_name, tab_name)
#     for fkey_def in table.foreign_keys:
#         print(fkey_def)
#         print(fkey_def['referenced_columns'])

# Read JSON data into the datastore variable
inserted_rows = 0
last_inserted_rows = 0

for filename in filename_list:
    with open('{}/{}'.format(files_dir, filename), 'r') as f:
        pdb = json.load(f)
        pdb = pdb[0]
    #print('File: {}'.format(filename))
    for tname, records in pdb.items():
        #print('\tTable: {}'.format(tname))
        if tname in ['_id', '_entry_id', '__entry_id', '_schema_version']:
            continue
        elif type(records) is dict:
            records = [records]

        table = pb.schemas[schema_name].tables[tname]
        """
        entities = table.path.entities()
        if len(entities) > 0 and '00000032' in filename:
            print ('********* 00000032 in {}'.format(filename))
            table.path.delete()
        """
        entities = []
        for r in records:
            for k, v in r.items():
                if (tname, k, v) in term_data_map.keys():
                    r[k] = term_data_map[(tname, k, v)]
            entities.append(r)
        try:
            table.insert(entities)
            inserted_rows = inserted_rows + len(entities)
        except HTTPError as e:
            print(e)
            print(e.response.text)
            print ('Inserted Rows: {}'.format(inserted_rows))
            exit(1)
    print ('File {}: inserted {} rows'.format(filename, (inserted_rows - last_inserted_rows)))
    last_inserted_rows = inserted_rows

print ('Successfully inserted Rows: {}'.format(inserted_rows))
