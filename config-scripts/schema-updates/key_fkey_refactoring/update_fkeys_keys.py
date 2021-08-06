#!/usr/bin/python

import sys
import json
from deriva.core import ErmrestCatalog, AttrDict, get_credential, DEFAULT_CREDENTIAL_FILE, tag, urlquote, DerivaServer, get_credential, BaseCLI
from deriva.core.ermrest_model import builtin_types, Schema, Table, Column, Key, ForeignKey
from collections import OrderedDict
import re

# TODO:
# - Create combo1 fkeys (2 column).
#    - Note on the number of fkeys created.
#    - Track a mapping of mmcif fkey and combo1 fkey names. Will need this to update the annotations and ACL docs.
#    - Update annotations, ACL
#    - * After model change, update RID column values. (SQL)
#    - * Update the model to set null-ok for RID column to False. (Another script/function)
#    - Test chaise to make sure that it works appropriately e.g. attempting to make structure_id inconsistent with combo1 key will throw an error.
#    - Note: you might want to test the script to only 1 table first to make sure everything is good before proceeding with all.
# - Delete combo1's corresponding mmcif fkeys (2 column). Make sure the number matches with combo1 created.
# - Repeat above for 4-column fkeys
#
# - Rename combo2 fkeys.
#    - Save the mapping between old and new names. Will need this to replace the strings in annotations and ACLs.
#    - Update the annottions and ACL
# - Rename combo2 key names.
#    - Save the mapping between old and new names. Will need this to replace the strings in annotations and ACLs.
#    - Update the annottions and ACL
# 
# - Rename RID columns
#    - Turn capitalized column names to Titled column names. Make note of the changes, so we can apply the change to ACL
#    - Rename out of place RID column name. Replace with "Script_File_RID", then remove this entry from the map.
#      ('ihm_starting_computational_models', 'ihm_external_files', ('script_file_id', 'structure_id')) : 'External_Files_RID',
#

#
# The purpose is to refactor the keys and forieng keys of the PDB table to conform to the naming convention.
#

class MyKey:
  def __init__(self, constraint_name, table_name, columns):
    self.constraint_name = constraint_name
    self.table_name = table_name
    self.columns = columns

  def display(self):
    return {'table_name': self.table_name, 'columns': self.columns}

my_keys = {}

def get_my_key(table_name, columns):
    for k,v in my_keys.items():
        if v.table_name == table_name and set(columns) == set(v.columns):
            return v
    return None

renamed_columns = {}
new_columns = {}

messages = []

def write_message(log_file, message):
    if message in messages:
        return
    messages.append(message)
    fw = open(log_file, 'a')
    fw.write('{}\n'.format(message))
    fw.close()

MAX_NAME_LENGTH = 63

KEY_TYPE_SUFFIX_DICT = {
    "COMBO1" : "_combo1_key", 
    "COMBO2" : "_combo2_key",
    "PRIMARY" : "_primary_key",
    "RID" : "_RID_key",
    "UNKNOWN" : "_key",
}

FKEY_TYPE_SUFFIX_DICT = {
    "COMBO1" : "_combo1_fkey", 
    "COMBO2" : "_combo2_fkey",
    "MMCIF" : "_mmcif_fkey",
    "RID" : "_rid_fkey",
    "UNKNOWN" : "_fkey"
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
    ("_reactive_", "_react_"),    
])

TABLE_NAME_DICT = {
    
}
KEY_NAME_DICT = {
    
}

