#!/usr/bin/python

"""
Script for defining the PDB ACLs.

"""

"""
Globus Groups
"""
pdb_admin = "https://auth.globus.org/0b98092c-3c41-11e9-a8c8-0ee7d80087ee"
isrd_staff = "https://auth.globus.org/176baec4-ed26-11e5-8e88-22000ab4b42b"
pdb_writer = "https://auth.globus.org/c94a1e5c-3c40-11e9-a5d1-0aacc65bfe9a"
pdb_reader = "https://auth.globus.org/8875a770-3c40-11e9-a8c8-0ee7d80087ee"
pdb_curator = "https://auth.globus.org/eef3e02a-3c40-11e9-9276-0edc9bdd56a6"
pdb_submitter = "https://auth.globus.org/99da042e-64a6-11ea-ad5f-0ef992ed7ca1"

"""
List with tables ACLs
"""
table_acls_list = {
    "select_admin_curator": {
        "delete": [],
        "insert": [],
        "select": [
            pdb_admin,
            pdb_curator
        ],
        "update": [],
        "enumerate": []
    },
    "select_admin_curator_writer": {
        "delete": [],
        "insert": [],
        "select": [
            pdb_writer,
            pdb_curator,
            pdb_admin
        ],
        "update": [],
        "enumerate": []
    },
    "insert_curator_curator": {
        "insert": [
            pdb_writer,
            pdb_curator
        ],
        "select": [
            pdb_reader
        ]
    },
    "owner_admin_staff": {
        "owner": [
            pdb_admin,
            isrd_staff
        ],
        "write": [],
        "delete": [
            pdb_curator
        ],
        "insert": [
            pdb_curator,
            pdb_writer,
            pdb_submitter
        ],
        "select": [
            pdb_writer,
            pdb_reader
        ],
        "update": [
            pdb_curator
        ],
        "enumerate": [
            "*"
        ]
    }
}

"""
List with tables ACL Bindings
"""
table_acl_bindings_list = {
    "group_creator": {
        "self_service_group": {
            "types": [
                "update",
                "delete"
            ],
            "projection": [
                "Owner"
            ],
            "projection_type": "acl",
            "scope_acl": [
                "*"
            ]
        },
        "self_service_creator": {
            "types": [
                "update",
                "delete"
            ],
            "projection": [
                "RCB"
            ],
            "projection_type": "acl",
            "scope_acl": [
                "*"
            ]
        }
    },
    "reader_creator": {
        "released_reader": {
            "types": [
                "select"
            ],
            "scope_acl": [
                pdb_submitter
            ],
            "projection": [
                "RCB"
            ],
            "projection_type": "acl"
        },
        "self_service_creator": {
            "types": [
                "update",
                "delete"
            ],
            "scope_acl": [
                pdb_submitter
            ],
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
                "RCB"
            ],
            "projection_type": "acl"
        }
    },
    "reader_group_creator": {
        "released_reader": {
            "types": [
                "select"
            ],
            "scope_acl": [
                pdb_submitter
            ],
            "projection": [
                "RID"
            ],
            "projection_type": "nonnull"
        },
        "self_service_group": {
            "types": [
                "update",
                "delete"
            ],
            "scope_acl": [
                "*"
            ],
            "projection": [
                "Owner"
            ],
            "projection_type": "acl"
        },
        "self_service_creator": {
            "types": [
                "update",
                "delete"
            ],
            "scope_acl": [
                "*"
            ],
            "projection": [
                "RCB"
            ],
            "projection_type": "acl"
        }
    }
}

"""
List with tables ACL Bindings Templates
"""
table_acl_bindings_template_list = {
    "reader_group_creator": """
{
    "released_reader": {
        "types": [
            "select"
        ],
        "scope_acl": [
            "pdb_submitter"
        ],
        "projection": [
            {
                "outbound": [
                    "PDB",
                    "%FOREIGN_KEY%"
                ]
            },
            "RCB"
        ],
        "projection_type": "acl"
    },
    "self_service_group": {
        "types": [
            "update",
            "delete"
        ],
        "scope_acl": [
            "*"
        ],
        "projection": [
            "Owner"
        ],
        "projection_type": "acl"
    },
    "self_service_creator": {
        "types": [
            "update",
            "delete"
        ],
        "scope_acl": [
            "pdb_submitter"
        ],
        "projection": [
            {
                "outbound": [
                    "PDB",
                    "%FOREIGN_KEY%"
                ]
            },
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
            "RCB"
        ],
        "projection_type": "acl"
    }
}
""",
    "reader_creator": """
{
    "released_reader": {
        "types": [
            "select"
        ],
        "scope_acl": [
            "pdb_submitter"
        ],
        "projection": [
            {
                "outbound": [
                    "PDB",
                    "%FOREIGN_KEY%"
                ]
            },
            "RCB"
        ],
        "projection_type": "acl"
    },
    "self_service_creator": {
        "types": [
            "update",
            "delete"
        ],
        "scope_acl": [
            "pdb_submitter"
        ],
        "projection": [
            {
                "outbound": [
                    "PDB",
                    "%FOREIGN_KEY%"
                ]
            },
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
            "RCB"
        ],
        "projection_type": "acl"
    }
}
""",
    "reader_group": """
{
    "released_reader": {
        "types": [
            "select"
        ],
        "scope_acl": [
            "pdb_submitter"
        ],
        "projection": [
            {
                "outbound": [
                    "PDB",
                    "%FOREIGN_KEY%"
                ]
            },
            "RCB"
        ],
        "projection_type": "acl"
    },
    "self_service_group": {
        "types": [
            "update",
            "delete"
        ],
        "scope_acl": [
            "*"
        ],
        "projection": [
            "Owner"
        ],
        "projection_type": "acl"
    }
}
""",
    "reader": """
{
    "released_reader": {
        "types": [
            "select"
        ],
        "scope_acl": [
            "pdb_submitter"
        ],
        "projection": [
            {
                "outbound": [
                    "PDB",
                    "Entry_mmCIF_File_Structure_Id_fkey"
                ]
            },
            "RCB"
        ],
        "projection_type": "acl"
    }
}
"""
}

"""
List with columns ACLs
"""
column_acls_list = {
    "select": {
        "select": [
            "*"
        ]
    },
    "insert_select_update": {
        "insert": [
            pdb_curator,
            pdb_writer
        ],
        "select": [
            "*"
        ],
        "update": [
            pdb_curator,
            pdb_writer
        ]
    }
}

"""
List with columns ACL Bindings
"""
column_acl_bindings_list = {
    "no_binding": {
        "no_binding": False
    },
    "self_service_creator": {
        "self_service_creator": False
    }
}

"""
List with Foreign Keys ACLs
"""
foreign_key_acls_list = {
    "insert_update_curator": {
        "insert": [
            pdb_curator
        ],
        "update": [
            pdb_curator
        ]
    },
    "insert_update_all": {
        "insert": [
            "*"
        ],
        "update": [
            "*"
        ]
    },
    "insert_update_curator_writer": {
        "insert": [
            pdb_curator,
            pdb_writer
        ],
        "update": [
            pdb_curator,
            pdb_writer
        ]
    }
}

"""
List with Foreign Keys ACL Bindings
"""
foreign_key_acl_bindings_list = {
    "set_owner": {
        "set_owner": {
            "types": [
                "insert"
            ],
            "projection": [
                "ID"
            ],
            "projection_type": "acl",
            "scope_acl": [
                "*"
            ]
        }
    },
    "submit_reader": {
        "submit_reader": {
            "types": [
                "insert",
                "update"
            ],
            "scope_acl": [
                pdb_submitter
            ],
            "projection": [
                {
                    "or": [
                        {
                            "filter": "Name",
                            "operand": "DRAFT",
                            "operator": "="
                        },
                        {
                            "filter": "Name",
                            "operand": "DEPO",
                            "operator": "="
                        },
                        {
                            "filter": "Name",
                            "operand": "SUBMIT",
                            "operator": "="
                        }
                    ]
                },
                "RID"
            ],
            "projection_type": "nonnull"
        }
    }
}

"""
Catalog ACLs
"""
catalog_acls = {
  "owner": [
    pdb_admin,
    isrd_staff
  ],
  "select": [
    pdb_writer,
    pdb_reader
  ],
  "write": [],
  "update": [
    pdb_curator
  ],
  "delete": [
    pdb_curator
  ],
  "enumerate": [
    "*"
  ],
  "insert": [
    pdb_curator,
    pdb_writer
  ],
  "create": []
}

