import sys
import json
from deriva.core import ErmrestCatalog, AttrDict, get_credential, DEFAULT_CREDENTIAL_FILE, tag, urlquote, DerivaServer, BaseCLI
from deriva.core.ermrest_model import builtin_types, Schema, Table, Column, Key, ForeignKey, DomainType, ArrayType
from deriva.utils.extras.model import create_vocab_tdoc
from deriva.utils.extras.data import insert_if_not_exist
import utils

# ========================================================
# -- create tables for IHMV (https://github.com/informatics-isi-edu/pdb-ihm/issues/278)
def define_tdoc_IHMV_Structure_mmCIF():
    table_name='Structure_mmCIF'
    comment='Input integrative structure mmCIF file for generation of validation report'

    column_defs = [
        Column.define(
            'Title',
            builtin_types.text,
            comment='Structure title',
            nullok=False
        ),
        Column.define(
            'File_URL',
            builtin_types.text,
            comment='Uploaded mmCIF file location',
            nullok=False
        ),
        Column.define(
            'File_Name',
            builtin_types.text,
            comment='Uploaded mmCIF file name',
            nullok=False
        ),
        Column.define(
            'File_Bytes',
            builtin_types.int8,
            comment='Uploaded mmCIF file size in bytes',
            nullok=False
        ),
        Column.define(
            'File_MD5',
            builtin_types.text,
            comment='Uploaded mmCIF file MD5',
            nullok=False
        ),
        Column.define(
            'Description',
            builtin_types.markdown,
            comment='Additional description of the structure and/or the uploaded file',
            nullok=True
        ),
        Column.define(
            'Processing_Status',
            builtin_types.text,
            comment='Workflow processing status for validation report generation',
            nullok=False,
            default="New"
        ),
        Column.define(
            'Processing_Details',
            builtin_types.markdown,
            comment='Captures log and error messages related to the processing status',
            nullok=True
        )
    ]
    key_defs = [
        Key.define(['RID'], constraint_names=[['IHMV', 'Structure_mmCIF_RID_key']]),
        Key.define(['RCB', 'Title'], constraint_names=[['IHMV', 'Structure_mmCIF_RCB_Title_key']]),
        Key.define(['RCB', 'File_MD5'], constraint_names=[['IHMV', 'Structure_mmCIF_RCB_File_MD5_key']])
    ]
    fkey_defs = [
        ForeignKey.define(["Processing_Status"], "Vocab", "Processing_Status", ["Name"],
                          constraint_names=[["Vocab", "Structure_mmCIF_Processing_Status_fkey"]],
                          on_update="CASCADE",
                          on_delete="NO ACTION"
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

def define_tdoc_IHMV_Generated_File():
    table_name='Generated_File'
    comment='System generated IHM validation report files'

    column_defs = [
        Column.define(
            'Structure_mmCIF',
            builtin_types.text,
            comment='RID of the uploaded structure mmCIF file',
            nullok=False
        ),
        Column.define(
            'File_Type',
            builtin_types.text,
            comment='Type of generated IHM validation report file',
            nullok=False
        ),
        Column.define(
            'File_URL',
            builtin_types.text,
            comment='Generated IHM validation report file location',
            nullok=False
        ),
        Column.define(
            'File_Name',
            builtin_types.text,
            comment='Generated IHM validation report file name',
            nullok=False
        ),
        Column.define(
            'File_Bytes',
            builtin_types.int8,
            comment='Generated IHM validation report file size in bytes',
            nullok=False
        ),
        Column.define(
            'File_MD5',
            builtin_types.text,
            comment='Generated IHM validation report file MD5',
            nullok=False
        ),
        Column.define(
            'Notes',
            builtin_types.markdown,
            comment='Additional notes about the generated IHM validation report file',
            nullok=True
        )
    ]
    key_defs = [
        Key.define(['RID'], constraint_names=[['IHMV', 'Generated_File_RID_key']]),
        Key.define(['Structure_mmCIF', 'File_Type'], constraint_names=[['IHMV', 'Generated_File_Structure_mmCIF_File_Type_key']]),
        Key.define(['Structure_mmCIF', 'File_MD5'], constraint_names=[['IHMV', 'Generated_File_Structure_mmCIF_File_MD5_key']])
    ]
    fkey_defs = [
        ForeignKey.define(["File_Type"], "Vocab", "File_Type", ["Name"],
                          constraint_names=[["Vocab", "Generated_File_File_Type_fkey"]],
                          on_update="CASCADE",
                          on_delete="NO ACTION"
        ),
        ForeignKey.define(['Structure_mmCIF'], 'IHMV', 'Structure_mmCIF', ['RID'],
                          constraint_names=[['IHMV', 'Generated_File_Structure_mmCIF_fkey']],
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

Processing_Status_rows = [
        {'Name': 'New', 'Description': 'New structure uploaded for IHM validation report generation'},
        {'Name': 'Reprocess', 'Description': 'Reprocess IHM validation report generation after error'},
        {'Name': 'In Progress', 'Description': 'IHM validation report generation in progress'},
        {'Name': 'Error', 'Description': 'IHM validation report generation error'},
        {'Name': 'Success', 'Description': 'IHM validation report generation success'}
    ]

File_Type_rows = [
        {'Name': 'Validation: Full PDF', 'Description': 'System generated full validation report in PDF format'},
        {'Name': 'Validation: Summary PDF', 'Description': 'System generated summary validation report in PDF format'},
        {'Name': 'Validation: HTML tar.gz', 'Description': 'System generated full validation report in HTML format, provided as a tar-gzipped file'}
    ]

def main(server_name, catalog_id, credentials):
    server = DerivaServer('https', server_name, credentials)
    catalog = server.connect_ermrest(catalog_id)
    catalog.dcctx['cid'] = "oneoff/model"
    model = catalog.getCatalogModel()


    model.schemas["IHMV"].tables["Generated_Files"].drop()
    model.schemas["IHMV"].tables["Structure_mmCIF"].drop()    

    if True:
        """
        Create new Vocab tables
        """
        utils.create_table_if_not_exist(model, 'Vocab', create_vocab_tdoc('Vocab', 'Processing_Status', 'IHM Validation Report Generation Processing Status'))
        utils.create_table_if_not_exist(model, 'Vocab', create_vocab_tdoc('Vocab', 'File_Type', 'IHM Validation Report Generated File Types'))
        #utils.create_table_if_not_exist(model, 'Vocab', utils.define_Vocab_table('Processing_Status', 'IHM Validation Report Generation Processing Status'))
        #utils.create_table_if_not_exist(model, 'Vocab', utils.define_Vocab_table('File_Type', 'IHM Validation Report Generated File Types'))

        """
        Load data into new and existing vocabulary tables
        """
        insert_if_not_exist(catalog, 'Vocab', 'Processing_Status', Processing_Status_rows)
        insert_if_not_exist(catalog, 'Vocab', 'File_Type', File_Type_rows)        
        #utils.add_rows_to_vocab_table(catalog, 'Processing_Status', Processing_Status_rows)
        #utils.add_rows_to_vocab_table(catalog, 'File_Type', File_Type_rows)

        """
        Create new table
        """
        utils.create_table_if_not_exist(model, 'IHMV',  define_tdoc_IHMV_Structure_mmCIF())
        utils.create_table_if_not_exist(model, 'IHMV',  define_tdoc_IHMV_Generated_File())

if __name__ == '__main__':
    args = BaseCLI("ad-hoc table creation tool", None, 1).parse_cli()
    credentials = get_credential(args.host, args.credential_file)

    main(args.host, 199, credentials)
    
