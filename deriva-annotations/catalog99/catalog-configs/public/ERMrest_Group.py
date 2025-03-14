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
    'isrd-staff': 'https://auth.globus.org/176baec4-ed26-11e5-8e88-22000ab4b42b'
}

table_name = 'ERMrest_Group'

schema_name = 'public'

column_annotations = {'Display_Name': {chaise_tags.display: {'name': 'Display Name'}}}

column_comment = {}

column_acls = {}

column_acl_bindings = {}

column_defs = [
    em.Column.define('ID', em.builtin_types['text'], nullok=False,
                     ),
    em.Column.define('URL', em.builtin_types['text'],
                     ),
    em.Column.define(
        'Display_Name', em.builtin_types['text'], annotations=column_annotations['Display_Name'],
    ),
    em.Column.define('Description', em.builtin_types['text'],
                     ),
]

generated = None

visible_columns = {
    '*': [
        {
            'source': 'Display_Name'
        }, {
            'source': 'ID'
        }, {
            'source': 'URL'
        }, {
            'source': 'Description'
        }
    ]
}

table_annotations = {
    chaise_tags.generated: generated,
    chaise_tags.visible_columns: visible_columns,
}

table_comment = None

table_acls = {
    'delete': [],
    'insert': [],
    'select': [groups['pdb-writer'], groups['pdb-curator'], groups['pdb-admin']],
    'update': [],
    'enumerate': []
}

table_acl_bindings = {}

key_defs = [
    em.Key.define(
        ['URL', 'ID', 'Display_Name', 'Description'],
        constraint_names=[['public', 'ERMrest_Group_ID_URL_Display_Name_Description_key']],
        comment='Group ID is unique.',
    ),
    em.Key.define(['ID'], constraint_names=[['public', 'ERMrest_Group_ID_key']],
                  ),
    em.Key.define(['RID'], constraint_names=[['public', 'ERMrest_Group_pkey']],
                  ),
]

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
