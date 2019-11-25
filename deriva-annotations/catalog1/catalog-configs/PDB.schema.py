import argparse
from deriva.core import ErmrestCatalog, AttrDict, get_credential, DerivaPathError
from deriva.utils.catalog.components.deriva_model import DerivaCatalog
import deriva.core.ermrest_model as em
from deriva.core.ermrest_config import tag as chaise_tags
from deriva.utils.catalog.manage.update_catalog import CatalogUpdater, parse_args

groups = {
    'pdb-reader': 'https://auth.globus.org/8875a770-3c40-11e9-a8c8-0ee7d80087ee',
    'pdb-writer': 'https://auth.globus.org/c94a1e5c-3c40-11e9-a5d1-0aacc65bfe9a',
    'pdb-admin': 'https://auth.globus.org/0b98092c-3c41-11e9-a8c8-0ee7d80087ee',
    'pdb-curator': 'https://auth.globus.org/eef3e02a-3c40-11e9-9276-0edc9bdd56a6',
    'isrd-staff': 'https://auth.globus.org/176baec4-ed26-11e5-8e88-22000ab4b42b'
}

schema_name = 'PDB'

table_names = [
    'ihm_non_poly_feature', 'ihm_ordered_ensemble', 'ihm_poly_atom_feature',
    'ihm_poly_probe_conjugate', 'ihm_poly_probe_position', 'ihm_poly_residue_feature',
    'ihm_predicted_contact_restraint', 'ihm_probe_list', 'ihm_pseudo_site_feature',
    'ihm_related_datasets', 'ihm_residues_not_modeled', 'ihm_sas_restraint',
    'ihm_starting_comparative_models', 'ihm_starting_computational_models',
    'ihm_struct_assembly_class_link', 'ihm_struct_assembly_details', 'pdbx_entity_nonpoly',
    'pdbx_entity_poly_na_type', 'pdbx_entry_details', 'pdbx_inhibitor_info', 'pdbx_ion_info',
    'ihm_starting_model_seq_dif', 'audit_author', 'audit_conform', 'chem_comp_atom',
    'citation_author', 'entity_name_com', 'entity_name_sys', 'entity_poly_seq', 'entity_src_gen',
    'ihm_2dem_class_average_fitting', 'ihm_3dem_restraint', 'ihm_chemical_component_descriptor',
    'ihm_cross_link_result', 'ihm_cross_link_result_parameters', 'ihm_dataset_external_reference',
    'ihm_dataset_group_link', 'ihm_dataset_related_db_reference', 'ihm_derived_distance_restraint',
    'ihm_epr_restraint', 'ihm_geometric_object_axis', 'ihm_geometric_object_distance_restraint',
    'ihm_geometric_object_half_torus', 'ihm_geometric_object_plane', 'ihm_geometric_object_sphere',
    'ihm_hydroxyl_radical_fp_restraint', 'ihm_interface_residue_feature', 'ihm_ligand_probe',
    'ihm_localization_density_files', 'ihm_model_group_link', 'ihm_model_representation_details',
    'ihm_model_representative', 'ihm_modeling_protocol_details', 'ihm_multi_state_model_group_link',
    'pdbx_protein_info', 'struct', 'entry', 'ihm_model_list', 'struct_asym', 'chem_comp', 'entity',
    'atom_type', 'citation', 'entity_poly', 'ihm_2dem_class_average_restraint', 'ihm_dataset_list',
    'ihm_struct_assembly', 'ihm_cross_link_list', 'ihm_ensemble_info', 'ihm_cross_link_restraint',
    'ihm_external_files', 'ihm_dataset_group', 'ihm_feature_list', 'ihm_model_group',
    'ihm_modeling_post_process', 'ihm_external_reference_info', 'ihm_geometric_object_list',
    'ihm_geometric_object_transformation', 'ihm_geometric_object_torus',
    'ihm_geometric_object_center', 'software', 'ihm_entity_poly_segment', 'ihm_modeling_protocol',
    'ihm_model_representation', 'ihm_starting_model_details', 'ihm_multi_state_modeling',
    'ihm_struct_assembly_class',
]

annotations = {chaise_tags.display: {'name_style': {'title_case': True, 'underline_space': True}}}

acls = {}

comment = None

schema_def = em.Schema.define('PDB', comment=comment, acls=acls, annotations=annotations, )


def main(catalog, mode, replace=False):
    updater = CatalogUpdater(catalog)
    updater.update_schema(mode, schema_def, replace=replace)


if __name__ == "__main__":
    host = 'pdb.isrd.isi.edu'
    catalog_id = 1
    mode, replace, host, catalog_id = parse_args(host, catalog_id, is_catalog=True)
    catalog = DerivaCatalog(host, catalog_id=catalog_id, validate=False)
    main(catalog, mode, replace)
