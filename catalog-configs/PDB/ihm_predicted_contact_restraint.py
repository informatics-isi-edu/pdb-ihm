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

table_name = 'ihm_predicted_contact_restraint'

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
    'id': {
        chaise_tags.generated: None
    },
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
    'structure_id': 'type:text\nThe value of _entry.id identifies the data block.\n\n Note that this item need not be a number; it can be any unique\n identifier.',
    'asym_id_1': 'type:text\nThe value of _struct_asym.id must uniquely identify a record in\n the STRUCT_ASYM list.\n\n Note that this item need not be a number; it can be any unique\n identifier.',
    'asym_id_2': 'type:text\nThe value of _struct_asym.id must uniquely identify a record in\n the STRUCT_ASYM list.\n\n Note that this item need not be a number; it can be any unique\n identifier.',
    'comp_id_1': 'type:text\nThe value of _chem_comp.id must uniquely identify each item in\n the CHEM_COMP list.\n\n For protein polymer entities, this is the three-letter code for\n the amino acid.\n\n For nucleic acid polymer entities, this is the one-letter code\n for the base.',
    'comp_id_2': 'type:text\nThe value of _chem_comp.id must uniquely identify each item in\n the CHEM_COMP list.\n\n For protein polymer entities, this is the three-letter code for\n the amino acid.\n\n For nucleic acid polymer entities, this is the one-letter code\n for the base.',
    'dataset_list_id': 'type:int4\nA unique identifier for the dataset.',
    'distance_lower_limit': 'type:float4\nThe lower limit to the distance threshold applied to this predicted contact restraint\n in the integrative modeling task.',
    'distance_upper_limit': 'type:float4\nThe upper limit to the distance threshold applied to this predicted contact restraint\n in the integrative modeling task.',
    'entity_description_1': 'type:text\nA text description of molecular entity 1. \n',
    'entity_description_2': 'type:text\nA text description of molecular entity 2. \n',
    'entity_id_1': 'type:text\nThe value of _entity.id must uniquely identify a record in the\n ENTITY list.\n\n Note that this item need not be a number; it can be any unique\n identifier.',
    'entity_id_2': 'type:text\nThe value of _entity.id must uniquely identify a record in the\n ENTITY list.\n\n Note that this item need not be a number; it can be any unique\n identifier.',
    'group_id': 'type:int4\nAn identifier to group the predicted contacts.',
    'id': 'type:int4\nA unique identifier for the predicted contact restraint.',
    'model_granularity': 'type:text\nThe granularity of the predicted contact as applied to the multi-scale model.',
    'probability': 'type:float4\nThe real number that indicates the probability that the predicted distance restraint \n is correct. This number should fall between 0.0 and 1.0.',
    'rep_atom_1': 'type:text\nIf _ihm_predicted_contact_restraint.model_granularity is by-residue, then indicate the atom \n used to represent the first monomer partner in three-dimension. Default is the C-alpha atom.',
    'rep_atom_2': 'type:text\nIf _ihm_predicted_contact_restraint.model_granularity is by-residue, then indicate the atom \n used to represent the second monomer partner in three-dimension. Default is the C-alpha atom.',
    'restraint_type': 'type:text\nThe type of distance restraint applied.',
    'seq_id_1': 'type:int4\nThe value of _entity_poly_seq.num must uniquely and sequentially\n identify a record in the ENTITY_POLY_SEQ list.\n\n Note that this item must be a number and that the sequence\n numbers must progress in increasing numerical order.',
    'seq_id_2': 'type:int4\nThe value of _entity_poly_seq.num must uniquely and sequentially\n identify a record in the ENTITY_POLY_SEQ list.\n\n Note that this item must be a number and that the sequence\n numbers must progress in increasing numerical order.',
    'software_id': 'type:int4\n\nAn ordinal index for this category',
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
    em.Column.define(
        'id',
        em.builtin_types['int4'],
        nullok=False,
        annotations=column_annotations['id'],
        comment=column_comment['id'],
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
]

