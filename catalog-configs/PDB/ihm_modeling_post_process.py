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

table_name = 'ihm_modeling_post_process'

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
    'analysis_id': {},
    'dataset_group_id': {},
    'feature': {},
    'feature_name': {},
    'id': {
        chaise_tags.generated: None
    },
    'num_models_begin': {},
    'num_models_end': {},
    'protocol_id': {},
    'script_file_id': {},
    'software_id': {},
    'step_id': {},
    'struct_assembly_id': {},
    'type': {},
    'Owner': {}
}

column_comment = {
    'structure_id': 'type:text\nThe value of _entry.id identifies the data block.\n\n Note that this item need not be a number; it can be any unique\n identifier.',
    'analysis_id': 'type:int4\nAn identifier for the post modeling analysis. This data item accounts for\n multiple post-modeling analyses that can be carried out.',
    'dataset_group_id': 'type:int4\nA unique identifier for the dataset group.',
    'feature': 'type:text\nThe parameter/feature used in the post modeling analysis.',
    'feature_name': 'type:text\nThe name of the parameter/feature used in the post modeling analysis.\nexamples:Rosetta energy,GOAP (orientation-dependent all-atom statistical potential)',
    'id': 'type:int4\nA unique identifier for the post modeling analysis/step combination.',
    'num_models_begin': 'type:int4\nThe number of models at the beginning of the post processing step.',
    'num_models_end': 'type:int4\nThe number of models the the end of the post processing step.',
    'protocol_id': 'type:int4\nA unique identifier for the modeling protocol.',
    'script_file_id': 'type:int4\nA unique identifier for each external file.',
    'software_id': 'type:int4\n\nAn ordinal index for this category',
    'step_id': 'type:int4\nIn a multi-step process, this identifier denotes the particular\n step in the post modeling analysis.',
    'struct_assembly_id': 'type:int4\nA unique identifier for the structural assembly.',
    'type': 'type:text\nThe type of post modeling analysis being carried out.',
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
        'analysis_id',
        em.builtin_types['int4'],
        nullok=False,
        comment=column_comment['analysis_id'],
    ),
    em.Column.define(
        'dataset_group_id', em.builtin_types['int4'], comment=column_comment['dataset_group_id'],
    ),
    em.Column.define(
        'feature', em.builtin_types['text'], nullok=False, comment=column_comment['feature'],
    ),
    em.Column.define(
        'feature_name', em.builtin_types['text'], comment=column_comment['feature_name'],
    ),
    em.Column.define(
        'id',
        em.builtin_types['int4'],
        nullok=False,
        annotations=column_annotations['id'],
        comment=column_comment['id'],
    ),
    em.Column.define(
        'num_models_begin', em.builtin_types['int4'], comment=column_comment['num_models_begin'],
    ),
    em.Column.define(
        'num_models_end', em.builtin_types['int4'], comment=column_comment['num_models_end'],
    ),
    em.Column.define(
        'protocol_id',
        em.builtin_types['int4'],
        nullok=False,
        comment=column_comment['protocol_id'],
    ),
    em.Column.define(
        'script_file_id', em.builtin_types['int4'], comment=column_comment['script_file_id'],
    ),
    em.Column.define(
        'software_id', em.builtin_types['int4'], comment=column_comment['software_id'],
    ),
    em.Column.define(
        'step_id', em.builtin_types['int4'], nullok=False, comment=column_comment['step_id'],
    ),
    em.Column.define(
        'struct_assembly_id',
        em.builtin_types['int4'],
        comment=column_comment['struct_assembly_id'],
    ),
    em.Column.define(
        'type', em.builtin_types['text'], nullok=False, comment=column_comment['type'],
    ),
    em.Column.define('Owner', em.builtin_types['text'], comment=column_comment['Owner'],
                     ),
]

