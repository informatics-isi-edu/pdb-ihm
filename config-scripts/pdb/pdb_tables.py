#!/usr/bin/python3

import json
#import python_jsonschema_objects as pjs
from collections import namedtuple
import csv
import pickle
import argparse
import sys
import traceback

parser = argparse.ArgumentParser()
parser.add_argument('filename')
parser.add_argument('output')
args = parser.parse_args()

filename = args.filename
output = args.output

# Read JSON data into the datastore variable
with open(filename, 'r') as f:
    pdb = json.load(f)


def table_schema(v):
    # A table will be represented as a array whose single item must be an object whose properties are the columns.
    return v['type'] == 'array' or v['type'] == 'object'
    # return v['type'] == 'array' and v["minItems"] == 1 and v["uniqueItems"] == True


FKey = namedtuple('fkey', ['column', 'reftable', 'refcolumn'])


def maptype(t):
    m = {'string': 'text',
         'integer': 'int4',
         'number': 'float4'
         }
    return m[t]


def nullOK(t):
    if t['type'] == 'object':
        return t['required']
    elif t['type'] == 'array':
        return t['items']['required']


def refertype(v):
    refer_column = v.get('$ref', '')
    if not refer_column or refer_column[0] != '#' or '/' not in refer_column:
        return None
    else:
        pair = refer_column[1:].split('/')
        refer_tab = pair[0]
        refer_col = pair[1]

        if pdb['properties'][refer_tab]['type'] == 'object':
            parent_col = pdb['properties'][refer_tab]['properties'][refer_col]
        elif pdb['properties'][refer_tab]['type'] == 'array':
            parent_col = pdb['properties'][refer_tab]['items']['properties'][refer_col]

        if '$ref' in parent_col.keys():
            return refertype(parent_col)
        return maptype(parent_col['type'])

def referRootColumn(table_name,col_name,v,column_desc_dict):
    if '$ref' not in v.keys():
        return (table_name, col_name)
    refer_column = v.get('$ref', '')
    if refer_column[0] != '#' or '/' not in refer_column:
        return None
    else:
        pair = refer_column[1:].split('/')
        refer_tab = pair[0]
        refer_col = pair[1]

        if pdb['properties'][refer_tab]['type'] == 'object':
            parent_col = pdb['properties'][refer_tab]['properties'][refer_col]
        elif pdb['properties'][refer_tab]['type'] == 'array':
            parent_col = pdb['properties'][refer_tab]['items']['properties'][refer_col]

        return referRootColumn(refer_tab,refer_col,parent_col,column_desc_dict)




def getColumnDesc():
    if not pdb:
        return None
    res = {}
    for tname, t in pdb['properties'].items():
        if tname in ['_entry_id', '_schema_version']:
            continue
        elif t['type'] == 'object':
            columns = t['properties']
        elif t['type'] == 'array':
            columns = t['items']['properties']

        for k, v in columns.items():
            if 'description' in v.keys():
                res[(tname,k)] = v['description']
    return res

class Table():
    def __init__(self, name, dict):
        self.columns = []
        self.fkeys = []
        self.pkey_columns = []
        self.vocab = {}

        # A table will be represented as a array whose single item must be an object whose properties are the columns.
        self.name = name

        assert (dict['type'] == 'array' or dict['type'] == 'object')
        # assert (dict['items']['type'] == 'object')

        if dict['type'] == 'object':
            columns = dict['properties']
        elif dict['type'] == 'array':
            columns = dict['items']['properties']

        for k, v in columns.items():
            try:
                column_type = maptype(v['type']) if 'type' in v.keys() else refertype(v)
            except:
                print ('k={}, v={}'.format(k,v))
                print ('v.keys(): {}'.format(v.keys()))
                et, ev, tb = sys.exc_info()
                print('got exception "%s"' % str(ev))
                print('%s' % str(traceback.format_exception(et, ev, tb)))
                sys.exit(1)
                
            if 'examples' in v.keys():
                example_info = ','.join(v['examples'])
            else:
                example_info = ''

            hasDescription = False
            if 'description' in v.keys():
                comment_str = v['description']
                hasDescription = True
            else:
                tab_col_key = referRootColumn(name,k,v,column_des_dict)
                if tab_col_key:
                    #comment_str = column_des_dict.get(tab_col_key,'')
                    table_name, col_name = tab_col_key
                    comment_str = 'A reference to table %s.%s.' % (table_name, col_name)
                else:
                    comment_str = ''
            if not comment_str or comment_str == '':
                print('missing description {}:{}'.format(name,k))
            elif hasDescription == True:
                comment_str = 'type:{}\n{}'.format(column_type,comment_str)

            if example_info:
                comment_str = '{}\nexamples:{}'.format(comment_str, example_info)

            #comment_str = comment_str.replace('\n', '</br>')
            self.columns.append(
                {
                    'name': k,
                    'type': column_type,
                    'nullok': k not in nullOK(dict),
                    'comment': comment_str,
                }
            )
            if 'enum' in v:
                self.vocab[(self.name, k)] = set(v['enum'])
                vocab_table_name = '{}_{}_term'.format(self.name, k)
                # limit of 63,
                vocab_table_name = vocab_table_name[-50:]
                if v['type'] == 'integer':
                    # if enum is integer type, skip it for now
                    pass
                else:
                    self.fkeys.append(FKey(k, vocab_table_name, 'ID'))
            if '_primary_key' in v:
                self.pkey_columns.extend([k])

        if 'structure_id' not in columns.keys():
            print('Table %s has not the column structure_id as a key.' % self.name)
            self.columns.append(
                {
                    'name': 'structure_id',
                    'type': 'text',
                    'nullok': False,
                    'comment': 'unique id for each entry in database',
                }
            )


column_des_dict = getColumnDesc()
tables = {k: Table(k, v) for k, v in pdb['properties'].items() if table_schema(v)}
json_tables = {}
for k,t in tables.items():
    t_json = {}
    t_json['name'] = t.name
    t_json['columns'] = t.columns
    vocab = {}
    for k, v in t.vocab:
        k = '{}'.format(k)
        vocab[k] = v
    t_json['vocab'] = vocab
    fkeys = []
    for fk in t.fkeys:
        fkeys.append({
            'column': fk.column,
            'reftable': fk.reftable,
            'refcolumn': fk.refcolumn
            })
    t_json['fkeys'] = fkeys
    t_json['pkey_columns'] = t.pkey_columns
    json_tables[k] = t_json
fw = open(output, 'w')
json.dump(json_tables, fw, indent=4)
fw.close()


