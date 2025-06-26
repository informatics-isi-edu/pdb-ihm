import sys
import json
from deriva.core import ErmrestCatalog, AttrDict, get_credential, DEFAULT_CREDENTIAL_FILE, tag, urlquote, DerivaServer, get_credential, BaseCLI
from deriva.core.ermrest_model import builtin_types, Schema, Table, Column, Key, ForeignKey, tag, AttrDict
from deriva.core import urlquote, urlunquote
import requests.exceptions
from ...utils.shared import DCCTX, PDBDEV_CLI, cfg
from deriva.utils.extras.model import get_schemas, get_tables, get_columns, print_catalog_model_extras, print_presence_tag_annotations, clear_catalog_annotations, tag2name
from . import bulk_upload
from ..acl.ermrest_acl import GROUPS, initialize_policies

catalog_wide_annotation_tags = [tag["generated"], tag["immutable"], tag["non_deletable"], tag["required"]]
catalog_specific_annotation_tags = [tag["chaise_config"], tag["bulk_upload"], tag["column_defaults"], tag["display"]]

# -- =================================================================================
# -- chaise config.. Assuming that navbar is set through chaise-config
# chaise-config params: https://github.com/informatics-isi-edu/chaise/blob/master/docs/user-docs/chaise-config.md#internalhosts
def get_chaise_config(catalog_id):
    config = {
        "defaultCatalog": catalog_id,
        "resolverImplicitCatalog": catalog_id,        
        "customCSS": '/assets/css/chaise.css',
        "allowErrorDismissal": True,
        "confirmDelete": True,
	"deleteRecord": True,
	"editRecord": True,
        "maxRecordsetRowHeight": 235,
        #"footerMarkdown": "[* Privacy policy](/privacy-policy){target='_blank'}",
        "exportServicePath": "/deriva/export",
        "SystemColumnsDisplayCompact": ["RID"],
        "SystemColumnsDisplayDetailed": ["RID", "RCT", "RMT"],
        "SystemColumnsDisplayEntry": [],
        "navbarBrand": "/",
        "headTitle": "PDB-IHM",
        "navbarBrandText": "PDB-IHM",
	"signUpURL": "https://app.globus.org/groups/99da042e-64a6-11ea-ad5f-0ef992ed7ca1/about",
        #"disableExternalLinkModal": True, # check this?
	#"internaleHosts": ["github.com"],
        "templating": {
            "engine": "handlebars",
            "site_var": {
                "acl_groups": {
                    "entry_submitters": ["https://auth.globus.org/99da042e-64a6-11ea-ad5f-0ef992ed7ca1"],
                    "entry_updaters": ["https://auth.globus.org/eef3e02a-3c40-11e9-9276-0edc9bdd56a6", "https://auth.globus.org/0b98092c-3c41-11e9-a8c8-0ee7d80087ee", "https://auth.globus.org/3938e0d0-ed35-11e5-8641-22000ab4b42b"], # pdb-curators, pdb-admins, isrd-systems
                }  
            },
        }
    }
    
    config.update(get_navbar_menu(catalog_id))        

    if cfg.is_dev == True:
        config["navbarBrandText"] = "%s (Dev)" % (config["navbarBrandText"])
    elif cfg.is_staging == True:
        config["navbarBrandText"] = "%s (Test)" % (config["navbarBrandText"])

    #print("%s\n" % (json.dumps(config, indent=2)))    
    return config

