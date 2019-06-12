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

table_name = 'ihm_ensemble_info_ensemble_clustering_feature_term'

schema_name = 'Vocab'

column_annotations = {
    'RCT': {
        chaise_tags.display: {
            'name': 'Creation Time'
        },
        chaise_tags.generated: None,
        chaise_tags.immutable: None
    },
    'RMT': {
        chaise_tags.display: {
            'name': 'Last Modified Time'
        },
        chaise_tags.generated: None,
        chaise_tags.immutable: None
    },
    'RCB': {
        chaise_tags.display: {
            'name': 'Created By'
        },
        chaise_tags.generated: None,
        chaise_tags.immutable: None
    },
    'RMB': {
        chaise_tags.display: {
            'name': 'Modified By'
        },
        chaise_tags.generated: None,
        chaise_tags.immutable: None
    },
    'ID': {},
    'URI': {},
    'Name': {},
    'Description': {},
    'Synonyms': {},
    'Owner': {}
}

column_comment = {
    'ID': 'The preferred Compact URI (CURIE) for this term.',
    'URI': 'The preferred URI for this term.',
    'Name': 'The preferred human-readable name for this term.',
    'Description': 'A longer human-readable description of this term.',
    'Synonyms': 'Alternate human-readable names for this term.',
    'Owner': 'Group that can update the record.'
}

column_acls = {}

column_acl_bindings = {}

column_defs = [
    em.Column.define(
        'ID',
        em.builtin_types['ermrest_curie'],
        nullok=False,
        default='PDB:{RID}',
        comment=column_comment['ID'],
    ),
    em.Column.define(
        'URI',
        em.builtin_types['ermrest_uri'],
        nullok=False,
        default='/id/{RID}',
        comment=column_comment['URI'],
    ),
    em.Column.define(
        'Name', em.builtin_types['text'], nullok=False, comment=column_comment['Name'],
    ),
    em.Column.define(
        'Description',
        em.builtin_types['markdown'],
        nullok=False,
        comment=column_comment['Description'],
    ),
    em.Column.define('Synonyms', em.builtin_types['text[]'], comment=column_comment['Synonyms'],
                     ),
    em.Column.define('Owner', em.builtin_types['text'], comment=column_comment['Owner'],
                     ),
]

visible_columns = {
    '*': [
        'RID', 'Name', 'Description', 'ID', 'URI',
        ['Vocab', 'ihm_ensemble_info_ensemble_clustering_feature_term_RCB_fkey'],
        ['Vocab', 'ihm_ensemble_info_ensemble_clustering_feature_term_RMB_fkey'], 'RCT', 'RMT',
        ['Vocab', 'ihm_ensemble_info_ensemble_clustering_feature_term_Owner_fkey']
    ]
}

table_display = {'row_name': {'row_markdown_pattern': '{{{Name}}}'}}

table_annotations = {
    chaise_tags.table_display: table_display,
    chaise_tags.visible_columns: visible_columns,
}

table_comment = 'A set of controlled vocabular terms.'

table_acls = {}

table_acl_bindings = {
    'self_service_group': {
        'types': ['update', 'delete'],
        'scope_acl': ['*'],
        'projection': ['Owner'],
        'projection_type': 'acl'
    },
    'self_service_creator': {
        'types': ['update', 'delete'],
        'scope_acl': ['*'],
        'projection': ['RCB'],
        'projection_type': 'acl'
    }
}

key_defs = [
    em.Key.define(
        ['RID'],
        constraint_names=[('Vocab', 'ihm_ensemble_info_ensemble_clustering_feature_term_RIDkey1')],
    ),
    em.Key.define(
        ['ID'],
        constraint_names=[('Vocab', 'ihm_ensemble_info_ensemble_clustering_feature_term_IDkey1')],
    ),
    em.Key.define(
        ['URI'],
        constraint_names=[('Vocab', 'ihm_ensemble_info_ensemble_clustering_feature_term_URIkey1')],
    ),
]

fkey_defs = [
    em.ForeignKey.define(
        ['Owner'],
        'public',
        'Catalog_Group', ['ID'],
        constraint_names=[
            ('Vocab', 'ihm_ensemble_info_ensemble_clustering_feature_term_Owner_fkey')
        ],
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
        ['RCB'],
        'public',
        'ERMrest_Client', ['ID'],
        constraint_names=[('Vocab', 'ihm_ensemble_info_ensemble_clustering_feature_term_RCB_fkey')],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
    ),
    em.ForeignKey.define(
        ['RMB'],
        'public',
        'ERMrest_Client', ['ID'],
        constraint_names=[('Vocab', 'ihm_ensemble_info_ensemble_clustering_feature_term_RMB_fkey')],
        acls={
            'insert': ['*'],
            'update': ['*']
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
    updater.update_table(mode, schema_name, table_def, replace=replace, really=really)


if __name__ == "__main__":
    host = 'pdb.isrd.isi.edu'
    catalog_id = 5
    mode, replace, host, catalog_id = parse_args(host, catalog_id, is_table=True)
    catalog = DerivaCatalog(host, catalog_id=catalog_id, validate=False)
    main(catalog, mode, replace)

