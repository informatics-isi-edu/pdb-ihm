import sys
import json
from deriva.core import ErmrestCatalog, AttrDict, get_credential, DEFAULT_CREDENTIAL_FILE, tag, urlquote, DerivaServer, get_credential, BaseCLI
from deriva.core.ermrest_model import builtin_types, Schema, Table, Column, Key, ForeignKey, DomainType, ArrayType
import utils
import traceback

location = {
    'ihm-extension.dic': 'https://github.com/ihmwg/IHM-dictionary/blob/master/ihm-extension.dic',
    'mmcif_pdbx.dic': 'http://mmcif.wwpdb.org/dictionaries/ascii/mmcif_pdbx_v50.dic',
    'flr-extension.dic': 'https://github.com/ihmwg/FLR-dictionary/blob/master/flr-extension.dic'
}

column = Column.define(
                    'Location',
                    builtin_types.text,
                    comment='Location of the Data Dictionary',
                    nullok=True
)

def update_Data_Dictionary_Name(catalog, model):
    try:
        utils.create_column_if_not_exist(model, 'Vocab', 'Data_Dictionary_Name', column)
        url = '/attribute/Vocab:{}/RID,Name'.format('Data_Dictionary_Name')
        resp = catalog.get(url)
        resp.raise_for_status()
        rows = resp.json()
        #print(json.dumps(rows, indent=4))
        values = []
        for row in rows:
            values.append({'RID': row['RID'], 'Location': location[row['Name']]})
        columns = ['RID', 'Location']
        url = '/attributegroup/Vocab:{}/RID;Location'.format('Data_Dictionary_Name')
        resp = catalog.put(
            url,
            json=values
        )
        resp.raise_for_status()
        print('Updated {}'.format('Data_Dictionary_Name'))
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
    Update vocabularies
    """
    update_Data_Dictionary_Name(catalog, model) 
    
# ===================================================    

if __name__ == '__main__':
    args = BaseCLI('ad-hoc table creation tool', None, 1).parse_cli()
    credentials = get_credential(args.host, args.credential_file)
    main(args.host, 1, credentials)
