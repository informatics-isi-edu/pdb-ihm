import sys
import json
from deriva.core import ErmrestCatalog, AttrDict, get_credential, DEFAULT_CREDENTIAL_FILE, tag, urlquote, DerivaServer, get_credential, BaseCLI
from deriva.core.ermrest_model import builtin_types, Schema, Table, Column, Key, ForeignKey, DomainType, ArrayType
import utils

def define_tdoc_Supported_Dictionary():
    table_name='Supported_Dictionary'
    comment='Dictionary containing the latest supported versions.'

    column_defs = [
        Column.define(
            'Data_Dictionary_RID',
            builtin_types.text,
            comment='The reference to the RID of the latest Data_Dictionary version',
            nullok=False
        ),
        Column.define(
            'Data_Dictionary_Category',
            builtin_types.text,
            comment='The reference to the category of the latest Data_Dictionary version',
            nullok=False
        )
    ]

    key_defs = [
        Key.define(['Data_Dictionary_Category'], constraint_names=[['PDB', 'Supported_Dictionary_primary_key']] ),
        Key.define(['RID'], constraint_names=[['PDB', 'Supported_Dictionary_RID_key']] ),
    ]

    fkey_defs = [
        ForeignKey.define(['Data_Dictionary_RID', 'Data_Dictionary_Category'], 'PDB', 'Data_Dictionary', ['RID', 'Category'],
                          constraint_names=[['PDB', 'Supported_Dictionary_fkey']],
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
    utils.create_table_if_not_exist(model, 'PDB',  define_tdoc_Supported_Dictionary()) 
    
# ===================================================    

if __name__ == '__main__':
    args = BaseCLI('ad-hoc table creation tool', None, 1).parse_cli()
    credentials = get_credential(args.host, args.credential_file)
    main(args.host, 1, credentials)
    
