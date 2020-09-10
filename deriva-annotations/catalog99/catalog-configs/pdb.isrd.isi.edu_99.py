import argparse
from deriva.core import ErmrestCatalog, AttrDict, get_credential
from deriva.utils.catalog.manage.update_catalog import CatalogUpdater, parse_args
from deriva.core.ermrest_config import tag as chaise_tags
import deriva.core.ermrest_model as em

groups = {
    'pdb-reader': 'https://auth.globus.org/8875a770-3c40-11e9-a8c8-0ee7d80087ee',
    'pdb-writer': 'https://auth.globus.org/c94a1e5c-3c40-11e9-a5d1-0aacc65bfe9a',
    'pdb-admin': 'https://auth.globus.org/0b98092c-3c41-11e9-a8c8-0ee7d80087ee',
    'pdb-curator': 'https://auth.globus.org/eef3e02a-3c40-11e9-9276-0edc9bdd56a6',
    'isrd-staff': 'https://auth.globus.org/176baec4-ed26-11e5-8e88-22000ab4b42b'
}

bulk_upload = {
    'asset_mappings': [
        {
            'asset_type': 'table',
            'ext_pattern': '^.*[.](?P<file_ext>json|csv)$',
            'file_pattern': '^((?!/assets/).)*/records/(?P<schema>WWW?)/(?P<table>Page)[.]',
            'target_table': ['WWW', 'Page'],
            'default_columns': ['RID', 'RCB', 'RMB', 'RCT', 'RMT']
        }, {
            'column_map': {
                'MD5': '{md5}',
                'URL': '{URI}',
                'Page': '{table_rid}',
                'Length': '{file_size}',
                'Filename': '{file_name}'
            },
            'dir_pattern': '^.*/(?P<schema>WWW)/(?P<table>Page)/(?P<key_column>.*)/',
            'ext_pattern': '^.*[.](?P<file_ext>.*)$',
            'file_pattern': '.*',
            'target_table': ['WWW', 'Page_Asset'],
            'checksum_types': ['md5'],
            'hatrac_options': {
                'versioned_uris': True
            },
            'hatrac_templates': {
                'hatrac_uri': '/hatrac/{schema}/{table}/{md5}.{file_name}'
            },
            'record_query_template': '/entity/{schema}:{table}_Asset/{table}={table_rid}/MD5={md5}/URL={URI_urlencoded}',
            'metadata_query_templates': [
                '/attribute/D:={schema}:{table}/RID={key_column}/table_rid:=D:RID'
            ]
        }
    ],
    'version_update_url': 'https://github.com/informatics-isi-edu/deriva-qt/releases',
    'version_compatibility': [['>=0.4.3', '<1.0.0']]
}

