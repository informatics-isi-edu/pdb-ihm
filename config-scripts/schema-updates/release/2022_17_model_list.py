import sys
import json
from deriva.core.ermrest_model import tag as chaise_tags
from deriva.core import get_credential, DerivaServer, BaseCLI
from deriva.core.ermrest_model import Key, Column, builtin_types
import utils
from utils import ApplicationClient

pdb_admin = "https://auth.globus.org/0b98092c-3c41-11e9-a8c8-0ee7d80087ee"
isrd_staff = "https://auth.globus.org/176baec4-ed26-11e5-8e88-22000ab4b42b"
pdb_curator = "https://auth.globus.org/eef3e02a-3c40-11e9-9276-0edc9bdd56a6"

acls = {
  "delete": [
    pdb_admin,
    isrd_staff,
    pdb_curator
  ],
  "insert": [
    pdb_admin,
    isrd_staff,
    pdb_curator
  ],
  "select": ['*'],
  "update": [
    pdb_admin,
    isrd_staff,
    pdb_curator
  ],
  "enumerate": ['*']
}

def main(server_name, catalog_id, credentials):
    server = DerivaServer('https', server_name, credentials)
    catalog = server.connect_ermrest(catalog_id)
    catalog.dcctx['cid'] = "oneoff/model"
    model = catalog.getCatalogModel()
    
    table = model.schemas['PDB'].tables['ihm_model_list']
    annotations = table.annotations
    del annotations[chaise_tags['generated']]
    model.apply()
    print('Deleted the annotation "generated" from the "ihm_model_list" table.')

    """
    Create the acls
    """
    utils.set_table_acls(catalog, 'PDB', 'ihm_model_list', acls)

if __name__ == '__main__':
    args = ApplicationClient('ad-hoc table creation tool', None, 1).parse_cli()
    credentials = get_credential(args.host, args.credential_file)
    main(args.host, args.catalog_id, credentials)
    
