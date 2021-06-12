#!/usr/bin/python

import sys
import json
from deriva.core import ErmrestCatalog, AttrDict, get_credential, DEFAULT_CREDENTIAL_FILE, tag, urlquote, DerivaServer, get_credential, BaseCLI
from deriva.core.ermrest_model import builtin_types, Schema, Table, Column, Key, ForeignKey
from collections import OrderedDict
import re

#
# The purpose is to refactor the keys and forieng keys of the PDB table to conform to the naming convention.
#

MAX_NAME_LENGTH = 62

KEY_TYPE_SUFFIX_DICT = {
    "COMBO1" : "_combo1_key", 
    "COMBO2" : "_combo2_key",
    "PRIMARY" : "_primary_key",
}

FKEY_TYPE_SUFFIX_DICT = {
    "COMBO1" : "_combo1_fkey", 
    "COMBO2" : "_combo2_fkey",
    "MMCIF" : "_mmcif_fkey",   
}

''' Thees string subsitition are used to shorten the key and forieng key names
'''
STRING_REPLACEMENT_DICT = OrderedDict([
    ("_ihm_", "__"),
    ("_representation_", "_rep_"),
    ("_geometric_", "_geom_"),
    ("_chemical_", "_chem_"),
    ("_component_", "_comp_"),
    ("_parameters_", "_param_"),
    ("_localization_", "_loc_"),                        
    ("_object_", "_obj_"),
    ("_transformation_", "_xform_"),
    ("_average_", "_avg_"),
    ("_segment_", "_seg_"),
    ("_restraint_", "_rest_"),
    ("_computational_", "_compute_"),
    ("_comparative_", "_compare_"),
    ("_conjugate_", "_conju_"),
    ("_position_", "_pos_"),
    ("_starting_", "_start_"),
    ("_assembly_", "_assem_"),
    ("_class_", "_cla_"),
    ("_group_", "_grp_"),
    ("_state_", "_sta_"),
])

TABLE_NAME_DICT = {
    
}
KEY_NAME_DICT = {
    
}

# multiple keys to the same parent tables: 2-column with RID
PARENT_RID_COLUMN_NAME_DICT = {
    # -- no need for this group of dict. Use hueristics
    #('ihm_cross_link_restraint', 'struct_asym', ('asym_id_1', 'structure_id')) : 'Asym_1_RID',
    #('ihm_cross_link_restraint', 'struct_asym', ('asym_id_2', 'structure_id')) : 'Asym_2_RID', 
    #('ihm_derived_distance_restraint', 'ihm_feature_list', ('feature_id_1', 'structure_id')) : 'Feature_list_RID_1', 
    #('ihm_derived_distance_restraint', 'ihm_feature_list', ('feature_id_2', 'structure_id')) : 'Feature_list_RID_2', 
    #('ihm_ordered_ensemble', 'ihm_model_group', ('model_group_id_begin', 'structure_id')) : 'Model_group_RID_begin', 
    #('ihm_ordered_ensemble', 'ihm_model_group', ('model_group_id_end', 'structure_id')) : 'Model_group_end_RID',  
    #('ihm_predicted_contact_restraint', 'struct_asym', ('asym_id_1', 'structure_id')) : 'Asym_RID_1', 
    #('ihm_predicted_contact_restraint', 'struct_asym', ('asym_id_2', 'structure_id')) : 'Asym_RID_2', 
    #('ihm_probe_list', 'ihm_chemical_component_descriptor', ('reactive_probe_chem_comp_descriptor_id')) : 'Reactive_Probe_Chem_Comp_Descriptor_RID', # single fkey
    #('ihm_probe_list', 'ihm_chemical_component_descriptor', ('probe_chem_comp_descriptor_id')) : 'Probe_chem_comp_descriptor_RID', 
    #('ihm_related_datasets', 'ihm_dataset_list', ('dataset_list_id_derived', 'structure_id')) : 'Dataset_list_RID_derived', 
    #('ihm_related_datasets', 'ihm_dataset_list', ('dataset_list_id_primary', 'structure_id')) : 'Dataset_list_RID_primary', 
    #('ihm_struct_assembly_details', 'ihm_struct_assembly', ('parent_assembly_id', 'structure_id')) : 'parent_assembly_RID', 
    #('ihm_struct_assembly_details', 'ihm_struct_assembly', ('assembly_id', 'structure_id')) : 'Assembly_RID',
    #
    # -- out of place RID column name
    ('ihm_starting_computational_models', 'ihm_external_files', ('script_file_id', 'structure_id')) : 'External_Files_RID',
    #
    # multiple keys to the same parent tables: 4-column with RID. Need to lookup
    ('ihm_cross_link_list', 'entity_poly_seq', ('comp_id_1', 'entity_id_1', 'seq_id_1', 'structure_id')) : 'Entity_poly_seq_RID_1', 
    ('ihm_cross_link_list', 'entity_poly_seq', ('comp_id_2', 'entity_id_2', 'seq_id_2', 'structure_id')) : 'Entity_poly_seq_RID_2', 
    ('ihm_cross_link_restraint', 'entity_poly_seq', ('comp_id_1', 'entity_id_1', 'seq_id_1', 'structure_id')) : 'Entity_poly_seq_RID_1', 
    ('ihm_cross_link_restraint', 'entity_poly_seq', ('comp_id_2', 'entity_id_2', 'seq_id_2', 'structure_id')) : 'Entity_poly_seq_RID_2', 
    ('ihm_poly_residue_feature', 'entity_poly_seq', ('comp_id_begin', 'entity_id', 'seq_id_begin', 'structure_id')) : 'Entity_poly_seq_RID_begin', 
    ('ihm_poly_residue_feature', 'entity_poly_seq', ('comp_id_end', 'entity_id', 'seq_id_end', 'structure_id')) : 'Entity_poly_seq_RID_end',
    ('ihm_predicted_contact_restraint', 'entity_poly_seq', ('comp_id_1', 'entity_id_1', 'seq_id_1', 'structure_id')) : 'Entity_poly_seq_RID_1', 
    ('ihm_predicted_contact_restraint', 'entity_poly_seq', ('comp_id_2', 'entity_id_2', 'seq_id_2', 'structure_id')) : 'Entity_poly_seq_RID_2',
    ('ihm_residues_not_modeled', 'entity_poly_seq', ('comp_id_begin', 'entity_id', 'seq_id_begin', 'structure_id')) : 'Entity_poly_seq_RID_begin',     
    ('ihm_residues_not_modeled', 'entity_poly_seq', ('comp_id_end', 'entity_id', 'seq_id_end', 'structure_id')) : 'Entity_poly_seq_RID_end', 
}

