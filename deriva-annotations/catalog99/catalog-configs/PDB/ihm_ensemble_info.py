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
    'isrd-staff': 'https://auth.globus.org/176baec4-ed26-11e5-8e88-22000ab4b42b',
    'pdb-submitter': 'https://auth.globus.org/99da042e-64a6-11ea-ad5f-0ef992ed7ca1'
}

table_name = 'ihm_ensemble_info'

schema_name = 'PDB'

column_annotations = {
    'structure_id': {},
    'details': {},
    'ensemble_clustering_feature': {},
    'ensemble_clustering_method': {},
    'ensemble_file_id': {},
    'ensemble_id': {},
    'ensemble_name': {},
    'ensemble_precision_value': {},
    'model_group_id': {},
    'num_ensemble_models': {},
    'num_ensemble_models_deposited': {},
    'post_process_id': {},
    'Owner': {}
}

column_comment = {
    'structure_id': 'A reference to table entry.id.',
    'details': 'type:text\nAdditional details regarding the ensemble.',
    'ensemble_clustering_feature': 'type:text\nThe parameter/feature used for clustering the models, if applicable.',
    'ensemble_clustering_method': 'type:text\nThe clustering method used to obtain the ensemble, if applicable.',
    'ensemble_file_id': 'A reference to table ihm_external_files.id.',
    'ensemble_id': 'type:int4\nA unique id for the ensemble.',
    'ensemble_name': 'type:text\nAn optional name for the cluster or ensemble for better description.\nexamples:ensemble1,ensemble2,cluster1,cluster2,open state,closed state',
    'ensemble_precision_value': 'type:float4\nThe precision of each cluster or ensemble is calculated as dRMSD, which\n is the average C-alpha distance root mean square deviation (dRMSD) \n between the individual models in the cluster and the cluster centroid.\n The cluster centroid is defined as the model with the minimal sum of\n dRMSDs to the other models in the cluster or ensemble.',
    'model_group_id': 'A reference to table ihm_model_group.id.',
    'num_ensemble_models': 'type:int4\nThe number of models in the current ensemble being described.',
    'num_ensemble_models_deposited': 'type:int4\nThe number of models from the current ensemble that is deposited.',
    'post_process_id': 'A reference to table ihm_modeling_post_process.id.',
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
        'ensemble_clustering_feature',
        em.builtin_types['text'],
        comment=column_comment['ensemble_clustering_feature'],
    ),
    em.Column.define(
        'ensemble_clustering_method',
        em.builtin_types['text'],
        comment=column_comment['ensemble_clustering_method'],
    ),
    em.Column.define(
        'ensemble_file_id', em.builtin_types['int4'], comment=column_comment['ensemble_file_id'],
    ),
    em.Column.define(
        'ensemble_id',
        em.builtin_types['int4'],
        nullok=False,
        comment=column_comment['ensemble_id'],
    ),
    em.Column.define(
        'ensemble_name', em.builtin_types['text'], comment=column_comment['ensemble_name'],
    ),
    em.Column.define(
        'ensemble_precision_value',
        em.builtin_types['float4'],
        comment=column_comment['ensemble_precision_value'],
    ),
    em.Column.define(
        'model_group_id', em.builtin_types['int4'], comment=column_comment['model_group_id'],
    ),
    em.Column.define(
        'num_ensemble_models',
        em.builtin_types['int4'],
        nullok=False,
        comment=column_comment['num_ensemble_models'],
    ),
    em.Column.define(
        'num_ensemble_models_deposited',
        em.builtin_types['int4'],
        comment=column_comment['num_ensemble_models_deposited'],
    ),
    em.Column.define(
        'post_process_id', em.builtin_types['int4'], comment=column_comment['post_process_id'],
    ),
    em.Column.define('Owner', em.builtin_types['text'], comment=column_comment['Owner'],
                     ),
    em.Column.define('Post_process_RID', em.builtin_types['text'],
                     ),
    em.Column.define('Ensemble_file_RID', em.builtin_types['text'],
                     ),
    em.Column.define('Model_group_RID', em.builtin_types['text'],
                     ),
]

display = {'name': 'Details of Ensembles'}

