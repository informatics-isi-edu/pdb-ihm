import sys
import json
from deriva.core import ErmrestCatalog, AttrDict, get_credential, DEFAULT_CREDENTIAL_FILE, tag, urlquote, DerivaServer, get_credential, BaseCLI
from deriva.core.ermrest_model import builtin_types, Schema, Table, Column, Key, ForeignKey, DomainType, ArrayType
import utils
from utils import ApplicationClient

"""
Referenced by:
    TABLE ""PDB"."Entry_Error_File"" CONSTRAINT "Entry_Error_File_Entry_RID_fkey" FOREIGN KEY ("Entry_RID") REFERENCES "PDB".entry("RID") ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB"."Entry_Related_File"" CONSTRAINT "Entry_Related_File_entry_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB"."Entry_mmCIF_File"" CONSTRAINT "Entry_mmCIF_File_Structure_Id_fkey" FOREIGN KEY ("Structure_Id") REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".atom_type" CONSTRAINT "atom_type_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".audit_author" CONSTRAINT "audit_author_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".audit_conform" CONSTRAINT "audit_conform_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".chem_comp_atom" CONSTRAINT "chem_comp_atom_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".chem_comp" CONSTRAINT "chem_comp_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".citation_author" CONSTRAINT "citation_author_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".citation" CONSTRAINT "citation_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".entity_name_com" CONSTRAINT "entity_name_com_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".entity_name_sys" CONSTRAINT "entity_name_sys_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".entity_poly_seq" CONSTRAINT "entity_poly_seq_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".entity_poly" CONSTRAINT "entity_poly_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".entity_src_gen" CONSTRAINT "entity_src_gen_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".entity" CONSTRAINT "entity_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".ihm_2dem_class_average_fitting" CONSTRAINT "ihm_2dem_class_average_fitting_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".ihm_2dem_class_average_restraint" CONSTRAINT "ihm_2dem_class_average_restraint_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".ihm_3dem_restraint" CONSTRAINT "ihm_3dem_restraint_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".ihm_chemical_component_descriptor" CONSTRAINT "ihm_chemical_component_descriptor_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".ihm_cross_link_list" CONSTRAINT "ihm_cross_link_list_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".ihm_cross_link_pseudo_site" CONSTRAINT "ihm_cross_link_pseudo_site_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE
    TABLE ""PDB".ihm_cross_link_restraint" CONSTRAINT "ihm_cross_link_restraint_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".ihm_cross_link_result_parameters" CONSTRAINT "ihm_cross_link_result_parameters_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".ihm_cross_link_result" CONSTRAINT "ihm_cross_link_result_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".ihm_data_transformation" CONSTRAINT "ihm_data_transformation_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE
    TABLE ""PDB".ihm_dataset_external_reference" CONSTRAINT "ihm_dataset_external_reference_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".ihm_dataset_group_link" CONSTRAINT "ihm_dataset_group_link_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".ihm_dataset_group" CONSTRAINT "ihm_dataset_group_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".ihm_dataset_list" CONSTRAINT "ihm_dataset_list_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".ihm_dataset_related_db_reference" CONSTRAINT "ihm_dataset_related_db_reference_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".ihm_derived_angle_restraint" CONSTRAINT "ihm_derived_angle_restraint_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE
    TABLE ""PDB".ihm_derived_dihedral_restraint" CONSTRAINT "ihm_derived_dihedral_restraint_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE
    TABLE ""PDB".ihm_derived_distance_restraint" CONSTRAINT "ihm_derived_distance_restraint_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".ihm_ensemble_info" CONSTRAINT "ihm_ensemble_info_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".ihm_ensemble_sub_sample" CONSTRAINT "ihm_ensemble_sub_sample_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE
    TABLE ""PDB".ihm_entity_poly_segment" CONSTRAINT "ihm_entity_poly_segment_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".ihm_epr_restraint" CONSTRAINT "ihm_epr_restraint_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".ihm_external_files" CONSTRAINT "ihm_external_files_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".ihm_external_reference_info" CONSTRAINT "ihm_external_reference_info_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".ihm_feature_list" CONSTRAINT "ihm_feature_list_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".ihm_geometric_object_axis" CONSTRAINT "ihm_geometric_object_axis_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".ihm_geometric_object_center" CONSTRAINT "ihm_geometric_object_center_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".ihm_geometric_object_distance_restraint" CONSTRAINT "ihm_geometric_object_distance_restraint_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".ihm_geometric_object_half_torus" CONSTRAINT "ihm_geometric_object_half_torus_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".ihm_geometric_object_list" CONSTRAINT "ihm_geometric_object_list_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".ihm_geometric_object_plane" CONSTRAINT "ihm_geometric_object_plane_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".ihm_geometric_object_sphere" CONSTRAINT "ihm_geometric_object_sphere_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".ihm_geometric_object_torus" CONSTRAINT "ihm_geometric_object_torus_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".ihm_geometric_object_transformation" CONSTRAINT "ihm_geometric_object_transformation_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".ihm_hdx_restraint" CONSTRAINT "ihm_hdx_restraint_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE
    TABLE ""PDB".ihm_hydroxyl_radical_fp_restraint" CONSTRAINT "ihm_hydroxyl_radical_fp_restraint_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".ihm_interface_residue_feature" CONSTRAINT "ihm_interface_residue_feature_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".ihm_ligand_probe" CONSTRAINT "ihm_ligand_probe_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".ihm_localization_density_files" CONSTRAINT "ihm_localization_density_files_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".ihm_model_group_link" CONSTRAINT "ihm_model_group_link_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".ihm_model_group" CONSTRAINT "ihm_model_group_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".ihm_model_list" CONSTRAINT "ihm_model_list_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".ihm_model_representation_details" CONSTRAINT "ihm_model_representation_details_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".ihm_model_representation" CONSTRAINT "ihm_model_representation_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".ihm_model_representative" CONSTRAINT "ihm_model_representative_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".ihm_modeling_post_process" CONSTRAINT "ihm_modeling_post_process_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".ihm_modeling_protocol_details" CONSTRAINT "ihm_modeling_protocol_details_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".ihm_modeling_protocol" CONSTRAINT "ihm_modeling_protocol_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".ihm_multi_state_model_group_link" CONSTRAINT "ihm_multi_state_model_group_link_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".ihm_multi_state_modeling" CONSTRAINT "ihm_multi_state_modeling_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".ihm_non_poly_feature" CONSTRAINT "ihm_non_poly_feature_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".ihm_ordered_ensemble" CONSTRAINT "ihm_ordered_ensemble_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".ihm_poly_atom_feature" CONSTRAINT "ihm_poly_atom_feature_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".ihm_poly_probe_conjugate" CONSTRAINT "ihm_poly_probe_conjugate_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".ihm_poly_probe_position" CONSTRAINT "ihm_poly_probe_position_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".ihm_poly_residue_feature" CONSTRAINT "ihm_poly_residue_feature_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".ihm_predicted_contact_restraint" CONSTRAINT "ihm_predicted_contact_restraint_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".ihm_probe_list" CONSTRAINT "ihm_probe_list_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".ihm_pseudo_site_feature" CONSTRAINT "ihm_pseudo_site_feature_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".ihm_pseudo_site" CONSTRAINT "ihm_pseudo_site_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE
    TABLE ""PDB".ihm_related_datasets" CONSTRAINT "ihm_related_datasets_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".ihm_residues_not_modeled" CONSTRAINT "ihm_residues_not_modeled_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".ihm_sas_restraint" CONSTRAINT "ihm_sas_restraint_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".ihm_starting_comparative_models" CONSTRAINT "ihm_starting_comparative_models_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".ihm_starting_computational_models" CONSTRAINT "ihm_starting_computational_models_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".ihm_starting_model_details" CONSTRAINT "ihm_starting_model_details_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".ihm_starting_model_seq_dif" CONSTRAINT "ihm_starting_model_seq_dif_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".ihm_struct_assembly_class_link" CONSTRAINT "ihm_struct_assembly_class_link_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".ihm_struct_assembly_class" CONSTRAINT "ihm_struct_assembly_class_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".ihm_struct_assembly_details" CONSTRAINT "ihm_struct_assembly_details_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".ihm_struct_assembly" CONSTRAINT "ihm_struct_assembly_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".pdbx_entity_nonpoly" CONSTRAINT "pdbx_entity_nonpoly_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".pdbx_entity_poly_na_type" CONSTRAINT "pdbx_entity_poly_na_type_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".pdbx_entry_details" CONSTRAINT "pdbx_entry_details_entry_id_fkey" FOREIGN KEY (entry_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".pdbx_inhibitor_info" CONSTRAINT "pdbx_inhibitor_info_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".pdbx_ion_info" CONSTRAINT "pdbx_ion_info_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".pdbx_protein_info" CONSTRAINT "pdbx_protein_info_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".software" CONSTRAINT "software_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".struct_asym" CONSTRAINT "struct_asym_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".struct" CONSTRAINT "struct_entry_id_fkey" FOREIGN KEY (entry_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".struct_ref_seq_dif" CONSTRAINT "struct_ref_seq_dif_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".struct_ref_seq" CONSTRAINT "struct_ref_seq_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".struct_ref" CONSTRAINT "struct_ref_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
Triggers:

"""

