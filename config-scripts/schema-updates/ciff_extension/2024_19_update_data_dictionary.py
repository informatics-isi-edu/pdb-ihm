import sys
import json
from deriva.core import get_credential, DerivaServer, BaseCLI
from deriva.core.ermrest_model import Key, Column, builtin_types
import utils

Data_Dictionary_rows = [
        {'Name': 'mmcif_ihm_ext.dic', 'Category': 'IHMCIF dictionary', 'Version': '1.26', 'Location': 'https://raw.githubusercontent.com/ihmwg/IHMCIF/master/archive/mmcif_ihm_ext-v1.26.dic'},
        {'Name': 'mmcif_pdbx.dic', 'Category': 'PDBx/mmCIF', 'Version': '5.395', 'Location': 'https://raw.githubusercontent.com/wwpdb-dictionaries/mmcif_pdbx/8d720719217bbeb36093992956e346448876c458/archive/mmcif_pdbx_v50-v5.395.dic'},
        {'Name': 'mmcif_ihm_flr_ext.dic', 'Category': 'FLRCIF dictionary', 'Version': '0.01', 'Location': 'https://raw.githubusercontent.com/ihmwg/flrCIF/master/archive/mmcif_ihm_flr_ext-v0.01.dic'}
    ]

def main(server_name, catalog_id, credentials):
    server = DerivaServer('https', server_name, credentials)
    catalog = server.connect_ermrest(catalog_id)
    catalog.dcctx['cid'] = "oneoff/model"
    model = catalog.getCatalogModel()

    """
    Create new rows in Data_Dictionary table
    """
    utils.insert_rows(catalog, 'PDB', 'Data_Dictionary', Data_Dictionary_rows)

if __name__ == '__main__':
    args = BaseCLI("ad-hoc table creation tool", None, 1).parse_cli()
    credentials = get_credential(args.host, args.credential_file)

    main(args.host, 1, credentials)
    