# -- ----------------------------------------------------------------------    
def get_navbar_menu(catalog_id):
    navbar = {
        "navbarMenu": {
            "newTab": False,
            "children": [
	        {
	            "name": "Entry",
	            "url": "/chaise/recordset/#"+catalog_id+"/PDB:entry"
	        },
                { 
                    "name": "Data Categories", 
                    "children": [
                        { 
                            "name": "2DEM",
                            "children": [
                                { "name": "Ihm 2DEM Class Average Fitting", "url": "/chaise/recordset/#"+catalog_id+"/PDB:ihm_2dem_class_average_fitting" },
                                { "name": "Ihm 2DEM Class Average Restraint", "url": "/chaise/recordset/#"+catalog_id+"/PDB:ihm_2dem_class_average_restraint" }
                            ],
                        },
                        {
                            "name": "3DEM",
                            "children": [
                                { "name": "Ihm 3DEM Restraint", "url": "/chaise/recordset/#"+catalog_id+"/PDB:ihm_3dem_restraint" }
                            ],
                        },
                        {
                            "name": "Audit Conform",
                            "children": [
                                { "name": "Audit Conform", "url": "/chaise/recordset/#"+catalog_id+"/PDB:audit_conform" }
                            ],
                        },
                        { #3
                            "name": "Chemical Components",                            
                            "children": [
                                { "name": "Chem Comp", "url": "/chaise/recordset/#"+catalog_id+"/PDB:chem_comp" },
                                { "name": "Chem Comp Atom", "url": "/chaise/recordset/#"+catalog_id+"/PDB:chem_comp_atom" }
                            ],
                        },
                        {
                            "name": "Chemical Crosslinks",                            
                            "children": [
                                { "name": "Ihm Cross Link List", "url": "/chaise/recordset/#"+catalog_id+"/PDB:ihm_cross_link_list" },
                                { "name": "Ihm Cross Link Restraint", "url": "/chaise/recordset/#"+catalog_id+"/PDB:ihm_cross_link_restraint" },
                                { "name": "Ihm Cross Link Result", "url": "/chaise/recordset/#"+catalog_id+"/PDB:ihm_cross_link_result" },
                                { "name": "Ihm Cross Link Result Parameters", "url": "/chaise/recordset/#"+catalog_id+"/PDB:ihm_cross_link_result_parameters" }
                            ],
                        },
                        {
                            "name": "Citation, Authors and Software",
                            "children": [
                                { "name": "Audit Author", "url": "/chaise/recordset/#"+catalog_id+"/PDB:audit_author" },
                                { "name": "Citation", "url": "/chaise/recordset/#"+catalog_id+"/PDB:citation" },
                                { "name": "Citation Author", "url": "/chaise/recordset/#"+catalog_id+"/PDB:citation_author" },
                                { "name": "Software", "url": "/chaise/recordset/#"+catalog_id+"/PDB:software" }
                            ],
                        },
                        {
                            "name": "Dictionaries",
                            "children": [
                                { "name": "Data Dictionary", "url": "/chaise/recordset/#"+catalog_id+"/PDB:Data_Dictionary" },
                                { "name": "Supported Dictionary", "url": "/chaise/recordset/#"+catalog_id+"/PDB:Supported_Dictionary" }
                            ],
                        },
                        {
                            "name": "Entry and Structure",
                            "children": [
                                { "name": "Entry", "url": "/chaise/recordset/#"+catalog_id+"/PDB:entry" },
                                {"name": "Struct", "url": "/chaise/recordset/#"+catalog_id+"/PDB:struct" }
                            ],
                        },
                        {
                            "name": "EPR",
                            "children": [
                                { "name": "Ihm EPR Restraint", "url": "/chaise/recordset/#"+catalog_id+"/PDB:ihm_epr_restraint" }
                            ],
                        },
                        {
                            "name": "Generic Distance Restraints",
                            "children": [
                                { "name": "Ihm Derived Distance Restraint", "url": "/chaise/recordset/#"+catalog_id+"/PDB:ihm_derived_distance_restraint" },
                                { "name": "Ihm Feature List", "url": "/chaise/recordset/#"+catalog_id+"/PDB:ihm_feature_list" },
                                { "name": "Ihm Interface Residue Feature", "url": "/chaise/recordset/#"+catalog_id+"/PDB:ihm_interface_residue_feature" },
                                { "name": "Ihm Non Poly Feature", "url": "/chaise/recordset/#"+catalog_id+"/PDB:ihm_non_poly_feature" },
                                { "name": "Ihm Poly Atom Feature", "url": "/chaise/recordset/#"+catalog_id+"/PDB:ihm_poly_atom_feature" },
                                { "name": "Ihm Poly Residue Feature", "url": "/chaise/recordset/#"+catalog_id+"/PDB:ihm_poly_residue_feature" },
                                { "name": "Ihm Pseudo Site Feature", "url": "/chaise/recordset/#"+catalog_id+"/PDB:ihm_pseudo_site_feature" }
                            ],
                        },
                        {
                            "name": "Geometric Objects",
                            "children": [
                                {
                                    "name": "Ihm Geometric Object Axis",
                                    "url": "/chaise/recordset/#"+catalog_id+"/PDB:ihm_geometric_object_axis"
                                },
                                {
                                    "name": "Ihm Geometric Object Center",
                                    "url": "/chaise/recordset/#"+catalog_id+"/PDB:ihm_geometric_object_center"
                                },
                                {
                                    "name": "Ihm Geometric Object Distance Restraint",
                                    "url": "/chaise/recordset/#"+catalog_id+"/PDB:ihm_geometric_object_distance_restraint"
                                },
                                {
                                    "name": "Ihm Geometric Object Half Torus",
                                    "url": "/chaise/recordset/#"+catalog_id+"/PDB:ihm_geometric_object_half_torus"
                                },
                                {
                                    "name": "Ihm Geometric Object List",
                                    "url": "/chaise/recordset/#"+catalog_id+"/PDB:ihm_geometric_object_list"
                                },
                                {
                                    "name": "Ihm Geometric Object Plane",
                                    "url": "/chaise/recordset/#"+catalog_id+"/PDB:ihm_geometric_object_plane"
                                },
                                {
                                    "name": "Ihm Geometric Object Sphere",
                                    "url": "/chaise/recordset/#"+catalog_id+"/PDB:ihm_geometric_object_sphere"
                                },
                                {
                                    "name": "Ihm Geometric Object Torus",
                                    "url": "/chaise/recordset/#"+catalog_id+"/PDB:ihm_geometric_object_torus"
                                },
                                {
                                    "name": "Ihm Geometric Object Transformation",
                                    "url": "/chaise/recordset/#"+catalog_id+"/PDB:ihm_geometric_object_transformation"
                                }
                            ],
                        },
                        {
                            "name": "Hydroxyl Radical Foot Printing",
                            "children": [
                                { "name": "Ihm Hydroxyl Radical Fp Restraint", "url": "/chaise/recordset/#"+catalog_id+"/PDB:ihm_hydroxyl_radical_fp_restraint" }
                            ],
                        },
                        {
                            "name": "Input Data",
                            "children": [
                                { "name": "Ihm Dataset External Reference", "url": "/chaise/recordset/#"+catalog_id+"/PDB:ihm_dataset_external_reference" },
                                { "name": "Ihm Dataset Group", "url": "/chaise/recordset/#"+catalog_id+"/PDB:ihm_dataset_group" },
                                { "name": "Ihm Dataset Group Link", "url": "/chaise/recordset/#"+catalog_id+"/PDB:ihm_dataset_group_link" },
                                { "name": "Ihm Dataset List", "url": "/chaise/recordset/#"+catalog_id+"/PDB:ihm_dataset_list" },
                                { "name": "Ihm Dataset Related Db Reference", "url": "/chaise/recordset/#"+catalog_id+"/PDB:ihm_dataset_related_db_reference" },
                                { "name": "Ihm External Files", "url": "/chaise/recordset/#"+catalog_id+"/PDB:ihm_external_files" },
                                { "name": "Ihm External Reference Info", "url": "/chaise/recordset/#"+catalog_id+"/PDB:ihm_external_reference_info" },
                                { "name": "Ihm Related Datasets", "url": "/chaise/recordset/#"+catalog_id+"/PDB:ihm_related_datasets" }
                            ],
                        },
                        {
                            "name": "Localization Densities",
                            "children": [
                                { "name": "Ihm Localization Density Files", "url": "/chaise/recordset/#"+catalog_id+"/PDB:ihm_localization_density_files" }
                            ],
                        },
                        {
                            "name": "Model List",
                            "children": [
                                {
                                    "name": "Ihm Model Group",
                                    "url": "/chaise/recordset/#"+catalog_id+"/PDB:ihm_model_group"
                                },
                                {
                                    "name": "Ihm Model Group Link",
                                    "url": "/chaise/recordset/#"+catalog_id+"/PDB:ihm_model_group_link"
                                },
                                {
                                    "name": "Ihm Model List",
                                    "url": "/chaise/recordset/#"+catalog_id+"/PDB:ihm_model_list"
                                },
                                {
                                    "name": "Ihm Model Representative",
                                    "url": "/chaise/recordset/#"+catalog_id+"/PDB:ihm_model_representative"
                                },
                                {
                                    "name": "Ihm Residues Not Modeled",
                                    "url": "/chaise/recordset/#"+catalog_id+"/PDB:ihm_residues_not_modeled"
                                }
                            ],
                        },
                        {
                            "name": "Model Representation",
                            "children": [
                                {
                                    "name": "Ihm Model Representation",
                                    "url": "/chaise/recordset/#"+catalog_id+"/PDB:ihm_model_representation"
                                },
                                {
                                    "name": "Ihm Model Representation Details",
                                    "url": "/chaise/recordset/#"+catalog_id+"/PDB:ihm_model_representation_details"
                                }
                            ],
                        },
                        {
                            "name": "Modeling Protocol",
                            "children": [
                                {
                                    "name": "Ihm Modeling Post Process",
                                    "url": "/chaise/recordset/#"+catalog_id+"/PDB:ihm_modeling_post_process"
                                },
                                {
                                    "name": "Ihm Modeling Protocol",
                                    "url": "/chaise/recordset/#"+catalog_id+"/PDB:ihm_modeling_protocol"
                                },
                                {
                                    "name": "Ihm Modeling Protocol Details",
                                    "url": "/chaise/recordset/#"+catalog_id+"/PDB:ihm_modeling_protocol_details"
                                }
                            ],
                        },
                        {
                            "name": "Molecular Entities, Instances and Segments",
                            "children": [
                                {
                                    "name": "Atom Type",
                                    "url": "/chaise/recordset/#"+catalog_id+"/PDB:atom_type"
                                },
                                {
                                    "name": "Entity",
                                    "url": "/chaise/recordset/#"+catalog_id+"/PDB:entity"
                                },
                                {
                                    "name": "Entity Name Com",
                                    "url": "/chaise/recordset/#"+catalog_id+"/PDB:entity_name_com"
                                },
                                {
                                    "name": "Entity Name Sys",
                                    "url": "/chaise/recordset/#"+catalog_id+"/PDB:entity_name_sys"
                                },
                                {
                                    "name": "Entity Poly",
                                    "url": "/chaise/recordset/#"+catalog_id+"/PDB:entity_poly"
                                },
                                {
                                    "name": "Entity Poly Seq",
                                    "url": "/chaise/recordset/#"+catalog_id+"/PDB:entity_poly_seq"
                                },
                                {
                                    "name": "Entity Src Gen",
                                    "url": "/chaise/recordset/#"+catalog_id+"/PDB:entity_src_gen"
                                },
                                {
                                    "name": "Ihm Entity Poly Segment",
                                    "url": "/chaise/recordset/#"+catalog_id+"/PDB:ihm_entity_poly_segment"
                                },
                                {
                                    "name": "PDBX Entity Nonpoly",
                                    "url": "/chaise/recordset/#"+catalog_id+"/PDB:pdbx_entity_nonpoly"
                                },
                                {
                                    "name": "Struct Asym",
                                    "url": "/chaise/recordset/#"+catalog_id+"/PDB:struct_asym"
                                }
                            ],
                        },
                        {
                            "name": "Multi-state Modeling, Ordered Models, and Ensembles",
                            "children": [
                                {
                                    "name": "Ihm Ensemble Info",
                                    "url": "/chaise/recordset/#"+catalog_id+"/PDB:ihm_ensemble_info"
                                },
                                {
                                    "name": "Ihm Multi State Model Group Link",
                                    "url": "/chaise/recordset/#"+catalog_id+"/PDB:ihm_multi_state_model_group_link"
                                },
                                {
                                    "name": "Ihm Multi State Modeling",
                                    "url": "/chaise/recordset/#"+catalog_id+"/PDB:ihm_multi_state_modeling"
                                },
                                {
                                    "name": "Ihm Ordered Model",
                                    "url": "/chaise/recordset/#"+catalog_id+"/PDB:ihm_ordered_model"
                                }
                            ],
                        },
                        {
                            "name": "Multi-State Schemes",
                            "children": [
                                {
                                    "name": "ihm Multi-State Scheme",
                                    "url": "/chaise/recordset/#"+catalog_id+"/PDB:ihm_multi_state_scheme"
                                },
                                {
                                    "name": "ihm Multi-State Scheme Connectivity",
                                    "url": "/chaise/recordset/#"+catalog_id+"/PDB:ihm_multi_state_scheme_connectivity"
                                },
                                {
                                    "name": "ihm Kinetic Rate",
                                    "url": "/chaise/recordset/#"+catalog_id+"/PDB:ihm_kinetic_rate"
                                },
                                {
                                    "name": "ihm Relaxation Time",
                                    "url": "/chaise/recordset/#"+catalog_id+"/PDB:ihm_relaxation_time"
                                },
                                {
                                    "name": "ihm Relaxation Time Multi-State Scheme",
                                    "url": "/chaise/recordset/#"+catalog_id+"/PDB:ihm_relaxation_time_multi_state_scheme"
                                }
                            ],
                        },
                        {
                            "name": "Predicted Contacts",
                            "children": [
                                {
                                    "name": "Ihm Predicted Contact Restraint",
                                    "url": "/chaise/recordset/#"+catalog_id+"/PDB:ihm_predicted_contact_restraint"
                                }
                            ],
                        },
                        {
                            "name": "Probe Labeling Information",
                            "children": [
                                {
                                    "name": "Ihm Chemical Component Descriptor",
                                    "url": "/chaise/recordset/#"+catalog_id+"/PDB:ihm_chemical_component_descriptor"
                                },
                                {
                                    "name": "Ihm Ligand Probe",
                                    "url": "/chaise/recordset/#"+catalog_id+"/PDB:ihm_ligand_probe"
                                },
                                {
                                    "name": "Ihm Poly Probe Conjugate",
                                    "url": "/chaise/recordset/#"+catalog_id+"/PDB:ihm_poly_probe_conjugate"
                                },
                                {
                                    "name": "Ihm Poly Probe Position",
                                    "url": "/chaise/recordset/#"+catalog_id+"/PDB:ihm_poly_probe_position"
                                },
                                {
                                    "name": "Ihm Probe List",
                                    "url": "/chaise/recordset/#"+catalog_id+"/PDB:ihm_probe_list"
                                }
                            ],
                        },
                        {
                            "name": "SAS",
                            "children": [
                                {
                                    "name": "Ihm SAS Restraint",
                                    "url": "/chaise/recordset/#"+catalog_id+"/PDB:ihm_sas_restraint"
                                }
                            ],
                        },
                        {
                            "name": "Starting Models",
                            "children": [
                                {
                                    "name": "Ihm Starting Comparative Models",
                                    "url": "/chaise/recordset/#"+catalog_id+"/PDB:ihm_starting_comparative_models"
                                },
                                {
                                    "name": "Ihm Starting Computational Models",
                                    "url": "/chaise/recordset/#"+catalog_id+"/PDB:ihm_starting_computational_models"
                                },
                                {
                                    "name": "Ihm Starting Model Details",
                                    "url": "/chaise/recordset/#"+catalog_id+"/PDB:ihm_starting_model_details"
                                },
                                {
                                    "name": "Ihm Starting Model Seq Dif",
                                    "url": "/chaise/recordset/#"+catalog_id+"/PDB:ihm_starting_model_seq_dif"
                                }
                            ],
                        },
                        {
                            "name": "Structure Assembly",
                            "children": [
                                {
                                    "name": "Ihm Struct Assembly",
                                    "url": "/chaise/recordset/#"+catalog_id+"/PDB:ihm_struct_assembly"
                                },
                                {
                                    "name": "Ihm Struct Assembly Class",
                                    "url": "/chaise/recordset/#"+catalog_id+"/PDB:ihm_struct_assembly_class"
                                },
                                {
                                    "name": "Ihm Struct Assembly Class Link",
                                    "url": "/chaise/recordset/#"+catalog_id+"/PDB:ihm_struct_assembly_class_link"
                                },
                                {
                                    "name": "Ihm Struct Assembly Details",
                                    "url": "/chaise/recordset/#"+catalog_id+"/PDB:ihm_struct_assembly_details"
                                }
                            ],
                        },
                        {
                            "name": "Workflow",
                            "children": [
                                {
                                    "name": "Accession Code",
                                    "url": "/chaise/recordset/#"+catalog_id+"/PDB:Accession_Code"
                                },
                                {
                                    "name": "Curation Log",
                                    "url": "/chaise/recordset/#"+catalog_id+"/PDB:Curation_Log"
                                },
                                {
                                    "name": "Entry Error File",
                                    "url": "/chaise/recordset/#"+catalog_id+"/PDB:Entry_Error_File"
                                },
                                {
                                    "name": "Entry Generated File",
                                    "url": "/chaise/recordset/#"+catalog_id+"/PDB:Entry_Generated_File"
                                },
                                {
                                    "name": "Entry Related File",
                                    "url": "/chaise/recordset/#"+catalog_id+"/PDB:Entry_Related_File"
                                }
                            ],
                        },
                        {
                            "name": "Entry Collection",
                            "children": [
                                {
                                    "name": "Entry Collection",
                                    "url": "/chaise/recordset/#"+catalog_id+"/PDB:ihm_entry_collection"
                                },
                                {
                                    "name": "Entry Collection Mapping",
                                    "url": "/chaise/recordset/#"+catalog_id+"/PDB:ihm_entry_collection_mapping"
                                }
                            ],
                        },
                        {
                            "name": "Archive",
                            "children": [
                                {
                                    "name": "PDB Archive",
                                    "url": "/chaise/recordset/#"+catalog_id+"/PDB:PDB_Archive"
                                },
                                {
                                    "name": "Entry Latest Archive",
                                    "url": "/chaise/recordset/#"+catalog_id+"/PDB:Entry_Latest_Archive"
                                }
                            ],
                        }
                    ],
                },
                {
                    "name": "Vocabulary",
                    "acls": { "show": GROUPS["owners"] + GROUPS["entry-updaters"], "enable": GROUPS["owners"] + GROUPS["entry-updaters"] },
                    #"acls": {
	            #    "show": ["https://auth.globus.org/0b98092c-3c41-11e9-a8c8-0ee7d80087ee", "https://auth.globus.org/eef3e02a-3c40-11e9-9276-0edc9bdd56a6"],
	            #    "enable": ["https://auth.globus.org/0b98092c-3c41-11e9-a8c8-0ee7d80087ee", "https://auth.globus.org/eef3e02a-3c40-11e9-9276-0edc9bdd56a6"]
                    #},
                    "children": [
                        {
                            "name": "Chem Comp",
                            "children": [
                                { "name": "Mon Nstd Flag", "url": "/chaise/recordset/#"+catalog_id+"/Vocab:chem_comp_mon_nstd_flag" },
                                { "name": "PDBX  Aromatic Flag", "url": "/chaise/recordset/#"+catalog_id+"/Vocab:chem_comp_atom_pdbx_aromatic_flag" },
                                { "name": "PDBX  Leaving Atom Flag", "url": "/chaise/recordset/#"+catalog_id+"/Vocab:chem_comp_atom_pdbx_leaving_atom_flag" },
                                { "name": "PDBX  Polymer Type", "url": "/chaise/recordset/#"+catalog_id+"/Vocab:chem_comp_atom_pdbx_polymer_type" },
                                { "name": "PDBX  Stereo Config", "url": "/chaise/recordset/#"+catalog_id+"/Vocab:chem_comp_atom_pdbx_stereo_config" },
                                { "name": "Substruct Code", "url": "/chaise/recordset/#"+catalog_id+"/Vocab:chem_comp_atom_substruct_code" },
                                { "name": "Type", "url": "/chaise/recordset/#"+catalog_id+"/Vocab:chem_comp_type" }
                            ],
                        },
                        {
                            "name": "Data Dictionaries",
                            "children": [
                                { "name": "Names", "url": "/chaise/recordset/#"+catalog_id+"/Vocab:Data_Dictionary_Name" },
                                { "name": "Categories", "url": "/chaise/recordset/#"+catalog_id+"/Vocab:Data_Dictionary_Category" }
                            ],
                        },
                        {
                            "name": "Entity",
                            "children": [
                                {
                                    "name": "Hetero",
                                    "url": "/chaise/recordset/#"+catalog_id+"/Vocab:entity_poly_seq_hetero"
                                },
                                {
                                    "name": "Nstd Chirality",
                                    "url": "/chaise/recordset/#"+catalog_id+"/Vocab:entity_poly_nstd_chirality"
                                },
                                {
                                    "name": "Nstd Linkage",
                                    "url": "/chaise/recordset/#"+catalog_id+"/Vocab:entity_poly_nstd_linkage"
                                },
                                {
                                    "name": "Nstd Monomer",
                                    "url": "/chaise/recordset/#"+catalog_id+"/Vocab:entity_poly_nstd_monomer"
                                },
                                {
                                    "name": "PDBX  Alt Source Flag",
                                    "url": "/chaise/recordset/#"+catalog_id+"/Vocab:entity_src_gen_pdbx_alt_source_flag"
                                },
                                {
                                    "name": "PDBX  Sequence Evidence Code",
                                    "url": "/chaise/recordset/#"+catalog_id+"/Vocab:entity_poly_pdbx_sequence_evidence_code"
                                },
                                {
                                    "name": "Poly Type",
                                    "url": "/chaise/recordset/#"+catalog_id+"/Vocab:entity_poly_type"
                                },
                                {
                                    "name": "Src Method",
                                    "url": "/chaise/recordset/#"+catalog_id+"/Vocab:entity_src_method"
                                },
                                {
                                    "name": "Type",
                                    "url": "/chaise/recordset/#"+catalog_id+"/Vocab:entity_type"
                                }
                            ],
                        },
                        {
                            "name": "Ihm 2dem",
                            "children": [
                                {
                                    "name": "Image Segment Flag",
                                    "url": "/chaise/recordset/#"+catalog_id+"/Vocab:ihm_2dem_class_average_restraint_image_segment_flag"
                                }
                            ],
                        },
                        {
                            "name": "Ihm 3dem",
                            "children": [
                                {
                                    "name": "Map Segment Flag",
                                    "url": "/chaise/recordset/#"+catalog_id+"/Vocab:ihm_3dem_restraint_map_segment_flag"
                                }
                            ],
                        },
                        {
                            "name": "Ihm Cross Link",
                            "children": [
                                {
                                    "name": "Conditional Crosslink Flag",
                                    "url": "/chaise/recordset/#"+catalog_id+"/Vocab:ihm_cross_link_restraint_conditional_crosslink_flag"
                                },
                                {
                                    "name": "Linker Type",
                                    "url": "/chaise/recordset/#"+catalog_id+"/Vocab:ihm_cross_link_list_linker_type"
                                },
                                {
                                    "name": "Model Granularity",
                                    "url": "/chaise/recordset/#"+catalog_id+"/Vocab:ihm_cross_link_restraint_model_granularity"
                                },
                                {
                                    "name": "Restraint Type",
                                    "url": "/chaise/recordset/#"+catalog_id+"/Vocab:ihm_cross_link_restraint_restraint_type"
                                }
                            ],
                        },
                        {
                            "name": "Ihm Dataset",
                            "children": [
                                {
                                    "name": "Application",
                                    "url": "/chaise/recordset/#"+catalog_id+"/Vocab:ihm_dataset_group_application"
                                },
                                {
                                    "name": "Data Type",
                                    "url": "/chaise/recordset/#"+catalog_id+"/Vocab:ihm_dataset_list_data_type"
                                },
                                {
                                    "name": "Database Hosted",
                                    "url": "/chaise/recordset/#"+catalog_id+"/Vocab:ihm_dataset_list_database_hosted"
                                },
                                {
                                    "name": "Related DB Reference DB Name",
                                    "url": "/chaise/recordset/#"+catalog_id+"/Vocab:ihm_dataset_related_db_reference_db_name"
                                },
                                {
                                    "name": "Group Conditionality",
                                    "url": "/chaise/recordset/#"+catalog_id+"/Vocab:ihm_derived_distance_restraint_group_conditionality"
                                },
                                {
                                    "name": "Restraint Type",
                                    "url": "/chaise/recordset/#"+catalog_id+"/Vocab:ihm_derived_distance_restraint_restraint_type"
                                }
                            ],
                        },
                        {
                            "name": "Ihm Derived Distance Restraint",
                            "children": [
                                {
                                    "name": "Group Conditionality",
                                    "url": "/chaise/recordset/#"+catalog_id+"/Vocab:ihm_derived_distance_restraint_group_conditionality"
                                },
                                {
                                    "name": "Restraint Type",
                                    "url": "/chaise/recordset/#"+catalog_id+"/Vocab:ihm_derived_distance_restraint_restraint_type"
                                }
                            ],
                        },
                        {
                            "name": "Ihm Ensemble Info",
                            "children": [
                                {
                                    "name": "Ensemble Clustering Feature",
                                    "url": "/chaise/recordset/#"+catalog_id+"/Vocab:ihm_ensemble_info_ensemble_clustering_feature"
                                },
                                {
                                    "name": "Ensemble Clustering Method",
                                    "url": "/chaise/recordset/#"+catalog_id+"/Vocab:ihm_ensemble_info_ensemble_clustering_method"
                                }
                            ],
                        },
                        {
                            "name": "Ihm Epr Restraint",
                            "children": [
                                {
                                    "name": "Fitting State",
                                    "url": "/chaise/recordset/#"+catalog_id+"/Vocab:ihm_epr_restraint_fitting_state"
                                }
                            ],
                        },
                        {
                            "name": "Ihm External",
                            "children": [
                                {
                                    "name": "Content Type",
                                    "url": "/chaise/recordset/#"+catalog_id+"/Vocab:ihm_external_files_content_type"
                                },
                                {
                                    "name": "File Format",
                                    "url": "/chaise/recordset/#"+catalog_id+"/Vocab:ihm_external_files_file_format"
                                },
                                {
                                    "name": "Reference Type",
                                    "url": "/chaise/recordset/#"+catalog_id+"/Vocab:ihm_external_reference_info_reference_type"
                                },
                                {
                                    "name": "Refers To",
                                    "url": "/chaise/recordset/#"+catalog_id+"/Vocab:ihm_external_reference_info_refers_to"
                                }
                            ],
                        },
                        {
                            "name": "Ihm Feature List",
                            "children": [
                                {
                                    "name": "Entity Type",
                                    "url": "/chaise/recordset/#"+catalog_id+"/Vocab:ihm_feature_list_entity_type"
                                },
                                {
                                    "name": "Feature Type",
                                    "url": "/chaise/recordset/#"+catalog_id+"/Vocab:ihm_feature_list_feature_type"
                                }
                            ],
                        },
                        {
                            "name": "Ihm Geometric",
                            "children": [
                                {
                                    "name": "Axis Type",
                                    "url": "/chaise/recordset/#"+catalog_id+"/Vocab:ihm_geometric_object_axis_axis_type"
                                },
                                {
                                    "name": "Group Conditionality",
                                    "url": "/chaise/recordset/#"+catalog_id+"/Vocab:geometric_object_distance_restraint_group_condition"
                                },
                                {
                                    "name": "Object Characteristic",
                                    "url": "/chaise/recordset/#"+catalog_id+"/Vocab:geometric_object_distance_restraint_object_character"
                                },
                                {
                                    "name": "Object Type",
                                    "url": "/chaise/recordset/#"+catalog_id+"/Vocab:ihm_geometric_object_list_object_type"
                                },
                                {
                                    "name": "Plane Type",
                                    "url": "/chaise/recordset/#"+catalog_id+"/Vocab:ihm_geometric_object_plane_plane_type"
                                },
                                {
                                    "name": "Restraint Type",
                                    "url": "/chaise/recordset/#"+catalog_id+"/Vocab:ihm_geometric_object_distance_restraint_restraint_type"
                                },
                                {
                                    "name": "Section",
                                    "url": "/chaise/recordset/#"+catalog_id+"/Vocab:ihm_geometric_object_half_torus_section"
                                }
                            ],
                        },
                        {
                            "name": "Ihm Model",
                            "children": [
                                {
                                    "name": "Ensemble Flag",
                                    "url": "/chaise/recordset/#"+catalog_id+"/Vocab:ihm_modeling_protocol_details_ensemble_flag"
                                },
                                {
                                    "name": "Feature",
                                    "url": "/chaise/recordset/#"+catalog_id+"/Vocab:ihm_modeling_post_process_feature"
                                },
                                {
                                    "name": "Model Granularity",
                                    "url": "/chaise/recordset/#"+catalog_id+"/Vocab:ihm_model_representation_details_model_granularity"
                                },
                                {
                                    "name": "Model Mode",
                                    "url": "/chaise/recordset/#"+catalog_id+"/Vocab:ihm_model_representation_details_model_mode"
                                },
                                {
                                    "name": "Model Object Primitive",
                                    "url": "/chaise/recordset/#"+catalog_id+"/Vocab:model_representation_details_model_object_primitive"
                                },
                                {
                                    "name": "Multi Scale Flag",
                                    "url": "/chaise/recordset/#"+catalog_id+"/Vocab:ihm_modeling_protocol_details_multi_scale_flag"
                                },
                                {
                                    "name": "Ordered Flag",
                                    "url": "/chaise/recordset/#"+catalog_id+"/Vocab:ihm_modeling_protocol_details_ordered_flag"
                                },
                                {
                                    "name": "Selection Criteria",
                                    "url": "/chaise/recordset/#"+catalog_id+"/Vocab:ihm_model_representative_selection_criteria"
                                },
                                {
                                    "name": "Type",
                                    "url": "/chaise/recordset/#"+catalog_id+"/Vocab:ihm_modeling_post_process_type"
                                }
                            ],
                        },
                        {
                            "name": "Ihm Multi State Modeling",
                            "children": [
                                {
                                    "name": "Experiment Type",
                                    "url": "/chaise/recordset/#"+catalog_id+"/Vocab:ihm_multi_state_modeling_experiment_type"
                                },
                                {
                                    "name": "Relaxation Time Unit",
                                    "url": "/chaise/recordset/#"+catalog_id+"/Vocab:ihm_relaxation_time_unit"
                                },
                                {
                                    "name": "Equilibrium Constant Determination Methods",
                                    "url": "/chaise/recordset/#"+catalog_id+"/Vocab:ihm_equilibrium_constant_determination_method"
                                }
                            ],
                        },
                        {
                            "name": "Ihm Poly",
                            "children": [
                                {
                                    "name": "Ambiguous Stoichiometry Flag",
                                    "url": "/chaise/recordset/#"+catalog_id+"/Vocab:ihm_poly_probe_conjugate_ambiguous_stoichiometry_flag"
                                },
                                {
                                    "name": "Interface Residue Flag",
                                    "url": "/chaise/recordset/#"+catalog_id+"/Vocab:ihm_poly_residue_feature_interface_residue_flag"
                                },
                                {
                                    "name": "Modification Flag",
                                    "url": "/chaise/recordset/#"+catalog_id+"/Vocab:ihm_poly_probe_position_modification_flag"
                                },
                                {
                                    "name": "Mutation Flag",
                                    "url": "/chaise/recordset/#"+catalog_id+"/Vocab:ihm_poly_probe_position_mutation_flag"
                                },
                                {
                                    "name": "Rep Atom",
                                    "url": "/chaise/recordset/#"+catalog_id+"/Vocab:ihm_poly_residue_feature_rep_atom"
                                },
                                {
                                    "name": "Residue Range Granularity",
                                    "url": "/chaise/recordset/#"+catalog_id+"/Vocab:ihm_poly_residue_feature_residue_range_granularity"
                                }
                            ],
                        },
                        {
                            "name": "Ihm Predicted Contact Restraint",
                            "children": [
                                {
                                    "name": "Model Granularity",
                                    "url": "/chaise/recordset/#"+catalog_id+"/Vocab:ihm_predicted_contact_restraint_model_granularity"
                                },
                                {
                                    "name": "Rep Atom 1",
                                    "url": "/chaise/recordset/#"+catalog_id+"/Vocab:ihm_predicted_contact_restraint_rep_atom_1"
                                },
                                {
                                    "name": "Rep Atom 2",
                                    "url": "/chaise/recordset/#"+catalog_id+"/Vocab:ihm_predicted_contact_restraint_rep_atom_2"
                                },
                                {
                                    "name": "Restraint Type",
                                    "url": "/chaise/recordset/#"+catalog_id+"/Vocab:ihm_predicted_contact_restraint_restraint_type"
                                }
                            ],
                        },
                        {
                            "name": "Ihm Probe List",
                            "children": [
                                {
                                    "name": "Probe Link Type",
                                    "url": "/chaise/recordset/#"+catalog_id+"/Vocab:ihm_probe_list_probe_link_type"
                                },
                                {
                                    "name": "Probe Origin",
                                    "url": "/chaise/recordset/#"+catalog_id+"/Vocab:ihm_probe_list_probe_origin"
                                },
                                {
                                    "name": "Reactive Probe Flag",
                                    "url": "/chaise/recordset/#"+catalog_id+"/Vocab:ihm_probe_list_reactive_probe_flag"
                                }
                            ],
                        },
                        {
                            "name": "Ihm Residues Not Modeled",
                            "children": [
                                {
                                    "name": "Reason",
                                    "url": "/chaise/recordset/#"+catalog_id+"/Vocab:ihm_residues_not_modeled_reason"
                                }
                            ],
                        },
                        {
                            "name": "Ihm SAS Restraint",
                            "children": [
                                {
                                    "name": "Fitting State",
                                    "url": "/chaise/recordset/#"+catalog_id+"/Vocab:ihm_sas_restraint_fitting_state"
                                },
                                {
                                    "name": "Profile Segment Flag",
                                    "url": "/chaise/recordset/#"+catalog_id+"/Vocab:ihm_sas_restraint_profile_segment_flag"
                                }
                            ],
                        },
                        {
                            "name": "Ihm Starting",
                            "children": [
                                {
                                    "name": "Starting Model Source",
                                    "url": "/chaise/recordset/#"+catalog_id+"/Vocab:ihm_starting_model_details_starting_model_source"
                                },
                                {
                                    "name": "Template Sequence Identity Denominator",
                                    "url": "/chaise/recordset/#"+catalog_id+"/Vocab:starting_comparative_models_template_sequence_id_denom"
                                }
                            ],
                        },
                        {
                            "name": "Ihm Struct Assembly Class",
                            "children": [
                                {
                                    "name": "Type",
                                    "url": "/chaise/recordset/#"+catalog_id+"/Vocab:ihm_struct_assembly_class_type"
                                }
                            ],
                        },
                        {
                            "name": "PDBX  Entity Poly Na Type",
                            "children": [
                                {
                                    "name": "Type",
                                    "url": "/chaise/recordset/#"+catalog_id+"/Vocab:pdbx_entity_poly_na_type_type"
                                }
                            ],
                        },
                        {
                            "name": "Software",
                            "children": [
                                {
                                    "name": "Type",
                                    "url": "/chaise/recordset/#"+catalog_id+"/Vocab:software_type"
                                }
                            ],
                        },
                        {
                            "name": "Struct",
                            "children": [
                                {   
                                    "name": "PDBX  Structure Determination Methodology",
                                    "url": "/chaise/recordset/#"+catalog_id+"/Vocab:struct_pdbx_structure_determination_methodology"
                                },
                                {
                                    "name": "PDBX  CASP Flag",
                                    "url": "/chaise/recordset/#"+catalog_id+"/Vocab:struct_pdbx_CASP_flag"
                                },
                                {
                                    "name": "PDBX  Blank PDB Chainid Flag",
                                    "url": "/chaise/recordset/#"+catalog_id+"/Vocab:struct_asym_pdbx_blank_PDB_chainid_flag"
                                },
                                {
                                    "name": "PDBX  Type",
                                    "url": "/chaise/recordset/#"+catalog_id+"/Vocab:struct_asym_pdbx_type"
                                }
                            ],
                        },
                        {
                            "name": "Workflow",
                            "children": [
                                { "name": "Archive Category", "url": "/chaise/recordset/#"+catalog_id+"/Vocab:Archive_Category" },
                                { "name": "File Format", "url": "/chaise/recordset/#"+catalog_id+"/Vocab:File_Format" },
                                { "name": "File Type", "url": "/chaise/recordset/#"+catalog_id+"/Vocab:File_Type" },
                                { "name": "Process Status", "url": "/chaise/recordset/#"+catalog_id+"/Vocab:Process_Status" },
                                { "name": "System Generated File Type", "url": "/chaise/recordset/#"+catalog_id+"/Vocab:System_Generated_File_Type" },
                                { "name": "Workflow Status", "url": "/chaise/recordset/#"+catalog_id+"/Vocab:Workflow_Status" }
                            ],
                        }
                    ],
                },
                {
                    "name": "Templates",
                    "children": [
                        {
                            "name": "Entry Related File",                            
                            "children": [
                                { "name": "CSV Templates for Restraint Files", "url": "/chaise/recordset/#"+catalog_id+"/PDB:Entry_Related_File_Templates" }
                            ],
                        }
                    ],
                },
                {
                    "name": "Documentation",
                    "children": [
                        {
                            "name": "User Guide",
                            "children": [
                                { "name": "PDB-IHM", "url": "https://docs.google.com/document/d/1CM8-6PYqI0DvETeQEfoUpSFZ8BhLrvYnihLSK8ghVcI/" }
                            ],
                        }
                    ],
                }
            ],
        }
    }

    # Once deploy to staging, put the code in the appropriate place above
    if cfg.is_dev:
        navbar["navbarMenu"]["children"][1]["children"][3] = {
            "name": "Chemical Components",                            
            "children": [
                { "name": "Chem Comp", "url": "/chaise/recordset/#"+catalog_id+"/PDB:chem_comp" },
                # -- dev # updaters only
                { "name": "IHM New Chem Comp", "url": "/chaise/recordset/#"+catalog_id+"/PDB:IHM_New_Chem_Comp"},
                # -- end dev
                { "name": "Chem Comp Atom", "url": "/chaise/recordset/#"+catalog_id+"/PDB:chem_comp_atom" }
            ],
        }
        navbar["navbarMenu"]["children"][2]["children"][0] = {            
            "name": "Chem Comp",
            "children": [
                { "name": "Mon Nstd Flag", "url": "/chaise/recordset/#"+catalog_id+"/Vocab:chem_comp_mon_nstd_flag" },
                { "name": "PDBX  Aromatic Flag", "url": "/chaise/recordset/#"+catalog_id+"/Vocab:chem_comp_atom_pdbx_aromatic_flag" },
                { "name": "PDBX  Leaving Atom Flag", "url": "/chaise/recordset/#"+catalog_id+"/Vocab:chem_comp_atom_pdbx_leaving_atom_flag" },
                { "name": "PDBX  Polymer Type", "url": "/chaise/recordset/#"+catalog_id+"/Vocab:chem_comp_atom_pdbx_polymer_type" },
                { "name": "PDBX  Stereo Config", "url": "/chaise/recordset/#"+catalog_id+"/Vocab:chem_comp_atom_pdbx_stereo_config" },
                { "name": "Substruct Code", "url": "/chaise/recordset/#"+catalog_id+"/Vocab:chem_comp_atom_substruct_code" },
                # -- dev
                { "name": "Chem Comp Release Status", "url": "/chaise/recordset/#"+catalog_id+"/Vocab:chem_comp_pdbx_release_status" },
                { "name": "Chem Comp Processing Site", "url": "/chaise/recordset/#"+catalog_id+"/Vocab:chem_comp_pdbx_processing_site" },
                { "name": "Chem Comp Created For", "url": "/chaise/recordset/#"+catalog_id+"/Vocab:chem_comp_ihm_created_for" },
                # -- end dev
                { "name": "Type", "url": "/chaise/recordset/#"+catalog_id+"/Vocab:chem_comp_type" }
            ],
        }
    
    return navbar