visible_columns = {
    '*': [
        'RID',
        {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_predicted_contact_restraint_structure_id_fkey']
                }, 'RID'
            ],
            'comment': 'type:text\nThe value of _entry.id identifies the data block.\n\n Note that this item need not be a number; it can be any unique\n identifier.',
            'markdown_name': 'structure id'
        },
        {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_predicted_contact_restraint_asym_id_1_fkey']
                }, 'RID'
            ],
            'comment': 'type:text\nThe value of _struct_asym.id must uniquely identify a record in\n the STRUCT_ASYM list.\n\n Note that this item need not be a number; it can be any unique\n identifier.',
            'markdown_name': 'asym id 1'
        },
        {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_predicted_contact_restraint_asym_id_2_fkey']
                }, 'RID'
            ],
            'comment': 'type:text\nThe value of _struct_asym.id must uniquely identify a record in\n the STRUCT_ASYM list.\n\n Note that this item need not be a number; it can be any unique\n identifier.',
            'markdown_name': 'asym id 2'
        },
        {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_predicted_contact_restraint_comp_id_1_fkey']
                }, 'RID'
            ],
            'comment': 'type:text\nThe value of _chem_comp.id must uniquely identify each item in\n the CHEM_COMP list.\n\n For protein polymer entities, this is the three-letter code for\n the amino acid.\n\n For nucleic acid polymer entities, this is the one-letter code\n for the base.',
            'markdown_name': 'comp id 1'
        },
        {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_predicted_contact_restraint_comp_id_2_fkey']
                }, 'RID'
            ],
            'comment': 'type:text\nThe value of _chem_comp.id must uniquely identify each item in\n the CHEM_COMP list.\n\n For protein polymer entities, this is the three-letter code for\n the amino acid.\n\n For nucleic acid polymer entities, this is the one-letter code\n for the base.',
            'markdown_name': 'comp id 2'
        },
        {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_predicted_contact_restraint_dataset_list_id_fkey']
                }, 'RID'
            ],
            'comment': 'type:int4\nA unique identifier for the dataset.',
            'markdown_name': 'dataset list id'
        }, 'distance_lower_limit', 'distance_upper_limit', 'entity_description_1',
        'entity_description_2',
        {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_predicted_contact_restraint_entity_id_1_fkey']
                }, 'RID'
            ],
            'comment': 'type:text\nThe value of _entity.id must uniquely identify a record in the\n ENTITY list.\n\n Note that this item need not be a number; it can be any unique\n identifier.',
            'markdown_name': 'entity id 1'
        },
        {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_predicted_contact_restraint_entity_id_2_fkey']
                }, 'RID'
            ],
            'comment': 'type:text\nThe value of _entity.id must uniquely identify a record in the\n ENTITY list.\n\n Note that this item need not be a number; it can be any unique\n identifier.',
            'markdown_name': 'entity id 2'
        }, 'group_id', 'id', ['PDB', 'predicted_contact_restraint_model_granularity_term_fkey'],
        'probability', ['PDB', 'ihm_predicted_contact_restraint_rep_atom_1_term_fkey'],
        ['PDB', 'ihm_predicted_contact_restraint_rep_atom_2_term_fkey'],
        ['PDB', 'hm_predicted_contact_restraint_restraint_type_term_fkey'],
        {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_predicted_contact_restraint_seq_id_1_fkey']
                }, 'RID'
            ],
            'comment': 'type:int4\nThe value of _entity_poly_seq.num must uniquely and sequentially\n identify a record in the ENTITY_POLY_SEQ list.\n\n Note that this item must be a number and that the sequence\n numbers must progress in increasing numerical order.',
            'markdown_name': 'seq id 1'
        },
        {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_predicted_contact_restraint_seq_id_2_fkey']
                }, 'RID'
            ],
            'comment': 'type:int4\nThe value of _entity_poly_seq.num must uniquely and sequentially\n identify a record in the ENTITY_POLY_SEQ list.\n\n Note that this item must be a number and that the sequence\n numbers must progress in increasing numerical order.',
            'markdown_name': 'seq id 2'
        },
        {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_predicted_contact_restraint_software_id_fkey']
                }, 'RID'
            ],
            'comment': 'type:int4\n\nAn ordinal index for this category',
            'markdown_name': 'software id'
        }, ['PDB', 'ihm_predicted_contact_restraint_RCB_fkey'],
        ['PDB', 'ihm_predicted_contact_restraint_RMB_fkey'], 'RCT', 'RMT',
        ['PDB', 'ihm_predicted_contact_restraint_Owner_fkey']
    ],
    'entry': [
        {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_predicted_contact_restraint_structure_id_fkey']
                }, 'RID'
            ],
            'comment': 'type:text\nThe value of _entry.id identifies the data block.\n\n Note that this item need not be a number; it can be any unique\n identifier.',
            'markdown_name': 'structure id'
        },
        {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_predicted_contact_restraint_asym_id_1_fkey']
                }, 'RID'
            ],
            'comment': 'type:text\nThe value of _struct_asym.id must uniquely identify a record in\n the STRUCT_ASYM list.\n\n Note that this item need not be a number; it can be any unique\n identifier.',
            'markdown_name': 'asym id 1'
        },
        {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_predicted_contact_restraint_asym_id_2_fkey']
                }, 'RID'
            ],
            'comment': 'type:text\nThe value of _struct_asym.id must uniquely identify a record in\n the STRUCT_ASYM list.\n\n Note that this item need not be a number; it can be any unique\n identifier.',
            'markdown_name': 'asym id 2'
        },
        {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_predicted_contact_restraint_comp_id_1_fkey']
                }, 'RID'
            ],
            'comment': 'type:text\nThe value of _chem_comp.id must uniquely identify each item in\n the CHEM_COMP list.\n\n For protein polymer entities, this is the three-letter code for\n the amino acid.\n\n For nucleic acid polymer entities, this is the one-letter code\n for the base.',
            'markdown_name': 'comp id 1'
        },
        {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_predicted_contact_restraint_comp_id_2_fkey']
                }, 'RID'
            ],
            'comment': 'type:text\nThe value of _chem_comp.id must uniquely identify each item in\n the CHEM_COMP list.\n\n For protein polymer entities, this is the three-letter code for\n the amino acid.\n\n For nucleic acid polymer entities, this is the one-letter code\n for the base.',
            'markdown_name': 'comp id 2'
        },
        {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_predicted_contact_restraint_dataset_list_id_fkey']
                }, 'RID'
            ],
            'comment': 'type:int4\nA unique identifier for the dataset.',
            'markdown_name': 'dataset list id'
        }, 'distance_lower_limit', 'distance_upper_limit', 'entity_description_1',
        'entity_description_2',
        {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_predicted_contact_restraint_entity_id_1_fkey']
                }, 'RID'
            ],
            'comment': 'type:text\nThe value of _entity.id must uniquely identify a record in the\n ENTITY list.\n\n Note that this item need not be a number; it can be any unique\n identifier.',
            'markdown_name': 'entity id 1'
        },
        {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_predicted_contact_restraint_entity_id_2_fkey']
                }, 'RID'
            ],
            'comment': 'type:text\nThe value of _entity.id must uniquely identify a record in the\n ENTITY list.\n\n Note that this item need not be a number; it can be any unique\n identifier.',
            'markdown_name': 'entity id 2'
        }, 'group_id', 'id', ['PDB', 'predicted_contact_restraint_model_granularity_term_fkey'],
        'probability', ['PDB', 'ihm_predicted_contact_restraint_rep_atom_1_term_fkey'],
        ['PDB', 'ihm_predicted_contact_restraint_rep_atom_2_term_fkey'],
        ['PDB', 'hm_predicted_contact_restraint_restraint_type_term_fkey'],
        {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_predicted_contact_restraint_seq_id_1_fkey']
                }, 'RID'
            ],
            'comment': 'type:int4\nThe value of _entity_poly_seq.num must uniquely and sequentially\n identify a record in the ENTITY_POLY_SEQ list.\n\n Note that this item must be a number and that the sequence\n numbers must progress in increasing numerical order.',
            'markdown_name': 'seq id 1'
        },
        {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_predicted_contact_restraint_seq_id_2_fkey']
                }, 'RID'
            ],
            'comment': 'type:int4\nThe value of _entity_poly_seq.num must uniquely and sequentially\n identify a record in the ENTITY_POLY_SEQ list.\n\n Note that this item must be a number and that the sequence\n numbers must progress in increasing numerical order.',
            'markdown_name': 'seq id 2'
        },
        {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_predicted_contact_restraint_software_id_fkey']
                }, 'RID'
            ],
            'comment': 'type:int4\n\nAn ordinal index for this category',
            'markdown_name': 'software id'
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
    em.Key.define(['RID'], constraint_names=[('PDB', 'ihm_predicted_contact_restraint_RIDkey1')],
                  ),
    em.Key.define(
        ['structure_id', 'id'],
        constraint_names=[('PDB', 'ihm_predicted_contact_restraint_primary_key')],
    ),
]

