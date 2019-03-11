import json
import python_jsonschema_objects as pjs
import deriva.core.ermrest_model as em
from collections import namedtuple
from deriva.core import ErmrestCatalog, get_credential, DerivaServer
import deriva.core.ermrest_model as em
from deriva.utils.catalog.manage.configure_catalog import DerivaCatalogConfigure, DerivaTableConfigure
import deriva.utils.catalog.components.model_elements as model_elements
from deriva.core.ermrest_config import tag as chaise_tags
import deriva.utils.catalog.components.model_elements
import csv

filename = 'json-schema-full-ihm_dev_v1_0_1.json'
#Read JSON data into the datastore variable
with open(filename, 'r') as f:
    pdb = json.load(f)

def table_schema(v):
    # A table will be represented as a array whose single item must be an object whose properties are the columns.
    return v['type'] == 'array' and v["minItems"] == 1 and v["uniqueItems"] == True

FKey = namedtuple('fkey', ['column', 'reftable', 'refcolumn']
                  )


def maptype(t):
    m = {'string': 'text',
         'integer': 'int4',
         'number': 'float4'
    }
    return m[t]

class Table():
    def __init__(self, name, dict):
        self.columns = []
        self.fkeys = []

        # A table will be represented as a array whose single item must be an object whose properties are the columns.
        self.name = name
        assert (dict['type'] == 'array' or dict['type'] == 'object')
        assert (dict['items']['type'] == 'object')
        columns = dict['items']['properties']
        for k, v in columns.items():
            self.columns.append(
                {
                    'name': k,
                    'type': maptype(v['type']),
                    'nullok': k not in dict['items']['required'],
                    'comment': v['description'],
                }
            )
            if 'enum' in v:
                vocab[(self.name, k)] = set(v['enum'])
                self.fkeys.append(FKey(k, '{}_terms'.format(k), 'id'))
        self.keys = ['id'] if 'id' in columns else []
        self.fkeys.extend([FKey(k, k.replace('_id', ''), 'id') for k in columns.keys() if '_id' in k])

vocab = {}
tables = { k:Table(k,v) for k,v in pdb['properties'].items() if table_schema(v)}
tables['_entry_id'] = {
        'nullok': False,
        'comment': pdb['properties']['_entry_id']['description'],
        'type': 'text',
        'name': '_entry_id'
    }

catalog = model_elements.DerivaCatalog('https','pdb.isrd.isi.edu',1,credentials=get_credential('pdb.isrd.isi.edu'))
schema_name = 'PDB'

schema = catalog.create_schema(schema_name, comment="PBD Schema from {}".format(pdb['schema']))

for t in tables:
    table = schema.create_table(t['name'],
                        [em.Column.define(c['name'],
                                          em.builtin_types[c['type']],
                                          nullok=c['nullok'],
                                          comment=c['comment']
                                          )
                         for c in t.columns],
                        keys=c['keys'],
                        comment=t['comment']
                        )
    table.configure_table_defaults()

for v in vocab:
    model_root.create_table(em.Table.define_vocabulary())

for t in tables:
    T.link_vo())


# Create tables
# Create vocabulary
# Create FKs

