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

table_name = 'Page_Asset'

schema_name = 'WWW'

column_annotations = {
    'URL': {
        chaise_tags.asset: {
            'md5': 'MD5',
            'url_pattern': '/hatrac/WWW/Page_Asset/{{{MD5}}}.{{#encode}}{{{Filename}}}{{/encode}}',
            'filename_column': 'Filename',
            'byte_count_column': 'Length'
        }
    },
    'Filename': {},
    'Description': {},
    'Length': {},
    'MD5': {},
    'Page': {}
}

column_comment = {
    'URL': 'URL to the asset',
    'Filename': 'Filename of the asset that was uploaded',
    'Description': 'Description of the asset',
    'Length': 'Asset length (bytes)',
    'MD5': 'Asset content MD5 checksum',
    'Page': 'The Page entry to which this asset is attached'
}

column_acls = {}

column_acl_bindings = {}

column_defs = [
    em.Column.define(
        'URL',
        em.builtin_types['text'],
        nullok=False,
        annotations=column_annotations['URL'],
        comment=column_comment['URL'],
    ),
    em.Column.define('Filename', em.builtin_types['text'], comment=column_comment['Filename'],
                     ),
    em.Column.define(
        'Description', em.builtin_types['markdown'], comment=column_comment['Description'],
    ),
    em.Column.define(
        'Length', em.builtin_types['int8'], nullok=False, comment=column_comment['Length'],
    ),
    em.Column.define(
        'MD5', em.builtin_types['text'], nullok=False, comment=column_comment['MD5'],
    ),
    em.Column.define(
        'Page', em.builtin_types['text'], nullok=False, comment=column_comment['Page'],
    ),
]

table_display = {'row_name': {'row_markdown_pattern': '{{{Filename}}}'}}

table_annotations = {chaise_tags.table_display: table_display, }

table_comment = 'Asset table for Page'

table_acls = {}

table_acl_bindings = {}

key_defs = [
    em.Key.define(['URL'], constraint_names=[['WWW', 'Page_Asset_URLkey1']],
                  ),
    em.Key.define(['RID'], constraint_names=[['WWW', 'Page_Asset_RIDkey1']],
                  ),
]

fkey_defs = [
    em.ForeignKey.define(
        ['Page'],
        'WWW',
        'Page', ['RID'],
        constraint_names=[['WWW', 'Page_Asset_Page_fkey']],
        acls={
            'insert': [groups['pdb-curator']],
            'update': [groups['pdb-curator']]
        },
        acl_bindings={
            'self_linkage_owner': {
                'types': ['insert', 'update'],
                'projection': ['Owner'],
                'projection_type': 'acl',
                'scope_acl': ['*']
            },
            'self_linkage_creator': {
                'types': ['insert', 'update'],
                'projection': ['RCB'],
                'projection_type': 'acl',
                'scope_acl': ['*']
            }
        },
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