# -- ----------------------------------------------------------------------
# TODO: check this annotation. I (HT) am not aware of this annotations. 
def update_catalog_config(model):
    pass
    """
    "tag:isrd.isi.edu,2019:catalog-config": {
        "name": "pdb",
        "groups": {
            "admin": "https://auth.globus.org/0b98092c-3c41-11e9-a8c8-0ee7d80087ee",
            "reader": "https://auth.globus.org/8875a770-3c40-11e9-a8c8-0ee7d80087ee",
            "writer": "https://auth.globus.org/c94a1e5c-3c40-11e9-a5d1-0aacc65bfe9a",
            "curator": "https://auth.globus.org/eef3e02a-3c40-11e9-9276-0edc9bdd56a6"
        }
    }
    """
    
# -- ===============================================================================================
# -- catalog level annotation

def update_catalog_display(model):
    model.display.update({
        "name_style" : {
            "title_case" : False,
            "underline_space" : True
        },
        "show_foreign_key_link" : {
	    "compact" : False,
	    "detailed" : True
	},
        "show_key_link" : {
	    "compact" : False,
	    "detailed" : True
	},        
    })

# -- ----------------------------------------------------------------------    
def update_catalog_column_defaults(model):
    # column-defaults
    #["tag:isrd.isi.edu,2023:column-defaults"]
    model.column_defaults.update({
        "by_type": {
            "boolean": {
                tag["column_display"]: {
                    "*": {
                        "pre_format": {
                            "format": "%t",
                            "bool_true_value": "Yes",
                            "bool_false_value": "No"
                        }
                    }
                },
            },
        },
        # NOTE: non_deletable doesn't apply to column level
        "by_name": {
            "RID": {
                "tag:misd.isi.edu,2015:display" : {
                    "comment": "Record ID",
                },
                #"tag:isrd.isi.edu,2016:generated": True,
                #"tag:isrd.isi.edu,2016:immutable": True,
                #"tag:isrd.isi.edu,2016:non-deletable": True, # NOT COLUMN LEVEL
            },
            "RCB": {
                "tag:misd.isi.edu,2015:display": {
                    "name": "RCB",
                    "comment": "Created by",
                },
            },
            "RMB": {
                "tag:misd.isi.edu,2015:display": {
                    "name": "RMB",
                    "comment": "Modified by"                    
                },
            },            
            "RCT": {
                "tag:misd.isi.edu,2015:display": {
                    "name": "Creation Time",
                },
                "tag:isrd.isi.edu,2016:generated": True,
                "tag:isrd.isi.edu,2016:immutable": True,
                "tag:isrd.isi.edu,2016:column-display": {
                    "*" : {
		        "pre_format" : {
                            "format" : "YYYY-MM-DD HH:mm"
		        }
                    }
	        },
            },
            "RMT": {
                "tag:misd.isi.edu,2015:display": {
                    "name": "Last Modified Time",
                },
                "tag:isrd.isi.edu,2016:generated": True,
                "tag:isrd.isi.edu,2016:immutable": True,
                "tag:isrd.isi.edu,2016:column-display": {
                    "*" : {
		        "pre_format" : {
                            "format" : "YYYY-MM-DD HH:mm"
		        }
                    }
	        },
            },
            "Accession_Code": {
                "tag:isrd.isi.edu,2016:generated": True,
                "tag:isrd.isi.edu,2016:immutable": True,
            },
            "Record_Status_Detail": {
                "tag:isrd.isi.edu,2016:generated": True,
                "tag:isrd.isi.edu,2016:immutable": True,
                #"tag:misd.isi.edu,2015:display" : {
                #    "comment": "Record status detail is listed"
                #},
            },
            "File_Bytes": {
                "tag:misd.isi.edu,2015:display" : {
                    "name": "File Size"                    
                },
            },
        },
    })
            
    
