import sys
import json
from deriva.core import get_credential, DerivaServer, BaseCLI
from deriva.core.ermrest_model import Key, Column, builtin_types
import utils
from utils import ApplicationClient

pdb_admin = "https://auth.globus.org/0b98092c-3c41-11e9-a8c8-0ee7d80087ee"
isrd_staff = "https://auth.globus.org/176baec4-ed26-11e5-8e88-22000ab4b42b"
pdb_curator = "https://auth.globus.org/eef3e02a-3c40-11e9-9276-0edc9bdd56a6"
pdb_writer = "https://auth.globus.org/c94a1e5c-3c40-11e9-a5d1-0aacc65bfe9a"

acls = {
        "insert": [
            pdb_admin,
            pdb_curator,
            pdb_writer,
            isrd_staff
        ],
        "select": [
            '*'
        ],
        "update": [
            pdb_admin,
            pdb_curator,
            pdb_writer,
            isrd_staff
        ]
}

acl_bindings = {
    "self_service_creator": False
    }
def main(server_name, catalog_id, credentials):
    server = DerivaServer('https', server_name, credentials)
    catalog = server.connect_ermrest(catalog_id)
    catalog.dcctx['cid'] = "oneoff/model"
    model = catalog.getCatalogModel()
    
    """
    Create the acls and dynamic acls
    """
    utils.set_column_acls(catalog, 'PDB', 'entry', 'Deposit_Date', acls)
    utils.set_column_acl_bindings(catalog, 'PDB', 'entry', 'Deposit_Date', acl_bindings)

if __name__ == '__main__':
    args = ApplicationClient('ad-hoc table creation tool', None, 1).parse_cli()
    credentials = get_credential(args.host, args.credential_file)
    main(args.host, args.catalog_id, credentials)
    