"""
Tables ACLs
"""
table_acls = [
    {
        "schema": "public",
        "acls": "select_admin_curator",
        "tables": ["ERMrest_Client"]
    },
    {
        "schema": "public",
        "acls": "select_admin_curator_writer",
        "tables": ["ERMrest_Group"]
    },
    {
        "schema": "public",
        "acls": "insert_curator_curator",
        "tables": ["Catalog_Group"]
    },
    {
        "schema": "PDB",
        "acls": "owner_admin_staff",
        "tables": [
            "ihm_epr_restraint",
            "ihm_model_representation_details",
            "entity_name_sys",
            "ihm_ensemble_sub_sample",
            "ihm_starting_model_details",
            "entity_poly",
            "ihm_struct_assembly_class_link",
            "ihm_cross_link_restraint",
            "ihm_struct_assembly_details",
            "software",
            "ihm_dataset_related_db_reference",
            "ihm_starting_comparative_models",
            "ihm_external_files",
            "ihm_predicted_contact_restraint",
            "ihm_geometric_object_list",
            "ihm_interface_residue_feature",
            "ihm_geometric_object_torus",
            "ihm_cross_link_list",
            "ihm_derived_angle_restraint",
            "ihm_model_representation",
            "ihm_cross_link_result_parameters",
            "entry",
            "ihm_ensemble_info",
            "ihm_dataset_group",
            "ihm_modeling_protocol",
            "ihm_modeling_post_process",
            "ihm_2dem_class_average_restraint",
            "ihm_entity_poly_segment",
            "ihm_poly_probe_position",
            "ihm_localization_density_files",
            "ihm_related_datasets",
            "ihm_pseudo_site",
            "ihm_multi_state_modeling",
            "ihm_non_poly_feature",
            "Entry_Related_File",
            "ihm_chemical_component_descriptor",
            "ihm_geometric_object_transformation",
            "ihm_pseudo_site_feature",
            "ihm_model_group_link",
            "atom_type",
            "ihm_derived_dihedral_restraint",
            "ihm_residues_not_modeled",
            "ihm_2dem_class_average_fitting",
            "ihm_dataset_list",
            "struct",
            "ihm_geometric_object_half_torus",
            "audit_author",
            "entity_src_gen",
            "ihm_struct_assembly_class",
            "ihm_geometric_object_distance_restraint",
            "pdbx_entity_nonpoly",
            "ihm_multi_state_model_group_link",
            "ihm_dataset_group_link",
            "ihm_hdx_restraint",
            "struct_ref",
            "ihm_geometric_object_sphere",
            "ihm_poly_probe_conjugate",
            "ihm_modeling_protocol_details",
            "ihm_dataset_external_reference",
            "ihm_ligand_probe",
            "ihm_3dem_restraint",
            "ihm_probe_list",
            "ihm_hydroxyl_radical_fp_restraint",
            "ihm_data_transformation",
            "struct_ref_seq",
            "ihm_model_list",
            "entity_name_com",
            "ihm_struct_assembly",
            "ihm_external_reference_info",
            "entity",
            "ihm_cross_link_pseudo_site",
            "ihm_sas_restraint",
            "ihm_starting_model_seq_dif",
            "ihm_geometric_object_center",
            "struct_asym",
            "ihm_poly_atom_feature",
            "struct_ref_seq_dif",
            "entity_poly_seq",
            "ihm_starting_computational_models",
            "chem_comp",
            "ihm_derived_distance_restraint",
            "ihm_geometric_object_axis",
            "ihm_geometric_object_plane",
            "ihm_ordered_ensemble",
            "ihm_poly_residue_feature",
            "citation_author",
            "ihm_model_representative",
            "ihm_model_group",
            "ihm_cross_link_result",
            "citation",
            "ihm_feature_list"
        ]
    }
]