# -- ===============================================================================================
# presence tag annotations: generated, immutable, non-deletable, required
# 
# -- ----------------------------------------------------------------------
# identify generated schemas/tables/columns and mark them as generated, immutable, and non-deletables
def update_generated_elements(model):
        
    generated_tables = set()
    generated_tables.update(get_tables(model, schema_names=["PDB"], table_names=[]))
    for table in generated_tables:
        table.annotations[tag["generated"]] = True
        #table.annotations[tag["immutable"]] = True
        table.annotations[tag["non_deletable"]] = True        

    generated_columns = set()
    #generated_columns.update(get_columns(model, schema_pattern=".*", table_pattern=".*", column_pattern="Accession_Code"))
    #generated_columns.update(get_columns(model, schema_names=["PDB"], table_names=["entry"], column_names=["Accession_Code"]))
    for column in generated_columns:
        column.annotations[tag["generated"]] = True
        column.annotations[tag["immutable"]] = True
        # column.non_deletable = True # -- not at column level

# -- ----------------------------------------------------------------------
def update_required_annotations(model):
    #if not schemas_not_in_model: set_elements_not_in_model(model)    
    required = set()
    
    #required.update(get_columns(model, schema_names=["PDB"], table_names=["Entry_Related_File", "Entry_Related_File_Templates"], column_names=["File_URL"])) # -- already in model
    #required.update(get_columns(model, schema_names=["PDB"], table_names=["Entry_Error_File", "Generated_File"], column_names=["File_URL"])) # -- already in model
    #required.update(get_columns(model, schema_names=["PDB"], table_names=["Supported_Dictionary"], column_names=["Data_Dictionary_RID", "Data_Dictionary_Category"])) # -- already in model
    #required.update(get_columns(model, schema_names=["PDB"], table_names=["Data_Dictionary"], column_names=["Name", "Category", "Version", "Location"])) # already in model
    
    for column in required:
        if column in columns_not_in_model: continue
        column.annotations[tag["required"]] = True
    
    
