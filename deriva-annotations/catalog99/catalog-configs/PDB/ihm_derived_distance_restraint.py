import argparse
from deriva.core import ErmrestCatalog, AttrDict, get_credential
import deriva.core.ermrest_model as em
from deriva.core.ermrest_config import tag as chaise_tags
from deriva.utils.catalog.manage.update_catalog import CatalogUpdater, parse_args

groups = {}

table_name = 'ihm_derived_distance_restraint'

schema_name = 'PDB'

column_annotations = {
    'structure_id': {},
    'dataset_list_id': {},
    'distance_lower_limit': {},
    'distance_lower_limit_esd': {},
    'distance_upper_limit': {},
    'distance_upper_limit_esd': {},
    'feature_id_1': {},
    'feature_id_2': {},
    'group_conditionality': {},
    'group_id': {},
    'id': {},
    'mic_value': {},
    'probability': {},
    'random_exclusion_fraction': {},
    'restraint_type': {},
    'Owner': {}
}

column_comment = {
    'structure_id': 'A reference to table entry.id.',
    'dataset_list_id': 'A reference to table ihm_dataset_list.id.',
    'distance_lower_limit': 'type:float4\nThe lower limit to the distance threshold applied to this distance restraint\n in the integrative modeling task.',
    'distance_lower_limit_esd': 'type:float4\nThe estimated standard deviation of the lower limit distance threshold applied to this distance restraint\n in the integrative modeling task.',
    'distance_upper_limit': 'type:float4\nThe upper limit to the distance threshold applied to this distance restraint\n in the integrative modeling task.',
    'distance_upper_limit_esd': 'type:float4\nThe estimated standard deviation of the upper limit distance threshold applied to this distance restraint\n in the integrative modeling task.',
    'feature_id_1': 'A reference to table ihm_feature_list.feature_id.',
    'feature_id_2': 'A reference to table ihm_feature_list.feature_id.',
    'group_conditionality': 'type:text\nIf a group of atoms or residues are restrained, this data item defines \n the conditionality based on which the restraint is applied in the modeling.',
    'group_id': 'type:int4\nAn identifier to group the distance restraints. \n This can be the same as the _ihm_derived_distance_restraint.id in case\n the some of the restraints are not grouped.',
    'id': 'type:int4\nA unique identifier for the derived distance restraint.',
    'mic_value': 'type:float4\nThe value of the Maximal Information Co-efficient (MIC), if applicable. \n MIC values are correlation measures derived from the genetic profiles\n and are used to derive restraint information  from quantitative measurements \n of genetic interactions.',
    'probability': 'type:float4\nThe real number that indicates the probability that the distance restraint \n is correct. This number should fall between 0.0 and 1.0.',
    'random_exclusion_fraction': 'type:float4\nThe fraction of randomly excluded distance restraints during modeling. \n In HADDOCK, this is used along with ambiguous interface restraints (AIRs) \n to account for uncertainties in AIRs.',
    'restraint_type': 'type:text\nThe type of distance restraint applied.',
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
        'feature_id_1',
        em.builtin_types['int4'],
        nullok=False,
        comment=column_comment['feature_id_1'],
    ),
    em.Column.define(
        'feature_id_2',
        em.builtin_types['int4'],
        nullok=False,
        comment=column_comment['feature_id_2'],
    ),
    em.Column.define(
        'group_conditionality',
        em.builtin_types['text'],
        comment=column_comment['group_conditionality'],
    ),
    em.Column.define('group_id', em.builtin_types['int4'], comment=column_comment['group_id'],
                     ),
    em.Column.define('id', em.builtin_types['int4'], nullok=False, comment=column_comment['id'],
                     ),
    em.Column.define(
        'mic_value', em.builtin_types['float4'], comment=column_comment['mic_value'],
    ),
    em.Column.define(
        'probability', em.builtin_types['float4'], comment=column_comment['probability'],
    ),
    em.Column.define(
        'random_exclusion_fraction',
        em.builtin_types['float4'],
        comment=column_comment['random_exclusion_fraction'],
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
                    'outbound': ['PDB', 'ihm_derived_distance_restraint_structure_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table entry.id.',
            'markdown_name': 'structure id'
        }, 'id', 'group_id', {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_derived_distance_restraint_feature_id_1_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table ihm_feature_list.feature_id.',
            'markdown_name': 'feature id 1'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_derived_distance_restraint_feature_id_2_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table ihm_feature_list.feature_id.',
            'markdown_name': 'feature id 2'
        }, ['PDB', 'ihm_derived_distance_restraint_group_conditionality_fkey'],
        'random_exclusion_fraction', 'distance_lower_limit', 'distance_upper_limit',
        'distance_lower_limit_esd', 'distance_upper_limit_esd', 'probability',
        ['PDB', 'ihm_derived_distance_restraint_restraint_type_fkey'], 'mic_value', {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_derived_distance_restraint_dataset_list_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table ihm_dataset_list.id.',
            'markdown_name': 'dataset list id'
        }, ['PDB', 'ihm_derived_distance_restraint_Entry_Related_File_fkey']
    ],
    'entry': [
        {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_derived_distance_restraint_structure_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table entry.id.',
            'markdown_name': 'structure id'
        }, 'id', 'group_id', {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_derived_distance_restraint_feature_id_1_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table ihm_feature_list.feature_id.',
            'markdown_name': 'feature id 1'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_derived_distance_restraint_feature_id_2_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table ihm_feature_list.feature_id.',
            'markdown_name': 'feature id 2'
        }, ['PDB', 'ihm_derived_distance_restraint_group_conditionality_fkey'],
        'random_exclusion_fraction', 'distance_lower_limit', 'distance_upper_limit',
        'distance_lower_limit_esd', 'distance_upper_limit_esd', 'probability',
        ['PDB', 'ihm_derived_distance_restraint_restraint_type_fkey'], 'mic_value', {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_derived_distance_restraint_dataset_list_id_fkey']
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
                    'outbound': ['PDB', 'ihm_derived_distance_restraint_structure_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table entry.id.',
            'markdown_name': 'structure id'
        }, 'id', 'group_id', {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_derived_distance_restraint_feature_id_1_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table ihm_feature_list.feature_id.',
            'markdown_name': 'feature id 1'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_derived_distance_restraint_feature_id_2_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table ihm_feature_list.feature_id.',
            'markdown_name': 'feature id 2'
        }, ['PDB', 'ihm_derived_distance_restraint_group_conditionality_fkey'],
        'random_exclusion_fraction', 'distance_lower_limit', 'distance_upper_limit',
        'distance_lower_limit_esd', 'distance_upper_limit_esd', 'probability',
        ['PDB', 'ihm_derived_distance_restraint_restraint_type_fkey'], 'mic_value', {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_derived_distance_restraint_dataset_list_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table ihm_dataset_list.id.',
            'markdown_name': 'dataset list id'
        }, ['PDB', 'ihm_derived_distance_restraint_Entry_Related_File_fkey'],
        ['PDB', 'ihm_derived_distance_restraint_RCB_fkey'],
        ['PDB', 'ihm_derived_distance_restraint_RMB_fkey'], 'RCT', 'RMT',
        ['PDB', 'ihm_derived_distance_restraint_Owner_fkey']
    ]
}