''' Lookup table based on foreign columns to forieng key name.
    The key is (from_table, to_table, tuple(col_list))
    The names in the dict should not exceed the maximum name length.
'''
FKEY_NAME_DICT = {
    # names too long
    #('ihm_2dem_class_average_fitting', 'ihm_2dem_class_average_restraint', ('Ihm_2dem_class_average_restraint_RID', 'restraint_id', 'structure_id')): "ihm_2dem_class_average_fitting_ihm_2dem_class_average_restraint_combo1_fkey",  # 75
    #('ihm_cross_link_result_parameters', 'ihm_cross_link_restraint', ('Ihm_cross_link_restraint_RID', 'restraint_id', 'structure_id')): "ihm_cross_link_result_parameters_ihm_cross_link_restraint_combo1_fkey",  # 69
    #('ihm_geometric_object_axis', 'ihm_geometric_object_transformation', ('Ihm_geometric_object_transformation_RID', 'transformation_id')): "ihm_geometric_object_axis_ihm_geometric_object_transformation_combo2_fkey",  # 73
    #('ihm_geometric_object_distance_restraint', 'ihm_dataset_list', ('Ihm_dataset_list_RID', 'dataset_list_id')): "ihm_geometric_object_distance_restraint_ihm_dataset_list_combo2_fkey",  # 68
    #('ihm_geometric_object_distance_restraint', 'ihm_geometric_object_list', ('Ihm_geometric_object_list_RID', 'object_id', 'structure_id')): "ihm_geometric_object_distance_restraint_ihm_geometric_object_list_combo1_fkey",  # 77
    #('ihm_geometric_object_distance_restraint', 'ihm_feature_list', ('Ihm_feature_list_RID', 'feature_id', 'structure_id')): "ihm_geometric_object_distance_restraint_ihm_feature_list_combo1_fkey",  # 68
    #('ihm_geometric_object_half_torus', 'ihm_geometric_object_torus', ('Ihm_geometric_object_torus_RID', 'object_id', 'structure_id')): "ihm_geometric_object_half_torus_ihm_geometric_object_torus_combo1_fkey",  # 70
    #('ihm_geometric_object_plane', 'ihm_geometric_object_transformation', ('Ihm_geometric_object_transformation_RID', 'transformation_id')): "ihm_geometric_object_plane_ihm_geometric_object_transformation_combo2_fkey",  # 74
    #('ihm_geometric_object_sphere', 'ihm_geometric_object_transformation', ('Ihm_geometric_object_transformation_RID', 'transformation_id')): "ihm_geometric_object_sphere_ihm_geometric_object_transformation_combo2_fkey",  # 75
    #('ihm_geometric_object_sphere', 'ihm_geometric_object_center', ('Ihm_geometric_object_center_RID', 'center_id', 'structure_id')): "ihm_geometric_object_sphere_ihm_geometric_object_center_combo1_fkey",  # 67
    #('ihm_geometric_object_torus', 'ihm_geometric_object_transformation', ('Ihm_geometric_object_transformation_RID', 'transformation_id')): "ihm_geometric_object_torus_ihm_geometric_object_transformation_combo2_fkey",  # 74
    #('ihm_model_representation_details', 'ihm_starting_model_details', ('Ihm_starting_model_details_RID', 'starting_model_id')): "ihm_model_representation_details_ihm_starting_model_details_combo2_fkey",  # 71
    #('ihm_model_representation_details', 'ihm_entity_poly_segment', ('Ihm_entity_poly_segment_RID', 'entity_poly_segment_id')): "ihm_model_representation_details_ihm_entity_poly_segment_combo2_fkey",  # 68
    #('ihm_model_representation_details', 'ihm_model_representation', ('Ihm_model_representation_RID', 'representation_id', 'structure_id')): "ihm_model_representation_details_ihm_model_representation_combo1_fkey",  # 69
    #('ihm_multi_state_model_group_link', 'ihm_multi_state_modeling', ('Ihm_multi_state_modeling_RID', 'state_id', 'structure_id')): "ihm_multi_state_model_group_link_ihm_multi_state_modeling_combo1_fkey",  # 69
    #('ihm_poly_probe_conjugate', 'ihm_chemical_component_descriptor', ('Ihm_chemical_component_descriptor_RID', 'chem_comp_descriptor_id')): "ihm_poly_probe_conjugate_ihm_chemical_component_descriptor_combo2_fkey",  # 70
    #('ihm_poly_probe_position', 'ihm_chemical_component_descriptor', ('Ihm_chemical_component_descriptor_RID', 'mod_res_chem_comp_descriptor_id')): "ihm_poly_probe_position_ihm_chemical_component_descriptor_combo2_fkey",  # 69
    #('ihm_starting_comparative_models', 'ihm_starting_model_details', ('Ihm_starting_model_details_RID', 'starting_model_id', 'structure_id')): "ihm_starting_comparative_models_ihm_starting_model_details_combo1_fkey",  # 70
    #('ihm_starting_computational_models', 'ihm_starting_model_details', ('Ihm_starting_model_details_RID', 'starting_model_id', 'structure_id')): "ihm_starting_computational_models_ihm_starting_model_details_combo1_fkey",  # 72
    #('ihm_struct_assembly_class_link', 'ihm_struct_assembly_class', ('Ihm_struct_assembly_class_RID', 'class_id', 'structure_id')): "ihm_struct_assembly_class_link_ihm_struct_assembly_class_combo1_fkey",  # 68
    
    # multiple keys to the same parent tables: 2-column with RID
    ('ihm_cross_link_restraint', 'struct_asym', ('Struct_asym_1_RID', 'asym_id_1', 'structure_id')) : "ihm_cross_link_restraint__struct_asym_1_combo1_fkey",
    ('ihm_cross_link_restraint', 'struct_asym', ('Struct_asym_2_RID', 'asym_id_2', 'structure_id')) : "ihm_cross_link_restraint__struct_asym_2_combo1_fkey",
    ('ihm_derived_distance_restraint', 'ihm_feature_list', ('Ihm_feature_list_1_RID', 'feature_id_1', 'structure_id')) : "ihm_derived_distance_restraint__feature_list_1_combo1_fkey",
    ('ihm_derived_distance_restraint', 'ihm_feature_list', ('Ihm_feature_list_2_RID', 'feature_id_2', 'structure_id')) : "ihm_derived_distance_restraint__feature_list_2_combo1_fkey",
    ('ihm_ordered_ensemble', 'ihm_model_group', ('Ihm_model_group_begin_RID', 'model_group_id_begin', 'structure_id')) : "ihm_ordered_ensemble__model_group_begin_combo1_fkey",
    ('ihm_ordered_ensemble', 'ihm_model_group', ('Ihm_model_group_end_RID', 'model_group_id_end', 'structure_id')) : "ihm_ordered_ensemble__model_group_end_combo1_fkey",
    ('ihm_predicted_contact_restraint', 'struct_asym', ('Struct_asym_1_RID', 'asym_id_1', 'structure_id')) : "ihm_predicted_contact_restraint__struct_asym_1_combo1_fkey",
    ('ihm_predicted_contact_restraint', 'struct_asym', ('Struct_asym_2_RID', 'asym_id_2', 'structure_id')) : "ihm_predicted_contact_restraint__struct_asym_2_combo1_fkey",
    ('ihm_probe_list', 'ihm_chemical_component_descriptor', ('Ihm_chemical_component_descriptor_reactive_RID', 'reactive_probe_chem_comp_descriptor_id')) : "ihm_probe_list__chem_comp_descriptor_reactive_combo2_fkey",
    ('ihm_probe_list', 'ihm_chemical_component_descriptor', ('Ihm_chemical_component_descriptor_probe_RID', 'probe_chem_comp_descriptor_id')) : "ihm_probe_list__chem_comp_descriptor_probe_combo2_fkey", #??
    ('ihm_related_datasets', 'ihm_dataset_list', ('Ihm_dataset_list_derived_RID', 'dataset_list_id_derived', 'structure_id')) : "ihm_related_datasets__dataset_list_derived_combo1_fkey",
    ('ihm_related_datasets', 'ihm_dataset_list', ('Ihm_dataset_list_primary_RID', 'dataset_list_id_primary', 'structure_id')) : "ihm_related_datasets__dataset_list_primary_combo1_fkey",
    ('ihm_struct_assembly_details', 'ihm_struct_assembly', ('Ihm_struct_assembly_parent_RID', 'parent_assembly_id', 'structure_id')) : "ihm_struct_assembly_details__struct_assembly_parent_combo1_fkey",
    ('ihm_struct_assembly_details', 'ihm_struct_assembly', ('Ihm_struct_assembly_RID', 'assembly_id', 'structure_id')) : "ihm_struct_assembly_details__struct_assembly_self_combo1_fkey", #??

    # multiple keys to the same parent tables: 4-column with RID
    ('ihm_cross_link_list', 'entity_poly_seq', ('Entity_poly_seq_1_RID', 'comp_id_1', 'entity_id_1', 'seq_id_1', 'structure_id')) : "ihm_cross_link_list__mm_poly_res_label_1_combo1_fkey",
    ('ihm_cross_link_list', 'entity_poly_seq', ('Entity_poly_seq_2_RID', 'comp_id_2', 'entity_id_2', 'seq_id_2', 'structure_id')) : "ihm_cross_link_list__mm_poly_res_label_2_combo1_fkey",
    ('ihm_cross_link_restraint', 'entity_poly_seq', ('Entity_poly_seq_1_RID', 'comp_id_1', 'entity_id_1', 'seq_id_1', 'structure_id')) : "ihm_cross_link_restraint__mm_poly_res_label_1_combo1_fkey",
    ('ihm_cross_link_restraint', 'entity_poly_seq', ('Entity_poly_seq_2_RID', 'comp_id_2', 'entity_id_2', 'seq_id_2', 'structure_id')) : "ihm_cross_link_restraint__mm_poly_res_label_2_combo1_fkey",
    ('ihm_poly_residue_feature', 'entity_poly_seq', ('Entity_poly_seq_begin_RID', 'comp_id_begin', 'entity_id', 'seq_id_begin', 'structure_id')) : "ihm_poly_residue_feature__mm_poly_res_label_begin_combo1_fkey",
    ('ihm_poly_residue_feature', 'entity_poly_seq', ('Entity_poly_seq_end_RID', 'comp_id_end', 'entity_id', 'seq_id_end', 'structure_id')) : "ihm_poly_residue_feature__mm_poly_res_label_end_combo1_fkey",
    ('ihm_predicted_contact_restraint', 'entity_poly_seq', ('Entity_poly_seq_1_RID', 'comp_id_1', 'entity_id_1', 'seq_id_1', 'structure_id')) : "ihm_predicted_contact_restraint__mm_poly_res_label_1_combo1_fkey",
    ('ihm_predicted_contact_restraint', 'entity_poly_seq', ('Entity_poly_seq_2_RID', 'comp_id_2', 'entity_id_2', 'seq_id_2', 'structure_id')) : "ihm_predicted_contact_restraint__mm_poly_res_label_2_combo1_fkey",
    ('ihm_residues_not_modeled', 'entity_poly_seq', ('Entity_poly_seq_begin_RID', 'comp_id_begin', 'entity_id', 'seq_id_begin', 'structure_id')) : "ihm_residues_not_modeled__mm_poly_res_label_begin_combo1_fkey",    
    ('ihm_residues_not_modeled', 'entity_poly_seq', ('Entity_poly_seq_end_RID', 'comp_id_end', 'entity_id', 'seq_id_end', 'structure_id')) : "ihm_residues_not_modeled__mm_poly_res_label_end_combo1_fkey",
}

