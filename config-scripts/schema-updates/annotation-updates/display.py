from deriva.core import DerivaServer, get_credential, BaseCLI
from deriva.core.ermrest_model import Table, Column, Key, ForeignKey, builtin_types

def table_annotations(model):
    #table = model.table("PDB", "software")
    #table.comment = "List of software used in the modeling"
    #table.column_definitions["Species_Tested_In"].comment = None

    model.table("PDB", "Entry_mmCIF_File").annotations.update({"tag:misd.isi.edu,2015:display": {"name": "System Generated mmCIF File"}})
    model.table("PDB", "struct").annotations.update({"tag:misd.isi.edu,2015:display": {"name": "Structure"}})
    model.table("PDB", "audit_author").annotations.update({"tag:misd.isi.edu,2015:display": {"name": "Authors of the Structure"}})
    model.table("PDB", "citation_author").annotations.update({"tag:misd.isi.edu,2015:display": {"name": "Authors in Citations"}})
    model.table("PDB", "chem_comp").annotations.update({"tag:misd.isi.edu,2015:display": {"name": "Chemical Components"}})
    model.table("PDB", "entity").annotations.update({"tag:misd.isi.edu,2015:display": {"name": "Molecular Entities"}})
    model.table("PDB", "entity_name_com").annotations.update({"tag:misd.isi.edu,2015:display": {"name": "Common Names of Entities"}})
    model.table("PDB", "entity_name_sys").annotations.update({"tag:misd.isi.edu,2015:display": {"name": "Systematic Names of Entities"}})
    model.table("PDB", "entity_src_gen").annotations.update({"tag:misd.isi.edu,2015:display": {"name": "Source of Genetically Manipulated Entities"}})
    model.table("PDB", "entity_poly").annotations.update({"tag:misd.isi.edu,2015:display": {"name": "Polymeric Entities"}})   
    model.table("PDB", "pdbx_entity_nonpoly").annotations.update({"tag:misd.isi.edu,2015:display": {"name": "Non-polymeric Entities"}})
    model.table("PDB", "entity_poly_seq").annotations.update({"tag:misd.isi.edu,2015:display": {"name": "Sequences of Polymeric Entities"}})
    model.table("PDB", "atom_type").annotations.update({"tag:misd.isi.edu,2015:display": {"name": "Types of Atoms in the Structure"}})
    model.table("PDB", "struct_asym").annotations.update({"tag:misd.isi.edu,2015:display": {"name": "Instances of Molecular Entities in the Structure"}})
    model.table("PDB", "ihm_dataset_list").annotations.update({"tag:misd.isi.edu,2015:display": {"name": "Input Datasets"}})
    model.table("PDB", "ihm_dataset_group").annotations.update({"tag:misd.isi.edu,2015:display": {"name": "Groups of Input Datasets"}})
    model.table("PDB", "ihm_dataset_group_link").annotations.update({"tag:misd.isi.edu,2015:display": {"name": "Datasets Belonging to Groups"}})
    model.table("PDB", "ihm_related_datasets").annotations.update({"tag:misd.isi.edu,2015:display": {"name": "Datasets Derived from Another"}})
    model.table("PDB", "ihm_dataset_related_db_reference").annotations.update({"tag:misd.isi.edu,2015:display": {"name": "Datasets Archived in Other Repositories"}})
    model.table("PDB", "ihm_external_reference_info").annotations.update({"tag:misd.isi.edu,2015:display": {"name": "Datasets Referenced Via DOI"}})
    model.table("PDB", "ihm_external_files").annotations.update({"tag:misd.isi.edu,2015:display": {"name": "External Files Referenced Via DOI"}})
    model.table("PDB", "ihm_dataset_external_reference").annotations.update({"tag:misd.isi.edu,2015:display": {"name": "Links Between External Files and Input Datasets"}})
    model.table("PDB", "ihm_entity_poly_segment").annotations.update({"tag:misd.isi.edu,2015:display": {"name": "Segments of Polymeric Entities"}})
    model.table("PDB", "ihm_struct_assembly").annotations.update({"tag:misd.isi.edu,2015:display": {"name": "Structural Assemblies"}})
    model.table("PDB", "ihm_struct_assembly_details").annotations.update({"tag:misd.isi.edu,2015:display": {"name": "Details of Structural Assemblies"}})
    model.table("PDB", "ihm_struct_assembly_class").annotations.update({"tag:misd.isi.edu,2015:display": {"name": "Structural Assembly Classes in Hierarchical Assemblies"}})
    model.table("PDB", "ihm_struct_assembly_class_link").annotations.update({"tag:misd.isi.edu,2015:display": {"name": "Structural Assemblies Belonging to Classes"}})
    model.table("PDB", "ihm_starting_model_details").annotations.update({"tag:misd.isi.edu,2015:display": {"name": "Starting Structural Models"}})
    model.table("PDB", "ihm_starting_comparative_models").annotations.update({"tag:misd.isi.edu,2015:display": {"name": "Starting Comparative Models"}})
    model.table("PDB", "ihm_starting_computational_models").annotations.update({"tag:misd.isi.edu,2015:display": {"name": "Starting Computational Models"}})
    model.table("PDB", "ihm_starting_model_seq_dif").annotations.update({"tag:misd.isi.edu,2015:display": {"name": "Point Differences in the Sequences of Starting Models"}})
    model.table("PDB", "ihm_model_representation").annotations.update({"tag:misd.isi.edu,2015:display": {"name": "Model Representations"}})
    model.table("PDB", "ihm_model_representation_details").annotations.update({"tag:misd.isi.edu,2015:display": {"name": "Details of Model Representations"}})
    model.table("PDB", "ihm_modeling_protocol").annotations.update({"tag:misd.isi.edu,2015:display": {"name": "Modeling Protocols"}})
    model.table("PDB", "ihm_modeling_protocol_details").annotations.update({"tag:misd.isi.edu,2015:display": {"name": "Details of Modeling Protocols"}})
    model.table("PDB", "ihm_modeling_post_process").annotations.update({"tag:misd.isi.edu,2015:display": {"name": "Post Modeling Analyses"}})
    model.table("PDB", "ihm_model_list").annotations.update({"tag:misd.isi.edu,2015:display": {"name": "Models Submitted"}})
    model.table("PDB", "ihm_model_group").annotations.update({"tag:misd.isi.edu,2015:display": {"name": "Groups of Models"}})
    model.table("PDB", "ihm_model_group_link").annotations.update({"tag:misd.isi.edu,2015:display": {"name": "Models Belonging to Groups"}})
    model.table("PDB", "ihm_model_representative").annotations.update({"tag:misd.isi.edu,2015:display": {"name": "Representative Model in an Ensemble"}})
    model.table("PDB", "ihm_residues_not_modeled").annotations.update({"tag:misd.isi.edu,2015:display": {"name": "Residues Not Modeled"}})
    model.table("PDB", "ihm_multi_state_modeling").annotations.update({"tag:misd.isi.edu,2015:display": {"name": "Multi-State Modeling"}})
    model.table("PDB", "ihm_multi_state_model_group_link").annotations.update({"tag:misd.isi.edu,2015:display": {"name": "Model Groups Belonging to Multiple States"}})
    model.table("PDB", "ihm_ordered_ensemble").annotations.update({"tag:misd.isi.edu,2015:display": {"name": "Ordered States"}})
    model.table("PDB", "ihm_ensemble_info").annotations.update({"tag:misd.isi.edu,2015:display": {"name": "Details of Ensembles"}})
    model.table("PDB", "ihm_localization_density_files").annotations.update({"tag:misd.isi.edu,2015:display": {"name": "Localization Density Files Referenced Via DOI"}})
    model.table("PDB", "ihm_2dem_class_average_restraint").annotations.update({"tag:misd.isi.edu,2015:display": {"name": "2DEM Class Average Restraints"}})
    model.table("PDB", "ihm_2dem_class_average_fitting").annotations.update({"tag:misd.isi.edu,2015:display": {"name": "2DEM Class Average Fitting"}})
    model.table("PDB", "ihm_3dem_restraint").annotations.update({"tag:misd.isi.edu,2015:display": {"name": "3DEM Restraints"}})
    model.table("PDB", "ihm_sas_restraint").annotations.update({"tag:misd.isi.edu,2015:display": {"name": "SAS Restraints"}})
    model.table("PDB", "ihm_epr_restraint").annotations.update({"tag:misd.isi.edu,2015:display": {"name": "EPR Restraints"}})
    model.table("PDB", "ihm_chemical_component_descriptor").annotations.update({"tag:misd.isi.edu,2015:display": {"name": "Chemical Descriptors of Molecular Probes Used in Experiments"}})
    model.table("PDB", "ihm_probe_list").annotations.update({"tag:misd.isi.edu,2015:display": {"name": "Molecular Probes"}})
    model.table("PDB", "ihm_poly_probe_position").annotations.update({"tag:misd.isi.edu,2015:display": {"name": "Residue Positions in Polymeric Entities where Probes are Attached"}})
    model.table("PDB", "ihm_poly_probe_conjugate").annotations.update({"tag:misd.isi.edu,2015:display": {"name": "Probes Attached to Residues in Polymeric Entities"}})
    model.table("PDB", "ihm_ligand_probe").annotations.update({"tag:misd.isi.edu,2015:display": {"name": "Non-polymeric Entities used as Probes"}})
    model.table("PDB", "ihm_geometric_object_list").annotations.update({"tag:misd.isi.edu,2015:display": {"name": "Geometric Objects used as Restraints"}})
    model.table("PDB", "ihm_geometric_object_center").annotations.update({"tag:misd.isi.edu,2015:display": {"name": "Centers of Geometric Objects"}})
    model.table("PDB", "ihm_geometric_object_transformation").annotations.update({"tag:misd.isi.edu,2015:display": {"name": "Transformations Applied to Geometric Objects"}})
    model.table("PDB", "ihm_geometric_object_sphere").annotations.update({"tag:misd.isi.edu,2015:display": {"name": "Spherical Geometric Objects"}})
    model.table("PDB", "ihm_geometric_object_torus").annotations.update({"tag:misd.isi.edu,2015:display": {"name": "Torus Geometric Objects"}})
    model.table("PDB", "ihm_geometric_object_half_torus").annotations.update({"tag:misd.isi.edu,2015:display": {"name": "Half-torus Geometric Objects"}})
    model.table("PDB", "ihm_geometric_object_plane").annotations.update({"tag:misd.isi.edu,2015:display": {"name": "Plane Geometric Objects"}})
    model.table("PDB", "ihm_geometric_object_axis").annotations.update({"tag:misd.isi.edu,2015:display": {"name": "Axis Geomtric Objects"}})
    model.table("PDB", "Entry_Related_File").annotations.update({"tag:misd.isi.edu,2015:display": {"name": "Uploaded Restraint Files"}})
    model.table("PDB", "ihm_cross_link_list").annotations.update({"tag:misd.isi.edu,2015:display": {"name": "Chemical Crosslinks from Experiments"}})
    model.table("PDB", "ihm_cross_link_restraint").annotations.update({"tag:misd.isi.edu,2015:display": {"name": "Chemical Crosslinking Restraints Applied in the Modeling"}})
    model.table("PDB", "ihm_cross_link_result").annotations.update({"tag:misd.isi.edu,2015:display": {"name": "Chemical Crosslink Restraint Results"}})
    model.table("PDB", "ihm_cross_link_result_parameters").annotations.update({"tag:misd.isi.edu,2015:display": {"name": "Chemical Crosslink Restraint Result Parameters"}})
    model.table("PDB", "ihm_predicted_contact_restraint").annotations.update({"tag:misd.isi.edu,2015:display": {"name": "Predicted Contact Restraints"}})
    model.table("PDB", "ihm_hydroxyl_radical_fp_restraint").annotations.update({"tag:misd.isi.edu,2015:display": {"name": "Hydroxyl Radical Footprinting Restraints"}})
    model.table("PDB", "ihm_feature_list").annotations.update({"tag:misd.isi.edu,2015:display": {"name": "Molecular Features used in Generic Restraints"}})
    model.table("PDB", "ihm_poly_atom_feature").annotations.update({"tag:misd.isi.edu,2015:display": {"name": "Molecular Features Comprising of Polymeric Atoms"}})
    model.table("PDB", "ihm_poly_residue_feature").annotations.update({"tag:misd.isi.edu,2015:display": {"name": "Molecular Features Comprising of Polymeric Residues"}})
    model.table("PDB", "ihm_non_poly_feature").annotations.update({"tag:misd.isi.edu,2015:display": {"name": "Molecular Features Comprising of Non-polymeric Entities"}})
    model.table("PDB", "ihm_interface_residue_feature").annotations.update({"tag:misd.isi.edu,2015:display": {"name": "Molecular Features Comprising of Polymeric Residues at Interfaces"}})
    model.table("PDB", "ihm_pseudo_site_feature").annotations.update({"tag:misd.isi.edu,2015:display": {"name": "Molecular Features Comprising of Pseudo Sites"}})
    model.table("PDB", "ihm_derived_distance_restraint").annotations.update({"tag:misd.isi.edu,2015:display": {"name": "Generic Distance Restraints Between Molecular Features"}})
    model.table("PDB", "ihm_geometric_object_distance_restraint").annotations.update({"tag:misd.isi.edu,2015:display": {"name": "Distance Restraints between Geometric Objects and Molecular Features"}})
    model.table("PDB", "audit_conform").annotations.update({"tag:misd.isi.edu,2015:display": {"name": "Dictionary Versions Compliant with the Data"}})
    model.table("PDB", "chem_comp_atom").annotations.update({"tag:misd.isi.edu,2015:display": {"name": "Atoms in Chemical Components"}})
    model.table("PDB", "pdbx_entity_poly_na_type").annotations.update({"tag:misd.isi.edu,2015:display": {"name": "Types of Nucleic Acid Polymeric Entities"}})
    model.table("PDB", "pdbx_entry_details").annotations.update({"tag:misd.isi.edu,2015:display": {"name": "Additional Details about the Entry"}})
    model.table("PDB", "pdbx_inhibitor_info").annotations.update({"tag:misd.isi.edu,2015:display": {"name": "Details of Inhibitors in the Entry"}})
    model.table("PDB", "pdbx_ion_info").annotations.update({"tag:misd.isi.edu,2015:display": {"name": "Details of Ions in the Entry"}})
    model.table("PDB", "pdbx_protein_info").annotations.update({"tag:misd.isi.edu,2015:display": {"name": "Details of Proteins in the Entry"}})

def column_annotations(model):
    
    model.table("PDB", "Entry_mmCIF_File").column_definitions["mmCIF_Schema_Version"].annotations.update({"tag:misd.isi.edu,2015:display": {"name": "mmCIF Schema Version"}})

# ===================================================
# -- this function will be called from the update_schemas.py file

def set_annotations(model):
    table_annotations(model)
    column_annotations(model)


# ===================================================    
def main(server_name, catalog_id, credentials):
    server = DerivaServer('https', server_name, credentials)
    catalog = server.connect_ermrest(catalog_id)
    catalog.dcctx['cid'] = "oneoff/model"
    model = catalog.getCatalogModel()

    set_annotations(model)

    # let's the library deals with applying the difference
    model.apply()

# ===================================================    

if __name__ == '__main__':
    args = BaseCLI("ad-hoc table creation tool", None, 1).parse_cli()
    credentials = get_credential(args.host, args.credential_file)
#    if args.catalog is None:
#        catalog_id = 99

    main(args.host, 99, credentials)
    
    