# multiple keys to the same parent tables: 2-column with RID
PARENT_RID_COLUMN_NAME_DICT = {
    # -- May not need for this group of dict. Might be able to use hueristics. But this is fine too.
    ('ihm_cross_link_restraint', 'struct_asym', ('asym_id_1', 'structure_id')) : 'Asym_RID_1',  # Struct_Asym_RID_1
    ('ihm_cross_link_restraint', 'struct_asym', ('asym_id_2', 'structure_id')) : 'Asym_RID_2', 
    ('ihm_derived_distance_restraint', 'ihm_feature_list', ('feature_id_1', 'structure_id')) : 'Feature_RID_1', # Ihm_Feature_List_RID_1 (without Ihm?)
    ('ihm_derived_distance_restraint', 'ihm_feature_list', ('feature_id_2', 'structure_id')) : 'Feature_RID_2', 
    ('ihm_ordered_ensemble', 'ihm_model_group', ('model_group_id_begin', 'structure_id')) : 'Model_Group_RID_Begin',  
    ('ihm_ordered_ensemble', 'ihm_model_group', ('model_group_id_end', 'structure_id')) : 'Model_Group_RID_End',  
    ('ihm_predicted_contact_restraint', 'struct_asym', ('asym_id_1', 'structure_id')) : 'Asym_RID_1',  # Struct_Asym_RID_1
    ('ihm_predicted_contact_restraint', 'struct_asym', ('asym_id_2', 'structure_id')) : 'Asym_RID_2', 
    ('ihm_probe_list', 'ihm_chemical_component_descriptor', ('reactive_probe_chem_comp_descriptor_id')) : 'Reactive_Probe_Chem_Comp_Descriptor_RID', ##! single col 
    ('ihm_probe_list', 'ihm_chemical_component_descriptor', ('probe_chem_comp_descriptor_id')) : 'Probe_Chem_Comp_Descriptor_RID', ##! single column
    ('ihm_related_datasets', 'ihm_dataset_list', ('dataset_list_id_derived', 'structure_id')) : 'Dataset_List_RID_Derived',  
    ('ihm_related_datasets', 'ihm_dataset_list', ('dataset_list_id_primary', 'structure_id')) : 'Dataset_List_RID_Primary',  
    ('ihm_struct_assembly_details', 'ihm_struct_assembly', ('parent_assembly_id', 'structure_id')) : 'Parent_Assembly_RID',  # Ihm_Parent_Struct_Assemboy_RID
    ('ihm_struct_assembly_details', 'ihm_struct_assembly', ('assembly_id', 'structure_id')) : 'Assembly_RID',                # Ihm_Struct_Assembly_RID
    #
    # -- TODO: out of place RID column name. Replace with "Script_File_RID"
    ('ihm_starting_computational_models', 'ihm_external_files', ('script_file_id', 'structure_id')) : 'External_Files_RID',
    #
    # multiple keys to the same parent tables: 4-column with RID. Need to lookup
    ('ihm_cross_link_list', 'entity_poly_seq', ('comp_id_1', 'entity_id_1', 'seq_id_1', 'structure_id')) : 'Entity_Poly_Seq_RID_1', 
    ('ihm_cross_link_list', 'entity_poly_seq', ('comp_id_2', 'entity_id_2', 'seq_id_2', 'structure_id')) : 'Entity_Poly_Seq_RID_2', 
    ('ihm_cross_link_restraint', 'entity_poly_seq', ('comp_id_1', 'entity_id_1', 'seq_id_1', 'structure_id')) : 'Entity_Poly_Seq_RID_1', 
    ('ihm_cross_link_restraint', 'entity_poly_seq', ('comp_id_2', 'entity_id_2', 'seq_id_2', 'structure_id')) : 'Entity_Poly_Seq_RID_2', 
    ('ihm_poly_residue_feature', 'entity_poly_seq', ('comp_id_begin', 'entity_id', 'seq_id_begin', 'structure_id')) : 'Entity_Poly_Seq_RID_Begin', 
    ('ihm_poly_residue_feature', 'entity_poly_seq', ('comp_id_end', 'entity_id', 'seq_id_end', 'structure_id')) : 'Entity_Poly_Seq_RID_End',
    ('ihm_predicted_contact_restraint', 'entity_poly_seq', ('comp_id_1', 'entity_id_1', 'seq_id_1', 'structure_id')) : 'Entity_Poly_Seq_RID_1', 
    ('ihm_predicted_contact_restraint', 'entity_poly_seq', ('comp_id_2', 'entity_id_2', 'seq_id_2', 'structure_id')) : 'Entity_Poly_Seq_RID_2',
    ('ihm_residues_not_modeled', 'entity_poly_seq', ('comp_id_begin', 'entity_id', 'seq_id_begin', 'structure_id')) : 'Entity_Poly_Seq_RID_Begin',     
    ('ihm_residues_not_modeled', 'entity_poly_seq', ('comp_id_end', 'entity_id', 'seq_id_end', 'structure_id')) : 'Entity_Poly_Seq_RID_End', 
}