"""
Tables ACL Bindings
"""
table_acl_bindings = [
    {
        "schema": "WWW",
        "acl_bindings": "group_creator",
        "tables": ["Page"]
    },
    {
        "schema": "PDB",
        "acl_bindings": "reader_group_creator",
        "tables": [
            "ihm_epr_restraint",
            "ihm_model_representation_details",
            "entity_name_sys",
            "ihm_starting_model_details",
            "ihm_struct_assembly_class_link",
            "pdbx_protein_info",
            "ihm_cross_link_restraint",
            "ihm_struct_assembly_details",
            "pdbx_inhibitor_info",
            "audit_conform",
            "software",
            "ihm_dataset_related_db_reference",
            "ihm_starting_comparative_models",
            "ihm_external_files",
            "ihm_predicted_contact_restraint",
            "ihm_geometric_object_list",
            "ihm_interface_residue_feature",
            "ihm_geometric_object_torus",
            "ihm_cross_link_list",
            "ihm_model_representation",
            "ihm_cross_link_result_parameters",
            "ihm_ensemble_info",
            "ihm_dataset_group",
            "ihm_modeling_protocol",
            "ihm_modeling_post_process",
            "ihm_2dem_class_average_restraint",
            "ihm_entity_poly_segment",
            "ihm_poly_probe_position",
            "ihm_localization_density_files",
            "ihm_related_datasets",
            "ihm_multi_state_modeling",
            "ihm_non_poly_feature",
            "ihm_chemical_component_descriptor",
            "ihm_geometric_object_transformation",
            "ihm_pseudo_site_feature",
            "ihm_model_group_link",
            "ihm_residues_not_modeled",
            "ihm_2dem_class_average_fitting",
            "ihm_dataset_list",
            "struct",
            "pdbx_entity_poly_na_type",
            "ihm_geometric_object_half_torus",
            "audit_author",
            "entity_src_gen",
            "ihm_struct_assembly_class",
            "ihm_geometric_object_distance_restraint",
            "pdbx_entity_nonpoly",
            "ihm_multi_state_model_group_link",
            "ihm_dataset_group_link",
            "ihm_geometric_object_sphere",
            "ihm_poly_probe_conjugate",
            "ihm_modeling_protocol_details",
            "ihm_dataset_external_reference",
            "ihm_ligand_probe",
            "ihm_3dem_restraint",
            "ihm_probe_list",
            "ihm_hydroxyl_radical_fp_restraint",
            "entity_name_com",
            "ihm_struct_assembly",
            "ihm_external_reference_info",
            "chem_comp_atom",
            "entity",
            "ihm_sas_restraint",
            "ihm_starting_model_seq_dif",
            "ihm_geometric_object_center",
            "ihm_poly_atom_feature",
            "ihm_starting_computational_models",
            "ihm_derived_distance_restraint",
            "pdbx_entry_details",
            "ihm_geometric_object_axis",
            "ihm_geometric_object_plane",
            "pdbx_ion_info",
            "ihm_ordered_ensemble",
            "ihm_poly_residue_feature",
            "citation_author",
            "ihm_model_representative",
            "ihm_model_group",
            "ihm_cross_link_result",
            "citation",
            "ihm_feature_list"
        ],
        "foreign_keys": {
            "ihm_epr_restraint": "ihm_epr_restraint_structure_id_fkey",
            "ihm_model_representation_details": "ihm_model_representation_details_structure_id_fkey",
            "entity_name_sys": "entity_name_sys_structure_id_fkey",
            "ihm_starting_model_details": "ihm_starting_model_details_structure_id_fkey",
            "ihm_struct_assembly_class_link": "ihm_struct_assembly_class_link_structure_id_fkey",
            "pdbx_protein_info": "pdbx_protein_info_structure_id_fkey",
            "ihm_cross_link_restraint": "ihm_cross_link_restraint_structure_id_fkey",
            "ihm_struct_assembly_details": "ihm_struct_assembly_details_structure_id_fkey",
            "pdbx_inhibitor_info": "pdbx_inhibitor_info_structure_id_fkey",
            "audit_conform": "audit_conform_structure_id_fkey",
            "software": "software_structure_id_fkey",
            "ihm_dataset_related_db_reference": "ihm_dataset_related_db_reference_structure_id_fkey",
            "ihm_starting_comparative_models": "ihm_starting_comparative_models_structure_id_fkey",
            "ihm_external_files": "ihm_external_files_structure_id_fkey",
            "ihm_predicted_contact_restraint": "ihm_predicted_contact_restraint_structure_id_fkey",
            "ihm_geometric_object_list": "ihm_geometric_object_list_structure_id_fkey",
            "ihm_interface_residue_feature": "ihm_interface_residue_feature_structure_id_fkey",
            "ihm_geometric_object_torus": "ihm_geometric_object_torus_structure_id_fkey",
            "ihm_cross_link_list": "ihm_cross_link_list_structure_id_fkey",
            "ihm_model_representation": "ihm_model_representation_structure_id_fkey",
            "ihm_cross_link_result_parameters": "ihm_cross_link_result_parameters_structure_id_fkey",
            "ihm_ensemble_info": "ihm_ensemble_info_structure_id_fkey",
            "ihm_dataset_group": "ihm_dataset_group_structure_id_fkey",
            "ihm_modeling_protocol": "ihm_modeling_protocol_structure_id_fkey",
            "ihm_modeling_post_process": "ihm_modeling_post_process_structure_id_fkey",
            "ihm_2dem_class_average_restraint": "ihm_2dem_class_average_restraint_structure_id_fkey",
            "ihm_entity_poly_segment": "ihm_entity_poly_segment_structure_id_fkey",
            "ihm_poly_probe_position": "ihm_poly_probe_position_structure_id_fkey",
            "ihm_localization_density_files": "ihm_localization_density_files_structure_id_fkey",
            "ihm_related_datasets": "ihm_related_datasets_structure_id_fkey",
            "ihm_multi_state_modeling": "ihm_multi_state_modeling_structure_id_fkey",
            "ihm_non_poly_feature": "ihm_non_poly_feature_structure_id_fkey",
            "ihm_chemical_component_descriptor": "ihm_chemical_component_descriptor_structure_id_fkey",
            "ihm_geometric_object_transformation": "ihm_geometric_object_transformation_structure_id_fkey",
            "ihm_pseudo_site_feature": "ihm_pseudo_site_feature_structure_id_fkey",
            "ihm_model_group_link": "ihm_model_group_link_structure_id_fkey",
            "ihm_residues_not_modeled": "ihm_residues_not_modeled_structure_id_fkey",
            "ihm_2dem_class_average_fitting": "ihm_2dem_class_average_fitting_structure_id_fkey",
            "ihm_dataset_list": "ihm_dataset_list_structure_id_fkey",
            "struct": "struct_entry_id_fkey",
            "pdbx_entity_poly_na_type": "pdbx_entity_poly_na_type_structure_id_fkey",
            "ihm_geometric_object_half_torus": "ihm_geometric_object_half_torus_structure_id_fkey",
            "audit_author": "audit_author_structure_id_fkey",
            "entity_src_gen": "entity_src_gen_structure_id_fkey",
            "ihm_struct_assembly_class": "ihm_struct_assembly_class_structure_id_fkey",
            "ihm_geometric_object_distance_restraint": "ihm_geometric_object_distance_restraint_structure_id_fkey",
            "pdbx_entity_nonpoly": "pdbx_entity_nonpoly_structure_id_fkey",
            "ihm_multi_state_model_group_link": "ihm_multi_state_model_group_link_structure_id_fkey",
            "ihm_dataset_group_link": "ihm_dataset_group_link_structure_id_fkey",
            "ihm_geometric_object_sphere": "ihm_geometric_object_sphere_structure_id_fkey",
            "ihm_poly_probe_conjugate": "ihm_poly_probe_conjugate_structure_id_fkey",
            "ihm_modeling_protocol_details": "ihm_modeling_protocol_details_structure_id_fkey",
            "ihm_dataset_external_reference": "ihm_dataset_external_reference_structure_id_fkey",
            "ihm_ligand_probe": "ihm_ligand_probe_structure_id_fkey",
            "ihm_3dem_restraint": "ihm_3dem_restraint_structure_id_fkey",
            "ihm_probe_list": "ihm_probe_list_structure_id_fkey",
            "ihm_hydroxyl_radical_fp_restraint": "ihm_hydroxyl_radical_fp_restraint_structure_id_fkey",
            "entity_name_com": "entity_name_com_structure_id_fkey",
            "ihm_struct_assembly": "ihm_struct_assembly_structure_id_fkey",
            "ihm_external_reference_info": "ihm_external_reference_info_structure_id_fkey",
            "chem_comp_atom": "chem_comp_atom_structure_id_fkey",
            "entity": "entity_structure_id_fkey",
            "ihm_sas_restraint": "ihm_sas_restraint_structure_id_fkey",
            "ihm_starting_model_seq_dif": "ihm_starting_model_seq_dif_structure_id_fkey",
            "ihm_geometric_object_center": "ihm_geometric_object_center_structure_id_fkey",
            "ihm_poly_atom_feature": "ihm_poly_atom_feature_structure_id_fkey",
            "ihm_starting_computational_models": "ihm_starting_computational_models_structure_id_fkey",
            "ihm_derived_distance_restraint": "ihm_derived_distance_restraint_structure_id_fkey",
            "pdbx_entry_details": "pdbx_entry_details_entry_id_fkey",
            "ihm_geometric_object_axis": "ihm_geometric_object_axis_structure_id_fkey",
            "ihm_geometric_object_plane": "ihm_geometric_object_plane_structure_id_fkey",
            "pdbx_ion_info": "pdbx_ion_info_structure_id_fkey",
            "ihm_ordered_ensemble": "ihm_ordered_ensemble_structure_id_fkey",
            "ihm_poly_residue_feature": "ihm_poly_residue_feature_structure_id_fkey",
            "citation_author": "citation_author_structure_id_fkey",
            "ihm_model_representative": "ihm_model_representative_structure_id_fkey",
            "ihm_model_group": "ihm_model_group_structure_id_fkey",
            "ihm_cross_link_result": "ihm_cross_link_result_structure_id_fkey",
            "citation": "citation_structure_id_fkey",
            "ihm_feature_list": "ihm_feature_list_structure_id_fkey"
        }
    },
    {
        "schema": "PDB",
        "acl_bindings": "reader_creator",
        "tables": [
            "ihm_ensemble_sub_sample",
            "ihm_derived_angle_restraint",
            "ihm_pseudo_site",
            "ihm_derived_dihedral_restraint",
            "ihm_hdx_restraint",
            "struct_ref",
            "ihm_data_transformation",
            "struct_ref_seq",
            "ihm_cross_link_pseudo_site",
            "struct_ref_seq_dif"
        ],
        "foreign_keys": {
            "ihm_ensemble_sub_sample": "ihm_ensemble_sub_sample_structure_id_fkey",
            "ihm_derived_angle_restraint": "ihm_derived_angle_restraint_structure_id_fkey",
            "ihm_pseudo_site": "ihm_pseudo_site_structure_id_fkey",
            "ihm_derived_dihedral_restraint": "ihm_derived_dihedral_restraint_structure_id_fkey",
            "ihm_hdx_restraint": "ihm_hdx_restraint_structure_id_fkey",
            "struct_ref": "struct_ref_structure_id_fkey",
            "ihm_data_transformation": "ihm_data_transformation_structure_id_fkey",
            "struct_ref_seq": "struct_ref_seq_structure_id_fkey",
            "ihm_cross_link_pseudo_site": "ihm_cross_link_pseudo_site_structure_id_fkey",
            "struct_ref_seq_dif": "struct_ref_seq_dif_structure_id_fkey"
        }
    },
    {
        "schema": "PDB",
        "acl_bindings": "reader_group",
        "tables": [
            "entity_poly",
            "atom_type",
            "ihm_model_list",
            "struct_asym",
            "entity_poly_seq",
            "chem_comp"
        ],
        "foreign_keys": {
            "entity_poly": "entity_poly_structure_id_fkey",
            "atom_type": "atom_type_structure_id_fkey",
            "ihm_model_list": "ihm_model_list_structure_id_fkey",
            "struct_asym": "struct_asym_structure_id_fkey",
            "entity_poly_seq": "entity_poly_seq_structure_id_fkey",
            "chem_comp": "chem_comp_structure_id_fkey"
        }
    },
    {
        "schema": "PDB",
        "acl_bindings": "reader",
        "tables": [
            "Entry_mmCIF_File"
        ],
        "foreign_keys": {
            "Entry_mmCIF_File": "Entry_mmCIF_File_Structure_Id_fkey"
        }
    },
    {
        "schema": "PDB",
        "acl_bindings": "reader_creator",
        "tables": [
            "entry",
            "Entry_Related_File"
        ]
    },
    {
        "schema": "PDB",
        "acl_bindings": "reader_group_creator",
        "tables": [
             "Entry_Related_File_Templates"
        ]
    },
    {
        "schema": "Vocab",
        "acl_bindings": "reader_group_creator",
        "tables": [
            "chem_comp_atom_substruct_code",
            "struct_asym_pdbx_type",
            "ihm_poly_residue_feature_interface_residue_flag",
            "ihm_modeling_post_process_feature",
            "ihm_modeling_protocol_details_ensemble_flag",
            "ihm_cross_link_restraint_conditional_crosslink_flag",
            "ihm_model_representation_details_model_mode",
            "ihm_poly_residue_feature_residue_range_granularity",
            "ihm_cross_link_restraint_model_granularity",
            "ihm_ensemble_info_ensemble_clustering_method",
            "ihm_probe_list_probe_origin",
            "pdbx_entity_poly_na_type_type",
            "ihm_geometric_object_axis_axis_type",
            "software_type",
            "ihm_feature_list_entity_type",
            "chem_comp_atom_pdbx_polymer_type",
            "pseudo_site_flag",
            "ihm_modeling_protocol_details_multi_state_flag",
            "ihm_geometric_object_half_torus_section",
            "ihm_probe_list_reactive_probe_flag",
            "ihm_3dem_restraint_map_segment_flag",
            "ihm_geometric_object_list_object_type",
            "geometric_object_distance_restraint_object_character",
            "chem_comp_type",
            "ihm_poly_residue_feature_rep_atom",
            "ihm_dataset_list_database_hosted",
            "ihm_modeling_protocol_details_ordered_flag",
            "ihm_external_files_content_type",
            "cross_link_partner",
            "geometric_object_distance_restraint_group_condition",
            "ihm_derived_angle_restraint_group_conditionality",
            "entity_poly_nstd_linkage",
            "ihm_derived_distance_restraint_group_conditionality",
            "entity_src_method",
            "ihm_residues_not_modeled_reason",
            "sub_sampling_type",
            "ihm_external_files_file_format",
            "ihm_epr_restraint_fitting_state",
            "File_Type",
            "chem_comp_atom_pdbx_leaving_atom_flag",
            "ihm_starting_model_details_starting_model_source",
            "chem_comp_atom_pdbx_aromatic_flag",
            "entity_poly_nstd_monomer",
            "ihm_derived_dihedral_restraint_restraint_type",
            "model_representation_details_model_object_primitive",
            "chem_comp_mon_nstd_flag",
            "ihm_sas_restraint_fitting_state",
            "entity_poly_seq_hetero",
            "ihm_predicted_contact_restraint_restraint_type",
            "ihm_geometric_object_plane_plane_type",
            "ihm_2dem_class_average_restraint_image_segment_flag",
            "entity_src_gen_pdbx_alt_source_flag",
            "ihm_model_representation_details_model_granularity",
            "ihm_derived_dihedral_restraint_group_conditionality",
            "entity_type",
            "ihm_predicted_contact_restraint_model_granularity",
            "ihm_predicted_contact_restraint_rep_atom_1",
            "chem_comp_atom_pdbx_stereo_config",
            "starting_comparative_models_template_sequence_id_denom",
            "ihm_modeling_protocol_details_multi_scale_flag",
            "ihm_dataset_list_data_type",
            "entity_poly_pdbx_sequence_evidence_code",
            "entity_poly_nstd_chirality",
            "ihm_poly_probe_position_modification_flag",
            "ihm_probe_list_probe_link_type",
            "ihm_poly_probe_position_mutation_flag",
            "ihm_dataset_related_db_reference_db_name",
            "ihm_external_reference_info_refers_to",
            "ihm_modeling_post_process_type",
            "ihm_external_reference_info_reference_type",
            "struct_asym_pdbx_blank_PDB_chainid_flag",
            "struct_ref_seq_dif_details",
            "struct_ref_db_name",
            "ihm_cross_link_list_linker_type",
            "ihm_predicted_contact_restraint_rep_atom_2",
            "ihm_model_representative_selection_criteria",
            "ihm_multi_state_modeling_experiment_type",
            "workflow_status",
            "ihm_ensemble_info_ensemble_clustering_feature",
            "entity_poly_type",
            "ihm_dataset_group_application",
            "sub_sample_flag",
            "ihm_struct_assembly_class_type",
            "struct_pdbx_CASP_flag",
            "ihm_cross_link_restraint_restraint_type",
            "File_Format",
            "ihm_sas_restraint_profile_segment_flag",
            "ihm_feature_list_feature_type",
            "ihm_derived_angle_restraint_restraint_type",
            "ihm_geometric_object_distance_restraint_restraint_type",
            "ihm_derived_distance_restraint_restraint_type",
            "ihm_poly_probe_conjugate_ambiguous_stoichiometry_flag"
        ]
    }
]

