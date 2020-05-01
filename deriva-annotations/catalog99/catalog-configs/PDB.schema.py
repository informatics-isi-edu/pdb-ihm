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
    'isrd-staff': 'https://auth.globus.org/176baec4-ed26-11e5-8e88-22000ab4b42b'
}

schema_name = 'PDB'

table_names = [
    'ihm_localization_density_files', 'ihm_model_representative', 'chem_comp_atom',
    'entity_poly_seq', 'chem_comp', 'citation_author', 'ihm_chemical_component_descriptor',
    'pdbx_inhibitor_info', 'ihm_dataset_external_reference', 'ihm_struct_assembly_details',
    'entity_src_gen', 'entity_name_com', 'ihm_cross_link_list', 'ihm_probe_list', 'struct_asym',
    'ihm_multi_state_model_group_link', 'ihm_epr_restraint', 'ihm_2dem_class_average_fitting',
    'software', 'ihm_poly_probe_conjugate', 'ihm_model_representation', 'ihm_model_list',
    'ihm_feature_list', 'pdbx_entity_poly_na_type', 'ihm_ordered_ensemble',
    'ihm_geometric_object_list', 'pdbx_ion_info', 'Entry_Related_File',
    'ihm_geometric_object_sphere', 'ihm_poly_residue_feature', 'audit_conform',
    'pdbx_entry_details', 'ihm_related_datasets', 'ihm_model_group', 'ihm_struct_assembly',
    'ihm_multi_state_modeling', 'ihm_dataset_group', 'entry', 'atom_type',
    'ihm_interface_residue_feature', 'ihm_dataset_list', 'audit_author', 'entity',
    'ihm_geometric_object_plane', 'ihm_predicted_contact_restraint', 'ihm_3dem_restraint',
    'ihm_derived_distance_restraint', 'ihm_cross_link_restraint', 'ihm_model_group_link',
    'citation', 'ihm_poly_atom_feature', 'ihm_model_representation_details', 'ihm_sas_restraint',
    'ihm_entity_poly_segment', 'ihm_hydroxyl_radical_fp_restraint', 'ihm_starting_model_seq_dif',
    'ihm_geometric_object_distance_restraint', 'ihm_external_files', 'ihm_external_reference_info',
    'ihm_modeling_post_process', 'ihm_2dem_class_average_restraint', 'ihm_cross_link_result',
    'ihm_starting_computational_models', 'ihm_residues_not_modeled', 'ihm_struct_assembly_class',
    'ihm_dataset_related_db_reference', 'ihm_geometric_object_axis', 'entity_poly',
    'entity_name_sys', 'ihm_non_poly_feature', 'ihm_geometric_object_half_torus',
    'pdbx_protein_info', 'ihm_geometric_object_torus', 'ihm_pseudo_site_feature',
    'pdbx_entity_nonpoly', 'ihm_cross_link_result_parameters', 'struct', 'ihm_modeling_protocol',
    'ihm_struct_assembly_class_link', 'ihm_geometric_object_center', 'ihm_ensemble_info',
    'ihm_poly_probe_position', 'ihm_starting_comparative_models', 'ihm_modeling_protocol_details',
    'ihm_ligand_probe', 'ihm_geometric_object_transformation', 'ihm_dataset_group_link',
    'ihm_starting_model_details',
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
    catalog_id = 99
    mode, replace, host, catalog_id = parse_args(host, catalog_id)
    catalog = ErmrestCatalog('https', host, catalog_id=catalog_id, credentials=get_credential(host))
    main(catalog, mode, replace)