chaise_config = {
    'navbarMenu': {
        'newTab': False,
        'children': [
            {
                'name': 'PDB',
                'children': [
                    {
                        'name': '2DEM',
                        'children': [
                            {
                                'url': '/chaise/recordset/#99/PDB:ihm_2dem_class_average_fitting',
                                'name': 'Ihm 2DEM Class Average Fitting'
                            }, {
                                'url': '/chaise/recordset/#99/PDB:ihm_2dem_class_average_restraint',
                                'name': 'Ihm 2DEM Class Average Restraint'
                            }
                        ]
                    }, {
                        'name': '3DEM',
                        'children': [
                            {
                                'url': '/chaise/recordset/#99/PDB:ihm_3dem_restraint',
                                'name': 'Ihm 3DEM Restraint'
                            }
                        ]
                    }, {
                        'name': 'Audit Conform',
                        'children': [
                            {
                                'url': '/chaise/recordset/#99/PDB:audit_conform',
                                'name': 'Audit Conform'
                            }
                        ]
                    }, {
                        'name': 'Chemical Components',
                        'children': [
                            {
                                'url': '/chaise/recordset/#99/PDB:chem_comp',
                                'name': 'Chem Comp'
                            }, {
                                'url': '/chaise/recordset/#99/PDB:chem_comp_atom',
                                'name': 'Chem Comp Atom'
                            }
                        ]
                    }, {
                        'name': 'Chemical Crosslinks',
                        'children': [
                            {
                                'url': '/chaise/recordset/#99/PDB:ihm_cross_link_list',
                                'name': 'Ihm Cross Link List'
                            }, {
                                'url': '/chaise/recordset/#99/PDB:ihm_cross_link_restraint',
                                'name': 'Ihm Cross Link Restraint'
                            }, {
                                'url': '/chaise/recordset/#99/PDB:ihm_cross_link_result',
                                'name': 'Ihm Cross Link Result'
                            }, {
                                'url': '/chaise/recordset/#99/PDB:ihm_cross_link_result_parameters',
                                'name': 'Ihm Cross Link Result Parameters'
                            }
                        ]
                    }, {
                        'name': 'Citation, Authors and Software',
                        'children': [
                            {
                                'url': '/chaise/recordset/#99/PDB:audit_author',
                                'name': 'Audit Author'
                            }, {
                                'url': '/chaise/recordset/#99/PDB:citation',
                                'name': 'Citation'
                            }, {
                                'url': '/chaise/recordset/#99/PDB:citation_author',
                                'name': 'Citation Author'
                            }, {
                                'url': '/chaise/recordset/#99/PDB:software',
                                'name': 'Software'
                            }
                        ]
                    }, {
                        'name': 'Entry and Structure',
                        'children': [
                            {
                                'url': '/chaise/recordset/#99/PDB:entry',
                                'name': 'Entry'
                            }, {
                                'url': '/chaise/recordset/#99/PDB:struct',
                                'name': 'Struct'
                            }
                        ]
                    }, {
                        'name': 'EPR',
                        'children': [
                            {
                                'url': '/chaise/recordset/#99/PDB:ihm_epr_restraint',
                                'name': 'Ihm EPR Restraint'
                            }
                        ]
                    }, {
                        'name': 'Generic Distance Restraints',
                        'children': [
                            {
                                'url': '/chaise/recordset/#99/PDB:ihm_derived_distance_restraint',
                                'name': 'Ihm Derived Distance Restraint'
                            }, {
                                'url': '/chaise/recordset/#99/PDB:ihm_feature_list',
                                'name': 'Ihm Feature List'
                            }, {
                                'url': '/chaise/recordset/#99/PDB:ihm_interface_residue_feature',
                                'name': 'Ihm Interface Residue Feature'
                            }, {
                                'url': '/chaise/recordset/#99/PDB:ihm_non_poly_feature',
                                'name': 'Ihm Non Poly Feature'
                            }, {
                                'url': '/chaise/recordset/#99/PDB:ihm_poly_atom_feature',
                                'name': 'Ihm Poly Atom Feature'
                            }, {
                                'url': '/chaise/recordset/#99/PDB:ihm_poly_residue_feature',
                                'name': 'Ihm Poly Residue Feature'
                            }, {
                                'url': '/chaise/recordset/#99/PDB:ihm_pseudo_site_feature',
                                'name': 'Ihm Pseudo Site Feature'
                            }
                        ]
                    }, {
                        'name': 'Geometric Objects',
                        'children': [
                            {
                                'url': '/chaise/recordset/#99/PDB:ihm_geometric_object_axis',
                                'name': 'Ihm Geometric Object Axis'
                            }, {
                                'url': '/chaise/recordset/#99/PDB:ihm_geometric_object_center',
                                'name': 'Ihm Geometric Object Center'
                            }, {
                                'url': '/chaise/recordset/#99/PDB:ihm_geometric_object_distance_restraint',
                                'name': 'Ihm Geometric Object Distance Restraint'
                            }, {
                                'url': '/chaise/recordset/#99/PDB:ihm_geometric_object_half_torus',
                                'name': 'Ihm Geometric Object Half Torus'
                            }, {
                                'url': '/chaise/recordset/#99/PDB:ihm_geometric_object_list',
                                'name': 'Ihm Geometric Object List'
                            }, {
                                'url': '/chaise/recordset/#99/PDB:ihm_geometric_object_plane',
                                'name': 'Ihm Geometric Object Plane'
                            }, {
                                'url': '/chaise/recordset/#99/PDB:ihm_geometric_object_sphere',
                                'name': 'Ihm Geometric Object Sphere'
                            }, {
                                'url': '/chaise/recordset/#99/PDB:ihm_geometric_object_torus',
                                'name': 'Ihm Geometric Object Torus'
                            }, {
                                'url': '/chaise/recordset/#99/PDB:ihm_geometric_object_transformation',
                                'name': 'Ihm Geometric Object Transformation'
                            }
                        ]
                    }, {
                        'name': 'Hydroxyl Radical Foot Printing',
                        'children': [
                            {
                                'url': '/chaise/recordset/#99/PDB:ihm_hydroxyl_radical_fp_restraint',
                                'name': 'Ihm Hydroxyl Radical Fp Restraint'
                            }
                        ]
                    }, {
                        'name': 'Input Data',
                        'children': [
                            {
                                'url': '/chaise/recordset/#99/PDB:ihm_dataset_external_reference',
                                'name': 'Ihm Dataset External Reference'
                            }, {
                                'url': '/chaise/recordset/#99/PDB:ihm_dataset_group',
                                'name': 'Ihm Dataset Group'
                            }, {
                                'url': '/chaise/recordset/#99/PDB:ihm_dataset_group_link',
                                'name': 'Ihm Dataset Group Link'
                            }, {
                                'url': '/chaise/recordset/#99/PDB:ihm_dataset_list',
                                'name': 'Ihm Dataset List'
                            }, {
                                'url': '/chaise/recordset/#99/PDB:ihm_dataset_related_db_reference',
                                'name': 'Ihm Dataset Related Db Reference'
                            }, {
                                'url': '/chaise/recordset/#99/PDB:ihm_external_files',
                                'name': 'Ihm External Files'
                            }, {
                                'url': '/chaise/recordset/#99/PDB:ihm_external_reference_info',
                                'name': 'Ihm External Reference Info'
                            }, {
                                'url': '/chaise/recordset/#99/PDB:ihm_related_datasets',
                                'name': 'Ihm Related Datasets'
                            }
                        ]
                    }, {
                        'name': 'Localization Densities',
                        'children': [
                            {
                                'url': '/chaise/recordset/#99/PDB:ihm_localization_density_files',
                                'name': 'Ihm Localization Density Files'
                            }
                        ]
                    }, {
                        'name': 'Model List',
                        'children': [
                            {
                                'url': '/chaise/recordset/#99/PDB:ihm_model_group',
                                'name': 'Ihm Model Group'
                            }, {
                                'url': '/chaise/recordset/#99/PDB:ihm_model_group_link',
                                'name': 'Ihm Model Group Link'
                            }, {
                                'url': '/chaise/recordset/#99/PDB:ihm_model_list',
                                'name': 'Ihm Model List'
                            }, {
                                'url': '/chaise/recordset/#99/PDB:ihm_model_representative',
                                'name': 'Ihm Model Representative'
                            }, {
                                'url': '/chaise/recordset/#99/PDB:ihm_residues_not_modeled',
                                'name': 'Ihm Residues Not Modeled'
                            }
                        ]
                    }, {
                        'name': 'Model Representation',
                        'children': [
                            {
                                'url': '/chaise/recordset/#99/PDB:ihm_model_representation',
                                'name': 'Ihm Model Representation'
                            }, {
                                'url': '/chaise/recordset/#99/PDB:ihm_model_representation_details',
                                'name': 'Ihm Model Representation Details'
                            }
                        ]
                    }, {
                        'name': 'Modeling Protocol',
                        'children': [
                            {
                                'url': '/chaise/recordset/#99/PDB:ihm_modeling_post_process',
                                'name': 'Ihm Modeling Post Process'
                            }, {
                                'url': '/chaise/recordset/#99/PDB:ihm_modeling_protocol',
                                'name': 'Ihm Modeling Protocol'
                            }, {
                                'url': '/chaise/recordset/#99/PDB:ihm_modeling_protocol_details',
                                'name': 'Ihm Modeling Protocol Details'
                            }
                        ]
                    }, {
                        'name': 'Molecular Entities, Instances and Segments',
                        'children': [
                            {
                                'url': '/chaise/recordset/#99/PDB:atom_type',
                                'name': 'Atom Type'
                            }, {
                                'url': '/chaise/recordset/#99/PDB:entity',
                                'name': 'Entity'
                            }, {
                                'url': '/chaise/recordset/#99/PDB:entity_name_com',
                                'name': 'Entity Name Com'
                            }, {
                                'url': '/chaise/recordset/#99/PDB:entity_name_sys',
                                'name': 'Entity Name Sys'
                            }, {
                                'url': '/chaise/recordset/#99/PDB:entity_poly',
                                'name': 'Entity Poly'
                            }, {
                                'url': '/chaise/recordset/#99/PDB:entity_poly_seq',
                                'name': 'Entity Poly Seq'
                            }, {
                                'url': '/chaise/recordset/#99/PDB:entity_src_gen',
                                'name': 'Entity Src Gen'
                            }, {
                                'url': '/chaise/recordset/#99/PDB:ihm_entity_poly_segment',
                                'name': 'Ihm Entity Poly Segment'
                            }, {
                                'url': '/chaise/recordset/#99/PDB:pdbx_entity_nonpoly',
                                'name': 'PDBX Entity Nonpoly'
                            }, {
                                'url': '/chaise/recordset/#99/PDB:struct_asym',
                                'name': 'Struct Asym'
                            }
                        ]
                    }, {
                        'name': 'Multi-state Modeling and Ordered Ensembles',
                        'children': [
                            {
                                'url': '/chaise/recordset/#99/PDB:ihm_ensemble_info',
                                'name': 'Ihm Ensemble Info'
                            }, {
                                'url': '/chaise/recordset/#99/PDB:ihm_multi_state_model_group_link',
                                'name': 'Ihm Multi State Model Group Link'
                            }, {
                                'url': '/chaise/recordset/#99/PDB:ihm_multi_state_modeling',
                                'name': 'Ihm Multi State Modeling'
                            }, {
                                'url': '/chaise/recordset/#99/PDB:ihm_ordered_ensemble',
                                'name': 'Ihm Ordered Ensemble'
                            }
                        ]
                    }, {
                        'name': 'PDBX Related',
                        'children': [
                            {
                                'url': '/chaise/recordset/#99/PDB:pdbx_entity_poly_na_type',
                                'name': 'PDBX Entity Poly Na Type'
                            }, {
                                'url': '/chaise/recordset/#99/PDB:pdbx_entry_details',
                                'name': 'PDBX Entry Details'
                            }, {
                                'url': '/chaise/recordset/#99/PDB:pdbx_inhibitor_info',
                                'name': 'PDBX Inhibitor Info'
                            }, {
                                'url': '/chaise/recordset/#99/PDB:pdbx_ion_info',
                                'name': 'PDBX Ion Info'
                            }, {
                                'url': '/chaise/recordset/#99/PDB:pdbx_protein_info',
                                'name': 'PDBX Protein Info'
                            }
                        ]
                    }, {
                        'name': 'Predicted Contacts',
                        'children': [
                            {
                                'url': '/chaise/recordset/#99/PDB:ihm_predicted_contact_restraint',
                                'name': 'Ihm Predicted Contact Restraint'
                            }
                        ]
                    }, {
                        'name': 'Probe Labeling Information',
                        'children': [
                            {
                                'url': '/chaise/recordset/#99/PDB:ihm_chemical_component_descriptor',
                                'name': 'Ihm Chemical Component Descriptor'
                            }, {
                                'url': '/chaise/recordset/#99/PDB:ihm_ligand_probe',
                                'name': 'Ihm Ligand Probe'
                            }, {
                                'url': '/chaise/recordset/#99/PDB:ihm_poly_probe_conjugate',
                                'name': 'Ihm Poly Probe Conjugate'
                            }, {
                                'url': '/chaise/recordset/#99/PDB:ihm_poly_probe_position',
                                'name': 'Ihm Poly Probe Position'
                            }, {
                                'url': '/chaise/recordset/#99/PDB:ihm_probe_list',
                                'name': 'Ihm Probe List'
                            }
                        ]
                    }, {
                        'name': 'SAS',
                        'children': [
                            {
                                'url': '/chaise/recordset/#99/PDB:ihm_sas_restraint',
                                'name': 'Ihm SAS Restraint'
                            }
                        ]
                    }, {
                        'name': 'Starting Models',
                        'children': [
                            {
                                'url': '/chaise/recordset/#99/PDB:ihm_starting_comparative_models',
                                'name': 'Ihm Starting Comparative Models'
                            }, {
                                'url': '/chaise/recordset/#99/PDB:ihm_starting_computational_models',
                                'name': 'Ihm Starting Computational Models'
                            }, {
                                'url': '/chaise/recordset/#99/PDB:ihm_starting_model_details',
                                'name': 'Ihm Starting Model Details'
                            }, {
                                'url': '/chaise/recordset/#99/PDB:ihm_starting_model_seq_dif',
                                'name': 'Ihm Starting Model Seq Dif'
                            }
                        ]
                    }, {
                        'name': 'Structure Assembly',
                        'children': [
                            {
                                'url': '/chaise/recordset/#99/PDB:ihm_struct_assembly',
                                'name': 'Ihm Struct Assembly'
                            }, {
                                'url': '/chaise/recordset/#99/PDB:ihm_struct_assembly_class',
                                'name': 'Ihm Struct Assembly Class'
                            }, {
                                'url': '/chaise/recordset/#99/PDB:ihm_struct_assembly_class_link',
                                'name': 'Ihm Struct Assembly Class Link'
                            }, {
                                'url': '/chaise/recordset/#99/PDB:ihm_struct_assembly_details',
                                'name': 'Ihm Struct Assembly Details'
                            }
                        ]
                    }, {
                        'name': 'Workflow',
                        'children': [
                            {
                                'url': '/chaise/recordset/#99/PDB:Entry_Related_File',
                                'name': 'Entry Related File'
                            }, {
                                'url': '/chaise/recordset/#99/PDB:Entry_mmCIF_File',
                                'name': 'Entry mmCIF File'
                            }
                        ]
                    }
                ]
            }, {
                'name': 'Vocabulary',
                'children': [
                    {
                        'name': 'Chem Comp',
                        'children': [
                            {
                                'url': '/chaise/recordset/#99/Vocab:chem_comp_mon_nstd_flag',
                                'name': 'Mon Nstd Flag'
                            }, {
                                'url': '/chaise/recordset/#99/Vocab:chem_comp_atom_pdbx_aromatic_flag',
                                'name': 'PDBX  Aromatic Flag'
                            }, {
                                'url': '/chaise/recordset/#99/Vocab:chem_comp_atom_pdbx_leaving_atom_flag',
                                'name': 'PDBX  Leaving Atom Flag'
                            }, {
                                'url': '/chaise/recordset/#99/Vocab:chem_comp_atom_pdbx_polymer_type',
                                'name': 'PDBX  Polymer Type'
                            }, {
                                'url': '/chaise/recordset/#99/Vocab:chem_comp_atom_pdbx_stereo_config',
                                'name': 'PDBX  Stereo Config'
                            }, {
                                'url': '/chaise/recordset/#99/Vocab:chem_comp_atom_substruct_code',
                                'name': 'Substruct Code'
                            }, {
                                'url': '/chaise/recordset/#99/Vocab:chem_comp_type',
                                'name': 'Type'
                            }
                        ]
                    }, {
                        'name': 'Entity',
                        'children': [
                            {
                                'url': '/chaise/recordset/#99/Vocab:entity_poly_seq_hetero',
                                'name': 'Hetero'
                            }, {
                                'url': '/chaise/recordset/#99/Vocab:entity_poly_nstd_chirality',
                                'name': 'Nstd Chirality'
                            }, {
                                'url': '/chaise/recordset/#99/Vocab:entity_poly_nstd_linkage',
                                'name': 'Nstd Linkage'
                            }, {
                                'url': '/chaise/recordset/#99/Vocab:entity_poly_nstd_monomer',
                                'name': 'Nstd Monomer'
                            }, {
                                'url': '/chaise/recordset/#99/Vocab:entity_src_gen_pdbx_alt_source_flag',
                                'name': 'PDBX  Alt Source Flag'
                            }, {
                                'url': '/chaise/recordset/#99/Vocab:entity_poly_pdbx_sequence_evidence_code',
                                'name': 'PDBX  Sequence Evidence Code'
                            }, {
                                'url': '/chaise/recordset/#99/Vocab:entity_poly_type',
                                'name': 'Poly Type'
                            }, {
                                'url': '/chaise/recordset/#99/Vocab:entity_src_method',
                                'name': 'Src Method'
                            }, {
                                'url': '/chaise/recordset/#99/Vocab:entity_type',
                                'name': 'Type'
                            }
                        ]
                    }, {
                        'name': 'Ihm 2dem',
                        'children': [
                            {
                                'url': '/chaise/recordset/#99/Vocab:ihm_2dem_class_average_restraint_image_segment_flag',
                                'name': 'Image Segment Flag'
                            }
                        ]
                    }, {
                        'name': 'Ihm 3dem',
                        'children': [
                            {
                                'url': '/chaise/recordset/#99/Vocab:ihm_3dem_restraint_map_segment_flag',
                                'name': 'Map Segment Flag'
                            }
                        ]
                    }, {
                        'name': 'Ihm Cross Link',
                        'children': [
                            {
                                'url': '/chaise/recordset/#99/Vocab:ihm_cross_link_restraint_conditional_crosslink_flag',
                                'name': 'Conditional Crosslink Flag'
                            }, {
                                'url': '/chaise/recordset/#99/Vocab:ihm_cross_link_list_linker_type',
                                'name': 'Linker Type'
                            }, {
                                'url': '/chaise/recordset/#99/Vocab:ihm_cross_link_restraint_model_granularity',
                                'name': 'Model Granularity'
                            }, {
                                'url': '/chaise/recordset/#99/Vocab:ihm_cross_link_restraint_restraint_type',
                                'name': 'Restraint Type'
                            }
                        ]
                    }, {
                        'name': 'Ihm Dataset',
                        'children': [
                            {
                                'url': '/chaise/recordset/#99/Vocab:ihm_dataset_group_application',
                                'name': 'Application'
                            }, {
                                'url': '/chaise/recordset/#99/Vocab:ihm_dataset_list_data_type',
                                'name': 'Data Type'
                            }, {
                                'url': '/chaise/recordset/#99/Vocab:ihm_dataset_list_database_hosted',
                                'name': 'Database Hosted'
                            }, {
                                'url': '/chaise/recordset/#99/Vocab:ihm_derived_distance_restraint_group_conditionality',
                                'name': 'Group Conditionality'
                            }, {
                                'url': '/chaise/recordset/#99/Vocab:ihm_derived_distance_restraint_restraint_type',
                                'name': 'Restraint Type'
                            }
                        ]
                    }, {
                        'name': 'Ihm Derived Distance Restraint',
                        'children': [
                            {
                                'url': '/chaise/recordset/#99/Vocab:ihm_derived_distance_restraint_group_conditionality',
                                'name': 'Group Conditionality'
                            }, {
                                'url': '/chaise/recordset/#99/Vocab:ihm_derived_distance_restraint_restraint_type',
                                'name': 'Restraint Type'
                            }
                        ]
                    }, {
                        'name': 'Ihm Ensemble Info',
                        'children': [
                            {
                                'url': '/chaise/recordset/#99/Vocab:ihm_ensemble_info_ensemble_clustering_feature',
                                'name': 'Ensemble Clustering Feature'
                            }, {
                                'url': '/chaise/recordset/#99/Vocab:ihm_ensemble_info_ensemble_clustering_method',
                                'name': 'Ensemble Clustering Method'
                            }
                        ]
                    }, {
                        'name': 'Ihm Epr Restraint',
                        'children': [
                            {
                                'url': '/chaise/recordset/#99/Vocab:ihm_epr_restraint_fitting_state',
                                'name': 'Fitting State'
                            }
                        ]
                    }, {
                        'name': 'Ihm External',
                        'children': [
                            {
                                'url': '/chaise/recordset/#99/Vocab:ihm_external_files_content_type',
                                'name': 'Content Type'
                            }, {
                                'url': '/chaise/recordset/#99/Vocab:ihm_external_files_file_format',
                                'name': 'File Format'
                            }, {
                                'url': '/chaise/recordset/#99/Vocab:ihm_external_reference_info_reference_type',
                                'name': 'Reference Type'
                            }, {
                                'url': '/chaise/recordset/#99/Vocab:ihm_external_reference_info_refers_to',
                                'name': 'Refers To'
                            }
                        ]
                    }, {
                        'name': 'Ihm Feature List',
                        'children': [
                            {
                                'url': '/chaise/recordset/#99/Vocab:ihm_feature_list_entity_type',
                                'name': 'Entity Type'
                            }, {
                                'url': '/chaise/recordset/#99/Vocab:ihm_feature_list_feature_type',
                                'name': 'Feature Type'
                            }
                        ]
                    }, {
                        'name': 'Ihm Geometric',
                        'children': [
                            {
                                'url': '/chaise/recordset/#99/Vocab:ihm_geometric_object_axis_axis_type',
                                'name': 'Axis Type'
                            }, {
                                'url': '/chaise/recordset/#99/Vocab:geometric_object_distance_restraint_group_condition',
                                'name': 'Group Conditionality'
                            }, {
                                'url': '/chaise/recordset/#99/Vocab:geometric_object_distance_restraint_object_character',
                                'name': 'Object Characteristic'
                            }, {
                                'url': '/chaise/recordset/#99/Vocab:ihm_geometric_object_list_object_type',
                                'name': 'Object Type'
                            }, {
                                'url': '/chaise/recordset/#99/Vocab:ihm_geometric_object_plane_plane_type',
                                'name': 'Plane Type'
                            }, {
                                'url': '/chaise/recordset/#99/Vocab:ihm_geometric_object_distance_restraint_restraint_type',
                                'name': 'Restraint Type'
                            }, {
                                'url': '/chaise/recordset/#99/Vocab:ihm_geometric_object_half_torus_section',
                                'name': 'Section'
                            }
                        ]
                    }, {
                        'name': 'Ihm Model',
                        'children': [
                            {
                                'url': '/chaise/recordset/#99/Vocab:ihm_modeling_protocol_details_ensemble_flag',
                                'name': 'Ensemble Flag'
                            }, {
                                'url': '/chaise/recordset/#99/Vocab:ihm_modeling_post_process_feature',
                                'name': 'Feature'
                            }, {
                                'url': '/chaise/recordset/#99/Vocab:ihm_model_representation_details_model_granularity',
                                'name': 'Model Granularity'
                            }, {
                                'url': '/chaise/recordset/#99/Vocab:ihm_model_representation_details_model_mode',
                                'name': 'Model Mode'
                            }, {
                                'url': '/chaise/recordset/#99/Vocab:model_representation_details_model_object_primitive',
                                'name': 'Model Object Primitive'
                            }, {
                                'url': '/chaise/recordset/#99/Vocab:ihm_modeling_protocol_details_multi_scale_flag',
                                'name': 'Multi Scale Flag'
                            }, {
                                'url': '/chaise/recordset/#99/Vocab:ihm_modeling_protocol_details_ordered_flag',
                                'name': 'Ordered Flag'
                            }, {
                                'url': '/chaise/recordset/#99/Vocab:ihm_model_representative_selection_criteria',
                                'name': 'Selection Criteria'
                            }, {
                                'url': '/chaise/recordset/#99/Vocab:ihm_modeling_post_process_type',
                                'name': 'Type'
                            }
                        ]
                    }, {
                        'name': 'Ihm Multi State Modeling',
                        'children': [
                            {
                                'url': '/chaise/recordset/#99/Vocab:ihm_multi_state_modeling_experiment_type',
                                'name': 'Experiment Type'
                            }
                        ]
                    }, {
                        'name': 'Ihm Poly',
                        'children': [
                            {
                                'url': '/chaise/recordset/#99/Vocab:ihm_poly_probe_conjugate_ambiguous_stoichiometry_flag',
                                'name': 'Ambiguous Stoichiometry Flag'
                            }, {
                                'url': '/chaise/recordset/#99/Vocab:ihm_poly_residue_feature_interface_residue_flag',
                                'name': 'Interface Residue Flag'
                            }, {
                                'url': '/chaise/recordset/#99/Vocab:ihm_poly_probe_position_modification_flag',
                                'name': 'Modification Flag'
                            }, {
                                'url': '/chaise/recordset/#99/Vocab:ihm_poly_probe_position_mutation_flag',
                                'name': 'Mutation Flag'
                            }, {
                                'url': '/chaise/recordset/#99/Vocab:ihm_poly_residue_feature_rep_atom',
                                'name': 'Rep Atom'
                            }, {
                                'url': '/chaise/recordset/#99/Vocab:ihm_poly_residue_feature_residue_range_granularity',
                                'name': 'Residue Range Granularity'
                            }
                        ]
                    }, {
                        'name': 'Ihm Predicted Contact Restraint',
                        'children': [
                            {
                                'url': '/chaise/recordset/#99/Vocab:ihm_predicted_contact_restraint_model_granularity',
                                'name': 'Model Granularity'
                            }, {
                                'url': '/chaise/recordset/#99/Vocab:ihm_predicted_contact_restraint_rep_atom_1',
                                'name': 'Rep Atom 1'
                            }, {
                                'url': '/chaise/recordset/#99/Vocab:ihm_predicted_contact_restraint_rep_atom_2',
                                'name': 'Rep Atom 2'
                            }, {
                                'url': '/chaise/recordset/#99/Vocab:ihm_predicted_contact_restraint_restraint_type',
                                'name': 'Restraint Type'
                            }
                        ]
                    }, {
                        'name': 'Ihm Probe List',
                        'children': [
                            {
                                'url': '/chaise/recordset/#99/Vocab:ihm_probe_list_probe_link_type',
                                'name': 'Probe Link Type'
                            }, {
                                'url': '/chaise/recordset/#99/Vocab:ihm_probe_list_probe_origin',
                                'name': 'Probe Origin'
                            }, {
                                'url': '/chaise/recordset/#99/Vocab:ihm_probe_list_reactive_probe_flag',
                                'name': 'Reactive Probe Flag'
                            }
                        ]
                    }, {
                        'name': 'Ihm Residues Not Modeled',
                        'children': [
                            {
                                'url': '/chaise/recordset/#99/Vocab:ihm_residues_not_modeled_reason',
                                'name': 'Reason'
                            }
                        ]
                    }, {
                        'name': 'Ihm SAS Restraint',
                        'children': [
                            {
                                'url': '/chaise/recordset/#99/Vocab:ihm_sas_restraint_fitting_state',
                                'name': 'Fitting State'
                            }, {
                                'url': '/chaise/recordset/#99/Vocab:ihm_sas_restraint_profile_segment_flag',
                                'name': 'Profile Segment Flag'
                            }
                        ]
                    }, {
                        'name': 'Ihm Starting',
                        'children': [
                            {
                                'url': '/chaise/recordset/#99/Vocab:ihm_starting_model_details_starting_model_source',
                                'name': 'Starting Model Source'
                            }, {
                                'url': '/chaise/recordset/#99/Vocab:starting_comparative_models_template_sequence_id_denom',
                                'name': 'Template Sequence Identity Denominator'
                            }
                        ]
                    }, {
                        'name': 'Ihm Struct Assembly Class',
                        'children': [
                            {
                                'url': '/chaise/recordset/#99/Vocab:ihm_struct_assembly_class_type',
                                'name': 'Type'
                            }
                        ]
                    }, {
                        'name': 'PDBX  Entity Poly Na Type',
                        'children': [
                            {
                                'url': '/chaise/recordset/#99/Vocab:pdbx_entity_poly_na_type_type',
                                'name': 'Type'
                            }
                        ]
                    }, {
                        'name': 'Software',
                        'children': [
                            {
                                'url': '/chaise/recordset/#99/Vocab:software_type',
                                'name': 'Type'
                            }
                        ]
                    }, {
                        'name': 'Struct',
                        'children': [
                            {
                                'url': '/chaise/recordset/#99/Vocab:struct_pdbx_CASP_flag',
                                'name': 'PDBX  CASP Flag'
                            }, {
                                'url': '/chaise/recordset/#99/Vocab:struct_asym_pdbx_blank_PDB_chainid_flag',
                                'name': 'PDBX  Blank PDB Chainid Flag'
                            }, {
                                'url': '/chaise/recordset/#99/Vocab:struct_asym_pdbx_type',
                                'name': 'PDBX  Type'
                            }
                        ]
                    }, {
                        'name': 'Workflow',
                        'children': [
                            {
                                'url': '/chaise/recordset/#99/Vocab:File_Format',
                                'name': 'File Format'
                            }, {
                                'url': '/chaise/recordset/#99/Vocab:File_Type',
                                'name': 'File Type'
                            }, {
                                'url': '/chaise/recordset/#99/Vocab:process_status',
                                'name': 'Process Status'
                            }, {
                                'url': '/chaise/recordset/#99/Vocab:workflow_status',
                                'name': 'Workflow Status'
                            }
                        ]
                    }
                ]
            }
        ]
    }
}