# print all keys that [RID, structure_id] is a subset of
# key.name returns [schema_obj, constraint_name]
def print_rid_structure_id_keys(model):
    for table in model.schemas["PDB"].tables.values():
        for key in table.keys:
            #if set([ c.name for c in key.unique_columns ]).issubset({'RID', 'structure_id'}) == True:
            if {'RID', 'structure_id'}.issubset(set([ c.name for c in key.unique_columns ])) == True:                                   
                print("%s %s: %s" % (table.name, key.constraint_name, set([ c.name for c in key.unique_columns ])))


# rename these incorrect key constraint
def print_keys_with_rid(model):
    # all composite keys contains [RID, structure_id] 
    for table in model.schemas["PDB"].tables.values():
        for key in table.keys:
            key_length = len(key.columns)
            if (key_length >= 2) and ({'RID'}.issubset(set([ c.name for c in key.unique_columns ])) == True):
                if ({'structure_id'}.issubset(set([ c.name for c in key.unique_columns ])) == True):
                    key_name = "_".join([table.name, 'combo1_key'])
                    if key.constraint_name == key_name:
                        print("++    [%d] %s %s : %s" % (key_length, table.name, key.constraint_name, set([ c.name for c in key.unique_columns ])))
                    else:
                        # need correction
                        print("++ ** [%d] %s %s => %s : %s" % (key_length, table.name, key.constraint_name, key_name, set([ c.name for c in key.unique_columns ])))

    # all composite keys contains RID but not structure_id
    for table in model.schemas["PDB"].tables.values():
        for key in table.keys:
            key_length = len(key.columns)
            if (key_length >= 2) and ({'RID'}.issubset(set([ c.name for c in key.unique_columns ])) == True):
                if ({'structure_id'}.issubset(set([ c.name for c in key.unique_columns ])) == False):
                    key_name = "_".join([table.name, 'combo2_key'])
                    if key.constraint_name == key_name:
                        print("--    [%d] %s %s : %s" % (key_length, table.name, key.constraint_name, set([ c.name for c in key.unique_columns ])))
                    else:
                        # need correction
                        print("-- ** [%d] %s %s => %s : %s" % (key_length, table.name, key.constraint_name, key_name, set([ c.name for c in key.unique_columns ])))


