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

table_name = 'ihm_geometric_object_transformation'

schema_name = 'PDB'

column_annotations = {
    'structure_id': {},
    'id': {},
    'rot_matrix_1_1': {},
    'rot_matrix_1_2': {},
    'rot_matrix_1_3': {},
    'rot_matrix_2_1': {},
    'rot_matrix_2_2': {},
    'rot_matrix_2_3': {},
    'rot_matrix_3_1': {},
    'rot_matrix_3_2': {},
    'rot_matrix_3_3': {},
    'tr_vector_1': {},
    'tr_vector_2': {},
    'tr_vector_3': {},
    'Owner': {}
}

column_comment = {
    'structure_id': 'A reference to table entry.id.',
    'id': 'type:int4\nA unique identifier for the transformation.',
    'rot_matrix_1_1': 'type:float4\nData item [1][1] of the rotation matrix used in the transformation.',
    'rot_matrix_1_2': 'type:float4\nData item [1][2] of the rotation matrix used in the transformation.',
    'rot_matrix_1_3': 'type:float4\nData item [1][3] of the rotation matrix used in the transformation.',
    'rot_matrix_2_1': 'type:float4\nData item [2][1] of the rotation matrix used in the transformation.',
    'rot_matrix_2_2': 'type:float4\nData item [2][2] of the rotation matrix used in the transformation.',
    'rot_matrix_2_3': 'type:float4\nData item [2][3] of the rotation matrix used in the transformation.',
    'rot_matrix_3_1': 'type:float4\nData item [3][1] of the rotation matrix used in the transformation.',
    'rot_matrix_3_2': 'type:float4\nData item [3][2] of the rotation matrix used in the transformation.',
    'rot_matrix_3_3': 'type:float4\nData item [3][3] of the rotation matrix used in the transformation.',
    'tr_vector_1': 'type:float4\nData item [1] of the translation vector used in the transformation.',
    'tr_vector_2': 'type:float4\nData item [2] of the translation vector used in the transformation.',
    'tr_vector_3': 'type:float4\nData item [3] of the translation vector used in the transformation.',
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
    em.Column.define('id', em.builtin_types['int4'], nullok=False, comment=column_comment['id'],
                     ),
    em.Column.define(
        'rot_matrix_1_1', em.builtin_types['float4'], comment=column_comment['rot_matrix_1_1'],
    ),
    em.Column.define(
        'rot_matrix_1_2', em.builtin_types['float4'], comment=column_comment['rot_matrix_1_2'],
    ),
    em.Column.define(
        'rot_matrix_1_3', em.builtin_types['float4'], comment=column_comment['rot_matrix_1_3'],
    ),
    em.Column.define(
        'rot_matrix_2_1', em.builtin_types['float4'], comment=column_comment['rot_matrix_2_1'],
    ),
    em.Column.define(
        'rot_matrix_2_2', em.builtin_types['float4'], comment=column_comment['rot_matrix_2_2'],
    ),
    em.Column.define(
        'rot_matrix_2_3', em.builtin_types['float4'], comment=column_comment['rot_matrix_2_3'],
    ),
    em.Column.define(
        'rot_matrix_3_1', em.builtin_types['float4'], comment=column_comment['rot_matrix_3_1'],
    ),
    em.Column.define(
        'rot_matrix_3_2', em.builtin_types['float4'], comment=column_comment['rot_matrix_3_2'],
    ),
    em.Column.define(
        'rot_matrix_3_3', em.builtin_types['float4'], comment=column_comment['rot_matrix_3_3'],
    ),
    em.Column.define(
        'tr_vector_1', em.builtin_types['float4'], comment=column_comment['tr_vector_1'],
    ),
    em.Column.define(
        'tr_vector_2', em.builtin_types['float4'], comment=column_comment['tr_vector_2'],
    ),
    em.Column.define(
        'tr_vector_3', em.builtin_types['float4'], comment=column_comment['tr_vector_3'],
    ),
    em.Column.define('Owner', em.builtin_types['text'], comment=column_comment['Owner'],
                     ),
]

display = {'name': 'Transformations Applied to Geometric Objects'}

