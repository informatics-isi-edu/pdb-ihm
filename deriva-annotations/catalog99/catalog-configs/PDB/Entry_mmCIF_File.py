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

table_name = 'Entry_mmCIF_File'

schema_name = 'PDB'

column_annotations = {
    'File_URL': {
        chaise_tags.asset: {
            'md5': 'File_MD5',
            'url_pattern': '/hatrac/pdb/entry_mmCIF/{{$moment.year}}/{{{File_MD5}}}',
            'filename_column': 'File_Name',
            'byte_count_column': 'File_Bytes'
        },
        'tag:isrd.isi.edu,2018:required': {}
    },
    'File_MD5': {},
    'File_Bytes': {},
    'Owner': {},
    'Structure_Id': {},
    'mmCIF_Schema_Version': {
        chaise_tags.display: {
            'name': 'mmCIF Schema Version'
        }
    }
}

column_comment = {
    'File_URL': 'URL of the system generated mmCIF file',
    'File_MD5': 'MD5 value of the system generated mmCIF file',
    'File_Bytes': 'Size of the system generated mmCIF file in bytes',
    'Owner': 'Group that can update the record.',
    'Structure_Id': 'A reference to the entry.id identifier in the entry table',
    'mmCIF_Schema_Version': 'Schema version of mmCIF IHM extension dictionary'
}

column_acls = {'File_URL': {'select': ['*']}}

column_acl_bindings = {'File_URL': {'no_binding': False}}

column_defs = [
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
    em.Column.define('Owner', em.builtin_types['text'], comment=column_comment['Owner'],
                     ),
    em.Column.define(
        'Structure_Id',
        em.builtin_types['text'],
        nullok=False,
        comment=column_comment['Structure_Id'],
    ),
    em.Column.define(
        'mmCIF_Schema_Version',
        em.builtin_types['text'],
        annotations=column_annotations['mmCIF_Schema_Version'],
        comment=column_comment['mmCIF_Schema_Version'],
    ),
]

generated = None

display = {'name': 'System Generated mmCIF File'}

visible_columns = {
    '*': ['RID', 'File_URL', 'mmCIF_Schema_Version', ['PDB', 'Entry_mmCIF_File_Structure_Id_fkey']],
    'entry': ['File_URL', 'mmCIF_Schema_Version', ['PDB', 'Entry_mmCIF_File_Structure_Id_fkey']],
    'detailed': [
        'RID', 'File_URL', 'mmCIF_Schema_Version', ['PDB', 'Entry_mmCIF_File_Structure_Id_fkey'],
        'File_Bytes', 'File_MD5'
    ]
}

table_annotations = {
    chaise_tags.display: display,
    chaise_tags.generated: generated,
    chaise_tags.visible_columns: visible_columns,
}

table_comment = 'Details of the mmCIF file generated based on all the data provided by the user'

table_acls = {}

table_acl_bindings = {
    'released_reader': {
        'types': ['select'],
        'scope_acl': [groups['pdb-submitter']],
        'projection': [{
            'outbound': ['PDB', 'Entry_mmCIF_File_Structure_Id_fkey']
        }, 'RCB'],
        'projection_type': 'acl'
    }
}

key_defs = [
    em.Key.define(['RID'], constraint_names=[['PDB', 'Entry_mmCIF_File_RID_key']],
                  ),
    em.Key.define(
        ['Structure_Id', 'mmCIF_Schema_Version'],
        constraint_names=[['PDB', 'Entry_mmCIF_File_Structure_Id_mmCIF_Schema_Version_key']],
    ),
]

fkey_defs = [
    em.ForeignKey.define(
        ['Owner'],
        'public',
        'Catalog_Group', ['ID'],
        constraint_names=[['PDB', 'Entry_mmCIF_File_Owner_fkey']],
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
        ['Structure_Id'],
        'PDB',
        'entry', ['id'],
        constraint_names=[['PDB', 'Entry_mmCIF_File_Structure_Id_fkey']],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
        on_update='CASCADE',
        on_delete='CASCADE',
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