''' Lookup table based on foreign columns to forieng key name.
    The key is (from_table, to_table, tuple(col_list))
    The names in the dict should not exceed the maximum name length.
'''
FKEY_NAME_DICT = {
    # Names too long. Use hueristics for this group.
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
    #
    # multiple keys to the same parent tables: 2-column with RID.
    # Note: - When remove _ihm_ replace, with _ to easily identify the table.
    #       - All RID column names in this group should follow naming convention above e.g. Struct_asym_1_RID should be Asym_RID_1
    #       - if needed, shorten reactive to react
    ('ihm_cross_link_restraint', 'struct_asym', ('Asym_RID_1', 'asym_id_1', 'structure_id')) : "ihm_cross_link_restraint_struct_asym_1_combo1_fkey",
    ('ihm_cross_link_restraint', 'struct_asym', ('Asym_RID_2', 'asym_id_2', 'structure_id')) : "ihm_cross_link_restraint_struct_asym_2_combo1_fkey",
    ('ihm_derived_distance_restraint', 'ihm_feature_list', ('Feature_RID_1', 'feature_id_1', 'structure_id')) : "ihm_derived_distance_restraint__feature_list_1_combo1_fkey",
    ('ihm_derived_distance_restraint', 'ihm_feature_list', ('Feature_RID_2', 'feature_id_2', 'structure_id')) : "ihm_derived_distance_restraint__feature_list_2_combo1_fkey",
    ('ihm_ordered_ensemble', 'ihm_model_group', ('Model_Group_RID_Begin', 'model_group_id_begin', 'structure_id')) : "ihm_ordered_ensemble__model_group_begin_combo1_fkey",
    ('ihm_ordered_ensemble', 'ihm_model_group', ('Model_Group_RID_End', 'model_group_id_end', 'structure_id')) : "ihm_ordered_ensemble__model_group_end_combo1_fkey",
    ('ihm_predicted_contact_restraint', 'struct_asym', ('Asym_RID_1', 'asym_id_1', 'structure_id')) : "ihm_predicted_contact_restraint_struct_asym_1_combo1_fkey",
    ('ihm_predicted_contact_restraint', 'struct_asym', ('Asym_RID_2', 'asym_id_2', 'structure_id')) : "ihm_predicted_contact_restraint_struct_asym_2_combo1_fkey",
    ('ihm_probe_list', 'ihm_chemical_component_descriptor', ('Reactive_Probe_Chem_Comp_Descriptor_RID', 'reactive_probe_chem_comp_descriptor_id')) : "ihm_probe_list__chem_comp_descriptor_reactive_probe_combo2_fkey",
    ('ihm_probe_list', 'ihm_chemical_component_descriptor', ('Probe_Chem_Comp_Descriptor_RID', 'probe_chem_comp_descriptor_id')) : "ihm_probe_list__chem_comp_descriptor_probe_combo2_fkey", 
    ('ihm_related_datasets', 'ihm_dataset_list', ('Dataset_List_RID_Derived', 'dataset_list_id_derived', 'structure_id')) : "ihm_related_datasets__dataset_list_derived_combo1_fkey",
    ('ihm_related_datasets', 'ihm_dataset_list', ('Dataset_List_RID_Primary', 'dataset_list_id_primary', 'structure_id')) : "ihm_related_datasets__dataset_list_primary_combo1_fkey",
    ('ihm_struct_assembly_details', 'ihm_struct_assembly', ('Parent_Assembly_RID', 'parent_assembly_id', 'structure_id')) : "ihm_struct_assembly_details__struct_assembly_parent_combo1_fkey",
    ('ihm_struct_assembly_details', 'ihm_struct_assembly', ('Assembly_RID', 'assembly_id', 'structure_id')) : "ihm_struct_assembly_details__struct_assembly_combo1_fkey", 
    #
    # multiple keys to the same parent tables: 4-column with RID
    # Note: - The RID column names should be Capitalized e.g. Entity_Poly_Seq_RID_1
    ('ihm_cross_link_list', 'entity_poly_seq', ('Entity_poly_seq_1_RID', 'comp_id_1', 'entity_id_1', 'seq_id_1', 'structure_id')) : "ihm_cross_link_list_entity_poly_seq_1_combo1_fkey",
    ('ihm_cross_link_list', 'entity_poly_seq', ('Entity_poly_seq_2_RID', 'comp_id_2', 'entity_id_2', 'seq_id_2', 'structure_id')) : "ihm_cross_link_list_entity_poly_seq_2_combo1_fkey",
    ('ihm_cross_link_restraint', 'entity_poly_seq', ('Entity_poly_seq_1_RID', 'comp_id_1', 'entity_id_1', 'seq_id_1', 'structure_id')) : "ihm_cross_link_restraint_entity_poly_seq_1_combo1_fkey",
    ('ihm_cross_link_restraint', 'entity_poly_seq', ('Entity_poly_seq_2_RID', 'comp_id_2', 'entity_id_2', 'seq_id_2', 'structure_id')) : "ihm_cross_link_restraint_entity_poly_seq_2_combo1_fkey",
    ('ihm_poly_residue_feature', 'entity_poly_seq', ('Entity_poly_seq_begin_RID', 'comp_id_begin', 'entity_id', 'seq_id_begin', 'structure_id')) : "ihm_poly_residue_feature_entity_poly_seq_begin_combo1_fkey",
    ('ihm_poly_residue_feature', 'entity_poly_seq', ('Entity_poly_seq_end_RID', 'comp_id_end', 'entity_id', 'seq_id_end', 'structure_id')) : "ihm_poly_residue_feature_entity_poly_seq_end_combo1_fkey",
    ('ihm_predicted_contact_restraint', 'entity_poly_seq', ('Entity_poly_seq_1_RID', 'comp_id_1', 'entity_id_1', 'seq_id_1', 'structure_id')) : "ihm_predicted_contact_restraint_entity_poly_seq_1_combo1_fkey",
    ('ihm_predicted_contact_restraint', 'entity_poly_seq', ('Entity_poly_seq_2_RID', 'comp_id_2', 'entity_id_2', 'seq_id_2', 'structure_id')) : "ihm_predicted_contact_restraint_entity_poly_seq_2_combo1_fkey",
    ('ihm_residues_not_modeled', 'entity_poly_seq', ('Entity_poly_seq_begin_RID', 'comp_id_begin', 'entity_id', 'seq_id_begin', 'structure_id')) : "ihm_residues_not_modeled_entity_poly_seq_begin_combo1_fkey",    
    ('ihm_residues_not_modeled', 'entity_poly_seq', ('Entity_poly_seq_end_RID', 'comp_id_end', 'entity_id', 'seq_id_end', 'structure_id')) : "ihm_residues_not_modeled_entity_poly_seq_end_combo1_fkey",
}