"""
Columns ACLs
"""
column_acls = [
    {
        "schema": "PDB",
        "table": "Entry_mmCIF_File",
        "acls": "select",
        "columns": ["File_URL"]
    },
    {
        "schema": "PDB",
        "table": "Entry_Related_File",
        "acls": "select",
        "columns": ["File_URL"]
    },
    {
        "schema": "PDB",
        "table": "Entry_Related_File_Templates",
        "acls": "select",
        "columns": ["File_URL"]
    },
    {
        "schema": "PDB",
        "table": "entry",
        "acls": "insert_select_update",
        "columns": ["accession_code"]
    }
]

"""
Columns ACL Bindings
"""
column_acl_bindings = [
    {
        "schema": "PDB",
        "table": "Entry_mmCIF_File",
        "acl_bindings": "no_binding",
        "columns": ["File_URL"]
    },
    {
        "schema": "PDB",
        "table": "Entry_Related_File",
        "acl_bindings": "no_binding",
        "columns": ["File_URL"]
    },
    {
        "schema": "PDB",
        "table": "Entry_Related_File_Templates",
        "acl_bindings": "no_binding",
        "columns": ["File_URL"]
    },
    {
        "schema": "PDB",
        "table": "entry",
        "acl_bindings": "self_service_creator",
        "columns": ["accession_code"]
    }
]

