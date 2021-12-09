import sys
import json
from deriva.core import ErmrestCatalog, AttrDict, get_credential, DEFAULT_CREDENTIAL_FILE, tag, urlquote, DerivaServer, get_credential, BaseCLI
from deriva.core.ermrest_model import builtin_types, Schema, Table, Column, Key, ForeignKey, DomainType, ArrayType
import utils

def define_tdoc_Conform_Dictionary():
    table_name='Conform_Dictionary'
    comment='Dictionary associated to the export mmCIF file.'

    column_defs = [
        Column.define(
            'Exported_mmCIF_RID',
            builtin_types.text,
            comment='The reference to the RID of the exported mmCIF file.',
            nullok=False
        ),
        Column.define(
            'Data_Dictionary_RID',
            builtin_types.text,
            comment='The reference to the RID of the Data_Dictionary version for the mmCIF file.',
            nullok=False
        )
    ]

    key_defs = [
        Key.define(['Exported_mmCIF_RID', 'Data_Dictionary_RID'], constraint_names=[['PDB', 'Conform_Dictionary_primary_key']] ),
        Key.define(['RID'], constraint_names=[['PDB', 'Conform_Dictionary_RID_key']] ),
    ]

    fkey_defs = [
        ForeignKey.define(['Exported_mmCIF_RID'], 'PDB', 'Entry_mmCIF_File', ['RID'],
                          constraint_names=[['PDB', 'Conform_Dictionary_Entry_mmCIF_File_fkey']],
                          on_update='CASCADE',
                          on_delete='CASCADE'
        ),
        ForeignKey.define(['Data_Dictionary_RID'], 'PDB', 'Data_Dictionary', ['RID'],
                          constraint_names=[['PDB', 'Conform_Dictionary_Data_Dictionary_fkey']],
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
    utils.create_table_if_not_exist(model, 'PDB',  define_tdoc_Conform_Dictionary()) 
    
# ===================================================    

if __name__ == '__main__':
    args = BaseCLI('ad-hoc table creation tool', None, 1).parse_cli()
    credentials = get_credential(args.host, args.credential_file)
    main(args.host, 1, credentials)
    