# given a primary key, get equivalent combo fkey 
def get_key_name(table, key_column_names):
    rid_included = True if "RID" in key_column_names else False
    struct_id_included = True if "struct_id" in key_column_names else False
    key_length = len(key_column_names)
    
    if rid_included and struct_id_included:
        suffix = '_combo1_key'
    elif rid_included and key_length > 1:
        suffix = '_combo2_key'
    elif rid_included and key_length == 1:
        suffix = '_RID_key'
    elif struct_id_included:
        suffix = '_primary_key'
    else:
        print("KEY COLUMN NAME ERROR: key_column_names %s is not combo or primiary key" % (key_column_names))
        
    expected_key_name = table.name+suffix
    key_name = expected_key_name
    key_name_length = len(key_name)
    for old, new in STRING_REPLACEMENT_DICT.items():
        if key_name_length <= MAX_NAME_LENGTH:
            break
        key_name = key_name.replace(old, new)        
        key_name_length = len(key_name)
        
    if key_name_length > MAX_NAME_LENGTH:            
        print('ERROR: KEY NAME TOO LONG (%d): t: %s, key name: %s' % (len(key_name), table.name, key_name))

    if key_name != expected_key_name:
        print('WARNING: RENAME KEY in table %s: "%s[%d] v.s. %s[%d]"  # ' % ( table.name, expected_key_name, len(expected_key_name), key_name, len(key_name)))

    return(key_name)



''' This function returns a combo1/combo2 names of a foreign key based on the provided flag. 
    If the flag is empty, the combo position in the string is empty. 
    The function consults existing FKEY_NAME_DICT.
    If the name is too long, it will apply string replacement to shorten the names. 
'''
def get_fkey_constraint_name(fkey, expected_fkey_col_names, combo_flag=''):
    key = (fkey.table.name, fkey.pk_table.name, tuple(sorted(expected_fkey_col_names)))
    suffix = ('combo'+combo_flag+'_fkey') if combo_flag else 'fkey'
    
    if key in FKEY_NAME_DICT.keys():
        expected_fkey_constraint_name = FKEY_NAME_DICT[key]
    else:
        expected_fkey_constraint_name = '_'.join([fkey.table.name, fkey.pk_table.name, suffix])                            
    
    constraint_name = expected_fkey_constraint_name
    contraint_name_length = len(expected_fkey_constraint_name)
    for old, new in STRING_REPLACEMENT_DICT.items():
        if contraint_name_length <= MAX_NAME_LENGTH:
            break
        constraint_name = constraint_name.replace(old, new)        
        contraint_name_length = len(constraint_name)
        
    if contraint_name_length > MAX_NAME_LENGTH:            
        print('ERROR: FKEY NAME TOO LONG: %s: "%s"  # %d' % ( key, expected_fkey_constraint_name, len(expected_fkey_constraint_name)))

    if constraint_name != expected_fkey_constraint_name:
        print('  WARNING: RENAME FKEY: %s: %s[%d] v.s. %s[%d] ' % ( key, expected_fkey_constraint_name, len(expected_fkey_constraint_name), constraint_name, len(constraint_name)))
    
    return(constraint_name)


