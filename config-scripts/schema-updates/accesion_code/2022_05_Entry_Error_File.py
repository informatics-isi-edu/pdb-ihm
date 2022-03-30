import sys
import json
from deriva.core import ErmrestCatalog, AttrDict, get_credential, DEFAULT_CREDENTIAL_FILE, tag, urlquote, DerivaServer, get_credential, BaseCLI
from deriva.core.ermrest_model import builtin_types, Schema, Table, Column, Key, ForeignKey, DomainType, ArrayType
import utils


# ========================================================
# -- create a table that is not a Vocab structure
# -- define ihm_pseudo_site table --> Brida reviewed
def define_tdoc_Entry_Error_File():
    table_name='Entry_Error_File'
    comment='Keeps track of the files involved in mmCIF validation failures'

    column_defs = [
        Column.define(
            'Entry_RID',
            builtin_types.text,
            nullok=False,
            comment='A reference to the entry table'
        ),
        Column.define(
            'File_Type',
            builtin_types.text,
            nullok=False,
            comment='Validation failure file type: diag_log, parser_log, mmCIF'
        ),
        Column.define(
            'File_Name',
            builtin_types.text,
            nullok=False,
            comment='The name of the system generated file'
        ),
        Column.define(
            'File_URL',
            builtin_types.text,
            nullok=False,
            comment='URL of the system generated file',
            acls={
                'select': [
                  '*'
                ]
              },
            acl_bindings={
                'no_binding': False
              },
        ),
        Column.define(
            'File_Bytes',
            builtin_types.int8,
            nullok=False,
            comment='Size of the system generated file in bytes'
        ),
        Column.define(
            'File_MD5',
            builtin_types.text,
            nullok=False,
            comment='MD5 of the system generated file'
        )
    ]

    key_defs = [
        Key.define(['Entry_RID', 'File_Type'], constraint_names=[['PDB', 'Entry_Error_File_primary_key']] )
    ]

    fkey_defs = [
        ForeignKey.define(['Entry_RID'], 'PDB', 'entry', ['RID'],
                          constraint_names=[['PDB', 'Entry_Error_File_Entry_RID_fkey']],
                          on_update='CASCADE',
                          on_delete='NO ACTION'   
        ),
        ForeignKey.define(['File_Type'], 'Vocab', 'Validation_File_Type', ['Name'],
                          constraint_names=[['PDB', 'Entry_Error_File_File_Type_fkey']],
                          on_update='CASCADE',
                          on_delete='NO ACTION'
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
    Drop table
    """
    utils.drop_table(catalog, 'PDB', 'Entry_Error_File')
    
    model = catalog.getCatalogModel()

    """
    Create table
    """
    utils.create_table_if_not_exist(model, 'PDB',  define_tdoc_Entry_Error_File())
        
# ===================================================    

if __name__ == '__main__':
    args = BaseCLI('ad-hoc table creation tool', None, 1).parse_cli()
    credentials = get_credential(args.host, args.credential_file)

    main(args.host, 1, credentials)
    