# ----------------------------------------------
# print all keys that [RID, structure_id] is a subset of
# key.name returns [schema_obj, constraint_name]
def print_rid_structure_id_keys(model):
    for table in model.schemas["PDB"].tables.values():
        for key in table.keys:
            #if set([ c.name for c in key.unique_columns ]).issubset({'RID', 'structure_id'}) == True:
            if {'RID', 'structure_id'}.issubset(set([ c.name for c in key.unique_columns ])) == True:                                   
                print("%s %s: %s" % (table.name, key.constraint_name, set([ c.name for c in key.unique_columns ])))

# ----------------------------------------------
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

# ----------------------------------------------
# given a primary key, get equivalent combo fkey 
def get_key_name_by_column_names(table, key_column_names):
    rid_included = True if "RID" in key_column_names else False
    struct_id_included = True if "structure_id" in key_column_names else False
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
        key_name = None
    elif key_name != expected_key_name:
        print('WARNING: RENAME KEY in table %s: "%s[%d] v.s. %s[%d]"  # ' % ( table.name, expected_key_name, len(expected_key_name), key_name, len(key_name)))
        write_message('rename.log', 'RENAME KEY {}:{} TO {}'.format(table.name, expected_key_name, key_name))

    return(key_name)


# ----------------------------------------------
''' This function returns a combo1/combo2 names of a foreign key based on the provided flag. 
    If the flag is empty, the combo position in the string is empty. 
    The function consults existing FKEY_NAME_DICT.
    If the name is too long, it will apply string replacement to shorten the names. 
'''
def get_fkey_constraint_name(fkey, expected_fkey_from_col_names, expected_fkey_to_col_names):
    fkey_dict_key = (fkey.table.name, fkey.pk_table.name, tuple(sorted(expected_fkey_from_col_names)))
    rid_included = True if "RID" in expected_fkey_to_col_names else False
    struct_id_included = True if "structure_id" in expected_fkey_to_col_names else False
    fkey_length = len(expected_fkey_to_col_names)
    
    if rid_included and struct_id_included:
        suffix = '_combo1_fkey'
    elif rid_included and fkey_length > 1:
        suffix = '_combo2_fkey'
    elif rid_included and fkey_length == 1:
        suffix = '_RID_fkey'
    elif struct_id_included:
        suffix = '_mmcif_fkey'
    else:
        suffix = '_fkey'
        print("FKEY COLUMN NAME ERROR: fkey_column_names %s is not combo or mmcif key" % (expected_fkey_to_col_names))

    if fkey_dict_key in FKEY_NAME_DICT.keys():
        expected_fkey_constraint_name = FKEY_NAME_DICT[fkey_dict_key]
    else:
        expected_fkey_constraint_name = '_'.join([fkey.table.name, fkey.pk_table.name, suffix[1:]])                            
    
    constraint_name = expected_fkey_constraint_name
    contraint_name_length = len(expected_fkey_constraint_name)
    for old, new in STRING_REPLACEMENT_DICT.items():
        if contraint_name_length <= MAX_NAME_LENGTH:
            break
        constraint_name = constraint_name.replace(old, new)        
        contraint_name_length = len(constraint_name)
        
    if contraint_name_length > MAX_NAME_LENGTH:            
        print('ERROR: FKEY NAME TOO LONG: %s: "%s"  # %d' % ( fkey_dict_key, expected_fkey_constraint_name, len(expected_fkey_constraint_name)))
        constraint_name = None
    elif constraint_name != expected_fkey_constraint_name:
        print('WARNING: FKEY NAME TOO LONG. RENAME FKEY: %s: from %s[%d] to %s[%d] ' % ( fkey_dict_key, expected_fkey_constraint_name, len(expected_fkey_constraint_name), constraint_name, len(constraint_name)))
    
    return(constraint_name)

