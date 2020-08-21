import argparse
from deriva.core import ErmrestCatalog, AttrDict, get_credential
import deriva.core.ermrest_model as em
from deriva.core.ermrest_config import tag as chaise_tags
from deriva.utils.catalog.manage.update_catalog import CatalogUpdater, parse_args

groups = {}

table_name = 'ihm_3dem_restraint'

schema_name = 'PDB'

column_annotations = {
    'structure_id': {},
    'cross_correlation_coefficient': {},
    'dataset_list_id': {},
    'details': {},
    'fitting_method': {},
    'fitting_method_citation_id': {},
    'id': {},
    'map_segment_flag': {},
    'model_id': {},
    'number_of_gaussians': {},
    'struct_assembly_id': {},
    'Owner': {}
}

column_comment = {
    'structure_id': 'A reference to table entry.id.',
    'cross_correlation_coefficient': 'type:float4\nThe cross correlation coefficient corresponding to the model to map fitting.',
    'dataset_list_id': 'A reference to table ihm_dataset_list.id.',
    'details': 'type:text\nAdditional details regarding the model to map fitting.\nexamples:The Nup-84 models generated and the 3DEM maps are converted to 3D Gaussians\n        using Gaussian mixture models (GMMs). The GMMs are then compared to obtain\n        a 3D fit of the map and the model.',
    'fitting_method': 'type:text\nMethod used to fit the model to the 3DEM map.\nexamples:Gaussian mixture model,Local refinement,Flexible fitting,Other',
    'fitting_method_citation_id': 'A reference to table citation.id.',
    'id': 'type:int4\nA unique identifier for the 3DEM restraint description.',
    'map_segment_flag': 'type:text\nA flag that indicates whether or not the 3DEM map is segmented i.e.,\n whether the whole map is used or only a portion of it is used (by masking\n or by other means) as restraint in the modeling.',
    'model_id': 'A reference to table ihm_model_list.model_id.',
    'number_of_gaussians': 'type:int4\nIn case of Gaussian mixture models, the number of gaussians\n is a parameter used to covert the 3DEM maps and models into\n GMMs. This captures the level of granularity used in\n representing the maps and/or models as 3D Gaussians.',
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
        'cross_correlation_coefficient',
        em.builtin_types['float4'],
        comment=column_comment['cross_correlation_coefficient'],
    ),
    em.Column.define(
        'dataset_list_id',
        em.builtin_types['int4'],
        nullok=False,
        comment=column_comment['dataset_list_id'],
    ),
    em.Column.define('details', em.builtin_types['text'], comment=column_comment['details'],
                     ),
    em.Column.define(
        'fitting_method', em.builtin_types['text'], comment=column_comment['fitting_method'],
    ),
    em.Column.define(
        'fitting_method_citation_id',
        em.builtin_types['text'],
        comment=column_comment['fitting_method_citation_id'],
    ),
    em.Column.define('id', em.builtin_types['int4'], nullok=False, comment=column_comment['id'],
                     ),
    em.Column.define(
        'map_segment_flag', em.builtin_types['text'], comment=column_comment['map_segment_flag'],
    ),
    em.Column.define(
        'model_id', em.builtin_types['int4'], nullok=False, comment=column_comment['model_id'],
    ),
    em.Column.define(
        'number_of_gaussians',
        em.builtin_types['int4'],
        comment=column_comment['number_of_gaussians'],
    ),
    em.Column.define(
        'struct_assembly_id',
        em.builtin_types['int4'],
        nullok=False,
        comment=column_comment['struct_assembly_id'],
    ),
    em.Column.define('Owner', em.builtin_types['text'], comment=column_comment['Owner'],
                     ),
    em.Column.define('Fitting_method_citation_RID', em.builtin_types['text'],
                     ),
]

