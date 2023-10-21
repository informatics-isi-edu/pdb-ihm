#!/usr/bin/python3

import sys
import traceback
import json
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('catalog_number')
parser.add_argument('input')
parser.add_argument('output')
args = parser.parse_args()


catalog_number = args.catalog_number
input = args.input
output = args.output

with open('{}'.format(input), 'r') as f:
    constraints = json.load(f)
    
tables = constraints['Catalog {}'.format(catalog_number)]['schemas']['PDB']['tables']

optional_constraints = {}
sql_queries = []

contraint_names = [
        'ihm_localization_density_files_asym_id_fkey',
        'ihm_localization_density_files_entity_poly_segment_id_fkey',
        'ihm_localization_density_files_entity_id_fkey',
        'ihm_struct_assembly_details_entity_poly_segment_id_fkey',
        'ihm_cross_link_list_linker_chem_comp_descriptor_id_fkey',
        'ihm_probe_list_probe_chem_comp_descriptor_id_fkey',
        'ihm_probe_list_reactive_probe_chem_comp_descriptor_id_fkey',
        'ihm_epr_restraint_fitting_method_citation_id_fkey',
        'software_citation_id_fkey',
        'ihm_poly_probe_conjugate_chem_comp_descriptor_id_fkey',
        'ihm_geometric_object_sphere_transformation_id_fkey',
        'ihm_poly_residue_feature_asym_id_fkey',
        'ihm_interface_residue_feature_binding_partner_asym_id_fkey',
        'ihm_geometric_object_plane_transformation_id_fkey',
        'ihm_predicted_contact_restraint_software_id_fkey',
        'ihm_3dem_restraint_fitting_method_citation_id_fkey',
        'ihm_poly_atom_feature_asym_id_fkey',
        'ihm_model_representation_details_starting_model_id_fkey',
        'ihm_model_representation_details_entity_poly_segment_id_fkey',
        'ihm_hydroxyl_radical_fp_restraint_software_id_fkey',
        'ihm_modeling_post_process_struct_assembly_id_fkey',
        'ihm_modeling_post_process_dataset_group_id_fkey',
        'ihm_modeling_post_process_script_file_id_fkey',
        'ihm_modeling_post_process_software_id_fkey',
        'ihm_geometric_object_axis_transformation_id_fkey',
        'ihm_non_poly_feature_asym_id_fkey',
        'ihm_geometric_object_torus_transformation_id_fkey',
        'pdbx_entity_nonpoly_comp_id_fkey',
        'ihm_ensemble_info_post_process_id_fkey',
        'ihm_ensemble_info_ensemble_file_id_fkey',
        'ihm_ensemble_info_model_group_id_fkey',
        'ihm_poly_probe_position_mut_res_chem_comp_id_fkey',
        'ihm_poly_probe_position_mod_res_chem_comp_descriptor_id_fkey',
        'ihm_starting_comparative_models_alignment_file_id_fkey',
        'ihm_modeling_protocol_details_software_id_fkey',
        'ihm_modeling_protocol_details_struct_assembly_id_fkey',
        'ihm_modeling_protocol_details_script_file_id_fkey',
        'ihm_modeling_protocol_details_dataset_group_id_fkey',
        'ihm_starting_model_details_entity_poly_segment_id_fkey',
        'ihm_starting_computational_models_script_file_id_fkey',
        'ihm_starting_computational_models_software_id_fkey',
        'ihm_interface_residue_feature_dataset_list_id_fkey',
        'ihm_derived_distance_restraint_dataset_list_id_fkey',
        'ihm_geometric_object_distance_restraint_dataset_list_id_fkey'
]

for table_name, table_description in tables.items():
    if 'foreign_keys' not in table_description.keys():
        continue
    fks = table_description['foreign_keys']
    for fk_name, fk_description in fks.items():
        if fk_name in contraint_names:
            if table_name not in optional_constraints.keys():
                optional_constraints[table_name] = []
            optional_constraint = {}
            fk_columns = fk_description['columns'][1:-1].split(',')
            ref_columns = fk_description['referenced_columns']['columns'][1:-1].split(',')
            ref_table = fk_description['referenced_columns']['table']
            optional_constraint['fk_columns'] = fk_columns
            optional_constraint['ref_columns'] = ref_columns
            optional_constraint['ref_table'] = ref_table
            optional_constraint['fk_name'] = fk_name
            
            if 'RID' not in ref_columns:
                print('Column RID not ref_columns {}'.format(ref_columns))
            
            if ref_columns[0] == 'RID':
                ref_RID = ref_columns[0]
                ref_other = ref_columns[1]
                fk_RID = fk_columns[0]
                fk_other = fk_columns[1]
            else:
                ref_RID = ref_columns[1]
                ref_other = ref_columns[0]
                fk_RID = fk_columns[1]
                fk_other = fk_columns[0]
            
            optional_constraint['ref_RID_column_name'] = ref_RID
            optional_constraint['ref_other_column_name'] = ref_other
            optional_constraint['fk_RID_column_name'] = fk_RID
            optional_constraint['fk_other_column_name'] = fk_other
            optional_constraint['url_structure_pattern'] = '/attribute/PDB:{}/{}={}&structure_id={}/RID?limit=1'
            optional_constraint['url_pattern'] = '/attribute/PDB:{}/{}={}/RID?limit=1'
            optional_constraints[table_name].append(optional_constraint)
            #sql_queries.append('update "{}" A set "{}" = (select "RID" from "{}" B where A."{}" = B."{}" limit 1) where A."{}" is null;'.format(table_name, fk_RID, ref_table, fk_other, ref_other, fk_RID))
            sql_queries.append('update "PDB"."{}" A set "{}" = (select "RID" from "PDB"."{}" B where A."{}" = B."{}" and A.structure_id = B.structure_id);'.format(table_name, fk_RID, ref_table, fk_other, ref_other))
            
fw = open('{}'.format(output), 'w')
json.dump(optional_constraints, fw, indent=4)
fw.close()

fw = open('{}.sql'.format(output.split('.')[0]), 'w')
for sql_query in sql_queries:
    fw.write('{}\n'.format(sql_query))
fw.close()

