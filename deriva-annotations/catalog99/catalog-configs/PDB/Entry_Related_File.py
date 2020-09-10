import argparse
from deriva.core import ErmrestCatalog, AttrDict, get_credential
import deriva.core.ermrest_model as em
from deriva.core.ermrest_config import tag as chaise_tags
from deriva.utils.catalog.manage.update_catalog import CatalogUpdater, parse_args

groups = {
    'pdb-reader': 'https://auth.globus.org/8875a770-3c40-11e9-a8c8-0ee7d80087ee',
    'pdb-writer': 'https://auth.globus.org/c94a1e5c-3c40-11e9-a5d1-0aacc65bfe9a',
    'pdb-admin': 'https://auth.globus.org/0b98092c-3c41-11e9-a8c8-0ee7d80087ee',
    'pdb-curator': 'https://auth.globus.org/eef3e02a-3c40-11e9-9276-0edc9bdd56a6',
    'isrd-staff': 'https://auth.globus.org/176baec4-ed26-11e5-8e88-22000ab4b42b',
    'pdb-submitter': 'https://auth.globus.org/99da042e-64a6-11ea-ad5f-0ef992ed7ca1'
}

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

column_acls = {'File_URL': {'select': ['*']}}

column_acl_bindings = {'File_URL': {'no_binding': False}}

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
        acls=column_acls['File_URL'],
        acl_bindings=column_acl_bindings['File_URL'],
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
        default='PDB:1-MSVE',
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

display = {'name': 'Uploaded Restraint Files'}

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

table_annotations = {chaise_tags.display: display, chaise_tags.visible_columns: visible_columns, }

table_comment = 'Restraint data files (in csv/tsv format) related to the entry'

table_acls = {
    'owner': [groups['pdb-admin'], groups['isrd-staff']],
    'write': [],
    'delete': [groups['pdb-curator']],
    'insert': [groups['pdb-curator'], groups['pdb-writer'], groups['pdb-submitter']],
    'select': [groups['pdb-writer'], groups['pdb-reader']],
    'update': [groups['pdb-curator']],
    'enumerate': ['*']
}

table_acl_bindings = {
    'released_reader': {
        'types': ['select'],
        'scope_acl': [groups['pdb-submitter']],
        'projection': ['RCB'],
        'projection_type': 'acl'
    },
    'self_service_creator': {
        'types': ['update', 'delete'],
        'scope_acl': [groups['pdb-submitter']],
        'projection': [
            {
                'or': [
                    {
                        'filter': 'Workflow_Status',
                        'operand': 'DRAFT',
                        'operator': '='
                    }, {
                        'filter': 'Workflow_Status',
                        'operand': 'DEPO',
                        'operator': '='
                    }, {
                        'filter': 'Workflow_Status',
                        'operand': 'RECORD READY',
                        'operator': '='
                    }, {
                        'filter': 'Workflow_Status',
                        'operand': 'ERROR',
                        'operator': '='
                    }
                ]
            }, 'RCB'
        ],
        'projection_type': 'acl'
    }
}

key_defs = [em.Key.define(['RID'], constraint_names=[['PDB', 'Entry_Related_File_RIDkey1']], ), ]

fkey_defs = [
    em.ForeignKey.define(
        ['File_Format'],
        'Vocab',
        'File_Format', ['Name'],
        constraint_names=[['PDB', 'Entry_Related_File_File_Format_fkey']],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
    ),
    em.ForeignKey.define(
        ['File_Type'],
        'Vocab',
        'File_Type', ['Name'],
        constraint_names=[['PDB', 'Entry_Related_File_File_Type_fkey']],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
    ),
    em.ForeignKey.define(
        ['Workflow_Status'],
        'Vocab',
        'workflow_status', ['Name'],
        constraint_names=[['PDB', 'Entry_Related_File_workflow_status_fkey']],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
        on_update='CASCADE',
    ),
    em.ForeignKey.define(
        ['structure_id'],
        'PDB',
        'entry', ['id'],
        constraint_names=[['PDB', 'Entry_Related_File_entry_id_fkey']],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
        on_update='CASCADE',
        on_delete='CASCADE',
    ),
    em.ForeignKey.define(
        ['Owner'],
        'public',
        'Catalog_Group', ['ID'],
        constraint_names=[['PDB', 'Entry_Related_File_Owner_fkey']],
        acls={
            'insert': [groups['pdb-curator']],
            'update': [groups['pdb-curator']]
        },
        acl_bindings={
            'set_owner': {
                'types': ['update', 'insert'],
                'scope_acl': ['*'],
                'projection': ['ID'],
                'projection_type': 'acl'
            }
        },
    ),
    em.ForeignKey.define(
        ['Process_Status'],
        'Vocab',
        'process_status', ['Name'],
        constraint_names=[['PDB', 'Entry_Related_File_process_status_fkey']],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
        on_update='CASCADE',
        on_delete='SET NULL',
    ),
]

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
    catalog_id = 99
    mode, replace, host, catalog_id = parse_args(host, catalog_id, is_table=True)
    catalog = ErmrestCatalog('https', host, catalog_id=catalog_id, credentials=get_credential(host))
    main(catalog, mode, replace)
