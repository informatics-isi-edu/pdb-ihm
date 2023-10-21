#!/usr/bin/python3

import os
import json
import sys
import traceback
import pickle
import csv
from ast import literal_eval

from deriva.core import ErmrestCatalog, get_credential
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('hostname')
parser.add_argument('catalog_number')
parser.add_argument('schema_name')
parser.add_argument('pickle_file')
parser.add_argument('data_map_file')

args = parser.parse_args()

hostname = args.hostname
catalog_number = args.catalog_number
schema_name = args.schema_name
pickle_file = args.pickle_file
data_map_file = args.data_map_file

credential = get_credential(hostname)
catalog_ermrest = ErmrestCatalog('https', hostname, catalog_number, credentials=credential)
catalog_ermrest.dcctx['cid'] = 'test/model'

with open(pickle_file, 'rb') as f:
    vocab_list = pickle.load(f)

pb = catalog_ermrest.getPathBuilder()

map_term_value = {}


vocabulary_new_tables_name = {
                              'ihm_geometric_object_distance_restraint_group_conditionality': 'geometric_object_distance_restraint_group_condition',
                              'ihm_geometric_object_distance_restraint_object_characteristic': 'geometric_object_distance_restraint_object_character',
                              'ihm_model_representation_details_model_object_primitive': 'model_representation_details_model_object_primitive',
                              'ihm_starting_comparative_models_template_sequence_identity_denominator': 'starting_comparative_models_template_sequence_id_denom'
                              }

"""
Map to ID of Vocabulary table
"""
term_data_map = {}
for vocab_dict in vocab_list:
    for k, v in vocab_dict.items():
        vocab_table_name = '{}_{}'.format(k[0], k[1])
        if vocab_table_name in vocabulary_new_tables_name.keys():
            vocab_table_name = vocabulary_new_tables_name[vocab_table_name]
        if vocab_table_name not in pb.schemas[schema_name].tables.keys():
            continue
        vocab_table = pb.schemas[schema_name].tables[vocab_table_name]
        entities = vocab_table.path.entities()
        for entity in entities:
            term_data_map[(k[0], k[1], entity['Name'])] = entity['ID']
        
fw = open(data_map_file, 'w')
fw.write('{}'.format(term_data_map))
fw.close()

fr = open(data_map_file, mode='r')
all_of_it = fr.read()
fr.close()

python_dict = literal_eval(all_of_it)

