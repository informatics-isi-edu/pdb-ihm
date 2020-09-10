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

table_name = 'ihm_modeling_protocol_details'

schema_name = 'PDB'

column_annotations = {
    'structure_id': {},
    'dataset_group_id': {},
    'description': {},
    'ensemble_flag': {},
    'id': {},
    'multi_scale_flag': {},
    'multi_state_flag': {},
    'num_models_begin': {},
    'num_models_end': {},
    'ordered_flag': {},
    'protocol_id': {},
    'script_file_id': {},
    'software_id': {},
    'step_id': {},
    'step_method': {},
    'step_name': {},
    'struct_assembly_description': {},
    'struct_assembly_id': {},
    'Owner': {}
}

column_comment = {
    'structure_id': 'A reference to table entry.id.',
    'dataset_group_id': 'A reference to table ihm_dataset_group.id.',
    'description': 'type:text\nTextual description of the protocol step.',
    'ensemble_flag': 'type:text\nA flag to indicate if the modeling involves an ensemble.',
    'id': 'type:int4\nA unique identifier for the modeling protocol/step combination.',
    'multi_scale_flag': 'type:text\nA flag to indicate if the modeling is multi scale.',
    'multi_state_flag': 'type:text\nA flag to indicate if the modeling is multi state.',
    'num_models_begin': 'type:int4\nThe number of models in the beginning of the step.',
    'num_models_end': 'type:int4\nThe number of models at the end of the step.',
    'ordered_flag': 'type:text\nA flag to indicate if the modeling involves an ensemble ordered by time or other order.',
    'protocol_id': 'A reference to table ihm_modeling_protocol.id.',
    'script_file_id': 'A reference to table ihm_external_files.id.',
    'software_id': 'A reference to table software.pdbx_ordinal.',
    'step_id': 'type:int4\nAn index for a particular step within the modeling protocol.',
    'step_method': 'type:text\nDescription of the method involved in the modeling step.\nexamples:Replica exchange monte carlo,Simulated annealing monte carlo,Monte carlo sampling',
    'step_name': 'type:text\nThe name or type of the modeling step.\nexamples:Sampling/Scoring,Refinement',
    'struct_assembly_description': 'type:text\nA textual description of the structural assembly being modeled.\nexamples:Nup84 sub-complex,PhoQ',
    'struct_assembly_id': 'A reference to table ihm_struct_assembly.id.',
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
        'dataset_group_id', em.builtin_types['int4'], comment=column_comment['dataset_group_id'],
    ),
    em.Column.define(
        'description', em.builtin_types['text'], comment=column_comment['description'],
    ),
    em.Column.define(
        'ensemble_flag', em.builtin_types['text'], comment=column_comment['ensemble_flag'],
    ),
    em.Column.define('id', em.builtin_types['int4'], nullok=False, comment=column_comment['id'],
                     ),
    em.Column.define(
        'multi_scale_flag', em.builtin_types['text'], comment=column_comment['multi_scale_flag'],
    ),
    em.Column.define(
        'multi_state_flag', em.builtin_types['text'], comment=column_comment['multi_state_flag'],
    ),
    em.Column.define(
        'num_models_begin', em.builtin_types['int4'], comment=column_comment['num_models_begin'],
    ),
    em.Column.define(
        'num_models_end', em.builtin_types['int4'], comment=column_comment['num_models_end'],
    ),
    em.Column.define(
        'ordered_flag', em.builtin_types['text'], comment=column_comment['ordered_flag'],
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
        'step_method', em.builtin_types['text'], comment=column_comment['step_method'],
    ),
    em.Column.define('step_name', em.builtin_types['text'], comment=column_comment['step_name'],
                     ),
    em.Column.define(
        'struct_assembly_description',
        em.builtin_types['text'],
        comment=column_comment['struct_assembly_description'],
    ),
    em.Column.define(
        'struct_assembly_id',
        em.builtin_types['int4'],
        comment=column_comment['struct_assembly_id'],
    ),
    em.Column.define('Owner', em.builtin_types['text'], comment=column_comment['Owner'],
                     ),
    em.Column.define('Software_RID', em.builtin_types['text'],
                     ),
    em.Column.define('Struct_assembly_RID', em.builtin_types['text'],
                     ),
    em.Column.define('Script_file_RID', em.builtin_types['text'],
                     ),
    em.Column.define('Dataset_group_RID', em.builtin_types['text'],
                     ),
]

display = {'name': 'Details of Modeling Protocols'}

