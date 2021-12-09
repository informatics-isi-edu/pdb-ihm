import sys
import json
from deriva.core import ErmrestCatalog, AttrDict, get_credential, DEFAULT_CREDENTIAL_FILE, tag, urlquote, DerivaServer, get_credential, BaseCLI
from deriva.core.ermrest_model import builtin_types, Schema, Table, Column, Key, ForeignKey, DomainType, ArrayType
import utils

def define_tdoc_Data_Dictionary():
    table_name='Data_Dictionary'
    comment='Dictionary containing all available versions.'

    column_defs = [
        Column.define(
            'Name',
            builtin_types.text,
            comment='The name of the dictionary',
            nullok=False
        ),
        Column.define(
            'Category',
            builtin_types.text,
            comment='The category of the dictionary',
            nullok=False
        ),
        Column.define(
            'Version',
            builtin_types.text,
            comment='The version of the dictionary',
            nullok=False
        ),
        Column.define(
            'Location',
            builtin_types.text,
            comment='The location of the dictionary',
            nullok=False
        )
    ]

    key_defs = [
        Key.define(['Name', 'Version'], constraint_names=[['PDB', 'Data_Dictionary_primary_key']] ),
        Key.define(['RID', 'Category'], constraint_names=[['PDB', 'Data_Dictionary_RID_Category_key']] ),
        Key.define(['RID'], constraint_names=[['PDB', 'Data_Dictionary_RID_key']] ),
    ]

    fkey_defs = [
        ForeignKey.define(['Name'], 'Vocab', 'Data_Dictionary_Name', ['Name'],
                          constraint_names=[['PDB', 'Data_Dictionary_Name_fkey']],
                          on_update='CASCADE',
                          on_delete='CASCADE'
        ),
        ForeignKey.define(['Category'], 'Vocab', 'Data_Dictionary_Category', ['Name'],
                          constraint_names=[['PDB', 'Data_Dictionary_Category_fkey']],
                          on_update='CASCADE',
                          on_delete='CASCADE'
        )

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


# ============================================================
def main(server_name, catalog_id, credentials):
    server = DerivaServer('https', server_name, credentials)
    catalog = server.connect_ermrest(catalog_id)
    catalog.dcctx['cid'] = 'oneoff/model'
    model = catalog.getCatalogModel()
    
    """
    Create table
    """
    utils.create_table_if_not_exist(model, 'PDB',  define_tdoc_Data_Dictionary()) 
    
# ===================================================    

if __name__ == '__main__':
    args = BaseCLI('ad-hoc table creation tool', None, 1).parse_cli()
    credentials = get_credential(args.host, args.credential_file)
    main(args.host, 1, credentials)
    
