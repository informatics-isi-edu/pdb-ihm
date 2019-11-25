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

schema_name = 'Vocab'

table_names = [
    'chem_comp_mon_nstd_flag_term', 'chem_comp_type_term', 'chem_comp_atom_pdbx_aromatic_flag_term',
    'chem_comp_atom_pdbx_leaving_atom_flag_term', 'chem_comp_atom_pdbx_polymer_type_term',
    'chem_comp_atom_pdbx_stereo_config_term', 'chem_comp_atom_substruct_code_term',
    'entity_src_method_term', 'entity_type_term', 'entity_poly_nstd_chirality_term',
    'entity_poly_nstd_linkage_term', 'entity_poly_nstd_monomer_term',
    'entity_poly_pdbx_sequence_evidence_code_term', 'entity_poly_type_term',
    'entity_poly_seq_hetero_term', 'entity_src_gen_pdbx_alt_source_flag_term',
    'em_class_average_restraint_image_segment_flag_term',
    'ihm_3dem_restraint_map_segment_flag_term', 'ihm_cross_link_list_linker_type_term',
    'oss_link_restraint_conditional_crosslink_flag_term',
    'ihm_cross_link_restraint_model_granularity_term',
    'ihm_cross_link_restraint_restraint_type_term', 'ihm_dataset_group_application_term',
    'ihm_dataset_list_data_type_term', 'ihm_dataset_list_database_hosted_term',
    'ihm_dataset_related_db_reference_db_name_term',
    'rived_distance_restraint_group_conditionality_term',
    'ihm_derived_distance_restraint_restraint_type_term',
    'ihm_ensemble_info_ensemble_clustering_feature_term',
    'ihm_ensemble_info_ensemble_clustering_method_term', 'ihm_epr_restraint_fitting_state_term',
    'ihm_external_files_content_type_term', 'ihm_external_files_file_format_term',
    'ihm_external_reference_info_reference_type_term', 'ihm_external_reference_info_refers_to_term',
    'ihm_feature_list_entity_type_term', 'ihm_feature_list_feature_type_term',
    'ihm_geometric_object_axis_axis_type_term',
    'bject_distance_restraint_group_conditionality_term',
    'ject_distance_restraint_object_characteristic_term',
    'tric_object_distance_restraint_restraint_type_term',
    'ihm_geometric_object_half_torus_section_term', 'ihm_geometric_object_list_object_type_term',
    'ihm_geometric_object_plane_plane_type_term',
    'odel_representation_details_model_granularity_term',
    'ihm_model_representation_details_model_mode_term',
    'representation_details_model_object_primitive_term',
    'ihm_model_representative_selection_criteria_term', 'ihm_modeling_post_process_feature_term',
    'ihm_modeling_post_process_type_term', 'ihm_modeling_protocol_details_ensemble_flag_term',
    'hm_modeling_protocol_details_multi_scale_flag_term',
    'hm_modeling_protocol_details_multi_state_flag_term',
    'ihm_modeling_protocol_details_ordered_flag_term',
    'ihm_multi_state_modeling_experiment_type_term',
    '_probe_conjugate_ambiguous_stoichiometry_flag_term',
    'ihm_poly_probe_position_modification_flag_term', 'ihm_poly_probe_position_mutation_flag_term',
    'm_poly_residue_feature_interface_residue_flag_term', 'ihm_poly_residue_feature_rep_atom_term',
    'oly_residue_feature_residue_range_granularity_term',
    'predicted_contact_restraint_model_granularity_term',
    'ihm_predicted_contact_restraint_rep_atom_1_term',
    'ihm_predicted_contact_restraint_rep_atom_2_term',
    'hm_predicted_contact_restraint_restraint_type_term', 'ihm_probe_list_probe_link_type_term',
    'ihm_probe_list_probe_origin_term', 'ihm_probe_list_reactive_probe_flag_term',
    'ihm_residues_not_modeled_reason_term', 'ihm_sas_restraint_fitting_state_term',
    'ihm_sas_restraint_profile_segment_flag_term',
    'models_template_sequence_identity_denominator_term',
    '_starting_model_details_starting_model_source_term', 'ihm_struct_assembly_class_type_term',
    'pdbx_entity_poly_na_type_type_term', 'software_type_term', 'struct_pdbx_CASP_flag_term',
    'struct_asym_pdbx_blank_PDB_chainid_flag_term', 'struct_asym_pdbx_type_term',
]

annotations = {chaise_tags.display: {'name_style': {'title_case': False, 'underline_space': True}}}

acls = {}

comment = None

schema_def = em.Schema.define('Vocab', comment=comment, acls=acls, annotations=annotations, )


def main(catalog, mode, replace=False):
    updater = CatalogUpdater(catalog)
    updater.update_schema(mode, schema_def, replace=replace)


if __name__ == "__main__":
    host = 'pdb.isrd.isi.edu'
    catalog_id = 1
    mode, replace, host, catalog_id = parse_args(host, catalog_id, is_catalog=True)
    catalog = DerivaCatalog(host, catalog_id=catalog_id, validate=False)
    main(catalog, mode, replace)
