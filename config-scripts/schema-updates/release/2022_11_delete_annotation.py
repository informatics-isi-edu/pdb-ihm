#!/usr/bin/python3

import sys
import json
from deriva.core.ermrest_model import tag as chaise_tags
from deriva.core import get_credential, DerivaServer, BaseCLI
from deriva.core.ermrest_model import Key, Column, builtin_types
import utils
from utils import ApplicationClient

def main(server_name, catalog_id, credentials):
    server = DerivaServer('https', server_name, credentials)
    catalog = server.connect_ermrest(catalog_id)
    catalog.dcctx['cid'] = "oneoff/model"
    model = catalog.getCatalogModel()
    
    table = model.schemas['PDB'].tables['entity_poly']
    annotations = table.annotations
    del annotations[chaise_tags['generated']]
    model.apply()
    print('Deleted the annotation "generated" from the "entity_poly" table.')

if __name__ == '__main__':
    args = ApplicationClient('ad-hoc table creation tool', None, 1).parse_cli()
    credentials = get_credential(args.host, args.credential_file)
    main(args.host, args.catalog_id, credentials)
    
