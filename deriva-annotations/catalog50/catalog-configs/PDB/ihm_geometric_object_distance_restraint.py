import argparse
from deriva.core import ErmrestCatalog, AttrDict, get_credential
import deriva.core.ermrest_model as em
from deriva.core.ermrest_config import tag as chaise_tags
from deriva.utils.catalog.manage.update_catalog import CatalogUpdater, parse_args

groups = {}

table_name = 'ihm_geometric_object_distance_restraint'

schema_name = 'PDB'

column_annotations = {
    'structure_id': {},
    'dataset_list_id': {},
    'details': {},
    'distance_lower_limit': {},
    'distance_lower_limit_esd': {},
    'distance_probability': {},
    'distance_upper_limit': {},
    'distance_upper_limit_esd': {},
    'feature_id': {},
    'group_conditionality': {},
    'harmonic_force_constant': {},
    'id': {},
    'object_characteristic': {},
    'object_id': {},
    'restraint_type': {},
    'Owner': {}
}

column_comment = {
    'structure_id': 'A reference to table entry.id.',
    'dataset_list_id': 'A reference to table ihm_dataset_list.id.',
    'details': 'type:text\nAdditional details about the geometric object distance restraints, \n especially if _ihm_geometric_object_distance_restraint.restraint_type or\n _ihm_geometric_object_distance_restraint.object_characteristic is "other".',
    'distance_lower_limit': 'type:float4\nThe lower limit to the distance threshold, if applicable.',
    'distance_lower_limit_esd': 'type:float4\nThe estimated standard deviation of the lower limit distance threshold, if applicable.',
    'distance_probability': 'type:float4\nThe real number that indicates the probability that the distance restraint\n is correct. This number should fall between 0.0 and 1.0.',
    'distance_upper_limit': 'type:float4\nThe upper limit to the distance threshold, if applicable.',
    'distance_upper_limit_esd': 'type:float4\nThe estimated standard deviation of the upper limit distance threshold, if applicable.',
    'feature_id': 'A reference to table ihm_feature_list.feature_id.',
    'group_conditionality': 'type:text\nIf a group of atoms or residues are restrained, this data item defines\n the conditionality based on which the restraint is applied in the modeling.',
    'harmonic_force_constant': 'type:float4\nThe harmonic force constant, if applicable.',
    'id': 'type:int4\nA unique id for the geometric object distance restraint.',
    'object_characteristic': 'type:text\nThe characteristic of the geometric object used in the restraint.',
    'object_id': 'A reference to table ihm_geometric_object_list.object_id.',
    'restraint_type': 'type:text\nThe type of restraint applied.',
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
        'dataset_list_id', em.builtin_types['int4'], comment=column_comment['dataset_list_id'],
    ),
    em.Column.define('details', em.builtin_types['text'], comment=column_comment['details'],
                     ),
    em.Column.define(
        'distance_lower_limit',
        em.builtin_types['float4'],
        comment=column_comment['distance_lower_limit'],
    ),
    em.Column.define(
        'distance_lower_limit_esd',
        em.builtin_types['float4'],
        comment=column_comment['distance_lower_limit_esd'],
    ),
    em.Column.define(
        'distance_probability',
        em.builtin_types['float4'],
        comment=column_comment['distance_probability'],
    ),
    em.Column.define(
        'distance_upper_limit',
        em.builtin_types['float4'],
        comment=column_comment['distance_upper_limit'],
    ),
    em.Column.define(
        'distance_upper_limit_esd',
        em.builtin_types['float4'],
        comment=column_comment['distance_upper_limit_esd'],
    ),
    em.Column.define(
        'feature_id',
        em.builtin_types['int4'],
        nullok=False,
        comment=column_comment['feature_id'],
    ),
    em.Column.define(
        'group_conditionality',
        em.builtin_types['text'],
        comment=column_comment['group_conditionality'],
    ),
    em.Column.define(
        'harmonic_force_constant',
        em.builtin_types['float4'],
        comment=column_comment['harmonic_force_constant'],
    ),
    em.Column.define('id', em.builtin_types['int4'], nullok=False, comment=column_comment['id'],
                     ),
    em.Column.define(
        'object_characteristic',
        em.builtin_types['text'],
        comment=column_comment['object_characteristic'],
    ),
    em.Column.define(
        'object_id', em.builtin_types['int4'], nullok=False, comment=column_comment['object_id'],
    ),
    em.Column.define(
        'restraint_type',
        em.builtin_types['text'],
        nullok=False,
        comment=column_comment['restraint_type'],
    ),
    em.Column.define('Owner', em.builtin_types['text'], comment=column_comment['Owner'],
                     ),
    em.Column.define('Entry_Related_File', em.builtin_types['text'],
                     ),
]

