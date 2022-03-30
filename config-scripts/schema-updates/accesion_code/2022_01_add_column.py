import sys
import json
from deriva.core import ErmrestCatalog, AttrDict, get_credential, DEFAULT_CREDENTIAL_FILE, tag, urlquote, DerivaServer, get_credential, BaseCLI
from deriva.core.ermrest_model import builtin_types, Schema, Table, Column, Key, ForeignKey, DomainType, ArrayType
import utils
import re

# ============================================================
def main(server_name, catalog_id, credentials):
    server = DerivaServer('https', server_name, credentials)
    catalog = server.connect_ermrest(catalog_id)
    catalog.dcctx['cid'] = 'oneoff/model'
    model = catalog.getCatalogModel()
    
    """
    Drop column if exists
    """
    utils.drop_column_if_exist(model, 'PDB', 'entry', 'Accession_Serial')

    """
    Create column Accession_Serial
    """
    model = catalog.getCatalogModel()
    utils.create_column_if_not_exist(model, 'PDB', 'entry', 
                                     Column.define(
                                        'Accession_Serial',
                                        builtin_types.serial4,
                                        comment='The Accession Serial value.',
                                        nullok=False
                                    ))
    
    url = '/aggregate/PDB:entry/max:=max(Accession_Serial)'
    resp = catalog.get(url)
    resp.raise_for_status()
    rows = resp.json()
    offset = rows[0]['max']
    print('offset: {}'.format(offset))
    url = '/attribute/PDB:entry/RID,accession_code,Accession_Serial'
    resp = catalog.get(url)
    resp.raise_for_status()
    rows = resp.json()
    updates  = []
    for row in rows:
        accession_code = row['accession_code']
        if accession_code != None:
            suffix = accession_code[accession_code.rfind('_')+1:]
            match = re.search(r'[^0]', suffix)
            accession_serial = int(suffix[match.start():])
        else:
            offset +=1
            accession_serial = offset
        updates.append({'RID': row['RID'],
                    'Accession_Serial': accession_serial    
            })
    url = '/attributegroup/PDB:entry/RID;Accession_Serial'
    resp = catalog.put(
        url,
        json=updates
    )
    resp.raise_for_status()
    print('Execute:\nselect setval(\'"PDB"."entry_Accession_Serial_seq"\', {});'.format(offset))
    
# ===================================================    

if __name__ == '__main__':
    args = BaseCLI('ad-hoc table creation tool', None, 1).parse_cli()
    credentials = get_credential(args.host, args.credential_file)
    main(args.host, 1, credentials)
    