pdb_admin = "https://auth.globus.org/0b98092c-3c41-11e9-a8c8-0ee7d80087ee"
isrd_staff = "https://auth.globus.org/176baec4-ed26-11e5-8e88-22000ab4b42b"
pdb_curator = "https://auth.globus.org/eef3e02a-3c40-11e9-9276-0edc9bdd56a6"


"""
Submitters
    TABLE ""PDB"."Entry_Related_File"" CONSTRAINT "Entry_Related_File_entry_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".audit_author" CONSTRAINT "audit_author_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".citation_author" CONSTRAINT "citation_author_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".citation" CONSTRAINT "citation_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".entity_name_com" CONSTRAINT "entity_name_com_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".entity_name_sys" CONSTRAINT "entity_name_sys_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".entity_src_gen" CONSTRAINT "entity_src_gen_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".entity" CONSTRAINT "entity_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".ihm_2dem_class_average_fitting" CONSTRAINT "ihm_2dem_class_average_fitting_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".ihm_2dem_class_average_restraint" CONSTRAINT "ihm_2dem_class_average_restraint_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".ihm_3dem_restraint" CONSTRAINT "ihm_3dem_restraint_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".ihm_chemical_component_descriptor" CONSTRAINT "ihm_chemical_component_descriptor_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".ihm_cross_link_list" CONSTRAINT "ihm_cross_link_list_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".ihm_cross_link_pseudo_site" CONSTRAINT "ihm_cross_link_pseudo_site_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE
    TABLE ""PDB".ihm_cross_link_restraint" CONSTRAINT "ihm_cross_link_restraint_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".ihm_cross_link_result_parameters" CONSTRAINT "ihm_cross_link_result_parameters_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".ihm_cross_link_result" CONSTRAINT "ihm_cross_link_result_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".ihm_data_transformation" CONSTRAINT "ihm_data_transformation_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE
    TABLE ""PDB".ihm_dataset_external_reference" CONSTRAINT "ihm_dataset_external_reference_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".ihm_dataset_group_link" CONSTRAINT "ihm_dataset_group_link_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".ihm_dataset_group" CONSTRAINT "ihm_dataset_group_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".ihm_dataset_list" CONSTRAINT "ihm_dataset_list_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".ihm_dataset_related_db_reference" CONSTRAINT "ihm_dataset_related_db_reference_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".ihm_derived_angle_restraint" CONSTRAINT "ihm_derived_angle_restraint_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE
    TABLE ""PDB".ihm_derived_dihedral_restraint" CONSTRAINT "ihm_derived_dihedral_restraint_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE
    TABLE ""PDB".ihm_derived_distance_restraint" CONSTRAINT "ihm_derived_distance_restraint_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".ihm_ensemble_info" CONSTRAINT "ihm_ensemble_info_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".ihm_ensemble_sub_sample" CONSTRAINT "ihm_ensemble_sub_sample_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE
    TABLE ""PDB".ihm_entity_poly_segment" CONSTRAINT "ihm_entity_poly_segment_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".ihm_epr_restraint" CONSTRAINT "ihm_epr_restraint_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".ihm_external_files" CONSTRAINT "ihm_external_files_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".ihm_external_reference_info" CONSTRAINT "ihm_external_reference_info_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".ihm_feature_list" CONSTRAINT "ihm_feature_list_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".ihm_geometric_object_axis" CONSTRAINT "ihm_geometric_object_axis_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".ihm_geometric_object_center" CONSTRAINT "ihm_geometric_object_center_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".ihm_geometric_object_distance_restraint" CONSTRAINT "ihm_geometric_object_distance_restraint_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".ihm_geometric_object_half_torus" CONSTRAINT "ihm_geometric_object_half_torus_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".ihm_geometric_object_list" CONSTRAINT "ihm_geometric_object_list_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".ihm_geometric_object_plane" CONSTRAINT "ihm_geometric_object_plane_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".ihm_geometric_object_sphere" CONSTRAINT "ihm_geometric_object_sphere_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".ihm_geometric_object_torus" CONSTRAINT "ihm_geometric_object_torus_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".ihm_geometric_object_transformation" CONSTRAINT "ihm_geometric_object_transformation_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".ihm_hdx_restraint" CONSTRAINT "ihm_hdx_restraint_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE
    TABLE ""PDB".ihm_hydroxyl_radical_fp_restraint" CONSTRAINT "ihm_hydroxyl_radical_fp_restraint_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".ihm_interface_residue_feature" CONSTRAINT "ihm_interface_residue_feature_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".ihm_ligand_probe" CONSTRAINT "ihm_ligand_probe_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".ihm_localization_density_files" CONSTRAINT "ihm_localization_density_files_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".ihm_model_group_link" CONSTRAINT "ihm_model_group_link_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".ihm_model_group" CONSTRAINT "ihm_model_group_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".ihm_model_representation_details" CONSTRAINT "ihm_model_representation_details_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".ihm_model_representation" CONSTRAINT "ihm_model_representation_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".ihm_model_representative" CONSTRAINT "ihm_model_representative_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".ihm_modeling_post_process" CONSTRAINT "ihm_modeling_post_process_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".ihm_modeling_protocol_details" CONSTRAINT "ihm_modeling_protocol_details_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".ihm_modeling_protocol" CONSTRAINT "ihm_modeling_protocol_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".ihm_multi_state_model_group_link" CONSTRAINT "ihm_multi_state_model_group_link_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".ihm_multi_state_modeling" CONSTRAINT "ihm_multi_state_modeling_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".ihm_non_poly_feature" CONSTRAINT "ihm_non_poly_feature_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".ihm_ordered_ensemble" CONSTRAINT "ihm_ordered_ensemble_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".ihm_poly_atom_feature" CONSTRAINT "ihm_poly_atom_feature_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".ihm_poly_probe_conjugate" CONSTRAINT "ihm_poly_probe_conjugate_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".ihm_poly_probe_position" CONSTRAINT "ihm_poly_probe_position_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".ihm_poly_residue_feature" CONSTRAINT "ihm_poly_residue_feature_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".ihm_predicted_contact_restraint" CONSTRAINT "ihm_predicted_contact_restraint_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".ihm_probe_list" CONSTRAINT "ihm_probe_list_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".ihm_pseudo_site_feature" CONSTRAINT "ihm_pseudo_site_feature_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".ihm_pseudo_site" CONSTRAINT "ihm_pseudo_site_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE
    TABLE ""PDB".ihm_related_datasets" CONSTRAINT "ihm_related_datasets_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".ihm_residues_not_modeled" CONSTRAINT "ihm_residues_not_modeled_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".ihm_sas_restraint" CONSTRAINT "ihm_sas_restraint_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".ihm_starting_comparative_models" CONSTRAINT "ihm_starting_comparative_models_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".ihm_starting_computational_models" CONSTRAINT "ihm_starting_computational_models_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".ihm_starting_model_details" CONSTRAINT "ihm_starting_model_details_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".ihm_starting_model_seq_dif" CONSTRAINT "ihm_starting_model_seq_dif_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".ihm_struct_assembly_class_link" CONSTRAINT "ihm_struct_assembly_class_link_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".ihm_struct_assembly_class" CONSTRAINT "ihm_struct_assembly_class_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".ihm_struct_assembly_details" CONSTRAINT "ihm_struct_assembly_details_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".ihm_struct_assembly" CONSTRAINT "ihm_struct_assembly_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".pdbx_entity_nonpoly" CONSTRAINT "pdbx_entity_nonpoly_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".software" CONSTRAINT "software_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".struct" CONSTRAINT "struct_entry_id_fkey" FOREIGN KEY (entry_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".struct_ref_seq_dif" CONSTRAINT "struct_ref_seq_dif_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".struct_ref_seq" CONSTRAINT "struct_ref_seq_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
    TABLE ""PDB".struct_ref" CONSTRAINT "struct_ref_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
"""



