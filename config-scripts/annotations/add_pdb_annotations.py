#!/usr/bin/python3

import argparse
import json
import sys

parser = argparse.ArgumentParser()
parser.add_argument('pattern_input')
parser.add_argument('dump_input')
parser.add_argument('output')

args = parser.parse_args()

pattern_input = args.pattern_input
dump_input = args.dump_input
output = args.output

with open('{}'.format(pattern_input), 'r') as f:
    pattern_annotations = json.load(f)

with open('{}'.format(dump_input), 'r') as f:
    dump_annotations = json.load(f)

target_annotations = {}

#print (dump_annotations.keys())
#print(json.dumps(dump_annotations['schema_annotations'], indent=4))
#print(json.dumps(pattern_annotations['schema_annotations'], indent=4))
target_annotations['known_attributes'] = dump_annotations['known_attributes']
target_annotations['schema_annotations'] = pattern_annotations['schema_annotations']
target_annotations['column_annotations'] = pattern_annotations['column_annotations']
target_annotations['table_annotations'] = pattern_annotations['table_annotations']
target_annotations['catalog_annotations'] = dump_annotations['catalog_annotations']
target_annotations['foreign_key_annotations'] = dump_annotations['foreign_key_annotations']

for v in dump_annotations['column_annotations']:
    if v['schema'] in ['Vocab']:
        if  v['column'] not in ['id', 'uri', 'description', 'name', 'synonyms']:
            target_annotations['column_annotations'].append(v)
    else:
        target_annotations['column_annotations'].append(v)
        
for v in dump_annotations['table_annotations']:
    if v['schema'] == 'PDB':
        target_annotations['table_annotations'].append(v)
    elif v['schema'] == 'Vocab' and v['uri'] == 'tag:isrd.isi.edu,2016:visible-columns':
        target_annotations['table_annotations'].append(v)
        
fp = open(output, 'w')
json.dump(target_annotations, fp, indent=4)
fp.close()