visible_columns = {
    '*': [
        'RID', {
            'source': [{
                'outbound': ['PDB', 'ihm_3dem_restraint_structure_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table entry.id.',
            'markdown_name': 'structure id'
        }, 'id', {
            'source': [{
                'outbound': ['PDB', 'ihm_3dem_restraint_model_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table ihm_model_list.model_id.',
            'markdown_name': 'model id'
        }, {
            'source': [{
                'outbound': ['PDB', 'ihm_3dem_restraint_struct_assembly_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table ihm_struct_assembly.id.',
            'markdown_name': 'struct assembly id'
        }, 'fitting_method', 'number_of_gaussians',
        ['PDB', 'ihm_3dem_restraint_map_segment_flag_fkey'], 'cross_correlation_coefficient', {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_3dem_restraint_fitting_method_citation_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table citation.id.',
            'markdown_name': 'fitting method citation id'
        }, 'details', {
            'source': [{
                'outbound': ['PDB', 'ihm_3dem_restraint_dataset_list_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table ihm_dataset_list.id.',
            'markdown_name': 'dataset list id'
        }
    ],
    'entry': [
        {
            'source': [{
                'outbound': ['PDB', 'ihm_3dem_restraint_structure_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table entry.id.',
            'markdown_name': 'structure id'
        }, 'id', {
            'source': [{
                'outbound': ['PDB', 'ihm_3dem_restraint_model_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table ihm_model_list.model_id.',
            'markdown_name': 'model id'
        }, {
            'source': [{
                'outbound': ['PDB', 'ihm_3dem_restraint_struct_assembly_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table ihm_struct_assembly.id.',
            'markdown_name': 'struct assembly id'
        }, 'fitting_method', 'number_of_gaussians',
        ['PDB', 'ihm_3dem_restraint_map_segment_flag_fkey'], 'cross_correlation_coefficient', {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_3dem_restraint_fitting_method_citation_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table citation.id.',
            'markdown_name': 'fitting method citation id'
        }, 'details', {
            'source': [{
                'outbound': ['PDB', 'ihm_3dem_restraint_dataset_list_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table ihm_dataset_list.id.',
            'markdown_name': 'dataset list id'
        }
    ],
    'detailed': [
        'RID', {
            'source': [{
                'outbound': ['PDB', 'ihm_3dem_restraint_structure_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table entry.id.',
            'markdown_name': 'structure id'
        }, 'id', {
            'source': [{
                'outbound': ['PDB', 'ihm_3dem_restraint_model_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table ihm_model_list.model_id.',
            'markdown_name': 'model id'
        }, {
            'source': [{
                'outbound': ['PDB', 'ihm_3dem_restraint_struct_assembly_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table ihm_struct_assembly.id.',
            'markdown_name': 'struct assembly id'
        }, 'fitting_method', 'number_of_gaussians',
        ['PDB', 'ihm_3dem_restraint_map_segment_flag_fkey'], 'cross_correlation_coefficient', {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_3dem_restraint_fitting_method_citation_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table citation.id.',
            'markdown_name': 'fitting method citation id'
        }, 'details', {
            'source': [{
                'outbound': ['PDB', 'ihm_3dem_restraint_dataset_list_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table ihm_dataset_list.id.',
            'markdown_name': 'dataset list id'
        }, ['PDB', 'ihm_3dem_restraint_RCB_fkey'], ['PDB', 'ihm_3dem_restraint_RMB_fkey'], 'RCT',
        'RMT', ['PDB', 'ihm_3dem_restraint_Owner_fkey']
    ]
}

table_annotations = {chaise_tags.visible_columns: visible_columns, }

table_comment = '3DEM maps used as restraints in the modeling'

table_acls = {}

table_acl_bindings = {}

key_defs = [
    em.Key.define(
        ['structure_id', 'id'], constraint_names=[['PDB', 'ihm_3dem_restraint_primary_key']],
    ),
    em.Key.define(['RID'], constraint_names=[['PDB', 'ihm_3dem_restraint_RIDkey1']],
                  ),
]

fkey_defs = [
    em.ForeignKey.define(
        ['map_segment_flag'],
        'Vocab',
        'ihm_3dem_restraint_map_segment_flag', ['Name'],
        constraint_names=[['PDB', 'ihm_3dem_restraint_map_segment_flag_fkey']],
    ),
    em.ForeignKey.define(
        ['structure_id', 'fitting_method_citation_id'],
        'PDB',
        'citation', ['structure_id', 'id'],
        constraint_names=[['PDB', 'ihm_3dem_restraint_fitting_method_citation_id_fk']],
        annotations={
            chaise_tags.foreign_key: {
                'domain_filter_pattern': 'structure_id={{structure_id}}'
            }
        },
        on_update='CASCADE',
        on_delete='SET NULL',
    ),
    em.ForeignKey.define(
        ['fitting_method_citation_id', 'Fitting_method_citation_RID'],
        'PDB',
        'citation', ['id', 'RID'],
        constraint_names=[['PDB', 'ihm_3dem_restraint_fitting_method_citation_id_fkey']],
        annotations={
            chaise_tags.foreign_key: {
                'domain_filter_pattern': 'structure_id={{structure_id}}'
            }
        },
        on_update='CASCADE',
        on_delete='SET NULL',
    ),
    em.ForeignKey.define(
        ['structure_id', 'struct_assembly_id'],
        'PDB',
        'ihm_struct_assembly', ['structure_id', 'id'],
        constraint_names=[['PDB', 'ihm_3dem_restraint_struct_assembly_id_fkey']],
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
        constraint_names=[['PDB', 'ihm_3dem_restraint_RCB_fkey']],
    ),
    em.ForeignKey.define(
        ['structure_id', 'model_id'],
        'PDB',
        'ihm_model_list', ['structure_id', 'model_id'],
        constraint_names=[['PDB', 'ihm_3dem_restraint_model_id_fkey']],
        annotations={
            chaise_tags.foreign_key: {
                'domain_filter_pattern': 'structure_id={{structure_id}}'
            }
        },
        on_update='CASCADE',
        on_delete='SET NULL',
    ),
    em.ForeignKey.define(
        ['structure_id', 'dataset_list_id'],
        'PDB',
        'ihm_dataset_list', ['structure_id', 'id'],
        constraint_names=[['PDB', 'ihm_3dem_restraint_dataset_list_id_fkey']],
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
        constraint_names=[['PDB', 'ihm_3dem_restraint_RMB_fkey']],
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
