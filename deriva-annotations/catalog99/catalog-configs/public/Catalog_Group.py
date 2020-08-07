import argparse
from deriva.core import ErmrestCatalog, AttrDict, get_credential
import deriva.core.ermrest_model as em
from deriva.core.ermrest_config import tag as chaise_tags
from deriva.utils.catalog.manage.update_catalog import CatalogUpdater, parse_args

groups = {}

table_name = 'Catalog_Group'

schema_name = 'public'

column_annotations = {'Display_Name': {chaise_tags.display: {'name': 'Display Name'}}}

column_comment = {}

column_acls = {}

column_acl_bindings = {}

column_defs = [
    em.Column.define(
        'Display_Name', em.builtin_types['text'], annotations=column_annotations['Display_Name'],
    ),
    em.Column.define('URL', em.builtin_types['text'],
                     ),
    em.Column.define('Description', em.builtin_types['text'],
                     ),
    em.Column.define('ID', em.builtin_types['text'], nullok=False,
                     ),
]

table_annotations = {}

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
