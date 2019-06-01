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

parser = argparse.ArgumentParser()
parser.add_argument('hostname')
parser.add_argument('catalog_number')
parser.add_argument('schema_name')
parser.add_argument('term_schema_name')
args = parser.parse_args()


filename_list = ['PDBDEV_00000001.json', 'PDBDEV_00000020.json']

vocab_list = []
term_data_map = {}
with open('exported_vocab.pickle', 'rb') as pickle_file:
    vocab_list = pickle.load(pickle_file)

hostname = args.hostname
vocab_schema_name = args.term_schema_name
schema_name = args.schema_name
catalog_number = args.catalog_number
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
for filename in filename_list:
    with open(filename, 'r') as f:
        pdb = json.load(f)
        pdb = pdb[0]
    for tname, records in pdb.items():
        print(tname)
        if tname in ['_id', '_entry_id', '__entry_id', '_schema_version']:
            continue
        elif type(records) is dict:
            records = [records]

        table = pb.schemas[schema_name].tables[tname]
        entities = table.path.entities()
        if len(entities) > 0 and '00000001' in filename:
            table.path.delete()

        entities = []
        for r in records:
            for k, v in r.items():
                if (tname, k, v) in term_data_map.keys():
                    r[k] = term_data_map[(tname, k, v)]
            entities.append(r)
        try:
            table.insert(entities)
        except HTTPError as e:
            print(e)
            print(e.response.text)
            exit(1)