visible_columns = {
    '*': [
        'RID', {
            'source': [{
                'outbound': ['PDB', 'ihm_ensemble_info_structure_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table entry.id.',
            'markdown_name': 'structure id'
        }, 'ensemble_id', 'ensemble_name', {
            'source': [{
                'outbound': ['PDB', 'ihm_ensemble_info_model_group_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table ihm_model_group.id.',
            'markdown_name': 'model group id'
        }, {
            'source': [{
                'outbound': ['PDB', 'ihm_ensemble_info_post_process_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table ihm_modeling_post_process.id.',
            'markdown_name': 'post process id'
        }, ['PDB', 'ihm_ensemble_info_ensemble_clustering_method_fkey'],
        ['PDB', 'ihm_ensemble_info_ensemble_clustering_feature_fkey'], 'num_ensemble_models',
        'num_ensemble_models_deposited', 'ensemble_precision_value', {
            'source': [{
                'outbound': ['PDB', 'ihm_ensemble_info_ensemble_file_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table ihm_external_files.id.',
            'markdown_name': 'ensemble file id'
        }, 'details'
    ],
    'entry': [
        {
            'source': [{
                'outbound': ['PDB', 'ihm_ensemble_info_structure_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table entry.id.',
            'markdown_name': 'structure id'
        }, 'ensemble_id', 'ensemble_name', {
            'source': [{
                'outbound': ['PDB', 'ihm_ensemble_info_model_group_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table ihm_model_group.id.',
            'markdown_name': 'model group id'
        }, {
            'source': [{
                'outbound': ['PDB', 'ihm_ensemble_info_post_process_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table ihm_modeling_post_process.id.',
            'markdown_name': 'post process id'
        }, ['PDB', 'ihm_ensemble_info_ensemble_clustering_method_fkey'],
        ['PDB', 'ihm_ensemble_info_ensemble_clustering_feature_fkey'], 'num_ensemble_models',
        'num_ensemble_models_deposited', 'ensemble_precision_value', {
            'source': [{
                'outbound': ['PDB', 'ihm_ensemble_info_ensemble_file_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table ihm_external_files.id.',
            'markdown_name': 'ensemble file id'
        }, 'details'
    ],
    'detailed': [
        'RID', {
            'source': [{
                'outbound': ['PDB', 'ihm_ensemble_info_structure_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table entry.id.',
            'markdown_name': 'structure id'
        }, 'ensemble_id', 'ensemble_name', {
            'source': [{
                'outbound': ['PDB', 'ihm_ensemble_info_model_group_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table ihm_model_group.id.',
            'markdown_name': 'model group id'
        }, {
            'source': [{
                'outbound': ['PDB', 'ihm_ensemble_info_post_process_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table ihm_modeling_post_process.id.',
            'markdown_name': 'post process id'
        }, ['PDB', 'ihm_ensemble_info_ensemble_clustering_method_fkey'],
        ['PDB', 'ihm_ensemble_info_ensemble_clustering_feature_fkey'], 'num_ensemble_models',
        'num_ensemble_models_deposited', 'ensemble_precision_value', {
            'source': [{
                'outbound': ['PDB', 'ihm_ensemble_info_ensemble_file_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table ihm_external_files.id.',
            'markdown_name': 'ensemble file id'
        }, 'details', ['PDB', 'ihm_ensemble_info_RCB_fkey'], ['PDB', 'ihm_ensemble_info_RMB_fkey'],
        'RCT', 'RMT', ['PDB', 'ihm_ensemble_info_Owner_fkey']
    ]
}

visible_foreign_keys = {
    'filter': 'detailed',
    'detailed': [
        ['PDB', 'ihm_cross_link_result_ensemble_id_fkey'],
        ['PDB', 'ihm_localization_density_files_ensemble_id_fkey']
    ]
}

table_display = {'row_name': {'row_markdown_pattern': '{{{ensemble_id}}}'}}

table_annotations = {
    chaise_tags.display: display,
    chaise_tags.table_display: table_display,
    chaise_tags.visible_columns: visible_columns,
    chaise_tags.visible_foreign_keys: visible_foreign_keys,
}

table_comment = 'Details of model ensembles'

table_acls = {
    'owner': [groups['pdb-admin'], groups['isrd-staff']],
    'write': [],
    'delete': [groups['pdb-curator']],
    'insert': [groups['pdb-curator'], groups['pdb-writer'], groups['pdb-submitter']],
    'select': [groups['pdb-writer'], groups['pdb-reader']],
    'update': [groups['pdb-curator']],
    'enumerate': ['*']
}

table_acl_bindings = {
    'released_reader': {
        'types': ['select'],
        'scope_acl': [groups['pdb-submitter']],
        'projection': [{
            'outbound': ['PDB', 'ihm_ensemble_info_structure_id_fkey']
        }, 'RCB'],
        'projection_type': 'acl'
    },
    'self_service_group': {
        'types': ['update', 'delete'],
        'scope_acl': ['*'],
        'projection': ['Owner'],
        'projection_type': 'acl'
    },
    'self_service_creator': {
        'types': ['update', 'delete'],
        'scope_acl': [groups['pdb-submitter']],
        'projection': [
            {
                'outbound': ['PDB', 'ihm_ensemble_info_structure_id_fkey']
            }, {
                'or': [
                    {
                        'filter': 'Workflow_Status',
                        'operand': 'DRAFT',
                        'operator': '='
                    }, {
                        'filter': 'Workflow_Status',
                        'operand': 'DEPO',
                        'operator': '='
                    }, {
                        'filter': 'Workflow_Status',
                        'operand': 'RECORD READY',
                        'operator': '='
                    }, {
                        'filter': 'Workflow_Status',
                        'operand': 'ERROR',
                        'operator': '='
                    }
                ]
            }, 'RCB'
        ],
        'projection_type': 'acl'
    }
}

key_defs = [
    em.Key.define(
        ['ensemble_id', 'structure_id'],
        constraint_names=[['PDB', 'ihm_ensemble_info_primary_key']],
    ),
    em.Key.define(['RID'], constraint_names=[['PDB', 'ihm_ensemble_info_RIDkey1']],
                  ),
]

fkey_defs = [
    em.ForeignKey.define(
        ['RMB'],
        'public',
        'ERMrest_Client', ['ID'],
        constraint_names=[['PDB', 'ihm_ensemble_info_RMB_fkey']],
    ),
    em.ForeignKey.define(
        ['RCB'],
        'public',
        'ERMrest_Client', ['ID'],
        constraint_names=[['PDB', 'ihm_ensemble_info_RCB_fkey']],
    ),
    em.ForeignKey.define(
        ['ensemble_clustering_feature'],
        'Vocab',
        'ihm_ensemble_info_ensemble_clustering_feature', ['Name'],
        constraint_names=[['PDB', 'ihm_ensemble_info_ensemble_clustering_feature_fkey']],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
    ),
    em.ForeignKey.define(
        ['ensemble_clustering_method'],
        'Vocab',
        'ihm_ensemble_info_ensemble_clustering_method', ['Name'],
        constraint_names=[['PDB', 'ihm_ensemble_info_ensemble_clustering_method_fkey']],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
    ),
    em.ForeignKey.define(
        ['Owner'],
        'public',
        'Catalog_Group', ['ID'],
        constraint_names=[['PDB', 'ihm_ensemble_info_Owner_fkey']],
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
        ['structure_id'],
        'PDB',
        'entry', ['id'],
        constraint_names=[['PDB', 'ihm_ensemble_info_structure_id_fkey']],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
        on_update='CASCADE',
        on_delete='CASCADE',
    ),
    em.ForeignKey.define(
        ['post_process_id', 'structure_id'],
        'PDB',
        'ihm_modeling_post_process', ['id', 'structure_id'],
        constraint_names=[['PDB', 'ihm_ensemble_info_post_process_id_fk']],
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
        ['Post_process_RID', 'post_process_id'],
        'PDB',
        'ihm_modeling_post_process', ['RID', 'id'],
        constraint_names=[['PDB', 'ihm_ensemble_info_post_process_id_fkey']],
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
        ['structure_id', 'ensemble_file_id'],
        'PDB',
        'ihm_external_files', ['structure_id', 'id'],
        constraint_names=[['PDB', 'ihm_ensemble_info_ensemble_file_id_fk']],
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
        ['ensemble_file_id', 'Ensemble_file_RID'],
        'PDB',
        'ihm_external_files', ['id', 'RID'],
        constraint_names=[['PDB', 'ihm_ensemble_info_ensemble_file_id_fkey']],
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
        ['structure_id', 'model_group_id'],
        'PDB',
        'ihm_model_group', ['structure_id', 'id'],
        constraint_names=[['PDB', 'ihm_ensemble_info_model_group_id_fk']],
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
        ['Model_group_RID', 'model_group_id'],
        'PDB',
        'ihm_model_group', ['RID', 'id'],
        constraint_names=[['PDB', 'ihm_ensemble_info_model_group_id_fkey']],
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
    catalog_id = 99
    mode, replace, host, catalog_id = parse_args(host, catalog_id, is_table=True)
    catalog = ErmrestCatalog('https', host, catalog_id=catalog_id, credentials=get_credential(host))
    main(catalog, mode, replace)
