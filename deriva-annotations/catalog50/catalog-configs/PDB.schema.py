import argparse
from deriva.core import ErmrestCatalog, AttrDict, get_credential
import deriva.core.ermrest_model as em
from deriva.core.ermrest_config import tag as chaise_tags
from deriva.utils.catalog.manage.update_catalog import CatalogUpdater, parse_args

groups = {}

schema_name = 'PDB'

table_names = [
    'ihm_chemical_component_descriptor', 'ihm_poly_probe_position', 'ihm_feature_list',
    'audit_conform', 'ihm_hydroxyl_radical_fp_restraint', 'ihm_2dem_class_average_fitting',
    'pdbx_ion_info', 'ihm_geometric_object_sphere', 'audit_author', 'ihm_related_datasets',
    'ihm_dataset_group', 'ihm_dataset_related_db_reference', 'pdbx_entity_poly_na_type',
    'ihm_dataset_external_reference', 'ihm_3dem_restraint', 'ihm_residues_not_modeled',
    'ihm_probe_list', 'entry', 'ihm_cross_link_list', 'ihm_epr_restraint', 'ihm_ordered_ensemble',
    'ihm_poly_probe_conjugate', 'ihm_geometric_object_torus', 'pdbx_entry_details',
    'ihm_multi_state_modeling', 'citation', 'pdbx_inhibitor_info', 'ihm_external_files',
    'ihm_model_list', 'ihm_ensemble_info', 'ihm_model_representative',
    'ihm_interface_residue_feature', 'ihm_2dem_class_average_restraint', 'ihm_sas_restraint',
    'ihm_geometric_object_center', 'ihm_external_reference_info', 'ihm_ligand_probe',
    'ihm_poly_residue_feature', 'ihm_geometric_object_transformation',
    'ihm_geometric_object_half_torus', 'ihm_geometric_object_plane', 'struct',
    'ihm_non_poly_feature', 'ihm_pseudo_site_feature', 'ihm_localization_density_files',
    'pdbx_protein_info', 'ihm_predicted_contact_restraint', 'ihm_dataset_list',
    'ihm_geometric_object_distance_restraint', 'ihm_derived_distance_restraint',
    'ihm_geometric_object_list', 'ihm_cross_link_result_parameters', 'ihm_geometric_object_axis',
    'software', 'ihm_struct_assembly_details', 'ihm_poly_atom_feature', 'Entry_Related_File',
    'entity', 'ihm_cross_link_restraint', 'ihm_dataset_group_link', 'ihm_model_representation',
    'pdbx_entity_nonpoly', 'chem_comp', 'ihm_model_group', 'ihm_entity_poly_segment',
    'ihm_starting_model_seq_dif', 'chem_comp_atom', 'ihm_starting_model_details',
    'ihm_struct_assembly_class', 'citation_author', 'entity_name_sys',
    'ihm_struct_assembly_class_link', 'entity_name_com', 'ihm_model_group_link',
    'ihm_modeling_protocol', 'ihm_cross_link_result', 'entity_src_gen', 'ihm_struct_assembly',
    'entity_poly', 'ihm_modeling_post_process', 'ihm_starting_computational_models',
    'ihm_model_representation_details', 'struct_asym', 'ihm_starting_comparative_models',
    'ihm_modeling_protocol_details', 'ihm_multi_state_model_group_link', 'entity_poly_seq',
    'atom_type', 'Entry_mmCIF_File',
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
    catalog_id = 50
    mode, replace, host, catalog_id = parse_args(host, catalog_id)
    catalog = ErmrestCatalog('https', host, catalog_id=catalog_id, credentials=get_credential(host))
    main(catalog, mode, replace)
