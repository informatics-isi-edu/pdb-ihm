#!/usr/bin/python3

from requests import HTTPError
from deriva.core import DerivaServer, ErmrestCatalog, get_credential
from deriva.core.ermrest_model import Table, Column, Key, builtin_types
import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument('hostname')
parser.add_argument('catalog_number')
parser.add_argument('schema_name')
parser.add_argument('term_schema_name')
args = parser.parse_args()


hostname = args.hostname
catalog_number = args.catalog_number

credential = get_credential(hostname)
server = DerivaServer('https', hostname, credential)
catalog = ErmrestCatalog('https', hostname, catalog_number, credential)

model_root = catalog.getCatalogModel()

schema_name = args.schema_name
schema = model_root.schemas[schema_name]

tables_to_delete = schema.tables.keys()
tables_not_deleted = []

while len(tables_to_delete) > 0:
	for tab_name in tables_to_delete:
		try:
			model_root = catalog.getCatalogModel()
			schema = model_root.schemas[schema_name]
			tab = schema.tables[tab_name]
			tab.delete(catalog)
			print('table deleted: %s.%s' % (schema_name, tab_name))
		except:
			tables_not_deleted.append(tab_name)
	tables_to_delete = tables_not_deleted
	tables_not_deleted = []


vocab_schema_name = args.term_schema_name
schema = model_root.schemas[vocab_schema_name]
for tab_name in schema.tables.keys():
    model_root = catalog.getCatalogModel()
    schema = model_root.schemas[vocab_schema_name]
    tab = schema.tables[tab_name]
    tab.delete(catalog)
    print('table deleted: %s.%s' % (vocab_schema_name, tab_name))


