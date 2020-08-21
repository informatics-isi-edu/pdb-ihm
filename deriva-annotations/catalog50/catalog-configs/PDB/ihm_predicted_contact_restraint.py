import argparse
from deriva.core import ErmrestCatalog, AttrDict, get_credential
import deriva.core.ermrest_model as em
from deriva.core.ermrest_config import tag as chaise_tags
from deriva.utils.catalog.manage.update_catalog import CatalogUpdater, parse_args

groups = {}

table_name = 'ihm_predicted_contact_restraint'

schema_name = 'PDB'

column_annotations = {
    'structure_id': {},
    'asym_id_1': {},
    'asym_id_2': {},
    'comp_id_1': {},
    'comp_id_2': {},
    'dataset_list_id': {},
    'distance_lower_limit': {},
    'distance_upper_limit': {},
    'entity_description_1': {},
    'entity_description_2': {},
    'entity_id_1': {},
    'entity_id_2': {},
    'group_id': {},
    'id': {},
    'model_granularity': {},
    'probability': {},
    'rep_atom_1': {},
    'rep_atom_2': {},
    'restraint_type': {},
    'seq_id_1': {},
    'seq_id_2': {},
    'software_id': {},
    'Owner': {}
}

column_comment = {
    'structure_id': 'A reference to table entry.id.',
    'asym_id_1': 'A reference to table struct_asym.id.',
    'asym_id_2': 'A reference to table struct_asym.id.',
    'comp_id_1': 'A reference to table entity_poly_seq.mon_id.',
    'comp_id_2': 'A reference to table entity_poly_seq.mon_id.',
    'dataset_list_id': 'A reference to table ihm_dataset_list.id.',
    'distance_lower_limit': 'type:float4\nThe lower limit to the distance threshold applied to this predicted contact restraint\n in the integrative modeling task.',
    'distance_upper_limit': 'type:float4\nThe upper limit to the distance threshold applied to this predicted contact restraint\n in the integrative modeling task.',
    'entity_description_1': 'type:text\nA text description of molecular entity 1. \n',
    'entity_description_2': 'type:text\nA text description of molecular entity 2. \n',
    'entity_id_1': 'A reference to table entity_poly_seq.entity_id.',
    'entity_id_2': 'A reference to table entity_poly_seq.entity_id.',
    'group_id': 'type:int4\nAn identifier to group the predicted contacts.',
    'id': 'type:int4\nA unique identifier for the predicted contact restraint.',
    'model_granularity': 'type:text\nThe granularity of the predicted contact as applied to the multi-scale model.',
    'probability': 'type:float4\nThe real number that indicates the probability that the predicted distance restraint \n is correct. This number should fall between 0.0 and 1.0.',
    'rep_atom_1': 'type:text\nIf _ihm_predicted_contact_restraint.model_granularity is by-residue, then indicate the atom \n used to represent the first monomer partner in three-dimension. Default is the C-alpha atom.',
    'rep_atom_2': 'type:text\nIf _ihm_predicted_contact_restraint.model_granularity is by-residue, then indicate the atom \n used to represent the second monomer partner in three-dimension. Default is the C-alpha atom.',
    'restraint_type': 'type:text\nThe type of distance restraint applied.',
    'seq_id_1': 'A reference to table entity_poly_seq.num.',
    'seq_id_2': 'A reference to table entity_poly_seq.num.',
    'software_id': 'A reference to table software.pdbx_ordinal.',
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
    em.Column.define(
        'comp_id_1', em.builtin_types['text'], nullok=False, comment=column_comment['comp_id_1'],
    ),
    em.Column.define(
        'comp_id_2', em.builtin_types['text'], nullok=False, comment=column_comment['comp_id_2'],
    ),
    em.Column.define(
        'dataset_list_id',
        em.builtin_types['int4'],
        nullok=False,
        comment=column_comment['dataset_list_id'],
    ),
    em.Column.define(
        'distance_lower_limit',
        em.builtin_types['float4'],
        comment=column_comment['distance_lower_limit'],
    ),
    em.Column.define(
        'distance_upper_limit',
        em.builtin_types['float4'],
        comment=column_comment['distance_upper_limit'],
    ),
    em.Column.define(
        'entity_description_1',
        em.builtin_types['text'],
        comment=column_comment['entity_description_1'],
    ),
    em.Column.define(
        'entity_description_2',
        em.builtin_types['text'],
        comment=column_comment['entity_description_2'],
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
    em.Column.define('group_id', em.builtin_types['int4'], comment=column_comment['group_id'],
                     ),
    em.Column.define('id', em.builtin_types['int4'], nullok=False, comment=column_comment['id'],
                     ),
    em.Column.define(
        'model_granularity',
        em.builtin_types['text'],
        nullok=False,
        comment=column_comment['model_granularity'],
    ),
    em.Column.define(
        'probability', em.builtin_types['float4'], comment=column_comment['probability'],
    ),
    em.Column.define(
        'rep_atom_1', em.builtin_types['text'], comment=column_comment['rep_atom_1'],
    ),
    em.Column.define(
        'rep_atom_2', em.builtin_types['text'], comment=column_comment['rep_atom_2'],
    ),
    em.Column.define(
        'restraint_type',
        em.builtin_types['text'],
        nullok=False,
        comment=column_comment['restraint_type'],
    ),
    em.Column.define(
        'seq_id_1', em.builtin_types['int4'], nullok=False, comment=column_comment['seq_id_1'],
    ),
    em.Column.define(
        'seq_id_2', em.builtin_types['int4'], nullok=False, comment=column_comment['seq_id_2'],
    ),
    em.Column.define(
        'software_id', em.builtin_types['int4'], comment=column_comment['software_id'],
    ),
    em.Column.define('Owner', em.builtin_types['text'], comment=column_comment['Owner'],
                     ),
    em.Column.define('Entry_Related_File', em.builtin_types['text'],
                     ),
    em.Column.define('Software_RID', em.builtin_types['text'],
                     ),
]

visible_columns = {
    '*': [
        'RID', {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_predicted_contact_restraint_structure_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table entry.id.',
            'markdown_name': 'structure id'
        }, 'id', 'group_id', 'entity_description_1', {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_predicted_contact_restraint_mm_poly_res_label_1_fkey']
                }, 'entity_id'
            ],
            'comment': 'A reference to table entity_poly_seq.entity_id.',
            'markdown_name': 'entity id 1'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_predicted_contact_restraint_asym_id_1_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table struct_asym.id.',
            'markdown_name': 'asym id 1'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_predicted_contact_restraint_mm_poly_res_label_1_fkey']
                }, 'mon_id'
            ],
            'comment': 'A reference to table entity_poly_seq.mon_id',
            'markdown_name': 'comp id 1'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_predicted_contact_restraint_mm_poly_res_label_1_fkey']
                }, 'num'
            ],
            'comment': 'A reference to table entity_poly_seq.num',
            'markdown_name': 'seq id 1'
        }, ['PDB', 'ihm_predicted_contact_restraint_rep_atom_1_fkey'], 'entity_description_2', {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_predicted_contact_restraint_mm_poly_res_label_2_fkey']
                }, 'entity_id'
            ],
            'comment': 'A reference to table entity_poly_seq.entity_id',
            'markdown_name': 'entity id 2'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_predicted_contact_restraint_asym_id_2_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table struct_asym.id.',
            'markdown_name': 'asym id 2'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_predicted_contact_restraint_mm_poly_res_label_2_fkey']
                }, 'mon_id'
            ],
            'comment': 'A reference to table entity_poly_seq.mon_id',
            'markdown_name': 'comp id 2'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_predicted_contact_restraint_mm_poly_res_label_2_fkey']
                }, 'mon_id'
            ],
            'comment': 'A reference to table entity_poly_seq.num',
            'markdown_name': 'seq id 2'
        }, ['PDB', 'ihm_predicted_contact_restraint_rep_atom_2_fkey'], 'distance_lower_limit',
        'distance_upper_limit', 'probability',
        ['PDB', 'ihm_predicted_contact_restraint_restraint_type_fkey'],
        ['PDB', 'ihm_predicted_contact_restraint_model_granularity_fkey'], {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_predicted_contact_restraint_software_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table software.pdbx_ordinal.',
            'markdown_name': 'software id'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_predicted_contact_restraint_dataset_list_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table ihm_dataset_list.id.',
            'markdown_name': 'dataset list id'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_predicted_contact_restraint_mm_poly_res_label_1_fkey']
                }, 'RID'
            ],
            'markdown_name': 'polymeric residue 1'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_predicted_contact_restraint_mm_poly_res_label_2_fkey']
                }, 'RID'
            ],
            'markdown_name': 'polymeric residue 2'
        }, ['PDB', 'ihm_predicted_contact_restraint_Entry_Related_File_fkey']
    ],
    'entry': [
        {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_predicted_contact_restraint_structure_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table entry.id.',
            'markdown_name': 'structure id'
        }, 'id', 'group_id', 'entity_description_1', {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_predicted_contact_restraint_mm_poly_res_label_1_fkey']
                }, 'entity_id'
            ],
            'comment': 'A reference to table entity_poly_seq.entity_id.',
            'markdown_name': 'entity id 1'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_predicted_contact_restraint_asym_id_1_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table struct_asym.id.',
            'markdown_name': 'asym id 1'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_predicted_contact_restraint_mm_poly_res_label_1_fkey']
                }, 'mon_id'
            ],
            'comment': 'A reference to table entity_poly_seq.mon_id',
            'markdown_name': 'comp id 1'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_predicted_contact_restraint_mm_poly_res_label_1_fkey']
                }, 'num'
            ],
            'comment': 'A reference to table entity_poly_seq.num',
            'markdown_name': 'seq id 1'
        }, ['PDB', 'ihm_predicted_contact_restraint_rep_atom_1_fkey'], 'entity_description_2', {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_predicted_contact_restraint_mm_poly_res_label_2_fkey']
                }, 'entity_id'
            ],
            'comment': 'A reference to table entity_poly_seq.entity_id',
            'markdown_name': 'entity id 2'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_predicted_contact_restraint_asym_id_2_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table struct_asym.id.',
            'markdown_name': 'asym id 2'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_predicted_contact_restraint_mm_poly_res_label_2_fkey']
                }, 'mon_id'
            ],
            'comment': 'A reference to table entity_poly_seq.mon_id',
            'markdown_name': 'comp id 2'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_predicted_contact_restraint_mm_poly_res_label_2_fkey']
                }, 'mon_id'
            ],
            'comment': 'A reference to table entity_poly_seq.num',
            'markdown_name': 'seq id 2'
        }, ['PDB', 'ihm_predicted_contact_restraint_rep_atom_2_fkey'], 'distance_lower_limit',
        'distance_upper_limit', 'probability',
        ['PDB', 'ihm_predicted_contact_restraint_restraint_type_fkey'],
        ['PDB', 'ihm_predicted_contact_restraint_model_granularity_fkey'], {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_predicted_contact_restraint_software_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table software.pdbx_ordinal.',
            'markdown_name': 'software id'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_predicted_contact_restraint_dataset_list_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table ihm_dataset_list.id.',
            'markdown_name': 'dataset list id'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_predicted_contact_restraint_mm_poly_res_label_1_fkey']
                }, 'RID'
            ],
            'markdown_name': 'polymeric residue 1'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_predicted_contact_restraint_mm_poly_res_label_2_fkey']
                }, 'RID'
            ],
            'markdown_name': 'polymeric residue 2'
        }
    ],
    'detailed': [
        'RID', {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_predicted_contact_restraint_structure_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table entry.id.',
            'markdown_name': 'structure id'
        }, 'id', 'group_id', 'entity_description_1', {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_predicted_contact_restraint_mm_poly_res_label_1_fkey']
                }, 'entity_id'
            ],
            'comment': 'A reference to table entity_poly_seq.entity_id.',
            'markdown_name': 'entity id 1'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_predicted_contact_restraint_asym_id_1_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table struct_asym.id.',
            'markdown_name': 'asym id 1'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_predicted_contact_restraint_mm_poly_res_label_1_fkey']
                }, 'mon_id'
            ],
            'comment': 'A reference to table entity_poly_seq.mon_id',
            'markdown_name': 'comp id 1'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_predicted_contact_restraint_mm_poly_res_label_1_fkey']
                }, 'num'
            ],
            'comment': 'A reference to table entity_poly_seq.num',
            'markdown_name': 'seq id 1'
        }, ['PDB', 'ihm_predicted_contact_restraint_rep_atom_1_fkey'], 'entity_description_2', {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_predicted_contact_restraint_mm_poly_res_label_2_fkey']
                }, 'entity_id'
            ],
            'comment': 'A reference to table entity_poly_seq.entity_id',
            'markdown_name': 'entity id 2'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_predicted_contact_restraint_asym_id_2_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table struct_asym.id.',
            'markdown_name': 'asym id 2'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_predicted_contact_restraint_mm_poly_res_label_2_fkey']
                }, 'mon_id'
            ],
            'comment': 'A reference to table entity_poly_seq.mon_id',
            'markdown_name': 'comp id 2'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_predicted_contact_restraint_mm_poly_res_label_2_fkey']
                }, 'mon_id'
            ],
            'comment': 'A reference to table entity_poly_seq.num',
            'markdown_name': 'seq id 2'
        }, ['PDB', 'ihm_predicted_contact_restraint_rep_atom_2_fkey'], 'distance_lower_limit',
        'distance_upper_limit', 'probability',
        ['PDB', 'ihm_predicted_contact_restraint_restraint_type_fkey'],
        ['PDB', 'ihm_predicted_contact_restraint_model_granularity_fkey'], {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_predicted_contact_restraint_software_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table software.pdbx_ordinal.',
            'markdown_name': 'software id'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_predicted_contact_restraint_dataset_list_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table ihm_dataset_list.id.',
            'markdown_name': 'dataset list id'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_predicted_contact_restraint_mm_poly_res_label_1_fkey']
                }, 'RID'
            ],
            'markdown_name': 'polymeric residue 1'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_predicted_contact_restraint_mm_poly_res_label_2_fkey']
                }, 'RID'
            ],
            'markdown_name': 'polymeric residue 2'
        }, ['PDB', 'ihm_predicted_contact_restraint_Entry_Related_File_fkey'],
        ['PDB', 'ihm_predicted_contact_restraint_RCB_fkey'],
        ['PDB', 'ihm_predicted_contact_restraint_RMB_fkey'], 'RCT', 'RMT',
        ['PDB', 'ihm_predicted_contact_restraint_Owner_fkey']
    ]
}