def get_fkey_type(fkey):
    fkey_col_names = {c.name for c in fkey.column_map.keys()}    
    fkey_parent_col_names = {c.name for c in fkey.column_map.values()}
    fkey_type = "UNKNOWN"
    
    if ('RID' in fkey_parent_col_names):
        # check for column_name corresponding to RID in the parent table
        for from_col, to_col in fkey.column_map.items():
            if to_col.name == 'RID':
                primary_col_names = fkey_col_names - {from_col.name}
        # check combo1 or combo2
        fkey_type = "COMBO1" if ('structure_id' in fkey_parent_col_names) else "COMBO2"
    else:
        if ('structure_id' in fkey_parent_col_names):
            fkey_type = "MMCIF"
        elif len(fkey_col_names) == 1:
            fkey_type = "MMCIF"

    return(fkey_type)

def get_fkey_rid_column(fkey):
    rid_column = None
    if 'RID' in {c.name for c in fkey.column_map.values()}:
        # check for column_name corresponding to RID in the parent table
        for from_col, to_col in fkey.column_map.items():
            if to_col.name == 'RID':
                rid_column = from_col
    return(rid_column)

def get_fkey_id_column(fkey):
    id_column = None
    if 'id' in {c.name for c in fkey.column_map.values()}:
        # check for column_name corresponding to RID in the parent table
        for from_col, to_col in fkey.column_map.items():
            if to_col.name == 'id':
                id_column = from_col
    return(id_column)

# When do the lookup, the function will remove RID column and add structure_id column for searching
def get_fkey_parent_rid_column_name(fkey):
    rid_col_name = None    
    fkey_col_names = {c.name for c in fkey.column_map.keys()}
    
    # remove RID columns if exists and add structure_id
    rid_column = get_fkey_rid_column(fkey)
    if (rid_column): # if rid is there, return the name
        #print("---0 rid_column already exist with name %s:%s" % (fkey.pk_table.name, rid_column.name))
        return rid_column.name
    else:
        primary_col_names = fkey_col_names | {"structure_id"}
        col_names_tuple = tuple(sorted(primary_col_names))
        lookup_key = (fkey.table.name, fkey.pk_table.name, col_names_tuple)

        # in case of multiple fkeys going to the same parent, can't just append RID to table name.
        if lookup_key in PARENT_RID_COLUMN_NAME_DICT:
            rid_col_name = PARENT_RID_COLUMN_NAME_DICT[lookup_key]
            #print("---1 USE LOOKUP VALUE  %s:[%s]->%s:[%s] will use %s for RID col name" % (fkey.table.name, {c.name for c in fkey.column_map.keys()}, fkey.pk_table.name, {c.name for c in fkey.column_map.values()}, rid_col_name))                            
        else:
            id_col = get_fkey_id_column(fkey)
            if id_col: # look for column name pointing to "id" column
                rid_col_name = (id_col.name.title()).replace("_Id", "_RID")
                #print("---2 Found id_col %s:[%s]->%s:[%s] will use %s for RID col name" % (fkey.table.name, {c.name for c in fkey.column_map.keys()}, fkey.pk_table.name, {c.name for c in fkey.column_map.values()}, rid_col_name))                
            else: # look for _id column for hint
                for col_name in (primary_col_names - {"structure_id"}):
                    if re.match(".*_id", col_name) or re.match(".*_id_(1|2|begin|end|primary|derived)", col_name):
                        rid_col_name = (col_name.title()).replace("_Id", "_RID")
                        #print("---3 id column in %s:[%s]->%s:[%s] not found. Will use %s for RID col name" % (fkey.table.name, {c.name for c in fkey.column_map.keys()}, fkey.pk_table.name, {c.name for c in fkey.column_map.values()}, rid_col_name))
                        break

    if not rid_col_name:
        rid_col_name = fkey.pk_table.name.capitalize() + '_RID'
        #print("--4 id column in %s:[%s]->[%s] not found. Will use %s for RID col name" % (fkey.table.name, {c.name for c in fkey.column_map.keys()}, {c.name for c in fkey.column_map.values()}, rid_col_name))                                

    return(rid_col_name)


# given fkey, get the corresponding fkey based on the fkey_type except itself. 
def get_equivalent_fkey_by_type(fkey, fkey_type="*"):
    fkey_col_names = {c.name for c in fkey.column_map.keys()}    
    fkey_parent_col_names = {c.name for c in fkey.column_map.values()}

    col_names = fkey_col_names
    parent_rid_col_name = get_fkey_parent_rid_column_name(fkey)
    rid_column_exist = (True if parent_rid_col_name in fkey.table.columns.elements else False)

    # try capitalize: a hack since we have both patter!!
    if not rid_column_exist:
        parent_rid_col_name = (parent_rid_col_name.capitalize()).replace("_rid", "_RID")
        rid_column_exist = (True if parent_rid_col_name in fkey.table.columns.elements else False)
        
    #print("-- check equivalent fkey of type %s: %s %s parent_rid:%s" % (fkey_type, fkey.table.name, fkey_col_names, parent_rid_col_name))
    
    # add RID and structure_id if not exist
    if fkey_type == 'COMBO1' and rid_column_exist:
        col_names = fkey_col_names|{parent_rid_col_name, "structure_id"}
    elif fkey_type == 'COMBO2' and rid_column_exist:
        col_names = (fkey_col_names|{parent_rid_col_name}) - {"structure_id"}
    elif fkey_type == 'MMCIF':
        col_names = (fkey_col_names - {parent_rid_col_name}) | {"structure_id"}
    elif fkey_type == '*' and rid_column_exist:
        col_names = (fkey_col_names - {parent_rid_col_name}) | {"structure_id"}
    else:
        return None

    match_list = []
    for fk in fkey.table.fkeys_by_columns(col_names, raise_nomatch=False):
        if fk is fkey:
            continue
        match_list.append(fk)

    if not match_list:
        return None
    elif len(match_list) > 1:
        # TODO: throw an exception instead
        print("SCHEMA ERROR: MULTIPLE MATCH EXIST: More than 1 are found")
        return(match_list[0])
    else:
        return(match_list[0])

