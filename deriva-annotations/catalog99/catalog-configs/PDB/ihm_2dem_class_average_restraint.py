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

table_name = 'ihm_2dem_class_average_restraint'

schema_name = 'PDB'

column_annotations = {
    'structure_id': {},
    'dataset_list_id': {},
    'details': {},
    'id': {},
    'image_resolution': {},
    'image_segment_flag': {},
    'number_of_projections': {},
    'number_raw_micrographs': {},
    'pixel_size_height': {},
    'pixel_size_width': {},
    'struct_assembly_id': {},
    'Owner': {}
}

column_comment = {
    'structure_id': 'A reference to table entry.id.',
    'dataset_list_id': 'A reference to table ihm_dataset_list.id.',
    'details': 'type:text\nDetails of how the 2DEM restraint is applied in the modeling algorithm.\nexamples:The 2DEM restraint fits a given model to an 2DEM class average and\n        computes a score that quantifies the match. The computation proceeds\n        in three stages: generation of 3D model projections on a 2D grid, \n        alignment of the model projections and the 2DEM class average image, \n        and calculation of the best fitting score.',
    'id': 'type:int4\nA unique identifier for the 2dem class average.',
    'image_resolution': 'type:float4\nResolution of the 2dem class average.',
    'image_segment_flag': 'type:text\nA flag that indicates whether or not the 2DEM class average image is segmented i.e.,\n whether the whole image is used or only a portion of it is used (by masking \n or by other means) as restraint in the modeling.',
    'number_of_projections': 'type:int4\nNumber of 2D projections of the model used in the fitting.',
    'number_raw_micrographs': 'type:int4\nThe number of raw micrographs used to obtain the class average.',
    'pixel_size_height': 'type:float4\nPixel size height of the 2dem class average image.\n While fitting the model to the image, _ihm_2dem_class_average_restraint.pixel_size_height\n is used along with _ihm_2dem_class_average_restraint.pixel_size_width to scale the image.',
    'pixel_size_width': 'type:float4\nPixel size width of the 2dem class average image.\n While fitting the model to the image, _ihm_2dem_class_average_restraint.pixel_size_width\n is used along with _ihm_2dem_class_average_restraint.pixel_size_height to scale the image.',
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
        'dataset_list_id',
        em.builtin_types['int4'],
        nullok=False,
        comment=column_comment['dataset_list_id'],
    ),
    em.Column.define('details', em.builtin_types['text'], comment=column_comment['details'],
                     ),
    em.Column.define('id', em.builtin_types['int4'], nullok=False, comment=column_comment['id'],
                     ),
    em.Column.define(
        'image_resolution',
        em.builtin_types['float4'],
        comment=column_comment['image_resolution'],
    ),
    em.Column.define(
        'image_segment_flag',
        em.builtin_types['text'],
        comment=column_comment['image_segment_flag'],
    ),
    em.Column.define(
        'number_of_projections',
        em.builtin_types['int4'],
        comment=column_comment['number_of_projections'],
    ),
    em.Column.define(
        'number_raw_micrographs',
        em.builtin_types['int4'],
        comment=column_comment['number_raw_micrographs'],
    ),
    em.Column.define(
        'pixel_size_height',
        em.builtin_types['float4'],
        comment=column_comment['pixel_size_height'],
    ),
    em.Column.define(
        'pixel_size_width',
        em.builtin_types['float4'],
        comment=column_comment['pixel_size_width'],
    ),
    em.Column.define(
        'struct_assembly_id',
        em.builtin_types['int4'],
        nullok=False,
        comment=column_comment['struct_assembly_id'],
    ),
    em.Column.define('Owner', em.builtin_types['text'], comment=column_comment['Owner'],
                     ),
]

display = {'name': '2DEM Class Average Restraints'}

