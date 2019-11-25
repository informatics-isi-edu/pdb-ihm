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

table_name = 'ihm_ordered_ensemble'

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
    'edge_description': {},
    'edge_id': {},
    'model_group_id_begin': {},
    'model_group_id_end': {},
    'ordered_by': {},
    'process_description': {},
    'process_id': {},
    'step_description': {},
    'step_id': {},
    'Owner': {}
}

column_comment = {
    'structure_id': 'A reference to table entry.id.',
    'edge_description': 'type:text\nDescription of the edge.',
    'edge_id': 'type:int4\nAn identifier that describes an edge in a directed graph, which\n represents an ordered ensemble. \n Forms the category key together with _ihm_ordered_ensemble.process_id.',
    'model_group_id_begin': 'A reference to table ihm_model_group.id.',
    'model_group_id_end': 'A reference to table ihm_model_group.id.',
    'ordered_by': 'type:text\nThe parameter based on which the ordering is carried out.\nexamples:time steps,steps in an assembly process,steps in a metabolic pathway,steps in an interaction pathway',
    'process_description': 'type:text\nDescription of the ordered process.',
    'process_id': 'type:int4\nAn identifier for the ordered process. \n Forms the category key together with _ihm_ordered_ensemble.edge_id.',
    'step_description': 'type:text\nDescription of the step.',
    'step_id': 'type:int4\nIdentifier for a particular step in the ordered process.',
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
    em.Column.define(
        'edge_description', em.builtin_types['text'], comment=column_comment['edge_description'],
    ),
    em.Column.define(
        'edge_id', em.builtin_types['int4'], nullok=False, comment=column_comment['edge_id'],
    ),
    em.Column.define(
        'model_group_id_begin',
        em.builtin_types['int4'],
        nullok=False,
        comment=column_comment['model_group_id_begin'],
    ),
    em.Column.define(
        'model_group_id_end',
        em.builtin_types['int4'],
        nullok=False,
        comment=column_comment['model_group_id_end'],
    ),
    em.Column.define(
        'ordered_by', em.builtin_types['text'], comment=column_comment['ordered_by'],
    ),
    em.Column.define(
        'process_description',
        em.builtin_types['text'],
        comment=column_comment['process_description'],
    ),
    em.Column.define(
        'process_id',
        em.builtin_types['int4'],
        nullok=False,
        comment=column_comment['process_id'],
    ),
    em.Column.define(
        'step_description', em.builtin_types['text'], comment=column_comment['step_description'],
    ),
    em.Column.define(
        'step_id', em.builtin_types['int4'], nullok=False, comment=column_comment['step_id'],
    ),
    em.Column.define('Owner', em.builtin_types['text'], comment=column_comment['Owner'],
                     ),
]

visible_columns = {
    '*': [
        'RID', {
            'source': [{
                'outbound': ['PDB', 'ihm_ordered_ensemble_structure_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table entry.id.',
            'markdown_name': 'structure id'
        }, 'edge_description', 'edge_id', {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_ordered_ensemble_model_group_id_begin_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table ihm_model_group.id.',
            'markdown_name': 'model group id begin'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_ordered_ensemble_model_group_id_end_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table ihm_model_group.id.',
            'markdown_name': 'model group id end'
        }, 'ordered_by', 'process_description', 'process_id', 'step_description', 'step_id',
        ['PDB', 'ihm_ordered_ensemble_RCB_fkey'], ['PDB', 'ihm_ordered_ensemble_RMB_fkey'], 'RCT',
        'RMT', ['PDB', 'ihm_ordered_ensemble_Owner_fkey']
    ],
    'entry': [
        {
            'source': [{
                'outbound': ['PDB', 'ihm_ordered_ensemble_structure_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table entry.id.',
            'markdown_name': 'structure id'
        }, 'edge_description', 'edge_id', {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_ordered_ensemble_model_group_id_begin_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table ihm_model_group.id.',
            'markdown_name': 'model group id begin'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_ordered_ensemble_model_group_id_end_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table ihm_model_group.id.',
            'markdown_name': 'model group id end'
        }, 'ordered_by', 'process_description', 'process_id', 'step_description', 'step_id'
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
    em.Key.define(['RID'], constraint_names=[('PDB', 'ihm_ordered_ensemble_RIDkey1')],
                  ),
    em.Key.define(
        ['structure_id', 'edge_id', 'process_id'],
        constraint_names=[('PDB', 'ihm_ordered_ensemble_primary_key')],
    ),
]

fkey_defs = [
    em.ForeignKey.define(
        ['structure_id'],
        'PDB',
        'entry', ['id'],
        constraint_names=[('PDB', 'ihm_ordered_ensemble_structure_id_fkey')],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
        on_update='CASCADE',
        on_delete='SET NULL',
    ),
    em.ForeignKey.define(
        ['Owner'],
        'public',
        'Catalog_Group', ['ID'],
        constraint_names=[('PDB', 'ihm_ordered_ensemble_Owner_fkey')],
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
        constraint_names=[('PDB', 'ihm_ordered_ensemble_RCB_fkey')],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
    ),
    em.ForeignKey.define(
        ['RMB'],
        'public',
        'ERMrest_Client', ['ID'],
        constraint_names=[('PDB', 'ihm_ordered_ensemble_RMB_fkey')],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
    ),
    em.ForeignKey.define(
        ['structure_id', 'model_group_id_begin'],
        'PDB',
        'ihm_model_group', ['structure_id', 'id'],
        constraint_names=[('PDB', 'ihm_ordered_ensemble_model_group_id_begin_fkey')],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
        on_update='CASCADE',
        on_delete='SET NULL',
    ),
    em.ForeignKey.define(
        ['structure_id', 'model_group_id_end'],
        'PDB',
        'ihm_model_group', ['structure_id', 'id'],
        constraint_names=[('PDB', 'ihm_ordered_ensemble_model_group_id_end_fkey')],
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
