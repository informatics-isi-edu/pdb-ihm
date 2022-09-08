import sys
import json
from deriva.core import ErmrestCatalog, AttrDict, get_credential, DEFAULT_CREDENTIAL_FILE, tag, urlquote, DerivaServer, get_credential, BaseCLI
from deriva.core.ermrest_model import builtin_types, Schema, Table, Column, Key, ForeignKey, DomainType, ArrayType
import utils
from utils import ApplicationClient

# ========================================================

# ============================================================

def main(server_name, catalog_id, credentials):
    server = DerivaServer('https', server_name, credentials)
    catalog = server.connect_ermrest(catalog_id)
    catalog.dcctx['cid'] = 'oneoff/model'
    model = catalog.getCatalogModel()

    utils.alter_on_delete_fkey_if_exist(model, 'PDB', 'struct_ref_seq', 'struct_ref_seq_struct_ref_combo1_fkey', 'CASCADE')
    utils.alter_on_delete_fkey_if_exist(model, 'PDB', 'struct_ref_seq_dif', 'struct_ref_seq_dif_struct_ref_seq_combo1_fkey', 'CASCADE')
    utils.alter_on_delete_fkey_if_exist(model, 'PDB', 'ihm_derived_angle_restraint', 'ihm_derived_angle_restraint_ihm_dataset_list_combo1_fkey', 'CASCADE')
    utils.alter_on_delete_fkey_if_exist(model, 'PDB', 'ihm_derived_dihedral_restraint', 'ihm_derived_dihedral_restraint_ihm_dataset_list_combo1_fkey', 'CASCADE')
    utils.alter_on_delete_fkey_if_exist(model, 'PDB', 'ihm_derived_distance_restraint', 'ihm_derived_distance_restraint_dataset_list_id_fkey', 'CASCADE')
    utils.alter_on_delete_fkey_if_exist(model, 'PDB', 'ihm_geometric_object_distance_restraint', 'ihm_geometric_object_distance_restraint_dataset_list_id_fkey', 'CASCADE')
    utils.alter_on_delete_fkey_if_exist(model, 'PDB', 'ihm_hdx_restraint', 'ihm_hdx_restraint_ihm_dataset_list_combo1_fkey', 'CASCADE')
    utils.alter_on_delete_fkey_if_exist(model, 'PDB', 'ihm_interface_residue_feature', 'ihm_interface_residue_feature_dataset_list_id_fkey', 'CASCADE')
    utils.alter_on_delete_fkey_if_exist(model, 'PDB', 'struct_ref', 'struct_ref_entity_combo1_fkey', 'CASCADE')
    utils.alter_on_delete_fkey_if_exist(model, 'PDB', 'ihm_starting_computational_models', 'ihm_starting_computational_models_software_id_fkey', 'CASCADE')
    utils.alter_on_delete_fkey_if_exist(model, 'PDB', 'citation_author', 'citation_author_citation_id_fkey', 'CASCADE')
    utils.alter_on_delete_fkey_if_exist(model, 'PDB', 'ihm_3dem_restraint', 'ihm_3dem_restraint_fitting_method_citation_id_fk', 'CASCADE')
    utils.alter_on_delete_fkey_if_exist(model, 'PDB', 'ihm_epr_restraint', 'ihm_epr_restraint_fitting_method_citation_id_fk', 'CASCADE')
    utils.alter_on_delete_fkey_if_exist(model, 'PDB', 'software', 'software_citation_id_fk', 'CASCADE')
    utils.alter_on_delete_fkey_if_exist(model, 'PDB', 'ihm_dataset_group_link', 'ihm_dataset_group_link_group_id_fkey', 'CASCADE')
    utils.alter_on_delete_fkey_if_exist(model, 'PDB', 'ihm_modeling_post_process', 'ihm_modeling_post_process_dataset_group_id_fk', 'CASCADE')
    utils.alter_on_delete_fkey_if_exist(model, 'PDB', 'ihm_modeling_protocol_details', 'ihm_modeling_protocol_details_dataset_group_id_fk', 'CASCADE')
    utils.alter_on_delete_fkey_if_exist(model, 'PDB', 'ihm_dataset_related_db_reference', 'ihm_dataset_related_db_reference_dataset_list_id_fkey', 'CASCADE')

    
    utils.alter_on_delete_fkey_if_exist(model, 'PDB', 'ihm_2dem_class_average_restraint', 'ihm_2dem_class_average_restraint_dataset_list_id_fkey', 'CASCADE')
    utils.alter_on_delete_fkey_if_exist(model, 'PDB', 'ihm_3dem_restraint', 'ihm_3dem_restraint_dataset_list_id_fkey', 'CASCADE')
    utils.alter_on_delete_fkey_if_exist(model, 'PDB', 'ihm_cross_link_list', 'ihm_cross_link_list_dataset_list_id_fkey', 'CASCADE')
    utils.alter_on_delete_fkey_if_exist(model, 'PDB', 'ihm_dataset_external_reference', 'ihm_dataset_external_reference_dataset_list_id_fkey', 'CASCADE')
    utils.alter_on_delete_fkey_if_exist(model, 'PDB', 'ihm_dataset_group_link', 'ihm_dataset_group_link_dataset_list_id_fkey', 'CASCADE')
    utils.alter_on_delete_fkey_if_exist(model, 'PDB', 'ihm_derived_distance_restraint', 'ihm_derived_distance_restraint_dataset_list_id_fk', 'CASCADE')
    utils.alter_on_delete_fkey_if_exist(model, 'PDB', 'ihm_epr_restraint', 'ihm_epr_restraint_dataset_list_id_fkey', 'CASCADE')
    utils.alter_on_delete_fkey_if_exist(model, 'PDB', 'ihm_hydroxyl_radical_fp_restraint', 'ihm_geometric_object_distance_restraint_dataset_list_id_fk', 'CASCADE')
    utils.alter_on_delete_fkey_if_exist(model, 'PDB', 'ihm_hydroxyl_radical_fp_restraint', 'ihm_hydroxyl_radical_fp_restraint_dataset_list_id_fkey', 'CASCADE')
    utils.alter_on_delete_fkey_if_exist(model, 'PDB', 'ihm_interface_residue_feature', 'ihm_interface_residue_feature_dataset_list_id_fk', 'CASCADE')
    utils.alter_on_delete_fkey_if_exist(model, 'PDB', 'ihm_ligand_probe', 'ihm_ligand_probe_dataset_list_id_fkey', 'CASCADE')
    utils.alter_on_delete_fkey_if_exist(model, 'PDB', 'ihm_poly_probe_conjugate', 'ihm_poly_probe_conjugate_dataset_list_id_fkey', 'CASCADE')
    utils.alter_on_delete_fkey_if_exist(model, 'PDB', 'ihm_predicted_contact_restraint', 'ihm_predicted_contact_restraint_dataset_list_id_fkey', 'CASCADE')
    utils.alter_on_delete_fkey_if_exist(model, 'PDB', 'ihm_related_datasets', 'ihm_related_datasets_dataset_list_id_derived_fkey', 'CASCADE')
    utils.alter_on_delete_fkey_if_exist(model, 'PDB', 'ihm_related_datasets', 'ihm_related_datasets_dataset_list_id_primary_fkey', 'CASCADE')
    utils.alter_on_delete_fkey_if_exist(model, 'PDB', 'ihm_sas_restraint', 'ihm_sas_restraint_dataset_list_id_fkey', 'CASCADE')
    utils.alter_on_delete_fkey_if_exist(model, 'PDB', 'ihm_starting_comparative_models', 'ihm_starting_comparative_models_template_dataset_list_id_fkey', 'CASCADE')
    utils.alter_on_delete_fkey_if_exist(model, 'PDB', 'ihm_starting_model_details', 'ihm_starting_model_details_dataset_list_id_fkey', 'CASCADE')
    
    utils.alter_on_delete_fkey_if_exist(model, 'PDB', 'ihm_model_representation_details', 'ihm_model_representation_details_entity_asym_id_fkey', 'CASCADE')
    utils.alter_on_delete_fkey_if_exist(model, 'PDB', 'ihm_model_representation_details', 'ihm_model_representation_details_entity_id_fkey', 'CASCADE')
    utils.alter_on_delete_fkey_if_exist(model, 'PDB', 'ihm_model_representation_details', 'ihm_model_representation_details_entity_poly_segment_id_fk', 'CASCADE')
    utils.alter_on_delete_fkey_if_exist(model, 'PDB', 'ihm_model_representation_details', 'ihm_model_representation_details_entity_poly_segment_id_fkey', 'CASCADE')
    utils.alter_on_delete_fkey_if_exist(model, 'PDB', 'ihm_model_representation_details', 'ihm_model_representation_details_representation_id_fkey', 'CASCADE')
    utils.alter_on_delete_fkey_if_exist(model, 'PDB', 'ihm_model_representation_details', 'ihm_model_representation_details_starting_model_id_fk', 'CASCADE')
    utils.alter_on_delete_fkey_if_exist(model, 'PDB', 'ihm_model_representation_details', 'ihm_model_representation_details_starting_model_id_fkey', 'CASCADE')

    utils.alter_on_delete_fkey_if_exist(model, 'PDB', 'ihm_2dem_class_average_fitting', 'ihm_2dem_class_average_fitting_model_id_fkey', 'CASCADE')
    utils.alter_on_delete_fkey_if_exist(model, 'PDB', 'ihm_3dem_restraint', 'ihm_3dem_restraint_model_id_fkey', 'CASCADE')
    utils.alter_on_delete_fkey_if_exist(model, 'PDB', 'ihm_cross_link_pseudo_site', 'ihm_cross_link_pseudo_site_ihm_model_list_combo2_fkey', 'CASCADE')
    utils.alter_on_delete_fkey_if_exist(model, 'PDB', 'ihm_cross_link_result_parameters', 'ihm_cross_link_result_parameters_model_id_fkey', 'CASCADE')
    utils.alter_on_delete_fkey_if_exist(model, 'PDB', 'ihm_epr_restraint', 'ihm_epr_restraint_model_id_fkey', 'CASCADE')
    utils.alter_on_delete_fkey_if_exist(model, 'PDB', 'ihm_model_representative', 'ihm_model_representative_model_id_fkey', 'CASCADE')
    utils.alter_on_delete_fkey_if_exist(model, 'PDB', 'ihm_residues_not_modeled', 'ihm_residues_not_modeled_model_id_fkey', 'CASCADE')
    utils.alter_on_delete_fkey_if_exist(model, 'PDB', 'ihm_sas_restraint', 'ihm_sas_restraint_model_id_fkey', 'CASCADE')
    utils.alter_on_delete_fkey_if_exist(model, 'PDB', 'ihm_model_group_link', 'ihm_model_group_link_group_id_fkey', 'CASCADE')
    utils.alter_on_delete_fkey_if_exist(model, 'PDB', 'ihm_model_group_link', 'ihm_model_group_link_model_id_fkey', 'CASCADE')
    utils.alter_on_delete_fkey_if_exist(model, 'PDB', 'ihm_model_group_link', 'ihm_model_group_link_structure_id_fkey', 'CASCADE')
    
    utils.alter_on_delete_fkey_if_exist(model, 'PDB', 'ihm_cross_link_list', 'ihm_cross_link_list_mm_poly_res_label_1_fkey', 'CASCADE')
    utils.alter_on_delete_fkey_if_exist(model, 'PDB', 'ihm_cross_link_list', 'ihm_cross_link_list_mm_poly_res_label_2_fkey', 'CASCADE')
    utils.alter_on_delete_fkey_if_exist(model, 'PDB', 'ihm_cross_link_restraint', 'ihm_cross_link_restraint_mm_poly_res_label_1_fkey', 'CASCADE')
    utils.alter_on_delete_fkey_if_exist(model, 'PDB', 'ihm_cross_link_restraint', 'ihm_cross_link_restraint_mm_poly_res_label_2_fkey', 'CASCADE')
    utils.alter_on_delete_fkey_if_exist(model, 'PDB', 'ihm_entity_poly_segment', 'ihm_entity_poly_segment_mm_poly_res_label_begin_fkey', 'CASCADE')
    utils.alter_on_delete_fkey_if_exist(model, 'PDB', 'ihm_entity_poly_segment', 'ihm_entity_poly_segment_mm_poly_res_label_end_fkey', 'CASCADE')
    utils.alter_on_delete_fkey_if_exist(model, 'PDB', 'ihm_hydroxyl_radical_fp_restraint', 'ihm_hydroxyl_radical_fp_restraint_mm_poly_res_label_fkey', 'CASCADE')
    utils.alter_on_delete_fkey_if_exist(model, 'PDB', 'ihm_poly_atom_feature', 'ihm_poly_atom_feature_mm_poly_res_label_fkey', 'CASCADE')
    utils.alter_on_delete_fkey_if_exist(model, 'PDB', 'ihm_poly_probe_position', 'ihm_poly_probe_position_mm_poly_res_label_fkey', 'CASCADE')
    utils.alter_on_delete_fkey_if_exist(model, 'PDB', 'ihm_poly_residue_feature', 'ihm_poly_residue_feature_mm_poly_res_label_begin_fkey', 'CASCADE')
    utils.alter_on_delete_fkey_if_exist(model, 'PDB', 'ihm_poly_residue_feature', 'ihm_poly_residue_feature_mm_poly_res_label_end_fkey', 'CASCADE')
    utils.alter_on_delete_fkey_if_exist(model, 'PDB', 'ihm_predicted_contact_restraint', 'ihm_predicted_contact_restraint_mm_poly_res_label_1_fkey', 'CASCADE')
    utils.alter_on_delete_fkey_if_exist(model, 'PDB', 'ihm_predicted_contact_restraint', 'ihm_predicted_contact_restraint_mm_poly_res_label_2_fkey', 'CASCADE')
    utils.alter_on_delete_fkey_if_exist(model, 'PDB', 'ihm_residues_not_modeled', 'ihm_residues_not_modeled_mm_poly_res_label_begin_fkey', 'CASCADE')
    utils.alter_on_delete_fkey_if_exist(model, 'PDB', 'ihm_residues_not_modeled', 'ihm_residues_not_modeled_mm_poly_res_label_end_fkey', 'CASCADE')
    utils.alter_on_delete_fkey_if_exist(model, 'PDB', 'ihm_starting_model_seq_dif', 'ihm_starting_model_seq_dif_mm_poly_res_label_fkey', 'CASCADE')
    utils.alter_on_delete_fkey_if_exist(model, 'PDB', 'ihm_entity_poly_segment', 'ihm_entity_poly_segment_structure_id_fkey', 'CASCADE')

    utils.alter_on_delete_fkey_if_exist(model, 'PDB', 'ihm_localization_density_files', 'ihm_localization_density_files_entity_poly_segment_id_fk', 'CASCADE')
    utils.alter_on_delete_fkey_if_exist(model, 'PDB', 'ihm_localization_density_files', 'ihm_localization_density_files_entity_poly_segment_id_fkey', 'CASCADE')
    utils.alter_on_delete_fkey_if_exist(model, 'PDB', 'ihm_starting_model_details', 'ihm_starting_model_details_entity_poly_segment_id_fk', 'CASCADE')
    utils.alter_on_delete_fkey_if_exist(model, 'PDB', 'ihm_starting_model_details', 'ihm_starting_model_details_entity_poly_segment_id_fkey', 'CASCADE')
    utils.alter_on_delete_fkey_if_exist(model, 'PDB', 'ihm_struct_assembly_details', 'ihm_struct_assembly_details_entity_poly_segment_id_fk', 'CASCADE')
    utils.alter_on_delete_fkey_if_exist(model, 'PDB', 'ihm_struct_assembly_details', 'ihm_struct_assembly_details_entity_poly_segment_id_fkey', 'CASCADE')

    utils.alter_on_delete_fkey_if_exist(model, 'PDB', 'entity_name_com', 'entity_name_com_entity_id_fkey', 'CASCADE')
    utils.alter_on_delete_fkey_if_exist(model, 'PDB', 'entity_name_sys', 'entity_name_sys_entity_id_fkey', 'CASCADE')
    utils.alter_on_delete_fkey_if_exist(model, 'PDB', 'entity_poly', 'entity_poly_entity_id_fkey', 'CASCADE')
    utils.alter_on_delete_fkey_if_exist(model, 'PDB', 'entity_src_gen', 'entity_src_gen_entity_id_fkey', 'CASCADE')
    utils.alter_on_delete_fkey_if_exist(model, 'PDB', 'ihm_interface_residue_feature', 'ihm_interface_residue_feature_binding_partner_entity_id_fkey', 'CASCADE')
    utils.alter_on_delete_fkey_if_exist(model, 'PDB', 'ihm_ligand_probe', 'ihm_ligand_probe_entity_id_fkey', 'CASCADE')
    utils.alter_on_delete_fkey_if_exist(model, 'PDB', 'ihm_localization_density_files', 'ihm_localization_density_files_entity_id_fk', 'CASCADE')
    utils.alter_on_delete_fkey_if_exist(model, 'PDB', 'ihm_localization_density_files', 'ihm_localization_density_files_entity_id_fkey', 'CASCADE')
    utils.alter_on_delete_fkey_if_exist(model, 'PDB', 'ihm_non_poly_feature', 'ihm_non_poly_feature_entity_id_fkey', 'CASCADE')
    utils.alter_on_delete_fkey_if_exist(model, 'PDB', 'ihm_starting_model_details', 'ihm_starting_model_details_entity_id_fkey', 'CASCADE')
    utils.alter_on_delete_fkey_if_exist(model, 'PDB', 'ihm_struct_assembly_details', 'ihm_struct_assembly_details_entity_id_fkey', 'CASCADE')
    utils.alter_on_delete_fkey_if_exist(model, 'PDB', 'pdbx_entity_nonpoly', 'pdbx_entity_nonpoly_entity_id_fkey', 'CASCADE')
    utils.alter_on_delete_fkey_if_exist(model, 'PDB', 'pdbx_entity_poly_na_type', 'pdbx_entity_poly_na_type_entity_id_fkey', 'CASCADE')
    utils.alter_on_delete_fkey_if_exist(model, 'PDB', 'struct_asym', 'struct_asym_entity_id_fkey', 'CASCADE')

    utils.alter_on_delete_fkey_if_exist(model, 'PDB', 'entity_poly', 'entity_poly_structure_id_fkey', 'CASCADE')
    utils.alter_on_delete_fkey_if_exist(model, 'PDB', 'entity_poly_seq', 'entity_poly_seq_entity_id_fkey', 'CASCADE')

    utils.alter_on_delete_fkey_if_exist(model, 'PDB', 'ihm_2dem_class_average_restraint', 'ihm_2dem_class_average_restraint_struct_assembly_id_fkey', 'CASCADE')
    utils.alter_on_delete_fkey_if_exist(model, 'PDB', 'ihm_3dem_restraint', 'ihm_3dem_restraint_struct_assembly_id_fkey', 'CASCADE')
    utils.alter_on_delete_fkey_if_exist(model, 'PDB', 'ihm_model_list', 'ihm_model_list_assembly_id_fkey', 'CASCADE')
    utils.alter_on_delete_fkey_if_exist(model, 'PDB', 'ihm_modeling_post_process', 'ihm_modeling_post_process_struct_assembly_id_fk', 'CASCADE')
    utils.alter_on_delete_fkey_if_exist(model, 'PDB', 'ihm_modeling_post_process', 'ihm_modeling_post_process_struct_assembly_id_fkey', 'CASCADE')
    utils.alter_on_delete_fkey_if_exist(model, 'PDB', 'ihm_modeling_protocol_details', 'ihm_modeling_protocol_details_struct_assembly_id_fk', 'CASCADE')
    utils.alter_on_delete_fkey_if_exist(model, 'PDB', 'ihm_modeling_protocol_details', 'ihm_modeling_protocol_details_struct_assembly_id_fkey', 'CASCADE')
    utils.alter_on_delete_fkey_if_exist(model, 'PDB', 'ihm_sas_restraint', 'ihm_sas_restraint_struct_assembly_id_fkey', 'CASCADE')
    utils.alter_on_delete_fkey_if_exist(model, 'PDB', 'ihm_struct_assembly_class_link', 'ihm_struct_assembly_class_link_assembly_id_fkey', 'CASCADE')
    utils.alter_on_delete_fkey_if_exist(model, 'PDB', 'ihm_struct_assembly_details', 'ihm_struct_assembly_details_assembly_id_fkey', 'CASCADE')
    utils.alter_on_delete_fkey_if_exist(model, 'PDB', 'ihm_struct_assembly_details', 'ihm_struct_assembly_details_parent_assembly_id_fkey', 'CASCADE')

    utils.alter_on_delete_fkey_if_exist(model, 'PDB', 'ihm_modeling_protocol_details', 'ihm_modeling_protocol_details_dataset_group_id_fkey', 'CASCADE')
    utils.alter_on_delete_fkey_if_exist(model, 'PDB', 'ihm_modeling_protocol_details', 'ihm_modeling_protocol_details_protocol_id_fkey', 'CASCADE')
    utils.alter_on_delete_fkey_if_exist(model, 'PDB', 'ihm_modeling_protocol_details', 'ihm_modeling_protocol_details_script_file_id_fk', 'CASCADE')
    utils.alter_on_delete_fkey_if_exist(model, 'PDB', 'ihm_modeling_protocol_details', 'ihm_modeling_protocol_details_script_file_id_fkey', 'CASCADE')
    utils.alter_on_delete_fkey_if_exist(model, 'PDB', 'ihm_modeling_protocol_details', 'ihm_modeling_protocol_details_software_id_fk', 'CASCADE')
    utils.alter_on_delete_fkey_if_exist(model, 'PDB', 'ihm_modeling_protocol_details', 'ihm_modeling_protocol_details_software_id_fkey', 'CASCADE')
    
# ===================================================    

if __name__ == '__main__':
    args = ApplicationClient('ad-hoc table creation tool', None, 1).parse_cli()
    credentials = get_credential(args.host, args.credential_file)
#    if args.catalog is None:
#        catalog_id = 99

    main(args.host, args.catalog_id, credentials)
    
