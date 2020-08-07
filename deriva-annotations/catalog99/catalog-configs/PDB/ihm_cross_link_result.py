import argparse
from deriva.core import ErmrestCatalog, AttrDict, get_credential
import deriva.core.ermrest_model as em
from deriva.core.ermrest_config import tag as chaise_tags
from deriva.utils.catalog.manage.update_catalog import CatalogUpdater, parse_args

groups = {}

table_name = 'ihm_cross_link_result'

schema_name = 'PDB'

column_annotations = {
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
    em.Column.define('Entry_Related_File', em.builtin_types['text'],
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
        }, 'id', {
            'source': [{
                'outbound': ['PDB', 'ihm_cross_link_result_restraint_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table ihm_cross_link_restraint.id.',
            'markdown_name': 'restraint id'
        }, {
            'source': [{
                'outbound': ['PDB', 'ihm_cross_link_result_ensemble_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table ihm_ensemble_info.ensemble_id.',
            'markdown_name': 'ensemble id'
        }, 'num_models', 'distance_threshold', 'median_distance', 'details',
        ['PDB', 'ihm_cross_link_result_Entry_Related_File_fkey']
    ],
    'entry': [
        {
            'source': [{
                'outbound': ['PDB', 'ihm_cross_link_result_structure_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table entry.id.',
            'markdown_name': 'structure id'
        }, 'id', {
            'source': [{
                'outbound': ['PDB', 'ihm_cross_link_result_restraint_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table ihm_cross_link_restraint.id.',
            'markdown_name': 'restraint id'
        }, {
            'source': [{
                'outbound': ['PDB', 'ihm_cross_link_result_ensemble_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table ihm_ensemble_info.ensemble_id.',
            'markdown_name': 'ensemble id'
        }, 'num_models', 'distance_threshold', 'median_distance', 'details'
    ],
    'detailed': [
        'RID', {
            'source': [{
                'outbound': ['PDB', 'ihm_cross_link_result_structure_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table entry.id.',
            'markdown_name': 'structure id'
        }, 'id', {
            'source': [{
                'outbound': ['PDB', 'ihm_cross_link_result_restraint_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table ihm_cross_link_restraint.id.',
            'markdown_name': 'restraint id'
        }, {
            'source': [{
                'outbound': ['PDB', 'ihm_cross_link_result_ensemble_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table ihm_ensemble_info.ensemble_id.',
            'markdown_name': 'ensemble id'
        }, 'num_models', 'distance_threshold', 'median_distance', 'details',
        ['PDB', 'ihm_cross_link_result_Entry_Related_File_fkey'],
        ['PDB', 'ihm_cross_link_result_RCB_fkey'], ['PDB', 'ihm_cross_link_result_RMB_fkey'], 'RCT',
        'RMT', ['PDB', 'ihm_cross_link_result_Owner_fkey']
    ]
}

table_annotations = {chaise_tags.visible_columns: visible_columns, }

table_comment = 'Results of the crosslinking restraints in integrative modeling'

table_acls = {}

table_acl_bindings = {}

key_defs = [
    em.Key.define(
        ['id', 'structure_id'], constraint_names=[['PDB', 'ihm_cross_link_result_primary_key']],
    ),
    em.Key.define(['RID'], constraint_names=[['PDB', 'ihm_cross_link_result_RIDkey1']],
                  ),
]

fkey_defs = [
    em.ForeignKey.define(
        ['RMB'],
        'public',
        'ERMrest_Client', ['ID'],
        constraint_names=[['PDB', 'ihm_cross_link_result_RMB_fkey']],
    ),
    em.ForeignKey.define(
        ['RCB'],
        'public',
        'ERMrest_Client', ['ID'],
        constraint_names=[['PDB', 'ihm_cross_link_result_RCB_fkey']],
    ),
    em.ForeignKey.define(
        ['structure_id', 'ensemble_id'],
        'PDB',
        'ihm_ensemble_info', ['structure_id', 'ensemble_id'],
        constraint_names=[['PDB', 'ihm_cross_link_result_ensemble_id_fkey']],
        annotations={
            chaise_tags.foreign_key: {
                'domain_filter_pattern': 'structure_id={{structure_id}}'
            }
        },
        on_update='CASCADE',
        on_delete='SET NULL',
    ),
    em.ForeignKey.define(
        ['structure_id', 'restraint_id'],
        'PDB',
        'ihm_cross_link_restraint', ['structure_id', 'id'],
        constraint_names=[['PDB', 'ihm_cross_link_result_restraint_id_fkey']],
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
    catalog_id = 99
    mode, replace, host, catalog_id = parse_args(host, catalog_id, is_table=True)
    catalog = ErmrestCatalog('https', host, catalog_id=catalog_id, credentials=get_credential(host))
    main(catalog, mode, replace)
