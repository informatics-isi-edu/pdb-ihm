import sys
import json
from deriva.core import get_credential, DerivaServer, BaseCLI
from deriva.core.ermrest_model import Key, Column, builtin_types
import utils

Supported_Dictionary_columns = ['Data_Dictionary_RID', 'Data_Dictionary_Category']

Supported_Dictionary_rows = [
    {'RID': '1-RE2T', 'Data_Dictionary_RID': '3-A45E', 'Data_Dictionary_Category': 'IHMCIF dictionary'},
    {'RID': '1-RE2W', 'Data_Dictionary_RID': '3-A45G', 'Data_Dictionary_Category': 'PDBx/mmCIF'}
    ]

def main(server_name, catalog_id, credentials):
    server = DerivaServer('https', server_name, credentials)
    catalog = server.connect_ermrest(catalog_id)
    catalog.dcctx['cid'] = "oneoff/model"
    model = catalog.getCatalogModel()
    
    """
    Update rows in Supported_Dictionary table
    """
    utils.update_rows(catalog, 'PDB', 'Supported_Dictionary', Supported_Dictionary_columns, Supported_Dictionary_rows, column_key='RID')

if __name__ == '__main__':
    args = BaseCLI("ad-hoc table creation tool", None, 1).parse_cli()
    credentials = get_credential(args.host, args.credential_file)

    main(args.host, 1, credentials)
    
