import sys
import json
from deriva.core import get_credential, DerivaServer, BaseCLI
from deriva.core.ermrest_model import Key, Column, builtin_types
import utils

pdb_admin = "https://auth.globus.org/0b98092c-3c41-11e9-a8c8-0ee7d80087ee"
isrd_staff = "https://auth.globus.org/176baec4-ed26-11e5-8e88-22000ab4b42b"

acls = {
        "owner": [
            pdb_admin,
            isrd_staff
        ],
        "write": [],
        "delete": [
            pdb_admin,
            isrd_staff
        ],
        "insert": [
            pdb_admin,
            isrd_staff
        ],
        "select": [
            "*"
        ],
        "update": [
            pdb_admin,
            isrd_staff
        ],
        "enumerate": [
            "*"
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
    utils.set_table_acls(catalog, 'PDB', 'Data_Dictionary', acls)
    utils.set_table_acls(catalog, 'PDB', 'Supported_Dictionary', acls)

if __name__ == '__main__':
    args = BaseCLI("ad-hoc table creation tool", None, 1).parse_cli()
    credentials = get_credential(args.host, args.credential_file)
    main(args.host, 1, credentials)
    
