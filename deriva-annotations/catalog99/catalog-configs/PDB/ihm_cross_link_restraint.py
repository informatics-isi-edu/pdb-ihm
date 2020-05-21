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

table_name = 'ihm_cross_link_restraint'

schema_name = 'PDB'

column_annotations = {
    'structure_id': {},
    'asym_id_1': {},
    'asym_id_2': {},
    'atom_id_1': {},
    'atom_id_2': {},
    'comp_id_1': {},
    'comp_id_2': {},
    'conditional_crosslink_flag': {},
    'distance_threshold': {},
    'entity_id_1': {},
    'entity_id_2': {},
    'group_id': {},
    'id': {},
    'model_granularity': {},
    'psi': {},
    'restraint_type': {},
    'seq_id_1': {},
    'seq_id_2': {},
    'sigma_1': {},
    'sigma_2': {},
    'Owner': {}
}

column_comment = {
    'structure_id': 'A reference to table entry.id.',
    'asym_id_1': 'A reference to table struct_asym.id.',
    'asym_id_2': 'A reference to table struct_asym.id.',
    'atom_id_1': 'type:text\nThe atom identifier for the first monomer partner in the cross link.\n This data item is a pointer to _chem_comp_atom.atom_id in the \n CHEM_COMP_ATOM category.',
    'atom_id_2': 'type:text\nThe atom identifier for the second monomer partner in the cross link.\n This data item is a pointer to _chem_comp_atom.atom_id in the \n CHEM_COMP_ATOM category.',
    'comp_id_1': 'A reference to table chem_comp.id.',
    'comp_id_2': 'A reference to table chem_comp.id.',
    'conditional_crosslink_flag': 'type:text\nThe cross link conditionality.',
    'distance_threshold': 'type:float4\nThe distance threshold applied to this crosslink in the integrative modeling task.',
    'entity_id_1': 'A reference to table entity.id.',
    'entity_id_2': 'A reference to table entity.id.',
    'group_id': 'A reference to table ihm_cross_link_list.id.',
    'id': 'type:int4\nA unique identifier for the cross link record.',
    'model_granularity': 'type:text\nThe coarse-graining information for the crosslink implementation.',
    'psi': 'type:float4\nThe uncertainty in the crosslinking experimental data;\n may be approximated to the false positive rate.',
    'restraint_type': 'type:text\nThe type of the cross link restraint applied.',
    'seq_id_1': 'A reference to table entity_poly_seq.num.',
    'seq_id_2': 'A reference to table entity_poly_seq.num.',
    'sigma_1': 'type:float4\nThe uncertainty in the position of residue 1 in the crosslink\n arising due to the multi-scale nature of the model represention.',
    'sigma_2': 'type:float4\nThe uncertainty in the position of residue 2 in the crosslink\n arising due to the multi-scale nature of the model represention.',
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
        'asym_id_1', em.builtin_types['text'], nullok=False, comment=column_comment['asym_id_1'],
    ),
    em.Column.define(
        'asym_id_2', em.builtin_types['text'], nullok=False, comment=column_comment['asym_id_2'],
    ),
    em.Column.define('atom_id_1', em.builtin_types['text'], comment=column_comment['atom_id_1'],
                     ),
    em.Column.define('atom_id_2', em.builtin_types['text'], comment=column_comment['atom_id_2'],
                     ),
    em.Column.define(
        'comp_id_1', em.builtin_types['text'], nullok=False, comment=column_comment['comp_id_1'],
    ),
    em.Column.define(
        'comp_id_2', em.builtin_types['text'], nullok=False, comment=column_comment['comp_id_2'],
    ),
    em.Column.define(
        'conditional_crosslink_flag',
        em.builtin_types['text'],
        comment=column_comment['conditional_crosslink_flag'],
    ),
    em.Column.define(
        'distance_threshold',
        em.builtin_types['float4'],
        nullok=False,
        comment=column_comment['distance_threshold'],
    ),
    em.Column.define(
        'entity_id_1',
        em.builtin_types['text'],
        nullok=False,
        comment=column_comment['entity_id_1'],
    ),
    em.Column.define(
        'entity_id_2',
        em.builtin_types['text'],
        nullok=False,
        comment=column_comment['entity_id_2'],
    ),
    em.Column.define(
        'group_id', em.builtin_types['int4'], nullok=False, comment=column_comment['group_id'],
    ),
    em.Column.define('id', em.builtin_types['int4'], nullok=False, comment=column_comment['id'],
                     ),
    em.Column.define(
        'model_granularity',
        em.builtin_types['text'],
        nullok=False,
        comment=column_comment['model_granularity'],
    ),
    em.Column.define('psi', em.builtin_types['float4'], comment=column_comment['psi'],
                     ),
    em.Column.define(
        'restraint_type', em.builtin_types['text'], comment=column_comment['restraint_type'],
    ),
    em.Column.define(
        'seq_id_1', em.builtin_types['int4'], nullok=False, comment=column_comment['seq_id_1'],
    ),
    em.Column.define(
        'seq_id_2', em.builtin_types['int4'], nullok=False, comment=column_comment['seq_id_2'],
    ),
    em.Column.define('sigma_1', em.builtin_types['float4'], comment=column_comment['sigma_1'],
                     ),
    em.Column.define('sigma_2', em.builtin_types['float4'], comment=column_comment['sigma_2'],
                     ),
    em.Column.define('Owner', em.builtin_types['text'], comment=column_comment['Owner'],
                     ),
    em.Column.define('Entry_Related_File', em.builtin_types['text'],
                     ),
]