fkey_defs = [
    em.ForeignKey.define(
        ['model_granularity'],
        'Vocab',
        'predicted_contact_restraint_model_granularity_term', ['ID'],
        constraint_names=[('PDB', 'predicted_contact_restraint_model_granularity_term_fkey')],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
        on_update='CASCADE',
        on_delete='SET NULL',
    ),
    em.ForeignKey.define(
        ['rep_atom_1'],
        'Vocab',
        'ihm_predicted_contact_restraint_rep_atom_1_term', ['ID'],
        constraint_names=[('PDB', 'ihm_predicted_contact_restraint_rep_atom_1_term_fkey')],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
        on_update='CASCADE',
        on_delete='SET NULL',
    ),
    em.ForeignKey.define(
        ['rep_atom_2'],
        'Vocab',
        'ihm_predicted_contact_restraint_rep_atom_2_term', ['ID'],
        constraint_names=[('PDB', 'ihm_predicted_contact_restraint_rep_atom_2_term_fkey')],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
        on_update='CASCADE',
        on_delete='SET NULL',
    ),
    em.ForeignKey.define(
        ['restraint_type'],
        'Vocab',
        'hm_predicted_contact_restraint_restraint_type_term', ['ID'],
        constraint_names=[('PDB', 'hm_predicted_contact_restraint_restraint_type_term_fkey')],
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
        constraint_names=[('PDB', 'ihm_predicted_contact_restraint_Owner_fkey')],
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
        constraint_names=[('PDB', 'ihm_predicted_contact_restraint_RCB_fkey')],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
    ),
    em.ForeignKey.define(
        ['RMB'],
        'public',
        'ERMrest_Client', ['ID'],
        constraint_names=[('PDB', 'ihm_predicted_contact_restraint_RMB_fkey')],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
    ),
    em.ForeignKey.define(
        ['structure_id'],
        'PDB',
        'entry', ['id'],
        constraint_names=[('PDB', 'ihm_predicted_contact_restraint_structure_id_fkey')],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
        on_update='CASCADE',
        on_delete='SET NULL',
    ),
    em.ForeignKey.define(
        ['structure_id', 'asym_id_1'],
        'PDB',
        'struct_asym', ['structure_id', 'id'],
        constraint_names=[('PDB', 'ihm_predicted_contact_restraint_asym_id_1_fkey')],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
        on_update='CASCADE',
        on_delete='SET NULL',
    ),
    em.ForeignKey.define(
        ['structure_id', 'asym_id_2'],
        'PDB',
        'struct_asym', ['structure_id', 'id'],
        constraint_names=[('PDB', 'ihm_predicted_contact_restraint_asym_id_2_fkey')],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
        on_update='CASCADE',
        on_delete='SET NULL',
    ),
    em.ForeignKey.define(
        ['structure_id', 'dataset_list_id'],
        'PDB',
        'ihm_dataset_list', ['structure_id', 'id'],
        constraint_names=[('PDB', 'ihm_predicted_contact_restraint_dataset_list_id_fkey')],
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
        constraint_names=[('PDB', 'ihm_predicted_contact_restraint_software_id_fkey')],
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
        ['structure_id', 'comp_id_1', 'entity_id_1', 'seq_id_1'],
        'PDB',
        'entity_poly_seq', ['structure_id', 'mon_id', 'entity_id', 'num'],
        constraint_names=[('PDB', 'ihm_predicted_contact_restraint_mm_poly_res_label_1_fkey')],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
        on_update='CASCADE',
        on_delete='SET NULL',
    ),
    em.ForeignKey.define(
        ['structure_id', 'comp_id_2', 'entity_id_2', 'seq_id_2'],
        'PDB',
        'entity_poly_seq', ['structure_id', 'mon_id', 'entity_id', 'num'],
        constraint_names=[('PDB', 'ihm_predicted_contact_restraint_mm_poly_res_label_2_fkey')],
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