catalog_config = {
    'name': 'pdb',
    'groups': {
        'admin': groups['pdb-admin'],
        'reader': groups['pdb-reader'],
        'writer': groups['pdb-writer'],
        'curator': groups['pdb-curator']
    }
}

annotations = {
    chaise_tags.bulk_upload: bulk_upload,
    chaise_tags.chaise_config: chaise_config,
    chaise_tags.catalog_config: catalog_config,
}

acls = {
    'update': [groups['pdb-curator']],
    'insert': [groups['pdb-curator'], groups['pdb-writer']],
    'create': [],
    'select': [groups['pdb-writer'], groups['pdb-reader']],
    'delete': [groups['pdb-curator']],
    'write': [],
    'owner': [groups['pdb-admin'], groups['isrd-staff']],
    'enumerate': ['*']
}


def main(catalog, mode, replace=False):
    updater = CatalogUpdater(catalog)
    updater.update_catalog(mode, annotations, acls, replace=replace)


if __name__ == "__main__":
    host = 'pdb.isrd.isi.edu'
    catalog_id = 99
    mode, replace, host, catalog_id = parse_args(host, catalog_id, is_catalog=True)
    catalog = ErmrestCatalog('https', host, catalog_id=catalog_id, credentials=get_credential(host))
    main(catalog, mode, replace)