visible_columns = {
    '*': [
        'RID', {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_geometric_object_transformation_structure_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table entry.id.',
            'markdown_name': 'structure id'
        }, 'id', 'rot_matrix_1_1', 'rot_matrix_1_2', 'rot_matrix_1_3', 'rot_matrix_2_1',
        'rot_matrix_2_2', 'rot_matrix_2_3', 'rot_matrix_3_1', 'rot_matrix_3_2', 'rot_matrix_3_3',
        'tr_vector_1', 'tr_vector_2', 'tr_vector_3'
    ],
    'entry': [
        {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_geometric_object_transformation_structure_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table entry.id.',
            'markdown_name': 'structure id'
        }, 'id', 'rot_matrix_1_1', 'rot_matrix_1_2', 'rot_matrix_1_3', 'rot_matrix_2_1',
        'rot_matrix_2_2', 'rot_matrix_2_3', 'rot_matrix_3_1', 'rot_matrix_3_2', 'rot_matrix_3_3',
        'tr_vector_1', 'tr_vector_2', 'tr_vector_3'
    ],
    'detailed': [
        'RID', {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_geometric_object_transformation_structure_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table entry.id.',
            'markdown_name': 'structure id'
        }, 'id', 'rot_matrix_1_1', 'rot_matrix_1_2', 'rot_matrix_1_3', 'rot_matrix_2_1',
        'rot_matrix_2_2', 'rot_matrix_2_3', 'rot_matrix_3_1', 'rot_matrix_3_2', 'rot_matrix_3_3',
        'tr_vector_1', 'tr_vector_2', 'tr_vector_3',
        ['PDB', 'ihm_geometric_object_transformation_RCB_fkey'],
        ['PDB', 'ihm_geometric_object_transformation_RMB_fkey'], 'RCT', 'RMT',
        ['PDB', 'ihm_geometric_object_transformation_Owner_fkey']
    ]
}

visible_foreign_keys = {
    'filter': 'detailed',
    'detailed': [
        ['PDB', 'ihm_geometric_object_sphere_transformation_id_fkey'],
        ['PDB', 'ihm_geometric_object_torus_transformation_id_fkey'],
        ['PDB', 'ihm_geometric_object_axis_transformation_id_fkey'],
        ['PDB', 'ihm_geometric_object_plane_transformation_id_fkey']
    ]
}

table_display = {'row_name': {'row_markdown_pattern': '{{{id}}}'}}

table_annotations = {
    chaise_tags.display: display,
    chaise_tags.table_display: table_display,
    chaise_tags.visible_columns: visible_columns,
    chaise_tags.visible_foreign_keys: visible_foreign_keys,
}

table_comment = 'Transformations of geometric objects'

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
                'outbound': ['PDB', 'ihm_geometric_object_transformation_structure_id_fkey']
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
                'outbound': ['PDB', 'ihm_geometric_object_transformation_structure_id_fkey']
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
        ['id', 'structure_id'],
        constraint_names=[['PDB', 'ihm_geometric_object_transformation_primary_key']],
    ),
    em.Key.define(
        ['RID'], constraint_names=[['PDB', 'ihm_geometric_object_transformation_RIDkey1']],
    ),
    em.Key.define(
        ['id', 'RID'],
        constraint_names=[['PDB', 'ihm_geometric_object_transformation_RID_id_key']],
    ),
]

fkey_defs = [
    em.ForeignKey.define(
        ['RMB'],
        'public',
        'ERMrest_Client', ['ID'],
        constraint_names=[['PDB', 'ihm_geometric_object_transformation_RMB_fkey']],
    ),
    em.ForeignKey.define(
        ['RCB'],
        'public',
        'ERMrest_Client', ['ID'],
        constraint_names=[['PDB', 'ihm_geometric_object_transformation_RCB_fkey']],
    ),
    em.ForeignKey.define(
        ['Owner'],
        'public',
        'Catalog_Group', ['ID'],
        constraint_names=[['PDB', 'ihm_geometric_object_transformation_Owner_fkey']],
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
        constraint_names=[['PDB', 'ihm_geometric_object_transformation_structure_id_fkey']],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
        on_update='CASCADE',
        on_delete='CASCADE',
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
