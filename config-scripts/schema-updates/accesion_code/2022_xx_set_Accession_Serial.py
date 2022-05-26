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
    
    url = '/attribute/PDB:entry/accession_code::null::&!id::ciregexp::PDBDEV_/RID,accession_code,Accession_Serial'
    resp = catalog.get(url)
    resp.raise_for_status()
    rows = resp.json()
    accession_serial = 112
    updates  = []
    for row in rows:
        accession_serial +=1
        updates.append({'RID': row['RID'],
                    'Accession_Serial': accession_serial    
            })
    url = '/attributegroup/PDB:entry/RID;Accession_Serial'
    resp = catalog.put(
        url,
        json=updates
    )
    resp.raise_for_status()
    print('Execute:\nselect setval(\'"PDB"."entry_Accession_Serial_seq"\', {});'.format(accession_serial))
    
# ===================================================    

if __name__ == '__main__':
    args = BaseCLI('ad-hoc table creation tool', None, 1).parse_cli()
    credentials = get_credential(args.host, args.credential_file)
    main(args.host, 1, credentials)
    
