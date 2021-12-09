import sys
import json
from deriva.core import ErmrestCatalog, AttrDict, get_credential, DEFAULT_CREDENTIAL_FILE, tag, urlquote, DerivaServer, get_credential, BaseCLI
from deriva.core.ermrest_model import builtin_types, Schema, Table, Column, Key, ForeignKey, DomainType, ArrayType
import utils
import traceback

tables = [
    'sub_sample_flag',
    'ihm_probe_list_reactive_probe_flag',
    'ihm_poly_probe_position_mutation_flag',
    'ihm_poly_probe_position_modification_flag',
    'ihm_poly_probe_conjugate_ambiguous_stoichiometry_flag',
    'pseudo_site_flag'
]

def update_vocabularies(catalog):
    try:
        for table in tables:
            url = '/attribute/Vocab:{}/RID,Name'.format(table)
            resp = catalog.get(url)
            resp.raise_for_status()
            rows = resp.json()
            #print(json.dumps(rows, indent=4))
            values = []
            for row in rows:
                newValue = 'YES'
                if row['Name'].upper() == 'NO':
                    newValue = 'NO'
                values.append({'RID': row['RID'], 'Name': newValue})
            #print(json.dumps(values, indent=4))
            #print('\n\n\n')
            columns = ['RID', 'Name']
            url = '/attributegroup/Vocab:{}/RID;Name'.format(table)
            resp = catalog.put(
                url,
                json=values
            )
            resp.raise_for_status()
            print('Updated {}'.format(table))
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
    
    utils.alter_on_update_fkey_if_exist(model, 'PDB', 'ihm_poly_probe_position', 'ihm_poly_probe_position_mutation_flag_fkey', 'CASCADE')
    utils.alter_on_update_fkey_if_exist(model, 'PDB', 'ihm_poly_probe_position', 'ihm_poly_probe_position_modification_flag_fkey', 'CASCADE')
    """
    Update vocabularies
    """
    update_vocabularies(catalog) 
    
# ===================================================    

if __name__ == '__main__':
    args = BaseCLI('ad-hoc table creation tool', None, 1).parse_cli()
    credentials = get_credential(args.host, args.credential_file)
    main(args.host, 1, credentials)
