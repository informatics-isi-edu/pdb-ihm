import argparse
from deriva.core import ErmrestCatalog, AttrDict, get_credential
import deriva.core.ermrest_model as em
from deriva.core.ermrest_config import tag as chaise_tags
from deriva.utils.catalog.manage.update_catalog import CatalogUpdater, parse_args

groups = {}

schema_name = 'PDB'

table_names = [
    'ihm_localization_density_files', 'ihm_model_representative',
    'ihm_chemical_component_descriptor', 'pdbx_inhibitor_info', 'ihm_dataset_external_reference',
    'ihm_cross_link_list', 'ihm_probe_list', 'ihm_epr_restraint', 'ihm_2dem_class_average_fitting',
    'ihm_poly_probe_conjugate', 'ihm_model_list', 'ihm_feature_list', 'pdbx_entity_poly_na_type',
    'ihm_ordered_ensemble', 'ihm_geometric_object_list', 'pdbx_ion_info',
    'ihm_geometric_object_sphere', 'ihm_poly_residue_feature', 'audit_conform',
    'pdbx_entry_details', 'ihm_related_datasets', 'ihm_multi_state_modeling', 'ihm_dataset_group',
    'entry', 'ihm_interface_residue_feature', 'ihm_dataset_list', 'audit_author',
    'ihm_geometric_object_plane', 'ihm_predicted_contact_restraint', 'ihm_3dem_restraint',
    'ihm_derived_distance_restraint', 'citation', 'ihm_sas_restraint',
    'ihm_hydroxyl_radical_fp_restraint', 'ihm_geometric_object_distance_restraint',
    'ihm_external_files', 'ihm_external_reference_info', 'ihm_2dem_class_average_restraint',
    'ihm_residues_not_modeled', 'ihm_dataset_related_db_reference', 'ihm_geometric_object_axis',
    'ihm_non_poly_feature', 'ihm_geometric_object_half_torus', 'pdbx_protein_info',
    'ihm_geometric_object_torus', 'ihm_pseudo_site_feature', 'ihm_cross_link_result_parameters',
    'struct', 'ihm_geometric_object_center', 'ihm_ensemble_info', 'ihm_poly_probe_position',
    'ihm_ligand_probe', 'ihm_geometric_object_transformation', 'software', 'chem_comp_atom',
    'entity_poly_seq', 'chem_comp', 'citation_author', 'ihm_struct_assembly_details',
    'entity_src_gen', 'entity_name_com', 'struct_asym', 'ihm_model_representation', 'atom_type',
    'entity', 'ihm_model_representation_details', 'ihm_entity_poly_segment', 'entity_poly',
    'entity_name_sys', 'pdbx_entity_nonpoly', 'Entry_mmCIF_File',
    'ihm_multi_state_model_group_link', 'ihm_model_group', 'ihm_cross_link_restraint',
    'ihm_model_group_link', 'ihm_poly_atom_feature', 'ihm_starting_model_seq_dif',
    'ihm_modeling_post_process', 'ihm_cross_link_result', 'ihm_starting_computational_models',
    'ihm_modeling_protocol', 'ihm_starting_comparative_models', 'ihm_modeling_protocol_details',
    'ihm_dataset_group_link', 'ihm_starting_model_details', 'Entry_Related_File',
    'ihm_struct_assembly', 'ihm_struct_assembly_class', 'ihm_struct_assembly_class_link',
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