table_annotations = {chaise_tags.visible_columns: visible_columns, }

table_comment = 'Generic distance restraints between features (atoms, residues, non-polymeric entities, pseudo sites)'

table_acls = {}

table_acl_bindings = {}

key_defs = [
    em.Key.define(
        ['id', 'structure_id'],
        constraint_names=[['PDB', 'ihm_derived_distance_restraint_primary_key']],
    ),
    em.Key.define(['RID'], constraint_names=[['PDB', 'ihm_derived_distance_restraint_RIDkey1']],
                  ),
]

fkey_defs = [
    em.ForeignKey.define(
        ['RCB'],
        'public',
        'ERMrest_Client', ['ID'],
        constraint_names=[['PDB', 'ihm_derived_distance_restraint_RCB_fkey']],
    ),
    em.ForeignKey.define(
        ['RMB'],
        'public',
        'ERMrest_Client', ['ID'],
        constraint_names=[['PDB', 'ihm_derived_distance_restraint_RMB_fkey']],
    ),
    em.ForeignKey.define(
        ['group_conditionality'],
        'Vocab',
        'ihm_derived_distance_restraint_group_conditionality', ['Name'],
        constraint_names=[['PDB', 'ihm_derived_distance_restraint_group_conditionality_fkey']],
    ),
    em.ForeignKey.define(
        ['restraint_type'],
        'Vocab',
        'ihm_derived_distance_restraint_restraint_type', ['Name'],
        constraint_names=[['PDB', 'ihm_derived_distance_restraint_restraint_type_fkey']],
    ),
    em.ForeignKey.define(
        ['dataset_list_id', 'structure_id'],
        'PDB',
        'ihm_dataset_list', ['id', 'structure_id'],
        constraint_names=[['PDB', 'ihm_derived_distance_restraint_dataset_list_id_fkey']],
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
        ['feature_id_2', 'structure_id'],
        'PDB',
        'ihm_feature_list', ['feature_id', 'structure_id'],
        constraint_names=[['PDB', 'ihm_derived_distance_restraint_feature_id_2_fkey']],
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
        ['feature_id_1', 'structure_id'],
        'PDB',
        'ihm_feature_list', ['feature_id', 'structure_id'],
        constraint_names=[['PDB', 'ihm_derived_distance_restraint_feature_id_1_fkey']],
        annotations={
            chaise_tags.foreign_key: {
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
    catalog_id = 99
    mode, replace, host, catalog_id = parse_args(host, catalog_id, is_table=True)
    catalog = ErmrestCatalog('https', host, catalog_id=catalog_id, credentials=get_credential(host))
    main(catalog, mode, replace)
