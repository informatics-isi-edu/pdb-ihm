import argparse
from deriva.core import ErmrestCatalog, AttrDict, get_credential
import deriva.core.ermrest_model as em
from deriva.core.ermrest_config import tag as chaise_tags
from deriva.utils.catalog.manage.update_catalog import CatalogUpdater, parse_args

groups = {}

table_name = 'ihm_geometric_object_sphere'

schema_name = 'PDB'

column_annotations = {
    'structure_id': {},
    'center_id': {},
    'object_id': {},
    'radius_r': {},
    'transformation_id': {},
    'Owner': {}
}

column_comment = {
    'structure_id': 'A reference to table entry.id.',
    'center_id': 'A reference to table ihm_geometric_object_center.id.',
    'object_id': 'A reference to table ihm_geometric_object_list.object_id.',
    'radius_r': 'type:float4\nRadius "r" of the sphere.',
    'transformation_id': 'A reference to table ihm_geometric_object_transformation.id.',
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
        'center_id', em.builtin_types['int4'], nullok=False, comment=column_comment['center_id'],
    ),
    em.Column.define(
        'object_id', em.builtin_types['int4'], nullok=False, comment=column_comment['object_id'],
    ),
    em.Column.define(
        'radius_r', em.builtin_types['float4'], nullok=False, comment=column_comment['radius_r'],
    ),
    em.Column.define(
        'transformation_id',
        em.builtin_types['int4'],
        comment=column_comment['transformation_id'],
    ),
    em.Column.define('Owner', em.builtin_types['text'], comment=column_comment['Owner'],
                     ),
    em.Column.define('Transformation_RID', em.builtin_types['text'],
                     ),
]

visible_columns = {
    '*': [
        'RID', {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_geometric_object_sphere_structure_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table entry.id.',
            'markdown_name': 'structure id'
        }, {
            'source': [{
                'outbound': ['PDB', 'ihm_geometric_object_sphere_object_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table ihm_geometric_object_list.object_id.',
            'markdown_name': 'object id'
        }, {
            'source': [{
                'outbound': ['PDB', 'ihm_geometric_object_sphere_center_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table ihm_geometric_object_center.id.',
            'markdown_name': 'center id'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_geometric_object_sphere_transformation_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table ihm_geometric_object_transformation.id.',
            'markdown_name': 'transformation id'
        }, 'radius_r'
    ],
    'entry': [
        {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_geometric_object_sphere_structure_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table entry.id.',
            'markdown_name': 'structure id'
        }, {
            'source': [{
                'outbound': ['PDB', 'ihm_geometric_object_sphere_object_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table ihm_geometric_object_list.object_id.',
            'markdown_name': 'object id'
        }, {
            'source': [{
                'outbound': ['PDB', 'ihm_geometric_object_sphere_center_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table ihm_geometric_object_center.id.',
            'markdown_name': 'center id'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_geometric_object_sphere_transformation_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table ihm_geometric_object_transformation.id.',
            'markdown_name': 'transformation id'
        }, 'radius_r'
    ],
    'detailed': [
        'RID', {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_geometric_object_sphere_structure_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table entry.id.',
            'markdown_name': 'structure id'
        }, {
            'source': [{
                'outbound': ['PDB', 'ihm_geometric_object_sphere_object_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table ihm_geometric_object_list.object_id.',
            'markdown_name': 'object id'
        }, {
            'source': [{
                'outbound': ['PDB', 'ihm_geometric_object_sphere_center_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table ihm_geometric_object_center.id.',
            'markdown_name': 'center id'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_geometric_object_sphere_transformation_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table ihm_geometric_object_transformation.id.',
            'markdown_name': 'transformation id'
        }, 'radius_r', ['PDB', 'ihm_geometric_object_sphere_RCB_fkey'],
        ['PDB', 'ihm_geometric_object_sphere_RMB_fkey'], 'RCT', 'RMT',
        ['PDB', 'ihm_geometric_object_sphere_Owner_fkey']
    ]
}

table_annotations = {chaise_tags.visible_columns: visible_columns, }

table_comment = 'Details of spherical geometric objects'

table_acls = {}

table_acl_bindings = {}

key_defs = [
    em.Key.define(
        ['structure_id', 'object_id'],
        constraint_names=[['PDB', 'ihm_geometric_object_sphere_primary_key']],
    ),
    em.Key.define(['RID'], constraint_names=[['PDB', 'ihm_geometric_object_sphere_RIDkey1']],
                  ),
]

fkey_defs = [
    em.ForeignKey.define(
        ['RMB'],
        'public',
        'ERMrest_Client', ['ID'],
        constraint_names=[['PDB', 'ihm_geometric_object_sphere_RMB_fkey']],
    ),
    em.ForeignKey.define(
        ['RCB'],
        'public',
        'ERMrest_Client', ['ID'],
        constraint_names=[['PDB', 'ihm_geometric_object_sphere_RCB_fkey']],
    ),
    em.ForeignKey.define(
        ['structure_id', 'object_id'],
        'PDB',
        'ihm_geometric_object_list', ['structure_id', 'object_id'],
        constraint_names=[['PDB', 'ihm_geometric_object_sphere_object_id_fkey']],
        annotations={
            chaise_tags.foreign_key: {
                'domain_filter_pattern': 'structure_id={{structure_id}}'
            }
        },
        on_update='CASCADE',
        on_delete='SET NULL',
    ),
    em.ForeignKey.define(
        ['structure_id', 'center_id'],
        'PDB',
        'ihm_geometric_object_center', ['structure_id', 'id'],
        constraint_names=[['PDB', 'ihm_geometric_object_sphere_center_id_fkey']],
        annotations={
            chaise_tags.foreign_key: {
                'domain_filter_pattern': 'structure_id={{structure_id}}'
            }
        },
        on_update='CASCADE',
        on_delete='SET NULL',
    ),
    em.ForeignKey.define(
        ['transformation_id', 'structure_id'],
        'PDB',
        'ihm_geometric_object_transformation', ['id', 'structure_id'],
        constraint_names=[['PDB', 'ihm_geometric_object_sphere_transformation_id_fk']],
        annotations={
            chaise_tags.foreign_key: {
                'domain_filter_pattern': 'structure_id={{structure_id}}'
            }
        },
        on_update='CASCADE',
        on_delete='SET NULL',
    ),
    em.ForeignKey.define(
        ['transformation_id', 'Transformation_RID'],
        'PDB',
        'ihm_geometric_object_transformation', ['id', 'RID'],
        constraint_names=[['PDB', 'ihm_geometric_object_sphere_transformation_id_fkey']],
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