visible_columns = {
    '*': [
        'RID', {
            'source': [
                {
                    'outbound': [
                        'PDB', 'ihm_geometric_object_distance_restraint_structure_id_fkey'
                    ]
                }, 'RID'
            ],
            'comment': 'A reference to table entry.id.',
            'markdown_name': 'structure id'
        }, 'id', {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_geometric_object_distance_restraint_object_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table ihm_geometric_object_list.object_id.',
            'markdown_name': 'object id'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_geometric_object_distance_restraint_feature_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table ihm_feature_list.feature_id.',
            'markdown_name': 'feature id'
        }, ['PDB', 'geometric_object_distance_restraint_object_character_fkey'],
        ['PDB',
         'ihm_geometric_object_distance_restraint_restraint_type_fkey'], 'harmonic_force_constant',
        ['PDB', 'geometric_object_distance_restraint_group_condition_fkey'], 'distance_lower_limit',
        'distance_upper_limit', 'distance_lower_limit_esd', 'distance_upper_limit_esd',
        'distance_probability', 'details', {
            'source': [
                {
                    'outbound': [
                        'PDB', 'ihm_geometric_object_distance_restraint_dataset_list_id_fkey'
                    ]
                }, 'RID'
            ],
            'comment': 'A reference to table ihm_dataset_list.id.',
            'markdown_name': 'dataset list id'
        }, ['PDB', 'geometric_object_distance_restraint_Entry_Related_File_fkey']
    ],
    'entry': [
        {
            'source': [
                {
                    'outbound': [
                        'PDB', 'ihm_geometric_object_distance_restraint_structure_id_fkey'
                    ]
                }, 'RID'
            ],
            'comment': 'A reference to table entry.id.',
            'markdown_name': 'structure id'
        }, 'id', {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_geometric_object_distance_restraint_object_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table ihm_geometric_object_list.object_id.',
            'markdown_name': 'object id'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_geometric_object_distance_restraint_feature_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table ihm_feature_list.feature_id.',
            'markdown_name': 'feature id'
        }, ['PDB', 'geometric_object_distance_restraint_object_character_fkey'],
        ['PDB',
         'ihm_geometric_object_distance_restraint_restraint_type_fkey'], 'harmonic_force_constant',
        ['PDB', 'geometric_object_distance_restraint_group_condition_fkey'], 'distance_lower_limit',
        'distance_upper_limit', 'distance_lower_limit_esd', 'distance_upper_limit_esd',
        'distance_probability', 'details', {
            'source': [
                {
                    'outbound': [
                        'PDB', 'ihm_geometric_object_distance_restraint_dataset_list_id_fkey'
                    ]
                }, 'RID'
            ],
            'comment': 'A reference to table ihm_dataset_list.id.',
            'markdown_name': 'dataset list id'
        }
    ],
    'detailed': [
        'RID', {
            'source': [
                {
                    'outbound': [
                        'PDB', 'ihm_geometric_object_distance_restraint_structure_id_fkey'
                    ]
                }, 'RID'
            ],
            'comment': 'A reference to table entry.id.',
            'markdown_name': 'structure id'
        }, 'id', {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_geometric_object_distance_restraint_object_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table ihm_geometric_object_list.object_id.',
            'markdown_name': 'object id'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_geometric_object_distance_restraint_feature_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table ihm_feature_list.feature_id.',
            'markdown_name': 'feature id'
        }, ['PDB', 'geometric_object_distance_restraint_object_character_fkey'],
        ['PDB',
         'ihm_geometric_object_distance_restraint_restraint_type_fkey'], 'harmonic_force_constant',
        ['PDB', 'geometric_object_distance_restraint_group_condition_fkey'], 'distance_lower_limit',
        'distance_upper_limit', 'distance_lower_limit_esd', 'distance_upper_limit_esd',
        'distance_probability', 'details', {
            'source': [
                {
                    'outbound': [
                        'PDB', 'ihm_geometric_object_distance_restraint_dataset_list_id_fkey'
                    ]
                }, 'RID'
            ],
            'comment': 'A reference to table ihm_dataset_list.id.',
            'markdown_name': 'dataset list id'
        }, ['PDB', 'geometric_object_distance_restraint_Entry_Related_File_fkey'],
        ['PDB', 'ihm_geometric_object_distance_restraint_RCB_fkey'],
        ['PDB', 'ihm_geometric_object_distance_restraint_RMB_fkey'], 'RCT', 'RMT',
        ['PDB', 'ihm_geometric_object_distance_restraint_Owner_fkey']
    ]
}

