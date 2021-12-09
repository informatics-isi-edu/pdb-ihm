import sys
import json
from deriva.core import ErmrestCatalog, AttrDict, get_credential, DEFAULT_CREDENTIAL_FILE, tag, urlquote, DerivaServer, get_credential, BaseCLI
from deriva.core.ermrest_model import builtin_types, Schema, Table, Column, Key, ForeignKey, DomainType, ArrayType
import utils
import traceback

def load_comfort_dictionary(catalog):
    try:
        url = '/attribute/PDB:Entry_mmCIF_File/RID,mmCIF_Schema_Version'
        resp = catalog.get(url)
        resp.raise_for_status()
        mmCIF_rows = resp.json()
        
        url = '/attribute/PDB:Data_Dictionary/RID,Version'
        resp = catalog.get(url)
        resp.raise_for_status()
        data_dictionary_rows = resp.json()
        
        rows = []
        for mmCIF_row in mmCIF_rows:
            for data_dictionary_row in data_dictionary_rows:
                if mmCIF_row['mmCIF_Schema_Version'] == data_dictionary_row['Version']:
                    rows.append({'Exported_mmCIF_RID': mmCIF_row['RID'], 'Data_Dictionary_RID': data_dictionary_row['RID']})
        
        url = '/entity/PDB:Conform_Dictionary'
        resp = catalog.post(
            url,
            json=rows
        )
        resp.raise_for_status()
        print('Successfully loaded the Conform_Dictionary.')

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
    load_comfort_dictionary(catalog) 
    
# ===================================================    

if __name__ == '__main__':
    args = BaseCLI('ad-hoc table creation tool', None, 1).parse_cli()
    credentials = get_credential(args.host, args.credential_file)
    main(args.host, 1, credentials)
    