tables = {
    'struct': 'struct_entry_id_fkey',
    'audit_author': 'audit_author_structure_id_fkey',
    'citation': 'citation_structure_id_fkey',
    'citation_author': 'citation_author_structure_id_fkey',
    'software': 'software_structure_id_fkey',
    'entity': 'entity_structure_id_fkey',
    'entity_name_com': 'entity_name_com_structure_id_fkey',
    'entity_name_sys': 'entity_name_sys_structure_id_fkey',
    'entity_src_gen': 'entity_src_gen_structure_id_fkey',
    'struct_ref': 'struct_ref_structure_id_fkey',
    'struct_ref_seq': 'struct_ref_seq_structure_id_fkey',
    'struct_ref_seq_dif': 'struct_ref_seq_dif_structure_id_fkey',
    'pdbx_entity_nonpoly': 'pdbx_entity_nonpoly_structure_id_fkey',
    'ihm_dataset_list': 'ihm_dataset_list_structure_id_fkey',
    'ihm_dataset_group': 'ihm_dataset_group_structure_id_fkey',
    'ihm_dataset_group_link': 'ihm_dataset_group_link_structure_id_fkey',
    'ihm_data_transformation': 'ihm_data_transformation_structure_id_fkey',
    'ihm_related_datasets': 'ihm_related_datasets_structure_id_fkey',
    'ihm_dataset_related_db_reference': 'ihm_dataset_related_db_reference_structure_id_fkey',
    'ihm_external_reference_info': 'ihm_external_reference_info_structure_id_fkey',
    'ihm_external_files': 'ihm_external_files_structure_id_fkey',
    'ihm_dataset_external_reference': 'ihm_dataset_external_reference_structure_id_fkey',
    'ihm_entity_poly_segment': 'ihm_entity_poly_segment_structure_id_fkey',
    'ihm_struct_assembly': 'ihm_struct_assembly_structure_id_fkey',
    'ihm_struct_assembly_details': 'ihm_struct_assembly_details_structure_id_fkey',
    'ihm_struct_assembly_class': 'ihm_struct_assembly_class_structure_id_fkey',
    'ihm_struct_assembly_class_link': 'ihm_struct_assembly_class_link_structure_id_fkey',
    'ihm_starting_model_details': 'ihm_starting_model_details_structure_id_fkey',
    'ihm_starting_comparative_models': 'ihm_starting_comparative_models_structure_id_fkey',
    'ihm_starting_computational_models': 'ihm_starting_computational_models_structure_id_fkey',
    'ihm_starting_model_seq_dif': 'ihm_starting_model_seq_dif_structure_id_fkey',
    'ihm_model_representation': 'ihm_model_representation_structure_id_fkey',
    'ihm_model_representation_details': 'ihm_model_representation_details_structure_id_fkey',
    'ihm_modeling_protocol': 'ihm_modeling_protocol_structure_id_fkey',
    'ihm_modeling_protocol_details': 'ihm_modeling_protocol_details_structure_id_fkey',
    'ihm_modeling_post_process': 'ihm_modeling_post_process_structure_id_fkey',
    'ihm_model_group': 'ihm_model_group_structure_id_fkey',
    'ihm_model_group_link': 'ihm_model_group_link_structure_id_fkey',
    'ihm_model_representative': 'ihm_model_representative_structure_id_fkey',
    'ihm_residues_not_modeled': 'ihm_residues_not_modeled_structure_id_fkey',
    'ihm_multi_state_modeling': 'ihm_multi_state_modeling_structure_id_fkey',
    'ihm_multi_state_model_group_link': 'ihm_multi_state_model_group_link_structure_id_fkey',
    'ihm_ordered_ensemble': 'ihm_ordered_ensemble_structure_id_fkey',
    'ihm_ensemble_info': 'ihm_ensemble_info_structure_id_fkey',
    'ihm_ensemble_sub_sample': 'ihm_ensemble_sub_sample_structure_id_fkey',
    'ihm_localization_density_files': 'ihm_localization_density_files_structure_id_fkey',
    'ihm_2dem_class_average_restraint': 'ihm_2dem_class_average_restraint_structure_id_fkey',
    'ihm_2dem_class_average_fitting': 'ihm_2dem_class_average_fitting_structure_id_fkey',
    'ihm_3dem_restraint': 'ihm_3dem_restraint_structure_id_fkey',
    'ihm_sas_restraint': 'ihm_sas_restraint_structure_id_fkey',
    'ihm_epr_restraint': 'ihm_epr_restraint_structure_id_fkey',
    'ihm_chemical_component_descriptor': 'ihm_chemical_component_descriptor_structure_id_fkey',
    'ihm_probe_list': 'ihm_probe_list_structure_id_fkey',
    'ihm_poly_probe_position': 'ihm_poly_probe_position_structure_id_fkey',
    'ihm_poly_probe_conjugate': 'ihm_poly_probe_conjugate_structure_id_fkey',
    'ihm_ligand_probe': 'ihm_ligand_probe_structure_id_fkey',
    'ihm_geometric_object_list': 'ihm_geometric_object_list_structure_id_fkey',
    'ihm_geometric_object_center': 'ihm_geometric_object_center_structure_id_fkey',
    'ihm_geometric_object_transformation': 'ihm_geometric_object_transformation_structure_id_fkey',
    'ihm_geometric_object_sphere': 'ihm_geometric_object_sphere_structure_id_fkey',
    'ihm_geometric_object_torus': 'ihm_geometric_object_torus_structure_id_fkey',
    'ihm_geometric_object_half_torus': 'ihm_geometric_object_half_torus_structure_id_fkey',
    'ihm_geometric_object_plane': 'ihm_geometric_object_plane_structure_id_fkey',
    'ihm_geometric_object_axis': 'ihm_geometric_object_axis_structure_id_fkey',
    'Entry_Related_File': 'Entry_Related_File_entry_id_fkey',
    'ihm_pseudo_site': 'ihm_pseudo_site_structure_id_fkey',
    'ihm_cross_link_list': 'ihm_cross_link_list_structure_id_fkey',
    'ihm_cross_link_restraint': 'ihm_cross_link_restraint_structure_id_fkey',
    'ihm_cross_link_pseudo_site': 'ihm_cross_link_pseudo_site_structure_id_fkey',
    'ihm_cross_link_result': 'ihm_cross_link_result_structure_id_fkey',
    'ihm_cross_link_result_parameters': 'ihm_cross_link_result_parameters_structure_id_fkey',
    'ihm_predicted_contact_restraint': 'ihm_predicted_contact_restraint_structure_id_fkey',
    'ihm_hydroxyl_radical_fp_restraint': 'ihm_hydroxyl_radical_fp_restraint_structure_id_fkey',
    'ihm_hdx_restraint': 'ihm_hdx_restraint_structure_id_fkey',
    'ihm_feature_list': 'ihm_feature_list_structure_id_fkey',
    'ihm_poly_atom_feature': 'ihm_poly_atom_feature_structure_id_fkey',
    'ihm_poly_residue_feature': 'ihm_poly_residue_feature_structure_id_fkey',
    'ihm_non_poly_feature': 'ihm_non_poly_feature_structure_id_fkey',
    'ihm_interface_residue_feature': 'ihm_interface_residue_feature_structure_id_fkey',
    'ihm_pseudo_site_feature': 'ihm_pseudo_site_feature_structure_id_fkey',
    'ihm_derived_distance_restraint': 'ihm_derived_distance_restraint_structure_id_fkey',
    'ihm_derived_angle_restraint': 'ihm_derived_angle_restraint_structure_id_fkey',
    'ihm_derived_dihedral_restraint': 'ihm_derived_dihedral_restraint_structure_id_fkey',
    'ihm_geometric_object_distance_restraint': 'ihm_geometric_object_distance_restraint_structure_id_fkey'
    }

