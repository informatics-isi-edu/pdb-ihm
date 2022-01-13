import sys
import json
from deriva.core import ErmrestCatalog, AttrDict, get_credential, DEFAULT_CREDENTIAL_FILE, tag, urlquote, DerivaServer, get_credential, BaseCLI
from deriva.core.ermrest_model import builtin_types, Schema, Table, Column, Key, ForeignKey, DomainType, ArrayType
import utils
import traceback

tables = [
    'chem_comp_mon_nstd_flag',
    'chem_comp_atom_substruct_code',
    'chem_comp_atom_pdbx_stereo_config',
    'chem_comp_atom_pdbx_aromatic_flag',
    'chem_comp_atom_pdbx_leaving_atom_flag',
    'entity_src_method',
    'entity_type',
    'entity_poly_nstd_chirality',
    'entity_poly_nstd_linkage',
    'entity_poly_nstd_monomer',
    'entity_poly_seq_hetero',
    'struct_asym_pdbx_type'
]

def update_vocabularies(catalog):
    try:
        for table in tables:
            url = '/attribute/Vocab:{}/RID,Name'.format(table)
            resp = catalog.get(url)
            resp.raise_for_status()
            rows = resp.json()
            values = []
            for row in rows:
                values.append({'RID': row['RID'], 'Name': row['Name'].upper()})
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
    schema = model.schemas['Vocab']

    
    for table_name in tables:
        table = schema.tables[table_name]
        referenced_by = table.referenced_by
        if len(referenced_by) != 1:
            print('Table {} has more than 1 FK'.format(table_name))
        else:
            referenced_by = referenced_by[0]
            schema_name = referenced_by.constraint_schema.name
            tname = referenced_by.table.name
            fk_name = referenced_by.constraint_name
            utils.alter_on_update_fkey_if_exist(model, schema_name, tname, fk_name, 'CASCADE')
    """
    Update vocabularies
    """
    update_vocabularies(catalog) 
    print('Updated the vocabulary tables.')
    
# ===================================================    

if __name__ == '__main__':
    args = BaseCLI('ad-hoc table creation tool', None, 1).parse_cli()
    credentials = get_credential(args.host, args.credential_file)
    main(args.host, 1, credentials)