# =================================================================================================
def print_generated_elements(model):
    set_elements_not_in_model(model)
    generated_dict = {}
    for schema in model.schemas.values():
        if schema.generated: 
            generated_dict.setdefault((schema.name, None), set())
        for table in schema.tables.values():
            if table.generated:
                generated_dict.setdefault((schema.name, table.name), set())
                for column in table.columns:
                    if column.name in ["RID", "RCT", "RMT", "RCB", "RMB"]: continue                    
                    if column.generated:
                        generated_dict.setdefault((schema.name, table.name), set()).add(column.name)

    print("# ---- generated elements ----")
    for key, cnames in generated_dict.items():
        sname, tname = key
        print("generated %s:%s: %s" % (sname, tname, cnames))

    
# -- ----------------------------------------------------------------------
def print_required_annotations(model):
    set_elements_not_in_model(model)
    required_dict = {}
    for schema in model.schemas.values():
        for table in schema.tables.values():
            for column in table.columns:
                if column.name in ["Principal_Investigator", "Consortium"]: continue
                if column.required:
                    required_dict.setdefault((schema.name, table.name), set()).add(column.name)

    print("# ---- required elements ----")
    for key, cnames in required_dict.items():
        sname, tname = key
        print("required %s:%s: %s" % (sname, tname, cnames))
        

