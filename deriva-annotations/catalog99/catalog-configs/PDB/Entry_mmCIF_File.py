import argparse
from deriva.core import ErmrestCatalog, AttrDict, get_credential
import deriva.core.ermrest_model as em
from deriva.core.ermrest_config import tag as chaise_tags
from deriva.utils.catalog.manage.update_catalog import CatalogUpdater, parse_args

groups = {}

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
    'Owner': {},
    'mmCIF_Schema_Version': {
        chaise_tags.display: {
            'name': 'mmCIF Schema Version'
        }
    }
}

column_comment = {'Owner': 'Group that can update the record.'}

column_acls = {}

column_acl_bindings = {}

column_defs = [
    em.Column.define(
        'File_URL', em.builtin_types['text'], annotations=column_annotations['File_URL'],
    ),
    em.Column.define('File_Name', em.builtin_types['text'],
                     ),
    em.Column.define('File_MD5', em.builtin_types['text'],
                     ),
    em.Column.define('File_Bytes', em.builtin_types['int8'],
                     ),
    em.Column.define('Owner', em.builtin_types['text'], comment=column_comment['Owner'],
                     ),
    em.Column.define('Structure_Id', em.builtin_types['text'], nullok=False,
                     ),
    em.Column.define(
        'mmCIF_Schema_Version',
        em.builtin_types['text'],
        annotations=column_annotations['mmCIF_Schema_Version'],
    ),
]

generated = None

display = {'name': 'Entry mmCIF File'}

visible_columns = {
    '*': [
        'RID', 'File_URL', 'mmCIF_Schema_Version', ['PDB', 'Entry_mmCIF_File_Structure_Id_fkey']
    ],
    'entry': [
        'File_URL', 'mmCIF_Schema_Version', ['PDB', 'Entry_mmCIF_File_Structure_Id_fkey']
    ],
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

table_comment = None

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
    catalog_id = 99
    mode, replace, host, catalog_id = parse_args(host, catalog_id, is_table=True)
    catalog = ErmrestCatalog('https', host, catalog_id=catalog_id, credentials=get_credential(host))
    main(catalog, mode, replace)
