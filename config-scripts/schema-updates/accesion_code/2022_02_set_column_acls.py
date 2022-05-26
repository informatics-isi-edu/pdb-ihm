import sys
import json
from deriva.core import get_credential, DerivaServer, BaseCLI
from deriva.core.ermrest_model import Key, Column, builtin_types
import utils

pdb_admin = "https://auth.globus.org/0b98092c-3c41-11e9-a8c8-0ee7d80087ee"
isrd_staff = "https://auth.globus.org/176baec4-ed26-11e5-8e88-22000ab4b42b"
pdb_curator = "https://auth.globus.org/eef3e02a-3c40-11e9-9276-0edc9bdd56a6"

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
        "enumerate": [
            pdb_admin,
            pdb_curator,
            isrd_staff
        ],
        "update": [
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
    utils.set_column_acls(catalog, 'PDB', 'entry', 'Accession_Serial', acls)

if __name__ == '__main__':
    args = BaseCLI("ad-hoc table creation tool", None, 1).parse_cli()
    credentials = get_credential(args.host, args.credential_file)
    main(args.host, 1, credentials)
    