# ----------------------------------------------
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

# ----------------------------------------------
def get_fkey_rid_column(fkey):
    rid_column = None
    if 'RID' in {c.name for c in fkey.column_map.values()}:
        # check for column_name corresponding to RID in the parent table
        for from_col, to_col in fkey.column_map.items():
            if to_col.name == 'RID':
                rid_column = from_col
    return(rid_column)

# ----------------------------------------------
def get_fkey_id_column(fkey):
    id_column = None
    if 'id' in {c.name for c in fkey.column_map.values()}:
        # check for column_name corresponding to RID in the parent table
        for from_col, to_col in fkey.column_map.items():
            if to_col.name == 'id':
                id_column = from_col
    return(id_column)

# ----------------------------------------------
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

# ----------------------------------------------
# given fkey, get the corresponding fkey based on the fkey_type except itself. 
def get_equivalent_fkey_by_type(fkey, fkey_type="MMCIF"):
    fkey_col_names = {c.name for c in fkey.column_map.keys()}    
    fkey_parent_col_names = {c.name for c in fkey.column_map.values()}

    col_names = fkey_col_names
    parent_rid_col_name = get_fkey_parent_rid_column_name(fkey)
    rid_column_exist = (True if parent_rid_col_name in fkey.table.columns.elements else False)

    # try capitalize: a hack since we have both patterns!!
    if not rid_column_exist:
        # Different naming convention.
        parent_rid_col_name_alt = (parent_rid_col_name.capitalize()).replace("_rid", "_RID")
        rid_column_exist = (True if parent_rid_col_name_alt in fkey.table.columns.elements else False)
        if rid_column_exist:
            # TODO: RENAME RID column to be consistent
            print("WARNING: RID COLUMN NAME MISMATCHED: %s should be %s" % (parent_rid_col_name_alt, parent_rid_col_name))
            write_message('rename.log', 'RENAME COLUMN {}:{} TO {}'.format(fkey.table.name, parent_rid_col_name_alt, parent_rid_col_name))
            if fkey.table.name not in renamed_columns.keys():
                renamed_columns[fkey.table.name] = {}
            if parent_rid_col_name_alt not in renamed_columns[fkey.table.name].keys():
                renamed_columns[fkey.table.name][parent_rid_col_name_alt] = parent_rid_col_name
            elif renamed_columns[fkey.table.name][parent_rid_col_name_alt] != parent_rid_col_name:
                print('WARNING: {}:{} was previous renamed to {}'.format(fkey.table.name, parent_rid_col_name_alt, renamed_columns[fkey.table.name][parent_rid_col_name_alt]))
            #fkey.pk_table.columns[parent_rid_col_name_alt].alter(name=parent_rid_col_name)
        parent_rid_col_name = parent_rid_col_name_alt
        
    #print("-- check equivalent fkey of type %s: %s %s parent_rid:%s" % (fkey_type, fkey.table.name, fkey_col_names, parent_rid_col_name))
    
    # add RID and structure_id if not exist
    if fkey_type == 'COMBO1' and rid_column_exist:
        col_names = fkey_col_names|{parent_rid_col_name, "structure_id"}
    elif fkey_type == 'COMBO2' and rid_column_exist:
        col_names = (fkey_col_names|{parent_rid_col_name}) - {"structure_id"}
    elif fkey_type == 'MMCIF':
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
        print("-- found matching %s fkey: %s : %s => %s -> %s " % (fkey_type, fk.table.name, fk.constraint_name, {c.name for c in fk.column_map.keys()}, {c.name for c in fk.column_map.values()}))
        return(match_list[0])

