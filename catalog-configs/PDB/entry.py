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

table_name = 'entry'

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
    'id': {},
    'Owner': {}
}

column_comment = {
    'structure_id': 'type:text\nThe value of _entry.id identifies the data block.\n\n Note that this item need not be a number; it can be any unique\n identifier.',
    'id': 'type:text\nThe value of _entry.id identifies the data block.\n\n Note that this item need not be a number; it can be any unique\n identifier.',
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
    em.Column.define('id', em.builtin_types['text'], nullok=False, comment=column_comment['id'],
                     ),
    em.Column.define('Owner', em.builtin_types['text'], comment=column_comment['Owner'],
                     ),
]

visible_columns = {
    '*': [
        'RID',
        {
            'source': [{
                'outbound': ['PDB', 'entry_structure_id_fkey']
            }, 'RID'],
            'comment': 'type:text\nThe value of _entry.id identifies the data block.\n\n Note that this item need not be a number; it can be any unique\n identifier.',
            'markdown_name': 'structure id'
        }, 'id', ['PDB', 'entry_RCB_fkey'], ['PDB', 'entry_RMB_fkey'], 'RCT', 'RMT',
        ['PDB', 'entry_Owner_fkey']
    ],
    'entry': [
        {
            'source': [{
                'outbound': ['PDB', 'entry_structure_id_fkey']
            }, 'RID'],
            'comment': 'type:text\nThe value of _entry.id identifies the data block.\n\n Note that this item need not be a number; it can be any unique\n identifier.',
            'markdown_name': 'structure id'
        }, 'id'
    ]
}

