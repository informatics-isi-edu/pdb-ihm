import sys
import json
from deriva.core import ErmrestCatalog, AttrDict, get_credential, DEFAULT_CREDENTIAL_FILE, tag, urlquote, DerivaServer, get_credential, BaseCLI
from deriva.core.ermrest_model import builtin_types, Schema, Table, Column, Key, ForeignKey, DomainType, ArrayType
import utils


"""
def define_tdoc_ihm():
    table_name='...'
    comment='...'

    column_defs = [
        Column.define(
            '...',
            builtin_types....,
            comment='...',
            nullok=...
        ),
        ...
    ]
    key_defs = [
        Key.define(['...', '...'], constraint_names=[['PDB', 'ihm_..._key']] ),
        ...
    ]

    fkey_defs = [
        ForeignKey.define(['...'], 'PDB', '...', ['...'],
                          constraint_names=[['PDB', 'ihm_..._fkey']],
                          on_update='CASCADE',
                          on_delete='NO ACTION'
        ),
        ...
    ]

    table_def = Table.define(
        table_name,
        column_defs,
        key_defs=key_defs,
        fkey_defs=fkey_defs,
        comment=comment,
        provide_system=True
    )

    return table_def
"""


# ============================================================
def main(server_name, catalog_id, credentials):
    server = DerivaServer('https', server_name, credentials)
    catalog = server.connect_ermrest(catalog_id)
    catalog.dcctx['cid'] = 'oneoff/model'
    model = catalog.getCatalogModel()

    #create_table_if_not_exist(model, 'PDB', define_tdoc_ihm())

# ===================================================    

if __name__ == '__main__':
    args = BaseCLI('ad-hoc table creation tool', None, 1).parse_cli()
    credentials = get_credential(args.host, args.credential_file)
#    if args.catalog is None:
#        catalog_id = 99

    main(args.host, 99, credentials)
    