def refactor_fkeys(model, ncols, deriva_included=False, combo1_included=True, combo2_included=True, primary_types=('combo1', 'combo2')):
    schema = model.schemas["PDB"]
    deriva_tables = {'Catalog_Group', 'ERMrest_Client', 'Entry_Related_File'}
    combo1_count = 1
    combo2_count = 1
    primary_count = 1
    
    print("=========== print_fkeys_with_rid with ncols = %d ================= " % (ncols))
    for table in sorted(schema.tables.values(), key = lambda x: x.name):
        
        for fkey in table.foreign_keys:
            fkey_length = len(fkey.columns)
            fkey_parent_col_names = {c.name for c in fkey.column_map.values()}
            fkey_col_names = {c.name for c in fkey.column_map.keys()}
            pk_table = fkey.pk_table

            # only look at fkeys to PDB schema (not Vocab)
            if fkey.pk_table.schema.name != 'PDB':
                continue
            # focus on a particular number of columns
            if (fkey_length != ncols):
                continue

            fkey_type = get_fkey_type(fkey)
            if fkey_type == "COMBO1":
                if not combo1_included:
                    continue
                mmcif_fk = get_equivalent_fkey_by_type(fkey, "MMCIF")
                if mmcif_fk:
                    print("[%2d] -c1  p  [%d] %s -> %s : %s : %s -> %s" % (combo1_count, fkey_length, table.name, fkey.pk_table.name, fkey.constraint_name, fkey_col_names, fkey_parent_col_names))
                else:
                    print("[%2d] -c1      [%d] %s -> %s : %s : %s -> %s" % (combo1_count, fkey_length, table.name, fkey.pk_table.name, fkey.constraint_name, fkey_col_names, fkey_parent_col_names))

                combo1_count = combo1_count + 1

            elif fkey_type == "COMBO2":
                if not combo2_included:
                    continue
                mmcif_fk = get_equivalent_fkey_by_type(fkey, "MMCIF")
                if mmcif_fk:
                    print("[%2d] -c2  p  [%d] %s -> %s : %s : %s -> %s" % (combo2_count, fkey_length, table.name, fkey.pk_table.name, fkey.constraint_name, fkey_col_names, fkey_parent_col_names))
                else:
                    print("[%2d] -c2      [%d] %s -> %s : %s : %s -> %s" % (combo2_count, fkey_length, table.name, fkey.pk_table.name, fkey.constraint_name, fkey_col_names, fkey_parent_col_names))

                combo2_count = combo2_count + 1
            
            elif fkey_type == "MMCIF":
                if not primary_types:
                    continue
                    
                # 1. determine whether it needs combo1 or combo2:
                # Except for structure_id, if a column in the key is not-null, then it is mandatory
                mandatory = False
                for col in fkey.column_map:
                    # exclude structure_id 
                    if col.name == 'structure_id':
                        continue
                    if col.nullok == False:
                        mandatory = True
                        break
                
                # 2. setup variables
                parent_rid_column_name = get_fkey_parent_rid_column_name(fkey)
                if mandatory == True:
                    expected_fkey_col_names = fkey_col_names|{parent_rid_column_name}
                    expected_fkey_parent_col_names = fkey_parent_col_names|{'RID'}
                    flag = '1'
                    fkey_type = "COMBO1"
                else:
                    expected_fkey_col_names = (fkey_col_names|{parent_rid_column_name})-{'structure_id'}
                    expected_fkey_parent_col_names = (fkey_parent_col_names|{'RID'})-{'structure_id'}
                    flag = '2'
                    fkey_type = "COMBO2"
                    
                # -- selectively omit primary fkeys investigation depending on the flag. This help with the printout readability
                if 'combo'+flag not in primary_types: 
                    continue
                expected_parent_key_name = '_'.join([pk_table.name, 'combo'+flag, 'key'])
                expected_fkey_constraint_name = get_fkey_constraint_name(fkey, expected_fkey_col_names, flag)
                    
                combo_fk = get_equivalent_fkey_by_type(fkey, fkey_type)
                if combo_fk:
                    print("[%2d] --p  c%s [%d] %s -> %s : %s : %s -> %s combo:%s" % (primary_count, flag, fkey_length, table.name, fkey.pk_table.name, fkey.constraint_name, fkey_col_names, fkey_parent_col_names, {c.name for c in combo_fk.column_map.keys()}))                        
                else:
                    #create
                    print("[%2d] --p      [%d] %s -> %s : %s : %s -> %s" % (primary_count, fkey_length, table.name, fkey.pk_table.name, fkey.constraint_name, fkey_col_names, fkey_parent_col_names))
                    exit()
                    # 5.1 check parent column in the table
                    if parent_rid_column_name not in table.columns.elements:
                        # TODO: add column
                        print("    +col: Add new column: %s.%s for fkey %s:%s" % (table.name, parent_rid_column_name, fkey.constraint_name, fkey_col_names))
                        
                    # 5.2 check whether expected key exist in the parent table
                    if fkey.pk_table.key_by_columns(expected_fkey_parent_col_names, raise_nomatch=False) is None:
                        print("    *key: c%s create %s %s:%s" % (flag, pk_table.name, expected_parent_key_name, expected_fkey_parent_col_names))
                        # TODO: create a new key
                            
                    # 5.3 create a new fkey
                    print("    +c%s  [%d] %s -> %s : %s : %s -> %s" % (flag, fkey_length, table.name, fkey.pk_table.name, expected_fkey_constraint_name, expected_fkey_col_names, expected_fkey_parent_col_names))
                        
                primary_count = primary_count + 1
            
            else:
                if fkey.pk_table.name not in deriva_tables or deriva_included == True:
                    print("---ERROR:    [%d] %s -> %s : %s : %s -> %s" % (fkey_length, table.name, fkey.pk_table.name, fkey.constraint_name, fkey_col_names, fkey_parent_col_names))

                
    
