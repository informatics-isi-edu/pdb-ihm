import argparse
from deriva.core import ErmrestCatalog, AttrDict, get_credential
import deriva.core.ermrest_model as em
from deriva.core.ermrest_config import tag as chaise_tags
from deriva.utils.catalog.manage.update_catalog import CatalogUpdater, parse_args

groups = {}

table_name = 'Entry_Related_File'

schema_name = 'PDB'

column_annotations = {
    'File_Type': {},
    'File_Format': {},
    'File_URL': {
        chaise_tags.asset: {
            'md5': 'File_MD5',
            'url_pattern': '/hatrac/pdb/entry_files/{{$moment.year}}/{{{File_MD5}}}',
            'filename_column': 'File_Name',
            'byte_count_column': 'File_Bytes'
        },
        'tag:isrd.isi.edu,2018:required': {}
    },
    'File_MD5': {},
    'File_Bytes': {},
    'Workflow_Status': {},
    'Record_Status_Detail': {},
    'Owner': {},
    'structure_id': {},
    'Description': {}
}

column_comment = {
    'File_Type': 'Restraint table corresponding to the uploaded file',
    'File_Format': 'CSV or TSV file format',
    'File_URL': 'URL of the uploaded file',
    'File_MD5': 'MD5 value of the uploaded file',
    'File_Bytes': 'Size of the uploaded file in bytes',
    'Workflow_Status': 'Workflow status corresponding to uploading restraint data files',
    'Record_Status_Detail': 'Captures error messages obtained while processing the uploaded restraint data files; remains empty if process is success',
    'Owner': 'Group that can update the record.',
    'structure_id': 'A reference to the entry.id identifier in the entry table',
    'Description': 'Description of the file'
}

column_acls = {}

column_acl_bindings = {}

column_defs = [
    em.Column.define(
        'File_Type', em.builtin_types['text'], nullok=False, comment=column_comment['File_Type'],
    ),
    em.Column.define(
        'File_Format',
        em.builtin_types['text'],
        nullok=False,
        comment=column_comment['File_Format'],
    ),
    em.Column.define(
        'File_URL',
        em.builtin_types['text'],
        annotations=column_annotations['File_URL'],
        comment=column_comment['File_URL'],
    ),
    em.Column.define('File_Name', em.builtin_types['text'],
                     ),
    em.Column.define('File_MD5', em.builtin_types['text'], comment=column_comment['File_MD5'],
                     ),
    em.Column.define(
        'File_Bytes', em.builtin_types['int8'], comment=column_comment['File_Bytes'],
    ),
    em.Column.define(
        'Workflow_Status',
        em.builtin_types['text'],
        nullok=False,
        default='DRAFT',
        comment=column_comment['Workflow_Status'],
    ),
    em.Column.define('Process_Status', em.builtin_types['text'], default='New',
                     ),
    em.Column.define(
        'Record_Status_Detail',
        em.builtin_types['text'],
        comment=column_comment['Record_Status_Detail'],
    ),
    em.Column.define('Owner', em.builtin_types['text'], comment=column_comment['Owner'],
                     ),
    em.Column.define(
        'structure_id',
        em.builtin_types['text'],
        nullok=False,
        comment=column_comment['structure_id'],
    ),
    em.Column.define(
        'Description', em.builtin_types['text'], comment=column_comment['Description'],
    ),
]

visible_columns = {
    '*': [
        'RID', ['PDB',
                'Entry_Related_File_entry_id_fkey'], ['PDB', 'Entry_Related_File_File_Type_fkey'],
        ['PDB', 'Entry_Related_File_File_Format_fkey'], 'File_URL', 'File_Bytes', 'File_MD5',
        'Description', ['PDB', 'Entry_Related_File_workflow_status_fkey'], 'Record_Status_Detail'
    ],
    'entry': [
        ['PDB', 'Entry_Related_File_entry_id_fkey'], ['PDB', 'Entry_Related_File_File_Type_fkey'],
        ['PDB', 'Entry_Related_File_File_Format_fkey'], 'File_Name', 'File_URL', 'File_Bytes',
        'File_MD5', 'Description', ['PDB', 'Entry_Related_File_workflow_status_fkey']
    ],
    'detailed': [
        'RID', ['PDB',
                'Entry_Related_File_entry_id_fkey'], ['PDB', 'Entry_Related_File_File_Type_fkey'],
        ['PDB', 'Entry_Related_File_File_Format_fkey'], 'File_URL', 'File_Bytes', 'File_MD5',
        'Description', ['PDB', 'Entry_Related_File_workflow_status_fkey'], 'Record_Status_Detail',
        ['PDB', 'Entry_Related_File_RCB_fkey'], ['PDB',
                                                 'Entry_Related_File_RMB_fkey'], 'RCT', 'RMT',
        ['PDB', 'Entry_Related_File_Owner_fkey']
    ]
}

table_annotations = {chaise_tags.visible_columns: visible_columns, }

table_comment = 'Restraint data files (in csv/tsv format) related to the entry'

table_acls = {}

table_acl_bindings = {}

key_defs = []

fkey_defs = []

table_def = em.Table.define(
    table_name,
    column_defs=column_defs,
    key_defs=key_defs,
    fkey_defs=fkey_defs,
    annotations=table_annotations,
    acls=table_acls,
    acl_bindings=table_acl_bindings,
    comment=table_comment,
    provide_system=True
)


def main(catalog, mode, replace=False, really=False):
    updater = CatalogUpdater(catalog)
    table_def['column_annotations'] = column_annotations
    table_def['column_comment'] = column_comment
    updater.update_table(mode, schema_name, table_def, replace=replace, really=really)


if __name__ == "__main__":
    host = 'pdb.isrd.isi.edu'
    catalog_id = 50
    mode, replace, host, catalog_id = parse_args(host, catalog_id, is_table=True)
    catalog = ErmrestCatalog('https', host, catalog_id=catalog_id, credentials=get_credential(host))
    main(catalog, mode, replace)
