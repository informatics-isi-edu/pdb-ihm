from deriva.core import DerivaServer, get_credential, BaseCLI
from deriva.core.ermrest_model import Table, Column, Key, ForeignKey, builtin_types

def table_comments(model):
    #table = model.table("PDB", "software")
    #table.comment = "List of software used in the modeling"
    #table.column_definitions["Species_Tested_In"].comment = None

    model.table("PDB", "software").comment = "List of software used in the modeling"
    model.table("PDB", "citation_author").comment = "Authors associated with citations in the citation list"
    model.table("PDB", "chem_comp").comment = "Chemical components including monomers and ligands"
    model.table("PDB", "chem_comp_atom").comment = "Details of atoms in chemical components"
    model.table("PDB", "entity_poly_seq").comment = "Sequence of monomers in polymeric entities"
    model.table("PDB", "entity_src_gen").comment = "Details of the source from which genetically manipulated entities are obtained"
    model.table("PDB", "entity_name_com").comment = "Common names associated with the entities"
    model.table("PDB", "struct_asym").comment = "Instances of entities, both polymeric and non-polymeric"
    model.table("PDB", "atom_type").comment = "Types of atoms in the structure"
    model.table("PDB", "entity").comment = "Details of molecular entities in the structure"
    model.table("PDB", "entity_poly").comment = "Details of polymeric entities"
    model.table("PDB", "entity_name_sys").comment = "Systematic names associated with the entities"
    model.table("PDB", "pdbx_entity_nonpoly").comment = "Details of non-polymeric entities"
    model.table("PDB", "ihm_struct_assembly_details").comment = "Details of structural assemblies in the models submitted"
    model.table("PDB", "ihm_model_representation").comment = "List of model representations used"
    model.table("PDB", "ihm_struct_assembly").comment = "List of structure assemblies in the models submitted"
    model.table("PDB", "ihm_model_representation_details").comment = "Details of model representations used; addresses representations of multi-scale models with atomic and coarse-grained representations"
    model.table("PDB", "ihm_entity_poly_segment").comment = "Segments of polymeric entities; specifies sequence ranges for use in other tables"
    model.table("PDB", "ihm_struct_assembly_class").comment = "List of structural assembly classes; allows for defining hierarchical structural assemblies"
    model.table("PDB", "ihm_struct_assembly_class_link").comment = "Table to link structural assemblies to the assembly classes"
    model.table("PDB", "Entry_Related_File").comment = "Restraint data files (in csv/tsv format) related to the entry"
    model.table("PDB", "Entry_mmCIF_File").comment = "Details of the mmCIF file generated based on all the data provided by the user"
    model.table("PDB", "ihm_dataset_group_link").comment = "Table to link input datasets with the dataset groups"
    model.table("PDB", "ihm_cross_link_restraint").comment = "Chemical crosslinking restraints used in the modeling"
    model.table("PDB", "ihm_poly_atom_feature").comment = "Details of atomic features in polymeric entities"
    model.table("PDB", "ihm_modeling_protocol").comment = "List of modeling protocols used in the integrative modeling study"
    model.table("PDB", "ihm_modeling_protocol_details").comment = "Details of the modeling protocols used in the integrative modeling study"
    model.table("PDB", "ihm_modeling_post_process").comment = "Post processing of the resulting models from the modeling protocols"
    model.table("PDB", "ihm_model_group").comment = "Collections or groups of models that can be used for defining clusters, multi-state models or ordered ensembles"
    model.table("PDB", "ihm_model_group_link").comment = "List of models belonging to a model group"
    model.table("PDB", "ihm_cross_link_result").comment = "Results of crosslinking restraints used in integrative modeling"
    model.table("PDB", "ihm_multi_state_model_group_link").comment = "List of model groups belonging to a particular state"
    model.table("PDB", "ihm_starting_model_details").comment = "Information regarding starting structural models used in the integrative modeling study"
    model.table("PDB", "ihm_starting_comparative_models").comment = "Additional information regarding comparative models used as starting structural models"
    model.table("PDB", "ihm_starting_computational_models").comment = "Generic information regarding all computational models used as starting structural models"
    model.table("PDB", "ihm_starting_model_seq_dif").comment = "Information regarding point mutations in the sequences of the starting models compared to the starting model in the reference database"
    

