import argparse
from deriva.core import ErmrestCatalog, AttrDict, get_credential, DerivaPathError
from deriva.utils.catalog.components.deriva_model import DerivaCatalog
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

table_name = 'ihm_cross_link_result'

schema_name = 'PDB'

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
    'structure_id': {},
    'details': {},
    'distance_threshold': {},
    'ensemble_id': {},
    'id': {},
    'median_distance': {},
    'num_models': {},
    'restraint_id': {},
    'Owner': {}
}

column_comment = {
    'structure_id': 'A reference to table entry.id.',
    'details': 'type:text\nThis records holds any associated details of the results of the particular \n crosslink restraint in the integrative modeling task.',
    'distance_threshold': 'type:float4\nThe distance threshold applied to this crosslink in the integrative modeling task.',
    'ensemble_id': 'A reference to table ihm_ensemble_info.ensemble_id.',
    'id': 'type:int4\nA unique identifier for the restraint/ensemble combination.',
    'median_distance': 'type:float4\nThe median distance between the crosslinked residues in the sampled models.',
    'num_models': 'type:int4\nNumber of models sampled in the integrative modeling task, for which\n the crosslinking distance is provided.',
    'restraint_id': 'A reference to table ihm_cross_link_restraint.id.',
    'Owner': 'Group that can update the record.'
}

column_acls = {}

column_acl_bindings = {}

column_defs = [
    em.Column.define(
        'structure_id',
        em.builtin_types['text'],
        nullok=False,
        comment=column_comment['structure_id'],
    ),
    em.Column.define('details', em.builtin_types['text'], comment=column_comment['details'],
                     ),
    em.Column.define(
        'distance_threshold',
        em.builtin_types['float4'],
        nullok=False,
        comment=column_comment['distance_threshold'],
    ),
    em.Column.define(
        'ensemble_id',
        em.builtin_types['int4'],
        nullok=False,
        comment=column_comment['ensemble_id'],
    ),
    em.Column.define('id', em.builtin_types['int4'], nullok=False, comment=column_comment['id'],
                     ),
    em.Column.define(
        'median_distance',
        em.builtin_types['float4'],
        nullok=False,
        comment=column_comment['median_distance'],
    ),
    em.Column.define(
        'num_models',
        em.builtin_types['int4'],
        nullok=False,
        comment=column_comment['num_models'],
    ),
    em.Column.define(
        'restraint_id',
        em.builtin_types['int4'],
        nullok=False,
        comment=column_comment['restraint_id'],
    ),
    em.Column.define('Owner', em.builtin_types['text'], comment=column_comment['Owner'],
                     ),
]

visible_columns = {
    '*': [
        'RID', {
            'source': [{
                'outbound': ['PDB', 'ihm_cross_link_result_structure_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table entry.id.',
            'markdown_name': 'structure id'
        }, 'details', 'distance_threshold', {
            'source': [{
                'outbound': ['PDB', 'ihm_cross_link_result_ensemble_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table ihm_ensemble_info.ensemble_id.',
            'markdown_name': 'ensemble id'
        }, 'id', 'median_distance', 'num_models', {
            'source': [{
                'outbound': ['PDB', 'ihm_cross_link_result_restraint_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table ihm_cross_link_restraint.id.',
            'markdown_name': 'restraint id'
        }, ['PDB', 'ihm_cross_link_result_RCB_fkey'], ['PDB', 'ihm_cross_link_result_RMB_fkey'],
        'RCT', 'RMT', ['PDB', 'ihm_cross_link_result_Owner_fkey']
    ],
    'entry': [
        {
            'source': [{
                'outbound': ['PDB', 'ihm_cross_link_result_structure_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table entry.id.',
            'markdown_name': 'structure id'
        }, 'details', 'distance_threshold', {
            'source': [{
                'outbound': ['PDB', 'ihm_cross_link_result_ensemble_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table ihm_ensemble_info.ensemble_id.',
            'markdown_name': 'ensemble id'
        }, 'id', 'median_distance', 'num_models', {
            'source': [{
                'outbound': ['PDB', 'ihm_cross_link_result_restraint_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table ihm_cross_link_restraint.id.',
            'markdown_name': 'restraint id'
        }
    ]
}

table_annotations = {chaise_tags.visible_columns: visible_columns, }

table_comment = None

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
    em.Key.define(['RID'], constraint_names=[('PDB', 'ihm_cross_link_result_RIDkey1')],
                  ),
    em.Key.define(
        ['structure_id', 'id'], constraint_names=[('PDB', 'ihm_cross_link_result_primary_key')],
    ),
]

fkey_defs = [
    em.ForeignKey.define(
        ['Owner'],
        'public',
        'Catalog_Group', ['ID'],
        constraint_names=[('PDB', 'ihm_cross_link_result_Owner_fkey')],
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
        constraint_names=[('PDB', 'ihm_cross_link_result_RCB_fkey')],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
    ),
    em.ForeignKey.define(
        ['RMB'],
        'public',
        'ERMrest_Client', ['ID'],
        constraint_names=[('PDB', 'ihm_cross_link_result_RMB_fkey')],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
    ),
    em.ForeignKey.define(
        ['structure_id'],
        'PDB',
        'entry', ['id'],
        constraint_names=[('PDB', 'ihm_cross_link_result_structure_id_fkey')],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
        on_update='CASCADE',
        on_delete='SET NULL',
    ),
    em.ForeignKey.define(
        ['structure_id', 'ensemble_id'],
        'PDB',
        'ihm_ensemble_info', ['structure_id', 'ensemble_id'],
        constraint_names=[('PDB', 'ihm_cross_link_result_ensemble_id_fkey')],
        annotations={
            chaise_tags.foreign_key: {
                'domain_filter_pattern': 'structure_id={{structure_id}}'
            }
        },
        acls={
            'insert': ['*'],
            'update': ['*']
        },
        on_update='CASCADE',
        on_delete='SET NULL',
    ),
    em.ForeignKey.define(
        ['structure_id', 'restraint_id'],
        'PDB',
        'ihm_cross_link_restraint', ['structure_id', 'id'],
        constraint_names=[('PDB', 'ihm_cross_link_result_restraint_id_fkey')],
        annotations={
            chaise_tags.foreign_key: {
                'domain_filter_pattern': 'structure_id={{structure_id}}'
            }
        },
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
    catalog_id = 1
    mode, replace, host, catalog_id = parse_args(host, catalog_id, is_table=True)
    catalog = DerivaCatalog(host, catalog_id=catalog_id, validate=False)
    main(catalog, mode, replace)