visible_columns = {
    '*': [
        {
            'source': 'RID'
        }, {
            'source': [{
                'outbound': ['PDB', 'ihm_cross_link_restraint_structure_id_fkey']
            }, 'RID']
        }, 'id', {
            'source': [{
                'outbound': ['PDB', 'ihm_cross_link_restraint_group_id_fkey']
            }, 'RID'],
            'markdown_name': 'group id'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_cross_link_restraint_mm_poly_res_label_1_fkey']
                }, 'entity_id'
            ],
            'markdown_name': 'entity id 1'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_cross_link_restraint_mm_poly_res_label_2_fkey']
                }, 'entity_id'
            ],
            'markdown_name': 'entity id 2'
        }, {
            'source': [{
                'outbound': ['PDB', 'ihm_cross_link_restraint_asym_id_1_fkey']
            }, 'RID'],
            'markdown_name': 'asym id 1'
        }, {
            'source': [{
                'outbound': ['PDB', 'ihm_cross_link_restraint_asym_id_2_fkey']
            }, 'RID'],
            'markdown_name': 'asym id 2'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_cross_link_restraint_mm_poly_res_label_1_fkey']
                }, 'mon_id'
            ],
            'markdown_name': 'comp id 1'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_cross_link_restraint_mm_poly_res_label_2_fkey']
                }, 'mon_id'
            ],
            'markdown_name': 'comp id 2'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_cross_link_restraint_mm_poly_res_label_1_fkey']
                }, 'num'
            ],
            'markdown_name': 'seq id 1'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_cross_link_restraint_mm_poly_res_label_2_fkey']
                }, 'num'
            ],
            'markdown_name': 'seq id 2'
        }, {
            'source': 'atom_id_1'
        }, {
            'source': 'atom_id_2'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_cross_link_restraint_restraint_type_fkey']
                }, 'RID'
            ]
        }, ['PDB', 'ihm_cross_link_restraint_conditional_crosslink_flag_fkey'], {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_cross_link_restraint_model_granularity_fkey']
                }, 'RID'
            ]
        }, {
            'source': 'distance_threshold'
        }, {
            'source': 'psi'
        }, {
            'source': 'sigma_1'
        }, {
            'source': 'sigma_2'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_cross_link_restraint_mm_poly_res_label_1_fkey']
                }, 'RID'
            ],
            'markdown_name': 'polymeric residue 1'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_cross_link_restraint_mm_poly_res_label_2_fkey']
                }, 'RID'
            ],
            'markdown_name': 'polymeric residue 2'
        }, ['PDB', 'ihm_cross_link_restraint_Entry_Related_File_fkey']
    ],
    'entry': [
        {
            'source': [{
                'outbound': ['PDB', 'ihm_cross_link_restraint_structure_id_fkey']
            }, 'RID']
        }, 'id', {
            'source': [{
                'outbound': ['PDB', 'ihm_cross_link_restraint_group_id_fkey']
            }, 'RID'],
            'markdown_name': 'group id'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_cross_link_restraint_mm_poly_res_label_1_fkey']
                }, 'entity_id'
            ],
            'markdown_name': 'entity id 1'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_cross_link_restraint_mm_poly_res_label_2_fkey']
                }, 'entity_id'
            ],
            'markdown_name': 'entity id 2'
        }, {
            'source': [{
                'outbound': ['PDB', 'ihm_cross_link_restraint_asym_id_1_fkey']
            }, 'RID'],
            'markdown_name': 'asym id 1'
        }, {
            'source': [{
                'outbound': ['PDB', 'ihm_cross_link_restraint_asym_id_2_fkey']
            }, 'RID'],
            'markdown_name': 'asym id 2'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_cross_link_restraint_mm_poly_res_label_1_fkey']
                }, 'mon_id'
            ],
            'markdown_name': 'comp id 1'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_cross_link_restraint_mm_poly_res_label_2_fkey']
                }, 'mon_id'
            ],
            'markdown_name': 'comp id 2'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_cross_link_restraint_mm_poly_res_label_1_fkey']
                }, 'num'
            ],
            'markdown_name': 'seq id 1'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_cross_link_restraint_mm_poly_res_label_2_fkey']
                }, 'num'
            ],
            'markdown_name': 'seq id 2'
        }, {
            'source': 'atom_id_1'
        }, {
            'source': 'atom_id_2'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_cross_link_restraint_restraint_type_fkey']
                }, 'RID'
            ]
        }, ['PDB', 'ihm_cross_link_restraint_conditional_crosslink_flag_fkey'], {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_cross_link_restraint_model_granularity_fkey']
                }, 'RID'
            ]
        }, {
            'source': 'distance_threshold'
        }, {
            'source': 'psi'
        }, {
            'source': 'sigma_1'
        }, {
            'source': 'sigma_2'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_cross_link_restraint_mm_poly_res_label_1_fkey']
                }, 'RID'
            ],
            'markdown_name': 'polymeric residue 1'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_cross_link_restraint_mm_poly_res_label_2_fkey']
                }, 'RID'
            ],
            'markdown_name': 'polymeric residue 2'
        }
    ],
    'detailed': [
        {
            'source': 'RID'
        }, {
            'source': [{
                'outbound': ['PDB', 'ihm_cross_link_restraint_structure_id_fkey']
            }, 'RID']
        }, 'id', {
            'source': [{
                'outbound': ['PDB', 'ihm_cross_link_restraint_group_id_fkey']
            }, 'RID'],
            'markdown_name': 'group id'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_cross_link_restraint_mm_poly_res_label_1_fkey']
                }, 'entity_id'
            ],
            'markdown_name': 'entity id 1'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_cross_link_restraint_mm_poly_res_label_2_fkey']
                }, 'entity_id'
            ],
            'markdown_name': 'entity id 2'
        }, {
            'source': [{
                'outbound': ['PDB', 'ihm_cross_link_restraint_asym_id_1_fkey']
            }, 'RID'],
            'markdown_name': 'asym id 1'
        }, {
            'source': [{
                'outbound': ['PDB', 'ihm_cross_link_restraint_asym_id_2_fkey']
            }, 'RID'],
            'markdown_name': 'asym id 2'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_cross_link_restraint_mm_poly_res_label_1_fkey']
                }, 'mon_id'
            ],
            'markdown_name': 'comp id 1'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_cross_link_restraint_mm_poly_res_label_2_fkey']
                }, 'mon_id'
            ],
            'markdown_name': 'comp id 2'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_cross_link_restraint_mm_poly_res_label_1_fkey']
                }, 'num'
            ],
            'markdown_name': 'seq id 1'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_cross_link_restraint_mm_poly_res_label_2_fkey']
                }, 'num'
            ],
            'markdown_name': 'seq id 2'
        }, {
            'source': 'atom_id_1'
        }, {
            'source': 'atom_id_2'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_cross_link_restraint_restraint_type_fkey']
                }, 'RID'
            ]
        }, ['PDB', 'ihm_cross_link_restraint_conditional_crosslink_flag_fkey'], {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_cross_link_restraint_model_granularity_fkey']
                }, 'RID'
            ]
        }, {
            'source': 'distance_threshold'
        }, {
            'source': 'psi'
        }, {
            'source': 'sigma_1'
        }, {
            'source': 'sigma_2'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_cross_link_restraint_mm_poly_res_label_1_fkey']
                }, 'RID'
            ],
            'markdown_name': 'polymeric residue 1'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_cross_link_restraint_mm_poly_res_label_2_fkey']
                }, 'RID'
            ],
            'markdown_name': 'polymeric residue 2'
        }, ['PDB', 'ihm_cross_link_restraint_Entry_Related_File_fkey'], {
            'source': 'RCT'
        }, {
            'source': 'RMT'
        }, {
            'source': [{
                'outbound': ['PDB', 'ihm_cross_link_restraint_RCB_fkey']
            }, 'RID']
        }, {
            'source': [{
                'outbound': ['PDB', 'ihm_cross_link_restraint_RMB_fkey']
            }, 'RID']
        }, {
            'source': [{
                'outbound': ['PDB', 'ihm_cross_link_restraint_Owner_fkey']
            }, 'RID']
        }
    ]
}