visible_columns = {
    '*': [
        'RID', {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_modeling_protocol_details_structure_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table entry.id.',
            'markdown_name': 'structure id'
        }, 'id', {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_modeling_protocol_details_protocol_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table ihm_modeling_protocol.id.',
            'markdown_name': 'protocol id'
        }, 'step_id', {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_modeling_protocol_details_dataset_group_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table ihm_dataset_group.id.',
            'markdown_name': 'dataset group id'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_modeling_protocol_details_struct_assembly_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table ihm_struct_assembly.id.',
            'markdown_name': 'struct assembly id'
        }, 'struct_assembly_description', 'step_name', 'step_method', 'num_models_begin',
        'num_models_end', ['PDB', 'ihm_modeling_protocol_details_multi_scale_flag_fkey'],
        ['PDB', 'ihm_modeling_protocol_details_multi_state_flag_fkey'],
        ['PDB', 'ihm_modeling_protocol_details_ordered_flag_fkey'],
        ['PDB', 'ihm_modeling_protocol_details_ensemble_flag_fkey'], {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_modeling_protocol_details_script_file_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table ihm_external_files.id.',
            'markdown_name': 'script file id'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_modeling_protocol_details_software_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table software.pdbx_ordinal.',
            'markdown_name': 'software id'
        }, 'description'
    ],
    'entry': [
        {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_modeling_protocol_details_structure_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table entry.id.',
            'markdown_name': 'structure id'
        }, 'id', {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_modeling_protocol_details_protocol_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table ihm_modeling_protocol.id.',
            'markdown_name': 'protocol id'
        }, 'step_id', {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_modeling_protocol_details_dataset_group_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table ihm_dataset_group.id.',
            'markdown_name': 'dataset group id'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_modeling_protocol_details_struct_assembly_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table ihm_struct_assembly.id.',
            'markdown_name': 'struct assembly id'
        }, 'struct_assembly_description', 'step_name', 'step_method', 'num_models_begin',
        'num_models_end', ['PDB', 'ihm_modeling_protocol_details_multi_scale_flag_fkey'],
        ['PDB', 'ihm_modeling_protocol_details_multi_state_flag_fkey'],
        ['PDB', 'ihm_modeling_protocol_details_ordered_flag_fkey'],
        ['PDB', 'ihm_modeling_protocol_details_ensemble_flag_fkey'], {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_modeling_protocol_details_script_file_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table ihm_external_files.id.',
            'markdown_name': 'script file id'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_modeling_protocol_details_software_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table software.pdbx_ordinal.',
            'markdown_name': 'software id'
        }, 'description'
    ],
    'detailed': [
        'RID', {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_modeling_protocol_details_structure_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table entry.id.',
            'markdown_name': 'structure id'
        }, 'id', {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_modeling_protocol_details_protocol_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table ihm_modeling_protocol.id.',
            'markdown_name': 'protocol id'
        }, 'step_id', {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_modeling_protocol_details_dataset_group_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table ihm_dataset_group.id.',
            'markdown_name': 'dataset group id'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_modeling_protocol_details_struct_assembly_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table ihm_struct_assembly.id.',
            'markdown_name': 'struct assembly id'
        }, 'struct_assembly_description', 'step_name', 'step_method', 'num_models_begin',
        'num_models_end', ['PDB', 'ihm_modeling_protocol_details_multi_scale_flag_fkey'],
        ['PDB', 'ihm_modeling_protocol_details_multi_state_flag_fkey'],
        ['PDB', 'ihm_modeling_protocol_details_ordered_flag_fkey'],
        ['PDB', 'ihm_modeling_protocol_details_ensemble_flag_fkey'], {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_modeling_protocol_details_script_file_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table ihm_external_files.id.',
            'markdown_name': 'script file id'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_modeling_protocol_details_software_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table software.pdbx_ordinal.',
            'markdown_name': 'software id'
        }, 'description', ['PDB', 'ihm_modeling_protocol_details_RCB_fkey'],
        ['PDB', 'ihm_modeling_protocol_details_RMB_fkey'], 'RCT', 'RMT',
        ['PDB', 'ihm_modeling_protocol_details_Owner_fkey']
    ]
}

table_annotations = {chaise_tags.display: display, chaise_tags.visible_columns: visible_columns, }