visible_columns = {
    '*': [
        'RID', {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_2dem_class_average_restraint_structure_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table entry.id.',
            'markdown_name': 'structure id'
        }, 'id', 'number_raw_micrographs', 'pixel_size_width', 'pixel_size_height',
        'image_resolution', ['PDB', 'ihm_2dem_class_average_restraint_image_segment_flag_fkey'],
        'number_of_projections', {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_2dem_class_average_restraint_struct_assembly_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table ihm_struct_assembly.id.',
            'markdown_name': 'struct assembly id'
        }, 'details', {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_2dem_class_average_restraint_dataset_list_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table ihm_dataset_list.id.',
            'markdown_name': 'dataset list id'
        }
    ],
    'entry': [
        {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_2dem_class_average_restraint_structure_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table entry.id.',
            'markdown_name': 'structure id'
        }, 'id', 'number_raw_micrographs', 'pixel_size_width', 'pixel_size_height',
        'image_resolution', ['PDB', 'ihm_2dem_class_average_restraint_image_segment_flag_fkey'],
        'number_of_projections', {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_2dem_class_average_restraint_struct_assembly_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table ihm_struct_assembly.id.',
            'markdown_name': 'struct assembly id'
        }, 'details', {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_2dem_class_average_restraint_dataset_list_id_fkey']
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
                    'outbound': ['PDB', 'ihm_2dem_class_average_restraint_structure_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table entry.id.',
            'markdown_name': 'structure id'
        }, 'id', 'number_raw_micrographs', 'pixel_size_width', 'pixel_size_height',
        'image_resolution', ['PDB', 'ihm_2dem_class_average_restraint_image_segment_flag_fkey'],
        'number_of_projections', {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_2dem_class_average_restraint_struct_assembly_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table ihm_struct_assembly.id.',
            'markdown_name': 'struct assembly id'
        }, 'details', {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_2dem_class_average_restraint_dataset_list_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table ihm_dataset_list.id.',
            'markdown_name': 'dataset list id'
        }, ['PDB', 'ihm_2dem_class_average_restraint_RCB_fkey'],
        ['PDB', 'ihm_2dem_class_average_restraint_RMB_fkey'], 'RCT', 'RMT',
        ['PDB', 'ihm_2dem_class_average_restraint_Owner_fkey']
    ]
}

visible_foreign_keys = {
    'filter': 'detailed',
    'detailed': [['PDB', 'ihm_2dem_class_average_fitting_restraint_id_fkey']]
}

table_display = {'row_name': {'row_markdown_pattern': '{{{id}}}'}}

table_annotations = {
    chaise_tags.display: display,
    chaise_tags.table_display: table_display,
    chaise_tags.visible_columns: visible_columns,
    chaise_tags.visible_foreign_keys: visible_foreign_keys,
}

table_comment = '2DEM images used as restraints in the modeling'

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
                'outbound': ['PDB', 'ihm_2dem_class_average_restraint_structure_id_fkey']
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
                'outbound': ['PDB', 'ihm_2dem_class_average_restraint_structure_id_fkey']
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
        constraint_names=[['PDB', 'ihm_2dem_class_average_restraint_primary_key']],
    ),
    em.Key.define(
        ['RID'], constraint_names=[['PDB', 'ihm_2dem_class_average_restraint_RIDkey1']],
    ),
]

fkey_defs = [
    em.ForeignKey.define(
        ['RCB'],
        'public',
        'ERMrest_Client', ['ID'],
        constraint_names=[['PDB', 'ihm_2dem_class_average_restraint_RCB_fkey']],
    ),
    em.ForeignKey.define(
        ['RMB'],
        'public',
        'ERMrest_Client', ['ID'],
        constraint_names=[['PDB', 'ihm_2dem_class_average_restraint_RMB_fkey']],
    ),
    em.ForeignKey.define(
        ['structure_id'],
        'PDB',
        'entry', ['id'],
        constraint_names=[['PDB', 'ihm_2dem_class_average_restraint_structure_id_fkey']],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
        on_update='CASCADE',
        on_delete='CASCADE',
    ),
    em.ForeignKey.define(
        ['image_segment_flag'],
        'Vocab',
        'ihm_2dem_class_average_restraint_image_segment_flag', ['Name'],
        constraint_names=[['PDB', 'ihm_2dem_class_average_restraint_image_segment_flag_fkey']],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
    ),
    em.ForeignKey.define(
        ['Owner'],
        'public',
        'Catalog_Group', ['ID'],
        constraint_names=[['PDB', 'ihm_2dem_class_average_restraint_Owner_fkey']],
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
        ['structure_id', 'struct_assembly_id'],
        'PDB',
        'ihm_struct_assembly', ['structure_id', 'id'],
        constraint_names=[['PDB', 'ihm_2dem_class_average_restraint_struct_assembly_id_fkey']],
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
        ['dataset_list_id', 'structure_id'],
        'PDB',
        'ihm_dataset_list', ['id', 'structure_id'],
        constraint_names=[['PDB', 'ihm_2dem_class_average_restraint_dataset_list_id_fkey']],
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