'''paramters:    
   model: relevant ermrest model 
   ncols: number of fkey columns to be investigated
   deriva_included: whether to include fkeys of deriva-related table (i.e. non-mmcif tables)
   combo1_included: whether to include combo1 fkeys in the logic
   combo2_included: whether to include combo2 fkeys in the logic
   primary_types: the types of primary fkeys to be included. If empty, no primary fkeys will be included. 
'''
def print_fkeys_with_rid(model, ncols, deriva_included=False, combo1_included=True, combo2_included=True, primary_types=('combo1', 'combo2')):
    schema = model.schemas["PDB"]
    deriva_tables = {'Catalog_Group', 'ERMrest_Client', 'Entry_Related_File'}
    combo1_count = 1
    combo2_count = 1
    primary_count = 1
    
    print("=========== print_fkeys_with_rid with ncols = %d ================= " % (ncols))
    for table in sorted(schema.tables.values(), key = lambda x: x.name):
        
        #if table.name == 'ihm_cross_link_pseudo_site':
            #print("********* TABLE NAME = %s fkeys: %s" % (table.name, table.foreign_keys))
        
        for fkey in table.foreign_keys:
            fkey_length = len(fkey.columns)
            fkey_parent_col_names = {c.name for c in fkey.column_map.values()}
            fkey_col_names = {c.name for c in fkey.column_map.keys()}
            pk_table = fkey.pk_table

            # only look at fkeys to PDB schema (not Vocab)
            if fkey.pk_table.schema.name != 'PDB':
                continue
            
            # focus on a particular number of columns
            if (fkey_length != ncols):
                continue

            #print("table name = %s, fkey_col_names = %s, parent_col_names = %s" % (table.name, fkey_col_names, fkey_parent_col_names))
            
            # combo1 or combo2 fkeys
            if ('RID' in fkey_parent_col_names):
                
                # check for column_name corresponding to RID in the parent table
                for from_col, to_col in fkey.column_map.items():
                    if to_col.name == 'RID':
                        primary_col_names = fkey_col_names - {from_col.name}

                # -- combo1 
                if ('structure_id' in fkey_parent_col_names):
                    if not combo1_included:
                        continue
                    # check whether primiary key still exists
                    primary_fkeys = list(table.fkeys_by_columns(primary_col_names, raise_nomatch=False))
                    if primary_fkeys:                    
                        print("-c1  p  [%d] %s -> %s : %s : %s -> %s" % (fkey_length, table.name, fkey.pk_table.name, fkey.constraint_name, fkey_col_names, fkey_parent_col_names))
                        # TODO: for ncols=2, delete corresponding primary key from the model. Somehow some are deleted but some are still present.
                        local_fk = get_equivalent_fkey_by_type(fkey, "MMCIF")
                        if local_fk and local_fk is not primary_fkeys[0]:
                            print("ERROR: COMBO1 MISMATCHED PRIMARY_FKEY: %s v.s. %s" % (local_fk.constraint_name, primary_fkeys[0].constraint_name))
                    else:
                        print("-c1      [%d] %s -> %s : %s : %s -> %s" % (fkey_length, table.name, fkey.pk_table.name, fkey.constraint_name, fkey_col_names, fkey_parent_col_names))
                    combo1_count = combo1_count + 1
                # -- combo2 case                
                else:
                    if not combo2_included:
                        continue
                    primary_col_names = primary_col_names | {'structure_id'}
                    # check whether primiary key still exists
                    primary_fkeys = list(table.fkeys_by_columns(primary_col_names, raise_nomatch=False))
                    if primary_fkeys:
                        print("%2d: -c2  p  [%d] %s -> %s : %s : %s -> %s --> p%s" % (combo2_count, fkey_length, table.name, fkey.pk_table.name, fkey.constraint_name, fkey_col_names, fkey_parent_col_names, primary_col_names))
                        # TODO: for ncols=2, delete corresponding primary key from the model. Somehow some are deleted but some are still present.
                        local_fk = get_equivalent_fkey_by_type(fkey, "MMCIF")
                        if local_fk and local_fk is not primary_fkeys[0]:
                            print("ERROR: COMBO2 MISMATCHED PRIMARY_FKEY: %s v.s. %s" % (local_fk.constraint_name, primary_fkeys[0].constraint_name))
                    else:
                        print("%2d: -c2     [%d] %s -> %s : %s : %s -> %s -- p%s" % (combo2_count, fkey_length, table.name, fkey.pk_table.name, fkey.constraint_name, fkey_col_names, fkey_parent_col_names, primary_col_names))
                    combo2_count = combo2_count + 1
                    
            # primary key with structure_id or other kinds
            else :
                # -- normal composite key
                if ('structure_id' in fkey_parent_col_names):
                    
                    if not primary_types:
                        continue
                    # TODO: create a lookup table for long table names
                    # can't check for combo1/2 since the parent_table RID column is not known. Some tables have shorter name lookup
                    
                    # 1. determine whether it needs combo1 or combo2:
                    # Except for structure_id, if a column in the key is not-null, then it is mandatory
                    mandatory = False
                    for col in fkey.column_map:
                        # exclude structure_id 
                        if col.name == 'structure_id':
                            continue
                        if col.nullok == False:
                            mandatory = True
                            break

                    # 2. determine whether there are multiple fkeys pointing to the same parent table.
                    dup_fkey_parent = False
                    dup_fkey_parent_fkey = None
                    for fk in table.foreign_keys:
                        if dup_fkey_parent == True:
                            break
                        # exclude fkey to other tables or its own
                        if fk.pk_table != pk_table or fkey is fk:
                            continue
                        # found same parent table
                        fk_parent_col_names = {c.name for c in fk.column_map.values()}
                        if 'RID' not in fk_parent_col_names:  # exclude combo keys
                            dup_fkey_parent = True
                            dup_fkey_parent_fkey = fk
                            print("    *dup: %s -> %s : %s vs %s : %s->%s" % (table.name, pk_table.name, fk.constraint_name, fkey.constraint_name, {c.name for c in fk.column_map.keys()}, {c.name for c in fk.column_map.values()}))
                        
                    # 3. setup variables
                    parent_rid_column_name = get_fkey_parent_rid_column_name(fkey)
                    if mandatory == True:
                        expected_fkey_col_names = fkey_col_names|{parent_rid_column_name}
                        expected_fkey_parent_col_names = fkey_parent_col_names|{'RID'}
                        flag = '1'
                        fkey_type = "COMBO1"
                    else:
                        expected_fkey_col_names = (fkey_col_names|{parent_rid_column_name})-{'structure_id'}
                        expected_fkey_parent_col_names = (fkey_parent_col_names|{'RID'})-{'structure_id'}
                        flag = '2'
                        fkey_type = "COMBO2"
                        
                    # -- selectively omit primary fkeys investigation depending on the flag. This help with the printout readability
                    if 'combo'+flag not in primary_types: 
                        continue
                    expected_parent_key_name = '_'.join([pk_table.name, 'combo'+flag, 'key'])
                    expected_fkey_constraint_name = get_fkey_constraint_name(fkey, expected_fkey_col_names, flag)
                    
                    # need a different fkey name suffix to distinguish between multiple fkeys
                    #if dup_fkey_parent:
                    #    key = (table.name, pk_table.name, tuple(sorted(expected_fkey_col_names)))
                    #    value = fkey.constraint_name.replace("_fkey", "_combo"+flag+"_fkey")
                    #    print('%s : "%s",' % (key, value))

                    
                    parent_rid_column_exist = (True if parent_rid_column_name in fkey.table.columns.elements else False)
                    combo_fk = get_equivalent_fkey_by_type(fkey, fkey_type)
                    if combo_fk:
                        print("**%2d: --p  c%s [%d] %s -> %s : %s : %s -> %s combo:%s" % (primary_count, flag, fkey_length, table.name, fkey.pk_table.name, fkey.constraint_name, fkey_col_names, fkey_parent_col_names, {c.name for c in combo_fk.column_map.keys()}))                        
                    else:
                        #create
                        print("**%2d: --p      [%d] %s -> %s : %s : %s -> %s" % (primary_count, fkey_length, table.name, fkey.pk_table.name, fkey.constraint_name, fkey_col_names, fkey_parent_col_names))
                        exit()
                        # 5.1 check parent column in the table
                        if parent_rid_column_name not in table.columns.elements:
                            # TODO: add column
                            print("    +col: Add new column: %s.%s for fkey %s:%s" % (table.name, parent_rid_column_name, fkey.constraint_name, fkey_col_names))
                                        
                        # 5.2 check whether expected key exist in the parent table
                        if fkey.pk_table.key_by_columns(expected_fkey_parent_col_names, raise_nomatch=False) is None:
                            print("    *key: c%s create %s %s:%s" % (flag, pk_table.name, expected_parent_key_name, expected_fkey_parent_col_names))
                            # TODO: create a new key
                            
                        # 5.3 create a new fkey
                        print("    +c%s  [%d] %s -> %s : %s : %s -> %s" % (flag, fkey_length, table.name, fkey.pk_table.name, expected_fkey_constraint_name, expected_fkey_col_names, expected_fkey_parent_col_names))
                        
                    
                    # 4. check whether the combo fkeys already exist.
                    #found = False                    
                    #for fk in table.foreign_keys:
                    #    if found == True:
                    #        break
                    #    
                    #    # exclude fkey to other tables
                    #    if fk.pk_table != pk_table or fk is fkey:
                    #        continue
                    #    
                    #    # look for fk with 'RID' in it.
                    #    fk_parent_col_names = {c.name for c in fk.column_map.values()}
                    #    if 'RID' in fk_parent_col_names:
                    #        if fk_parent_col_names == expected_fkey_parent_col_names:
                    #            found = True
                    #            print("%2d: --p  c%s [%d] %s -> %s : %s : %s -> %s combo:%s" % (primary_count, flag, fkey_length, table.name, fkey.pk_table.name, fkey.constraint_name, fkey_col_names, fkey_parent_col_names, {c.name for c in combo_fk.column_map.keys()}))
                    #        else:
                    #            print("ERROR: found 'RID' fkey but not combo%s in %s -> %s : %s : %s -> %s" % (flag, table.name, pk_table.name, fk.constraint_name, {c.name for c in fk.column_map.keys()}, {c.name for c in fk.column_map.values()}))
                    
                    primary_count = primary_count + 1


                # -- single keys or composite keys without structure_id (which should be none)
                else:
                    if fkey.pk_table.name not in deriva_tables or deriva_included == True:
                        print("---ERROR:    [%d] %s -> %s : %s : %s -> %s" % (fkey_length, table.name, fkey.pk_table.name, fkey.constraint_name, fkey_col_names, fkey_parent_col_names))


