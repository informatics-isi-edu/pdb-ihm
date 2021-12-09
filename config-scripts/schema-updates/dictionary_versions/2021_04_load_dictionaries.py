import sys
import json
from deriva.core import ErmrestCatalog, AttrDict, get_credential, DEFAULT_CREDENTIAL_FILE, tag, urlquote, DerivaServer, get_credential, BaseCLI
from deriva.core.ermrest_model import builtin_types, Schema, Table, Column, Key, ForeignKey, DomainType, ArrayType
import utils
import traceback

data_dictionary_rows = [
    {'Name': 'ihm-extension.dic', 'Category': 'IHM-dictionary', 'Version': '1.0', 'Location': 'https://github.com/ihmwg/IHM-dictionary/blob/fd3ef4bfdf6cf0901302c0498e118199c0cb9b59/ihm-extension.dic'},
    {'Name': 'ihm-extension.dic', 'Category': 'IHM-dictionary', 'Version': '1.17', 'Location': 'https://github.com/ihmwg/IHM-dictionary/blob/f15a6bb9a9581340c3311a7b5851ce9b5bac2242/ihm-extension.dic'},
    {'Name': 'mmcif_pdbx.dic', 'Category': 'PDBx/mmCIF', 'Version': '5.342', 'Location': ' https://github.com/wwpdb-dictionaries/mmcif_pdbx/blob/d1f04bc6d400e0531f53c612145c4e72d5c26bd2/dist/mmcif_pdbx_v50.dic'},
    {'Name': 'flr-extension.dic', 'Category': 'FLR-dictionary', 'Version': '0.007', 'Location': 'https://github.com/ihmwg/FLR-dictionary/blob/c850a8afea88a188ac6776f595306fb2f45311ca/flr-extension.dic'}
]

supported_dictionary_rows = [
    {'Data_Dictionary_RID': 'ihm-extension.dic', 'Data_Dictionary_Category': 'IHM-dictionary'},
    {'Data_Dictionary_RID': 'mmcif_pdbx.dic', 'Data_Dictionary_Category': 'PDBx/mmCIF'}
]

def load_dictionaries(catalog):
    try:
        url = '/entity/PDB:Data_Dictionary'
        resp = catalog.post(
            url,
            json=data_dictionary_rows
        )
        resp.raise_for_status()
        rows = resp.json()
        supported_dictionary_rows[0]['Data_Dictionary_RID'] = rows[1]['RID']
        supported_dictionary_rows[1]['Data_Dictionary_RID'] = rows[2]['RID']
        
        url = '/entity/PDB:Supported_Dictionary'
        resp = catalog.post(
            url,
            json=supported_dictionary_rows
        )
        resp.raise_for_status()
        print('Successfully loaded the dictionary tables.')

    except:
        et, ev, tb = sys.exc_info()
        print('got exception "%s"' % str(ev))
        print('%s' % ''.join(traceback.format_exception(et, ev, tb)))

# ============================================================
def main(server_name, catalog_id, credentials):
    server = DerivaServer('https', server_name, credentials)
    catalog = server.connect_ermrest(catalog_id)
    catalog.dcctx['cid'] = 'oneoff/model'
    model = catalog.getCatalogModel()
    
    """
    Create table
    """
    load_dictionaries(catalog) 
    
# ===================================================    

if __name__ == '__main__':
    args = BaseCLI('ad-hoc table creation tool', None, 1).parse_cli()
    credentials = get_credential(args.host, args.credential_file)
    main(args.host, 1, credentials)
    
