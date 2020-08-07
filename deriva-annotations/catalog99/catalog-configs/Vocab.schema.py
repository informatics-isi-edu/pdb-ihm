import argparse
from deriva.core import ErmrestCatalog, AttrDict, get_credential
import deriva.core.ermrest_model as em
from deriva.core.ermrest_config import tag as chaise_tags
from deriva.utils.catalog.manage.update_catalog import CatalogUpdater, parse_args

groups = {}

schema_name = 'Vocab'

table_names = [
    'ihm_geometric_object_plane_plane_type', 'chem_comp_atom_pdbx_leaving_atom_flag',
    'entity_poly_nstd_monomer', 'ihm_derived_distance_restraint_group_conditionality',
    'ihm_sas_restraint_profile_segment_flag', 'ihm_probe_list_probe_link_type',
    'ihm_dataset_related_db_reference_db_name', 'chem_comp_mon_nstd_flag',
    'ihm_feature_list_entity_type', 'entity_poly_nstd_linkage',
    'ihm_cross_link_restraint_restraint_type', 'ihm_sas_restraint_fitting_state',
    'ihm_predicted_contact_restraint_rep_atom_2', 'entity_type',
    'ihm_predicted_contact_restraint_model_granularity', 'File_Format',
    'ihm_probe_list_probe_origin', 'ihm_poly_residue_feature_rep_atom',
    'geometric_object_distance_restraint_object_character',
    'ihm_ensemble_info_ensemble_clustering_feature', 'ihm_cross_link_list_linker_type',
    'ihm_modeling_protocol_details_multi_state_flag', 'ihm_epr_restraint_fitting_state',
    'ihm_cross_link_restraint_model_granularity', 'ihm_3dem_restraint_map_segment_flag',
    'entity_poly_nstd_chirality', 'geometric_object_distance_restraint_group_condition',
    'chem_comp_type', 'ihm_external_files_content_type', 'ihm_modeling_post_process_feature',
    'chem_comp_atom_pdbx_polymer_type', 'ihm_modeling_protocol_details_ensemble_flag',
    'entity_poly_pdbx_sequence_evidence_code', 'chem_comp_atom_substruct_code',
    'ihm_poly_probe_conjugate_ambiguous_stoichiometry_flag', 'struct_asym_pdbx_type',
    'ihm_derived_distance_restraint_restraint_type', 'ihm_geometric_object_list_object_type',
    'ihm_residues_not_modeled_reason', 'ihm_model_representation_details_model_granularity',
    'ihm_modeling_protocol_details_multi_scale_flag',
    'ihm_predicted_contact_restraint_restraint_type', 'File_Type',
    'ihm_model_representation_details_model_mode', 'ihm_poly_probe_position_mutation_flag',
    'ihm_modeling_post_process_type', 'ihm_starting_model_details_starting_model_source',
    'ihm_poly_residue_feature_residue_range_granularity',
    'ihm_external_reference_info_reference_type', 'workflow_status', 'ihm_dataset_list_data_type',
    'ihm_probe_list_reactive_probe_flag', 'ihm_feature_list_feature_type',
    'ihm_cross_link_restraint_conditional_crosslink_flag', 'ihm_external_files_file_format',
    'ihm_geometric_object_axis_axis_type', 'ihm_external_reference_info_refers_to',
    'struct_asym_pdbx_blank_PDB_chainid_flag', 'chem_comp_atom_pdbx_aromatic_flag',
    'ihm_modeling_protocol_details_ordered_flag', 'entity_src_gen_pdbx_alt_source_flag',
    'ihm_poly_residue_feature_interface_residue_flag',
    'ihm_2dem_class_average_restraint_image_segment_flag',
    'ihm_ensemble_info_ensemble_clustering_method',
    'starting_comparative_models_template_sequence_id_denom', 'struct_pdbx_CASP_flag',
    'software_type', 'ihm_multi_state_modeling_experiment_type',
    'ihm_geometric_object_half_torus_section', 'chem_comp_atom_pdbx_stereo_config',
    'ihm_geometric_object_distance_restraint_restraint_type',
    'ihm_poly_probe_position_modification_flag', 'entity_poly_type',
    'ihm_model_representative_selection_criteria', 'ihm_struct_assembly_class_type',
    'ihm_dataset_list_database_hosted', 'model_representation_details_model_object_primitive',
    'pdbx_entity_poly_na_type_type', 'ihm_predicted_contact_restraint_rep_atom_1',
    'entity_src_method', 'ihm_dataset_group_application', 'entity_poly_seq_hetero',
    'process_status',
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
    catalog_id = 99
    mode, replace, host, catalog_id = parse_args(host, catalog_id)
    catalog = ErmrestCatalog('https', host, catalog_id=catalog_id, credentials=get_credential(host))
    main(catalog, mode, replace)