"""
Foreign Keys ACLs
"""
foreign_key_acls = [
    {
        "schema": "public",
        "table": "Catalog_Group",
        "acls": "insert_update_curator",
        "foreign_keys": [
            "Catalog_Group_ID1"
        ]
    },
    {
        "schema": "PDB",
        "table": "ihm_epr_restraint",
        "acls": "insert_update_all",
        "foreign_keys": [
            "ihm_epr_restraint_dataset_list_id_fkey",
            "ihm_epr_restraint_fitting_state_fkey",
            "ihm_epr_restraint_model_id_fkey",
            "ihm_epr_restraint_structure_id_fkey",
            "ihm_epr_restraint_fitting_software_id_fkey",
            "ihm_epr_restraint_fitting_method_citation_id_fk",
            "ihm_epr_restraint_fitting_method_citation_id_fkey"
        ]
    },
    {
        "schema": "PDB",
        "table": "ihm_model_representation_details",
        "acls": "insert_update_all",
        "foreign_keys": [
            "ihm_model_representation_details_starting_model_id_fk",
            "ihm_model_representation_details_entity_poly_segment_id_fk",
            "ihm_model_representation_details_entity_id_fkey",
            "ihm_model_representation_details_model_mode_fkey",
            "ihm_model_representation_details_entity_asym_id_fkey",
            "ihm_model_representation_details_model_granularity_fkey",
            "ihm_model_representation_details_starting_model_id_fkey",
            "ihm_model_representation_details_structure_id_fkey",
            "ihm_model_representation_details_entity_poly_segment_id_fkey",
            "model_representation_details_model_object_primitive_fkey",
            "ihm_model_representation_details_representation_id_fkey"
        ]
    },
    {
        "schema": "PDB",
        "table": "entity_name_sys",
        "acls": "insert_update_all",
        "foreign_keys": [
            "entity_name_sys_entity_id_fkey",
            "entity_name_sys_structure_id_fkey"
        ]
    },
    {
        "schema": "PDB",
        "table": "ihm_ensemble_sub_sample",
        "acls": "insert_update_all",
        "foreign_keys": [
            "ihm_ensemble_sub_sample_ihm_ensemble_info_combo1_fkey",
            "ihm_ensemble_sub_sample_ihm_external_files_combo2_fkey",
            "ihm_ensemble_sub_sample_ihm_model_group_combo2_fkey",
            "ihm_ensemble_sub_sample_structure_id_fkey"
        ]
    },
    {
        "schema": "PDB",
        "table": "ihm_starting_model_details",
        "acls": "insert_update_all",
        "foreign_keys": [
            "ihm_starting_model_details_entity_poly_segment_id_fk",
            "ihm_starting_model_details_entity_id_fkey",
            "ihm_starting_model_details_starting_model_source_fkey",
            "ihm_starting_model_details_entity_poly_segment_id_fkey",
            "ihm_starting_model_details_asym_id_fkey",
            "ihm_starting_model_details_dataset_list_id_fkey",
            "ihm_starting_model_details_structure_id_fkey"
        ]
    },
    {
        "schema": "PDB",
        "table": "entity_poly",
        "acls": "insert_update_all",
        "foreign_keys": [
            "entity_poly_nstd_chirality_fkey",
            "entity_poly_pdbx_sequence_evidence_code_fkey",
            "entity_poly_entity_id_fkey",
            "entity_poly_structure_id_fkey",
            "entity_poly_nstd_monomer_fkey",
            "entity_poly_type_fkey",
            "entity_poly_nstd_linkage_fkey"
        ]
    },
    {
        "schema": "PDB",
        "table": "ihm_struct_assembly_class_link",
        "acls": "insert_update_all",
        "foreign_keys": [
            "ihm_struct_assembly_class_link_class_id_fkey",
            "ihm_struct_assembly_class_link_structure_id_fkey",
            "ihm_struct_assembly_class_link_assembly_id_fkey"
        ]
    },
    {
        "schema": "PDB",
        "table": "pdbx_protein_info",
        "acls": "insert_update_all",
        "foreign_keys": [
            "pdbx_protein_info_structure_id_fkey"
        ]
    },
    {
        "schema": "PDB",
        "table": "ihm_cross_link_restraint",
        "acls": "insert_update_all",
        "foreign_keys": [
            "ihm_cross_link_restraint_mm_poly_res_label_2_fkey",
            "ihm_cross_link_restraint_model_granularity_fkey",
            "ihm_cross_link_restraint_asym_id_2_fkey",
            "ihm_cross_link_restraint_pseudo_site_flag_fkey",
            "ihm_cross_link_restraint_structure_id_fkey",
            "ihm_cross_link_restraint_group_id_fkey",
            "ihm_cross_link_restraint_asym_id_1_fkey",
            "ihm_cross_link_restraint_restraint_type_fkey",
            "ihm_cross_link_restraint_conditional_crosslink_flag_fkey",
            "ihm_cross_link_restraint_mm_poly_res_label_1_fkey"
        ]
    },
    {
        "schema": "PDB",
        "table": "Entry_mmCIF_File",
        "acls": "insert_update_all",
        "foreign_keys": [
            "Entry_mmCIF_File_Structure_Id_fkey"
        ]
    },
    {
        "schema": "PDB",
        "table": "ihm_struct_assembly_details",
        "acls": "insert_update_all",
        "foreign_keys": [
            "ihm_struct_assembly_details_entity_poly_segment_id_fkey",
            "ihm_struct_assembly_details_entity_poly_segment_id_fk",
            "ihm_struct_assembly_details_asym_id_fkey",
            "ihm_struct_assembly_details_parent_assembly_id_fkey",
            "ihm_struct_assembly_details_assembly_id_fkey",
            "ihm_struct_assembly_details_structure_id_fkey",
            "ihm_struct_assembly_details_entity_id_fkey"
        ]
    },
    {
        "schema": "PDB",
        "table": "pdbx_inhibitor_info",
        "acls": "insert_update_all",
        "foreign_keys": [
            "pdbx_inhibitor_info_structure_id_fkey"
        ]
    },
    {
        "schema": "PDB",
        "table": "audit_conform",
        "acls": "insert_update_all",
        "foreign_keys": [
            "audit_conform_structure_id_fkey"
        ]
    },
    {
        "schema": "PDB",
        "table": "software",
        "acls": "insert_update_all",
        "foreign_keys": [
            "software_citation_id_fk",
            "software_type_fkey",
            "software_structure_id_fkey",
            "software_citation_id_fkey"
        ]
    },
    {
        "schema": "PDB",
        "table": "ihm_dataset_related_db_reference",
        "acls": "insert_update_all",
        "foreign_keys": [
            "ihm_dataset_related_db_reference_db_name_fkey",
            "ihm_dataset_related_db_reference_dataset_list_id_fkey",
            "ihm_dataset_related_db_reference_structure_id_fkey"
        ]
    },
    {
        "schema": "PDB",
        "table": "ihm_starting_comparative_models",
        "acls": "insert_update_all",
        "foreign_keys": [
            "ihm_starting_comparative_models_alignment_file_id_fkey",
            "ihm_starting_comparative_models_starting_model_id_fkey",
            "ihm_starting_comparative_models_template_dataset_list_id_fkey",
            "ihm_starting_comparative_models_alignment_file_id_fk",
            "ihm_starting_comparative_models_structure_id_fkey",
            "starting_comparative_models_template_sequence_id_denom_fkey"
        ]
    },
    {
        "schema": "PDB",
        "table": "ihm_external_files",
        "acls": "insert_update_all",
        "foreign_keys": [
            "ihm_external_files_content_type_fkey",
            "ihm_external_files_structure_id_fkey",
            "ihm_external_files_file_format_fkey",
            "ihm_external_files_reference_id_fkey"
        ]
    },
    {
        "schema": "PDB",
        "table": "ihm_predicted_contact_restraint",
        "acls": "insert_update_all",
        "foreign_keys": [
            "ihm_predicted_contact_restraint_rep_atom_1_fkey",
            "ihm_predicted_contact_restraint_software_id_fkey",
            "ihm_predicted_contact_restraint_model_granularity_fkey",
            "ihm_predicted_contact_restraint_rep_atom_2_fkey",
            "ihm_predicted_contact_restraint_restraint_type_fkey",
            "ihm_predicted_contact_restraint_structure_id_fkey",
            "ihm_predicted_contact_restraint_dataset_list_id_fkey",
            "ihm_predicted_contact_restraint_asym_id_1_fkey",
            "ihm_predicted_contact_restraint_mm_poly_res_label_2_fkey",
            "ihm_predicted_contact_restraint_software_id_fk",
            "ihm_predicted_contact_restraint_mm_poly_res_label_1_fkey",
            "ihm_predicted_contact_restraint_asym_id_2_fkey"
        ]
    },
    {
        "schema": "PDB",
        "table": "ihm_geometric_object_list",
        "acls": "insert_update_all",
        "foreign_keys": [
            "ihm_geometric_object_list_object_type_fkey",
            "ihm_geometric_object_list_structure_id_fkey"
        ]
    },
    {
        "schema": "PDB",
        "table": "ihm_interface_residue_feature",
        "acls": "insert_update_all",
        "foreign_keys": [
            "ihm_interface_residue_feature_binding_partner_asym_id_fk",
            "ihm_interface_residue_feature_feature_id_fkey",
            "ihm_interface_residue_feature_structure_id_fkey",
            "ihm_interface_residue_feature_dataset_list_id_fk",
            "ihm_interface_residue_feature_binding_partner_entity_id_fkey",
            "ihm_interface_residue_feature_dataset_list_id_fkey",
            "ihm_interface_residue_feature_binding_partner_asym_id_fkey"
        ]
    },
    {
        "schema": "PDB",
        "table": "ihm_geometric_object_torus",
        "acls": "insert_update_all",
        "foreign_keys": [
            "ihm_geometric_object_torus_transformation_id_fkey",
            "ihm_geometric_object_torus_structure_id_fkey",
            "ihm_geometric_object_torus_transformation_id_fk",
            "ihm_geometric_object_torus_object_id_fkey",
            "ihm_geometric_object_torus_center_id_fkey"
        ]
    },
    {
        "schema": "PDB",
        "table": "ihm_cross_link_list",
        "acls": "insert_update_all",
        "foreign_keys": [
            "ihm_cross_link_list_dataset_list_id_fkey",
            "ihm_cross_link_list_linker_chem_comp_descriptor_id_fk",
            "ihm_cross_link_list_linker_type_fkey",
            "ihm_cross_link_list_mm_poly_res_label_2_fkey",
            "ihm_cross_link_list_structure_id_fkey",
            "ihm_cross_link_list_linker_chem_comp_descriptor_id_fkey",
            "ihm_cross_link_list_mm_poly_res_label_1_fkey"
        ]
    },
    {
        "schema": "PDB",
        "table": "ihm_derived_angle_restraint",
        "acls": "insert_update_all",
        "foreign_keys": [
            "ihm_derived_angle_restraint_Entry_Related_File_fkey",
            "ihm_derived_angle_restraint_ihm_dataset_list_combo1_fkey",
            "ihm_derived_angle_restraint_ihm_feature_list_1_combo1_fkey",
            "ihm_derived_angle_restraint_group_conditionality_fkey",
            "ihm_derived_angle_restraint_structure_id_fkey",
            "ihm_derived_angle_restraint_restraint_type_fkey",
            "ihm_derived_angle_restraint_ihm_feature_list_2_combo1_fkey",
            "ihm_derived_angle_restraint_ihm_feature_list_3_combo1_fkey"
        ]
    },
    {
        "schema": "PDB",
        "table": "ihm_model_representation",
        "acls": "insert_update_all",
        "foreign_keys": [
            "ihm_model_representation_structure_id_fkey"
        ]
    },
    {
        "schema": "PDB",
        "table": "ihm_cross_link_result_parameters",
        "acls": "insert_update_all",
        "foreign_keys": [
            "ihm_cross_link_result_parameters_model_id_fkey",
            "ihm_cross_link_result_parameters_structure_id_fkey",
            "ihm_cross_link_result_parameters_restraint_id_fkey"
        ]
    },
    {
        "schema": "PDB",
        "table": "entry",
        "acls": "insert_update_all",
        "foreign_keys": [
            "entry_process_status_fkey"
        ]
    },
    {
        "schema": "PDB",
        "table": "ihm_ensemble_info",
        "acls": "insert_update_all",
        "foreign_keys": [
            "ihm_ensemble_info_ensemble_clustering_feature_fkey",
            "ihm_ensemble_info_post_process_id_fk",
            "ihm_ensemble_info_model_group_id_fk",
            "ihm_ensemble_info_model_group_id_fkey",
            "ihm_ensemble_info_sub_sample_flag_fkey",
            "ihm_ensemble_info_sub_sampling_type_fkey",
            "ihm_ensemble_info_post_process_id_fkey",
            "ihm_ensemble_info_ensemble_clustering_method_fkey",
            "ihm_ensemble_info_ensemble_file_id_fk",
            "ihm_ensemble_info_structure_id_fkey",
            "ihm_ensemble_info_ensemble_file_id_fkey"
        ]
    },
    {
        "schema": "PDB",
        "table": "ihm_dataset_group",
        "acls": "insert_update_all",
        "foreign_keys": [
            "ihm_dataset_group_application_fkey",
            "ihm_dataset_group_structure_id_fkey"
        ]
    },
    {
        "schema": "PDB",
        "table": "ihm_modeling_protocol",
        "acls": "insert_update_all",
        "foreign_keys": [
            "ihm_modeling_protocol_structure_id_fkey"
        ]
    },
    {
        "schema": "PDB",
        "table": "ihm_modeling_post_process",
        "acls": "insert_update_all",
        "foreign_keys": [
            "ihm_modeling_post_process_software_id_fk",
            "ihm_modeling_post_process_type_fkey",
            "ihm_modeling_post_process_script_file_id_fk",
            "ihm_modeling_post_process_protocol_id_fkey",
            "ihm_modeling_post_process_feature_fkey",
            "ihm_modeling_post_process_dataset_group_id_fk",
            "ihm_modeling_post_process_script_file_id_fkey",
            "ihm_modeling_post_process_struct_assembly_id_fk",
            "ihm_modeling_post_process_dataset_group_id_fkey",
            "ihm_modeling_post_process_software_id_fkey",
            "ihm_modeling_post_process_struct_assembly_id_fkey",
            "ihm_modeling_post_process_structure_id_fkey"
        ]
    },
    {
        "schema": "PDB",
        "table": "ihm_2dem_class_average_restraint",
        "acls": "insert_update_all",
        "foreign_keys": [
            "ihm_2dem_class_average_restraint_image_segment_flag_fkey",
            "ihm_2dem_class_average_restraint_structure_id_fkey",
            "ihm_2dem_class_average_restraint_dataset_list_id_fkey",
            "ihm_2dem_class_average_restraint_struct_assembly_id_fkey"
        ]
    },
    {
        "schema": "PDB",
        "table": "ihm_entity_poly_segment",
        "acls": "insert_update_all",
        "foreign_keys": [
            "ihm_entity_poly_segment_mm_poly_res_label_begin_fkey",
            "ihm_entity_poly_segment_mm_poly_res_label_end_fkey",
            "ihm_entity_poly_segment_structure_id_fkey"
        ]
    },
    {
        "schema": "PDB",
        "table": "ihm_poly_probe_position",
        "acls": "insert_update_all",
        "foreign_keys": [
            "ihm_poly_probe_position_mut_res_chem_comp_id_fk",
            "ihm_poly_probe_position_mod_res_chem_comp_descriptor_id_fkey",
            "ihm_poly_probe_position_mm_poly_res_label_fkey",
            "ihm_poly_probe_position_structure_id_fkey",
            "ihm_poly_probe_position_mod_res_chem_comp_descriptor_id_fk",
            "ihm_poly_probe_position_mutation_flag_fkey",
            "ihm_poly_probe_position_modification_flag_fkey",
            "ihm_poly_probe_position_mut_res_chem_comp_id_fkey"
        ]
    },
    {
        "schema": "PDB",
        "table": "ihm_localization_density_files",
        "acls": "insert_update_all",
        "foreign_keys": [
            "ihm_localization_density_files_file_id_fkey",
            "ihm_localization_density_files_entity_poly_segment_id_fkey",
            "ihm_localization_density_files_structure_id_fkey",
            "ihm_localization_density_files_ensemble_id_fkey",
            "ihm_localization_density_files_entity_id_fk",
            "ihm_localization_density_files_asym_id_fk",
            "ihm_localization_density_files_entity_poly_segment_id_fk",
            "ihm_localization_density_files_asym_id_fkey",
            "ihm_localization_density_files_entity_id_fkey"
        ]
    },
    {
        "schema": "PDB",
        "table": "ihm_related_datasets",
        "acls": "insert_update_all",
        "foreign_keys": [
            "ihm_related_datasets_dataset_list_id_primary_fkey",
            "ihm_related_datasets_dataset_list_id_derived_fkey",
            "ihm_related_datasets_structure_id_fkey",
            "ihm_related_datasets_ihm_data_transformation_combo2_fkey"
        ]
    },
    {
        "schema": "PDB",
        "table": "ihm_pseudo_site",
        "acls": "insert_update_all",
        "foreign_keys": [
            "ihm_pseudo_site_structure_id_fkey",
            "ihm_pseudo_site_Entry_Related_File_fkey"
        ]
    },
    {
        "schema": "PDB",
        "table": "ihm_multi_state_modeling",
        "acls": "insert_update_all",
        "foreign_keys": [
            "ihm_multi_state_modeling_experiment_type_fkey",
            "ihm_multi_state_modeling_structure_id_fkey"
        ]
    },
    {
        "schema": "PDB",
        "table": "ihm_non_poly_feature",
        "acls": "insert_update_all",
        "foreign_keys": [
            "ihm_non_poly_feature_structure_id_fkey",
            "ihm_non_poly_feature_asym_id_fkey",
            "ihm_non_poly_feature_comp_id_fkey",
            "ihm_non_poly_feature_asym_id_fk",
            "ihm_non_poly_feature_entity_id_fkey",
            "ihm_non_poly_feature_feature_id_fkey"
        ]
    },
    {
        "schema": "PDB",
        "table": "Entry_Related_File",
        "acls": "insert_update_all",
        "foreign_keys": [
            "Entry_Related_File_entry_id_fkey",
            "Entry_Related_File_workflow_status_fkey",
            "Entry_Related_File_File_Format_fkey",
            "Entry_Related_File_File_Type_fkey",
            "Entry_Related_File_process_status_fkey"
        ]
    },
    {
        "schema": "PDB",
        "table": "ihm_chemical_component_descriptor",
        "acls": "insert_update_all",
        "foreign_keys": [
            "ihm_chemical_component_descriptor_structure_id_fkey"
        ]
    },
    {
        "schema": "PDB",
        "table": "ihm_geometric_object_transformation",
        "acls": "insert_update_all",
        "foreign_keys": [
            "ihm_geometric_object_transformation_structure_id_fkey"
        ]
    },
    {
        "schema": "PDB",
        "table": "ihm_pseudo_site_feature",
        "acls": "insert_update_all",
        "foreign_keys": [
            "ihm_pseudo_site_feature_ihm_feature_list_combo1_fkey",
            "ihm_pseudo_site_feature_structure_id_fkey",
            "ihm_pseudo_site_feature_ihm_pseudo_site_combo1_fkey"
        ]
    },
    {
        "schema": "PDB",
        "table": "ihm_model_group_link",
        "acls": "insert_update_all",
        "foreign_keys": [
            "ihm_model_group_link_group_id_fkey",
            "ihm_model_group_link_model_id_fkey",
            "ihm_model_group_link_structure_id_fkey"
        ]
    },
    {
        "schema": "PDB",
        "table": "atom_type",
        "acls": "insert_update_all",
        "foreign_keys": [
            "atom_type_structure_id_fkey"
        ]
    },
    {
        "schema": "PDB",
        "table": "ihm_derived_dihedral_restraint",
        "acls": "insert_update_all",
        "foreign_keys": [
            "ihm_derived_dihedral_restraint_ihm_feature_list_2_combo1_fkey",
            "ihm_derived_dihedral_restraint_Entry_Related_File_fkey",
            "ihm_derived_dihedral_restraint_ihm_feature_list_4_combo1_fkey",
            "ihm_derived_dihedral_restraint_restraint_type_fkey",
            "ihm_derived_dihedral_restraint_group_conditionality_fkey",
            "ihm_derived_dihedral_restraint_ihm_feature_list_3_combo1_fkey",
            "ihm_derived_dihedral_restraint_ihm_feature_list_1_combo1_fkey",
            "ihm_derived_dihedral_restraint_ihm_dataset_list_combo1_fkey",
            "ihm_derived_dihedral_restraint_structure_id_fkey"
        ]
    },
    {
        "schema": "PDB",
        "table": "ihm_residues_not_modeled",
        "acls": "insert_update_all",
        "foreign_keys": [
            "ihm_residues_not_modeled_model_id_fkey",
            "ihm_residues_not_modeled_structure_id_fkey",
            "ihm_residues_not_modeled_reason_fkey",
            "ihm_residues_not_modeled_mm_poly_res_label_begin_fkey",
            "ihm_residues_not_modeled_mm_poly_res_label_end_fkey",
            "ihm_residues_not_modeled_asym_id_fkey"
        ]
    },
    {
        "schema": "PDB",
        "table": "ihm_2dem_class_average_fitting",
        "acls": "insert_update_all",
        "foreign_keys": [
            "ihm_2dem_class_average_fitting_model_id_fkey",
            "ihm_2dem_class_average_fitting_structure_id_fkey",
            "ihm_2dem_class_average_fitting_restraint_id_fkey"
        ]
    },
    {
        "schema": "PDB",
        "table": "ihm_dataset_list",
        "acls": "insert_update_all",
        "foreign_keys": [
            "ihm_dataset_list_database_hosted_fkey",
            "ihm_dataset_list_structure_id_fkey",
            "ihm_dataset_list_data_type_fkey"
        ]
    },
    {
        "schema": "PDB",
        "table": "struct",
        "acls": "insert_update_all",
        "foreign_keys": [
            "struct_pdbx_CASP_flag_fkey",
            "struct_entry_id_fkey"
        ]
    },
    {
        "schema": "PDB",
        "table": "pdbx_entity_poly_na_type",
        "acls": "insert_update_all",
        "foreign_keys": [
            "pdbx_entity_poly_na_type_structure_id_fkey",
            "pdbx_entity_poly_na_type_type_fkey",
            "pdbx_entity_poly_na_type_entity_id_fkey"
        ]
    },
    {
        "schema": "PDB",
        "table": "ihm_geometric_object_half_torus",
        "acls": "insert_update_all",
        "foreign_keys": [
            "ihm_geometric_object_half_torus_structure_id_fkey",
            "ihm_geometric_object_half_torus_section_fkey",
            "ihm_geometric_object_half_torus_object_id_fkey"
        ]
    },
    {
        "schema": "PDB",
        "table": "audit_author",
        "acls": "insert_update_all",
        "foreign_keys": [
            "audit_author_structure_id_fkey"
        ]
    },
    {
        "schema": "PDB",
        "table": "entity_src_gen",
        "acls": "insert_update_all",
        "foreign_keys": [
            "entity_src_gen_entity_id_fkey",
            "entity_src_gen_structure_id_fkey",
            "entity_src_gen_pdbx_alt_source_flag_fkey"
        ]
    },
    {
        "schema": "PDB",
        "table": "ihm_struct_assembly_class",
        "acls": "insert_update_all",
        "foreign_keys": [
            "ihm_struct_assembly_class_type_fkey",
            "ihm_struct_assembly_class_structure_id_fkey"
        ]
    },
    {
        "schema": "PDB",
        "table": "ihm_geometric_object_distance_restraint",
        "acls": "insert_update_all",
        "foreign_keys": [
            "geometric_object_distance_restraint_group_condition_fkey",
            "ihm_geometric_object_distance_restraint_structure_id_fkey",
            "ihm_geometric_object_distance_restraint_dataset_list_id_fk",
            "ihm_geometric_object_distance_restraint_object_id_fkey",
            "geometric_object_distance_restraint_object_character_fkey",
            "ihm_geometric_object_distance_restraint_dataset_list_id_fkey",
            "ihm_geometric_object_distance_restraint_restraint_type_fkey",
            "ihm_geometric_object_distance_restraint_feature_id_fkey"
        ]
    },
    {
        "schema": "PDB",
        "table": "pdbx_entity_nonpoly",
        "acls": "insert_update_all",
        "foreign_keys": [
            "pdbx_entity_nonpoly_comp_id_fk",
            "pdbx_entity_nonpoly_structure_id_fkey",
            "pdbx_entity_nonpoly_entity_id_fkey",
            "pdbx_entity_nonpoly_comp_id_fkey"
        ]
    },
    {
        "schema": "PDB",
        "table": "ihm_multi_state_model_group_link",
        "acls": "insert_update_all",
        "foreign_keys": [
            "ihm_multi_state_model_group_link_model_group_id_fkey",
            "ihm_multi_state_model_group_link_state_id_fkey",
            "ihm_multi_state_model_group_link_structure_id_fkey"
        ]
    },
    {
        "schema": "PDB",
        "table": "ihm_dataset_group_link",
        "acls": "insert_update_all",
        "foreign_keys": [
            "ihm_dataset_group_link_structure_id_fkey",
            "ihm_dataset_group_link_dataset_list_id_fkey",
            "ihm_dataset_group_link_group_id_fkey"
        ]
    },
    {
        "schema": "PDB",
        "table": "ihm_hdx_restraint",
        "acls": "insert_update_all",
        "foreign_keys": [
            "ihm_hdx_restraint_structure_id_fkey",
            "ihm_hdx_restraint_ihm_dataset_list_combo1_fkey",
            "ihm_hdx_restraint_ihm_feature_list_combo1_fkey",
            "ihm_hdx_restraint_Entry_Related_File_fkey"
        ]
    },
    {
        "schema": "PDB",
        "table": "struct_ref",
        "acls": "insert_update_all",
        "foreign_keys": [
            "struct_ref_entity_combo1_fkey",
            "struct_ref_structure_id_fkey",
            "struct_ref_db_name_fkey"
        ]
    },
    {
        "schema": "PDB",
        "table": "ihm_geometric_object_sphere",
        "acls": "insert_update_all",
        "foreign_keys": [
            "ihm_geometric_object_sphere_transformation_id_fkey",
            "ihm_geometric_object_sphere_object_id_fkey",
            "ihm_geometric_object_sphere_transformation_id_fk",
            "ihm_geometric_object_sphere_structure_id_fkey",
            "ihm_geometric_object_sphere_center_id_fkey"
        ]
    },
    {
        "schema": "PDB",
        "table": "ihm_poly_probe_conjugate",
        "acls": "insert_update_all",
        "foreign_keys": [
            "ihm_poly_probe_conjugate_chem_comp_descriptor_id_fkey",
            "ihm_poly_probe_conjugate_probe_id_fkey",
            "ihm_poly_probe_conjugate_chem_comp_descriptor_id_fk",
            "ihm_poly_probe_conjugate_position_id_fkey",
            "ihm_poly_probe_conjugate_structure_id_fkey",
            "ihm_poly_probe_conjugate_dataset_list_id_fkey",
            "ihm_poly_probe_conjugate_ambiguous_stoichiometry_flag_fkey"
        ]
    },
    {
        "schema": "PDB",
        "table": "ihm_modeling_protocol_details",
        "acls": "insert_update_all",
        "foreign_keys": [
            "ihm_modeling_protocol_details_software_id_fk",
            "ihm_modeling_protocol_details_multi_scale_flag_fkey",
            "ihm_modeling_protocol_details_structure_id_fkey",
            "ihm_modeling_protocol_details_dataset_group_id_fkey",
            "ihm_modeling_protocol_details_struct_assembly_id_fkey",
            "ihm_modeling_protocol_details_script_file_id_fk",
            "ihm_modeling_protocol_details_ensemble_flag_fkey",
            "ihm_modeling_protocol_details_software_id_fkey",
            "ihm_modeling_protocol_details_protocol_id_fkey",
            "ihm_modeling_protocol_details_dataset_group_id_fk",
            "ihm_modeling_protocol_details_struct_assembly_id_fk",
            "ihm_modeling_protocol_details_multi_state_flag_fkey",
            "ihm_modeling_protocol_details_script_file_id_fkey",
            "ihm_modeling_protocol_details_ordered_flag_fkey"
        ]
    },
    {
        "schema": "PDB",
        "table": "ihm_dataset_external_reference",
        "acls": "insert_update_all",
        "foreign_keys": [
            "ihm_dataset_external_reference_dataset_list_id_fkey",
            "ihm_dataset_external_reference_file_id_fkey",
            "ihm_dataset_external_reference_structure_id_fkey"
        ]
    },
    {
        "schema": "PDB",
        "table": "ihm_ligand_probe",
        "acls": "insert_update_all",
        "foreign_keys": [
            "ihm_ligand_probe_structure_id_fkey",
            "ihm_ligand_probe_entity_id_fkey",
            "ihm_ligand_probe_dataset_list_id_fkey",
            "ihm_ligand_probe_probe_id_fkey"
        ]
    },
    {
        "schema": "PDB",
        "table": "ihm_3dem_restraint",
        "acls": "insert_update_all",
        "foreign_keys": [
            "ihm_3dem_restraint_struct_assembly_id_fkey",
            "ihm_3dem_restraint_dataset_list_id_fkey",
            "ihm_3dem_restraint_model_id_fkey",
            "ihm_3dem_restraint_map_segment_flag_fkey",
            "ihm_3dem_restraint_structure_id_fkey",
            "ihm_3dem_restraint_fitting_method_citation_id_fkey",
            "ihm_3dem_restraint_fitting_method_citation_id_fk"
        ]
    },
    {
        "schema": "PDB",
        "table": "ihm_probe_list",
        "acls": "insert_update_all",
        "foreign_keys": [
            "ihm_probe_list_probe_origin_fkey",
            "ihm_probe_list_reactive_probe_chem_comp_descriptor_id_fk",
            "ihm_probe_list_probe_link_type_fkey",
            "ihm_probe_list_structure_id_fkey",
            "ihm_probe_list_reactive_probe_chem_comp_descriptor_id_fkey",
            "ihm_probe_list_reactive_probe_flag_fkey",
            "ihm_probe_list_probe_chem_comp_descriptor_id_fk",
            "ihm_probe_list_probe_chem_comp_descriptor_id_fkey"
        ]
    },
    {
        "schema": "PDB",
        "table": "ihm_hydroxyl_radical_fp_restraint",
        "acls": "insert_update_all",
        "foreign_keys": [
            "ihm_hydroxyl_radical_fp_restraint_asym_id_fkey",
            "ihm_hydroxyl_radical_fp_restraint_dataset_list_id_fkey",
            "ihm_hydroxyl_radical_fp_restraint_software_id_fkey",
            "ihm_hydroxyl_radical_fp_restraint_software_id_fk",
            "ihm_hydroxyl_radical_fp_restraint_structure_id_fkey",
            "ihm_hydroxyl_radical_fp_restraint_mm_poly_res_label_fkey"
        ]
    },
    {
        "schema": "PDB",
        "table": "ihm_data_transformation",
        "acls": "insert_update_all",
        "foreign_keys": [
            "ihm_data_transformation_structure_id_fkey"
        ]
    },
    {
        "schema": "PDB",
        "table": "struct_ref_seq",
        "acls": "insert_update_all",
        "foreign_keys": [
            "struct_ref_seq_struct_ref_combo1_fkey",
            "struct_ref_seq_structure_id_fkey"
        ]
    },
    {
        "schema": "PDB",
        "table": "ihm_model_list",
        "acls": "insert_update_all",
        "foreign_keys": [
            "ihm_model_list_protocol_id_fkey",
            "ihm_model_list_representation_id_fkey",
            "ihm_model_list_structure_id_fkey",
            "ihm_model_list_assembly_id_fkey"
        ]
    },
    {
        "schema": "PDB",
        "table": "entity_name_com",
        "acls": "insert_update_all",
        "foreign_keys": [
            "entity_name_com_entity_id_fkey",
            "entity_name_com_structure_id_fkey"
        ]
    },
    {
        "schema": "PDB",
        "table": "ihm_struct_assembly",
        "acls": "insert_update_all",
        "foreign_keys": [
            "ihm_struct_assembly_structure_id_fkey"
        ]
    },
    {
        "schema": "PDB",
        "table": "ihm_external_reference_info",
        "acls": "insert_update_all",
        "foreign_keys": [
            "ihm_external_reference_info_refers_to_fkey",
            "ihm_external_reference_info_structure_id_fkey",
            "ihm_external_reference_info_reference_type_fkey"
        ]
    },
    {
        "schema": "PDB",
        "table": "chem_comp_atom",
        "acls": "insert_update_all",
        "foreign_keys": [
            "chem_comp_atom_pdbx_polymer_type_fkey",
            "chem_comp_atom_pdbx_stereo_config_fkey",
            "chem_comp_atom_pdbx_leaving_atom_flag_fkey",
            "chem_comp_atom_substruct_code_fkey",
            "chem_comp_atom_comp_id_fkey",
            "chem_comp_atom_pdbx_aromatic_flag_fkey",
            "chem_comp_atom_structure_id_fkey"
        ]
    },
    {
        "schema": "PDB",
        "table": "entity",
        "acls": "insert_update_all",
        "foreign_keys": [
            "entity_src_method_fkey",
            "entity_structure_id_fkey",
            "entity_type_fkey"
        ]
    },
    {
        "schema": "PDB",
        "table": "ihm_cross_link_pseudo_site",
        "acls": "insert_update_all",
        "foreign_keys": [
            "ihm_cross_link_pseudo_site_structure_id_fkey",
            "ihm_cross_link_pseudo_site_ihm_model_list_combo2_fkey",
            "ihm_cross_link_pseudo_site_cross_link_partner_fkey",
            "ihm_cross_link_pseudo_site_ihm_cross_link_restraint_combo1_fkey",
            "ihm_cross_link_pseudo_site_ihm_pseudo_site_combo1_fkey",
            "ihm_cross_link_pseudo_site_Entry_Related_File_fkey"
        ]
    },
    {
        "schema": "PDB",
        "table": "ihm_sas_restraint",
        "acls": "insert_update_all",
        "foreign_keys": [
            "ihm_sas_restraint_structure_id_fkey",
            "ihm_sas_restraint_dataset_list_id_fkey",
            "ihm_sas_restraint_model_id_fkey",
            "ihm_sas_restraint_struct_assembly_id_fkey",
            "ihm_sas_restraint_profile_segment_flag_fkey",
            "ihm_sas_restraint_fitting_state_fkey"
        ]
    },
    {
        "schema": "PDB",
        "table": "Entry_Related_File_Templates",
        "acls": "insert_update_all",
        "foreign_keys": [
            "Entry_Template_File_File_Type_fkey"
        ]
    },
    {
        "schema": "PDB",
        "table": "ihm_starting_model_seq_dif",
        "acls": "insert_update_all",
        "foreign_keys": [
            "ihm_starting_model_seq_dif_starting_model_id_fkey",
            "ihm_starting_model_seq_dif_asym_id_fkey",
            "ihm_starting_model_seq_dif_mm_poly_res_label_fkey",
            "ihm_starting_model_seq_dif_structure_id_fkey"
        ]
    },
    {
        "schema": "PDB",
        "table": "ihm_geometric_object_center",
        "acls": "insert_update_all",
        "foreign_keys": [
            "ihm_geometric_object_center_structure_id_fkey"
        ]
    },
    {
        "schema": "PDB",
        "table": "struct_asym",
        "acls": "insert_update_all",
        "foreign_keys": [
            "struct_asym_structure_id_fkey",
            "struct_asym_entity_id_fkey",
            "struct_asym_pdbx_type_fkey",
            "struct_asym_pdbx_blank_PDB_chainid_flag_fkey"
        ]
    },
    {
        "schema": "PDB",
        "table": "ihm_poly_atom_feature",
        "acls": "insert_update_all",
        "foreign_keys": [
            "ihm_poly_atom_feature_feature_id_fkey",
            "ihm_poly_atom_feature_asym_id_fkey",
            "ihm_poly_atom_feature_asym_id_fk",
            "ihm_poly_atom_feature_structure_id_fkey",
            "ihm_poly_atom_feature_mm_poly_res_label_fkey"
        ]
    },
    {
        "schema": "PDB",
        "table": "struct_ref_seq_dif",
        "acls": "insert_update_all",
        "foreign_keys": [
            "struct_ref_seq_dif_struct_ref_seq_combo1_fkey",
            "struct_ref_seq_dif_structure_id_fkey",
            "struct_ref_seq_dif_details_fkey"
        ]
    },
    {
        "schema": "PDB",
        "table": "entity_poly_seq",
        "acls": "insert_update_all",
        "foreign_keys": [
            "entity_poly_seq_structure_id_fkey",
            "entity_poly_seq_hetero_fkey",
            "entity_poly_seq_entity_id_fkey",
            "entity_poly_seq_mon_id_fkey"
        ]
    },
    {
        "schema": "PDB",
        "table": "ihm_starting_computational_models",
        "acls": "insert_update_all",
        "foreign_keys": [
            "ihm_starting_computational_models_script_file_id_fkey",
            "ihm_starting_computational_models_structure_id_fkey",
            "ihm_starting_computational_models_starting_model_id_fkey",
            "ihm_starting_computational_models_software_id_fkey",
            "ihm_starting_computational_models_script_file_id_fk",
            "ihm_starting_computational_models_software_id_fk"
        ]
    },
    {
        "schema": "PDB",
        "table": "chem_comp",
        "acls": "insert_update_all",
        "foreign_keys": [
            "chem_comp_type_fkey",
            "chem_comp_structure_id_fkey",
            "chem_comp_mon_nstd_flag_fkey"
        ]
    },
    {
        "schema": "PDB",
        "table": "ihm_derived_distance_restraint",
        "acls": "insert_update_all",
        "foreign_keys": [
            "ihm_derived_distance_restraint_restraint_type_fkey",
            "ihm_derived_distance_restraint_feature_id_2_fkey",
            "ihm_derived_distance_restraint_feature_id_1_fkey",
            "ihm_derived_distance_restraint_dataset_list_id_fkey",
            "ihm_derived_distance_restraint_dataset_list_id_fk",
            "ihm_derived_distance_restraint_group_conditionality_fkey",
            "ihm_derived_distance_restraint_structure_id_fkey"
        ]
    },
    {
        "schema": "PDB",
        "table": "pdbx_entry_details",
        "acls": "insert_update_all",
        "foreign_keys": [
            "pdbx_entry_details_entry_id_fkey"
        ]
    },
    {
        "schema": "PDB",
        "table": "ihm_geometric_object_axis",
        "acls": "insert_update_all",
        "foreign_keys": [
            "ihm_geometric_object_axis_transformation_id_fk",
            "ihm_geometric_object_axis_object_id_fkey",
            "ihm_geometric_object_axis_transformation_id_fkey",
            "ihm_geometric_object_axis_structure_id_fkey",
            "ihm_geometric_object_axis_axis_type_fkey"
        ]
    },
    {
        "schema": "PDB",
        "table": "ihm_geometric_object_plane",
        "acls": "insert_update_all",
        "foreign_keys": [
            "ihm_geometric_object_plane_structure_id_fkey",
            "ihm_geometric_object_plane_plane_type_fkey",
            "ihm_geometric_object_plane_transformation_id_fkey",
            "ihm_geometric_object_plane_object_id_fkey",
            "ihm_geometric_object_plane_transformation_id_fk"
        ]
    },
    {
        "schema": "PDB",
        "table": "pdbx_ion_info",
        "acls": "insert_update_all",
        "foreign_keys": [
            "pdbx_ion_info_structure_id_fkey"
        ]
    },
    {
        "schema": "PDB",
        "table": "ihm_ordered_ensemble",
        "acls": "insert_update_all",
        "foreign_keys": [
            "ihm_ordered_ensemble_structure_id_fkey",
            "ihm_ordered_ensemble_model_group_id_begin_fkey",
            "ihm_ordered_ensemble_model_group_id_end_fkey"
        ]
    },
    {
        "schema": "PDB",
        "table": "ihm_poly_residue_feature",
        "acls": "insert_update_all",
        "foreign_keys": [
            "ihm_poly_residue_feature_mm_poly_res_label_begin_fkey",
            "ihm_poly_residue_feature_structure_id_fkey",
            "ihm_poly_residue_feature_asym_id_fk",
            "ihm_poly_residue_feature_mm_poly_res_label_end_fkey",
            "ihm_poly_residue_feature_asym_id_fkey",
            "ihm_poly_residue_feature_residue_range_granularity_fkey",
            "ihm_poly_residue_feature_rep_atom_fkey",
            "ihm_poly_residue_feature_interface_residue_flag_fkey",
            "ihm_poly_residue_feature_feature_id_fkey"
        ]
    },
    {
        "schema": "PDB",
        "table": "citation_author",
        "acls": "insert_update_all",
        "foreign_keys": [
            "citation_author_structure_id_fkey",
            "citation_author_citation_id_fkey"
        ]
    },
    {
        "schema": "PDB",
        "table": "ihm_model_representative",
        "acls": "insert_update_all",
        "foreign_keys": [
            "ihm_model_representative_model_id_fkey",
            "ihm_model_representative_model_group_id_fkey",
            "ihm_model_representative_structure_id_fkey",
            "ihm_model_representative_selection_criteria_fkey"
        ]
    },
    {
        "schema": "PDB",
        "table": "ihm_model_group",
        "acls": "insert_update_all",
        "foreign_keys": [
            "ihm_model_group_structure_id_fkey"
        ]
    },
    {
        "schema": "PDB",
        "table": "ihm_cross_link_result",
        "acls": "insert_update_all",
        "foreign_keys": [
            "ihm_cross_link_result_ensemble_id_fkey",
            "ihm_cross_link_result_restraint_id_fkey",
            "ihm_cross_link_result_structure_id_fkey"
        ]
    },
    {
        "schema": "PDB",
        "table": "citation",
        "acls": "insert_update_all",
        "foreign_keys": [
            "citation_structure_id_fkey"
        ]
    },
    {
        "schema": "PDB",
        "table": "ihm_feature_list",
        "acls": "insert_update_all",
        "foreign_keys": [
            "ihm_feature_list_feature_type_fkey",
            "ihm_feature_list_entity_type_fkey",
            "ihm_feature_list_structure_id_fkey"
        ]
    },
    {
        "schema": "PDB",
        "table": "entry",
        "acls": "insert_update_curator_writer",
        "foreign_keys": [
            "entry_workflow_status_fkey"
        ]
    }
]

"""
Foreign Keys ACL Bindings
"""
foreign_key_acl_bindings = [
    {
        "schema": "public",
        "table": "Catalog_Group",
        "acl_bindings": "set_owner",
        "foreign_keys": [
            "Catalog_Group_ID1"
        ]
    },
    {
        "schema": "PDB",
        "table": "entry",
        "acl_bindings": "submit_reader",
        "foreign_keys": [
            "entry_workflow_status_fkey"
        ]
    }
]