acls = {
    "insert": [ pdb_curator ],
    "update": [ pdb_curator ]
  }

acl_bindings = {
    "unfrozen": {
      "types": [ "insert", "update" ],
      "projection": [ 
            {
                "or": [
                    {
                        "filter": "Workflow_Status",
                        "operand": "DRAFT",
                        "operator": "="
                    },
                    {
                        "filter": "Workflow_Status",
                        "operand": "DEPO",
                        "operator": "="
                    },
                    {
                        "filter": "Workflow_Status",
                        "operand": "RECORD READY",
                        "operator": "="
                    },
                    {
                        "filter": "Workflow_Status",
                        "operand": "ERROR",
                        "operator": "="
                    }
                ]
            },
           "RID" ],
      "projection_type": "nonnull"
    }
  }

def main(server_name, catalog_id, credentials):
    server = DerivaServer('https', server_name, credentials)
    catalog = server.connect_ermrest(catalog_id)
    catalog.dcctx['cid'] = 'oneoff/model'
    """
    print('acl_bindings')
    print(json.dumps(fk.acl_bindings, indent=4))
    print('acls')
    print(json.dumps(fk.acls, indent=4))
    """
    for table_name, constraint_name in tables.items():
        model = catalog.getCatalogModel()
        schema = model.schemas['PDB']
        table = model.schemas['PDB'].tables[table_name]
        fk = table.foreign_keys.__getitem__((schema, constraint_name))
        #print(table_name, constraint_name)    
    
        utils.set_foreign_key_acls(catalog, 'PDB', table_name, constraint_name, acls)
        utils.set_foreign_key_acl_bindings(catalog, 'PDB', table_name, constraint_name, acl_bindings)

if __name__ == '__main__':
    args = ApplicationClient('ad-hoc table creation tool', None, 1).parse_cli()
    credentials = get_credential(args.host, args.credential_file)
    main(args.host, args.catalog_id, credentials)
    