visible_foreign_keys = {
    'filter': 'detailed',
    'detailed': [
        ['PDB', 'entry_structure_id_fkey'], ['PDB', 'struct_structure_id_fkey'],
        ['PDB', 'struct_entry_id_fkey'], ['PDB', 'audit_conform_structure_id_fkey'],
        ['PDB', 'citation_structure_id_fkey'], ['PDB', 'citation_author_structure_id_fkey'],
        ['PDB', 'audit_author_structure_id_fkey'], ['PDB', 'software_structure_id_fkey'],
        ['PDB', 'entity_structure_id_fkey'], ['PDB', 'entity_poly_structure_id_fkey'],
        ['PDB', 'pdbx_entity_nonpoly_structure_id_fkey'],
        ['PDB', 'entity_poly_seq_structure_id_fkey'], ['PDB', 'struct_asym_structure_id_fkey'],
        ['PDB', 'chem_comp_structure_id_fkey'], ['PDB', 'pdbx_poly_seq_scheme_structure_id_fkey'],
        ['PDB', 'pdbx_seq_map_depositor_info_structure_id_fkey'],
        ['PDB', 'ihm_entity_poly_segment_structure_id_fkey'],
        ['PDB', 'ihm_model_representation_structure_id_fkey'],
        ['PDB', 'ihm_model_representation_details_structure_id_fkey'],
        ['PDB', 'ihm_struct_assembly_structure_id_fkey'],
        ['PDB', 'ihm_struct_assembly_details_structure_id_fkey'],
        ['PDB', 'ihm_struct_assembly_class_structure_id_fkey'],
        ['PDB', 'ihm_struct_assembly_class_link_structure_id_fkey'],
        ['PDB', 'ihm_modeling_protocol_structure_id_fkey'],
        ['PDB', 'ihm_modeling_protocol_details_structure_id_fkey'],
        ['PDB', 'ihm_modeling_post_process_structure_id_fkey'],
        ['PDB',
         'ihm_dataset_list_structure_id_fkey'], ['PDB', 'ihm_dataset_group_structure_id_fkey'],
        ['PDB', 'ihm_dataset_group_link_structure_id_fkey'],
        ['PDB', 'ihm_dataset_related_db_reference_structure_id_fkey'],
        ['PDB', 'ihm_external_reference_info_structure_id_fkey'],
        ['PDB', 'ihm_external_files_structure_id_fkey'],
        ['PDB', 'ihm_dataset_external_reference_structure_id_fkey'],
        ['PDB', 'ihm_related_datasets_structure_id_fkey'],
        ['PDB', 'ihm_starting_model_details_structure_id_fkey'],
        ['PDB', 'ihm_starting_computational_models_structure_id_fkey'],
        ['PDB', 'ihm_starting_comparative_models_structure_id_fkey'],
        ['PDB', 'ihm_starting_model_seq_dif_structure_id_fkey'],
        ['PDB', 'ihm_cross_link_list_structure_id_fkey'],
        ['PDB', 'ihm_cross_link_restraint_structure_id_fkey'],
        ['PDB', 'ihm_cross_link_result_structure_id_fkey'],
        ['PDB', 'ihm_cross_link_result_parameters_structure_id_fkey'],
        ['PDB', 'ihm_2dem_class_average_restraint_structure_id_fkey'],
        ['PDB', 'ihm_2dem_class_average_fitting_structure_id_fkey'],
        ['PDB', 'ihm_3dem_restraint_structure_id_fkey'],
        ['PDB', 'ihm_sas_restraint_structure_id_fkey'],
        ['PDB', 'ihm_predicted_contact_restraint_structure_id_fkey'],
        ['PDB', 'ihm_hydroxyl_radical_fp_restraint_structure_id_fkey'],
        ['PDB', 'ihm_feature_list_structure_id_fkey'],
        ['PDB', 'ihm_pseudo_site_feature_structure_id_fkey'],
        ['PDB', 'ihm_poly_atom_feature_structure_id_fkey'],
        ['PDB', 'ihm_poly_residue_feature_structure_id_fkey'],
        ['PDB', 'ihm_non_poly_feature_structure_id_fkey'],
        ['PDB', 'ihm_interface_residue_feature_structure_id_fkey'],
        ['PDB', 'ihm_derived_distance_restraint_structure_id_fkey'],
        ['PDB', 'ihm_geometric_object_list_structure_id_fkey'],
        ['PDB', 'ihm_geometric_object_center_structure_id_fkey'],
        ['PDB', 'ihm_geometric_object_transformation_structure_id_fkey'],
        ['PDB', 'ihm_geometric_object_sphere_structure_id_fkey'],
        ['PDB', 'ihm_geometric_object_torus_structure_id_fkey'],
        ['PDB', 'ihm_geometric_object_half_torus_structure_id_fkey'],
        ['PDB', 'ihm_geometric_object_axis_structure_id_fkey'],
        ['PDB', 'ihm_geometric_object_plane_structure_id_fkey'],
        ['PDB', 'ihm_geometric_object_distance_restraint_structure_id_fkey'],
        ['PDB', 'ihm_model_list_structure_id_fkey'], ['PDB', 'ihm_model_group_structure_id_fkey'],
        ['PDB', 'ihm_model_group_link_structure_id_fkey'],
        ['PDB', 'ihm_model_representative_structure_id_fkey'],
        ['PDB', 'ihm_residues_not_modeled_structure_id_fkey'],
        ['PDB', 'atom_site_structure_id_fkey'], ['PDB', 'ihm_sphere_obj_site_structure_id_fkey'],
        ['PDB', 'ihm_gaussian_obj_site_structure_id_fkey'],
        ['PDB', 'ihm_starting_model_coord_structure_id_fkey'],
        ['PDB', 'ihm_multi_state_modeling_structure_id_fkey'],
        ['PDB', 'ihm_multi_state_model_group_link_structure_id_fkey'],
        ['PDB', 'ihm_ordered_ensemble_structure_id_fkey'],
        ['PDB', 'ihm_ensemble_info_structure_id_fkey'],
        ['PDB', 'ihm_localization_density_files_structure_id_fkey'],
        ['PDB', 'ihm_gaussian_obj_ensemble_structure_id_fkey']
    ]
}

table_display = {'row_name': {'row_markdown_pattern': '{{{id}}}'}}

table_annotations = {
    chaise_tags.table_display: table_display,
    chaise_tags.visible_columns: visible_columns,
    chaise_tags.visible_foreign_keys: visible_foreign_keys,
}

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
    em.Key.define(['RID'], constraint_names=[('PDB', 'entry_RIDkey1')],
                  ),
    em.Key.define(['structure_id', 'id'], constraint_names=[('PDB', 'entry_primary_key')],
                  ),
    em.Key.define(['id'], constraint_names=[('PDB', 'entry_id_unique_key')],
                  ),
]

fkey_defs = [
    em.ForeignKey.define(
        ['Owner'],
        'public',
        'Catalog_Group', ['ID'],
        constraint_names=[('PDB', 'entry_Owner_fkey')],
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
        constraint_names=[('PDB', 'entry_RCB_fkey')],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
    ),
    em.ForeignKey.define(
        ['RMB'],
        'public',
        'ERMrest_Client', ['ID'],
        constraint_names=[('PDB', 'entry_RMB_fkey')],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
    ),
    em.ForeignKey.define(
        ['structure_id'],
        'PDB',
        'entry', ['id'],
        constraint_names=[('PDB', 'entry_structure_id_fkey')],
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

