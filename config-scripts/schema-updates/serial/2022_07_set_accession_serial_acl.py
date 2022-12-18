import sys
import json
import traceback
from deriva.core.ermrest_model import tag as chaise_tags
from deriva.core import get_credential, DerivaServer, BaseCLI, urlquote
from deriva.core.ermrest_model import Column, builtin_types, Table, Key, ForeignKey
import utils
from utils import ApplicationClient

pdb_admin = "https://auth.globus.org/0b98092c-3c41-11e9-a8c8-0ee7d80087ee"
isrd_staff = "https://auth.globus.org/176baec4-ed26-11e5-8e88-22000ab4b42b"
pdb_curator = "https://auth.globus.org/eef3e02a-3c40-11e9-9276-0edc9bdd56a6"
pdb_submitter = "https://auth.globus.org/99da042e-64a6-11ea-ad5f-0ef992ed7ca1"

acls = {
        "insert": [
            pdb_admin,
            pdb_curator,
            isrd_staff
        ],
        "select": [
            pdb_admin,
            pdb_curator,
            isrd_staff
        ],
        "update": [
            pdb_admin,
            pdb_curator,
            isrd_staff
        ],
      "enumerate": [
            pdb_admin,
            pdb_curator,
            isrd_staff
          ]
}

def main(server_name, catalog_id, credentials):
    server = DerivaServer('https', server_name, credentials)
    catalog = server.connect_ermrest(catalog_id)
    catalog.dcctx['cid'] = "oneoff/model"
    model = catalog.getCatalogModel()
    
    """
    Create the acls
    """
    utils.set_column_acls(catalog, 'PDB', 'Accession_Code', 'Accession_Serial', acls)

if __name__ == '__main__':
    args = ApplicationClient('ad-hoc table creation tool', None, 1).parse_cli()
    credentials = get_credential(args.host, args.credential_file)
    main(args.host, args.catalog_id, credentials)