# fix inconsistant naming
# Entry_Related_File:
#  column name:
#    structure_id -> Structure_Id
#  change fkey name to be consistent with convention
#    "Entry_Related_File_entry_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
#    "Entry_Related_File_process_status_fkey" FOREIGN KEY ("Process_Status") REFERENCES "Vocab".process_status("Name") ON UPDATE CASCADE ON DELETE SET NULL
#    "Entry_Related_File_workflow_status_fkey" FOREIGN KEY ("Workflow_Status") REFERENCES "Vocab".workflow_status("Name") ON UPDATE CASCADE


def main(server_name, catalog_id, credentials):
    server = DerivaServer('https', server_name, credentials)
    catalog = server.connect_ermrest(catalog_id)
    catalog.dcctx['cid'] = "oneoff/model"
    model = catalog.getCatalogModel()

    refactor_fkeys(model, 2, combo1_included=True, combo2_included=False, primary_types=("combo2"))
    #print_fkeys_with_rid(model, 2, combo1_included=True, combo2_included=False, primary_types=("combo2"))
    
    #print_fkeys_with_rid(model, 4, combo1_included=False, combo2_included=True, primary_types=("x"))
 
        

if __name__ == '__main__':
    args = BaseCLI("ad-hoc table creation tool", None, 1).parse_cli()
    credentials = get_credential(args.host, args.credential_file)
    main(args.host, 99, credentials)