# -- ------------------------------------------------------------------------
def print_isolated_tables(model):
    referenced_tables = set()
    referring_tables = set()
    for schema in model.schemas.values():
        for table in schema.tables.values():
            if table.foreign_keys:
                referring_tables.add(table)
            for fkey in table.foreign_keys:
                referenced_tables.add(fkey.pk_table)

    print("# ----- print isolated/outbound-only/inbound-only tables ---- ")
    for schema in model.schemas.values():
        for table in schema.tables.values():
            if table not in referenced_tables and table not in referring_tables:
                print("-- isolated: %s:%s" % (table.schema.name, table.name))
            if table in referenced_tables - referring_tables:
                print("-> in_only: %s:%s" % (table.schema.name, table.name))
            if table in referring_tables - referenced_tables:
                print("<- out_only: %s:%s" % (table.schema.name, table.name))
            

# -- ---------------------------------------------------------------------------------
def remove_catalog_generated(model):

    print(model.annotations.keys())
    if tag["generated"] in model.annotations.keys():  model.annotations.pop(tag["generated"])
    if tag["immutable"] in model.annotations.keys():  model.annotations.pop(tag["immutable"])
    if tag["non_deletable"] in model.annotations.keys(): model.annotations.pop(tag["non_deletable"])
    print(model.annotations.keys())
    model.apply()
                    