table_comment = 'Details of the modeling protocols used in the integrative modeling study'

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
        'projection': [
            {
                'outbound': ['PDB', 'ihm_modeling_protocol_details_structure_id_fkey']
            }, 'RCB'
        ],
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
                'outbound': ['PDB', 'ihm_modeling_protocol_details_structure_id_fkey']
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
        ['structure_id', 'id'],
        constraint_names=[['PDB', 'ihm_modeling_protocol_details_primary_key']],
    ),
    em.Key.define(['RID'], constraint_names=[['PDB', 'ihm_modeling_protocol_details_RIDkey1']],
                  ),
]

fkey_defs = [
    em.ForeignKey.define(
        ['RMB'],
        'public',
        'ERMrest_Client', ['ID'],
        constraint_names=[['PDB', 'ihm_modeling_protocol_details_RMB_fkey']],
    ),
    em.ForeignKey.define(
        ['RCB'],
        'public',
        'ERMrest_Client', ['ID'],
        constraint_names=[['PDB', 'ihm_modeling_protocol_details_RCB_fkey']],
    ),
    em.ForeignKey.define(
        ['multi_state_flag'],
        'Vocab',
        'ihm_modeling_protocol_details_multi_state_flag', ['Name'],
        constraint_names=[['PDB', 'ihm_modeling_protocol_details_multi_state_flag_fkey']],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
    ),
    em.ForeignKey.define(
        ['ensemble_flag'],
        'Vocab',
        'ihm_modeling_protocol_details_ensemble_flag', ['Name'],
        constraint_names=[['PDB', 'ihm_modeling_protocol_details_ensemble_flag_fkey']],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
    ),
    em.ForeignKey.define(
        ['multi_scale_flag'],
        'Vocab',
        'ihm_modeling_protocol_details_multi_scale_flag', ['Name'],
        constraint_names=[['PDB', 'ihm_modeling_protocol_details_multi_scale_flag_fkey']],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
    ),
    em.ForeignKey.define(
        ['ordered_flag'],
        'Vocab',
        'ihm_modeling_protocol_details_ordered_flag', ['Name'],
        constraint_names=[['PDB', 'ihm_modeling_protocol_details_ordered_flag_fkey']],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
    ),
    em.ForeignKey.define(
        ['protocol_id', 'structure_id'],
        'PDB',
        'ihm_modeling_protocol', ['id', 'structure_id'],
        constraint_names=[['PDB', 'ihm_modeling_protocol_details_protocol_id_fkey']],
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
        ['Owner'],
        'public',
        'Catalog_Group', ['ID'],
        constraint_names=[['PDB', 'ihm_modeling_protocol_details_Owner_fkey']],
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
        constraint_names=[['PDB', 'ihm_modeling_protocol_details_structure_id_fkey']],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
        on_update='CASCADE',
        on_delete='CASCADE',
    ),
    em.ForeignKey.define(
        ['software_id', 'structure_id'],
        'PDB',
        'software', ['pdbx_ordinal', 'structure_id'],
        constraint_names=[['PDB', 'ihm_modeling_protocol_details_software_id_fk']],
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
        ['Software_RID', 'software_id'],
        'PDB',
        'software', ['RID', 'pdbx_ordinal'],
        constraint_names=[['PDB', 'ihm_modeling_protocol_details_software_id_fkey']],
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
        ['struct_assembly_id', 'structure_id'],
        'PDB',
        'ihm_struct_assembly', ['id', 'structure_id'],
        constraint_names=[['PDB', 'ihm_modeling_protocol_details_struct_assembly_id_fk']],
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
        ['Struct_assembly_RID', 'struct_assembly_id'],
        'PDB',
        'ihm_struct_assembly', ['RID', 'id'],
        constraint_names=[['PDB', 'ihm_modeling_protocol_details_struct_assembly_id_fkey']],
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
        ['script_file_id', 'structure_id'],
        'PDB',
        'ihm_external_files', ['id', 'structure_id'],
        constraint_names=[['PDB', 'ihm_modeling_protocol_details_script_file_id_fk']],
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
        ['script_file_id', 'Script_file_RID'],
        'PDB',
        'ihm_external_files', ['id', 'RID'],
        constraint_names=[['PDB', 'ihm_modeling_protocol_details_script_file_id_fkey']],
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
        ['structure_id', 'dataset_group_id'],
        'PDB',
        'ihm_dataset_group', ['structure_id', 'id'],
        constraint_names=[['PDB', 'ihm_modeling_protocol_details_dataset_group_id_fk']],
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
        ['Dataset_group_RID', 'dataset_group_id'],
        'PDB',
        'ihm_dataset_group', ['RID', 'id'],
        constraint_names=[['PDB', 'ihm_modeling_protocol_details_dataset_group_id_fkey']],
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