def column_comments(model):
    
    model.table("PDB", "software").column_definitions["citation_id"].comment = "Citation corresponding to the software; a reference to the citation id in the citation table"
    model.table("PDB", "Entry_Related_File").column_definitions["File_Type"].comment = "Restraint table corresponding to the uploaded file"
    model.table("PDB", "Entry_Related_File").column_definitions["File_Format"].comment = "CSV or TSV file format"
    #model.table("PDB", "Entry_Related_File").column_definitions["File_Url"].comment = "URL of the uploaded file"
    model.table("PDB", "Entry_Related_File").column_definitions["Description"].comment = "Description of the file"
    model.table("PDB", "Entry_Related_File").column_definitions["Workflow_Status"].comment = "Workflow status corresponding to uploading restraint data files"
    model.table("PDB", "Entry_Related_File").column_definitions["Record_Status_Detail"].comment = "Captures error messages obtained while processing the uploaded restraint data files; remains empty if process is success"
    model.table("PDB", "Entry_Related_File").column_definitions["File_Bytes"].comment = "Size of the uploaded file in bytes"
    #model.table("PDB", "Entry_Related_File").column_definitions["File_Md5"].comment = "MD5 value of uploaded file"
    #model.table("PDB", "Entry_Related_File").column_definitions["Structure_Id"].comment = "A reference to the entry.id identifier in the entry table"
    #model.table("PDB", "Entry").column_definitions["Image_File_Url"].comment = "URL of the uploaded image file"
    #model.table("PDB", "Entry").column_definitions["Image_File_Size"].comment = "Size of the uploaded image file in bytes"
    #model.table("PDB", "Entry").column_definitions["mmCIF_File_Url"].comment = "URL of the uploaded mmCIF file"
    #model.table("PDB", "Entry").column_definitions["mmCIF_File_Size"].comment = "Size of the uploaded mmCIF file in bytes"
    #model.table("PDB", "Entry").column_definitions["Workflow_Status"].comment = "Workflow status corresponding to the entry"
    #model.table("PDB", "Entry").column_definitions["Accession_Code"].comment = "Accession code issued by the archive after processing the entry"
    #model.table("PDB", "Entry").column_definitions["Record_Status_Detail"].comment = "Captures error messages obtained while processing the uploaded mmCIF files; remain empty if process is success"
    #model.table("PDB", "Entry").column_definitions["Generated_mmCIF_Processing_Status"].comment = "Indicates whether the status of processing the uploaded mmCIF file is success or failure"
    #model.table("PDB", "Entry_mmCIF_File").column_definitions["File_Url"].comment = "URL of the system generated mmCIF file"
    model.table("PDB", "Entry_mmCIF_File").column_definitions["mmCIF_Schema_Version"].comment = "Schema version of mmCIF IHM extension dictionary"
    model.table("PDB", "Entry_mmCIF_File").column_definitions["Structure_Id"].comment = "A reference to the entry.id identifier in the entry table"
    model.table("PDB", "Entry_mmCIF_File").column_definitions["File_Bytes"].comment = "Size of the system generated mmCIF file in bytes"
    #model.table("PDB", "Entry_mmCIF_File").column_definitions["File_Md5"].comment = "MD5 value of the system generated mmCIF file"

# ===================================================
# -- this function will be called from the update_schemas.py file

def set_comments(model):
    table_comments(model)
    column_comments(model)


# ===================================================    
def main(server_name, catalog_id, credentials):
    server = DerivaServer('https', server_name, credentials)
    catalog = server.connect_ermrest(catalog_id)
    catalog.dcctx['cid'] = "oneoff/model"
    model = catalog.getCatalogModel()

    set_comments(model)

    # let's the library deals with applying the difference
    model.apply()

# ===================================================    

if __name__ == '__main__':
    args = BaseCLI("ad-hoc table creation tool", None, 1).parse_cli()
    credentials = get_credential(args.host, args.credential_file)
#    if args.catalog is None:
#        catalog_id = 99

    main(args.host, 99, credentials)
    
    