# -- =================================================================================                    

# -- update annotations across multiple schemas
def update_catalog_wide_annotations(model):
    #if not schemas_not_in_model: set_elements_not_in_model(model)
    
    # -- catalog-wide annotations
    update_generated_elements(model)
    update_required_annotations(model)

# -- ---------------------------------------------------------------------------------
# catalog annotation
def update_catalog_annotations(model):
    initialize_policies(model.catalog)
    
    chaise_config = get_chaise_config(model.catalog.catalog_id)
    model.annotations[tag["chaise_config"]] = chaise_config
    bulk_upload.update_bulk_upload_annotations(model)
    update_catalog_display(model)
    update_catalog_column_defaults(model)
    
# -- ---------------------------------------------------------------------------------
# catalog annotation
def clear_catalog_catalog_wide_annotations(model):
    model.annotations.clear()
    clear_catalog_annotations(model, catalog_specific_annotation_tags, recursive=False)                                    
    clear_catalog_annotations(model, catalog_wide_annotation_tags)

    
# -- =================================================================================

# -- =================================================================================
        
def main(server_name, catalog_id, credentials, args):
    server = DerivaServer('https', server_name, credentials)
    catalog = server.connect_ermrest(catalog_id)
    catalog.dcctx['cid'] = DCCTX["annotation"]        
    model = catalog.getCatalogModel()
    
    if args.pre_print:
        #print_isolated_tables(model)
        print("def catalog_annotations(model):");
        print("    model.annotations = %s" % (json.dumps(model.annotations, indent=4)))
        print_presence_tag_annotations(model, [tag["generated"], tag["immutable"], tag["non_deletable"]])
        print_presence_tag_annotations(model, [tag["required"]])

    clear_catalog_catalog_wide_annotations(model)
    update_catalog_annotations(model)
    update_catalog_wide_annotations(model)
    
    if args.post_print:
        print("def catalog_annotations(model):");
        print("    model.annotations = %s" % (json.dumps(model.annotations, indent=4)))
        print_presence_tag_annotations(model, [tag["generated"], tag["immutable"], tag["non_deletable"]])
        print_presence_tag_annotations(model, [tag["required"]])
        
    if not args.dry_run:
        model.apply()
        pass
    
# -- =================================================================================

if __name__ == '__main__':
    args = PDBDEV_CLI("PDB_Dev", None, 1).parse_cli()
    credentials = get_credential(args.host, args.credential_file)
    print(credentials)
    main(args.host, args.catalog_id, credentials, args)