visible_foreign_keys = {
    'filter': 'detailed',
    'detailed': [
        ['PDB', 'ihm_cross_link_result_restraint_id_fkey'],
        ['PDB', 'ihm_cross_link_result_parameters_restraint_id_fkey']
    ]
}

table_display = {'row_name': {'row_markdown_pattern': '{{{id}}}'}}

table_annotations = {
    chaise_tags.table_display: table_display,
    chaise_tags.visible_columns: visible_columns,
    chaise_tags.visible_foreign_keys: visible_foreign_keys,
}

table_comment = 'Chemical crosslinking restraints used in modeling'

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
                'outbound': ['PDB', 'ihm_cross_link_restraint_structure_id_fkey']
            }, {
                'outbound': ['PDB', 'entry_workflow_status_fkey']
            }, {
                'filter': 'Name',
                'operand': 'REL',
                'operator': '='
            }, 'RID'
        ],
        'projection_type': 'nonnull'
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
                'outbound': ['PDB', 'ihm_cross_link_restraint_structure_id_fkey']
            }, {
                'outbound': ['PDB', 'entry_workflow_status_fkey']
            }, {
                'or': [
                    {
                        'filter': 'Name',
                        'operand': 'DRAFT',
                        'operator': '='
                    }, {
                        'filter': 'Name',
                        'operand': 'DEPO',
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
        constraint_names=[['PDB', 'ihm_cross_link_restraint_primary_key']],
    ),
    em.Key.define(['RID'], constraint_names=[['PDB', 'ihm_cross_link_restraint_RIDkey1']],
                  ),
]

fkey_defs = [
    em.ForeignKey.define(
        ['RMB'],
        'public',
        'ERMrest_Client', ['ID'],
        constraint_names=[['PDB', 'ihm_cross_link_restraint_RMB_fkey']],
    ),
    em.ForeignKey.define(
        ['restraint_type'],
        'Vocab',
        'ihm_cross_link_restraint_restraint_type', ['ID'],
        constraint_names=[['PDB', 'ihm_cross_link_restraint_restraint_type_fkey']],
    ),
    em.ForeignKey.define(
        ['Entry_Related_File'],
        'PDB',
        'Entry_Related_File', ['RID'],
        constraint_names=[['PDB', 'ihm_cross_link_restraint_Entry_Related_File_fkey']],
        on_delete='CASCADE',
    ),
    em.ForeignKey.define(
        ['model_granularity'],
        'Vocab',
        'ihm_cross_link_restraint_model_granularity', ['ID'],
        constraint_names=[['PDB', 'ihm_cross_link_restraint_model_granularity_fkey']],
    ),
    em.ForeignKey.define(
        ['RCB'],
        'public',
        'ERMrest_Client', ['ID'],
        constraint_names=[['PDB', 'ihm_cross_link_restraint_RCB_fkey']],
    ),
    em.ForeignKey.define(
        ['conditional_crosslink_flag'],
        'Vocab',
        'ihm_cross_link_restraint_conditional_crosslink_flag', ['ID'],
        constraint_names=[['PDB', 'ihm_cross_link_restraint_conditional_crosslink_flag_fkey']],
    ),
    em.ForeignKey.define(
        ['asym_id_1', 'structure_id'],
        'PDB',
        'struct_asym', ['id', 'structure_id'],
        constraint_names=[['PDB', 'ihm_cross_link_restraint_asym_id_1_fkey']],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
        on_update='CASCADE',
        on_delete='SET NULL',
    ),
    em.ForeignKey.define(
        ['structure_id', 'group_id'],
        'PDB',
        'ihm_cross_link_list', ['structure_id', 'id'],
        constraint_names=[['PDB', 'ihm_cross_link_restraint_group_id_fkey']],
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
        constraint_names=[['PDB', 'ihm_cross_link_restraint_Owner_fkey']],
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
        constraint_names=[['PDB', 'ihm_cross_link_restraint_structure_id_fkey']],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
        on_update='CASCADE',
        on_delete='SET NULL',
    ),
    em.ForeignKey.define(
        ['entity_id_2', 'seq_id_2', 'comp_id_2', 'structure_id'],
        'PDB',
        'entity_poly_seq', ['entity_id', 'num', 'mon_id', 'structure_id'],
        constraint_names=[['PDB', 'ihm_cross_link_restraint_mm_poly_res_label_2_fkey']],
        annotations={
            chaise_tags.foreign_key: {
                'from_name': 'Ihm Cross Link Restraint Label 2',
                'template_engine': 'handlebars',
                'domain_filter_pattern': '{{#if _structure_id}}structure_id={{{_structure_id}}}{{/if}}'
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
        ['comp_id_1', 'entity_id_1', 'seq_id_1', 'structure_id'],
        'PDB',
        'entity_poly_seq', ['mon_id', 'entity_id', 'num', 'structure_id'],
        constraint_names=[['PDB', 'ihm_cross_link_restraint_mm_poly_res_label_1_fkey']],
        annotations={
            chaise_tags.foreign_key: {
                'from_name': 'Ihm Cross Link Restraint Label 1',
                'template_engine': 'handlebars',
                'domain_filter_pattern': '{{#if _structure_id}}structure_id={{{_structure_id}}}{{/if}}'
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
        ['asym_id_2', 'structure_id'],
        'PDB',
        'struct_asym', ['id', 'structure_id'],
        constraint_names=[['PDB', 'ihm_cross_link_restraint_asym_id_2_fkey']],
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