table_annotations = {chaise_tags.visible_columns: visible_columns, }

table_comment = 'Restraints derived from predicted contacts'

table_acls = {}

table_acl_bindings = {}

key_defs = [
    em.Key.define(
        ['structure_id', 'id'],
        constraint_names=[['PDB', 'ihm_predicted_contact_restraint_primary_key']],
    ),
    em.Key.define(['RID'], constraint_names=[['PDB', 'ihm_predicted_contact_restraint_RIDkey1']],
                  ),
]

fkey_defs = [
    em.ForeignKey.define(
        ['model_granularity'],
        'Vocab',
        'ihm_predicted_contact_restraint_model_granularity', ['Name'],
        constraint_names=[['PDB', 'ihm_predicted_contact_restraint_model_granularity_fkey']],
    ),
    em.ForeignKey.define(
        ['rep_atom_1'],
        'Vocab',
        'ihm_predicted_contact_restraint_rep_atom_1', ['Name'],
        constraint_names=[['PDB', 'ihm_predicted_contact_restraint_rep_atom_1_fkey']],
    ),
    em.ForeignKey.define(
        ['rep_atom_2'],
        'Vocab',
        'ihm_predicted_contact_restraint_rep_atom_2', ['Name'],
        constraint_names=[['PDB', 'ihm_predicted_contact_restraint_rep_atom_2_fkey']],
    ),
    em.ForeignKey.define(
        ['restraint_type'],
        'Vocab',
        'ihm_predicted_contact_restraint_restraint_type', ['Name'],
        constraint_names=[['PDB', 'ihm_predicted_contact_restraint_restraint_type_fkey']],
    ),
    em.ForeignKey.define(
        ['software_id', 'structure_id'],
        'PDB',
        'software', ['pdbx_ordinal', 'structure_id'],
        constraint_names=[['PDB', 'ihm_predicted_contact_restraint_software_id_fk']],
        annotations={
            chaise_tags.foreign_key: {
                'domain_filter_pattern': 'structure_id={{structure_id}}'
            }
        },
        on_update='CASCADE',
        on_delete='SET NULL',
    ),
    em.ForeignKey.define(
        ['Software_RID', 'software_id'],
        'PDB',
        'software', ['RID', 'pdbx_ordinal'],
        constraint_names=[['PDB', 'ihm_predicted_contact_restraint_software_id_fkey']],
        annotations={
            chaise_tags.foreign_key: {
                'domain_filter_pattern': 'structure_id={{structure_id}}'
            }
        },
        on_update='CASCADE',
        on_delete='SET NULL',
    ),
    em.ForeignKey.define(
        ['RMB'],
        'public',
        'ERMrest_Client', ['ID'],
        constraint_names=[['PDB', 'ihm_predicted_contact_restraint_RMB_fkey']],
    ),
    em.ForeignKey.define(
        ['dataset_list_id', 'structure_id'],
        'PDB',
        'ihm_dataset_list', ['id', 'structure_id'],
        constraint_names=[['PDB', 'ihm_predicted_contact_restraint_dataset_list_id_fkey']],
        annotations={
            chaise_tags.foreign_key: {
                'template_engine': 'handlebars',
                'domain_filter_pattern': '{{#if _structure_id}}structure_id={{{_structure_id}}}{{/if}}'
            }
        },
        on_update='CASCADE',
        on_delete='SET NULL',
    ),
    em.ForeignKey.define(
        ['RCB'],
        'public',
        'ERMrest_Client', ['ID'],
        constraint_names=[['PDB', 'ihm_predicted_contact_restraint_RCB_fkey']],
    ),
    em.ForeignKey.define(
        ['asym_id_1', 'structure_id'],
        'PDB',
        'struct_asym', ['id', 'structure_id'],
        constraint_names=[['PDB', 'ihm_predicted_contact_restraint_asym_id_1_fkey']],
        annotations={
            chaise_tags.foreign_key: {
                'template_engine': 'handlebars',
                'domain_filter_pattern': '{{#if _structure_id}}structure_id={{{_structure_id}}}{{/if}}'
            }
        },
        on_update='CASCADE',
        on_delete='SET NULL',
    ),
    em.ForeignKey.define(
        ['asym_id_2', 'structure_id'],
        'PDB',
        'struct_asym', ['id', 'structure_id'],
        constraint_names=[['PDB', 'ihm_predicted_contact_restraint_asym_id_2_fkey']],
        annotations={
            chaise_tags.foreign_key: {
                'template_engine': 'handlebars',
                'domain_filter_pattern': '{{#if _structure_id}}structure_id={{{_structure_id}}}{{/if}}'
            }
        },
        on_update='CASCADE',
        on_delete='SET NULL',
    ),
    em.ForeignKey.define(
        ['structure_id', 'entity_id_1', 'comp_id_1', 'seq_id_1'],
        'PDB',
        'entity_poly_seq', ['structure_id', 'entity_id', 'mon_id', 'num'],
        constraint_names=[['PDB', 'ihm_predicted_contact_restraint_mm_poly_res_label_1_fkey']],
        annotations={
            chaise_tags.foreign_key: {
                'from_name': 'Ihm Predicted Contact Restraint Label 1',
                'template_engine': 'handlebars',
                'domain_filter_pattern': '{{#if _structure_id}}structure_id={{{_structure_id}}}{{/if}}'
            }
        },
        on_update='CASCADE',
        on_delete='SET NULL',
    ),
    em.ForeignKey.define(
        ['seq_id_2', 'structure_id', 'comp_id_2', 'entity_id_2'],
        'PDB',
        'entity_poly_seq', ['num', 'structure_id', 'mon_id', 'entity_id'],
        constraint_names=[['PDB', 'ihm_predicted_contact_restraint_mm_poly_res_label_2_fkey']],
        annotations={
            chaise_tags.foreign_key: {
                'from_name': 'Ihm Predicted Contact Restraint Label 2',
                'template_engine': 'handlebars',
                'domain_filter_pattern': '{{#if _structure_id}}structure_id={{{_structure_id}}}{{/if}}'
            }
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
    catalog_id = 50
    mode, replace, host, catalog_id = parse_args(host, catalog_id, is_table=True)
    catalog = ErmrestCatalog('https', host, catalog_id=catalog_id, credentials=get_credential(host))
    main(catalog, mode, replace)
