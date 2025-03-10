import argparse
from deriva.core import ErmrestCatalog, AttrDict, get_credential
import deriva.core.ermrest_model as em
from deriva.core.ermrest_config import tag as chaise_tags
from deriva.utils.catalog.manage.update_catalog import CatalogUpdater, parse_args

groups = {}

table_name = 'ihm_pseudo_site_feature'

schema_name = 'PDB'

column_annotations = {
    'structure_id': {},
    'Cartn_x': {},
    'Cartn_y': {},
    'Cartn_z': {},
    'description': {},
    'feature_id': {},
    'radius': {},
    'Owner': {}
}

column_comment = {
    'structure_id': 'A reference to table entry.id.',
    'Cartn_x': 'type:float4\nThe Cartesian X component corresponding to this pseudo site.',
    'Cartn_y': 'type:float4\nThe Cartesian Y component corresponding to this pseudo site.',
    'Cartn_z': 'type:float4\nThe Cartesian Z component corresponding to this pseudo site.',
    'description': 'type:text\nTextual description of the pseudo site representing the specific feature.\nexamples:centroid of the feature',
    'feature_id': 'A reference to table ihm_feature_list.feature_id.',
    'radius': 'type:float4\nThe radius associated with the feature at this position, if applicable.',
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
        'Cartn_x', em.builtin_types['float4'], nullok=False, comment=column_comment['Cartn_x'],
    ),
    em.Column.define(
        'Cartn_y', em.builtin_types['float4'], nullok=False, comment=column_comment['Cartn_y'],
    ),
    em.Column.define(
        'Cartn_z', em.builtin_types['float4'], nullok=False, comment=column_comment['Cartn_z'],
    ),
    em.Column.define(
        'description', em.builtin_types['text'], comment=column_comment['description'],
    ),
    em.Column.define(
        'feature_id',
        em.builtin_types['int4'],
        nullok=False,
        comment=column_comment['feature_id'],
    ),
    em.Column.define('radius', em.builtin_types['float4'], comment=column_comment['radius'],
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
                'outbound': ['PDB', 'ihm_pseudo_site_feature_structure_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table entry.id.',
            'markdown_name': 'structure id'
        }, {
            'source': [{
                'outbound': ['PDB', 'ihm_pseudo_site_feature_feature_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table ihm_feature_list.feature_id.',
            'markdown_name': 'feature id'
        }, 'Cartn_x', 'Cartn_y', 'Cartn_z', 'radius', 'description',
        ['PDB', 'ihm_pseudo_site_feature_Entry_Related_File_fkey']
    ],
    'entry': [
        {
            'source': [{
                'outbound': ['PDB', 'ihm_pseudo_site_feature_structure_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table entry.id.',
            'markdown_name': 'structure id'
        }, {
            'source': [{
                'outbound': ['PDB', 'ihm_pseudo_site_feature_feature_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table ihm_feature_list.feature_id.',
            'markdown_name': 'feature id'
        }, 'Cartn_x', 'Cartn_y', 'Cartn_z', 'radius', 'description'
    ],
    'detailed': [
        'RID', {
            'source': [{
                'outbound': ['PDB', 'ihm_pseudo_site_feature_structure_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table entry.id.',
            'markdown_name': 'structure id'
        }, {
            'source': [{
                'outbound': ['PDB', 'ihm_pseudo_site_feature_feature_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table ihm_feature_list.feature_id.',
            'markdown_name': 'feature id'
        }, 'Cartn_x', 'Cartn_y', 'Cartn_z', 'radius', 'description',
        ['PDB', 'ihm_pseudo_site_feature_Entry_Related_File_fkey'],
        ['PDB', 'ihm_pseudo_site_feature_RCB_fkey'], ['PDB', 'ihm_pseudo_site_feature_RMB_fkey'],
        'RCT', 'RMT', ['PDB', 'ihm_pseudo_site_feature_Owner_fkey']
    ]
}

table_annotations = {chaise_tags.visible_columns: visible_columns, }

table_comment = 'Details of pseudo positions used in generic distance restraints'

table_acls = {}

table_acl_bindings = {}

key_defs = [
    em.Key.define(
        ['structure_id', 'feature_id'],
        constraint_names=[['PDB', 'ihm_pseudo_site_feature_primary_key']],
    ),
    em.Key.define(['RID'], constraint_names=[['PDB', 'ihm_pseudo_site_feature_RIDkey1']],
                  ),
]

fkey_defs = [
    em.ForeignKey.define(
        ['RCB'],
        'public',
        'ERMrest_Client', ['ID'],
        constraint_names=[['PDB', 'ihm_pseudo_site_feature_RCB_fkey']],
    ),
    em.ForeignKey.define(
        ['structure_id', 'feature_id'],
        'PDB',
        'ihm_feature_list', ['structure_id', 'feature_id'],
        constraint_names=[['PDB', 'ihm_pseudo_site_feature_feature_id_fkey']],
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
        constraint_names=[['PDB', 'ihm_pseudo_site_feature_RMB_fkey']],
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