table_annotations = {chaise_tags.visible_columns: visible_columns, }

table_comment = 'Generic distance restraints between geometric objects and molecular features (atoms, residues etc.)'

table_acls = {}

table_acl_bindings = {}

key_defs = [
    em.Key.define(
        ['structure_id', 'id'],
        constraint_names=[['PDB', 'ihm_geometric_object_distance_restraint_primary_key']],
    ),
    em.Key.define(
        ['RID'], constraint_names=[['PDB', 'ihm_geometric_object_distance_restraint_RIDkey1']],
    ),
]

fkey_defs = [
    em.ForeignKey.define(
        ['group_conditionality'],
        'Vocab',
        'geometric_object_distance_restraint_group_condition', ['Name'],
        constraint_names=[['PDB', 'geometric_object_distance_restraint_group_condition_fkey']],
    ),
    em.ForeignKey.define(
        ['object_characteristic'],
        'Vocab',
        'geometric_object_distance_restraint_object_character', ['Name'],
        constraint_names=[['PDB', 'geometric_object_distance_restraint_object_character_fkey']],
    ),
    em.ForeignKey.define(
        ['restraint_type'],
        'Vocab',
        'ihm_geometric_object_distance_restraint_restraint_type', ['Name'],
        constraint_names=[['PDB', 'ihm_geometric_object_distance_restraint_restraint_type_fkey']],
    ),
    em.ForeignKey.define(
        ['object_id', 'structure_id'],
        'PDB',
        'ihm_geometric_object_list', ['object_id', 'structure_id'],
        constraint_names=[['PDB', 'ihm_geometric_object_distance_restraint_object_id_fkey']],
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
        constraint_names=[['PDB', 'ihm_geometric_object_distance_restraint_RMB_fkey']],
    ),
    em.ForeignKey.define(
        ['feature_id', 'structure_id'],
        'PDB',
        'ihm_feature_list', ['feature_id', 'structure_id'],
        constraint_names=[['PDB', 'ihm_geometric_object_distance_restraint_feature_id_fkey']],
        annotations={
            chaise_tags.foreign_key: {
                'domain_filter_pattern': 'structure_id={{structure_id}}'
            }
        },
        on_update='CASCADE',
        on_delete='SET NULL',
    ),
    em.ForeignKey.define(
        ['RCB'],
        'public',
        'ERMrest_Client', ['ID'],
        constraint_names=[['PDB', 'ihm_geometric_object_distance_restraint_RCB_fkey']],
    ),
    em.ForeignKey.define(
        ['structure_id', 'dataset_list_id'],
        'PDB',
        'ihm_dataset_list', ['structure_id', 'id'],
        constraint_names=[['PDB', 'ihm_geometric_object_distance_restraint_dataset_list_id_fkey']],
        annotations={
            chaise_tags.foreign_key: {
                'domain_filter_pattern': 'structure_id={{structure_id}}'
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