# ----------------------------------------------
'''paramters:    
   model: relevant ermrest model 
   ncols: number of fkey columns to be investigated
   deriva_included: whether to include fkeys of deriva-related table (i.e. non-mmcif tables)
   combo1_included: whether to include COMBO1 fkeys in the logic
   combo2_included: whether to include COMBO2 fkeys in the logic
   primary_types: the types of primary fkeys to be included e.g. ("COMBO1"). If empty, no primary fkeys will be included. 
'''
def refactor_fkeys(model, ncols, deriva_included=False, combo1_included=True, combo2_included=True, primary_types=('COMBO1', 'COMBO2')):
    schema = model.schemas["PDB"]
    deriva_tables = {'Catalog_Group', 'ERMrest_Client', 'Entry_Related_File'}
    combo1_count = 1
    combo2_count = 1
    primary_count = 1
    
    #print("=========== print_fkeys_with_rid with ncols = %d ================= " % (ncols))
    for table in sorted(schema.tables.values(), key = lambda x: x.name):
        #print("\n====== table: %s ================= " % (table.name))        
        for fkey in table.foreign_keys:
            fkey_length = len(fkey.columns)
            fkey_parent_col_names = {c.name for c in fkey.column_map.values()}
            fkey_col_names = {c.name for c in fkey.column_map.keys()}
            pk_table = fkey.pk_table

            #print("---- %s -> %s : %s : %s -> %s" % (table.name, fkey.pk_table.name, fkey.constraint_name, fkey_col_names, fkey_parent_col_names))
            
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
                    print("[%2d] --c1  p  [%d] %s -> %s : %s : %s -> %s" % (combo1_count, fkey_length, table.name, fkey.pk_table.name, fkey.constraint_name, fkey_col_names, fkey_parent_col_names))
                    # TODO: remove fkey
                    # mmcif_fk.drop()
                else:
                    print("[%2d] --c1      [%d] %s -> %s : %s : %s -> %s" % (combo1_count, fkey_length, table.name, fkey.pk_table.name, fkey.constraint_name, fkey_col_names, fkey_parent_col_names))

                combo1_count = combo1_count + 1

            elif fkey_type == "COMBO2":
                if not combo2_included:
                    continue
                mmcif_fk = get_equivalent_fkey_by_type(fkey, "MMCIF")
                if mmcif_fk:
                    print("[%2d] --c2  p  [%d] %s -> %s : %s : %s -> %s" % (combo2_count, fkey_length, table.name, fkey.pk_table.name, fkey.constraint_name, fkey_col_names, fkey_parent_col_names))
                    # TODO: remove fkey
                    # mmcif_fk.drop()                    
                else:
                    print("[%2d] --c2      [%d] %s -> %s : %s : %s -> %s" % (combo2_count, fkey_length, table.name, fkey.pk_table.name, fkey.constraint_name, fkey_col_names, fkey_parent_col_names))

                combo2_count = combo2_count + 1
            
            elif fkey_type == "MMCIF":
                if not primary_types:
                    continue
                    
                # 1. determine whether it needs combo1 or combo2:
                # Except for structure_id, if a column in the key is not-null, then it is mandatory
                mandatory = False
                for from_col in fkey.column_map:
                    # exclude structure_id 
                    if from_col.name == 'structure_id':
                        continue
                    if from_col.nullok == False:
                        mandatory = True
                        break
                
                # 2. setup variables
                parent_rid_column_name = get_fkey_parent_rid_column_name(fkey)
                if mandatory == True:
                    flag = '1'
                    fkey_type = "COMBO1"
                else:
                    flag = '2'
                    fkey_type = "COMBO2"

                combo_fkey_from_col_names = []
                combo_fkey_to_col_names = []
                # create from column names and to column names in order, so they can be used for creation.
                # add RID
                if fkey_type == "COMBO1" or fkey_type == "COMBO2":
                    combo_fkey_from_col_names.append(parent_rid_column_name)
                    combo_fkey_to_col_names.append("RID")
                for from_col, to_col in fkey.column_map.items():
                    # remove structure_id
                    if fkey_type == "COMBO2" and from_col.name == "structure_id":
                        continue
                    combo_fkey_from_col_names.append(from_col.name)
                    combo_fkey_to_col_names.append(to_col.name)
                    
                # -- selectively omit primary fkeys investigation depending on the flag. This help with the printout readability
                if fkey_type not in primary_types: 
                    continue
                combo_fkey_parent_key_name = get_key_name_by_column_names(pk_table, combo_fkey_to_col_names)
                combo_fkey_constraint_name = get_fkey_constraint_name(fkey, combo_fkey_from_col_names, combo_fkey_to_col_names)
                    
                combo_fk = get_equivalent_fkey_by_type(fkey, fkey_type)
                if combo_fk:
                    # check existing combo names for consistentcy
                    print("[%2d] --p  c%s [%d] %s -> %s : %s : %s -> %s combo:%s" % (primary_count, flag, fkey_length, table.name, fkey.pk_table.name, fkey.constraint_name, fkey_col_names, fkey_parent_col_names, {c.name for c in combo_fk.column_map.keys()}))
                    if (combo_fk.constraint_name != combo_fkey_constraint_name):
                        # TODO: rename fkey if the name are not consistent
                        #combo_fk.alter(constraint_name=combo_fkey_constraint_name)
                        print("       RENAME COMBO_FKEY: from %s[%d] to %s[%d]" % (combo_fk.constraint_name, len(combo_fk.constraint_name), combo_fkey_constraint_name, len(combo_fkey_constraint_name)))
                        write_message('rename.log', 'RENAME FKEY {}:{} TO {}'.format(fkey.table.name, combo_fk.constraint_name, combo_fkey_constraint_name))
                        pass

                else:
                    #create
                    print("[%2d] --p      [%d] %s -> %s : %s : %s -> %s" % (primary_count, fkey_length, table.name, fkey.pk_table.name, fkey.constraint_name, fkey_col_names, fkey_parent_col_names))

                    # 5.1 check parent column in the table
                    if parent_rid_column_name not in table.columns.elements:
                        # TODO: create parent RID column. Can't set nullok to False. Need to set after all rows have RID filled in. 
                        if table.name not in new_columns.keys():
                            new_columns[table.name] = []
                            if parent_rid_column_name not in new_columns[table.name]:
                                new_columns[table.name].append(parent_rid_column_name)
                            else:
                                print('WARNING: {}:{} was previous defined'.format(table.name, parent_rid_column_name))
                        print("    +col: Add new column: %s : %s for fkey %s:%s" % (table.name, parent_rid_column_name, fkey.constraint_name, fkey_col_names))
                        write_message('new.log', 'NEW COLUMN {}:{}'.format(table.name, parent_rid_column_name))
                        #table.create_column(Column.define(
                        #    parent_rid_column_name,
                        #    builtin_types.text,
                        #    nullok=(True if mandatory else False)
                        #))
                        
                    # 5.2 check whether expected key exist in the parent table
                    parent_key = fkey.pk_table.key_by_columns(combo_fkey_to_col_names, raise_nomatch=False) 
                    if parent_key is None:
                        parent_key = get_my_key(pk_table.name, combo_fkey_to_col_names)
                    if parent_key is None:
                        print("    +key: c%s create %s %s:%s" % (flag, pk_table.name, combo_fkey_parent_key_name, combo_fkey_to_col_names))
                        
                        if combo_fkey_parent_key_name in my_keys.keys():
                            print('WARNING: DUPLICATE NEW KEY: {}:{} {}'.format(pk_table.name, combo_fkey_parent_key_name, combo_fkey_to_col_names))
                        else:
                            my_keys[combo_fkey_parent_key_name] = MyKey(combo_fkey_parent_key_name, pk_table.name, combo_fkey_to_col_names)
                            
                        write_message('new.log', 'NEW KEY {}:{} {}'.format(pk_table.name, combo_fkey_parent_key_name, combo_fkey_to_col_names))
                        # TODO: create a new key
                        #Key.define(combo_fkey_to_col_names, constraint_names = [[pk_table.schema.name, combo_fkey_parent_key_name]])
                    else:
                        # TODO: rename incorrect key names
                        if (parent_key.constraint_name != combo_fkey_parent_key_name):
                            print("    *key exists: rename %s from %s to %s" % (combo_fkey_to_col_names, parent_key.constraint_name, combo_fkey_parent_key_name))
                            write_message('rename.log', 'RENAME FKEY {}:{} TO {}'.format(fkey.table.name, fkey.constraint_name, combo_fkey_parent_key_name))
                            #parent_key.alter(name=combo_fkey_parent_key_name)
                            
                    # 5.3 create a new fkey
                    print("    +c%s:  Add fkey(len=%d) %s -> %s : %s : %s -> %s" % (flag, fkey_length, table.name, fkey.pk_table.name, combo_fkey_constraint_name, combo_fkey_from_col_names, combo_fkey_to_col_names))
                    write_message('new.log', 'NEW FKEY {}:{} TO TABLE {} {} {}'.format(table.name, combo_fkey_constraint_name, fkey.pk_table.name, combo_fkey_from_col_names, combo_fkey_to_col_names))
                    # TODO: create fkey
                    #ForeignKey.define(combo_fkey_from_col_names, table.schema.name, table.name, combo_fkey_to_col_names,
                    #                  constraint_names = [[table.schema.name, combo_fkey_constraint_name]],
                    #                  on_update = 'CASECADE',
                    #                  on_delete = 'NO ACTION'
                    #)
                    
                primary_count = primary_count + 1
                print("")
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

    #refactor_fkeys(model, 2, combo1_included=True, combo2_included=False, primary_types=("COMBO1"))
    #refactor_fkeys(model, 2, combo1_included=True, combo2_included=True, primary_types=())
    refactor_fkeys(model, 2, combo1_included=True, combo2_included=True)
    
    """
    Check that the new columns are not among the renamed columns
    """
    for new_column_table, new_column_values in new_columns.items():
        if new_column_table in renamed_columns.keys():
            renamed_values = renamed_columns[new_column_table]
            for new_column in new_column_values:
                for old_column, renamed_column in renamed_values.items():
                    if new_column == renamed_column:
                        print('WARNING: New column {}:{} is also a renamed column'.format(new_column_table, new_column))
            

if __name__ == '__main__':
    args = BaseCLI("ad-hoc table creation tool", None, 1).parse_cli()
    credentials = get_credential(args.host, args.credential_file)
    main(args.host, 99, credentials)
