import argparse
from attrdict import AttrDict
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
from deriva.utils.catalog.components.deriva_model import DerivaCatalog
import deriva.core.ermrest_model as em
from deriva.core.ermrest_config import tag as chaise_tags
from deriva.utils.catalog.manage.update_catalog import CatalogUpdater, parse_args

groups = {
    'pdb-admin': 'https://auth.globus.org/0b98092c-3c41-11e9-a8c8-0ee7d80087ee',
    'pdb-reader': 'https://auth.globus.org/8875a770-3c40-11e9-a8c8-0ee7d80087ee',
    'pdb-writer': 'https://auth.globus.org/c94a1e5c-3c40-11e9-a5d1-0aacc65bfe9a',
    'pdb-curator': 'https://auth.globus.org/eef3e02a-3c40-11e9-9276-0edc9bdd56a6',
    'isrd-staff': 'https://auth.globus.org/176baec4-ed26-11e5-8e88-22000ab4b42b'
}

table_name = 'ERMrest_Group'

schema_name = 'public'

column_annotations = {}

column_comment = {}

column_acls = {}

column_acl_bindings = {}

column_defs = [
    em.Column.define('ID', em.builtin_types['text'], nullok=False,
                     ),
    em.Column.define('URL', em.builtin_types['text'],
                     ),
    em.Column.define('Display_Name', em.builtin_types['text'],
                     ),
    em.Column.define('Description', em.builtin_types['text'],
                     ),
]

display = {'name': 'Globus Group'}

visible_columns = {'*': ['Display_Name', 'Description', 'URL', 'ID']}

table_display = {'row_name': {'row_markdown_pattern': '{{{Display_Name}}}'}}

table_annotations = {
    chaise_tags.display: display,
    chaise_tags.table_display: table_display,
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
    em.Key.define(['RID'], constraint_names=[('public', 'ERMrest_Group_pkey')],
                  ),
    em.Key.define(['ID'], constraint_names=[('public', 'ERMrest_Group_ID_key')],
                  ),
    em.Key.define(
        ['ID', 'URL', 'Display_Name', 'Description'],
        constraint_names=[('public', 'ERMrest_Group_ID_URL_Display_Name_Description_key')],
        comment='Group ID is unique.',
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
    updater.update_table(mode, schema_name, table_def, replace=replace, really=really)


if __name__ == "__main__":
    host = 'pdb.isrd.isi.edu'
    catalog_id = 5
    mode, replace, host, catalog_id = parse_args(host, catalog_id, is_table=True)
    catalog = DerivaCatalog(host, catalog_id=catalog_id, validate=False)
    main(catalog, mode, replace)