visible_columns = {
    '*': [
        'RID',
        {
            'source': [{
                'outbound': ['PDB', 'ihm_modeling_post_process_structure_id_fkey']
            }, 'RID'],
            'comment': 'type:text\nThe value of _entry.id identifies the data block.\n\n Note that this item need not be a number; it can be any unique\n identifier.',
            'markdown_name': 'structure id'
        }, 'analysis_id',
        {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_modeling_post_process_dataset_group_id_fkey']
                }, 'RID'
            ],
            'comment': 'type:int4\nA unique identifier for the dataset group.',
            'markdown_name': 'dataset group id'
        }, ['PDB', 'ihm_modeling_post_process_feature_term_fkey'], 'feature_name', 'id',
        'num_models_begin', 'num_models_end',
        {
            'source': [{
                'outbound': ['PDB', 'ihm_modeling_post_process_protocol_id_fkey']
            }, 'RID'],
            'comment': 'type:int4\nA unique identifier for the modeling protocol.',
            'markdown_name': 'protocol id'
        },
        {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_modeling_post_process_script_file_id_fkey']
                }, 'RID'
            ],
            'comment': 'type:int4\nA unique identifier for each external file.',
            'markdown_name': 'script file id'
        },
        {
            'source': [{
                'outbound': ['PDB', 'ihm_modeling_post_process_software_id_fkey']
            }, 'RID'],
            'comment': 'type:int4\n\nAn ordinal index for this category',
            'markdown_name': 'software id'
        }, 'step_id',
        {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_modeling_post_process_struct_assembly_id_fkey']
                }, 'RID'
            ],
            'comment': 'type:int4\nA unique identifier for the structural assembly.',
            'markdown_name': 'struct assembly id'
        }, ['PDB', 'ihm_modeling_post_process_type_term_fkey'],
        ['PDB', 'ihm_modeling_post_process_RCB_fkey'],
        ['PDB', 'ihm_modeling_post_process_RMB_fkey'], 'RCT', 'RMT',
        ['PDB', 'ihm_modeling_post_process_Owner_fkey']
    ],
    'entry': [
        {
            'source': [{
                'outbound': ['PDB', 'ihm_modeling_post_process_structure_id_fkey']
            }, 'RID'],
            'comment': 'type:text\nThe value of _entry.id identifies the data block.\n\n Note that this item need not be a number; it can be any unique\n identifier.',
            'markdown_name': 'structure id'
        }, 'analysis_id',
        {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_modeling_post_process_dataset_group_id_fkey']
                }, 'RID'
            ],
            'comment': 'type:int4\nA unique identifier for the dataset group.',
            'markdown_name': 'dataset group id'
        }, ['PDB', 'ihm_modeling_post_process_feature_term_fkey'], 'feature_name', 'id',
        'num_models_begin', 'num_models_end',
        {
            'source': [{
                'outbound': ['PDB', 'ihm_modeling_post_process_protocol_id_fkey']
            }, 'RID'],
            'comment': 'type:int4\nA unique identifier for the modeling protocol.',
            'markdown_name': 'protocol id'
        },
        {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_modeling_post_process_script_file_id_fkey']
                }, 'RID'
            ],
            'comment': 'type:int4\nA unique identifier for each external file.',
            'markdown_name': 'script file id'
        },
        {
            'source': [{
                'outbound': ['PDB', 'ihm_modeling_post_process_software_id_fkey']
            }, 'RID'],
            'comment': 'type:int4\n\nAn ordinal index for this category',
            'markdown_name': 'software id'
        }, 'step_id',
        {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_modeling_post_process_struct_assembly_id_fkey']
                }, 'RID'
            ],
            'comment': 'type:int4\nA unique identifier for the structural assembly.',
            'markdown_name': 'struct assembly id'
        }, ['PDB', 'ihm_modeling_post_process_type_term_fkey']
    ]
}

visible_foreign_keys = {
    'filter': 'detailed',
    'detailed': [['PDB', 'ihm_ensemble_info_post_process_id_fkey']]
}

table_display = {'row_name': {'row_markdown_pattern': '{{{id}}}'}}

table_annotations = {
    chaise_tags.table_display: table_display,
    chaise_tags.visible_columns: visible_columns,
    chaise_tags.visible_foreign_keys: visible_foreign_keys,
}

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
    em.Key.define(['RID'], constraint_names=[('PDB', 'ihm_modeling_post_process_RIDkey1')],
                  ),
    em.Key.define(
        ['structure_id', 'id'],
        constraint_names=[('PDB', 'ihm_modeling_post_process_primary_key')],
    ),
]

fkey_defs = [
    em.ForeignKey.define(
        ['feature'],
        'Vocab',
        'ihm_modeling_post_process_feature_term', ['ID'],
        constraint_names=[('PDB', 'ihm_modeling_post_process_feature_term_fkey')],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
        on_update='CASCADE',
        on_delete='SET NULL',
    ),
    em.ForeignKey.define(
        ['type'],
        'Vocab',
        'ihm_modeling_post_process_type_term', ['ID'],
        constraint_names=[('PDB', 'ihm_modeling_post_process_type_term_fkey')],
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
        constraint_names=[('PDB', 'ihm_modeling_post_process_Owner_fkey')],
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
        constraint_names=[('PDB', 'ihm_modeling_post_process_RCB_fkey')],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
    ),
    em.ForeignKey.define(
        ['RMB'],
        'public',
        'ERMrest_Client', ['ID'],
        constraint_names=[('PDB', 'ihm_modeling_post_process_RMB_fkey')],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
    ),
    em.ForeignKey.define(
        ['structure_id'],
        'PDB',
        'entry', ['id'],
        constraint_names=[('PDB', 'ihm_modeling_post_process_structure_id_fkey')],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
        on_update='CASCADE',
        on_delete='SET NULL',
    ),
    em.ForeignKey.define(
        ['structure_id', 'dataset_group_id'],
        'PDB',
        'ihm_dataset_group', ['structure_id', 'id'],
        constraint_names=[('PDB', 'ihm_modeling_post_process_dataset_group_id_fkey')],
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
        ['structure_id', 'protocol_id'],
        'PDB',
        'ihm_modeling_protocol', ['structure_id', 'id'],
        constraint_names=[('PDB', 'ihm_modeling_post_process_protocol_id_fkey')],
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
        ['structure_id', 'script_file_id'],
        'PDB',
        'ihm_external_files', ['structure_id', 'id'],
        constraint_names=[('PDB', 'ihm_modeling_post_process_script_file_id_fkey')],
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
        ['structure_id', 'software_id'],
        'PDB',
        'software', ['structure_id', 'pdbx_ordinal'],
        constraint_names=[('PDB', 'ihm_modeling_post_process_software_id_fkey')],
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
        ['structure_id', 'struct_assembly_id'],
        'PDB',
        'ihm_struct_assembly', ['structure_id', 'id'],
        constraint_names=[('PDB', 'ihm_modeling_post_process_struct_assembly_id_fkey')],
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
    updater.update_table(mode, schema_name, table_def, replace=replace, really=really)


if __name__ == "__main__":
    host = 'pdb.isrd.isi.edu'
    catalog_id = 5
    mode, replace, host, catalog_id = parse_args(host, catalog_id, is_table=True)
    catalog = DerivaCatalog(host, catalog_id=catalog_id, validate=False)
    main(catalog, mode, replace)

