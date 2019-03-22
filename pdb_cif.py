import json
import python_jsonschema_objects as pjs
import deriva.core.ermrest_model as em
from collections import namedtuple
from deriva.core import ErmrestCatalog, get_credential, DerivaServer
from deriva.utils.catalog.manage.configure_catalog import DerivaCatalogConfigure, DerivaTableConfigure
import deriva.utils.catalog.components.model_elements as model_elements
from deriva.core.ermrest_config import tag as chaise_tags
import csv

filename = 'json-schema-full-ihm_dev_v1_0_1.json'
# Read JSON data into the datastore variable
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
tables = {k: Table(k, v) for k, v in pdb['properties'].items() if table_schema(v)}
tables['_entry_id'] = {
    'nullok': False,
    'comment': pdb['properties']['_entry_id']['description'],
    'type': 'text',
    'name': '_entry_id'
}

hostname = 'pdb.isrd.isi.edu'
credential = get_credential(hostname)
catalog_ermrest = ErmrestCatalog('https', hostname, 1, credentials=credential)

catalog = model_elements.DerivaCatalog(catalog_ermrest)
schema_name = 'PDB'

if schema_name not in catalog.model.schemas.keys():
    schema = catalog.create_schema(schema_name, comment=pdb['title'])
else:
    schema = catalog.model.schemas[schema_name]



for tname, t in tables.items():
    if tname == '_entry_id':
        continue
    table = schema.create_table(catalog_ermrest, em.Table.define(tname,
                                                                 [em.Column.define(c['name'],
                                                                                   em.builtin_types[c['type']],
                                                                                   nullok=c['nullok'],
                                                                                   comment=c['comment']
                                                                                   ) for c in t.columns]
                                                                 # key_defs=t.keys
                                                                 ))

    table = DerivaTableConfigure(catalog,schema_name,tname)
    table.configure_table_defaults()
    # table.apply()

# model_root = catalog_ermrest.getCatalogModel()
# for v in vocab:
#     model_root.create_table(em.Table.define_vocabulary())

# for t in tables:
#     T.link_vo()

# Create tables
# Create vocabulary
# Create FKs
