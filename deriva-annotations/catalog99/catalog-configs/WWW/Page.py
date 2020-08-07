import argparse
from deriva.core import ErmrestCatalog, AttrDict, get_credential
import deriva.core.ermrest_model as em
from deriva.core.ermrest_config import tag as chaise_tags
from deriva.utils.catalog.manage.update_catalog import CatalogUpdater, parse_args

groups = {}

table_name = 'Page'

schema_name = 'WWW'

column_annotations = {'Title': {}, 'Content': {}, 'Owner': {}}

column_comment = {
    'Title': 'Unique title for the page',
    'Content': 'Content of the page in markdown',
    'Owner': 'Group that can update the record.'
}

column_acls = {}

column_acl_bindings = {}

column_defs = [
    em.Column.define(
        'Title', em.builtin_types['text'], nullok=False, comment=column_comment['Title'],
    ),
    em.Column.define('Content', em.builtin_types['markdown'], comment=column_comment['Content'],
                     ),
    em.Column.define('Owner', em.builtin_types['text'], comment=column_comment['Owner'],
                     ),
]

visible_columns = {
    '*': [
        {
            'source': 'RID'
        }, {
            'source': 'RCT'
        }, {
            'source': 'RMT'
        }, {
            'source': [{
                'outbound': ['WWW', 'Page_RCB_fkey']
            }, 'RID']
        }, {
            'source': [{
                'outbound': ['WWW', 'Page_RMB_fkey']
            }, 'RID']
        }, {
            'source': [{
                'outbound': ['WWW', 'Page_Owner_fkey']
            }, 'RID']
        }, {
            'source': 'Title'
        }, {
            'source': 'Content'
        }
    ],
    'entry': [
        {
            'source': 'RID'
        }, {
            'source': 'RCT'
        }, {
            'source': 'RMT'
        }, {
            'source': [{
                'outbound': ['WWW', 'Page_RCB_fkey']
            }, 'RID']
        }, {
            'source': [{
                'outbound': ['WWW', 'Page_RMB_fkey']
            }, 'RID']
        }, {
            'source': [{
                'outbound': ['WWW', 'Page_Owner_fkey']
            }, 'RID']
        }, {
            'source': 'Title'
        }, {
            'source': 'Content'
        }
    ]
}

visible_foreign_keys = {'detailed': {}}

table_display = {'detailed': {'collapse_toc_panel': True, 'hide_column_headers': True}}

table_annotations = {
    chaise_tags.table_display: table_display,
    chaise_tags.visible_columns: visible_columns,
    chaise_tags.visible_foreign_keys: visible_foreign_keys,
}

table_comment = None

table_acls = {}

table_acl_bindings = {}

key_defs = [
    em.Key.define(['Title'], constraint_names=[['WWW', 'Page_Title_key']],
                  ),
    em.Key.define(['RID'], constraint_names=[['WWW', 'Page_RIDkey1']],
                  ),
]

fkey_defs = [
    em.ForeignKey.define(
        ['RMB'], 'public', 'ERMrest_Client', ['ID'], constraint_names=[['WWW', 'Page_RMB_fkey']],
    ),
    em.ForeignKey.define(
        ['RCB'], 'public', 'ERMrest_Client', ['ID'], constraint_names=[['WWW', 'Page_RCB_fkey']],
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
