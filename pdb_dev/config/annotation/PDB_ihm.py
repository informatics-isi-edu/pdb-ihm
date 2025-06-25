import json
from deriva.core import ErmrestCatalog, AttrDict, get_credential, DEFAULT_CREDENTIAL_FILE, tag, urlquote, DerivaServer, get_credential, BaseCLI
from deriva.core.ermrest_model import builtin_types, Schema, Table, Column, Key, ForeignKey
from deriva.core import urlquote, urlunquote
import requests.exceptions
from ...utils.shared import DCCTX, PDBDEV_CLI
from deriva.utils.extras.model import print_schema_model_extras, print_table_model_extras, print_schema_annotations, per_schema_annotation_tags, clear_schema_annotations


# -- ==========================================================================================================
def update_PDB_ihm_2dem_class_average_fitting(model):
    schema = model.schemas["PDB"]
    table = schema.tables["ihm_2dem_class_average_fitting"]
    # ----------------------------
    schema.tables["ihm_2dem_class_average_fitting"].display.update(
        {'name' : '2DEM Class Average Fitting', 'comment_display' : {'*': {'table_comment_display': 'inline'}}, }
    )

    # ----------------------------
    schema.tables["ihm_2dem_class_average_fitting"].visible_columns.update({
        '*' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_2dem_class_average_fitting_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'id', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_2dem_class_average_fitting_restraint_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_2dem_class_average_restraint.id.',
                'markdown_name' : 'Restraint Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_2dem_class_average_fitting_model_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_model_list.model_id.',
                'markdown_name' : 'Model Id',
            },
            'cross_correlation_coefficient', 
            'rot_matrix[1][1]', 
            'rot_matrix[1][2]', 
            'rot_matrix[1][3]', 
            'rot_matrix[2][1]', 
            'rot_matrix[2][2]', 
            'rot_matrix[2][3]', 
            'rot_matrix[3][1]', 
            'rot_matrix[3][2]', 
            'rot_matrix[3][3]', 
            'tr_vector[1]', 
            'tr_vector[2]', 
            'tr_vector[3]', 
        ],
        'entry' :  [
            {
                'source' : [{'outbound': ['PDB', 'ihm_2dem_class_average_fitting_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'id', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_2dem_class_average_fitting_restraint_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_2dem_class_average_restraint.id.',
                'markdown_name' : 'Restraint Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_2dem_class_average_fitting_model_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_model_list.model_id.',
                'markdown_name' : 'Model Id',
            },
            'cross_correlation_coefficient', 
            'rot_matrix[1][1]', 
            'rot_matrix[1][2]', 
            'rot_matrix[1][3]', 
            'rot_matrix[2][1]', 
            'rot_matrix[2][2]', 
            'rot_matrix[2][3]', 
            'rot_matrix[3][1]', 
            'rot_matrix[3][2]', 
            'rot_matrix[3][3]', 
            'tr_vector[1]', 
            'tr_vector[2]', 
            'tr_vector[3]', 
        ],
        'detailed' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_2dem_class_average_fitting_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'id', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_2dem_class_average_fitting_restraint_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_2dem_class_average_restraint.id.',
                'markdown_name' : 'Restraint Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_2dem_class_average_fitting_model_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_model_list.model_id.',
                'markdown_name' : 'Model Id',
            },
            'cross_correlation_coefficient', 
            'rot_matrix[1][1]', 
            'rot_matrix[1][2]', 
            'rot_matrix[1][3]', 
            'rot_matrix[2][1]', 
            'rot_matrix[2][2]', 
            'rot_matrix[2][3]', 
            'rot_matrix[3][1]', 
            'rot_matrix[3][2]', 
            'rot_matrix[3][3]', 
            'tr_vector[1]', 
            'tr_vector[2]', 
            'tr_vector[3]', 
            ['PDB', 'ihm_2dem_class_average_fitting_RCB_fkey'], 
            ['PDB', 'ihm_2dem_class_average_fitting_RMB_fkey'], 
            'RCT', 
            'RMT', 
            ['PDB', 'ihm_2dem_class_average_fitting_Owner_fkey'], 
        ],
    })

    # ----------------------------
    schema.tables["ihm_2dem_class_average_fitting"].foreign_keys[(schema,"ihm_2dem_class_average_fitting_restraint_id_fkey")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })

    # ----------------------------
    schema.tables["ihm_2dem_class_average_fitting"].foreign_keys[(schema,"ihm_2dem_class_average_fitting_model_id_fkey")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })

# -- -----------------------------------------------------------------------------
def update_PDB_ihm_2dem_class_average_restraint(model):
    schema = model.schemas["PDB"]
    table = schema.tables["ihm_2dem_class_average_restraint"]
    # ----------------------------
    schema.tables["ihm_2dem_class_average_restraint"].display.update(
        {'name' : '2DEM Class Average Restraints', 'comment_display' : {'*': {'table_comment_display': 'inline'}}, }
    )

    # ----------------------------
    schema.tables["ihm_2dem_class_average_restraint"].table_display.update({
        'row_name' : { 'row_markdown_pattern' : '{{{id}}}', },
    })

    # ----------------------------
    schema.tables["ihm_2dem_class_average_restraint"].visible_columns.update({
        '*' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_2dem_class_average_restraint_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'id', 
            'number_raw_micrographs', 
            'pixel_size_width', 
            'pixel_size_height', 
            'image_resolution', 
            ['PDB', 'ihm_2dem_class_average_restraint_image_segment_flag_fkey'], 
            'number_of_projections', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_2dem_class_average_restraint_struct_assembly_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_struct_assembly.id.',
                'markdown_name' : 'Struct Assembly Id',
            },
            'details', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_2dem_class_average_restraint_dataset_list_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_dataset_list.id.',
                'markdown_name' : 'Dataset List Id',
            },
        ],
        'entry' :  [
            {
                'source' : [{'outbound': ['PDB', 'ihm_2dem_class_average_restraint_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'id', 
            'number_raw_micrographs', 
            'pixel_size_width', 
            'pixel_size_height', 
            'image_resolution', 
            ['PDB', 'ihm_2dem_class_average_restraint_image_segment_flag_fkey'], 
            'number_of_projections', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_2dem_class_average_restraint_struct_assembly_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_struct_assembly.id.',
                'markdown_name' : 'Struct Assembly Id',
            },
            'details', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_2dem_class_average_restraint_dataset_list_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_dataset_list.id.',
                'markdown_name' : 'Dataset List Id',
            },
        ],
        'detailed' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_2dem_class_average_restraint_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'id', 
            'number_raw_micrographs', 
            'pixel_size_width', 
            'pixel_size_height', 
            'image_resolution', 
            ['PDB', 'ihm_2dem_class_average_restraint_image_segment_flag_fkey'], 
            'number_of_projections', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_2dem_class_average_restraint_struct_assembly_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_struct_assembly.id.',
                'markdown_name' : 'Struct Assembly Id',
            },
            'details', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_2dem_class_average_restraint_dataset_list_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_dataset_list.id.',
                'markdown_name' : 'Dataset List Id',
            },
            ['PDB', 'ihm_2dem_class_average_restraint_RCB_fkey'], 
            ['PDB', 'ihm_2dem_class_average_restraint_RMB_fkey'], 
            'RCT', 
            'RMT', 
            ['PDB', 'ihm_2dem_class_average_restraint_Owner_fkey'], 
        ],
    })
    
    # ----------------------------
    schema.tables["ihm_2dem_class_average_restraint"].visible_foreign_keys.update({
        'filter' :  'detailed',
        'detailed' :  [
            ['PDB', 'ihm_2dem_class_average_fitting_restraint_id_fkey'], 
        ],
    })

    # ----------------------------
    schema.tables["ihm_2dem_class_average_restraint"].columns["number_raw_micrographs"].display.update(
        {'name' : 'Number of Raw Micrographs', }
    )

    # ----------------------------
    schema.tables["ihm_2dem_class_average_restraint"].foreign_keys[(schema,"ihm_2dem_class_average_restraint_dataset_list_id_fkey")].foreign_key.update(
        {
            'domain_filter_pattern' :  'structure_id={{structure_id}}',
        }
    )

    # ----------------------------
    schema.tables["ihm_2dem_class_average_restraint"].foreign_keys[(schema,"ihm_2dem_class_average_restraint_struct_assembly_id_fkey")].foreign_key.update(
        {
            'domain_filter_pattern' :  'structure_id={{structure_id}}',
        }
    )


# -- -----------------------------------------------------------------------------

def update_PDB_ihm_3dem_restraint(model):
    schema = model.schemas["PDB"]
    table = schema.tables["ihm_3dem_restraint"]
    # ----------------------------
    schema.tables["ihm_3dem_restraint"].display.update(
        {'name' : '3DEM Restraints', 'comment_display' : {'*': {'table_comment_display': 'inline'}}, }
    )

    # ----------------------------
    schema.tables["ihm_3dem_restraint"].visible_columns.update({
        '*' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_3dem_restraint_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'id', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_3dem_restraint_model_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_model_list.model_id.',
                'markdown_name' : 'Model Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_3dem_restraint_struct_assembly_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_struct_assembly.id.',
                'markdown_name' : 'Struct Assembly Id',
            },
            'fitting_method', 
            'number_of_gaussians', 
            ['PDB', 'ihm_3dem_restraint_map_segment_flag_fkey'], 
            'cross_correlation_coefficient', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_3dem_restraint_fitting_method_citation_id_fkey']}, 'RID'],
                'comment' : 'A reference to table citation.id.',
                'markdown_name' : 'Fitting Method Citation Id',
            },
            'details', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_3dem_restraint_dataset_list_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_dataset_list.id.',
                'markdown_name' : 'Dataset List Id',
            },
        ],
        'entry' :  [
            {
                'source' : [{'outbound': ['PDB', 'ihm_3dem_restraint_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'id', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_3dem_restraint_model_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_model_list.model_id.',
                'markdown_name' : 'Model Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_3dem_restraint_struct_assembly_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_struct_assembly.id.',
                'markdown_name' : 'Struct Assembly Id',
            },
            'fitting_method', 
            'number_of_gaussians', 
            ['PDB', 'ihm_3dem_restraint_map_segment_flag_fkey'], 
            'cross_correlation_coefficient', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_3dem_restraint_fitting_method_citation_id_fkey']}, 'RID'],
                'comment' : 'A reference to table citation.id.',
                'markdown_name' : 'Fitting Method Citation Id',
            },
            'details', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_3dem_restraint_dataset_list_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_dataset_list.id.',
                'markdown_name' : 'Dataset List Id',
            },
        ],
        'detailed' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_3dem_restraint_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'id', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_3dem_restraint_model_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_model_list.model_id.',
                'markdown_name' : 'Model Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_3dem_restraint_struct_assembly_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_struct_assembly.id.',
                'markdown_name' : 'Struct Assembly Id',
            },
            'fitting_method', 
            'number_of_gaussians', 
            ['PDB', 'ihm_3dem_restraint_map_segment_flag_fkey'], 
            'cross_correlation_coefficient', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_3dem_restraint_fitting_method_citation_id_fkey']}, 'RID'],
                'comment' : 'A reference to table citation.id.',
                'markdown_name' : 'Fitting Method Citation Id',
            },
            'details', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_3dem_restraint_dataset_list_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_dataset_list.id.',
                'markdown_name' : 'Dataset List Id',
            },
            ['PDB', 'ihm_3dem_restraint_RCB_fkey'], 
            ['PDB', 'ihm_3dem_restraint_RMB_fkey'], 
            'RCT', 
            'RMT', 
            ['PDB', 'ihm_3dem_restraint_Owner_fkey'], 
        ],
    })

    # ----------------------------
    schema.tables["ihm_3dem_restraint"].foreign_keys[(schema,"ihm_3dem_restraint_fitting_method_citation_id_fkey")].foreign_key.update({
            'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })

    # ----------------------------
    schema.tables["ihm_3dem_restraint"].foreign_keys[(schema,"ihm_3dem_restraint_fitting_method_citation_id_fk")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })

    # ----------------------------
    schema.tables["ihm_3dem_restraint"].foreign_keys[(schema,"ihm_3dem_restraint_dataset_list_id_fkey")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })

    # ----------------------------
    schema.tables["ihm_3dem_restraint"].foreign_keys[(schema,"ihm_3dem_restraint_model_id_fkey")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })

    # ----------------------------
    schema.tables["ihm_3dem_restraint"].foreign_keys[(schema,"ihm_3dem_restraint_struct_assembly_id_fkey")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })

# -- -----------------------------------------------------------------------------
def update_PDB_ihm_chemical_component_descriptor(model):
    schema = model.schemas["PDB"]
    table = schema.tables["ihm_chemical_component_descriptor"]
    # ----------------------------
    schema.tables["ihm_chemical_component_descriptor"].display.update(
        {'name' : 'Chemical Descriptors', 'comment_display' : {'*': {'table_comment_display': 'inline'}}, }
    )

    # ----------------------------
    schema.tables["ihm_chemical_component_descriptor"].visible_columns.update({
        '*' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_chemical_component_descriptor_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'id', 
            'chemical_name', 
            'common_name', 
            'auth_name', 
            'smiles', 
            'smiles_canonical', 
            'inchi', 
            'inchi_key', 
            'details', 
        ],
        'entry' :  [
            {
                'source' : [{'outbound': ['PDB', 'ihm_chemical_component_descriptor_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'id', 
            'chemical_name', 
            'common_name', 
            'auth_name', 
            'smiles', 
            'smiles_canonical', 
            'inchi', 
            'inchi_key', 
            'details', 
        ],
        'detailed' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_chemical_component_descriptor_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'id', 
            'chemical_name', 
            'common_name', 
            'auth_name', 
            'smiles', 
            'smiles_canonical', 
            'inchi', 
            'inchi_key', 
            'details', 
            ['PDB', 'ihm_chemical_component_descriptor_RCB_fkey'], 
            ['PDB', 'ihm_chemical_component_descriptor_RMB_fkey'], 
            'RCT', 
            'RMT', 
            ['PDB', 'ihm_chemical_component_descriptor_Owner_fkey'], 
        ],
    })

    # ----------------------------
    schema.tables["ihm_chemical_component_descriptor"].visible_foreign_keys.update(
        {
            'filter' :  'detailed',
            'detailed' :  [
                ['PDB', 'ihm_cross_link_list_linker_chem_comp_descriptor_id_fkey'], 
                ['PDB', 'ihm_probe_list_probe_chem_comp_descriptor_id_fkey'], 
                ['PDB', 'ihm_probe_list_reactive_probe_chem_comp_descriptor_id_fkey'], 
                ['PDB', 'ihm_poly_probe_position_mod_res_chem_comp_descriptor_id_fkey'], 
                ['PDB', 'ihm_poly_probe_conjugate_chem_comp_descriptor_id_fkey'], 
            ],
        }
    )


# -- -----------------------------------------------------------------------------
def update_PDB_ihm_cross_link_list(model):
    schema = model.schemas["PDB"]
    table = schema.tables["ihm_cross_link_list"]
    # ----------------------------
    schema.tables["ihm_cross_link_list"].display.update(
        {'name' : 'Chemical Crosslinks from Experiments', 'comment_display' : {'*': {'table_comment_display': 'inline'}}, }
    )

    # ----------------------------
    schema.tables["ihm_cross_link_list"].table_display.update(
        {
            'row_name' : { 'row_markdown_pattern' : '{{{id}}}', },
        }
    )

    # ----------------------------
    schema.tables["ihm_cross_link_list"].visible_columns.update({
        '*' :  [
            {'source' : 'RID', },
            {'source' : [{'outbound': ['PDB', 'ihm_cross_link_list_structure_id_fkey']}, 'RID'], },
            'id', 
            'group_id', 
            'entity_description_1', 
            'entity_description_2', 
            {'source' : [{'outbound': ['PDB', 'ihm_cross_link_list_mm_poly_res_label_1_fkey']}, 'entity_id'], 'markdown_name' : 'Entity Id 1', },
            {'source' : [{'outbound': ['PDB', 'ihm_cross_link_list_mm_poly_res_label_2_fkey']}, 'entity_id'], 'markdown_name' : 'Entity Id 2', },
            {'source' : [{'outbound': ['PDB', 'ihm_cross_link_list_mm_poly_res_label_1_fkey']}, 'mon_id'], 'markdown_name' : 'Component Id 1', },
            {'source' : [{'outbound': ['PDB', 'ihm_cross_link_list_mm_poly_res_label_2_fkey']}, 'mon_id'], 'markdown_name' : 'Component Id 2', },
            {'source' : [{'outbound': ['PDB', 'ihm_cross_link_list_mm_poly_res_label_1_fkey']}, 'num'], 'markdown_name' : 'Sequence Id 1', },
            {'source' : [{'outbound': ['PDB', 'ihm_cross_link_list_mm_poly_res_label_2_fkey']}, 'num'], 'markdown_name' : 'Sequence Id 2', },
            ['PDB', 'ihm_cross_link_list_linker_type_fkey'], 
            {
                'source' : [{'outbound': ['PDB', 'ihm_cross_link_list_linker_chem_comp_descriptor_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_chemical_component_descriptor.id for the cross linker.',
                'markdown_name' : 'Linker Chemical Component Descriptor Id',
            },
            'details', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_cross_link_list_dataset_list_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_dataset_list.id.',
                'markdown_name' : 'Dataset List Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_cross_link_list_mm_poly_res_label_1_fkey']}, 'RID'],
                'comment' : 'Refers to a combination of Entity Id, Sequence Id and Component Id in the entity_poly_seq table.',
                'markdown_name' : 'Polymeric Residue 1',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_cross_link_list_mm_poly_res_label_2_fkey']}, 'RID'],
                'comment' : 'Refers to a combination of Entity Id, Sequence Id and Component Id in the entity_poly_seq table.',
                'markdown_name' : 'Polymeric Residue 2',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_cross_link_list_Entry_Related_File_fkey']}, 'RID'],
                'comment' : 'A reference to the uploaded restraint file in the table Entry_Related_File.id.',
                'markdown_name' : 'Uploaded Restraint File',
            },
        ],
        'entry' :  [
            {'source' : [{'outbound': ['PDB', 'ihm_cross_link_list_structure_id_fkey']}, 'RID'], },
            'id', 
            'group_id', 
            'entity_description_1', 
            'entity_description_2', 
            {'source' : [{'outbound': ['PDB', 'ihm_cross_link_list_mm_poly_res_label_1_fkey']}, 'entity_id'], 'markdown_name' : 'Entity Id 1', },
            {'source' : [{'outbound': ['PDB', 'ihm_cross_link_list_mm_poly_res_label_2_fkey']}, 'entity_id'], 'markdown_name' : 'Entity Id 2', },
            {'source' : [{'outbound': ['PDB', 'ihm_cross_link_list_mm_poly_res_label_1_fkey']}, 'mon_id'], 'markdown_name' : 'Component Id 1', },
            {'source' : [{'outbound': ['PDB', 'ihm_cross_link_list_mm_poly_res_label_2_fkey']}, 'mon_id'], 'markdown_name' : 'Component Id 2', },
            {'source' : [{'outbound': ['PDB', 'ihm_cross_link_list_mm_poly_res_label_1_fkey']}, 'num'], 'markdown_name' : 'Sequence Id 1', },
            {'source' : [{'outbound': ['PDB', 'ihm_cross_link_list_mm_poly_res_label_2_fkey']}, 'num'], 'markdown_name' : 'Sequence Id 2', },
            ['PDB', 'ihm_cross_link_list_linker_type_fkey'], 
            {
                'source' : [{'outbound': ['PDB', 'ihm_cross_link_list_linker_chem_comp_descriptor_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_chemical_component_descriptor.id for the cross linker.',
                'markdown_name' : 'Linker Chemical Component Descriptor Id',
            },
            'details', 
            ['PDB', 'ihm_cross_link_list_dataset_list_id_fkey'], 
            {
                'source' : [{'outbound': ['PDB', 'ihm_cross_link_list_mm_poly_res_label_1_fkey']}, 'RID'],
                'comment' : 'Refers to a combination of Entity Id, Sequence Id and Component Id in the entity_poly_seq table.',
                'markdown_name' : 'Polymeric Residue 1',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_cross_link_list_mm_poly_res_label_2_fkey']}, 'RID'],
                'comment' : 'Refers to a combination of Entity Id, Sequence Id and Component Id in the entity_poly_seq table.',
                'markdown_name' : 'Polymeric Residue 2',
            },
        ],
        'detailed' :  [
            {'source' : 'RID', },
            {'source' : [{'outbound': ['PDB', 'ihm_cross_link_list_structure_id_fkey']}, 'RID'], },
            'id', 
            'group_id', 
            'entity_description_1', 
            'entity_description_2', 
            {'source' : [{'outbound': ['PDB', 'ihm_cross_link_list_mm_poly_res_label_1_fkey']}, 'entity_id'], 'markdown_name' : 'Entity Id 1', },
            {'source' : [{'outbound': ['PDB', 'ihm_cross_link_list_mm_poly_res_label_2_fkey']}, 'entity_id'], 'markdown_name' : 'Entity Id 2', },
            {'source' : [{'outbound': ['PDB', 'ihm_cross_link_list_mm_poly_res_label_1_fkey']}, 'mon_id'], 'markdown_name' : 'Component Id 1', },
            {'source' : [{'outbound': ['PDB', 'ihm_cross_link_list_mm_poly_res_label_2_fkey']}, 'mon_id'], 'markdown_name' : 'Component Id 2', },
            {'source' : [{'outbound': ['PDB', 'ihm_cross_link_list_mm_poly_res_label_1_fkey']}, 'num'], 'markdown_name' : 'Sequence Id 1', },
            {'source' : [{'outbound': ['PDB', 'ihm_cross_link_list_mm_poly_res_label_2_fkey']}, 'num'], 'markdown_name' : 'Sequence Id 2', },
            ['PDB', 'ihm_cross_link_list_linker_type_fkey'], 
            {
                'source' : [{'outbound': ['PDB', 'ihm_cross_link_list_linker_chem_comp_descriptor_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_chemical_component_descriptor.id for the cross linker.',
                'markdown_name' : 'Linker Chemical Component Descriptor Id',
            },
            'details', 
            ['PDB', 'ihm_cross_link_list_dataset_list_id_fkey'], 
            {
                'source' : [{'outbound': ['PDB', 'ihm_cross_link_list_mm_poly_res_label_1_fkey']}, 'RID'],
                'comment' : 'Refers to a combination of Entity Id, Sequence Id and Component Id in the entity_poly_seq table.',
                'markdown_name' : 'Polymeric Residue 1',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_cross_link_list_mm_poly_res_label_2_fkey']}, 'RID'],
                'comment' : 'Refers to a combination of Entity Id, Sequence Id and Component Id in the entity_poly_seq table.',
                'markdown_name' : 'Polymeric Residue 2',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_cross_link_list_Entry_Related_File_fkey']}, 'RID'],
                'comment' : 'A reference to the uploaded restraint file in the table Entry_Related_File.id.',
                'markdown_name' : 'Uploaded Restraint File',
            },
            {'source' : 'RCT', },
            {'source' : 'RMT', },
            {'source' : [{'outbound': ['PDB', 'ihm_cross_link_list_RCB_fkey']}, 'RID'], },
            {'source' : [{'outbound': ['PDB', 'ihm_cross_link_list_RMB_fkey']}, 'RID'], },
            {'source' : [{'outbound': ['PDB', 'ihm_cross_link_list_Owner_fkey']}, 'RID'], },
        ],
    })
    
    # ----------------------------
    schema.tables["ihm_cross_link_list"].visible_foreign_keys.update(
        {
            'filter' :  'detailed',
            'detailed' :  [
                ['PDB', 'ihm_cross_link_restraint_group_id_fkey'], 
            ],
        }
    )

    # ----------------------------
    schema.tables["ihm_cross_link_list"].foreign_keys[(schema,"ihm_cross_link_list_linker_chem_comp_descriptor_id_fk")].foreign_key.update(
        {
            'domain_filter_pattern' :  'structure_id={{structure_id}}',
        }
    )

    # ----------------------------
    schema.tables["ihm_cross_link_list"].foreign_keys[(schema,"ihm_cross_link_list_linker_chem_comp_descriptor_id_fkey")].foreign_key.update(
        {
            'domain_filter_pattern' :  'structure_id={{structure_id}}',
        }
    )

    # ----------------------------
    schema.tables["ihm_cross_link_list"].foreign_keys[(schema,"ihm_cross_link_list_mm_poly_res_label_1_fkey")].foreign_key.update(
        {
            'from_name' :  'Ihm Cross Link List Label 1',
            'template_engine' :  'handlebars',
            'domain_filter_pattern' :  '{{#if _structure_id}}structure_id={{{_structure_id}}}{{/if}}',
        }
    )

    # ----------------------------
    schema.tables["ihm_cross_link_list"].foreign_keys[(schema,"ihm_cross_link_list_dataset_list_id_fkey")].foreign_key.update(
        {
            'template_engine' :  'handlebars',
            'domain_filter_pattern' :  '{{#if _structure_id}}structure_id={{{_structure_id}}}{{/if}}',
        }
    )

    # ----------------------------
    schema.tables["ihm_cross_link_list"].foreign_keys[(schema,"ihm_cross_link_list_mm_poly_res_label_2_fkey")].foreign_key.update(
        {
            'from_name' :  'Ihm Cross Link List Label 2',
            'template_engine' :  'handlebars',
            'domain_filter_pattern' :  '{{#if _structure_id}}structure_id={{{_structure_id}}}{{/if}}',
        }
    )


# -- -----------------------------------------------------------------------------
def update_PDB_ihm_cross_link_pseudo_site(model):
    schema = model.schemas["PDB"]
    table = schema.tables["ihm_cross_link_pseudo_site"]
    # ----------------------------
    schema.tables["ihm_cross_link_pseudo_site"].display.update(
        {'name' : 'Chemical Crosslinks with Pseudo Sites', 'comment_display' : {'*': {'table_comment_display': 'inline'}}, }
    )

    # ----------------------------
    schema.tables["ihm_cross_link_pseudo_site"].visible_columns.update({
        '*' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_cross_link_pseudo_site_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'id', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_cross_link_pseudo_site_ihm_cross_link_restraint_combo1_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_cross_link_restraint.id.',
                'markdown_name' : 'Restraint Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_cross_link_pseudo_site_ihm_model_list_combo2_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_model_list.model_id.',
                'markdown_name' : 'Model Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_cross_link_pseudo_site_ihm_pseudo_site_combo1_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_pseudo_site.id.',
                'markdown_name' : 'Pseudo Site Id',
            },
            ['PDB', 'ihm_cross_link_pseudo_site_cross_link_partner_fkey'], 
            {
                'source' : [{'outbound': ['PDB', 'ihm_cross_link_pseudo_site_Entry_Related_File_fkey']}, 'RID'],
                'comment' : 'A reference to the uploaded restraint file in the table Entry_Related_File.id.',
                'markdown_name' : 'Uploaded Restraint File',
            },
        ],
        'entry' :  [
            {
                'source' : [{'outbound': ['PDB', 'ihm_cross_link_pseudo_site_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'id', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_cross_link_pseudo_site_ihm_cross_link_restraint_combo1_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_cross_link_restraint.id.',
                'markdown_name' : 'Restraint Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_cross_link_pseudo_site_ihm_model_list_combo2_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_model_list.model_id.',
                'markdown_name' : 'Model Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_cross_link_pseudo_site_ihm_pseudo_site_combo1_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_pseudo_site.id.',
                'markdown_name' : 'Pseudo Site Id',
            },
            ['PDB', 'ihm_cross_link_pseudo_site_cross_link_partner_fkey'], 
        ],
        'detailed' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_cross_link_pseudo_site_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'id', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_cross_link_pseudo_site_ihm_cross_link_restraint_combo1_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_cross_link_restraint.id.',
                'markdown_name' : 'Restraint Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_cross_link_pseudo_site_ihm_model_list_combo2_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_model_list.model_id.',
                'markdown_name' : 'Model Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_cross_link_pseudo_site_ihm_pseudo_site_combo1_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_pseudo_site.id.',
                'markdown_name' : 'Pseudo Site Id',
            },
            ['PDB', 'ihm_cross_link_pseudo_site_cross_link_partner_fkey'], 
            {
                'source' : [{'outbound': ['PDB', 'ihm_cross_link_pseudo_site_Entry_Related_File_fkey']}, 'RID'],
                'comment' : 'A reference to the uploaded restraint file in the table Entry_Related_File.id.',
                'markdown_name' : 'Uploaded Restraint File',
            },
            ['PDB', 'ihm_cross_link_pseudo_site_RCB_fkey'], 
            ['PDB', 'ihm_cross_link_pseudo_site_RMB_fkey'], 
            'RCT', 
            'RMT', 
            ['PDB', 'ihm_cross_link_pseudo_site_Owner_fkey'], 
        ],
    })

    # ----------------------------
    schema.tables["ihm_cross_link_pseudo_site"].foreign_keys[(schema,"ihm_cross_link_pseudo_site_ihm_model_list_combo2_fkey")].foreign_key.update(
        {
            'template_engine' :  'handlebars',
            'domain_filter_pattern' :  '{{#if _structure_id}}structure_id={{{_structure_id}}}{{/if}}',
        }
    )

    # ----------------------------
    schema.tables["ihm_cross_link_pseudo_site"].foreign_keys[(schema,"ihm_cross_link_pseudo_site_ihm_cross_link_restraint_combo1_fkey")].foreign_key.update(
        {
            'template_engine' :  'handlebars',
            'domain_filter_pattern' :  '{{#if _structure_id}}structure_id={{{_structure_id}}}{{/if}}',
        }
    )

    # ----------------------------
    schema.tables["ihm_cross_link_pseudo_site"].foreign_keys[(schema,"ihm_cross_link_pseudo_site_ihm_pseudo_site_combo1_fkey")].foreign_key.update(
        {
            'template_engine' :  'handlebars',
            'domain_filter_pattern' :  '{{#if _structure_id}}structure_id={{{_structure_id}}}{{/if}}',
        }
    )


# -- -----------------------------------------------------------------------------
def update_PDB_ihm_cross_link_restraint(model):
    schema = model.schemas["PDB"]
    table = schema.tables["ihm_cross_link_restraint"]
    # ----------------------------
    schema.tables["ihm_cross_link_restraint"].display.update(
        {'name' : 'Chemical Crosslinking Restraints', 'comment_display' : {'*': {'table_comment_display': 'inline'}}, }
    )

    # ----------------------------
    schema.tables["ihm_cross_link_restraint"].table_display.update(
        {
            'row_name' : { 'row_markdown_pattern' : '{{{id}}}', },
        }
    )

    # ----------------------------
    schema.tables["ihm_cross_link_restraint"].visible_columns.update({
        '*' :  [
            {'source' : 'RID', },
            {'source' : [{'outbound': ['PDB', 'ihm_cross_link_restraint_structure_id_fkey']}, 'RID'], },
            'id', 
            {'source' : [{'outbound': ['PDB', 'ihm_cross_link_restraint_group_id_fkey']}, 'RID'], 'markdown_name' : 'Group Id', },
            {'source' : [{'outbound': ['PDB', 'ihm_cross_link_restraint_mm_poly_res_label_1_fkey']}, 'entity_id'], 'markdown_name' : 'Entity Id 1', },
            {'source' : [{'outbound': ['PDB', 'ihm_cross_link_restraint_mm_poly_res_label_2_fkey']}, 'entity_id'], 'markdown_name' : 'Entity Id 2', },
            {'source' : [{'outbound': ['PDB', 'ihm_cross_link_restraint_asym_id_1_fkey']}, 'RID'], 'markdown_name' : 'Asym Id 1', },
            {'source' : [{'outbound': ['PDB', 'ihm_cross_link_restraint_asym_id_2_fkey']}, 'RID'], 'markdown_name' : 'Asym Id 2', },
            {'source' : [{'outbound': ['PDB', 'ihm_cross_link_restraint_mm_poly_res_label_1_fkey']}, 'mon_id'], 'markdown_name' : 'Component Id 1', },
            {'source' : [{'outbound': ['PDB', 'ihm_cross_link_restraint_mm_poly_res_label_2_fkey']}, 'mon_id'], 'markdown_name' : 'Component Id 2', },
            {'source' : [{'outbound': ['PDB', 'ihm_cross_link_restraint_mm_poly_res_label_1_fkey']}, 'num'], 'markdown_name' : 'Sequence Id 1', },
            {'source' : [{'outbound': ['PDB', 'ihm_cross_link_restraint_mm_poly_res_label_2_fkey']}, 'num'], 'markdown_name' : 'Sequence Id 2', },
            {'source' : 'atom_id_1', },
            {'source' : 'atom_id_2', },
            {'source' : [{'outbound': ['PDB', 'ihm_cross_link_restraint_restraint_type_fkey']}, 'RID'], },
            ['PDB', 'ihm_cross_link_restraint_conditional_crosslink_flag_fkey'], 
            ['PDB', 'ihm_cross_link_restraint_pseudo_site_flag_fkey'], 
            {'source' : [{'outbound': ['PDB', 'ihm_cross_link_restraint_model_granularity_fkey']}, 'RID'], },
            {'source' : 'distance_threshold', },
            {'source' : 'psi', },
            {'source' : 'sigma_1', },
            {'source' : 'sigma_2', },
            {
                'source' : [{'outbound': ['PDB', 'ihm_cross_link_restraint_mm_poly_res_label_1_fkey']}, 'RID'],
                'comment' : 'Refers to a combination of Entity Id, Sequence Id and Component Id in the entity_poly_seq table.',
                'markdown_name' : 'Polymeric Residue 1',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_cross_link_restraint_mm_poly_res_label_2_fkey']}, 'RID'],
                'comment' : 'Refers to a combination of Entity Id, Sequence Id and Component Id in the entity_poly_seq table.',
                'markdown_name' : 'Polymeric Residue 2',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_cross_link_restraint_Entry_Related_File_fkey']}, 'RID'],
                'comment' : 'A reference to the uploaded restraint file in the table Entry_Related_File.id.',
                'markdown_name' : 'Uploaded Restraint File',
            },
        ],
        'entry' :  [
            {'source' : [{'outbound': ['PDB', 'ihm_cross_link_restraint_structure_id_fkey']}, 'RID'], },
            'id', 
            {'source' : [{'outbound': ['PDB', 'ihm_cross_link_restraint_group_id_fkey']}, 'RID'], 'markdown_name' : 'Group Id', },
            {'source' : [{'outbound': ['PDB', 'ihm_cross_link_restraint_mm_poly_res_label_1_fkey']}, 'entity_id'], 'markdown_name' : 'Entity Id 1', },
            {'source' : [{'outbound': ['PDB', 'ihm_cross_link_restraint_mm_poly_res_label_2_fkey']}, 'entity_id'], 'markdown_name' : 'Entity Id 2', },
            {'source' : [{'outbound': ['PDB', 'ihm_cross_link_restraint_asym_id_1_fkey']}, 'RID'], 'markdown_name' : 'Asym Id 1', },
            {'source' : [{'outbound': ['PDB', 'ihm_cross_link_restraint_asym_id_2_fkey']}, 'RID'], 'markdown_name' : 'Asym Id 2', },
            {'source' : [{'outbound': ['PDB', 'ihm_cross_link_restraint_mm_poly_res_label_1_fkey']}, 'mon_id'], 'markdown_name' : 'Component Id 1', },
            {'source' : [{'outbound': ['PDB', 'ihm_cross_link_restraint_mm_poly_res_label_2_fkey']}, 'mon_id'], 'markdown_name' : 'Component Id 2', },
            {'source' : [{'outbound': ['PDB', 'ihm_cross_link_restraint_mm_poly_res_label_1_fkey']}, 'num'], 'markdown_name' : 'Sequence Id 1', },
            {'source' : [{'outbound': ['PDB', 'ihm_cross_link_restraint_mm_poly_res_label_2_fkey']}, 'num'], 'markdown_name' : 'Sequence Id 2', },
            {'source' : 'atom_id_1', },
            {'source' : 'atom_id_2', },
            {'source' : [{'outbound': ['PDB', 'ihm_cross_link_restraint_restraint_type_fkey']}, 'RID'], },
            ['PDB', 'ihm_cross_link_restraint_conditional_crosslink_flag_fkey'], 
            ['PDB', 'ihm_cross_link_restraint_pseudo_site_flag_fkey'], 
            {'source' : [{'outbound': ['PDB', 'ihm_cross_link_restraint_model_granularity_fkey']}, 'RID'], },
            {'source' : 'distance_threshold', },
            {'source' : 'psi', },
            {'source' : 'sigma_1', },
            {'source' : 'sigma_2', },
            {
                'source' : [{'outbound': ['PDB', 'ihm_cross_link_restraint_mm_poly_res_label_1_fkey']}, 'RID'],
                'comment' : 'Refers to a combination of Entity Id, Sequence Id and Component Id in the entity_poly_seq table.',
                'markdown_name' : 'Polymeric Residue 1',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_cross_link_restraint_mm_poly_res_label_2_fkey']}, 'RID'],
                'comment' : 'Refers to a combination of Entity Id, Sequence Id and Component Id in the entity_poly_seq table.',
                'markdown_name' : 'Polymeric Residue 2',
            },
        ],
        'detailed' :  [
            {'source' : 'RID', },
            {'source' : [{'outbound': ['PDB', 'ihm_cross_link_restraint_structure_id_fkey']}, 'RID'], },
            'id', 
            {'source' : [{'outbound': ['PDB', 'ihm_cross_link_restraint_group_id_fkey']}, 'RID'], 'markdown_name' : 'Group Id', },
            {'source' : [{'outbound': ['PDB', 'ihm_cross_link_restraint_mm_poly_res_label_1_fkey']}, 'entity_id'], 'markdown_name' : 'Entity Id 1', },
            {'source' : [{'outbound': ['PDB', 'ihm_cross_link_restraint_mm_poly_res_label_2_fkey']}, 'entity_id'], 'markdown_name' : 'Entity Id 2', },
            {'source' : [{'outbound': ['PDB', 'ihm_cross_link_restraint_asym_id_1_fkey']}, 'RID'], 'markdown_name' : 'Asym Id 1', },
            {'source' : [{'outbound': ['PDB', 'ihm_cross_link_restraint_asym_id_2_fkey']}, 'RID'], 'markdown_name' : 'Asym Id 2', },
            {'source' : [{'outbound': ['PDB', 'ihm_cross_link_restraint_mm_poly_res_label_1_fkey']}, 'mon_id'], 'markdown_name' : 'Component Id 1', },
            {'source' : [{'outbound': ['PDB', 'ihm_cross_link_restraint_mm_poly_res_label_2_fkey']}, 'mon_id'], 'markdown_name' : 'Component Id 2', },
            {'source' : [{'outbound': ['PDB', 'ihm_cross_link_restraint_mm_poly_res_label_1_fkey']}, 'num'], 'markdown_name' : 'Sequence Id 1', },
            {'source' : [{'outbound': ['PDB', 'ihm_cross_link_restraint_mm_poly_res_label_2_fkey']}, 'num'], 'markdown_name' : 'Sequence Id 2', },
            {'source' : 'atom_id_1', },
            {'source' : 'atom_id_2', },
            {'source' : [{'outbound': ['PDB', 'ihm_cross_link_restraint_restraint_type_fkey']}, 'RID'], },
            ['PDB', 'ihm_cross_link_restraint_conditional_crosslink_flag_fkey'], 
            ['PDB', 'ihm_cross_link_restraint_pseudo_site_flag_fkey'], 
            {'source' : [{'outbound': ['PDB', 'ihm_cross_link_restraint_model_granularity_fkey']}, 'RID'], },
            {'source' : 'distance_threshold', },
            {'source' : 'psi', },
            {'source' : 'sigma_1', },
            {'source' : 'sigma_2', },
            {
                'source' : [{'outbound': ['PDB', 'ihm_cross_link_restraint_mm_poly_res_label_1_fkey']}, 'RID'],
                'comment' : 'Refers to a combination of Entity Id, Sequence Id and Component Id in the entity_poly_seq table.',
                'markdown_name' : 'Polymeric Residue 1',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_cross_link_restraint_mm_poly_res_label_2_fkey']}, 'RID'],
                'comment' : 'Refers to a combination of Entity Id, Sequence Id and Component Id in the entity_poly_seq table.',
                'markdown_name' : 'Polymeric Residue 2',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_cross_link_restraint_Entry_Related_File_fkey']}, 'RID'],
                'comment' : 'A reference to the uploaded restraint file in the table Entry_Related_File.id.',
                'markdown_name' : 'Uploaded Restraint File',
            },
            {'source' : 'RCT', },
            {'source' : 'RMT', },
            {'source' : [{'outbound': ['PDB', 'ihm_cross_link_restraint_RCB_fkey']}, 'RID'], },
            {'source' : [{'outbound': ['PDB', 'ihm_cross_link_restraint_RMB_fkey']}, 'RID'], },
            {'source' : [{'outbound': ['PDB', 'ihm_cross_link_restraint_Owner_fkey']}, 'RID'], },
        ],
    })

    # ----------------------------
    schema.tables["ihm_cross_link_restraint"].visible_foreign_keys.update({
        'filter' :  'detailed',
        'detailed' :  [
            ['PDB', 'ihm_cross_link_pseudo_site_ihm_cross_link_restraint_combo1_fkey'], 
            ['PDB', 'ihm_cross_link_result_restraint_id_fkey'], 
            ['PDB', 'ihm_cross_link_result_parameters_restraint_id_fkey'], 
        ],
    })

    # ----------------------------
    schema.tables["ihm_cross_link_restraint"].foreign_keys[(schema,"ihm_cross_link_restraint_asym_id_2_fkey")].foreign_key.update({
        'template_engine' :  'handlebars',
        'domain_filter_pattern' :  '{{#if _structure_id}}structure_id={{{_structure_id}}}{{/if}}',
    })

    # ----------------------------
    schema.tables["ihm_cross_link_restraint"].foreign_keys[(schema,"ihm_cross_link_restraint_mm_poly_res_label_1_fkey")].foreign_key.update({
        'from_name' :  'Ihm Cross Link Restraint Label 1',
        'template_engine' :  'handlebars',
        'domain_filter_pattern' :  '{{#if _structure_id}}structure_id={{{_structure_id}}}{{/if}}',
    })

    # ----------------------------
    schema.tables["ihm_cross_link_restraint"].foreign_keys[(schema,"ihm_cross_link_restraint_mm_poly_res_label_2_fkey")].foreign_key.update({
        'from_name' :  'Ihm Cross Link Restraint Label 2',
        'template_engine' :  'handlebars',
        'domain_filter_pattern' :  '{{#if _structure_id}}structure_id={{{_structure_id}}}{{/if}}',
    })

    # ----------------------------
    schema.tables["ihm_cross_link_restraint"].foreign_keys[(schema,"ihm_cross_link_restraint_group_id_fkey")].foreign_key.update({
        'template_engine' :  'handlebars',
        'domain_filter_pattern' :  '{{#if _structure_id}}structure_id={{{_structure_id}}}{{/if}}',
    })

    # ----------------------------
    schema.tables["ihm_cross_link_restraint"].foreign_keys[(schema,"ihm_cross_link_restraint_asym_id_1_fkey")].foreign_key.update({
        'template_engine' :  'handlebars',
        'domain_filter_pattern' :  '{{#if _structure_id}}structure_id={{{_structure_id}}}{{/if}}',
    })

# -- -----------------------------------------------------------------------------
def update_PDB_ihm_cross_link_result(model):
    schema = model.schemas["PDB"]
    table = schema.tables["ihm_cross_link_result"]
    # ----------------------------
    schema.tables["ihm_cross_link_result"].display.update(
        {'name' : 'Chemical Crosslink Restraint Results', 'comment_display' : {'*': {'table_comment_display': 'inline'}}, }
    )

    table.source_definitions.update({
        'fkeys' :  [],
        'columns' :  True,
        'sources' : {
            'structure_id_fkey': {
                'source' : [{'outbound': ['PDB', 'ihm_cross_link_result_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'restraint_combo1_fkey': {
                'source' : [{'outbound': ['PDB', 'ihm_cross_link_result_cross_link_restraint_combo1_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_cross_link_restraint.id.',
                'markdown_name' : 'Restraint Id',
            },
            'model_group_combo2_fkey': { 
                "comment": "An identifier for the group of structure models whose results are described",
                "markdown_name": "Model Group Id",
                'source' : [{'outbound': ['PDB', 'ihm_cross_link_result_model_group_combo2_fkey']}, 'RID'],
            },
            'ensemble_info_combo2_fkey': { 
                "comment": "A reference to table ihm_ensemble_info.ensemble_id.",
                "markdown_name": "Ensemble Id",
                'source' : [{'outbound': ['PDB', 'ihm_cross_link_result_ensemble_info_combo2_fkey']}, 'RID'],
            },
            'upload_restraint_file_fkey': {
                'source' : [{'outbound': ['PDB', 'ihm_cross_link_result_Entry_Related_File_fkey']}, 'RID'],
                'comment' : 'A reference to the uploaded restraint file in the table Entry_Related_File.id.',
                'markdown_name' : 'Uploaded Restraint File',
            },
        },
    })
    
    # ----------------------------
    schema.tables["ihm_cross_link_result"].visible_columns.update({
        '*' :  [
            'RID',
            { "sourcekey": 'structure_id_fkey' },
            'id',
            { "sourcekey": 'restraint_combo1_fkey' },
            { "sourcekey": 'model_group_combo2_fkey' },
            { "sourcekey": 'ensemble_info_combo2_fkey' },                                    
            'num_models', 
            'distance_threshold', 
            'median_distance', 
            'details',
            { "sourcekey": 'upload_restraint_file_fkey' },                                                
        ],
        'entry' :  [
            { "sourcekey": 'structure_id_fkey' },
            'id',
            { "sourcekey": 'restraint_combo1_fkey' },
            { "sourcekey": 'model_group_combo2_fkey' },
            { "sourcekey": 'ensemble_info_combo2_fkey' },
            'num_models', 
            'distance_threshold', 
            'median_distance', 
            'details',
        ],
        'detailed' :  [
            'RID',
            { "sourcekey": 'structure_id_fkey' },
            'id',
            { "sourcekey": 'restraint_combo1_fkey' },
            { "sourcekey": 'model_group_combo2_fkey' },
            { "sourcekey": 'ensemble_info_combo2_fkey' },
            'num_models', 
            'distance_threshold', 
            'median_distance', 
            'details',
            { "sourcekey": 'upload_restraint_file_fkey' },                                                
            ['PDB', 'ihm_cross_link_result_RCB_fkey'], 
            ['PDB', 'ihm_cross_link_result_RMB_fkey'], 
            'RCT', 
            'RMT', 
        ],
    })

    # ----------------------------
    schema.tables["ihm_cross_link_result"].columns["num_models"].display.update(
        {'name' : 'Number of Models', }
    )

    # ----------------------------
    schema.tables["ihm_cross_link_result"].foreign_keys[(schema,"ihm_cross_link_result_cross_link_restraint_combo1_fkey")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })

    # ----------------------------
    if (schema,"ihm_cross_link_result_ensemble_info_combo2_fkey") in table.foreign_keys.elements:
        table.foreign_keys[(schema,"ihm_cross_link_result_ensemble_info_combo2_fkey")].foreign_key.update({
            'domain_filter_pattern' :  'structure_id={{structure_id}}',
        })
        
    if (schema,"ihm_cross_link_result_model_group_combo2_fkey") in table.foreign_keys.elements:
        table.foreign_keys[(schema,"ihm_cross_link_result_model_group_combo2_fkey")].foreign_key.update({
            'domain_filter_pattern' :  'structure_id={{structure_id}}',
        })
    

# -- -----------------------------------------------------------------------------
def update_PDB_ihm_cross_link_result_parameters(model):
    schema = model.schemas["PDB"]
    table = schema.tables["ihm_cross_link_result_parameters"]
    # ----------------------------
    schema.tables["ihm_cross_link_result_parameters"].display.update({
        'name' : 'Chemical Crosslink Restraint Result Parameters',
        'comment_display' : {'*': {'table_comment_display': 'inline'}},
    })

    # ----------------------------
    schema.tables["ihm_cross_link_result_parameters"].visible_columns.update({
        '*' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_cross_link_result_parameters_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'id', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_cross_link_result_parameters_restraint_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_cross_link_restraint.id.',
                'markdown_name' : 'Restraint Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_cross_link_result_parameters_model_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_model_list.model_id.',
                'markdown_name' : 'Model Id',
            },
            'psi', 
            'sigma_1', 
            'sigma_2', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_cross_link_result_parameters_Entry_Related_File_fkey']}, 'RID'],
                'comment' : 'A reference to the uploaded restraint file in the table Entry_Related_File.id.',
                'markdown_name' : 'Uploaded Restraint File',
            },
        ],
        'entry' :  [
            {
                'source' : [{'outbound': ['PDB', 'ihm_cross_link_result_parameters_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'id', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_cross_link_result_parameters_restraint_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_cross_link_restraint.id.',
                'markdown_name' : 'Restraint Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_cross_link_result_parameters_model_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_model_list.model_id.',
                'markdown_name' : 'Model Id',
            },
            'psi', 
            'sigma_1', 
            'sigma_2', 
        ],
        'detailed' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_cross_link_result_parameters_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'id', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_cross_link_result_parameters_restraint_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_cross_link_restraint.id.',
                'markdown_name' : 'Restraint Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_cross_link_result_parameters_model_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_model_list.model_id.',
                'markdown_name' : 'Model Id',
            },
            'psi', 
            'sigma_1', 
            'sigma_2', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_cross_link_result_parameters_Entry_Related_File_fkey']}, 'RID'],
                'comment' : 'A reference to the uploaded restraint file in the table Entry_Related_File.id.',
                'markdown_name' : 'Uploaded Restraint File',
            },
            ['PDB', 'ihm_cross_link_result_parameters_RCB_fkey'], 
            ['PDB', 'ihm_cross_link_result_parameters_RMB_fkey'], 
            'RCT', 
            'RMT', 
            ['PDB', 'ihm_cross_link_result_parameters_Owner_fkey'], 
        ],
    })

    # ----------------------------
    schema.tables["ihm_cross_link_result_parameters"].foreign_keys[(schema,"ihm_cross_link_result_parameters_model_id_fkey")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })

    # ----------------------------
    schema.tables["ihm_cross_link_result_parameters"].foreign_keys[(schema,"ihm_cross_link_result_parameters_restraint_id_fkey")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })

# -- -----------------------------------------------------------------------------
def update_PDB_ihm_data_transformation(model):
    schema = model.schemas["PDB"]
    table = schema.tables["ihm_data_transformation"]
    # ----------------------------
    schema.tables["ihm_data_transformation"].display.update({
        'name' : 'Data Transformation',
        'comment_display' : {'*': {'table_comment_display': 'inline'}},
    })

    # ----------------------------
    schema.tables["ihm_data_transformation"].visible_columns.update({
        '*' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_data_transformation_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'id', 
            'rot_matrix[1][1]', 
            'rot_matrix[1][2]', 
            'rot_matrix[1][3]', 
            'rot_matrix[2][1]', 
            'rot_matrix[2][2]', 
            'rot_matrix[2][3]', 
            'rot_matrix[3][1]', 
            'rot_matrix[3][2]', 
            'rot_matrix[3][3]', 
            'tr_vector[1]', 
            'tr_vector[2]', 
            'tr_vector[3]', 
        ],
        'entry' :  [
            {
                'source' : [{'outbound': ['PDB', 'ihm_data_transformation_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'id', 
            'rot_matrix[1][1]', 
            'rot_matrix[1][2]', 
            'rot_matrix[1][3]', 
            'rot_matrix[2][1]', 
            'rot_matrix[2][2]', 
            'rot_matrix[2][3]', 
            'rot_matrix[3][1]', 
            'rot_matrix[3][2]', 
            'rot_matrix[3][3]', 
            'tr_vector[1]', 
            'tr_vector[2]', 
            'tr_vector[3]', 
        ],
        'detailed' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_data_transformation_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'id', 
            'rot_matrix[1][1]', 
            'rot_matrix[1][2]', 
            'rot_matrix[1][3]', 
            'rot_matrix[2][1]', 
            'rot_matrix[2][2]', 
            'rot_matrix[2][3]', 
            'rot_matrix[3][1]', 
            'rot_matrix[3][2]', 
            'rot_matrix[3][3]', 
            'tr_vector[1]', 
            'tr_vector[2]', 
            'tr_vector[3]', 
            ['PDB', 'ihm_data_transformation_RCB_fkey'], 
            ['PDB', 'ihm_data_transformation_RMB_fkey'], 
            'RCT', 
            'RMT', 
            ['PDB', 'ihm_data_transformation_Owner_fkey'], 
        ],
    })

    # ----------------------------
    schema.tables["ihm_data_transformation"].visible_foreign_keys.update( {
        'filter' :  'detailed',
        'detailed' :  [
            ['PDB', 'ihm_related_datasets_ihm_data_transformation_combo2_fkey'], 
        ],
    })

# -- -----------------------------------------------------------------------------
def update_PDB_ihm_dataset_external_reference(model):
    schema = model.schemas["PDB"]
    table = schema.tables["ihm_dataset_external_reference"]
    # ----------------------------
    schema.tables["ihm_dataset_external_reference"].display.update(
        {'name' : 'External Files Corresponding to Input Datasets', 'comment_display' : {'*': {'table_comment_display': 'inline'}}, }
    )
    
    # ----------------------------
    schema.tables["ihm_dataset_external_reference"].visible_columns.update( {
        '*' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_dataset_external_reference_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'id', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_dataset_external_reference_dataset_list_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_dataset_list.id.',
                'markdown_name' : 'Dataset List Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_dataset_external_reference_file_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_external_files.id.',
                'markdown_name' : 'File Id',
            },
        ],
        'entry' :  [
            {
                'source' : [{'outbound': ['PDB', 'ihm_dataset_external_reference_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'id', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_dataset_external_reference_dataset_list_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_dataset_list.id.',
                'markdown_name' : 'Dataset List Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_dataset_external_reference_file_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_external_files.id.',
                'markdown_name' : 'File Id',
            },
        ],
        'detailed' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_dataset_external_reference_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'id', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_dataset_external_reference_dataset_list_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_dataset_list.id.',
                'markdown_name' : 'Dataset List Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_dataset_external_reference_file_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_external_files.id.',
                'markdown_name' : 'File Id',
            },
            ['PDB', 'ihm_dataset_external_reference_RCB_fkey'], 
            ['PDB', 'ihm_dataset_external_reference_RMB_fkey'], 
            'RCT', 
            'RMT', 
            ['PDB', 'ihm_dataset_external_reference_Owner_fkey'], 
        ],
    })
    
    # ----------------------------
    schema.tables["ihm_dataset_external_reference"].columns["dataset_list_id"].display.update(
        {'name' : 'Dataset List Id', }
    )

    # ----------------------------
    schema.tables["ihm_dataset_external_reference"].columns["file_id"].display.update(
        {'name' : 'File Id', }
    )

    # ----------------------------
    schema.tables["ihm_dataset_external_reference"].foreign_keys[(schema,"ihm_dataset_external_reference_file_id_fkey")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })

    # ----------------------------
    schema.tables["ihm_dataset_external_reference"].foreign_keys[(schema,"ihm_dataset_external_reference_dataset_list_id_fkey")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })

# -- -----------------------------------------------------------------------------
def update_PDB_ihm_dataset_group(model):
    schema = model.schemas["PDB"]
    table = schema.tables["ihm_dataset_group"]
    # ----------------------------
    schema.tables["ihm_dataset_group"].display.update(
        {'markdown_name' : 'Input Dataset Groups^*^', 'comment_display' : {'*': {'table_comment_display': 'inline'}}, }
    )

    # ----------------------------
    schema.tables["ihm_dataset_group"].table_display.update({
        'row_name' : { 'row_markdown_pattern' : '{{{id}}}', },
    })

    # ----------------------------
    schema.tables["ihm_dataset_group"].visible_columns.update({
        '*' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_dataset_group_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'id', 
            'name', 
            ['PDB', 'ihm_dataset_group_application_fkey'], 
            'details', 
        ],
        'entry' :  [
            {
                'source' : [{'outbound': ['PDB', 'ihm_dataset_group_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'id', 
            'name', 
            ['PDB', 'ihm_dataset_group_application_fkey'], 
            'details', 
        ],
        'detailed' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_dataset_group_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'id', 
            'name', 
            ['PDB', 'ihm_dataset_group_application_fkey'], 
            'details', 
            ['PDB', 'ihm_dataset_group_RCB_fkey'], 
            ['PDB', 'ihm_dataset_group_RMB_fkey'], 
            'RCT', 
            'RMT', 
            ['PDB', 'ihm_dataset_group_Owner_fkey'], 
        ],
    })

    # ----------------------------
    schema.tables["ihm_dataset_group"].visible_foreign_keys.update({
        'filter' :  'detailed',
        'detailed' :  [
            ['PDB', 'ihm_dataset_group_link_group_id_fkey'], 
            ['PDB', 'ihm_modeling_protocol_details_dataset_group_id_fkey'], 
            ['PDB', 'ihm_modeling_post_process_dataset_group_id_fkey'], 
            ['PDB', 'multi_state_scheme_connectivity_dataset_group_combo1_fkey'], 
            ['PDB', 'ihm_kinetic_rate_ihm_dataset_group_combo1_fkey'], 
            ['PDB', 'ihm_relaxation_time_ihm_dataset_group_combo1_fkey'], 
        ],
    })


# -- -----------------------------------------------------------------------------
def update_PDB_ihm_dataset_group_link(model):
    schema = model.schemas["PDB"]
    table = schema.tables["ihm_dataset_group_link"]
    # ----------------------------
    schema.tables["ihm_dataset_group_link"].display.update(
        {'markdown_name' : 'Datasets Belonging to Groups^*^', 'comment_display' : {'*': {'table_comment_display': 'inline'}}, }
    )
    
    # ----------------------------
    schema.tables["ihm_dataset_group_link"].visible_columns.update({
        '*' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_dataset_group_link_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_dataset_group_link_dataset_list_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_dataset_list.id.',
                'markdown_name' : 'Dataset List Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_dataset_group_link_group_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_dataset_group.id.',
                'markdown_name' : 'Dataset Group Id',
            },
        ],
        'entry' :  [
            {
                'source' : [{'outbound': ['PDB', 'ihm_dataset_group_link_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_dataset_group_link_dataset_list_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_dataset_list.id.',
                'markdown_name' : 'Dataset List Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_dataset_group_link_group_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_dataset_group.id.',
                'markdown_name' : 'Dataset Group Id',
            },
        ],
        'detailed' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_dataset_group_link_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_dataset_group_link_dataset_list_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_dataset_list.id.',
                'markdown_name' : 'Dataset List Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_dataset_group_link_group_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_dataset_group.id.',
                'markdown_name' : 'Dataset Group Id',
            },
            ['PDB', 'ihm_dataset_group_link_RCB_fkey'], 
            ['PDB', 'ihm_dataset_group_link_RMB_fkey'], 
            'RCT', 
            'RMT', 
            ['PDB', 'ihm_dataset_group_link_Owner_fkey'], 
        ],
    })

    # ----------------------------
    schema.tables["ihm_dataset_group_link"].columns["dataset_list_id"].display.update(
        {'name' : 'Dataset List Id', }
    )

    # ----------------------------
    schema.tables["ihm_dataset_group_link"].foreign_keys[(schema,"ihm_dataset_group_link_dataset_list_id_fkey")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })
    
    # ----------------------------
    schema.tables["ihm_dataset_group_link"].foreign_keys[(schema,"ihm_dataset_group_link_group_id_fkey")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })


# -- -----------------------------------------------------------------------------
def update_PDB_ihm_dataset_list(model):
    schema = model.schemas["PDB"]
    table = schema.tables["ihm_dataset_list"]
    # ----------------------------
    schema.tables["ihm_dataset_list"].display.update(
        {'markdown_name' : 'Input Datasets^*^', 'comment_display' : {'*': {'table_comment_display': 'inline'}}, }
    )

    # ----------------------------
    schema.tables["ihm_dataset_list"].table_display.update({
        'row_name' : { 'row_markdown_pattern' : '{{{id}}}', },
    })

    # ----------------------------
    schema.tables["ihm_dataset_list"].visible_columns.update({
        '*' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_dataset_list_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'id', 
            ['PDB', 'ihm_dataset_list_data_type_fkey'], 
            ['PDB', 'ihm_dataset_list_database_hosted_fkey'], 
            'details', 
        ],
        'entry' :  [
            {
                'source' : [{'outbound': ['PDB', 'ihm_dataset_list_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'id', 
            ['PDB', 'ihm_dataset_list_data_type_fkey'], 
            ['PDB', 'ihm_dataset_list_database_hosted_fkey'], 
            'details', 
        ],
        'detailed' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_dataset_list_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'id', 
            ['PDB', 'ihm_dataset_list_data_type_fkey'], 
            ['PDB', 'ihm_dataset_list_database_hosted_fkey'], 
            'details', 
            ['PDB', 'ihm_dataset_list_RCB_fkey'], 
            ['PDB', 'ihm_dataset_list_RMB_fkey'], 
            'RCT', 
            'RMT', 
            ['PDB', 'ihm_dataset_list_Owner_fkey'], 
        ],
    })

    # ----------------------------
    schema.tables["ihm_dataset_list"].visible_foreign_keys.update({
        'filter' :  'detailed',
        'detailed' :  [
            ['PDB', 'ihm_dataset_group_link_dataset_list_id_fkey'], 
            ['PDB', 'ihm_dataset_related_db_reference_dataset_list_id_fkey'], 
            ['PDB', 'ihm_dataset_external_reference_dataset_list_id_fkey'], 
            ['PDB', 'ihm_related_datasets_dataset_list_id_derived_fkey'], 
            ['PDB', 'ihm_related_datasets_dataset_list_id_primary_fkey'], 
            ['PDB', 'ihm_starting_model_details_dataset_list_id_fkey'], 
            ['PDB', 'ihm_starting_comparative_models_template_dataset_list_id_fkey'], 
            ['PDB', 'ihm_poly_probe_conjugate_dataset_list_id_fkey'], 
            ['PDB', 'ihm_ligand_probe_dataset_list_id_fkey'], 
            ['PDB', 'ihm_cross_link_list_dataset_list_id_fkey'], 
            ['PDB', 'ihm_2dem_class_average_restraint_dataset_list_id_fkey'], 
            ['PDB', 'ihm_3dem_restraint_dataset_list_id_fkey'], 
            ['PDB', 'ihm_sas_restraint_dataset_list_id_fkey'], 
            ['PDB', 'ihm_epr_restraint_dataset_list_id_fkey'], 
            ['PDB', 'ihm_hdx_restraint_ihm_dataset_list_combo1_fkey'], 
            ['PDB', 'ihm_hydroxyl_radical_fp_restraint_dataset_list_id_fkey'], 
            ['PDB', 'ihm_predicted_contact_restraint_dataset_list_id_fkey'], 
            ['PDB', 'ihm_interface_residue_feature_dataset_list_id_fkey'], 
            ['PDB', 'ihm_derived_distance_restraint_dataset_list_id_fkey'], 
            ['PDB', 'ihm_derived_angle_restraint_ihm_dataset_list_combo1_fkey'], 
            ['PDB', 'ihm_derived_dihedral_restraint_ihm_dataset_list_combo1_fkey'], 
            ['PDB', 'ihm_geometric_object_distance_restraint_dataset_list_id_fkey'], 
        ],
    })


# -- -----------------------------------------------------------------------------
def update_PDB_ihm_dataset_related_db_reference(model):
    schema = model.schemas["PDB"]
    table = schema.tables["ihm_dataset_related_db_reference"]
    # ----------------------------
    schema.tables["ihm_dataset_related_db_reference"].display.update(
        {'name' : 'Datasets Archived in Other Repositories', 'comment_display' : {'*': {'table_comment_display': 'inline'}}, }
    )

    # ----------------------------
    schema.tables["ihm_dataset_related_db_reference"].visible_columns.update({
        '*' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_dataset_related_db_reference_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'id', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_dataset_related_db_reference_dataset_list_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_dataset_list.id.',
                'markdown_name' : 'Dataset List Id',
            },
            ['PDB', 'ihm_dataset_related_db_reference_db_name_fkey'], 
            'accession_code', 
            'version', 
            'details', 
        ],
        'entry' :  [
            {
                'source' : [{'outbound': ['PDB', 'ihm_dataset_related_db_reference_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'id', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_dataset_related_db_reference_dataset_list_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_dataset_list.id.',
                'markdown_name' : 'Dataset List Id',
            },
            ['PDB', 'ihm_dataset_related_db_reference_db_name_fkey'], 
            'accession_code', 
            'version', 
            'details', 
        ],
        'detailed' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_dataset_related_db_reference_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'id', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_dataset_related_db_reference_dataset_list_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_dataset_list.id.',
                'markdown_name' : 'Dataset List Id',
            },
            ['PDB', 'ihm_dataset_related_db_reference_db_name_fkey'], 
            'accession_code', 
            'version', 
            'details', 
            ['PDB', 'ihm_dataset_related_db_reference_RCB_fkey'], 
            ['PDB', 'ihm_dataset_related_db_reference_RMB_fkey'], 
            'RCT', 
            'RMT', 
            ['PDB', 'ihm_dataset_related_db_reference_Owner_fkey'], 
        ],
    })

    # ----------------------------
    schema.tables["ihm_dataset_related_db_reference"].columns["dataset_list_id"].display.update(
        {'name' : 'Dataset List Id', }
    )

    # ----------------------------
    schema.tables["ihm_dataset_related_db_reference"].columns["db_name"].display.update(
        {'name' : 'Database Name', }
    )

    # ----------------------------
    schema.tables["ihm_dataset_related_db_reference"].foreign_keys[(schema,"ihm_dataset_related_db_reference_dataset_list_id_fkey")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })


# -- -----------------------------------------------------------------------------
def update_PDB_ihm_derived_angle_restraint(model):
    schema = model.schemas["PDB"]
    table = schema.tables["ihm_derived_angle_restraint"]
    # ----------------------------
    schema.tables["ihm_derived_angle_restraint"].display.update(
        {'name' : 'Angle Restraints Between Molecular Features', 'comment_display' : {'*': {'table_comment_display': 'inline'}}, }
    )

    # ----------------------------
    schema.tables["ihm_derived_angle_restraint"].visible_columns.update({
        '*' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_derived_angle_restraint_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'id', 
            'group_id', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_derived_angle_restraint_ihm_feature_list_1_combo1_fkey']}, 'RID'],
                'comment' : 'The feature identifier for the first partner in the angle restraint',
                'markdown_name' : 'Feature Id 1',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_derived_angle_restraint_ihm_feature_list_2_combo1_fkey']}, 'RID'],
                'comment' : 'The feature identifier for the second partner in the angle restraint',
                'markdown_name' : 'Feature Id 2',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_derived_angle_restraint_ihm_feature_list_3_combo1_fkey']}, 'RID'],
                'comment' : 'The feature identifier for the third partner in the angle restraint',
                'markdown_name' : 'Feature Id 3',
            },
            ['PDB', 'ihm_derived_angle_restraint_group_conditionality_fkey'], 
            'angle_lower_limit', 
            'angle_upper_limit', 
            'angle_lower_limit_esd', 
            'angle_upper_limit_esd', 
            'probability', 
            ['PDB', 'ihm_derived_angle_restraint_restraint_type_fkey'], 
            'angle_threshold_mean', 
            'angle_threshold_mean_esd', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_derived_angle_restraint_ihm_dataset_list_combo1_fkey']}, 'RID'],
                'comment' : 'Identifier to the input data from which the angle restraint is derived',
                'markdown_name' : 'Dataset List Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_derived_angle_restraint_Entry_Related_File_fkey']}, 'RID'],
                'comment' : 'A reference to the uploaded restraint file in the table Entry_Related_File.id.',
                'markdown_name' : 'Uploaded Restraint File',
            },
        ],
        'entry' :  [
            {
                'source' : [{'outbound': ['PDB', 'ihm_derived_angle_restraint_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'id', 
            'group_id', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_derived_angle_restraint_ihm_feature_list_1_combo1_fkey']}, 'RID'],
                'comment' : 'The feature identifier for the first partner in the angle restraint',
                'markdown_name' : 'Feature Id 1',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_derived_angle_restraint_ihm_feature_list_2_combo1_fkey']}, 'RID'],
                'comment' : 'The feature identifier for the second partner in the angle restraint',
                'markdown_name' : 'Feature Id 2',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_derived_angle_restraint_ihm_feature_list_3_combo1_fkey']}, 'RID'],
                'comment' : 'The feature identifier for the third partner in the angle restraint',
                'markdown_name' : 'Feature Id 3',
            },
            ['PDB', 'ihm_derived_angle_restraint_group_conditionality_fkey'], 
            'angle_lower_limit', 
            'angle_upper_limit', 
            'angle_lower_limit_esd', 
            'angle_upper_limit_esd', 
            'probability', 
            ['PDB', 'ihm_derived_angle_restraint_restraint_type_fkey'], 
            'angle_threshold_mean', 
            'angle_threshold_mean_esd', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_derived_angle_restraint_ihm_dataset_list_combo1_fkey']}, 'RID'],
                'comment' : 'Identifier to the input data from which the angle restraint is derived',
                'markdown_name' : 'Dataset List Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_derived_angle_restraint_Entry_Related_File_fkey']}, 'RID'],
                'comment' : 'A reference to the uploaded restraint file in the table Entry_Related_File.id.',
                'markdown_name' : 'Uploaded Restraint File',
            },
        ],
        'detailed' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_derived_angle_restraint_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'id', 
            'group_id', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_derived_angle_restraint_ihm_feature_list_1_combo1_fkey']}, 'RID'],
                'comment' : 'The feature identifier for the first partner in the angle restraint',
                'markdown_name' : 'Feature Id 1',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_derived_angle_restraint_ihm_feature_list_2_combo1_fkey']}, 'RID'],
                'comment' : 'The feature identifier for the second partner in the angle restraint',
                'markdown_name' : 'Feature Id 2',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_derived_angle_restraint_ihm_feature_list_3_combo1_fkey']}, 'RID'],
                'comment' : 'The feature identifier for the third partner in the angle restraint',
                'markdown_name' : 'Feature Id 3',
            },
            ['PDB', 'ihm_derived_angle_restraint_group_conditionality_fkey'], 
            'angle_lower_limit', 
            'angle_upper_limit', 
            'angle_lower_limit_esd', 
            'angle_upper_limit_esd', 
            'probability', 
            ['PDB', 'ihm_derived_angle_restraint_restraint_type_fkey'], 
            'angle_threshold_mean', 
            'angle_threshold_mean_esd', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_derived_angle_restraint_ihm_dataset_list_combo1_fkey']}, 'RID'],
                'comment' : 'Identifier to the input data from which the angle restraint is derived',
                'markdown_name' : 'Dataset List Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_derived_angle_restraint_Entry_Related_File_fkey']}, 'RID'],
                'comment' : 'A reference to the uploaded restraint file in the table Entry_Related_File.id.',
                'markdown_name' : 'Uploaded Restraint File',
            },
            ['PDB', 'ihm_derived_angle_restraint_RCB_fkey'], 
            ['PDB', 'ihm_derived_angle_restraint_RMB_fkey'], 
            'RCT', 
            'RMT', 
            ['PDB', 'ihm_derived_angle_restraint_Owner_fkey'], 
        ],
    })

    # ----------------------------
    schema.tables["ihm_derived_angle_restraint"].foreign_keys[(schema,"ihm_derived_angle_restraint_ihm_feature_list_3_combo1_fkey")].foreign_key.update({
        'from_name' :  'Ihm Angle Restraint Feature 3',
        'template_engine' :  'handlebars',
        'domain_filter_pattern' :  '{{#if _structure_id}}structure_id={{{_structure_id}}}{{/if}}',
    })

    # ----------------------------
    schema.tables["ihm_derived_angle_restraint"].foreign_keys[(schema,"ihm_derived_angle_restraint_ihm_dataset_list_combo1_fkey")].foreign_key.update({
        'template_engine' :  'handlebars',
        'domain_filter_pattern' :  '{{#if _structure_id}}structure_id={{{_structure_id}}}{{/if}}',
    })

    # ----------------------------
    schema.tables["ihm_derived_angle_restraint"].foreign_keys[(schema,"ihm_derived_angle_restraint_ihm_feature_list_2_combo1_fkey")].foreign_key.update({
        'from_name' :  'Ihm Angle Restraint Feature 2',
        'template_engine' :  'handlebars',
        'domain_filter_pattern' :  '{{#if _structure_id}}structure_id={{{_structure_id}}}{{/if}}',
    })

    # ----------------------------
    schema.tables["ihm_derived_angle_restraint"].foreign_keys[(schema,"ihm_derived_angle_restraint_ihm_feature_list_1_combo1_fkey")].foreign_key.update({
        'from_name' :  'Ihm Angle Restraint Feature 1',
        'template_engine' :  'handlebars',
        'domain_filter_pattern' :  '{{#if _structure_id}}structure_id={{{_structure_id}}}{{/if}}',
    })


# -- -----------------------------------------------------------------------------
def update_PDB_ihm_derived_dihedral_restraint(model):
    schema = model.schemas["PDB"]
    table = schema.tables["ihm_derived_dihedral_restraint"]
    # ----------------------------
    schema.tables["ihm_derived_dihedral_restraint"].display.update(
        {'name' : 'Dihedral Restraints Between Molecular Features', 'comment_display' : {'*': {'table_comment_display': 'inline'}}, }
    )

    # ----------------------------
    schema.tables["ihm_derived_dihedral_restraint"].visible_columns.update({
        '*' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_derived_dihedral_restraint_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'id', 
            'group_id', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_derived_dihedral_restraint_ihm_feature_list_1_combo1_fkey']}, 'RID'],
                'comment' : 'The feature identifier for the first partner in the dihedral restraint',
                'markdown_name' : 'Feature Id 1',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_derived_dihedral_restraint_ihm_feature_list_2_combo1_fkey']}, 'RID'],
                'comment' : 'The feature identifier for the second partner in the dihedral restraint',
                'markdown_name' : 'Feature Id 2',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_derived_dihedral_restraint_ihm_feature_list_3_combo1_fkey']}, 'RID'],
                'comment' : 'The feature identifier for the third partner in the dihedral restraint',
                'markdown_name' : 'Feature Id 3',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_derived_dihedral_restraint_ihm_feature_list_4_combo1_fkey']}, 'RID'],
                'comment' : 'The feature identifier for the fourth partner in the dihedral restraint',
                'markdown_name' : 'Feature Id 4',
            },
            ['PDB', 'ihm_derived_dihedral_restraint_group_conditionality_fkey'], 
            'dihedral_lower_limit', 
            'dihedral_upper_limit', 
            'dihedral_lower_limit_esd', 
            'dihedral_upper_limit_esd', 
            'probability', 
            ['PDB', 'ihm_derived_dihedral_restraint_restraint_type_fkey'], 
            'dihedral_threshold_mean', 
            'dihedral_threshold_mean_esd', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_derived_dihedral_restraint_ihm_dataset_list_combo1_fkey']}, 'RID'],
                'comment' : 'Identifier to the input data from which the dihedral restraint is derived',
                'markdown_name' : 'Dataset List Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_derived_dihedral_restraint_Entry_Related_File_fkey']}, 'RID'],
                'comment' : 'A reference to the uploaded restraint file in the table Entry_Related_File.id.',
                'markdown_name' : 'Uploaded Restraint File',
            },
        ],
        'entry' :  [
            {
                'source' : [{'outbound': ['PDB', 'ihm_derived_dihedral_restraint_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'id', 
            'group_id', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_derived_dihedral_restraint_ihm_feature_list_1_combo1_fkey']}, 'RID'],
                'comment' : 'The feature identifier for the first partner in the dihedral restraint',
                'markdown_name' : 'Feature Id 1',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_derived_dihedral_restraint_ihm_feature_list_2_combo1_fkey']}, 'RID'],
                'comment' : 'The feature identifier for the second partner in the dihedral restraint',
                'markdown_name' : 'Feature Id 2',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_derived_dihedral_restraint_ihm_feature_list_3_combo1_fkey']}, 'RID'],
                'comment' : 'The feature identifier for the third partner in the dihedral restraint',
                'markdown_name' : 'Feature Id 3',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_derived_dihedral_restraint_ihm_feature_list_4_combo1_fkey']}, 'RID'],
                'comment' : 'The feature identifier for the fourth partner in the dihedral restraint',
                'markdown_name' : 'Feature Id 4',
            },
            ['PDB', 'ihm_derived_dihedral_restraint_group_conditionality_fkey'], 
            'dihedral_lower_limit', 
            'dihedral_upper_limit', 
            'dihedral_lower_limit_esd', 
            'dihedral_upper_limit_esd', 
            'probability', 
            ['PDB', 'ihm_derived_dihedral_restraint_restraint_type_fkey'], 
            'dihedral_threshold_mean', 
            'dihedral_threshold_mean_esd', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_derived_dihedral_restraint_ihm_dataset_list_combo1_fkey']}, 'RID'],
                'comment' : 'Identifier to the input data from which the dihedral restraint is derived',
                'markdown_name' : 'Dataset List Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_derived_dihedral_restraint_Entry_Related_File_fkey']}, 'RID'],
                'comment' : 'A reference to the uploaded restraint file in the table Entry_Related_File.id.',
                'markdown_name' : 'Uploaded Restraint File',
            },
        ],
        'detailed' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_derived_dihedral_restraint_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'id', 
            'group_id', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_derived_dihedral_restraint_ihm_feature_list_1_combo1_fkey']}, 'RID'],
                'comment' : 'The feature identifier for the first partner in the dihedral restraint',
                'markdown_name' : 'Feature Id 1',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_derived_dihedral_restraint_ihm_feature_list_2_combo1_fkey']}, 'RID'],
                'comment' : 'The feature identifier for the second partner in the dihedral restraint',
                'markdown_name' : 'Feature Id 2',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_derived_dihedral_restraint_ihm_feature_list_3_combo1_fkey']}, 'RID'],
                'comment' : 'The feature identifier for the third partner in the dihedral restraint',
                'markdown_name' : 'Feature Id 3',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_derived_dihedral_restraint_ihm_feature_list_4_combo1_fkey']}, 'RID'],
                'comment' : 'The feature identifier for the fourth partner in the dihedral restraint',
                'markdown_name' : 'Feature Id 4',
            },
            ['PDB', 'ihm_derived_dihedral_restraint_group_conditionality_fkey'], 
            'dihedral_lower_limit', 
            'dihedral_upper_limit', 
            'dihedral_lower_limit_esd', 
            'dihedral_upper_limit_esd', 
            'probability', 
            ['PDB', 'ihm_derived_dihedral_restraint_restraint_type_fkey'], 
            'dihedral_threshold_mean', 
            'dihedral_threshold_mean_esd', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_derived_dihedral_restraint_ihm_dataset_list_combo1_fkey']}, 'RID'],
                'comment' : 'Identifier to the input data from which the dihedral restraint is derived',
                'markdown_name' : 'Dataset List Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_derived_dihedral_restraint_Entry_Related_File_fkey']}, 'RID'],
                'comment' : 'A reference to the uploaded restraint file in the table Entry_Related_File.id.',
                'markdown_name' : 'Uploaded Restraint File',
            },
            ['PDB', 'ihm_derived_dihedral_restraint_RCB_fkey'], 
            ['PDB', 'ihm_derived_dihedral_restraint_RMB_fkey'], 
            'RCT', 
            'RMT', 
            ['PDB', 'ihm_derived_dihedral_restraint_Owner_fkey'], 
        ],
    })

    # ----------------------------
    schema.tables["ihm_derived_dihedral_restraint"].foreign_keys[(schema,"ihm_derived_dihedral_restraint_ihm_dataset_list_combo1_fkey")].foreign_key.update({
        'template_engine' :  'handlebars',
        'domain_filter_pattern' :  '{{#if _structure_id}}structure_id={{{_structure_id}}}{{/if}}',
    })

    # ----------------------------
    schema.tables["ihm_derived_dihedral_restraint"].foreign_keys[(schema,"ihm_derived_dihedral_restraint_ihm_feature_list_2_combo1_fkey")].foreign_key.update({
        'from_name' :  'Ihm Dihedral Restraint Feature 2',
        'template_engine' :  'handlebars',
        'domain_filter_pattern' :  '{{#if _structure_id}}structure_id={{{_structure_id}}}{{/if}}',
    })

    # ----------------------------
    schema.tables["ihm_derived_dihedral_restraint"].foreign_keys[(schema,"ihm_derived_dihedral_restraint_ihm_feature_list_4_combo1_fkey")].foreign_key.update({
        'from_name' :  'Ihm Dihedral Restraint Feature 4',
        'template_engine' :  'handlebars',
        'domain_filter_pattern' :  '{{#if _structure_id}}structure_id={{{_structure_id}}}{{/if}}',
    })

    # ----------------------------
    schema.tables["ihm_derived_dihedral_restraint"].foreign_keys[(schema,"ihm_derived_dihedral_restraint_ihm_feature_list_3_combo1_fkey")].foreign_key.update({
        'from_name' :  'Ihm Dihedral Restraint Feature 3',
        'template_engine' :  'handlebars',
        'domain_filter_pattern' :  '{{#if _structure_id}}structure_id={{{_structure_id}}}{{/if}}',
    })

    # ----------------------------
    schema.tables["ihm_derived_dihedral_restraint"].foreign_keys[(schema,"ihm_derived_dihedral_restraint_ihm_feature_list_1_combo1_fkey")].foreign_key.update({
        'from_name' :  'Ihm Dihedral Restraint Feature 1',
        'template_engine' :  'handlebars',
        'domain_filter_pattern' :  '{{#if _structure_id}}structure_id={{{_structure_id}}}{{/if}}',
    })


# -- -----------------------------------------------------------------------------
def update_PDB_ihm_derived_distance_restraint(model):
    schema = model.schemas["PDB"]
    table = schema.tables["ihm_derived_distance_restraint"]
    # ----------------------------
    schema.tables["ihm_derived_distance_restraint"].display.update(
        {'name' : 'Distance Restraints Between Molecular Features', 'comment_display' : {'*': {'table_comment_display': 'inline'}}, }
    )

    # ----------------------------
    schema.tables["ihm_derived_distance_restraint"].visible_columns.update({
        '*' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_derived_distance_restraint_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'id', 
            'group_id', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_derived_distance_restraint_feature_id_1_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_feature_list.feature_id.',
                'markdown_name' : 'Feature Id 1',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_derived_distance_restraint_feature_id_2_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_feature_list.feature_id.',
                'markdown_name' : 'Feature Id 2',
            },
            ['PDB', 'ihm_derived_distance_restraint_group_conditionality_fkey'], 
            ['PDB', 'ihm_derived_distance_restraint_restraint_type_fkey'], 
            'distance_lower_limit', 
            'distance_upper_limit', 
            'distance_lower_limit_esd', 
            'distance_upper_limit_esd', 
            'distance_threshold_mean', 
            'distance_threshold_esd', 
            'probability', 
            'random_exclusion_fraction', 
            'mic_value', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_derived_distance_restraint_dataset_list_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_dataset_list.id.',
                'markdown_name' : 'Dataset List Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_derived_distance_restraint_Entry_Related_File_fkey']}, 'RID'],
                'comment' : 'A reference to the uploaded restraint file in the table Entry_Related_File.id.',
                'markdown_name' : 'Uploaded Restraint File',
            },
        ],
        'entry' :  [
            {
                'source' : [{'outbound': ['PDB', 'ihm_derived_distance_restraint_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'id', 
            'group_id', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_derived_distance_restraint_feature_id_1_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_feature_list.feature_id.',
                'markdown_name' : 'Feature Id 1',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_derived_distance_restraint_feature_id_2_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_feature_list.feature_id.',
                'markdown_name' : 'Feature Id 2',
            },
            ['PDB', 'ihm_derived_distance_restraint_group_conditionality_fkey'], 
            ['PDB', 'ihm_derived_distance_restraint_restraint_type_fkey'], 
            'distance_lower_limit', 
            'distance_upper_limit', 
            'distance_lower_limit_esd', 
            'distance_upper_limit_esd', 
            'distance_threshold_mean', 
            'distance_threshold_esd', 
            'probability', 
            'random_exclusion_fraction', 
            'mic_value', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_derived_distance_restraint_dataset_list_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_dataset_list.id.',
                'markdown_name' : 'Dataset List Id',
            },
        ],
        'detailed' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_derived_distance_restraint_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'id', 
            'group_id', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_derived_distance_restraint_feature_id_1_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_feature_list.feature_id.',
                'markdown_name' : 'Feature Id 1',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_derived_distance_restraint_feature_id_2_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_feature_list.feature_id.',
                'markdown_name' : 'Feature Id 2',
            },
            ['PDB', 'ihm_derived_distance_restraint_group_conditionality_fkey'], 
            ['PDB', 'ihm_derived_distance_restraint_restraint_type_fkey'], 
            'distance_lower_limit', 
            'distance_upper_limit', 
            'distance_lower_limit_esd', 
            'distance_upper_limit_esd', 
            'distance_threshold_mean', 
            'distance_threshold_esd', 
            'probability', 
            'random_exclusion_fraction', 
            'mic_value', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_derived_distance_restraint_dataset_list_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_dataset_list.id.',
                'markdown_name' : 'Dataset List Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_derived_distance_restraint_Entry_Related_File_fkey']}, 'RID'],
                'comment' : 'A reference to the uploaded restraint file in the table Entry_Related_File.id.',
                'markdown_name' : 'Uploaded Restraint File',
            },
            ['PDB', 'ihm_derived_distance_restraint_RCB_fkey'], 
            ['PDB', 'ihm_derived_distance_restraint_RMB_fkey'], 
            'RCT', 
            'RMT', 
            ['PDB', 'ihm_derived_distance_restraint_Owner_fkey'], 
        ],
    })

    # ----------------------------
    schema.tables["ihm_derived_distance_restraint"].columns["distance_lower_limit_esd"].display.update(
        {'name' : 'Distance Lower Limit Standard Deviation', }
    )

    # ----------------------------
    schema.tables["ihm_derived_distance_restraint"].columns["distance_upper_limit_esd"].display.update(
        {'name' : 'Distance Upper Limit Standard Deviation', }
    )

    # ----------------------------
    schema.tables["ihm_derived_distance_restraint"].foreign_keys[(schema,"ihm_derived_distance_restraint_feature_id_1_fkey")].foreign_key.update({
        'template_engine' :  'handlebars',
        'domain_filter_pattern' :  '{{#if _structure_id}}structure_id={{{_structure_id}}}{{/if}}',
    })

    # ----------------------------
    schema.tables["ihm_derived_distance_restraint"].foreign_keys[(schema,"ihm_derived_distance_restraint_feature_id_2_fkey")].foreign_key.update({
        'template_engine' :  'handlebars',
        'domain_filter_pattern' :  '{{#if _structure_id}}structure_id={{{_structure_id}}}{{/if}}',
    })

    # ----------------------------
    schema.tables["ihm_derived_distance_restraint"].foreign_keys[(schema,"ihm_derived_distance_restraint_dataset_list_id_fkey")].foreign_key.update({
        'template_engine' :  'handlebars',
        'domain_filter_pattern' :  '{{#if _structure_id}}structure_id={{{_structure_id}}}{{/if}}',
    })


# -- -----------------------------------------------------------------------------

def update_PDB_ihm_ensemble_info(model):
    schema = model.schemas["PDB"]
    table = schema.tables["ihm_ensemble_info"]
    # ----------------------------
    schema.tables["ihm_ensemble_info"].display.update(
        {'name' : 'Ensembles', 'comment_display' : {'*': {'table_comment_display': 'inline'}}, }
    )

    # ----------------------------
    schema.tables["ihm_ensemble_info"].table_display.update(
        {
            'row_name' : { 'row_markdown_pattern' : '{{{ensemble_id}}}', },
        }
    )

    # ----------------------------
    schema.tables["ihm_ensemble_info"].visible_columns.update( {
        '*' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_ensemble_info_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'ensemble_id', 
            'ensemble_name', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_ensemble_info_model_group_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_model_group.id.',
                'markdown_name' : 'Model Group Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_ensemble_info_post_process_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_modeling_post_process.id.',
                'markdown_name' : 'Post Process Id',
            },
            ['PDB', 'ihm_ensemble_info_ensemble_clustering_method_fkey'], 
            ['PDB', 'ihm_ensemble_info_ensemble_clustering_feature_fkey'], 
            ['PDB', 'ihm_ensemble_info_sub_sample_flag_fkey'], 
            ['PDB', 'ihm_ensemble_info_sub_sampling_type_fkey'], 
            ['PDB', 'ihm_ensemble_info_model_group_superimposed_flag_fkey'], 
            'num_ensemble_models', 
            'num_ensemble_models_deposited', 
            'ensemble_precision_value', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_ensemble_info_ensemble_file_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_external_files.id.',
                'markdown_name' : 'Ensemble File Id',
            },
            'details', 
        ],
        'entry' :  [
            {
                'source' : [{'outbound': ['PDB', 'ihm_ensemble_info_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'ensemble_id', 
            'ensemble_name', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_ensemble_info_model_group_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_model_group.id.',
                'markdown_name' : 'Model Group Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_ensemble_info_post_process_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_modeling_post_process.id.',
                'markdown_name' : 'Post Process Id',
            },
            ['PDB', 'ihm_ensemble_info_ensemble_clustering_method_fkey'], 
            ['PDB', 'ihm_ensemble_info_ensemble_clustering_feature_fkey'], 
            ['PDB', 'ihm_ensemble_info_sub_sample_flag_fkey'], 
            ['PDB', 'ihm_ensemble_info_sub_sampling_type_fkey'], 
            ['PDB', 'ihm_ensemble_info_model_group_superimposed_flag_fkey'], 
            'num_ensemble_models', 
            'num_ensemble_models_deposited', 
            'ensemble_precision_value', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_ensemble_info_ensemble_file_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_external_files.id.',
                'markdown_name' : 'Ensemble File Id',
            },
            'details', 
        ],
        'detailed' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_ensemble_info_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'ensemble_id', 
            'ensemble_name', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_ensemble_info_model_group_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_model_group.id.',
                'markdown_name' : 'Model Group Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_ensemble_info_post_process_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_modeling_post_process.id.',
                'markdown_name' : 'Post Process Id',
            },
            ['PDB', 'ihm_ensemble_info_ensemble_clustering_method_fkey'], 
            ['PDB', 'ihm_ensemble_info_ensemble_clustering_feature_fkey'], 
            ['PDB', 'ihm_ensemble_info_sub_sample_flag_fkey'], 
            ['PDB', 'ihm_ensemble_info_sub_sampling_type_fkey'], 
            ['PDB', 'ihm_ensemble_info_model_group_superimposed_flag_fkey'], 
            'num_ensemble_models', 
            'num_ensemble_models_deposited', 
            'ensemble_precision_value', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_ensemble_info_ensemble_file_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_external_files.id.',
                'markdown_name' : 'Ensemble File Id',
            },
            'details', 
            ['PDB', 'ihm_ensemble_info_RCB_fkey'], 
            ['PDB', 'ihm_ensemble_info_RMB_fkey'], 
            'RCT', 
            'RMT', 
            ['PDB', 'ihm_ensemble_info_Owner_fkey'], 
        ],
    })

    # ----------------------------
    schema.tables["ihm_ensemble_info"].visible_foreign_keys.update({
        'filter' :  'detailed',
        'detailed' :  [
            ['PDB', 'ihm_ensemble_sub_sample_ihm_ensemble_info_combo1_fkey'], 
            ['PDB', 'ihm_cross_link_result_ensemble_id_fkey'], 
            ['PDB', 'ihm_localization_density_files_ensemble_id_fkey'], 
        ],
    })

    # ----------------------------
    schema.tables["ihm_ensemble_info"].columns["num_ensemble_models"].display.update(
        {'name' : 'Number of Models in the Ensemble', }
    )

    # ----------------------------
    schema.tables["ihm_ensemble_info"].columns["num_ensemble_models_deposited"].display.update(
        {'name' : 'Number of Models Deposited that Belong to the Ensemble', }
    )

    # ----------------------------
    schema.tables["ihm_ensemble_info"].foreign_keys[(schema,"ihm_ensemble_info_model_group_id_fk")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })

    # ----------------------------
    schema.tables["ihm_ensemble_info"].foreign_keys[(schema,"ihm_ensemble_info_post_process_id_fkey")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })

    # ----------------------------
    schema.tables["ihm_ensemble_info"].foreign_keys[(schema,"ihm_ensemble_info_post_process_id_fk")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })

    # ----------------------------
    schema.tables["ihm_ensemble_info"].foreign_keys[(schema,"ihm_ensemble_info_ensemble_file_id_fk")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })

    # ----------------------------
    schema.tables["ihm_ensemble_info"].foreign_keys[(schema,"ihm_ensemble_info_ensemble_file_id_fkey")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })

    # ----------------------------
    schema.tables["ihm_ensemble_info"].foreign_keys[(schema,"ihm_ensemble_info_model_group_id_fkey")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })


# -- -----------------------------------------------------------------------------

def update_PDB_ihm_ensemble_sub_sample(model):
    schema = model.schemas["PDB"]
    table = schema.tables["ihm_ensemble_sub_sample"]
    # ----------------------------
    schema.tables["ihm_ensemble_sub_sample"].display.update(
        {'name' : 'Ensembles with Sub-samples', 'comment_display' : {'*': {'table_comment_display': 'inline'}}, }
    )

    # ----------------------------
    schema.tables["ihm_ensemble_sub_sample"].visible_columns.update( {
        '*' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_ensemble_sub_sample_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'id', 
            'sample_name', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_ensemble_sub_sample_ihm_ensemble_info_combo1_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_ensemble_info.ensemble_id.',
                'markdown_name' : 'Ensemble Id',
            },
            'num_models', 
            'num_models_deposited', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_ensemble_sub_sample_ihm_model_group_combo2_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_model_group.id.',
                'markdown_name' : 'Model Group Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_ensemble_sub_sample_ihm_external_files_combo2_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_external_files.id.',
                'markdown_name' : 'File Id',
            },
        ],
        'entry' :  [
            {
                'source' : [{'outbound': ['PDB', 'ihm_ensemble_sub_sample_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'id', 
            'sample_name', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_ensemble_sub_sample_ihm_ensemble_info_combo1_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_ensemble_info.ensemble_id.',
                'markdown_name' : 'Ensemble Id',
            },
            'num_models', 
            'num_models_deposited', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_ensemble_sub_sample_ihm_model_group_combo2_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_model_group.id.',
                'markdown_name' : 'Model Group Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_ensemble_sub_sample_ihm_external_files_combo2_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_external_files.id.',
                'markdown_name' : 'File Id',
            },
        ],
        'detailed' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_ensemble_sub_sample_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'id', 
            'sample_name', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_ensemble_sub_sample_ihm_ensemble_info_combo1_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_ensemble_info.ensemble_id.',
                'markdown_name' : 'Ensemble Id',
            },
            'num_models', 
            'num_models_deposited', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_ensemble_sub_sample_ihm_model_group_combo2_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_model_group.id.',
                'markdown_name' : 'Model Group Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_ensemble_sub_sample_ihm_external_files_combo2_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_external_files.id.',
                'markdown_name' : 'File Id',
            },
            ['PDB', 'ihm_ensemble_sub_sample_RCB_fkey'], 
            ['PDB', 'ihm_ensemble_sub_sample_RMB_fkey'], 
            'RCT', 
            'RMT', 
            ['PDB', 'ihm_ensemble_sub_sample_Owner_fkey'], 
        ],
    })

    # ----------------------------
    schema.tables["ihm_ensemble_sub_sample"].foreign_keys[(schema,"ihm_ensemble_sub_sample_ihm_external_files_combo2_fkey")].foreign_key.update({
        'template_engine' :  'handlebars',
        'domain_filter_pattern' :  '{{#if _structure_id}}structure_id={{{_structure_id}}}{{/if}}',
    })

    # ----------------------------
    schema.tables["ihm_ensemble_sub_sample"].foreign_keys[(schema,"ihm_ensemble_sub_sample_ihm_model_group_combo2_fkey")].foreign_key.update({
        'template_engine' :  'handlebars',
        'domain_filter_pattern' :  '{{#if _structure_id}}structure_id={{{_structure_id}}}{{/if}}',
    })

    # ----------------------------
    schema.tables["ihm_ensemble_sub_sample"].foreign_keys[(schema,"ihm_ensemble_sub_sample_ihm_ensemble_info_combo1_fkey")].foreign_key.update({
        'template_engine' :  'handlebars',
        'domain_filter_pattern' :  '{{#if _structure_id}}structure_id={{{_structure_id}}}{{/if}}',
    })


# -- -----------------------------------------------------------------------------
def update_PDB_ihm_entity_poly_segment(model):
    schema = model.schemas["PDB"]
    table = schema.tables["ihm_entity_poly_segment"]
    # ----------------------------
    schema.tables["ihm_entity_poly_segment"].display.update(
        {'markdown_name' : 'Segments of Polymeric Entities^*^', 'comment_display' : {'*': {'table_comment_display': 'inline'}}, }
    )

    # ----------------------------
    schema.tables["ihm_entity_poly_segment"].table_display.update({
        'row_name' : { 'row_markdown_pattern' : '{{{id}}}', },
    })

    # ----------------------------
    schema.tables["ihm_entity_poly_segment"].visible_columns.update({
        '*' :  [
            {'source' : 'RID', },
            {'source' : [{'outbound': ['PDB', 'ihm_entity_poly_segment_structure_id_fkey']}, 'RID'], },
            {'source' : 'id', },
            {'source' : [{'outbound': ['PDB', 'ihm_entity_poly_segment_mm_poly_res_label_begin_fkey']}, 'entity_id'], 'markdown_name' : 'Entity Id', },
            {'source' : [{'outbound': ['PDB', 'ihm_entity_poly_segment_mm_poly_res_label_begin_fkey']}, 'mon_id'], 'markdown_name' : 'Component Id Begin', },
            {'source' : [{'outbound': ['PDB', 'ihm_entity_poly_segment_mm_poly_res_label_end_fkey']}, 'mon_id'], 'markdown_name' : 'Component Id End', },
            {'source' : [{'outbound': ['PDB', 'ihm_entity_poly_segment_mm_poly_res_label_begin_fkey']}, 'num'], 'markdown_name' : 'Sequence Id Begin', },
            {'source' : [{'outbound': ['PDB', 'ihm_entity_poly_segment_mm_poly_res_label_end_fkey']}, 'num'], 'markdown_name' : 'Sequence Id End', },
            {
                'source' : [{'outbound': ['PDB', 'ihm_entity_poly_segment_mm_poly_res_label_begin_fkey']}, 'RID'],
                'comment' : 'Refers to a combination of Entity Id, Sequence Id and Component Id in the entity_poly_seq table.',
                'markdown_name' : 'Polymeric Residue Begin',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_entity_poly_segment_mm_poly_res_label_end_fkey']}, 'RID'],
                'comment' : 'Refers to a combination of Entity Id, Sequence Id and Component Id in the entity_poly_seq table.',
                'markdown_name' : 'Polymeric Residue End',
            },
        ],
        'entry' :  [
            {'source' : [{'outbound': ['PDB', 'ihm_entity_poly_segment_structure_id_fkey']}, 'RID'], },
            {'source' : 'id', },
            {'source' : [{'outbound': ['PDB', 'ihm_entity_poly_segment_mm_poly_res_label_begin_fkey']}, 'entity_id'], 'markdown_name' : 'Entity Id', },
            {'source' : [{'outbound': ['PDB', 'ihm_entity_poly_segment_mm_poly_res_label_begin_fkey']}, 'mon_id'], 'markdown_name' : 'Component Id Begin', },
            {'source' : [{'outbound': ['PDB', 'ihm_entity_poly_segment_mm_poly_res_label_end_fkey']}, 'mon_id'], 'markdown_name' : 'Component Id End', },
            {'source' : [{'outbound': ['PDB', 'ihm_entity_poly_segment_mm_poly_res_label_begin_fkey']}, 'num'], 'markdown_name' : 'Sequence Id Begin', },
            {'source' : [{'outbound': ['PDB', 'ihm_entity_poly_segment_mm_poly_res_label_end_fkey']}, 'num'], 'markdown_name' : 'Sequence Id End', },
            {
                'source' : [{'outbound': ['PDB', 'ihm_entity_poly_segment_mm_poly_res_label_begin_fkey']}, 'RID'],
                'comment' : 'Refers to a combination of Entity Id, Sequence Id and Component Id in the entity_poly_seq table.',
                'markdown_name' : 'Polymeric Residue Begin',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_entity_poly_segment_mm_poly_res_label_end_fkey']}, 'RID'],
                'comment' : 'Refers to a combination of Entity Id, Sequence Id and Component Id in the entity_poly_seq table.',
                'markdown_name' : 'Polymeric Residue End',
            },
        ],
        'detailed' :  [
            {'source' : 'RID', },
            {'source' : [{'outbound': ['PDB', 'ihm_entity_poly_segment_structure_id_fkey']}, 'RID'], },
            {'source' : 'id', },
            {'source' : [{'outbound': ['PDB', 'ihm_entity_poly_segment_mm_poly_res_label_begin_fkey']}, 'entity_id'], 'markdown_name' : 'Entity Id', },
            {'source' : [{'outbound': ['PDB', 'ihm_entity_poly_segment_mm_poly_res_label_begin_fkey']}, 'mon_id'], 'markdown_name' : 'Component Id Begin', },
            {'source' : [{'outbound': ['PDB', 'ihm_entity_poly_segment_mm_poly_res_label_end_fkey']}, 'mon_id'], 'markdown_name' : 'Component Id End', },
            {'source' : [{'outbound': ['PDB', 'ihm_entity_poly_segment_mm_poly_res_label_begin_fkey']}, 'num'], 'markdown_name' : 'Sequence Id Begin', },
            {'source' : [{'outbound': ['PDB', 'ihm_entity_poly_segment_mm_poly_res_label_end_fkey']}, 'num'], 'markdown_name' : 'Sequence Id End', },
            {
                'source' : [{'outbound': ['PDB', 'ihm_entity_poly_segment_mm_poly_res_label_begin_fkey']}, 'RID'],
                'comment' : 'Refers to a combination of Entity Id, Sequence Id and Component Id in the entity_poly_seq table.',
                'markdown_name' : 'Polymeric Residue Begin',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_entity_poly_segment_mm_poly_res_label_end_fkey']}, 'RID'],
                'comment' : 'Refers to a combination of Entity Id, Sequence Id and Component Id in the entity_poly_seq table.',
                'markdown_name' : 'Polymeric Residue End',
            },
            {'source' : 'RCT', },
            {'source' : 'RMT', },
            {'source' : [{'outbound': ['PDB', 'ihm_entity_poly_segment_RCB_fkey']}, 'RID'], },
            {'source' : [{'outbound': ['PDB', 'ihm_entity_poly_segment_RMB_fkey']}, 'RID'], },
            {'source' : [{'outbound': ['PDB', 'ihm_entity_poly_segment_Owner_fkey']}, 'RID'], },
        ],
    })

    # ----------------------------
    schema.tables["ihm_entity_poly_segment"].visible_foreign_keys.update({
        'filter' :  'detailed',
        'detailed' :  [
            ['PDB', 'ihm_model_representation_details_entity_poly_segment_id_fkey'], 
            ['PDB', 'ihm_struct_assembly_details_entity_poly_segment_id_fkey'], 
            ['PDB', 'ihm_starting_model_details_entity_poly_segment_id_fkey'], 
            ['PDB', 'ihm_localization_density_files_entity_poly_segment_id_fkey'], 
        ],
    })

    # ----------------------------
    schema.tables["ihm_entity_poly_segment"].foreign_keys[(schema,"ihm_entity_poly_segment_mm_poly_res_label_end_fkey")].foreign_key.update({
        'template_engine' :  'handlebars',
        'domain_filter_pattern' :  '{{#if _structure_id}}structure_id={{{_structure_id}}}{{/if}}',
    })

    # ----------------------------
    schema.tables["ihm_entity_poly_segment"].foreign_keys[(schema,"ihm_entity_poly_segment_mm_poly_res_label_begin_fkey")].foreign_key.update({
        'template_engine' :  'handlebars',
        'domain_filter_pattern' :  '{{#if _structure_id}}structure_id={{{_structure_id}}}{{/if}}',
    })



# -- -----------------------------------------------------------------------------
def update_PDB_ihm_entry_collection(model):
    schema = model.schemas["PDB"]
    table = schema.tables["ihm_entry_collection"]
    # ----------------------------
    schema.tables["ihm_entry_collection"].display.update(
        {'name' : 'Entry Collections', 'comment_display' : {'*': {'table_comment_display': 'inline'}}, }
    )

    # ----------------------------
    schema.tables["ihm_entry_collection"].visible_columns.update({
        '*' :  [
            'RID', 
            'id', 
            'name', 
            'details', 
        ],
        'entry' :  [
            'id', 
            'name', 
            'details', 
        ],
        'detailed' :  [
            'RID', 
            'id', 
            'name', 
            'details', 
            ['PDB', 'ihm_entry_collection_RCB_fkey'], 
            ['PDB', 'ihm_entry_collection_RMB_fkey'], 
            'RCT', 
            'RMT', 
            ['PDB', 'ihm_entry_collection_Owner_fkey'], 
        ],
    })

    # ----------------------------
    schema.tables["ihm_entry_collection"].visible_foreign_keys.update({
        'filter' :  'detailed',
        'detailed' :  [
            {
                'source' : [{'inbound': ['PDB', 'ihm_entry_collection_mapping_collection_id_fkey']}, {'outbound': ['PDB', 'ihm_entry_collection_mapping_entry_id_fkey']}, 'RID'],
                'comment' : 'Entries in this collection',
                'markdown_name' : 'Entry',
            },
        ],
    })

    # ----------------------------
    schema.tables["ihm_entry_collection"].columns["id"].display.update(
        {'name' : 'Collection Identifier', }
    )

    # ----------------------------
    schema.tables["ihm_entry_collection"].columns["name"].display.update(
        {'name' : 'Collection Name', }
    )

    # ----------------------------
    schema.tables["ihm_entry_collection"].columns["details"].display.update(
        {'name' : 'Collection Details', }
    )


# -- -----------------------------------------------------------------------------
def update_PDB_ihm_entry_collection_mapping(model):
    schema = model.schemas["PDB"]
    table = schema.tables["ihm_entry_collection_mapping"]
    # ----------------------------
    schema.tables["ihm_entry_collection_mapping"].display.update(
        {'name' : 'Entry Collection Mappings', 'comment_display' : {'*': {'table_comment_display': 'inline'}}, }
    )

    # ----------------------------
    schema.tables["ihm_entry_collection_mapping"].visible_columns.update({
        'entry' :  [
            {
                'source' : [{'outbound': ['PDB', 'ihm_entry_collection_mapping_collection_id_fkey']}, 'id'],
                'comment' : 'Entry Collection Id',
                'markdown_name' : 'Entry Collection Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_entry_collection_mapping_entry_id_fkey']}, 'id'],
                'comment' : 'Entry Id',
                'markdown_name' : 'Entry Id',
            },
        ],
        'compact' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_entry_collection_mapping_collection_id_fkey']}, 'id'],
                'comment' : 'Entry Collection Id',
                'markdown_name' : 'Entry Collection Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_entry_collection_mapping_entry_id_fkey']}, 'id'],
                'comment' : 'Entry Id',
                'markdown_name' : 'Entry Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_entry_collection_mapping_entry_id_fkey']}, 'Accession_Code'],
                'comment' : 'Entry Accession Code',
                'markdown_name' : 'Accession Code',
            },
        ],
        'detailed' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_entry_collection_mapping_collection_id_fkey']}, 'id'],
                'comment' : 'Entry Collection Id',
                'markdown_name' : 'Entry Collection Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_entry_collection_mapping_entry_id_fkey']}, 'id'],
                'comment' : 'Entry Id',
                'markdown_name' : 'Entry Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_entry_collection_mapping_entry_id_fkey']}, 'Accession_Code'],
                'comment' : 'Entry Accession Code',
                'markdown_name' : 'Accession Code',
            },
            ['PDB', 'ihm_entry_collection_mapping_RCB_fkey'], 
            ['PDB', 'ihm_entry_collection_mapping_RMB_fkey'], 
            'RCT', 
            'RMT', 
            ['PDB', 'ihm_entry_collection_mapping_Owner_fkey'], 
        ],
    })

    # ----------------------------
    schema.tables["ihm_entry_collection_mapping"].columns["collection_id"].display.update(
        {'name' : 'Collection Identifier', }
    )

    # ----------------------------
    schema.tables["ihm_entry_collection_mapping"].columns["entry_id"].display.update(
        {'name' : 'Entry Identifier', }
    )



# -- -----------------------------------------------------------------------------
def update_PDB_ihm_epr_restraint(model):
    schema = model.schemas["PDB"]
    table = schema.tables["ihm_epr_restraint"]
    # ----------------------------
    schema.tables["ihm_epr_restraint"].display.update(
        {'name' : 'EPR Restraints', 'comment_display' : {'*': {'table_comment_display': 'inline'}}, }
    )

    # ----------------------------
    schema.tables["ihm_epr_restraint"].visible_columns.update({
        '*' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_epr_restraint_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'ordinal_id', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_epr_restraint_model_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_model_list.model_id.',
                'markdown_name' : 'Model Id',
            },
            'fitting_particle_type', 
            'fitting_method', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_epr_restraint_fitting_method_citation_id_fkey']}, 'RID'],
                'comment' : 'A reference to table citation.id.',
                'markdown_name' : 'Fitting Method Citation Id',
            },
            ['PDB', 'ihm_epr_restraint_fitting_state_fkey'], 
            {
                'source' : [{'outbound': ['PDB', 'ihm_epr_restraint_fitting_software_id_fkey']}, 'RID'],
                'comment' : 'A reference to table software.pdbx_ordinal.',
                'markdown_name' : 'Fitting Software Id',
            },
            'chi_value', 
            'details', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_epr_restraint_dataset_list_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_dataset_list.id.',
                'markdown_name' : 'Dataset List Id',
            },
        ],
        'entry' :  [
            {
                'source' : [{'outbound': ['PDB', 'ihm_epr_restraint_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'ordinal_id', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_epr_restraint_model_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_model_list.model_id.',
                'markdown_name' : 'Model Id',
            },
            'fitting_particle_type', 
            'fitting_method', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_epr_restraint_fitting_method_citation_id_fkey']}, 'RID'],
                'comment' : 'A reference to table citation.id.',
                'markdown_name' : 'Fitting Method Citation Id',
            },
            ['PDB', 'ihm_epr_restraint_fitting_state_fkey'], 
            {
                'source' : [{'outbound': ['PDB', 'ihm_epr_restraint_fitting_software_id_fkey']}, 'RID'],
                'comment' : 'A reference to table software.pdbx_ordinal.',
                'markdown_name' : 'Fitting Software Id',
            },
            'chi_value', 
            'details', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_epr_restraint_dataset_list_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_dataset_list.id.',
                'markdown_name' : 'Dataset List Id',
            },
        ],
        'detailed' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_epr_restraint_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'ordinal_id', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_epr_restraint_model_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_model_list.model_id.',
                'markdown_name' : 'Model Id',
            },
            'fitting_particle_type', 
            'fitting_method', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_epr_restraint_fitting_method_citation_id_fkey']}, 'RID'],
                'comment' : 'A reference to table citation.id.',
                'markdown_name' : 'Fitting Method Citation Id',
            },
            ['PDB', 'ihm_epr_restraint_fitting_state_fkey'], 
            {
                'source' : [{'outbound': ['PDB', 'ihm_epr_restraint_fitting_software_id_fkey']}, 'RID'],
                'comment' : 'A reference to table software.pdbx_ordinal.',
                'markdown_name' : 'Fitting Software Id',
            },
            'chi_value', 
            'details', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_epr_restraint_dataset_list_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_dataset_list.id.',
                'markdown_name' : 'Dataset List Id',
            },
            ['PDB', 'ihm_epr_restraint_RCB_fkey'], 
            ['PDB', 'ihm_epr_restraint_RMB_fkey'], 
            'RCT', 
            'RMT', 
            ['PDB', 'ihm_epr_restraint_Owner_fkey'], 
        ],
    })

    # ----------------------------
    schema.tables["ihm_epr_restraint"].foreign_keys[(schema,"ihm_epr_restraint_fitting_method_citation_id_fkey")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })

    # ----------------------------
    schema.tables["ihm_epr_restraint"].foreign_keys[(schema,"ihm_epr_restraint_dataset_list_id_fkey")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })

    # ----------------------------
    schema.tables["ihm_epr_restraint"].foreign_keys[(schema,"ihm_epr_restraint_model_id_fkey")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })

    # ----------------------------
    schema.tables["ihm_epr_restraint"].foreign_keys[(schema,"ihm_epr_restraint_fitting_software_id_fkey")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })

    # ----------------------------
    schema.tables["ihm_epr_restraint"].foreign_keys[(schema,"ihm_epr_restraint_fitting_method_citation_id_fk")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })


# -- -----------------------------------------------------------------------------
def update_PDB_ihm_external_files(model):
    schema = model.schemas["PDB"]
    table = schema.tables["ihm_external_files"]
    # ----------------------------
    schema.tables["ihm_external_files"].display.update(
        {'name' : 'External Files Referenced Via DOI', 'comment_display' : {'*': {'table_comment_display': 'inline'}}, }
    )
    
    # ----------------------------
    schema.tables["ihm_external_files"].table_display.update({
        'row_name' : { 'row_markdown_pattern' : '{{{id}}}', },
    })

    # ----------------------------
    schema.tables["ihm_external_files"].visible_columns.update({
        '*' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_external_files_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'id', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_external_files_reference_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_external_reference_info.reference_id.',
                'markdown_name' : 'Reference Id',
            },
            'file_path', 
            ['PDB', 'ihm_external_files_file_format_fkey'], 
            ['PDB', 'ihm_external_files_content_type_fkey'], 
            'file_size_bytes', 
            'details', 
        ],
        'entry' :  [
            {
                'source' : [{'outbound': ['PDB', 'ihm_external_files_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'id', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_external_files_reference_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_external_reference_info.reference_id.',
                'markdown_name' : 'Reference Id',
            },
            'file_path', 
            ['PDB', 'ihm_external_files_file_format_fkey'], 
            ['PDB', 'ihm_external_files_content_type_fkey'], 
            'file_size_bytes', 
            'details', 
        ],
        'detailed' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_external_files_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'id', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_external_files_reference_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_external_reference_info.reference_id.',
                'markdown_name' : 'Reference Id',
            },
            'file_path', 
            ['PDB', 'ihm_external_files_file_format_fkey'], 
            ['PDB', 'ihm_external_files_content_type_fkey'], 
            'file_size_bytes', 
            'details', 
            ['PDB', 'ihm_external_files_RCB_fkey'], 
            ['PDB', 'ihm_external_files_RMB_fkey'], 
            'RCT', 
            'RMT', 
            ['PDB', 'ihm_external_files_Owner_fkey'], 
        ],
    })

    # ----------------------------
    schema.tables["ihm_external_files"].visible_foreign_keys.update({
        'filter' :  'detailed',
        'detailed' :  [
            ['PDB', 'ihm_dataset_external_reference_file_id_fkey'], 
            ['PDB', 'ihm_modeling_protocol_details_script_file_id_fkey'], 
            ['PDB', 'ihm_modeling_post_process_script_file_id_fkey'], 
            ['PDB', 'ihm_starting_comparative_models_alignment_file_id_fkey'], 
            ['PDB', 'ihm_starting_computational_models_script_file_id_fkey'], 
            ['PDB', 'ihm_ensemble_info_ensemble_file_id_fkey'], 
            ['PDB', 'ihm_ensemble_sub_sample_ihm_external_files_combo2_fkey'], 
            ['PDB', 'ihm_localization_density_files_file_id_fkey'], 
            ['PDB', 'ihm_kinetic_rate_ihm_external_files_combo2_fkey'], 
            ['PDB', 'ihm_relaxation_time_ihm_external_files_combo2_fkey'], 
        ],
    })

    # ----------------------------
    schema.tables["ihm_external_files"].columns["reference_id"].display.update(
        {'name' : 'Reference Id', }
    )
    
    # ----------------------------
    schema.tables["ihm_external_files"].foreign_keys[(schema,"ihm_external_files_reference_id_fkey")].foreign_key.update( {
            'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })


# -- -----------------------------------------------------------------------------
def update_PDB_ihm_external_reference_info(model):
    schema = model.schemas["PDB"]
    table = schema.tables["ihm_external_reference_info"]
    # ----------------------------
    schema.tables["ihm_external_reference_info"].display.update(
        {'name' : 'Datasets Referenced Via DOI', 'comment_display' : {'*': {'table_comment_display': 'inline'}}, }
    )

    # ----------------------------
    schema.tables["ihm_external_reference_info"].table_display.update({
        'row_name' : { 'row_markdown_pattern' : '{{{reference_id}}}', },
    })

    # ----------------------------
    schema.tables["ihm_external_reference_info"].visible_columns.update({
        '*' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_external_reference_info_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'reference_id', 
            'reference_provider', 
            ['PDB', 'ihm_external_reference_info_reference_type_fkey'], 
            'reference', 
            ['PDB', 'ihm_external_reference_info_refers_to_fkey'], 
            'associated_url', 
            'details', 
        ],
        'entry' :  [
            {
                'source' : [{'outbound': ['PDB', 'ihm_external_reference_info_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'reference_id', 
            'reference_provider', 
            ['PDB', 'ihm_external_reference_info_reference_type_fkey'], 
            'reference', 
            ['PDB', 'ihm_external_reference_info_refers_to_fkey'], 
            'associated_url', 
            'details', 
        ],
        'detailed' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_external_reference_info_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'reference_id', 
            'reference_provider', 
            ['PDB', 'ihm_external_reference_info_reference_type_fkey'], 
            'reference', 
            ['PDB', 'ihm_external_reference_info_refers_to_fkey'], 
            'associated_url', 
            'details', 
            ['PDB', 'ihm_external_reference_info_RCB_fkey'], 
            ['PDB', 'ihm_external_reference_info_RMB_fkey'], 
            'RCT', 
            'RMT', 
            ['PDB', 'ihm_external_reference_info_Owner_fkey'], 
        ],
    })

    # ----------------------------
    schema.tables["ihm_external_reference_info"].visible_foreign_keys.update({
        'filter' :  'detailed',
        'detailed' :  [
            ['PDB', 'ihm_external_files_reference_id_fkey'], 
        ],
    })

    # ----------------------------
    schema.tables["ihm_external_reference_info"].columns["reference_id"].display.update(
        {'name' : 'Reference Id', }
    )


# -- -----------------------------------------------------------------------------
def update_PDB_ihm_feature_list(model):
    schema = model.schemas["PDB"]
    table = schema.tables["ihm_feature_list"]
    # ----------------------------
    schema.tables["ihm_feature_list"].display.update(
        {'name' : 'Molecular Features used in Generic Restraints', 'comment_display' : {'*': {'table_comment_display': 'inline'}}, }
    )

    # ----------------------------
    schema.tables["ihm_feature_list"].table_display.update({
        'row_name' : { 'row_markdown_pattern' : '{{{feature_id}}}', },
    })

    # ----------------------------
    schema.tables["ihm_feature_list"].visible_columns.update({
        '*' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_feature_list_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'feature_id', 
            ['PDB', 'ihm_feature_list_feature_type_fkey'], 
            ['PDB', 'ihm_feature_list_entity_type_fkey'], 
            'details', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_feature_list_Entry_Related_File_fkey']}, 'RID'],
                'comment' : 'A reference to the uploaded restraint file in the table Entry_Related_File.id.',
                'markdown_name' : 'Uploaded Restraint File',
            },
        ],
        'entry' :  [
            {
                'source' : [{'outbound': ['PDB', 'ihm_feature_list_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'feature_id', 
            ['PDB', 'ihm_feature_list_feature_type_fkey'], 
            ['PDB', 'ihm_feature_list_entity_type_fkey'], 
            'details', 
        ],
        'detailed' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_feature_list_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'feature_id', 
            ['PDB', 'ihm_feature_list_feature_type_fkey'], 
            ['PDB', 'ihm_feature_list_entity_type_fkey'], 
            'details', 
            ['PDB', 'ihm_feature_list_feature_type_fkey'], 
            {
                'source' : [{'outbound': ['PDB', 'ihm_feature_list_Entry_Related_File_fkey']}, 'RID'],
                'comment' : 'A reference to the uploaded restraint file in the table Entry_Related_File.id.',
                'markdown_name' : 'Uploaded Restraint File',
            },
            ['PDB', 'ihm_feature_list_RCB_fkey'], 
            ['PDB', 'ihm_feature_list_RMB_fkey'], 
            'RCT', 
            'RMT', 
            ['PDB', 'ihm_feature_list_Owner_fkey'], 
        ],
    })

    # ----------------------------
    schema.tables["ihm_feature_list"].visible_foreign_keys.update({
        'filter' :  'detailed',
        'detailed' :  [
            ['PDB', 'ihm_poly_atom_feature_feature_id_fkey'], 
            ['PDB', 'ihm_poly_residue_feature_feature_id_fkey'], 
            ['PDB', 'ihm_non_poly_feature_feature_id_fkey'], 
            ['PDB', 'ihm_interface_residue_feature_feature_id_fkey'], 
            ['PDB', 'ihm_pseudo_site_feature_ihm_feature_list_combo1_fkey'], 
            ['PDB', 'ihm_hdx_restraint_ihm_feature_list_combo1_fkey'], 
            ['PDB', 'ihm_derived_distance_restraint_feature_id_1_fkey'], 
            ['PDB', 'ihm_derived_angle_restraint_ihm_feature_list_1_combo1_fkey'], 
            ['PDB', 'ihm_derived_dihedral_restraint_ihm_feature_list_1_combo1_fkey'], 
            ['PDB', 'ihm_geometric_object_distance_restraint_feature_id_fkey'], 
        ],
    })


# -- -----------------------------------------------------------------------------
def update_PDB_ihm_geometric_object_axis(model):
    schema = model.schemas["PDB"]
    table = schema.tables["ihm_geometric_object_axis"]
    # ----------------------------
    schema.tables["ihm_geometric_object_axis"].display.update(
        {'name' : 'Axis Geomtric Objects', 'comment_display' : {'*': {'table_comment_display': 'inline'}}, }
    )

    # ----------------------------
    schema.tables["ihm_geometric_object_axis"].visible_columns.update({
        '*' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_geometric_object_axis_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_geometric_object_axis_object_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_geometric_object_list.object_id.',
                'markdown_name' : 'Object Id',
            },
            ['PDB', 'ihm_geometric_object_axis_axis_type_fkey'], 
            {
                'source' : [{'outbound': ['PDB', 'ihm_geometric_object_axis_transformation_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_geometric_object_transformation.id.',
                'markdown_name' : 'Transformation Id',
            },
        ],
        'entry' :  [
            {
                'source' : [{'outbound': ['PDB', 'ihm_geometric_object_axis_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_geometric_object_axis_object_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_geometric_object_list.object_id.',
                'markdown_name' : 'Object Id',
            },
            ['PDB', 'ihm_geometric_object_axis_axis_type_fkey'], 
            {
                'source' : [{'outbound': ['PDB', 'ihm_geometric_object_axis_transformation_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_geometric_object_transformation.id.',
                'markdown_name' : 'Transformation Id',
            },
        ],
        'detailed' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_geometric_object_axis_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_geometric_object_axis_object_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_geometric_object_list.object_id.',
                'markdown_name' : 'Object Id',
            },
            ['PDB', 'ihm_geometric_object_axis_axis_type_fkey'], 
            {
                'source' : [{'outbound': ['PDB', 'ihm_geometric_object_axis_transformation_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_geometric_object_transformation.id.',
                'markdown_name' : 'Transformation Id',
            },
            ['PDB', 'ihm_geometric_object_axis_RCB_fkey'], 
            ['PDB', 'ihm_geometric_object_axis_RMB_fkey'], 
            'RCT', 
            'RMT', 
            ['PDB', 'ihm_geometric_object_axis_Owner_fkey'], 
        ],
    })

    # ----------------------------
    schema.tables["ihm_geometric_object_axis"].foreign_keys[(schema,"ihm_geometric_object_axis_object_id_fkey")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })

    # ----------------------------
    schema.tables["ihm_geometric_object_axis"].foreign_keys[(schema,"ihm_geometric_object_axis_transformation_id_fk")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })

    # ----------------------------
    schema.tables["ihm_geometric_object_axis"].foreign_keys[(schema,"ihm_geometric_object_axis_transformation_id_fkey")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })



# -- -----------------------------------------------------------------------------
def update_PDB_ihm_geometric_object_center(model):
    schema = model.schemas["PDB"]
    table = schema.tables["ihm_geometric_object_center"]
    # ----------------------------
    schema.tables["ihm_geometric_object_center"].display.update(
        {'name' : 'Geometric Object Centers', 'comment_display' : {'*': {'table_comment_display': 'inline'}}, }
    )
    
    # ----------------------------
    schema.tables["ihm_geometric_object_center"].table_display.update({
        'row_name' : { 'row_markdown_pattern' : '{{{id}}}', },
    })

    # ----------------------------
    schema.tables["ihm_geometric_object_center"].visible_columns.update({
        '*' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_geometric_object_center_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'id', 
            'xcoord', 
            'ycoord', 
            'zcoord', 
        ],
        'entry' :  [
            {
                'source' : [{'outbound': ['PDB', 'ihm_geometric_object_center_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'id', 
            'xcoord', 
            'ycoord', 
            'zcoord', 
        ],
        'detailed' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_geometric_object_center_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'id', 
            'xcoord', 
            'ycoord', 
            'zcoord', 
            ['PDB', 'ihm_geometric_object_center_RCB_fkey'], 
            ['PDB', 'ihm_geometric_object_center_RMB_fkey'], 
            'RCT', 
            'RMT', 
            ['PDB', 'ihm_geometric_object_center_Owner_fkey'], 
        ],
    })

    # ----------------------------
    schema.tables["ihm_geometric_object_center"].visible_foreign_keys.update({
        'filter' :  'detailed',
        'detailed' :  [
            ['PDB', 'ihm_geometric_object_sphere_center_id_fkey'], 
            ['PDB', 'ihm_geometric_object_torus_center_id_fkey'], 
        ],
    })

# -- -----------------------------------------------------------------------------
def update_PDB_ihm_geometric_object_distance_restraint(model):
    schema = model.schemas["PDB"]
    table = schema.tables["ihm_geometric_object_distance_restraint"]
    # ----------------------------
    schema.tables["ihm_geometric_object_distance_restraint"].display.update(
        {'name' : 'Distance Restraints between Geometric Objects and Molecular Features', 'comment_display' : {'*': {'table_comment_display': 'inline'}}, }
    )
    
    # ----------------------------
    schema.tables["ihm_geometric_object_distance_restraint"].visible_columns.update({
        '*' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_geometric_object_distance_restraint_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'id', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_geometric_object_distance_restraint_object_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_geometric_object_list.object_id.',
                'markdown_name' : 'Object Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_geometric_object_distance_restraint_feature_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_feature_list.feature_id.',
                'markdown_name' : 'Feature Id',
            },
            ['PDB', 'geometric_object_distance_restraint_object_character_fkey'], 
            ['PDB', 'ihm_geometric_object_distance_restraint_restraint_type_fkey'], 
            'harmonic_force_constant', 
            ['PDB', 'geometric_object_distance_restraint_group_condition_fkey'], 
            'distance_lower_limit', 
            'distance_upper_limit', 
            'distance_lower_limit_esd', 
            'distance_upper_limit_esd', 
            'distance_probability', 
            'details', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_geometric_object_distance_restraint_dataset_list_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_dataset_list.id.',
                'markdown_name' : 'Dataset List Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'geometric_object_distance_restraint_Entry_Related_File_fkey']}, 'RID'],
                'comment' : 'A reference to the uploaded restraint file in the table Entry_Related_File.id.',
                'markdown_name' : 'Uploaded Restraint File',
            },
        ],
        'entry' :  [
            {
                'source' : [{'outbound': ['PDB', 'ihm_geometric_object_distance_restraint_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'id', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_geometric_object_distance_restraint_object_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_geometric_object_list.object_id.',
                'markdown_name' : 'Object Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_geometric_object_distance_restraint_feature_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_feature_list.feature_id.',
                'markdown_name' : 'Feature Id',
            },
            ['PDB', 'geometric_object_distance_restraint_object_character_fkey'], 
            ['PDB', 'ihm_geometric_object_distance_restraint_restraint_type_fkey'], 
            'harmonic_force_constant', 
            ['PDB', 'geometric_object_distance_restraint_group_condition_fkey'], 
            'distance_lower_limit', 
            'distance_upper_limit', 
            'distance_lower_limit_esd', 
            'distance_upper_limit_esd', 
            'distance_probability', 
            'details', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_geometric_object_distance_restraint_dataset_list_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_dataset_list.id.',
                'markdown_name' : 'Dataset List Id',
            },
        ],
        'detailed' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_geometric_object_distance_restraint_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'id', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_geometric_object_distance_restraint_object_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_geometric_object_list.object_id.',
                'markdown_name' : 'Object Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_geometric_object_distance_restraint_feature_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_feature_list.feature_id.',
                'markdown_name' : 'Feature Id',
            },
            ['PDB', 'geometric_object_distance_restraint_object_character_fkey'], 
            ['PDB', 'ihm_geometric_object_distance_restraint_restraint_type_fkey'], 
            'harmonic_force_constant', 
            ['PDB', 'geometric_object_distance_restraint_group_condition_fkey'], 
            'distance_lower_limit', 
            'distance_upper_limit', 
            'distance_lower_limit_esd', 
            'distance_upper_limit_esd', 
            'distance_probability', 
            'details', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_geometric_object_distance_restraint_dataset_list_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_dataset_list.id.',
                'markdown_name' : 'Dataset List Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'geometric_object_distance_restraint_Entry_Related_File_fkey']}, 'RID'],
                'comment' : 'A reference to the uploaded restraint file in the table Entry_Related_File.id.',
                'markdown_name' : 'Uploaded Restraint File',
            },
            ['PDB', 'ihm_geometric_object_distance_restraint_RCB_fkey'], 
            ['PDB', 'ihm_geometric_object_distance_restraint_RMB_fkey'], 
            'RCT', 
            'RMT', 
            ['PDB', 'ihm_geometric_object_distance_restraint_Owner_fkey'], 
        ],
    })
    
    # ----------------------------
    schema.tables["ihm_geometric_object_distance_restraint"].columns["distance_lower_limit_esd"].display.update(
        {'name' : 'Distance Lower Limit Standard Deviation', }
    )

    # ----------------------------
    schema.tables["ihm_geometric_object_distance_restraint"].columns["distance_upper_limit_esd"].display.update(
        {'name' : 'Distance Upper Limit Standard Deviation', }
    )

    # ----------------------------
    schema.tables["ihm_geometric_object_distance_restraint"].foreign_keys[(schema,"ihm_geometric_object_distance_restraint_object_id_fkey")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })

    # ----------------------------
    schema.tables["ihm_geometric_object_distance_restraint"].foreign_keys[(schema,"ihm_geometric_object_distance_restraint_feature_id_fkey")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })

    # ----------------------------
    schema.tables["ihm_geometric_object_distance_restraint"].foreign_keys[(schema,"ihm_geometric_object_distance_restraint_dataset_list_id_fkey")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })


# -- -----------------------------------------------------------------------------
def update_PDB_ihm_geometric_object_half_torus(model):
    schema = model.schemas["PDB"]
    table = schema.tables["ihm_geometric_object_half_torus"]
    # ----------------------------
    schema.tables["ihm_geometric_object_half_torus"].display.update(
        {'name' : 'Half-torus Geometric Objects', 'comment_display' : {'*': {'table_comment_display': 'inline'}}, }
    )

    # ----------------------------
    schema.tables["ihm_geometric_object_half_torus"].visible_columns.update({
        '*' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_geometric_object_half_torus_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_geometric_object_half_torus_object_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_geometric_object_list.object_id.',
                'markdown_name' : 'Object Id',
            },
            'thickness_th', 
            ['PDB', 'ihm_geometric_object_half_torus_section_fkey'], 
        ],
        'entry' :  [
            {
                'source' : [{'outbound': ['PDB', 'ihm_geometric_object_half_torus_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_geometric_object_half_torus_object_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_geometric_object_list.object_id.',
                'markdown_name' : 'Object Id',
            },
            'thickness_th', 
            ['PDB', 'ihm_geometric_object_half_torus_section_fkey'], 
        ],
        'detailed' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_geometric_object_half_torus_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_geometric_object_half_torus_object_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_geometric_object_list.object_id.',
                'markdown_name' : 'Object Id',
            },
            'thickness_th', 
            ['PDB', 'ihm_geometric_object_half_torus_section_fkey'], 
            ['PDB', 'ihm_geometric_object_half_torus_RCB_fkey'], 
            ['PDB', 'ihm_geometric_object_half_torus_RMB_fkey'], 
            'RCT', 
            'RMT', 
            ['PDB', 'ihm_geometric_object_half_torus_Owner_fkey'], 
        ],
    })

    # ----------------------------
    schema.tables["ihm_geometric_object_half_torus"].columns["thickness_th"].display.update(
        {'name' : 'Thickness', }
    )

    # ----------------------------
    schema.tables["ihm_geometric_object_half_torus"].foreign_keys[(schema,"ihm_geometric_object_half_torus_object_id_fkey")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })


# -- -----------------------------------------------------------------------------
def update_PDB_ihm_geometric_object_list(model):
    schema = model.schemas["PDB"]
    table = schema.tables["ihm_geometric_object_list"]
    
    # ----------------------------
    schema.tables["ihm_geometric_object_list"].display.update(
        {'name' : 'Geometric Objects used as Restraints', 'comment_display' : {'*': {'table_comment_display': 'inline'}}, }
    )

    # ----------------------------
    schema.tables["ihm_geometric_object_list"].table_display.update({
        'row_name' : { 'row_markdown_pattern' : '{{{object_id}}}', },
    })

    # ----------------------------
    schema.tables["ihm_geometric_object_list"].visible_columns.update({
        '*' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_geometric_object_list_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'object_id', 
            ['PDB', 'ihm_geometric_object_list_object_type_fkey'], 
            'object_name', 
            'object_description', 
        ],
        'entry' :  [
            {
                'source' : [{'outbound': ['PDB', 'ihm_geometric_object_list_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'object_id', 
            ['PDB', 'ihm_geometric_object_list_object_type_fkey'], 
            'object_name', 
            'object_description', 
        ],
        'detailed' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_geometric_object_list_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'object_id', 
            ['PDB', 'ihm_geometric_object_list_object_type_fkey'], 
            'object_name', 
            'object_description', 
            ['PDB', 'ihm_geometric_object_list_RCB_fkey'], 
            ['PDB', 'ihm_geometric_object_list_RMB_fkey'], 
            'RCT', 
            'RMT', 
            ['PDB', 'ihm_geometric_object_list_Owner_fkey'], 
        ],
    })

    # ----------------------------
    schema.tables["ihm_geometric_object_list"].visible_foreign_keys.update({
        'filter' :  'detailed',
        'detailed' :  [
            ['PDB', 'ihm_geometric_object_sphere_object_id_fkey'], 
            ['PDB', 'ihm_geometric_object_torus_object_id_fkey'], 
            ['PDB', 'ihm_geometric_object_axis_object_id_fkey'], 
            ['PDB', 'ihm_geometric_object_plane_object_id_fkey'], 
            ['PDB', 'ihm_geometric_object_distance_restraint_object_id_fkey'], 
        ],
    })


# -- -----------------------------------------------------------------------------
def update_PDB_ihm_geometric_object_plane(model):
    schema = model.schemas["PDB"]
    table = schema.tables["ihm_geometric_object_plane"]
    # ----------------------------
    schema.tables["ihm_geometric_object_plane"].display.update(
        {'name' : 'Plane Geometric Objects', 'comment_display' : {'*': {'table_comment_display': 'inline'}}, }
    )

    # ----------------------------
    schema.tables["ihm_geometric_object_plane"].visible_columns.update({
        '*' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_geometric_object_plane_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_geometric_object_plane_object_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_geometric_object_list.object_id.',
                'markdown_name' : 'Object Id',
            },
            ['PDB', 'ihm_geometric_object_plane_plane_type_fkey'], 
            {
                'source' : [{'outbound': ['PDB', 'ihm_geometric_object_plane_transformation_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_geometric_object_transformation.id.',
                'markdown_name' : 'Transformation Id',
            },
        ],
        'entry' :  [
            {
                'source' : [{'outbound': ['PDB', 'ihm_geometric_object_plane_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_geometric_object_plane_object_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_geometric_object_list.object_id.',
                'markdown_name' : 'Object Id',
            },
            ['PDB', 'ihm_geometric_object_plane_plane_type_fkey'], 
            {
                'source' : [{'outbound': ['PDB', 'ihm_geometric_object_plane_transformation_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_geometric_object_transformation.id.',
                'markdown_name' : 'Transformation Id',
            },
        ],
        'detailed' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_geometric_object_plane_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_geometric_object_plane_object_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_geometric_object_list.object_id.',
                'markdown_name' : 'Object Id',
            },
            ['PDB', 'ihm_geometric_object_plane_plane_type_fkey'], 
            {
                'source' : [{'outbound': ['PDB', 'ihm_geometric_object_plane_transformation_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_geometric_object_transformation.id.',
                'markdown_name' : 'Transformation Id',
            },
            ['PDB', 'ihm_geometric_object_plane_RCB_fkey'], 
            ['PDB', 'ihm_geometric_object_plane_RMB_fkey'], 
            'RCT', 
            'RMT', 
            ['PDB', 'ihm_geometric_object_plane_Owner_fkey'], 
        ],
    })

    # ----------------------------
    schema.tables["ihm_geometric_object_plane"].foreign_keys[(schema,"ihm_geometric_object_plane_transformation_id_fk")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })
    
    # ----------------------------
    schema.tables["ihm_geometric_object_plane"].foreign_keys[(schema,"ihm_geometric_object_plane_object_id_fkey")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })

    # ----------------------------
    schema.tables["ihm_geometric_object_plane"].foreign_keys[(schema,"ihm_geometric_object_plane_transformation_id_fkey")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })


# -- -----------------------------------------------------------------------------
def update_PDB_ihm_geometric_object_sphere(model):
    schema = model.schemas["PDB"]
    table = schema.tables["ihm_geometric_object_sphere"]
    # ----------------------------
    schema.tables["ihm_geometric_object_sphere"].display.update(
        {'name' : 'Spherical Geometric Objects', 'comment_display' : {'*': {'table_comment_display': 'inline'}}, }
    )
    
    # ----------------------------
    schema.tables["ihm_geometric_object_sphere"].visible_columns.update({
        '*' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_geometric_object_sphere_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_geometric_object_sphere_object_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_geometric_object_list.object_id.',
                'markdown_name' : 'Object Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_geometric_object_sphere_center_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_geometric_object_center.id.',
                'markdown_name' : 'Center Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_geometric_object_sphere_transformation_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_geometric_object_transformation.id.',
                'markdown_name' : 'Transformation Id',
            },
            'radius_r', 
        ],
        'entry' :  [
            {
                'source' : [{'outbound': ['PDB', 'ihm_geometric_object_sphere_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_geometric_object_sphere_object_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_geometric_object_list.object_id.',
                'markdown_name' : 'Object Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_geometric_object_sphere_center_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_geometric_object_center.id.',
                'markdown_name' : 'Center Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_geometric_object_sphere_transformation_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_geometric_object_transformation.id.',
                'markdown_name' : 'Transformation Id',
            },
            'radius_r', 
        ],
        'detailed' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_geometric_object_sphere_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_geometric_object_sphere_object_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_geometric_object_list.object_id.',
                'markdown_name' : 'Object Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_geometric_object_sphere_center_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_geometric_object_center.id.',
                'markdown_name' : 'Center Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_geometric_object_sphere_transformation_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_geometric_object_transformation.id.',
                'markdown_name' : 'Transformation Id',
            },
            'radius_r', 
            ['PDB', 'ihm_geometric_object_sphere_RCB_fkey'], 
            ['PDB', 'ihm_geometric_object_sphere_RMB_fkey'], 
            'RCT', 
            'RMT', 
            ['PDB', 'ihm_geometric_object_sphere_Owner_fkey'], 
        ],
    })

    # ----------------------------
    schema.tables["ihm_geometric_object_sphere"].foreign_keys[(schema,"ihm_geometric_object_sphere_center_id_fkey")].foreign_key.update( {
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })

    # ----------------------------
    schema.tables["ihm_geometric_object_sphere"].foreign_keys[(schema,"ihm_geometric_object_sphere_transformation_id_fk")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })

    # ----------------------------
    schema.tables["ihm_geometric_object_sphere"].foreign_keys[(schema,"ihm_geometric_object_sphere_transformation_id_fkey")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })
    
    # ----------------------------
    schema.tables["ihm_geometric_object_sphere"].foreign_keys[(schema,"ihm_geometric_object_sphere_object_id_fkey")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })


# -- -----------------------------------------------------------------------------
def update_PDB_ihm_geometric_object_torus(model):
    schema = model.schemas["PDB"]
    table = schema.tables["ihm_geometric_object_torus"]
    # ----------------------------
    schema.tables["ihm_geometric_object_torus"].display.update(
        {'name' : 'Torus Geometric Objects', 'comment_display' : {'*': {'table_comment_display': 'inline'}}, }
    )

    # ----------------------------
    schema.tables["ihm_geometric_object_torus"].table_display.update({
        'row_name' : { 'row_markdown_pattern' : '{{{object_id}}}', },
    })

    # ----------------------------
    schema.tables["ihm_geometric_object_torus"].visible_columns.update({
        '*' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_geometric_object_torus_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_geometric_object_torus_object_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_geometric_object_list.object_id.',
                'markdown_name' : 'Object Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_geometric_object_torus_center_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_geometric_object_center.id.',
                'markdown_name' : 'Center Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_geometric_object_torus_transformation_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_geometric_object_transformation.id.',
                'markdown_name' : 'Transformation Id',
            },
            'major_radius_R', 
            'minor_radius_r', 
        ],
        'entry' :  [
            {
                'source' : [{'outbound': ['PDB', 'ihm_geometric_object_torus_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_geometric_object_torus_object_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_geometric_object_list.object_id.',
                'markdown_name' : 'Object Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_geometric_object_torus_center_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_geometric_object_center.id.',
                'markdown_name' : 'Center Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_geometric_object_torus_transformation_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_geometric_object_transformation.id.',
                'markdown_name' : 'Transformation Id',
            },
            'major_radius_R', 
            'minor_radius_r', 
        ],
        'detailed' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_geometric_object_torus_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_geometric_object_torus_object_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_geometric_object_list.object_id.',
                'markdown_name' : 'Object Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_geometric_object_torus_center_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_geometric_object_center.id.',
                'markdown_name' : 'Center Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_geometric_object_torus_transformation_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_geometric_object_transformation.id.',
                'markdown_name' : 'Transformation Id',
            },
            'major_radius_R', 
            'minor_radius_r', 
            ['PDB', 'ihm_geometric_object_torus_RCB_fkey'], 
            ['PDB', 'ihm_geometric_object_torus_RMB_fkey'], 
            'RCT', 
            'RMT', 
            ['PDB', 'ihm_geometric_object_torus_Owner_fkey'], 
        ],
    })

    # ----------------------------
    schema.tables["ihm_geometric_object_torus"].visible_foreign_keys.update({
        'filter' :  'detailed',
        'detailed' :  [
            ['PDB', 'ihm_geometric_object_half_torus_object_id_fkey'], 
        ],
    })

    # ----------------------------
    schema.tables["ihm_geometric_object_torus"].columns["minor_radius_r"].display.update(
        {'name' : 'Minor Radius r', }
    )

    # ----------------------------
    schema.tables["ihm_geometric_object_torus"].foreign_keys[(schema,"ihm_geometric_object_torus_transformation_id_fk")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })

    # ----------------------------
    schema.tables["ihm_geometric_object_torus"].foreign_keys[(schema,"ihm_geometric_object_torus_object_id_fkey")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })

    # ----------------------------
    schema.tables["ihm_geometric_object_torus"].foreign_keys[(schema,"ihm_geometric_object_torus_center_id_fkey")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })

    # ----------------------------
    schema.tables["ihm_geometric_object_torus"].foreign_keys[(schema,"ihm_geometric_object_torus_transformation_id_fkey")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })


# -- -----------------------------------------------------------------------------
def update_PDB_ihm_geometric_object_transformation(model):
    schema = model.schemas["PDB"]
    table = schema.tables["ihm_geometric_object_transformation"]
    # ----------------------------
    schema.tables["ihm_geometric_object_transformation"].display.update(
        {'name' : 'Geometric Object Transformations', 'comment_display' : {'*': {'table_comment_display': 'inline'}}, }
    )

    # ----------------------------
    schema.tables["ihm_geometric_object_transformation"].table_display.update({
        'row_name' : { 'row_markdown_pattern' : '{{{id}}}', },
    })

    # ----------------------------
    schema.tables["ihm_geometric_object_transformation"].visible_columns.update({
        '*' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_geometric_object_transformation_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'id', 
            'rot_matrix[1][1]', 
            'rot_matrix[1][2]', 
            'rot_matrix[1][3]', 
            'rot_matrix[2][1]', 
            'rot_matrix[2][2]', 
            'rot_matrix[2][3]', 
            'rot_matrix[3][1]', 
            'rot_matrix[3][2]', 
            'rot_matrix[3][3]', 
            'tr_vector[1]', 
            'tr_vector[2]', 
            'tr_vector[3]', 
        ],
        'entry' :  [
            {
                'source' : [{'outbound': ['PDB', 'ihm_geometric_object_transformation_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'id', 
            'rot_matrix[1][1]', 
            'rot_matrix[1][2]', 
            'rot_matrix[1][3]', 
            'rot_matrix[2][1]', 
            'rot_matrix[2][2]', 
            'rot_matrix[2][3]', 
            'rot_matrix[3][1]', 
            'rot_matrix[3][2]', 
            'rot_matrix[3][3]', 
            'tr_vector[1]', 
            'tr_vector[2]', 
            'tr_vector[3]', 
        ],
        'detailed' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_geometric_object_transformation_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'id', 
            'rot_matrix[1][1]', 
            'rot_matrix[1][2]', 
            'rot_matrix[1][3]', 
            'rot_matrix[2][1]', 
            'rot_matrix[2][2]', 
            'rot_matrix[2][3]', 
            'rot_matrix[3][1]', 
            'rot_matrix[3][2]', 
            'rot_matrix[3][3]', 
            'tr_vector[1]', 
            'tr_vector[2]', 
            'tr_vector[3]', 
            ['PDB', 'ihm_geometric_object_transformation_RCB_fkey'], 
            ['PDB', 'ihm_geometric_object_transformation_RMB_fkey'], 
            'RCT', 
            'RMT', 
            ['PDB', 'ihm_geometric_object_transformation_Owner_fkey'], 
        ],
    })

    # ----------------------------
    schema.tables["ihm_geometric_object_transformation"].visible_foreign_keys.update({
        'filter' :  'detailed',
        'detailed' :  [
            ['PDB', 'ihm_geometric_object_sphere_transformation_id_fkey'], 
            ['PDB', 'ihm_geometric_object_torus_transformation_id_fkey'], 
            ['PDB', 'ihm_geometric_object_axis_transformation_id_fkey'], 
            ['PDB', 'ihm_geometric_object_plane_transformation_id_fkey'], 
        ],
    })


# -- -----------------------------------------------------------------------------
def update_PDB_ihm_hdx_restraint(model):
    schema = model.schemas["PDB"]
    table = schema.tables["ihm_hdx_restraint"]
    # ----------------------------
    schema.tables["ihm_hdx_restraint"].display.update(
        {'name' : 'HD Exchange Restraints', 'comment_display' : {'*': {'table_comment_display': 'inline'}}, }
    )

    # ----------------------------
    schema.tables["ihm_hdx_restraint"].visible_columns.update({
        '*' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_hdx_restraint_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'id', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_hdx_restraint_ihm_feature_list_combo1_fkey']}, 'RID'],
                'comment' : 'An identifier for the peptide / residue feature',
                'markdown_name' : 'Feature Id',
            },
            'protection_factor', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_hdx_restraint_ihm_dataset_list_combo1_fkey']}, 'RID'],
                'comment' : 'Identifier to the H/D exchange input data from which the restraints are derived',
                'markdown_name' : 'Dataset List Id',
            },
            'details', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_hdx_restraint_Entry_Related_File_fkey']}, 'RID'],
                'comment' : 'A reference to the uploaded restraint file in the table Entry_Related_File.id.',
                'markdown_name' : 'Uploaded Restraint File',
            },
        ],
        'entry' :  [
            {
                'source' : [{'outbound': ['PDB', 'ihm_hdx_restraint_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'id', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_hdx_restraint_ihm_feature_list_combo1_fkey']}, 'RID'],
                'comment' : 'An identifier for the peptide / residue feature',
                'markdown_name' : 'Feature Id',
            },
            'protection_factor', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_hdx_restraint_ihm_dataset_list_combo1_fkey']}, 'RID'],
                'comment' : 'Identifier to the H/D exchange input data from which the restraints are derived',
                'markdown_name' : 'Dataset List Id',
            },
            'details', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_hdx_restraint_Entry_Related_File_fkey']}, 'RID'],
                'comment' : 'A reference to the uploaded restraint file in the table Entry_Related_File.id.',
                'markdown_name' : 'Uploaded Restraint File',
            },
        ],
        'detailed' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_hdx_restraint_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'id', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_hdx_restraint_ihm_feature_list_combo1_fkey']}, 'RID'],
                'comment' : 'An identifier for the peptide / residue feature',
                'markdown_name' : 'Feature Id',
            },
            'protection_factor', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_hdx_restraint_ihm_dataset_list_combo1_fkey']}, 'RID'],
                'comment' : 'Identifier to the H/D exchange input data from which the restraints are derived',
                'markdown_name' : 'Dataset List Id',
            },
            'details', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_hdx_restraint_Entry_Related_File_fkey']}, 'RID'],
                'comment' : 'A reference to the uploaded restraint file in the table Entry_Related_File.id.',
                'markdown_name' : 'Uploaded Restraint File',
            },
            ['PDB', 'ihm_hdx_restraint_RCB_fkey'], 
            ['PDB', 'ihm_hdx_restraint_RMB_fkey'], 
            'RCT', 
            'RMT', 
            ['PDB', 'ihm_hdx_restraint_Owner_fkey'], 
        ],
    })

    # ----------------------------
    schema.tables["ihm_hdx_restraint"].foreign_keys[(schema,"ihm_hdx_restraint_ihm_dataset_list_combo1_fkey")].foreign_key.update({
        'template_engine' :  'handlebars',
        'domain_filter_pattern' :  '{{#if _structure_id}}structure_id={{{_structure_id}}}{{/if}}',
    })

    # ----------------------------
    schema.tables["ihm_hdx_restraint"].foreign_keys[(schema,"ihm_hdx_restraint_ihm_feature_list_combo1_fkey")].foreign_key.update({
        'template_engine' :  'handlebars',
        'domain_filter_pattern' :  '{{#if _structure_id}}structure_id={{{_structure_id}}}{{/if}}',
    })


# -- -----------------------------------------------------------------------------
def update_PDB_ihm_hydroxyl_radical_fp_restraint(model):
    schema = model.schemas["PDB"]
    table = schema.tables["ihm_hydroxyl_radical_fp_restraint"]
    # ----------------------------
    schema.tables["ihm_hydroxyl_radical_fp_restraint"].display.update(
        {'name' : 'Hydroxyl Radical Footprinting Restraints', 'comment_display' : {'*': {'table_comment_display': 'inline'}}, }
    )
    
    # ----------------------------
    schema.tables["ihm_hydroxyl_radical_fp_restraint"].visible_columns.update({
        '*' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_hydroxyl_radical_fp_restraint_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'id', 
            'group_id', 
            'entity_description', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_hydroxyl_radical_fp_restraint_mm_poly_res_label_fkey']}, 'entity_id'],
                'comment' : 'A reference to table entity_poly_seq.entity_id',
                'markdown_name' : 'Entity Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_hydroxyl_radical_fp_restraint_asym_id_fkey']}, 'RID'],
                'comment' : 'A reference to table struct_asym.id.',
                'markdown_name' : 'Asym Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_hydroxyl_radical_fp_restraint_mm_poly_res_label_fkey']}, 'mon_id'],
                'comment' : 'A reference to table entity_poly_seq.mon_id',
                'markdown_name' : 'Component Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_hydroxyl_radical_fp_restraint_mm_poly_res_label_fkey']}, 'num'],
                'comment' : 'A reference to table entity_poly_seq.num.',
                'markdown_name' : 'Sequence Id',
            },
            'fp_rate', 
            'fp_rate_error', 
            'log_pf', 
            'log_pf_error', 
            'predicted_sasa', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_hydroxyl_radical_fp_restraint_software_id_fkey']}, 'RID'],
                'comment' : 'A reference to table software.pdbx_ordinal.',
                'markdown_name' : 'Software Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_hydroxyl_radical_fp_restraint_dataset_list_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_dataset_list.id.',
                'markdown_name' : 'Dataset List Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_hydroxyl_radical_fp_restraint_mm_poly_res_label_fkey']}, 'RID'],
                'comment' : 'Refers to a combination of Entity Id, Sequence Id and Component Id in the entity_poly_seq table.',
                'markdown_name' : 'Polymeric Residue',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_hydroxyl_radical_fp_restraint_Entry_Related_File_fkey']}, 'RID'],
                'comment' : 'A reference to the uploaded restraint file in the table Entry_Related_File.id.',
                'markdown_name' : 'Uploaded Restraint File',
            },
        ],
        'entry' :  [
            {
                'source' : [{'outbound': ['PDB', 'ihm_hydroxyl_radical_fp_restraint_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'id', 
            'group_id', 
            'entity_description', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_hydroxyl_radical_fp_restraint_mm_poly_res_label_fkey']}, 'entity_id'],
                'comment' : 'A reference to table entity_poly_seq.entity_id',
                'markdown_name' : 'Entity Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_hydroxyl_radical_fp_restraint_asym_id_fkey']}, 'RID'],
                'comment' : 'A reference to table struct_asym.id.',
                'markdown_name' : 'Asym Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_hydroxyl_radical_fp_restraint_mm_poly_res_label_fkey']}, 'mon_id'],
                'comment' : 'A reference to table entity_poly_seq.mon_id',
                'markdown_name' : 'Component Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_hydroxyl_radical_fp_restraint_mm_poly_res_label_fkey']}, 'num'],
                'comment' : 'A reference to table entity_poly_seq.num.',
                'markdown_name' : 'Sequence Id',
            },
            'fp_rate', 
            'fp_rate_error', 
            'log_pf', 
            'log_pf_error', 
            'predicted_sasa', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_hydroxyl_radical_fp_restraint_software_id_fkey']}, 'RID'],
                'comment' : 'A reference to table software.pdbx_ordinal.',
                'markdown_name' : 'Software Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_hydroxyl_radical_fp_restraint_dataset_list_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_dataset_list.id.',
                'markdown_name' : 'Dataset List Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_hydroxyl_radical_fp_restraint_mm_poly_res_label_fkey']}, 'RID'],
                'comment' : 'Refers to a combination of Entity Id, Sequence Id and Component Id in the entity_poly_seq table.',
                'markdown_name' : 'Polymeric Residue',
            },
        ],
        'detailed' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_hydroxyl_radical_fp_restraint_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'id', 
            'group_id', 
            'entity_description', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_hydroxyl_radical_fp_restraint_mm_poly_res_label_fkey']}, 'entity_id'],
                'comment' : 'A reference to table entity_poly_seq.entity_id',
                'markdown_name' : 'Entity Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_hydroxyl_radical_fp_restraint_asym_id_fkey']}, 'RID'],
                'comment' : 'A reference to table struct_asym.id.',
                'markdown_name' : 'Asym Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_hydroxyl_radical_fp_restraint_mm_poly_res_label_fkey']}, 'mon_id'],
                'comment' : 'A reference to table entity_poly_seq.mon_id',
                'markdown_name' : 'Component Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_hydroxyl_radical_fp_restraint_mm_poly_res_label_fkey']}, 'num'],
                'comment' : 'A reference to table entity_poly_seq.num.',
                'markdown_name' : 'Sequence Id',
            },
            'fp_rate', 
            'fp_rate_error', 
            'log_pf', 
            'log_pf_error', 
            'predicted_sasa', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_hydroxyl_radical_fp_restraint_software_id_fkey']}, 'RID'],
                'comment' : 'A reference to table software.pdbx_ordinal.',
                'markdown_name' : 'Software Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_hydroxyl_radical_fp_restraint_dataset_list_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_dataset_list.id.',
                'markdown_name' : 'Dataset List Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_hydroxyl_radical_fp_restraint_mm_poly_res_label_fkey']}, 'RID'],
                'comment' : 'Refers to a combination of Entity Id, Sequence Id and Component Id in the entity_poly_seq table.',
                'markdown_name' : 'Polymeric Residue',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_hydroxyl_radical_fp_restraint_Entry_Related_File_fkey']}, 'RID'],
                'comment' : 'A reference to the uploaded restraint file in the table Entry_Related_File.id.',
                'markdown_name' : 'Uploaded Restraint File',
            },
            ['PDB', 'ihm_hydroxyl_radical_fp_restraint_RCB_fkey'], 
            ['PDB', 'ihm_hydroxyl_radical_fp_restraint_RMB_fkey'], 
            'RCT', 
            'RMT', 
            ['PDB', 'ihm_hydroxyl_radical_fp_restraint_Owner_fkey'], 
        ],
    })

    # ----------------------------
    schema.tables["ihm_hydroxyl_radical_fp_restraint"].columns["fp_rate"].display.update(
        {'name' : 'FP Rate', }
    )
    
    # ----------------------------
    schema.tables["ihm_hydroxyl_radical_fp_restraint"].columns["fp_rate_error"].display.update(
        {'name' : 'FP Rate Error', }
    )

    # ----------------------------
    schema.tables["ihm_hydroxyl_radical_fp_restraint"].columns["log_pf"].display.update(
        {'name' : 'Log PF', }
    )
    
    # ----------------------------
    schema.tables["ihm_hydroxyl_radical_fp_restraint"].columns["log_pf_error"].display.update(
        {'name' : 'Log PF Error', }
    )

    # ----------------------------
    schema.tables["ihm_hydroxyl_radical_fp_restraint"].columns["predicted_sasa"].display.update(
        {'name' : 'Predicted SASA', }
    )
    
    # ----------------------------
    schema.tables["ihm_hydroxyl_radical_fp_restraint"].foreign_keys[(schema,"ihm_hydroxyl_radical_fp_restraint_mm_poly_res_label_fkey")].foreign_key.update({
        'template_engine' :  'handlebars',
        'domain_filter_pattern' :  '{{#if _structure_id}}structure_id={{{_structure_id}}}{{/if}}',
    })

    # ----------------------------
    schema.tables["ihm_hydroxyl_radical_fp_restraint"].foreign_keys[(schema,"ihm_hydroxyl_radical_fp_restraint_dataset_list_id_fkey")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })

    # ----------------------------
    schema.tables["ihm_hydroxyl_radical_fp_restraint"].foreign_keys[(schema,"ihm_hydroxyl_radical_fp_restraint_asym_id_fkey")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })

    # ----------------------------
    schema.tables["ihm_hydroxyl_radical_fp_restraint"].foreign_keys[(schema,"ihm_hydroxyl_radical_fp_restraint_software_id_fk")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })

    # ----------------------------
    schema.tables["ihm_hydroxyl_radical_fp_restraint"].foreign_keys[(schema,"ihm_hydroxyl_radical_fp_restraint_software_id_fkey")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })



# -- -----------------------------------------------------------------------------
def update_PDB_ihm_interface_residue_feature(model):
    schema = model.schemas["PDB"]
    table = schema.tables["ihm_interface_residue_feature"]
    # ----------------------------
    schema.tables["ihm_interface_residue_feature"].display.update(
        {'name' : 'Molecular Features - Interface Residues', 'comment_display' : {'*': {'table_comment_display': 'inline'}}, }
    )

    # ----------------------------
    schema.tables["ihm_interface_residue_feature"].visible_columns.update({
        '*' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_interface_residue_feature_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'ordinal_id', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_interface_residue_feature_feature_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_feature_list.feature_id.',
                'markdown_name' : 'Feature Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_interface_residue_feature_binding_partner_entity_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entity.id.',
                'markdown_name' : 'Binding Partner Entity Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_interface_residue_feature_binding_partner_asym_id_fkey']}, 'RID'],
                'comment' : 'A reference to table struct_asym.id.',
                'markdown_name' : 'Binding Partner Asym Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_interface_residue_feature_dataset_list_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_dataset_list.id.',
                'markdown_name' : 'Dataset List Id',
            },
            'details', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_interface_residue_feature_Entry_Related_File_fkey']}, 'RID'],
                'comment' : 'A reference to the uploaded restraint file in the table Entry_Related_File.id.',
                'markdown_name' : 'Uploaded Restraint File',
            },
        ],
        'entry' :  [
            {
                'source' : [{'outbound': ['PDB', 'ihm_interface_residue_feature_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'ordinal_id', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_interface_residue_feature_feature_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_feature_list.feature_id.',
                'markdown_name' : 'Feature Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_interface_residue_feature_binding_partner_entity_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entity.id.',
                'markdown_name' : 'Binding Partner Entity Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_interface_residue_feature_binding_partner_asym_id_fkey']}, 'RID'],
                'comment' : 'A reference to table struct_asym.id.',
                'markdown_name' : 'Binding Partner Asym Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_interface_residue_feature_dataset_list_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_dataset_list.id.',
                'markdown_name' : 'Dataset List Id',
            },
            'details', 
        ],
        'detailed' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_interface_residue_feature_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'ordinal_id', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_interface_residue_feature_feature_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_feature_list.feature_id.',
                'markdown_name' : 'Feature Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_interface_residue_feature_binding_partner_entity_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entity.id.',
                'markdown_name' : 'Binding Partner Entity Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_interface_residue_feature_binding_partner_asym_id_fkey']}, 'RID'],
                'comment' : 'A reference to table struct_asym.id.',
                'markdown_name' : 'Binding Partner Asym Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_interface_residue_feature_dataset_list_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_dataset_list.id.',
                'markdown_name' : 'Dataset List Id',
            },
            'details', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_interface_residue_feature_Entry_Related_File_fkey']}, 'RID'],
                'comment' : 'A reference to the uploaded restraint file in the table Entry_Related_File.id.',
                'markdown_name' : 'Uploaded Restraint File',
            },
            ['PDB', 'ihm_interface_residue_feature_RCB_fkey'], 
            ['PDB', 'ihm_interface_residue_feature_RMB_fkey'], 
            'RCT', 
            'RMT', 
            ['PDB', 'ihm_interface_residue_feature_Owner_fkey'], 
        ],
    })

    # ----------------------------
    schema.tables["ihm_interface_residue_feature"].foreign_keys[(schema,"ihm_interface_residue_feature_binding_partner_asym_id_fkey")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })

    # ----------------------------
    schema.tables["ihm_interface_residue_feature"].foreign_keys[(schema,"ihm_interface_residue_feature_binding_partner_entity_id_fkey")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })

    # ----------------------------
    schema.tables["ihm_interface_residue_feature"].foreign_keys[(schema,"ihm_interface_residue_feature_binding_partner_asym_id_fk")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })

    # ----------------------------
    schema.tables["ihm_interface_residue_feature"].foreign_keys[(schema,"ihm_interface_residue_feature_feature_id_fkey")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })

    # ----------------------------
    schema.tables["ihm_interface_residue_feature"].foreign_keys[(schema,"ihm_interface_residue_feature_dataset_list_id_fkey")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })


# -- -----------------------------------------------------------------------------
def update_PDB_ihm_kinetic_rate(model):
    schema = model.schemas["PDB"]
    table = schema.tables["ihm_kinetic_rate"]
    # ----------------------------
    schema.tables["ihm_kinetic_rate"].display.update(
        {'name' : 'Kinetic Rates from Biophysical Experiments', 'comment_display' : {'*': {'table_comment_display': 'inline'}}, }
    )

    # ----------------------------
    schema.tables["ihm_kinetic_rate"].visible_columns.update({
        '*' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_kinetic_rate_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'id', 
            'transition_rate_constant', 
            'equilibrium_constant', 
            ['PDB', 'ihm_equilibrium_constant_determination_method_fkey'], 
            'equilibrium_constant_unit', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_kinetic_rate_multi_state_scheme_connectivity_combo1_fkey']}, 'RID'],
                'comment' : 'Identifier for the multi-state scheme connectivity',
                'markdown_name' : 'Scheme Connectivity Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_kinetic_rate_ihm_external_files_combo2_fkey']}, 'RID'],
                'comment' : 'Identifier for the external file corresponding to the kinetic rate measurement',
                'markdown_name' : 'External File Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_kinetic_rate_ihm_dataset_group_combo1_fkey']}, 'RID'],
                'comment' : 'Identifier for the dataset group from which the kinetic rate is obtained',
                'markdown_name' : 'Dataset Group Id',
            },
            'details', 
        ],
        'entry' :  [
            {
                'source' : [{'outbound': ['PDB', 'ihm_kinetic_rate_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'id', 
            'transition_rate_constant', 
            'equilibrium_constant', 
            ['PDB', 'ihm_equilibrium_constant_determination_method_fkey'], 
            'equilibrium_constant_unit', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_kinetic_rate_multi_state_scheme_connectivity_combo1_fkey']}, 'RID'],
                'comment' : 'Identifier for the multi-state scheme connectivity',
                'markdown_name' : 'Scheme Connectivity Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_kinetic_rate_ihm_external_files_combo2_fkey']}, 'RID'],
                'comment' : 'Identifier for the external file corresponding to the kinetic rate measurement',
                'markdown_name' : 'External File Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_kinetic_rate_ihm_dataset_group_combo1_fkey']}, 'RID'],
                'comment' : 'Identifier for the dataset group from which the kinetic rate is obtained',
                'markdown_name' : 'Dataset Group Id',
            },
            'details', 
        ],
        'detailed' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_kinetic_rate_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'id', 
            'transition_rate_constant', 
            'equilibrium_constant', 
            ['PDB', 'ihm_equilibrium_constant_determination_method_fkey'], 
            'equilibrium_constant_unit', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_kinetic_rate_multi_state_scheme_connectivity_combo1_fkey']}, 'RID'],
                'comment' : 'Identifier for the multi-state scheme connectivity',
                'markdown_name' : 'Scheme Connectivity Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_kinetic_rate_ihm_external_files_combo2_fkey']}, 'RID'],
                'comment' : 'Identifier for the external file corresponding to the kinetic rate measurement',
                'markdown_name' : 'External File Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_kinetic_rate_ihm_dataset_group_combo1_fkey']}, 'RID'],
                'comment' : 'Identifier for the dataset group from which the kinetic rate is obtained',
                'markdown_name' : 'Dataset Group Id',
            },
            'details', 
            ['PDB', 'ihm_kinetic_rate_RCB_fkey'], 
            ['PDB', 'ihm_kinetic_rate_RMB_fkey'], 
            'RCT', 
            'RMT', 
            ['PDB', 'ihm_kinetic_rate_Owner_fkey'], 
        ],
    })
    
    # ----------------------------
    schema.tables["ihm_kinetic_rate"].foreign_keys[(schema,"ihm_kinetic_rate_ihm_external_files_combo2_fkey")].foreign_key.update({
        'template_engine' :  'handlebars',
        'domain_filter_pattern' :  '{{#if _structure_id}}structure_id={{{_structure_id}}}{{/if}}',
    })

    # ----------------------------
    schema.tables["ihm_kinetic_rate"].foreign_keys[(schema,"ihm_kinetic_rate_multi_state_scheme_connectivity_combo1_fkey")].foreign_key.update({
        'template_engine' :  'handlebars',
        'domain_filter_pattern' :  '{{#if _structure_id}}structure_id={{{_structure_id}}}{{/if}}',
    })

    # ----------------------------
    schema.tables["ihm_kinetic_rate"].foreign_keys[(schema,"ihm_kinetic_rate_ihm_dataset_group_combo1_fkey")].foreign_key.update({
        'template_engine' :  'handlebars',
        'domain_filter_pattern' :  '{{#if _structure_id}}structure_id={{{_structure_id}}}{{/if}}',
    })

# -- -----------------------------------------------------------------------------
def update_PDB_ihm_ligand_probe(model):
    schema = model.schemas["PDB"]
    table = schema.tables["ihm_ligand_probe"]
    # ----------------------------
    schema.tables["ihm_ligand_probe"].display.update(
        {'name' : 'Non-polymeric Entity Probes', 'comment_display' : {'*': {'table_comment_display': 'inline'}}, }
    )

    # ----------------------------
    schema.tables["ihm_ligand_probe"].visible_columns.update({
        '*' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_ligand_probe_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_ligand_probe_probe_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_probe_list.probe_id.',
                'markdown_name' : 'Probe Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_ligand_probe_entity_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entity.id.',
                'markdown_name' : 'Entity Id',
            },
            'details', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_ligand_probe_dataset_list_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_dataset_list.id.',
                'markdown_name' : 'Dataset List Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_ligand_probe_Entry_Related_File_fkey']}, 'RID'],
                'comment' : 'A reference to the uploaded restraint file in the table Entry_Related_File.id.',
                'markdown_name' : 'Uploaded Restraint File',
            },
        ],
        'entry' :  [
            {
                'source' : [{'outbound': ['PDB', 'ihm_ligand_probe_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_ligand_probe_probe_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_probe_list.probe_id.',
                'markdown_name' : 'Probe Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_ligand_probe_entity_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entity.id.',
                'markdown_name' : 'Entity Id',
            },
            'details', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_ligand_probe_dataset_list_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_dataset_list.id.',
                'markdown_name' : 'Dataset List Id',
            },
        ],
        'detailed' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_ligand_probe_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_ligand_probe_probe_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_probe_list.probe_id.',
                'markdown_name' : 'Probe Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_ligand_probe_entity_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entity.id.',
                'markdown_name' : 'Entity Id',
            },
            'details', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_ligand_probe_dataset_list_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_dataset_list.id.',
                'markdown_name' : 'Dataset List Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_ligand_probe_Entry_Related_File_fkey']}, 'RID'],
                'comment' : 'A reference to the uploaded restraint file in the table Entry_Related_File.id.',
                'markdown_name' : 'Uploaded Restraint File',
            },
            ['PDB', 'ihm_ligand_probe_RCB_fkey'], 
            ['PDB', 'ihm_ligand_probe_RMB_fkey'], 
            'RCT', 
            'RMT', 
            ['PDB', 'ihm_ligand_probe_Owner_fkey'], 
        ],
    })

    # ----------------------------
    schema.tables["ihm_ligand_probe"].foreign_keys[(schema,"ihm_ligand_probe_dataset_list_id_fkey")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })

    # ----------------------------
    schema.tables["ihm_ligand_probe"].foreign_keys[(schema,"ihm_ligand_probe_probe_id_fkey")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })

    # ----------------------------
    schema.tables["ihm_ligand_probe"].foreign_keys[(schema,"ihm_ligand_probe_entity_id_fkey")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })


# -- -----------------------------------------------------------------------------
def update_PDB_ihm_localization_density_files(model):
    schema = model.schemas["PDB"]
    table = schema.tables["ihm_localization_density_files"]
    # ----------------------------
    schema.tables["ihm_localization_density_files"].display.update(
        {'name' : 'Localization Density Files', 'comment_display' : {'*': {'table_comment_display': 'inline'}}, }
    )

    # ----------------------------
    schema.tables["ihm_localization_density_files"].visible_columns.update({
        '*' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_localization_density_files_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'id', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_localization_density_files_file_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_external_files.id.',
                'markdown_name' : 'File Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_localization_density_files_ensemble_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_ensemble_info.ensemble_id.',
                'markdown_name' : 'Ensemble Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_localization_density_files_entity_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entity.id.',
                'markdown_name' : 'Entity Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_localization_density_files_asym_id_fkey']}, 'RID'],
                'comment' : 'A reference to table struct_asym.id.',
                'markdown_name' : 'Asym Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_localization_density_files_entity_poly_segment_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_entity_poly_segment.id.',
                'markdown_name' : 'Entity Poly Segment Id',
            },
        ],
        'entry' :  [
            {
                'source' : [{'outbound': ['PDB', 'ihm_localization_density_files_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'id', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_localization_density_files_file_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_external_files.id.',
                'markdown_name' : 'File Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_localization_density_files_ensemble_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_ensemble_info.ensemble_id.',
                'markdown_name' : 'Ensemble Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_localization_density_files_entity_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entity.id.',
                'markdown_name' : 'Entity Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_localization_density_files_asym_id_fkey']}, 'RID'],
                'comment' : 'A reference to table struct_asym.id.',
                'markdown_name' : 'Asym Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_localization_density_files_entity_poly_segment_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_entity_poly_segment.id.',
                'markdown_name' : 'Entity Poly Segment Id',
            },
        ],
        'detailed' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_localization_density_files_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'id', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_localization_density_files_file_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_external_files.id.',
                'markdown_name' : 'File Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_localization_density_files_ensemble_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_ensemble_info.ensemble_id.',
                'markdown_name' : 'Ensemble Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_localization_density_files_entity_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entity.id.',
                'markdown_name' : 'Entity Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_localization_density_files_asym_id_fkey']}, 'RID'],
                'comment' : 'A reference to table struct_asym.id.',
                'markdown_name' : 'Asym Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_localization_density_files_entity_poly_segment_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_entity_poly_segment.id.',
                'markdown_name' : 'Entity Poly Segment Id',
            },
            ['PDB', 'ihm_localization_density_files_RCB_fkey'], 
            ['PDB', 'ihm_localization_density_files_RMB_fkey'], 
            'RCT', 
            'RMT', 
            ['PDB', 'ihm_localization_density_files_Owner_fkey'], 
        ],
    })

    # ----------------------------
    schema.tables["ihm_localization_density_files"].foreign_keys[(schema,"ihm_localization_density_files_entity_id_fk")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })

    # ----------------------------
    schema.tables["ihm_localization_density_files"].foreign_keys[(schema,"ihm_localization_density_files_ensemble_id_fkey")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })

    # ----------------------------
    schema.tables["ihm_localization_density_files"].foreign_keys[(schema,"ihm_localization_density_files_entity_id_fkey")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })

    # ----------------------------
    schema.tables["ihm_localization_density_files"].foreign_keys[(schema,"ihm_localization_density_files_entity_poly_segment_id_fkey")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })

    # ----------------------------
    schema.tables["ihm_localization_density_files"].foreign_keys[(schema,"ihm_localization_density_files_asym_id_fk")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })

    # ----------------------------
    schema.tables["ihm_localization_density_files"].foreign_keys[(schema,"ihm_localization_density_files_asym_id_fkey")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })

    # ----------------------------
    schema.tables["ihm_localization_density_files"].foreign_keys[(schema,"ihm_localization_density_files_file_id_fkey")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })

    # ----------------------------
    schema.tables["ihm_localization_density_files"].foreign_keys[(schema,"ihm_localization_density_files_entity_poly_segment_id_fk")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })


# -- -----------------------------------------------------------------------------
def update_PDB_ihm_model_group(model):
    schema = model.schemas["PDB"]
    table = schema.tables["ihm_model_group"]
    # ----------------------------
    schema.tables["ihm_model_group"].display.update(
        {'markdown_name' : 'Model Groups^*^', 'comment_display' : {'*': {'table_comment_display': 'inline'}}, }
    )

    # ----------------------------
    schema.tables["ihm_model_group"].table_display.update({
            'row_name' : { 'row_markdown_pattern' : '{{{id}}}', },
    })

    # ----------------------------
    schema.tables["ihm_model_group"].visible_columns.update({
        '*' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_model_group_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'id', 
            'name', 
            'details', 
        ],
        'entry' :  [
            {
                'source' : [{'outbound': ['PDB', 'ihm_model_group_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'id', 
            'name', 
            'details', 
        ],
        'detailed' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_model_group_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'id', 
            'name', 
            'details', 
            ['PDB', 'ihm_model_group_RCB_fkey'], 
            ['PDB', 'ihm_model_group_RMB_fkey'], 
            'RCT', 
            'RMT', 
            ['PDB', 'ihm_model_group_Owner_fkey'], 
        ],
    })

    # ----------------------------
    schema.tables["ihm_model_group"].visible_foreign_keys.update({
        'filter' :  'detailed',
        'detailed' :  [
            ['PDB', 'ihm_model_group_link_group_id_fkey'], 
            ['PDB', 'ihm_model_representative_model_group_id_fkey'], 
            ['PDB', 'ihm_multi_state_model_group_link_model_group_id_fkey'], 
            ['PDB', 'ihm_ordered_model_ihm_model_group_begin_combo1_fkey'], 
            ['PDB', 'ihm_ordered_ensemble_model_group_id_begin_fkey'], 
            ['PDB', 'ihm_ensemble_info_model_group_id_fkey'], 
            ['PDB', 'ihm_ensemble_sub_sample_ihm_model_group_combo2_fkey'], 
        ],
    })


# -- -----------------------------------------------------------------------------
def update_PDB_ihm_model_group_link(model):
    schema = model.schemas["PDB"]
    table = schema.tables["ihm_model_group_link"]
    # ----------------------------
    schema.tables["ihm_model_group_link"].display.update(
        {'markdown_name' : 'Models Belonging to Groups^*^', 'comment_display' : {'*': {'table_comment_display': 'inline'}}, }
    )

    # ----------------------------
    schema.tables["ihm_model_group_link"].visible_columns.update({
        '*' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_model_group_link_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_model_group_link_model_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_model_list.model_id.',
                'markdown_name' : 'Model Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_model_group_link_group_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_model_group.id.',
                'markdown_name' : 'Group Id',
            },
        ],
        'entry' :  [
            {
                'source' : [{'outbound': ['PDB', 'ihm_model_group_link_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_model_group_link_model_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_model_list.model_id.',
                'markdown_name' : 'Model Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_model_group_link_group_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_model_group.id.',
                'markdown_name' : 'Group Id',
            },
        ],
        'detailed' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_model_group_link_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_model_group_link_model_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_model_list.model_id.',
                'markdown_name' : 'Model Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_model_group_link_group_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_model_group.id.',
                'markdown_name' : 'Group Id',
            },
            ['PDB', 'ihm_model_group_link_RCB_fkey'], 
            ['PDB', 'ihm_model_group_link_RMB_fkey'], 
            'RCT', 
            'RMT', 
            ['PDB', 'ihm_model_group_link_Owner_fkey'], 
        ],
    })

    # ----------------------------
    schema.tables["ihm_model_group_link"].foreign_keys[(schema,"ihm_model_group_link_model_id_fkey")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })

    # ----------------------------
    schema.tables["ihm_model_group_link"].foreign_keys[(schema,"ihm_model_group_link_group_id_fkey")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })


# -- -----------------------------------------------------------------------------
def update_PDB_ihm_model_list(model):
    schema = model.schemas["PDB"]
    table = schema.tables["ihm_model_list"]
    # ----------------------------
    schema.tables["ihm_model_list"].display.update(
        {'markdown_name' : 'Models Submitted^*^', 'comment_display' : {'*': {'table_comment_display': 'inline'}}, }
    )
    
    # ----------------------------
    schema.tables["ihm_model_list"].table_display.update({
        'row_name' : { 'row_markdown_pattern' : '{{{model_id}}}', },
    })

    # ----------------------------
    schema.tables["ihm_model_list"].visible_columns.update({
        '*' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_model_list_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'model_id', 
            'model_name', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_model_list_assembly_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_struct_assembly.id.',
                'markdown_name' : 'Assembly Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_model_list_protocol_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_modeling_protocol.id.',
                'markdown_name' : 'Protocol Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_model_list_representation_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_model_representation.id.',
                'markdown_name' : 'Representation Id',
            },
        ],
        'entry' :  [
            {
                'source' : [{'outbound': ['PDB', 'ihm_model_list_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'model_id', 
            'model_name', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_model_list_assembly_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_struct_assembly.id.',
                'markdown_name' : 'Assembly Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_model_list_protocol_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_modeling_protocol.id.',
                'markdown_name' : 'Protocol Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_model_list_representation_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_model_representation.id.',
                'markdown_name' : 'Representation Id',
            },
        ],
        'detailed' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_model_list_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'model_id', 
            'model_name', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_model_list_assembly_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_struct_assembly.id.',
                'markdown_name' : 'Assembly Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_model_list_protocol_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_modeling_protocol.id.',
                'markdown_name' : 'Protocol Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_model_list_representation_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_model_representation.id.',
                'markdown_name' : 'Representation Id',
            },
            ['PDB', 'ihm_model_list_RCB_fkey'], 
            ['PDB', 'ihm_model_list_RMB_fkey'], 
            'RCT', 
            'RMT', 
            ['PDB', 'ihm_model_list_Owner_fkey'], 
        ],
    })

    # ----------------------------
    schema.tables["ihm_model_list"].visible_foreign_keys.update({
        'filter' :  'detailed',
        'detailed' :  [
            ['PDB', 'ihm_model_group_link_model_id_fkey'], 
            ['PDB', 'ihm_model_representative_model_id_fkey'], 
            ['PDB', 'ihm_residues_not_modeled_model_id_fkey'], 
            ['PDB', 'ihm_cross_link_result_parameters_model_id_fkey'], 
            ['PDB', 'ihm_2dem_class_average_fitting_model_id_fkey'], 
            ['PDB', 'ihm_3dem_restraint_model_id_fkey'], 
            ['PDB', 'ihm_sas_restraint_model_id_fkey'], 
            ['PDB', 'ihm_epr_restraint_model_id_fkey'], 
            ['PDB', 'ihm_cross_link_pseudo_site_ihm_model_list_combo2_fkey'], 
        ],
    })

    # ----------------------------
    schema.tables["ihm_model_list"].foreign_keys[(schema,"ihm_model_list_representation_id_fkey")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })

    # ----------------------------
    schema.tables["ihm_model_list"].foreign_keys[(schema,"ihm_model_list_assembly_id_fkey")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })

    # ----------------------------
    schema.tables["ihm_model_list"].foreign_keys[(schema,"ihm_model_list_protocol_id_fkey")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })


# -- -----------------------------------------------------------------------------
def update_PDB_ihm_model_representation(model):
    schema = model.schemas["PDB"]
    table = schema.tables["ihm_model_representation"]
    # ----------------------------
    schema.tables["ihm_model_representation"].display.update(
        {'markdown_name' : 'Model Representations^*^', 'comment_display' : {'*': {'table_comment_display': 'inline'}}, }
    )

    # ----------------------------
    schema.tables["ihm_model_representation"].table_display.update({
        'row_name' : { 'row_markdown_pattern' : '{{{id}}}', },
    })

    # ----------------------------
    schema.tables["ihm_model_representation"].visible_columns.update({
        '*' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_model_representation_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'id', 
            'name', 
            'details', 
        ],
        'entry' :  [
            {
                'source' : [{'outbound': ['PDB', 'ihm_model_representation_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'id', 
            'name', 
            'details', 
        ],
        'detailed' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_model_representation_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'id', 
            'name', 
            'details', 
            ['PDB', 'ihm_model_representation_RCB_fkey'], 
            ['PDB', 'ihm_model_representation_RMB_fkey'], 
            'RCT', 
            'RMT', 
            ['PDB', 'ihm_model_representation_Owner_fkey'], 
        ],
    })

    # ----------------------------
    schema.tables["ihm_model_representation"].visible_foreign_keys.update({
        'filter' :  'detailed',
        'detailed' :  [
            ['PDB', 'ihm_model_representation_details_representation_id_fkey'], 
            ['PDB', 'ihm_model_list_representation_id_fkey'], 
        ],
    })

# -- -----------------------------------------------------------------------------
def update_PDB_ihm_model_representation_details(model):
    schema = model.schemas["PDB"]
    table = schema.tables["ihm_model_representation_details"]
    # ----------------------------
    schema.tables["ihm_model_representation_details"].display.update(
        {'markdown_name' : 'Details of Model Representations^*^', 'comment_display' : {'*': {'table_comment_display': 'inline'}}, }
    )

    # ----------------------------
    schema.tables["ihm_model_representation_details"].visible_columns.update({
        '*' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_model_representation_details_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'id', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_model_representation_details_representation_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_model_representation.id.',
                'markdown_name' : 'Representation Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_model_representation_details_entity_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entity.id.',
                'markdown_name' : 'Entity Id',
            },
            'entity_description', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_model_representation_details_entity_asym_id_fkey']}, 'RID'],
                'comment' : 'A reference to table struct_asym.id.',
                'markdown_name' : 'Entity Asym Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_model_representation_details_entity_poly_segment_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_entity_poly_segment.id.',
                'markdown_name' : 'Entity Poly Segment Id',
            },
            ['PDB', 'ihm_model_representation_details_model_granularity_fkey'], 
            ['PDB', 'ihm_model_representation_details_model_mode_fkey'], 
            'model_object_count', 
            ['PDB', 'model_representation_details_model_object_primitive_fkey'], 
            {
                'source' : [{'outbound': ['PDB', 'ihm_model_representation_details_starting_model_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_starting_model_details.starting_model_id.',
                'markdown_name' : 'Starting Model Id',
            },
            'description', 
        ],
        'entry' :  [
            {
                'source' : [{'outbound': ['PDB', 'ihm_model_representation_details_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'id', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_model_representation_details_representation_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_model_representation.id.',
                'markdown_name' : 'Representation Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_model_representation_details_entity_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entity.id.',
                'markdown_name' : 'Entity Id',
            },
            'entity_description', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_model_representation_details_entity_asym_id_fkey']}, 'RID'],
                'comment' : 'A reference to table struct_asym.id.',
                'markdown_name' : 'Entity Asym Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_model_representation_details_entity_poly_segment_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_entity_poly_segment.id.',
                'markdown_name' : 'Entity Poly Segment Id',
            },
            ['PDB', 'ihm_model_representation_details_model_granularity_fkey'], 
            ['PDB', 'ihm_model_representation_details_model_mode_fkey'], 
            'model_object_count', 
            ['PDB', 'model_representation_details_model_object_primitive_fkey'], 
            {
                'source' : [{'outbound': ['PDB', 'ihm_model_representation_details_starting_model_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_starting_model_details.starting_model_id.',
                'markdown_name' : 'Starting Model Id',
            },
            'description', 
        ],
        'detailed' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_model_representation_details_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'id', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_model_representation_details_representation_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_model_representation.id.',
                'markdown_name' : 'Representation Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_model_representation_details_entity_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entity.id.',
                'markdown_name' : 'Entity Id',
            },
            'entity_description', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_model_representation_details_entity_asym_id_fkey']}, 'RID'],
                'comment' : 'A reference to table struct_asym.id.',
                'markdown_name' : 'Entity Asym Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_model_representation_details_entity_poly_segment_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_entity_poly_segment.id.',
                'markdown_name' : 'Entity Poly Segment Id',
            },
            ['PDB', 'ihm_model_representation_details_model_granularity_fkey'], 
            ['PDB', 'ihm_model_representation_details_model_mode_fkey'], 
            'model_object_count', 
            ['PDB', 'model_representation_details_model_object_primitive_fkey'], 
            {
                'source' : [{'outbound': ['PDB', 'ihm_model_representation_details_starting_model_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_starting_model_details.starting_model_id.',
                'markdown_name' : 'Starting Model Id',
            },
            'description', 
            ['PDB', 'ihm_model_representation_details_RCB_fkey'], 
            ['PDB', 'ihm_model_representation_details_RMB_fkey'], 
            'RCT', 
            'RMT', 
            ['PDB', 'ihm_model_representation_details_Owner_fkey'], 
        ],
    })

    # ----------------------------
    schema.tables["ihm_model_representation_details"].foreign_keys[(schema,"ihm_model_representation_details_representation_id_fkey")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })

    # ----------------------------
    schema.tables["ihm_model_representation_details"].foreign_keys[(schema,"ihm_model_representation_details_starting_model_id_fk")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })

    # ----------------------------
    schema.tables["ihm_model_representation_details"].foreign_keys[(schema,"ihm_model_representation_details_entity_asym_id_fkey")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })

    # ----------------------------
    schema.tables["ihm_model_representation_details"].foreign_keys[(schema,"ihm_model_representation_details_entity_poly_segment_id_fk")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })

    # ----------------------------
    schema.tables["ihm_model_representation_details"].foreign_keys[(schema,"ihm_model_representation_details_entity_id_fkey")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })

    # ----------------------------
    schema.tables["ihm_model_representation_details"].foreign_keys[(schema,"ihm_model_representation_details_starting_model_id_fkey")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })

    # ----------------------------
    schema.tables["ihm_model_representation_details"].foreign_keys[(schema,"ihm_model_representation_details_entity_poly_segment_id_fkey")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })


# -- -----------------------------------------------------------------------------
def update_PDB_ihm_model_representative(model):
    schema = model.schemas["PDB"]
    table = schema.tables["ihm_model_representative"]
    # ----------------------------
    schema.tables["ihm_model_representative"].display.update(
        {'name' : 'Representative Model in an Ensemble', 'comment_display' : {'*': {'table_comment_display': 'inline'}}, }
    )

    # ----------------------------
    schema.tables["ihm_model_representative"].visible_columns.update({
        '*' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_model_representative_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'id', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_model_representative_model_group_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_model_group.id.',
                'markdown_name' : 'Model Group Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_model_representative_model_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_model_list.model_id.',
                'markdown_name' : 'Model Id',
            },
            ['PDB', 'ihm_model_representative_selection_criteria_fkey'], 
        ],
        'entry' :  [
            {
                'source' : [{'outbound': ['PDB', 'ihm_model_representative_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'id', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_model_representative_model_group_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_model_group.id.',
                'markdown_name' : 'Model Group Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_model_representative_model_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_model_list.model_id.',
                'markdown_name' : 'Model Id',
            },
            ['PDB', 'ihm_model_representative_selection_criteria_fkey'], 
        ],
        'detailed' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_model_representative_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'id', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_model_representative_model_group_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_model_group.id.',
                'markdown_name' : 'Model Group Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_model_representative_model_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_model_list.model_id.',
                'markdown_name' : 'Model Id',
            },
            ['PDB', 'ihm_model_representative_selection_criteria_fkey'], 
            ['PDB', 'ihm_model_representative_RCB_fkey'], 
            ['PDB', 'ihm_model_representative_RMB_fkey'], 
            'RCT', 
            'RMT', 
            ['PDB', 'ihm_model_representative_Owner_fkey'], 
        ],
    })

    # ----------------------------
    schema.tables["ihm_model_representative"].foreign_keys[(schema,"ihm_model_representative_model_id_fkey")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })

    # ----------------------------
    schema.tables["ihm_model_representative"].foreign_keys[(schema,"ihm_model_representative_model_group_id_fkey")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })


# -- -----------------------------------------------------------------------------
def update_PDB_ihm_modeling_post_process(model):
    schema = model.schemas["PDB"]
    table = schema.tables["ihm_modeling_post_process"]
    # ----------------------------
    schema.tables["ihm_modeling_post_process"].display.update(
        {'name' : 'Post Modeling Analyses', 'comment_display' : {'*': {'table_comment_display': 'inline'}}, }
    )

    # ----------------------------
    schema.tables["ihm_modeling_post_process"].table_display.update({
        'row_name' : { 'row_markdown_pattern' : '{{{id}}}', },
    })

    # ----------------------------
    schema.tables["ihm_modeling_post_process"].visible_columns.update({
        '*' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_modeling_post_process_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'id', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_modeling_post_process_protocol_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_modeling_protocol.id.',
                'markdown_name' : 'Protocol Id',
            },
            'analysis_id', 
            'step_id', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_modeling_post_process_struct_assembly_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_struct_assembly.id.',
                'markdown_name' : 'Struct Assembly Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_modeling_post_process_dataset_group_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_dataset_group.id.',
                'markdown_name' : 'Dataset Group Id',
            },
            ['PDB', 'ihm_modeling_post_process_type_fkey'], 
            ['PDB', 'ihm_modeling_post_process_feature_fkey'], 
            'feature_name', 
            'num_models_begin', 
            'num_models_end', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_modeling_post_process_script_file_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_external_files.id.',
                'markdown_name' : 'Script File Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_modeling_post_process_software_id_fkey']}, 'RID'],
                'comment' : 'A reference to table software.pdbx_ordinal.',
                'markdown_name' : 'Software Id',
            },
            'details', 
        ],
        'entry' :  [
            {
                'source' : [{'outbound': ['PDB', 'ihm_modeling_post_process_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'id', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_modeling_post_process_protocol_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_modeling_protocol.id.',
                'markdown_name' : 'Protocol Id',
            },
            'analysis_id', 
            'step_id', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_modeling_post_process_struct_assembly_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_struct_assembly.id.',
                'markdown_name' : 'Struct Assembly Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_modeling_post_process_dataset_group_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_dataset_group.id.',
                'markdown_name' : 'Dataset Group Id',
            },
            ['PDB', 'ihm_modeling_post_process_type_fkey'], 
            ['PDB', 'ihm_modeling_post_process_feature_fkey'], 
            'feature_name', 
            'num_models_begin', 
            'num_models_end', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_modeling_post_process_script_file_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_external_files.id.',
                'markdown_name' : 'Script File Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_modeling_post_process_software_id_fkey']}, 'RID'],
                'comment' : 'A reference to table software.pdbx_ordinal.',
                'markdown_name' : 'Software Id',
            },
            'details', 
        ],
        'detailed' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_modeling_post_process_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'id', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_modeling_post_process_protocol_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_modeling_protocol.id.',
                'markdown_name' : 'Protocol Id',
            },
            'analysis_id', 
            'step_id', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_modeling_post_process_struct_assembly_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_struct_assembly.id.',
                'markdown_name' : 'Struct Assembly Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_modeling_post_process_dataset_group_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_dataset_group.id.',
                'markdown_name' : 'Dataset Group Id',
            },
            ['PDB', 'ihm_modeling_post_process_type_fkey'], 
            ['PDB', 'ihm_modeling_post_process_feature_fkey'], 
            'feature_name', 
            'num_models_begin', 
            'num_models_end', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_modeling_post_process_script_file_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_external_files.id.',
                'markdown_name' : 'Script File Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_modeling_post_process_software_id_fkey']}, 'RID'],
                'comment' : 'A reference to table software.pdbx_ordinal.',
                'markdown_name' : 'Software Id',
            },
            'details', 
            ['PDB', 'ihm_modeling_post_process_RCB_fkey'], 
            ['PDB', 'ihm_modeling_post_process_RMB_fkey'], 
            'RCT', 
            'RMT', 
            ['PDB', 'ihm_modeling_post_process_Owner_fkey'], 
        ],
    })

    # ----------------------------
    schema.tables["ihm_modeling_post_process"].visible_foreign_keys.update({
        'filter' :  'detailed',
        'detailed' :  [
            ['PDB', 'ihm_ensemble_info_post_process_id_fkey'], 
        ],
    })

    # ----------------------------
    schema.tables["ihm_modeling_post_process"].columns["num_models_begin"].display.update(
        {'name' : 'Number of Models in the Beginning of the Analysis', }
    )

    # ----------------------------
    schema.tables["ihm_modeling_post_process"].columns["num_models_end"].display.update(
        {'name' : 'Number of Models at the End of the Analysis', }
    )

    # ----------------------------
    schema.tables["ihm_modeling_post_process"].foreign_keys[(schema,"ihm_modeling_post_process_struct_assembly_id_fkey")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })

    # ----------------------------
    schema.tables["ihm_modeling_post_process"].foreign_keys[(schema,"ihm_modeling_post_process_struct_assembly_id_fk")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })

    # ----------------------------
    schema.tables["ihm_modeling_post_process"].foreign_keys[(schema,"ihm_modeling_post_process_protocol_id_fkey")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })

    # ----------------------------
    schema.tables["ihm_modeling_post_process"].foreign_keys[(schema,"ihm_modeling_post_process_dataset_group_id_fk")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })

    # ----------------------------
    schema.tables["ihm_modeling_post_process"].foreign_keys[(schema,"ihm_modeling_post_process_software_id_fkey")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })

    # ----------------------------
    schema.tables["ihm_modeling_post_process"].foreign_keys[(schema,"ihm_modeling_post_process_script_file_id_fkey")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })

    # ----------------------------
    schema.tables["ihm_modeling_post_process"].foreign_keys[(schema,"ihm_modeling_post_process_script_file_id_fk")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })

    # ----------------------------
    schema.tables["ihm_modeling_post_process"].foreign_keys[(schema,"ihm_modeling_post_process_dataset_group_id_fkey")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })

    # ----------------------------
    schema.tables["ihm_modeling_post_process"].foreign_keys[(schema,"ihm_modeling_post_process_software_id_fk")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })


# -- -----------------------------------------------------------------------------
def update_PDB_ihm_modeling_protocol(model):
    schema = model.schemas["PDB"]
    table = schema.tables["ihm_modeling_protocol"]
    # ----------------------------
    schema.tables["ihm_modeling_protocol"].display.update(
        {'markdown_name' : 'Modeling Protocols^*^', 'comment_display' : {'*': {'table_comment_display': 'inline'}}, }
    )

    # ----------------------------
    schema.tables["ihm_modeling_protocol"].table_display.update({
        'row_name' : { 'row_markdown_pattern' : '{{{id}}}', },
    })

    # ----------------------------
    schema.tables["ihm_modeling_protocol"].visible_columns.update({
        '*' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_modeling_protocol_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'id', 
            'num_steps', 
            'protocol_name', 
            'details', 
        ],
        'entry' :  [
            {
                'source' : [{'outbound': ['PDB', 'ihm_modeling_protocol_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'id', 
            'num_steps', 
            'protocol_name', 
            'details', 
        ],
        'detailed' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_modeling_protocol_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'id', 
            'num_steps', 
            'protocol_name', 
            'details', 
            ['PDB', 'ihm_modeling_protocol_RCB_fkey'], 
            ['PDB', 'ihm_modeling_protocol_RMB_fkey'], 
            'RCT', 
            'RMT', 
            ['PDB', 'ihm_modeling_protocol_Owner_fkey'], 
        ],
    })

    # ----------------------------
    schema.tables["ihm_modeling_protocol"].visible_foreign_keys.update({
        'filter' :  'detailed',
        'detailed' :  [
            ['PDB', 'ihm_modeling_protocol_details_protocol_id_fkey'], 
            ['PDB', 'ihm_model_list_protocol_id_fkey'], 
            ['PDB', 'ihm_modeling_post_process_protocol_id_fkey'], 
        ],
    })

# -- -----------------------------------------------------------------------------
def update_PDB_ihm_modeling_protocol_details(model):
    schema = model.schemas["PDB"]
    table = schema.tables["ihm_modeling_protocol_details"]
    # ----------------------------
    schema.tables["ihm_modeling_protocol_details"].display.update(
        {'markdown_name' : 'Details of Modeling Protocols^*^', 'comment_display' : {'*': {'table_comment_display': 'inline'}}, }
    )

    # ----------------------------
    schema.tables["ihm_modeling_protocol_details"].visible_columns.update({
        '*' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_modeling_protocol_details_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'id', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_modeling_protocol_details_protocol_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_modeling_protocol.id.',
                'markdown_name' : 'Protocol Id',
            },
            'step_id', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_modeling_protocol_details_dataset_group_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_dataset_group.id.',
                'markdown_name' : 'Dataset Group Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_modeling_protocol_details_struct_assembly_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_struct_assembly.id.',
                'markdown_name' : 'Struct Assembly Id',
            },
            'struct_assembly_description', 
            'step_name', 
            'step_method', 
            'num_models_begin', 
            'num_models_end', 
            ['PDB', 'ihm_modeling_protocol_details_multi_scale_flag_fkey'], 
            ['PDB', 'ihm_modeling_protocol_details_multi_state_flag_fkey'], 
            ['PDB', 'ihm_modeling_protocol_details_ordered_flag_fkey'], 
            ['PDB', 'ihm_modeling_protocol_details_ensemble_flag_fkey'], 
            {
                'source' : [{'outbound': ['PDB', 'ihm_modeling_protocol_details_script_file_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_external_files.id.',
                'markdown_name' : 'Script File Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_modeling_protocol_details_software_id_fkey']}, 'RID'],
                'comment' : 'A reference to table software.pdbx_ordinal.',
                'markdown_name' : 'Software Id',
            },
            'description', 
        ],
        'entry' :  [
            {
                'source' : [{'outbound': ['PDB', 'ihm_modeling_protocol_details_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'id', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_modeling_protocol_details_protocol_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_modeling_protocol.id.',
                'markdown_name' : 'Protocol Id',
            },
            'step_id', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_modeling_protocol_details_dataset_group_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_dataset_group.id.',
                'markdown_name' : 'Dataset Group Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_modeling_protocol_details_struct_assembly_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_struct_assembly.id.',
                'markdown_name' : 'Struct Assembly Id',
            },
            'struct_assembly_description', 
            'step_name', 
            'step_method', 
            'num_models_begin', 
            'num_models_end', 
            ['PDB', 'ihm_modeling_protocol_details_multi_scale_flag_fkey'], 
            ['PDB', 'ihm_modeling_protocol_details_multi_state_flag_fkey'], 
            ['PDB', 'ihm_modeling_protocol_details_ordered_flag_fkey'], 
            ['PDB', 'ihm_modeling_protocol_details_ensemble_flag_fkey'], 
            {
                'source' : [{'outbound': ['PDB', 'ihm_modeling_protocol_details_script_file_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_external_files.id.',
                'markdown_name' : 'Script File Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_modeling_protocol_details_software_id_fkey']}, 'RID'],
                'comment' : 'A reference to table software.pdbx_ordinal.',
                'markdown_name' : 'Software Id',
            },
            'description', 
        ],
        'detailed' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_modeling_protocol_details_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'id', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_modeling_protocol_details_protocol_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_modeling_protocol.id.',
                'markdown_name' : 'Protocol Id',
            },
            'step_id', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_modeling_protocol_details_dataset_group_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_dataset_group.id.',
                'markdown_name' : 'Dataset Group Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_modeling_protocol_details_struct_assembly_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_struct_assembly.id.',
                'markdown_name' : 'Struct Assembly Id',
            },
            'struct_assembly_description', 
            'step_name', 
            'step_method', 
            'num_models_begin', 
            'num_models_end', 
            ['PDB', 'ihm_modeling_protocol_details_multi_scale_flag_fkey'], 
            ['PDB', 'ihm_modeling_protocol_details_multi_state_flag_fkey'], 
            ['PDB', 'ihm_modeling_protocol_details_ordered_flag_fkey'], 
            ['PDB', 'ihm_modeling_protocol_details_ensemble_flag_fkey'], 
            {
                'source' : [{'outbound': ['PDB', 'ihm_modeling_protocol_details_script_file_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_external_files.id.',
                'markdown_name' : 'Script File Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_modeling_protocol_details_software_id_fkey']}, 'RID'],
                'comment' : 'A reference to table software.pdbx_ordinal.',
                'markdown_name' : 'Software Id',
            },
            'description', 
            ['PDB', 'ihm_modeling_protocol_details_RCB_fkey'], 
            ['PDB', 'ihm_modeling_protocol_details_RMB_fkey'], 
            'RCT', 
            'RMT', 
            ['PDB', 'ihm_modeling_protocol_details_Owner_fkey'], 
        ],
    })

    # ----------------------------
    schema.tables["ihm_modeling_protocol_details"].columns["num_models_begin"].display.update(
        {'name' : 'Number of Models in the Beginning of the Step', }
    )
    
    # ----------------------------
    schema.tables["ihm_modeling_protocol_details"].columns["num_models_end"].display.update(
        {'name' : 'Number of Models at the End of the Step', }
    )
    
    # ----------------------------
    schema.tables["ihm_modeling_protocol_details"].foreign_keys[(schema,"ihm_modeling_protocol_details_protocol_id_fkey")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })

    # ----------------------------
    schema.tables["ihm_modeling_protocol_details"].foreign_keys[(schema,"ihm_modeling_protocol_details_script_file_id_fkey")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })

    # ----------------------------
    schema.tables["ihm_modeling_protocol_details"].foreign_keys[(schema,"ihm_modeling_protocol_details_software_id_fkey")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })

    # ----------------------------
    schema.tables["ihm_modeling_protocol_details"].foreign_keys[(schema,"ihm_modeling_protocol_details_script_file_id_fk")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })

    # ----------------------------
    schema.tables["ihm_modeling_protocol_details"].foreign_keys[(schema,"ihm_modeling_protocol_details_struct_assembly_id_fkey")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })

    # ----------------------------
    schema.tables["ihm_modeling_protocol_details"].foreign_keys[(schema,"ihm_modeling_protocol_details_dataset_group_id_fk")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })

    # ----------------------------
    schema.tables["ihm_modeling_protocol_details"].foreign_keys[(schema,"ihm_modeling_protocol_details_struct_assembly_id_fk")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })

    # ----------------------------
    schema.tables["ihm_modeling_protocol_details"].foreign_keys[(schema,"ihm_modeling_protocol_details_dataset_group_id_fkey")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })

    # ----------------------------
    schema.tables["ihm_modeling_protocol_details"].foreign_keys[(schema,"ihm_modeling_protocol_details_software_id_fk")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })


# -- -----------------------------------------------------------------------------
def update_PDB_ihm_multi_state_model_group_link(model):
    schema = model.schemas["PDB"]
    table = schema.tables["ihm_multi_state_model_group_link"]
    # ----------------------------
    schema.tables["ihm_multi_state_model_group_link"].display.update(
        {'name' : 'Model Groups Belonging to Multiple States', 'comment_display' : {'*': {'table_comment_display': 'inline'}}, }
    )

    # ----------------------------
    schema.tables["ihm_multi_state_model_group_link"].visible_columns.update({
        '*' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_multi_state_model_group_link_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_multi_state_model_group_link_state_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_multi_state_modeling.state_id.',
                'markdown_name' : 'State Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_multi_state_model_group_link_model_group_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_model_group.id.',
                'markdown_name' : 'Model Group Id',
            },
        ],
        'entry' :  [
            {
                'source' : [{'outbound': ['PDB', 'ihm_multi_state_model_group_link_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_multi_state_model_group_link_state_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_multi_state_modeling.state_id.',
                'markdown_name' : 'State Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_multi_state_model_group_link_model_group_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_model_group.id.',
                'markdown_name' : 'Model Group Id',
            },
        ],
        'detailed' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_multi_state_model_group_link_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_multi_state_model_group_link_state_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_multi_state_modeling.state_id.',
                'markdown_name' : 'State Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_multi_state_model_group_link_model_group_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_model_group.id.',
                'markdown_name' : 'Model Group Id',
            },
            ['PDB', 'ihm_multi_state_model_group_link_RCB_fkey'], 
            ['PDB', 'ihm_multi_state_model_group_link_RMB_fkey'], 
            'RCT', 
            'RMT', 
            ['PDB', 'ihm_multi_state_model_group_link_Owner_fkey'], 
        ],
    })
    
    # ----------------------------
    schema.tables["ihm_multi_state_model_group_link"].foreign_keys[(schema,"ihm_multi_state_model_group_link_state_id_fkey")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })

    # ----------------------------
    schema.tables["ihm_multi_state_model_group_link"].foreign_keys[(schema,"ihm_multi_state_model_group_link_model_group_id_fkey")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })

# -- -----------------------------------------------------------------------------
def update_PDB_ihm_multi_state_modeling(model):
    schema = model.schemas["PDB"]
    table = schema.tables["ihm_multi_state_modeling"]
    # ----------------------------
    schema.tables["ihm_multi_state_modeling"].display.update(
        {'name' : 'Multi-State Modeling', 'comment_display' : {'*': {'table_comment_display': 'inline'}}, }
    )

    # ----------------------------
    schema.tables["ihm_multi_state_modeling"].table_display.update({
        'row_name' : { 'row_markdown_pattern' : '{{{state_id}}}', },
    })

    # ----------------------------
    schema.tables["ihm_multi_state_modeling"].visible_columns.update({
        '*' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_multi_state_modeling_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'state_id', 
            'state_group_id', 
            'state_type', 
            'state_name', 
            ['PDB', 'ihm_multi_state_modeling_experiment_type_fkey'], 
            'population_fraction', 
            'population_fraction_sd', 
            'details', 
        ],
        'entry' :  [
            {
                'source' : [{'outbound': ['PDB', 'ihm_multi_state_modeling_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'state_id', 
            'state_group_id', 
            'state_type', 
            'state_name', 
            ['PDB', 'ihm_multi_state_modeling_experiment_type_fkey'], 
            'population_fraction', 
            'population_fraction_sd', 
            'details', 
        ],
        'detailed' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_multi_state_modeling_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'state_id', 
            'state_group_id', 
            'state_type', 
            'state_name', 
            ['PDB', 'ihm_multi_state_modeling_experiment_type_fkey'], 
            'population_fraction', 
            'population_fraction_sd', 
            'details', 
            ['PDB', 'ihm_multi_state_modeling_RCB_fkey'], 
            ['PDB', 'ihm_multi_state_modeling_RMB_fkey'], 
            'RCT', 
            'RMT', 
            ['PDB', 'ihm_multi_state_modeling_Owner_fkey'], 
        ],
    })

    # ----------------------------
    schema.tables["ihm_multi_state_modeling"].visible_foreign_keys.update({
        'filter' :  'detailed',
        'detailed' :  [
            ['PDB', 'ihm_multi_state_model_group_link_state_id_fkey'], 
            ['PDB', 'ihm_multi_state_scheme_connectivity_modeling_1_combo1_fkey'], 
        ],
    })

    # ----------------------------
    schema.tables["ihm_multi_state_modeling"].columns["population_fraction_sd"].display.update(
        {'name' : 'Population Fraction Standard Deviation', }
    )


# -- -----------------------------------------------------------------------------
def update_PDB_ihm_multi_state_scheme(model):
    schema = model.schemas["PDB"]
    table = schema.tables["ihm_multi_state_scheme"]
    # ----------------------------
    schema.tables["ihm_multi_state_scheme"].display.update(
        {'name' : 'Multi-State Schemes', 'comment_display' : {'*': {'table_comment_display': 'inline'}}, }
    )

    # ----------------------------
    schema.tables["ihm_multi_state_scheme"].visible_columns.update({
        '*' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_multi_state_scheme_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'id', 
            'name', 
            'details', 
        ],
        'entry' :  [
            'id', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_multi_state_scheme_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'name', 
            'details', 
        ],
        'detailed' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_multi_state_scheme_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'id', 
            'name', 
            'details', 
            ['PDB', 'ihm_multi_state_scheme_RCB_fkey'], 
            ['PDB', 'ihm_multi_state_scheme_RMB_fkey'], 
            'RCT', 
            'RMT', 
            ['PDB', 'ihm_multi_state_scheme_Owner_fkey'], 
        ],
    })

    # ----------------------------
    schema.tables["ihm_multi_state_scheme"].visible_foreign_keys.update({
        'filter' :  'detailed',
        'detailed' :  [
            ['PDB', 'ihm_multi_state_scheme_connectivity_scheme_combo1_fkey'], 
            ['PDB', 'ihm_relaxation_time_multi_state_scheme_scheme_combo1_fkey'], 
        ],
    })

# -- -----------------------------------------------------------------------------
def update_PDB_ihm_multi_state_scheme_connectivity(model):
    schema = model.schemas["PDB"]
    table = schema.tables["ihm_multi_state_scheme_connectivity"]
    # ----------------------------
    schema.tables["ihm_multi_state_scheme_connectivity"].display.update(
        {'name' : 'Multi-State Scheme Connectivities', 'comment_display' : {'*': {'table_comment_display': 'inline'}}, }
    )
    
    # ----------------------------
    schema.tables["ihm_multi_state_scheme_connectivity"].visible_columns.update({
        '*' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_multi_state_scheme_connectivity_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'id', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_multi_state_scheme_connectivity_scheme_combo1_fkey']}, 'RID'],
                'comment' : 'Identifier for the multi-state scheme',
                'markdown_name' : 'Scheme Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_multi_state_scheme_connectivity_modeling_1_combo1_fkey']}, 'RID'],
                'comment' : 'Identifier for the starting state in the multi-state scheme',
                'markdown_name' : 'Begin State Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_multi_state_scheme_connectivity_modeling_2_combo2_fkey']}, 'RID'],
                'comment' : 'Identifier for the ending state in the multi-state scheme',
                'markdown_name' : 'End State Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'multi_state_scheme_connectivity_dataset_group_combo1_fkey']}, 'RID'],
                'comment' : 'Identifier for the dataset group from which the multi-state scheme is obtained',
                'markdown_name' : 'Dataset Group Id',
            },
            'details', 
        ],
        'entry' :  [
            {
                'source' : [{'outbound': ['PDB', 'ihm_multi_state_scheme_connectivity_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'id', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_multi_state_scheme_connectivity_scheme_combo1_fkey']}, 'RID'],
                'comment' : 'Identifier for the multi-state scheme',
                'markdown_name' : 'Scheme Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_multi_state_scheme_connectivity_modeling_1_combo1_fkey']}, 'RID'],
                'comment' : 'Identifier for the starting state in the multi-state scheme',
                'markdown_name' : 'Begin State Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_multi_state_scheme_connectivity_modeling_2_combo2_fkey']}, 'RID'],
                'comment' : 'Identifier for the ending state in the multi-state scheme',
                'markdown_name' : 'End State Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'multi_state_scheme_connectivity_dataset_group_combo1_fkey']}, 'RID'],
                'comment' : 'Identifier for the dataset group from which the multi-state scheme is obtained',
                'markdown_name' : 'Dataset Group Id',
            },
            'details', 
        ],
        'detailed' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_multi_state_scheme_connectivity_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'id', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_multi_state_scheme_connectivity_scheme_combo1_fkey']}, 'RID'],
                'comment' : 'Identifier for the multi-state scheme',
                'markdown_name' : 'Scheme Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_multi_state_scheme_connectivity_modeling_1_combo1_fkey']}, 'RID'],
                'comment' : 'Identifier for the starting state in the multi-state scheme',
                'markdown_name' : 'Begin State Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_multi_state_scheme_connectivity_modeling_2_combo2_fkey']}, 'RID'],
                'comment' : 'Identifier for the ending state in the multi-state scheme',
                'markdown_name' : 'End State Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'multi_state_scheme_connectivity_dataset_group_combo1_fkey']}, 'RID'],
                'comment' : 'Identifier for the dataset group from which the multi-state scheme is obtained',
                'markdown_name' : 'Dataset Group Id',
            },
            'details', 
            ['PDB', 'ihm_multi_state_scheme_connectivity_RCB_fkey'], 
            ['PDB', 'ihm_multi_state_scheme_connectivity_RMB_fkey'], 
            'RCT', 
            'RMT', 
            ['PDB', 'ihm_multi_state_scheme_connectivity_Owner_fkey'], 
        ],
    })

    # ----------------------------
    schema.tables["ihm_multi_state_scheme_connectivity"].visible_foreign_keys.update({
        'filter' :  'detailed',
        'detailed' :  [
            ['PDB', 'ihm_kinetic_rate_multi_state_scheme_connectivity_combo1_fkey'], 
            ['PDB', 'relaxation_time_multi_state_scheme_connectivity_combo2_fkey'], 
        ],
    })

    # ----------------------------
    schema.tables["ihm_multi_state_scheme_connectivity"].foreign_keys[(schema,"ihm_multi_state_scheme_connectivity_modeling_1_combo1_fkey")].foreign_key.update({
        'template_engine' :  'handlebars',
        'domain_filter_pattern' :  '{{#if _structure_id}}structure_id={{{_structure_id}}}{{/if}}',
    })

    # ----------------------------
    schema.tables["ihm_multi_state_scheme_connectivity"].foreign_keys[(schema,"multi_state_scheme_connectivity_dataset_group_combo1_fkey")].foreign_key.update({
        'template_engine' :  'handlebars',
        'domain_filter_pattern' :  '{{#if _structure_id}}structure_id={{{_structure_id}}}{{/if}}',
    })

    # ----------------------------
    schema.tables["ihm_multi_state_scheme_connectivity"].foreign_keys[(schema,"ihm_multi_state_scheme_connectivity_modeling_2_combo2_fkey")].foreign_key.update({
        'template_engine' :  'handlebars',
        'domain_filter_pattern' :  '{{#if _structure_id}}structure_id={{{_structure_id}}}{{/if}}',
    })

    # ----------------------------
    schema.tables["ihm_multi_state_scheme_connectivity"].foreign_keys[(schema,"ihm_multi_state_scheme_connectivity_scheme_combo1_fkey")].foreign_key.update({
        'template_engine' :  'handlebars',
        'domain_filter_pattern' :  '{{#if _structure_id}}structure_id={{{_structure_id}}}{{/if}}',
    })

# -- -----------------------------------------------------------------------------
def update_PDB_ihm_non_poly_feature(model):
    schema = model.schemas["PDB"]
    table = schema.tables["ihm_non_poly_feature"]
    # ----------------------------
    schema.tables["ihm_non_poly_feature"].display.update(
        {'name' : 'Molecular Features - Non-polymeric Entities', 'comment_display' : {'*': {'table_comment_display': 'inline'}}, }
    )

    # ----------------------------
    schema.tables["ihm_non_poly_feature"].visible_columns.update({
        '*' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_non_poly_feature_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'ordinal_id', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_non_poly_feature_feature_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_feature_list.feature_id.',
                'markdown_name' : 'Feature Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_non_poly_feature_entity_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entity.id.',
                'markdown_name' : 'Entity Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_non_poly_feature_asym_id_fkey']}, 'RID'],
                'comment' : 'A reference to table struct_asym.id.',
                'markdown_name' : 'Asym Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_non_poly_feature_comp_id_fkey']}, 'RID'],
                'comment' : 'A reference to table chem_comp.id.',
                'markdown_name' : 'Component Id',
            },
            'atom_id', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_non_poly_feature_Entry_Related_File_fkey']}, 'RID'],
                'comment' : 'A reference to the uploaded restraint file in the table Entry_Related_File.id.',
                'markdown_name' : 'Uploaded Restraint File',
            },
        ],
        'entry' :  [
            {
                'source' : [{'outbound': ['PDB', 'ihm_non_poly_feature_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'ordinal_id', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_non_poly_feature_feature_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_feature_list.feature_id.',
                'markdown_name' : 'Feature Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_non_poly_feature_entity_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entity.id.',
                'markdown_name' : 'Entity Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_non_poly_feature_asym_id_fkey']}, 'RID'],
                'comment' : 'A reference to table struct_asym.id.',
                'markdown_name' : 'Asym Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_non_poly_feature_comp_id_fkey']}, 'RID'],
                'comment' : 'A reference to table chem_comp.id.',
                'markdown_name' : 'Component Id',
            },
            'atom_id', 
        ],
        'detailed' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_non_poly_feature_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'ordinal_id', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_non_poly_feature_feature_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_feature_list.feature_id.',
                'markdown_name' : 'Feature Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_non_poly_feature_entity_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entity.id.',
                'markdown_name' : 'Entity Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_non_poly_feature_asym_id_fkey']}, 'RID'],
                'comment' : 'A reference to table struct_asym.id.',
                'markdown_name' : 'Asym Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_non_poly_feature_comp_id_fkey']}, 'RID'],
                'comment' : 'A reference to table chem_comp.id.',
                'markdown_name' : 'Component Id',
            },
            'atom_id', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_non_poly_feature_Entry_Related_File_fkey']}, 'RID'],
                'comment' : 'A reference to the uploaded restraint file in the table Entry_Related_File.id.',
                'markdown_name' : 'Uploaded Restraint File',
            },
            ['PDB', 'ihm_non_poly_feature_RCB_fkey'], 
            ['PDB', 'ihm_non_poly_feature_RMB_fkey'], 
            'RCT', 
            'RMT', 
            ['PDB', 'ihm_non_poly_feature_Owner_fkey'], 
        ],
    })

    # ----------------------------
    schema.tables["ihm_non_poly_feature"].foreign_keys[(schema,"ihm_non_poly_feature_comp_id_fkey")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })

    # ----------------------------
    schema.tables["ihm_non_poly_feature"].foreign_keys[(schema,"ihm_non_poly_feature_feature_id_fkey")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })

    # ----------------------------
    schema.tables["ihm_non_poly_feature"].foreign_keys[(schema,"ihm_non_poly_feature_asym_id_fk")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })

    # ----------------------------
    schema.tables["ihm_non_poly_feature"].foreign_keys[(schema,"ihm_non_poly_feature_entity_id_fkey")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })

    # ----------------------------
    schema.tables["ihm_non_poly_feature"].foreign_keys[(schema,"ihm_non_poly_feature_asym_id_fkey")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })


# -- -----------------------------------------------------------------------------
def update_PDB_ihm_ordered_ensemble(model):
    schema = model.schemas["PDB"]
    table = schema.tables["ihm_ordered_ensemble"]
    # ----------------------------
    schema.tables["ihm_ordered_ensemble"].display.update(
        {'name' : 'Ordered Ensembles (to be deprecated and superseded by Ordered Models)', 'comment_display' : {'*': {'table_comment_display': 'inline'}}, }
    )
    
    # ----------------------------
    schema.tables["ihm_ordered_ensemble"].visible_columns.update({
        '*' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_ordered_ensemble_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'process_id', 
            'process_description', 
            'edge_id', 
            'edge_description', 
            'step_id', 
            'step_description', 
            'ordered_by', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_ordered_ensemble_model_group_id_begin_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_model_group.id.',
                'markdown_name' : 'Model Group Id Begin',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_ordered_ensemble_model_group_id_end_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_model_group.id.',
                'markdown_name' : 'Model Group Id End',
            },
        ],
        'entry' :  [
            {
                'source' : [{'outbound': ['PDB', 'ihm_ordered_ensemble_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'process_id', 
            'process_description', 
            'edge_id', 
            'edge_description', 
            'step_id', 
            'step_description', 
            'ordered_by', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_ordered_ensemble_model_group_id_begin_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_model_group.id.',
                'markdown_name' : 'Model Group Id Begin',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_ordered_ensemble_model_group_id_end_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_model_group.id.',
                'markdown_name' : 'Model Group Id End',
            },
        ],
        'detailed' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_ordered_ensemble_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'process_id', 
            'process_description', 
            'edge_id', 
            'edge_description', 
            'step_id', 
            'step_description', 
            'ordered_by', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_ordered_ensemble_model_group_id_begin_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_model_group.id.',
                'markdown_name' : 'Model Group Id Begin',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_ordered_ensemble_model_group_id_end_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_model_group.id.',
                'markdown_name' : 'Model Group Id End',
            },
            ['PDB', 'ihm_ordered_ensemble_RCB_fkey'], 
            ['PDB', 'ihm_ordered_ensemble_RMB_fkey'], 
            'RCT', 
            'RMT', 
            ['PDB', 'ihm_ordered_ensemble_Owner_fkey'], 
        ],
    })

    # ----------------------------
    schema.tables["ihm_ordered_ensemble"].foreign_keys[(schema,"ihm_ordered_ensemble_model_group_id_begin_fkey")].foreign_key.update({
        'template_engine' :  'handlebars',
        'domain_filter_pattern' :  '{{#if _structure_id}}structure_id={{{_structure_id}}}{{/if}}',
    })

    # ----------------------------
    schema.tables["ihm_ordered_ensemble"].foreign_keys[(schema,"ihm_ordered_ensemble_model_group_id_end_fkey")].foreign_key.update({
        'template_engine' :  'handlebars',
        'domain_filter_pattern' :  '{{#if _structure_id}}structure_id={{{_structure_id}}}{{/if}}',
    })


# -- -----------------------------------------------------------------------------
def update_PDB_ihm_ordered_model(model):
    schema = model.schemas["PDB"]
    table = schema.tables["ihm_ordered_model"]
    # ----------------------------
    schema.tables["ihm_ordered_model"].display.update(
        {'name' : 'Ordered Models', 'comment_display' : {'*': {'table_comment_display': 'inline'}}, }
    )

    # ----------------------------
    schema.tables["ihm_ordered_model"].visible_columns.update({
        '*' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_ordered_model_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'process_id', 
            'process_description', 
            'edge_id', 
            'edge_description', 
            'step_id', 
            'step_description', 
            'ordered_by', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_ordered_model_ihm_model_group_begin_combo1_fkey']}, 'RID'],
                'comment' : 'Model group id corresponding to the node at the origin of the directed edge',
                'markdown_name' : 'Model Group Id Begin',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_ordered_model_ihm_model_group_end_combo1_fkey']}, 'RID'],
                'comment' : 'Model group id corresponding to the node at the end of the directed edge',
                'markdown_name' : 'Model Group Id End',
            },
        ],
        'entry' :  [
            {
                'source' : [{'outbound': ['PDB', 'ihm_ordered_model_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'process_id', 
            'process_description', 
            'edge_id', 
            'edge_description', 
            'step_id', 
            'step_description', 
            'ordered_by', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_ordered_model_ihm_model_group_begin_combo1_fkey']}, 'RID'],
                'comment' : 'Model group id corresponding to the node at the origin of the directed edge',
                'markdown_name' : 'Model Group Id Begin',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_ordered_model_ihm_model_group_end_combo1_fkey']}, 'RID'],
                'comment' : 'Model group id corresponding to the node at the end of the directed edge',
                'markdown_name' : 'Model Group Id End',
            },
        ],
        'detailed' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_ordered_model_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'process_id', 
            'process_description', 
            'edge_id', 
            'edge_description', 
            'step_id', 
            'step_description', 
            'ordered_by', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_ordered_model_ihm_model_group_begin_combo1_fkey']}, 'RID'],
                'comment' : 'Model group id corresponding to the node at the origin of the directed edge',
                'markdown_name' : 'Model Group Id Begin',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_ordered_model_ihm_model_group_end_combo1_fkey']}, 'RID'],
                'comment' : 'Model group id corresponding to the node at the end of the directed edge',
                'markdown_name' : 'Model Group Id End',
            },
            ['PDB', 'ihm_ordered_model_RCB_fkey'], 
            ['PDB', 'ihm_ordered_model_RMB_fkey'], 
            'RCT', 
            'RMT', 
            ['PDB', 'ihm_ordered_model_Owner_fkey'], 
        ],
    })

    # ----------------------------
    schema.tables["ihm_ordered_model"].foreign_keys[(schema,"ihm_ordered_model_ihm_model_group_begin_combo1_fkey")].foreign_key.update({
        'template_engine' :  'handlebars',
        'domain_filter_pattern' :  '{{#if _structure_id}}structure_id={{{_structure_id}}}{{/if}}',
    })

    # ----------------------------
    schema.tables["ihm_ordered_model"].foreign_keys[(schema,"ihm_ordered_model_ihm_model_group_end_combo1_fkey")].foreign_key.update({
        'template_engine' :  'handlebars',
        'domain_filter_pattern' :  '{{#if _structure_id}}structure_id={{{_structure_id}}}{{/if}}',
    })


# -- -----------------------------------------------------------------------------
def update_PDB_ihm_poly_atom_feature(model):
    schema = model.schemas["PDB"]
    table = schema.tables["ihm_poly_atom_feature"]
    # ----------------------------
    schema.tables["ihm_poly_atom_feature"].display.update(
        {'name' : 'Molecular Features - Polymeric Atoms', 'comment_display' : {'*': {'table_comment_display': 'inline'}}, }
    )
    
    # ----------------------------
    schema.tables["ihm_poly_atom_feature"].visible_columns.update({
        '*' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_poly_atom_feature_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'ordinal_id', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_poly_atom_feature_feature_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_feature_list.feature_id.',
                'markdown_name' : 'Feature Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_poly_atom_feature_mm_poly_res_label_fkey']}, 'entity_id'],
                'comment' : 'A reference to table entity_poly_seq.entity_id',
                'markdown_name' : 'Entity Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_poly_atom_feature_asym_id_fkey']}, 'RID'],
                'comment' : 'A reference to table struct_asym.id.',
                'markdown_name' : 'Asym Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_poly_atom_feature_mm_poly_res_label_fkey']}, 'mon_id'],
                'comment' : 'A reference to table entity_poly_seq.mon_id',
                'markdown_name' : 'Component Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_poly_atom_feature_mm_poly_res_label_fkey']}, 'num'],
                'comment' : 'A reference to table entity_poly_seq.num',
                'markdown_name' : 'Sequence Id',
            },
            'atom_id', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_poly_atom_feature_mm_poly_res_label_fkey']}, 'RID'],
                'comment' : 'Refers to a combination of Entity Id, Sequence Id and Component Id in the entity_poly_seq table.',
                'markdown_name' : 'Polymeric Residue',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_poly_atom_feature_Entry_Related_File_fkey']}, 'RID'],
                'comment' : 'A reference to the uploaded restraint file in the table Entry_Related_File.id.',
                'markdown_name' : 'Uploaded Restraint File',
            },
        ],
        'entry' :  [
            {
                'source' : [{'outbound': ['PDB', 'ihm_poly_atom_feature_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'ordinal_id', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_poly_atom_feature_feature_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_feature_list.feature_id.',
                'markdown_name' : 'Feature Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_poly_atom_feature_mm_poly_res_label_fkey']}, 'entity_id'],
                'comment' : 'A reference to table entity_poly_seq.entity_id',
                'markdown_name' : 'Entity Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_poly_atom_feature_asym_id_fkey']}, 'RID'],
                'comment' : 'A reference to table struct_asym.id.',
                'markdown_name' : 'Asym Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_poly_atom_feature_mm_poly_res_label_fkey']}, 'mon_id'],
                'comment' : 'A reference to table entity_poly_seq.mon_id',
                'markdown_name' : 'Component Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_poly_atom_feature_mm_poly_res_label_fkey']}, 'num'],
                'comment' : 'A reference to table entity_poly_seq.num',
                'markdown_name' : 'Sequence Id',
            },
            'atom_id', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_poly_atom_feature_mm_poly_res_label_fkey']}, 'RID'],
                'comment' : 'Refers to a combination of Entity Id, Sequence Id and Component Id in the entity_poly_seq table.',
                'markdown_name' : 'Polymeric Residue',
            },
        ],
        'detailed' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_poly_atom_feature_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'ordinal_id', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_poly_atom_feature_feature_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_feature_list.feature_id.',
                'markdown_name' : 'Feature Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_poly_atom_feature_mm_poly_res_label_fkey']}, 'entity_id'],
                'comment' : 'A reference to table entity_poly_seq.entity_id',
                'markdown_name' : 'Entity Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_poly_atom_feature_asym_id_fkey']}, 'RID'],
                'comment' : 'A reference to table struct_asym.id.',
                'markdown_name' : 'Asym Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_poly_atom_feature_mm_poly_res_label_fkey']}, 'mon_id'],
                'comment' : 'A reference to table entity_poly_seq.mon_id',
                'markdown_name' : 'Component Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_poly_atom_feature_mm_poly_res_label_fkey']}, 'num'],
                'comment' : 'A reference to table entity_poly_seq.num',
                'markdown_name' : 'Sequence Id',
            },
            'atom_id', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_poly_atom_feature_mm_poly_res_label_fkey']}, 'RID'],
                'comment' : 'Refers to a combination of Entity Id, Sequence Id and Component Id in the entity_poly_seq table.',
                'markdown_name' : 'Polymeric Residue',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_poly_atom_feature_Entry_Related_File_fkey']}, 'RID'],
                'comment' : 'A reference to the uploaded restraint file in the table Entry_Related_File.id.',
                'markdown_name' : 'Uploaded Restraint File',
            },
            ['PDB', 'ihm_poly_atom_feature_RCB_fkey'], 
            ['PDB', 'ihm_poly_atom_feature_RMB_fkey'], 
            'RCT', 
            'RMT', 
            ['PDB', 'ihm_poly_atom_feature_Owner_fkey'], 
        ],
    })

    # ----------------------------
    schema.tables["ihm_poly_atom_feature"].foreign_keys[(schema,"ihm_poly_atom_feature_asym_id_fk")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })

    # ----------------------------
    schema.tables["ihm_poly_atom_feature"].foreign_keys[(schema,"ihm_poly_atom_feature_mm_poly_res_label_fkey")].foreign_key.update({
        'template_engine' :  'handlebars',
        'domain_filter_pattern' :  '{{#if _structure_id}}structure_id={{{_structure_id}}}{{/if}}',
    })

    # ----------------------------
    schema.tables["ihm_poly_atom_feature"].foreign_keys[(schema,"ihm_poly_atom_feature_asym_id_fkey")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })

    # ----------------------------
    schema.tables["ihm_poly_atom_feature"].foreign_keys[(schema,"ihm_poly_atom_feature_feature_id_fkey")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })


# -- -----------------------------------------------------------------------------
def update_PDB_ihm_poly_probe_conjugate(model):
    schema = model.schemas["PDB"]
    table = schema.tables["ihm_poly_probe_conjugate"]
    # ----------------------------
    schema.tables["ihm_poly_probe_conjugate"].display.update(
        {'name' : 'Probes Attached to Polymeric Residues', 'comment_display' : {'*': {'table_comment_display': 'inline'}}, }
    )

    # ----------------------------
    schema.tables["ihm_poly_probe_conjugate"].visible_columns.update({
        '*' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_poly_probe_conjugate_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'id', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_poly_probe_conjugate_probe_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_probe_list.probe_id.',
                'markdown_name' : 'Probe Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_poly_probe_conjugate_position_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_poly_probe_position.id.',
                'markdown_name' : 'Position Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_poly_probe_conjugate_chem_comp_descriptor_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_chemical_component_descriptor.id.',
                'markdown_name' : 'Chemical Component Descriptor Id',
            },
            ['PDB', 'ihm_poly_probe_conjugate_ambiguous_stoichiometry_flag_fkey'], 
            'probe_stoichiometry', 
            'details', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_poly_probe_conjugate_dataset_list_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_dataset_list.id.',
                'markdown_name' : 'Dataset List Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_poly_probe_conjugate_Entry_Related_File_fkey']}, 'RID'],
                'comment' : 'A reference to the uploaded restraint file in the table Entry_Related_File.id.',
                'markdown_name' : 'Uploaded Restraint File',
            },
        ],
        'entry' :  [
            {
                'source' : [{'outbound': ['PDB', 'ihm_poly_probe_conjugate_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'id', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_poly_probe_conjugate_probe_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_probe_list.probe_id.',
                'markdown_name' : 'Probe Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_poly_probe_conjugate_position_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_poly_probe_position.id.',
                'markdown_name' : 'Position Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_poly_probe_conjugate_chem_comp_descriptor_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_chemical_component_descriptor.id.',
                'markdown_name' : 'Chemical Component Descriptor Id',
            },
            ['PDB', 'ihm_poly_probe_conjugate_ambiguous_stoichiometry_flag_fkey'], 
            'probe_stoichiometry', 
            'details', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_poly_probe_conjugate_dataset_list_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_dataset_list.id.',
                'markdown_name' : 'Dataset List Id',
            },
        ],
        'detailed' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_poly_probe_conjugate_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'id', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_poly_probe_conjugate_probe_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_probe_list.probe_id.',
                'markdown_name' : 'Probe Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_poly_probe_conjugate_position_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_poly_probe_position.id.',
                'markdown_name' : 'Position Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_poly_probe_conjugate_chem_comp_descriptor_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_chemical_component_descriptor.id.',
                'markdown_name' : 'Chemical Component Descriptor Id',
            },
            ['PDB', 'ihm_poly_probe_conjugate_ambiguous_stoichiometry_flag_fkey'], 
            'probe_stoichiometry', 
            'details', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_poly_probe_conjugate_dataset_list_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_dataset_list.id.',
                'markdown_name' : 'Dataset List Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_poly_probe_conjugate_Entry_Related_File_fkey']}, 'RID'],
                'comment' : 'A reference to the uploaded restraint file in the table Entry_Related_File.id.',
                'markdown_name' : 'Uploaded Restraint File',
            },
            ['PDB', 'ihm_poly_probe_conjugate_RCB_fkey'], 
            ['PDB', 'ihm_poly_probe_conjugate_RMB_fkey'], 
            'RCT', 
            'RMT', 
            ['PDB', 'ihm_poly_probe_conjugate_Owner_fkey'], 
        ],
    })

    # ----------------------------
    schema.tables["ihm_poly_probe_conjugate"].foreign_keys[(schema,"ihm_poly_probe_conjugate_chem_comp_descriptor_id_fk")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })

    # ----------------------------
    schema.tables["ihm_poly_probe_conjugate"].foreign_keys[(schema,"ihm_poly_probe_conjugate_dataset_list_id_fkey")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })

    # ----------------------------
    schema.tables["ihm_poly_probe_conjugate"].foreign_keys[(schema,"ihm_poly_probe_conjugate_chem_comp_descriptor_id_fkey")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })

    # ----------------------------
    schema.tables["ihm_poly_probe_conjugate"].foreign_keys[(schema,"ihm_poly_probe_conjugate_position_id_fkey")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })

    # ----------------------------
    schema.tables["ihm_poly_probe_conjugate"].foreign_keys[(schema,"ihm_poly_probe_conjugate_probe_id_fkey")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })


# -- -----------------------------------------------------------------------------
def update_PDB_ihm_poly_probe_position(model):
    schema = model.schemas["PDB"]
    table = schema.tables["ihm_poly_probe_position"]
    # ----------------------------
    schema.tables["ihm_poly_probe_position"].display.update(
        {'name' : 'Polymeric Residue Positions', 'comment_display' : {'*': {'table_comment_display': 'inline'}}, }
    )

    # ----------------------------
    schema.tables["ihm_poly_probe_position"].visible_columns.update({
        '*' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_poly_probe_position_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'id', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_poly_probe_position_mm_poly_res_label_fkey']}, 'entity_id'],
                'comment' : 'A reference to table entity.id.',
                'markdown_name' : 'Entity Id',
            },
            'entity_description', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_poly_probe_position_mm_poly_res_label_fkey']}, 'num'],
                'comment' : 'A reference to table entity_poly_seq.num.',
                'markdown_name' : 'Sequence Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_poly_probe_position_mm_poly_res_label_fkey']}, 'mon_id'],
                'comment' : 'A reference to table entity_poly_seq.mon_id.',
                'markdown_name' : 'Component Id',
            },
            ['PDB', 'ihm_poly_probe_position_mutation_flag_fkey'], 
            {
                'source' : [{'outbound': ['PDB', 'ihm_poly_probe_position_mut_res_chem_comp_id_fkey']}, 'RID'],
                'comment' : 'A reference to table chem_comp.id.',
                'markdown_name' : 'Chemical Component Id of the Mutated Residue',
            },
            ['PDB', 'ihm_poly_probe_position_modification_flag_fkey'], 
            {
                'source' : [{'outbound': ['PDB', 'ihm_poly_probe_position_mod_res_chem_comp_descriptor_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_chemical_component_descriptor.id.',
                'markdown_name' : 'Chemical Descriptor Id of the Modified Residue',
            },
            'description', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_poly_probe_position_mm_poly_res_label_fkey']}, 'RID'],
                'comment' : 'Refers to a combination of Entity Id, Sequence Id and Component Id in the entity_poly_seq table.',
                'markdown_name' : 'Polymeric Residue',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_poly_probe_position_Entry_Related_File_fkey']}, 'RID'],
                'comment' : 'A reference to the uploaded restraint file in the table Entry_Related_File.id.',
                'markdown_name' : 'Uploaded Restraint File',
            },
        ],
        'entry' :  [
            {
                'source' : [{'outbound': ['PDB', 'ihm_poly_probe_position_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'id', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_poly_probe_position_mm_poly_res_label_fkey']}, 'entity_id'],
                'comment' : 'A reference to table entity.id.',
                'markdown_name' : 'Entity Id',
            },
            'entity_description', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_poly_probe_position_mm_poly_res_label_fkey']}, 'num'],
                'comment' : 'A reference to table entity_poly_seq.num.',
                'markdown_name' : 'Sequence Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_poly_probe_position_mm_poly_res_label_fkey']}, 'mon_id'],
                'comment' : 'A reference to table entity_poly_seq.mon_id.',
                'markdown_name' : 'Component Id',
            },
            ['PDB', 'ihm_poly_probe_position_mutation_flag_fkey'], 
            {
                'source' : [{'outbound': ['PDB', 'ihm_poly_probe_position_mut_res_chem_comp_id_fkey']}, 'RID'],
                'comment' : 'A reference to table chem_comp.id.',
                'markdown_name' : 'Chemical Component Id of the Mutated Residue',
            },
            ['PDB', 'ihm_poly_probe_position_modification_flag_fkey'], 
            {
                'source' : [{'outbound': ['PDB', 'ihm_poly_probe_position_mod_res_chem_comp_descriptor_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_chemical_component_descriptor.id.',
                'markdown_name' : 'Chemical Descriptor Id of the Modified Residue',
            },
            'description', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_poly_probe_position_mm_poly_res_label_fkey']}, 'RID'],
                'comment' : 'Refers to a combination of Entity Id, Sequence Id and Component Id in the entity_poly_seq table.',
                'markdown_name' : 'Polymeric Residue',
            },
        ],
        'detailed' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_poly_probe_position_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'id', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_poly_probe_position_mm_poly_res_label_fkey']}, 'entity_id'],
                'comment' : 'A reference to table entity.id.',
                'markdown_name' : 'Entity Id',
            },
            'entity_description', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_poly_probe_position_mm_poly_res_label_fkey']}, 'num'],
                'comment' : 'A reference to table entity_poly_seq.num.',
                'markdown_name' : 'Sequence Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_poly_probe_position_mm_poly_res_label_fkey']}, 'mon_id'],
                'comment' : 'A reference to table entity_poly_seq.mon_id.',
                'markdown_name' : 'Component Id',
            },
            ['PDB', 'ihm_poly_probe_position_mutation_flag_fkey'], 
            {
                'source' : [{'outbound': ['PDB', 'ihm_poly_probe_position_mut_res_chem_comp_id_fkey']}, 'RID'],
                'comment' : 'A reference to table chem_comp.id.',
                'markdown_name' : 'Chemical Component Id of the Mutated Residue',
            },
            ['PDB', 'ihm_poly_probe_position_modification_flag_fkey'], 
            {
                'source' : [{'outbound': ['PDB', 'ihm_poly_probe_position_mod_res_chem_comp_descriptor_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_chemical_component_descriptor.id.',
                'markdown_name' : 'Chemical Descriptor Id of the Modified Residue',
            },
            'description', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_poly_probe_position_mm_poly_res_label_fkey']}, 'RID'],
                'comment' : 'Refers to a combination of Entity Id, Sequence Id and Component Id in the entity_poly_seq table.',
                'markdown_name' : 'Polymeric Residue',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_poly_probe_position_Entry_Related_File_fkey']}, 'RID'],
                'comment' : 'A reference to the uploaded restraint file in the table Entry_Related_File.id.',
                'markdown_name' : 'Uploaded Restraint File',
            },
            ['PDB', 'ihm_poly_probe_position_RCB_fkey'], 
            ['PDB', 'ihm_poly_probe_position_RMB_fkey'], 
            'RCT', 
            'RMT', 
            ['PDB', 'ihm_poly_probe_position_Owner_fkey'], 
        ],
    })

    # ----------------------------
    schema.tables["ihm_poly_probe_position"].visible_foreign_keys.update({
        'filter' :  'detailed',
        'detailed' :  [
            ['PDB', 'ihm_poly_probe_conjugate_position_id_fkey'], 
        ],
    })

    # ----------------------------
    schema.tables["ihm_poly_probe_position"].foreign_keys[(schema,"ihm_poly_probe_position_mut_res_chem_comp_id_fk")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })

    # ----------------------------
    schema.tables["ihm_poly_probe_position"].foreign_keys[(schema,"ihm_poly_probe_position_mut_res_chem_comp_id_fkey")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })

    # ----------------------------
    schema.tables["ihm_poly_probe_position"].foreign_keys[(schema,"ihm_poly_probe_position_mod_res_chem_comp_descriptor_id_fk")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })

    # ----------------------------
    schema.tables["ihm_poly_probe_position"].foreign_keys[(schema,"ihm_poly_probe_position_mod_res_chem_comp_descriptor_id_fkey")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })

    # ----------------------------
    schema.tables["ihm_poly_probe_position"].foreign_keys[(schema,"ihm_poly_probe_position_mm_poly_res_label_fkey")].foreign_key.update({
        'template_engine' :  'handlebars',
        'domain_filter_pattern' :  '{{#if _structure_id}}structure_id={{{_structure_id}}}{{/if}}',
    })


# -- -----------------------------------------------------------------------------
def update_PDB_ihm_poly_residue_feature(model):
    schema = model.schemas["PDB"]
    table = schema.tables["ihm_poly_residue_feature"]
    # ----------------------------
    schema.tables["ihm_poly_residue_feature"].display.update(
        {'name' : 'Molecular Features - Polymeric Residues', 'comment_display' : {'*': {'table_comment_display': 'inline'}}, }
    )
    
    # ----------------------------
    schema.tables["ihm_poly_residue_feature"].visible_columns.update({
        '*' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_poly_residue_feature_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'ordinal_id', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_poly_residue_feature_feature_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_feature_list.feature_id.',
                'markdown_name' : 'Feature Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_poly_residue_feature_mm_poly_res_label_begin_fkey']}, 'entity_id'],
                'comment' : 'A reference to table entity_poly_seq.entity_id',
                'markdown_name' : 'Entity Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_poly_residue_feature_asym_id_fkey']}, 'RID'],
                'comment' : 'A reference to table struct_asym.id.',
                'markdown_name' : 'Asym Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_poly_residue_feature_mm_poly_res_label_begin_fkey']}, 'mon_id'],
                'comment' : 'A reference to table entity_poly_seq.mon_id',
                'markdown_name' : 'Component Id Begin',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_poly_residue_feature_mm_poly_res_label_end_fkey']}, 'mon_id'],
                'comment' : 'A reference to table entity_poly_seq.mon_id',
                'markdown_name' : 'Component Id End',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_poly_residue_feature_mm_poly_res_label_begin_fkey']}, 'num'],
                'comment' : 'A reference to table entity_poly_seq.num',
                'markdown_name' : 'Sequence Id Begin',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_poly_residue_feature_mm_poly_res_label_end_fkey']}, 'num'],
                'comment' : 'A reference to table entity_poly_seq.num',
                'markdown_name' : 'Sequence Id End',
            },
            ['PDB', 'ihm_poly_residue_feature_rep_atom_fkey'], 
            ['PDB', 'ihm_poly_residue_feature_residue_range_granularity_fkey'], 
            ['PDB', 'ihm_poly_residue_feature_interface_residue_flag_fkey'], 
            {
                'source' : [{'outbound': ['PDB', 'ihm_poly_residue_feature_mm_poly_res_label_begin_fkey']}, 'RID'],
                'comment' : 'Refers to a combination of Entity Id, Sequence Id and Component Id in the entity_poly_seq table.',
                'markdown_name' : 'Polymeric Residue Begin',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_poly_residue_feature_mm_poly_res_label_end_fkey']}, 'RID'],
                'comment' : 'Refers to a combination of Entity Id, Sequence Id and Component Id in the entity_poly_seq table.',
                'markdown_name' : 'Polymeric Residue End',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_poly_residue_feature_Entry_Related_File_fkey']}, 'RID'],
                'comment' : 'A reference to the uploaded restraint file in the table Entry_Related_File.id.',
                'markdown_name' : 'Uploaded Restraint File',
            },
        ],
        'entry' :  [
            {
                'source' : [{'outbound': ['PDB', 'ihm_poly_residue_feature_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'ordinal_id', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_poly_residue_feature_feature_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_feature_list.feature_id.',
                'markdown_name' : 'Feature Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_poly_residue_feature_mm_poly_res_label_begin_fkey']}, 'entity_id'],
                'comment' : 'A reference to table entity_poly_seq.entity_id',
                'markdown_name' : 'Entity Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_poly_residue_feature_asym_id_fkey']}, 'RID'],
                'comment' : 'A reference to table struct_asym.id.',
                'markdown_name' : 'Asym Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_poly_residue_feature_mm_poly_res_label_begin_fkey']}, 'mon_id'],
                'comment' : 'A reference to table entity_poly_seq.mon_id',
                'markdown_name' : 'Component Id Begin',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_poly_residue_feature_mm_poly_res_label_end_fkey']}, 'mon_id'],
                'comment' : 'A reference to table entity_poly_seq.mon_id',
                'markdown_name' : 'Component Id End',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_poly_residue_feature_mm_poly_res_label_begin_fkey']}, 'num'],
                'comment' : 'A reference to table entity_poly_seq.num',
                'markdown_name' : 'Sequence Id Begin',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_poly_residue_feature_mm_poly_res_label_end_fkey']}, 'num'],
                'comment' : 'A reference to table entity_poly_seq.num',
                'markdown_name' : 'Sequence Id End',
            },
            ['PDB', 'ihm_poly_residue_feature_rep_atom_fkey'], 
            ['PDB', 'ihm_poly_residue_feature_residue_range_granularity_fkey'], 
            ['PDB', 'ihm_poly_residue_feature_interface_residue_flag_fkey'], 
            {
                'source' : [{'outbound': ['PDB', 'ihm_poly_residue_feature_mm_poly_res_label_begin_fkey']}, 'RID'],
                'comment' : 'Refers to a combination of Entity Id, Sequence Id and Component Id in the entity_poly_seq table.',
                'markdown_name' : 'Polymeric Residue Begin',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_poly_residue_feature_mm_poly_res_label_end_fkey']}, 'RID'],
                'comment' : 'Refers to a combination of Entity Id, Sequence Id and Component Id in the entity_poly_seq table.',
                'markdown_name' : 'Polymeric Residue End',
            },
        ],
        'detailed' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_poly_residue_feature_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'ordinal_id', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_poly_residue_feature_feature_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_feature_list.feature_id.',
                'markdown_name' : 'Feature Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_poly_residue_feature_mm_poly_res_label_begin_fkey']}, 'entity_id'],
                'comment' : 'A reference to table entity_poly_seq.entity_id',
                'markdown_name' : 'Entity Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_poly_residue_feature_asym_id_fkey']}, 'RID'],
                'comment' : 'A reference to table struct_asym.id.',
                'markdown_name' : 'Asym Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_poly_residue_feature_mm_poly_res_label_begin_fkey']}, 'mon_id'],
                'comment' : 'A reference to table entity_poly_seq.mon_id',
                'markdown_name' : 'Component Id Begin',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_poly_residue_feature_mm_poly_res_label_end_fkey']}, 'mon_id'],
                'comment' : 'A reference to table entity_poly_seq.mon_id',
                'markdown_name' : 'Component Id End',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_poly_residue_feature_mm_poly_res_label_begin_fkey']}, 'num'],
                'comment' : 'A reference to table entity_poly_seq.num',
                'markdown_name' : 'Sequence Id Begin',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_poly_residue_feature_mm_poly_res_label_end_fkey']}, 'num'],
                'comment' : 'A reference to table entity_poly_seq.num',
                'markdown_name' : 'Sequence Id End',
            },
            ['PDB', 'ihm_poly_residue_feature_rep_atom_fkey'], 
            ['PDB', 'ihm_poly_residue_feature_residue_range_granularity_fkey'], 
            ['PDB', 'ihm_poly_residue_feature_interface_residue_flag_fkey'], 
            {
                'source' : [{'outbound': ['PDB', 'ihm_poly_residue_feature_mm_poly_res_label_begin_fkey']}, 'RID'],
                'comment' : 'Refers to a combination of Entity Id, Sequence Id and Component Id in the entity_poly_seq table.',
                'markdown_name' : 'Polymeric Residue Begin',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_poly_residue_feature_mm_poly_res_label_end_fkey']}, 'RID'],
                'comment' : 'Refers to a combination of Entity Id, Sequence Id and Component Id in the entity_poly_seq table.',
                'markdown_name' : 'Polymeric Residue End',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_poly_residue_feature_Entry_Related_File_fkey']}, 'RID'],
                'comment' : 'A reference to the uploaded restraint file in the table Entry_Related_File.id.',
                'markdown_name' : 'Uploaded Restraint File',
            },
            ['PDB', 'ihm_poly_residue_feature_RCB_fkey'], 
            ['PDB', 'ihm_poly_residue_feature_RMB_fkey'], 
            'RCT', 
            'RMT', 
            ['PDB', 'ihm_poly_residue_feature_Owner_fkey'], 
        ],
    })

    # ----------------------------
    schema.tables["ihm_poly_residue_feature"].columns["rep_atom"].display.update(
        {'name' : 'Representative Atom', }
    )

    # ----------------------------
    schema.tables["ihm_poly_residue_feature"].foreign_keys[(schema,"ihm_poly_residue_feature_feature_id_fkey")].foreign_key.update({
        'template_engine' :  'handlebars',
        'domain_filter_pattern' :  '{{#if _structure_id}}structure_id={{{_structure_id}}}{{/if}}',
    })

    # ----------------------------
    schema.tables["ihm_poly_residue_feature"].foreign_keys[(schema,"ihm_poly_residue_feature_asym_id_fk")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })

    # ----------------------------
    schema.tables["ihm_poly_residue_feature"].foreign_keys[(schema,"ihm_poly_residue_feature_mm_poly_res_label_begin_fkey")].foreign_key.update({
        'from_name' :  'Ihm Poly Contact Residue Feature Begin',
        'template_engine' :  'handlebars',
        'domain_filter_pattern' :  '{{#if _structure_id}}structure_id={{{_structure_id}}}{{/if}}',
    })

    # ----------------------------
    schema.tables["ihm_poly_residue_feature"].foreign_keys[(schema,"ihm_poly_residue_feature_mm_poly_res_label_end_fkey")].foreign_key.update({
        'from_name' :  'Ihm Poly Contact Residue Feature End',
        'template_engine' :  'handlebars',
        'domain_filter_pattern' :  '{{#if _structure_id}}structure_id={{{_structure_id}}}{{/if}}',
    })

    # ----------------------------
    schema.tables["ihm_poly_residue_feature"].foreign_keys[(schema,"ihm_poly_residue_feature_asym_id_fkey")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })


# -- -----------------------------------------------------------------------------
def update_PDB_ihm_predicted_contact_restraint(model):
    schema = model.schemas["PDB"]
    table = schema.tables["ihm_predicted_contact_restraint"]
    # ----------------------------
    schema.tables["ihm_predicted_contact_restraint"].display.update(
        {'name' : 'Predicted Contact Restraints', 'comment_display' : {'*': {'table_comment_display': 'inline'}}, }
    )

    # ----------------------------
    schema.tables["ihm_predicted_contact_restraint"].visible_columns.update({
        '*' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_predicted_contact_restraint_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'id', 
            'group_id', 
            'entity_description_1', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_predicted_contact_restraint_mm_poly_res_label_1_fkey']}, 'entity_id'],
                'comment' : 'A reference to table entity_poly_seq.entity_id.',
                'markdown_name' : 'Entity Id 1',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_predicted_contact_restraint_asym_id_1_fkey']}, 'RID'],
                'comment' : 'A reference to table struct_asym.id.',
                'markdown_name' : 'Asym Id 1',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_predicted_contact_restraint_mm_poly_res_label_1_fkey']}, 'mon_id'],
                'comment' : 'A reference to table entity_poly_seq.mon_id',
                'markdown_name' : 'Component Id 1',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_predicted_contact_restraint_mm_poly_res_label_1_fkey']}, 'num'],
                'comment' : 'A reference to table entity_poly_seq.num',
                'markdown_name' : 'Sequence Id 1',
            },
            ['PDB', 'ihm_predicted_contact_restraint_rep_atom_1_fkey'], 
            'entity_description_2', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_predicted_contact_restraint_mm_poly_res_label_2_fkey']}, 'entity_id'],
                'comment' : 'A reference to table entity_poly_seq.entity_id',
                'markdown_name' : 'Entity Id 2',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_predicted_contact_restraint_asym_id_2_fkey']}, 'RID'],
                'comment' : 'A reference to table struct_asym.id.',
                'markdown_name' : 'Asym Id 2',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_predicted_contact_restraint_mm_poly_res_label_2_fkey']}, 'mon_id'],
                'comment' : 'A reference to table entity_poly_seq.mon_id',
                'markdown_name' : 'Component Id 2',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_predicted_contact_restraint_mm_poly_res_label_2_fkey']}, 'num'],
                'comment' : 'A reference to table entity_poly_seq.num',
                'markdown_name' : 'Sequence Id 2',
            },
            ['PDB', 'ihm_predicted_contact_restraint_rep_atom_2_fkey'], 
            ['PDB', 'ihm_predicted_contact_restraint_restraint_type_fkey'], 
            'distance_lower_limit', 
            'distance_upper_limit', 
            'probability', 
            ['PDB', 'ihm_predicted_contact_restraint_model_granularity_fkey'], 
            {
                'source' : [{'outbound': ['PDB', 'ihm_predicted_contact_restraint_software_id_fkey']}, 'RID'],
                'comment' : 'A reference to table software.pdbx_ordinal.',
                'markdown_name' : 'Software Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_predicted_contact_restraint_dataset_list_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_dataset_list.id.',
                'markdown_name' : 'Dataset List Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_predicted_contact_restraint_mm_poly_res_label_1_fkey']}, 'RID'],
                'comment' : 'Refers to a combination of Entity Id, Sequence Id and Component Id in the entity_poly_seq table.',
                'markdown_name' : 'Polymeric Residue 1',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_predicted_contact_restraint_mm_poly_res_label_2_fkey']}, 'RID'],
                'comment' : 'Refers to a combination of Entity Id, Sequence Id and Component Id in the entity_poly_seq table.',
                'markdown_name' : 'Polymeric Residue 2',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_predicted_contact_restraint_Entry_Related_File_fkey']}, 'RID'],
                'comment' : 'A reference to the uploaded restraint file in the table Entry_Related_File.id.',
                'markdown_name' : 'Uploaded Restraint File',
            },
        ],
        'entry' :  [
            {
                'source' : [{'outbound': ['PDB', 'ihm_predicted_contact_restraint_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'id', 
            'group_id', 
            'entity_description_1', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_predicted_contact_restraint_mm_poly_res_label_1_fkey']}, 'entity_id'],
                'comment' : 'A reference to table entity_poly_seq.entity_id.',
                'markdown_name' : 'Entity Id 1',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_predicted_contact_restraint_asym_id_1_fkey']}, 'RID'],
                'comment' : 'A reference to table struct_asym.id.',
                'markdown_name' : 'Asym Id 1',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_predicted_contact_restraint_mm_poly_res_label_1_fkey']}, 'mon_id'],
                'comment' : 'A reference to table entity_poly_seq.mon_id',
                'markdown_name' : 'Component Id 1',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_predicted_contact_restraint_mm_poly_res_label_1_fkey']}, 'num'],
                'comment' : 'A reference to table entity_poly_seq.num',
                'markdown_name' : 'Sequence Id 1',
            },
            ['PDB', 'ihm_predicted_contact_restraint_rep_atom_1_fkey'], 
            'entity_description_2', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_predicted_contact_restraint_mm_poly_res_label_2_fkey']}, 'entity_id'],
                'comment' : 'A reference to table entity_poly_seq.entity_id',
                'markdown_name' : 'Entity Id 2',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_predicted_contact_restraint_asym_id_2_fkey']}, 'RID'],
                'comment' : 'A reference to table struct_asym.id.',
                'markdown_name' : 'Asym Id 2',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_predicted_contact_restraint_mm_poly_res_label_2_fkey']}, 'mon_id'],
                'comment' : 'A reference to table entity_poly_seq.mon_id',
                'markdown_name' : 'Component Id 2',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_predicted_contact_restraint_mm_poly_res_label_2_fkey']}, 'mon_id'],
                'comment' : 'A reference to table entity_poly_seq.num',
                'markdown_name' : 'Sequence Id 2',
            },
            ['PDB', 'ihm_predicted_contact_restraint_rep_atom_2_fkey'], 
            ['PDB', 'ihm_predicted_contact_restraint_restraint_type_fkey'], 
            'distance_lower_limit', 
            'distance_upper_limit', 
            'probability', 
            ['PDB', 'ihm_predicted_contact_restraint_model_granularity_fkey'], 
            {
                'source' : [{'outbound': ['PDB', 'ihm_predicted_contact_restraint_software_id_fkey']}, 'RID'],
                'comment' : 'A reference to table software.pdbx_ordinal.',
                'markdown_name' : 'Software Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_predicted_contact_restraint_dataset_list_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_dataset_list.id.',
                'markdown_name' : 'Dataset List Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_predicted_contact_restraint_mm_poly_res_label_1_fkey']}, 'RID'],
                'comment' : 'Refers to a combination of Entity Id, Sequence Id and Component Id in the entity_poly_seq table.',
                'markdown_name' : 'Polymeric Residue 1',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_predicted_contact_restraint_mm_poly_res_label_2_fkey']}, 'RID'],
                'comment' : 'Refers to a combination of Entity Id, Sequence Id and Component Id in the entity_poly_seq table.',
                'markdown_name' : 'Polymeric Residue 2',
            },
        ],
        'detailed' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_predicted_contact_restraint_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'id', 
            'group_id', 
            'entity_description_1', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_predicted_contact_restraint_mm_poly_res_label_1_fkey']}, 'entity_id'],
                'comment' : 'A reference to table entity_poly_seq.entity_id.',
                'markdown_name' : 'Entity Id 1',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_predicted_contact_restraint_asym_id_1_fkey']}, 'RID'],
                'comment' : 'A reference to table struct_asym.id.',
                'markdown_name' : 'Asym Id 1',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_predicted_contact_restraint_mm_poly_res_label_1_fkey']}, 'mon_id'],
                'comment' : 'A reference to table entity_poly_seq.mon_id',
                'markdown_name' : 'Component Id 1',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_predicted_contact_restraint_mm_poly_res_label_1_fkey']}, 'num'],
                'comment' : 'A reference to table entity_poly_seq.num',
                'markdown_name' : 'Sequence Id 1',
            },
            ['PDB', 'ihm_predicted_contact_restraint_rep_atom_1_fkey'], 
            'entity_description_2', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_predicted_contact_restraint_mm_poly_res_label_2_fkey']}, 'entity_id'],
                'comment' : 'A reference to table entity_poly_seq.entity_id',
                'markdown_name' : 'Entity Id 2',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_predicted_contact_restraint_asym_id_2_fkey']}, 'RID'],
                'comment' : 'A reference to table struct_asym.id.',
                'markdown_name' : 'Asym Id 2',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_predicted_contact_restraint_mm_poly_res_label_2_fkey']}, 'mon_id'],
                'comment' : 'A reference to table entity_poly_seq.mon_id',
                'markdown_name' : 'Component Id 2',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_predicted_contact_restraint_mm_poly_res_label_2_fkey']}, 'mon_id'],
                'comment' : 'A reference to table entity_poly_seq.num',
                'markdown_name' : 'Sequence Id 2',
            },
            ['PDB', 'ihm_predicted_contact_restraint_rep_atom_2_fkey'], 
            ['PDB', 'ihm_predicted_contact_restraint_restraint_type_fkey'], 
            'distance_lower_limit', 
            'distance_upper_limit', 
            'probability', 
            ['PDB', 'ihm_predicted_contact_restraint_model_granularity_fkey'], 
            {
                'source' : [{'outbound': ['PDB', 'ihm_predicted_contact_restraint_software_id_fkey']}, 'RID'],
                'comment' : 'A reference to table software.pdbx_ordinal.',
                'markdown_name' : 'Software Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_predicted_contact_restraint_dataset_list_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_dataset_list.id.',
                'markdown_name' : 'Dataset List Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_predicted_contact_restraint_mm_poly_res_label_1_fkey']}, 'RID'],
                'comment' : 'Refers to a combination of Entity Id, Sequence Id and Component Id in the entity_poly_seq table.',
                'markdown_name' : 'Polymeric Residue 1',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_predicted_contact_restraint_mm_poly_res_label_2_fkey']}, 'RID'],
                'comment' : 'Refers to a combination of Entity Id, Sequence Id and Component Id in the entity_poly_seq table.',
                'markdown_name' : 'Polymeric Residue 2',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_predicted_contact_restraint_Entry_Related_File_fkey']}, 'RID'],
                'comment' : 'A reference to the uploaded restraint file in the table Entry_Related_File.id.',
                'markdown_name' : 'Uploaded Restraint File',
            },
            ['PDB', 'ihm_predicted_contact_restraint_RCB_fkey'], 
            ['PDB', 'ihm_predicted_contact_restraint_RMB_fkey'], 
            'RCT', 
            'RMT', 
            ['PDB', 'ihm_predicted_contact_restraint_Owner_fkey'], 
        ],
    })

    # ----------------------------
    schema.tables["ihm_predicted_contact_restraint"].columns["rep_atom_1"].display.update(
        {'name' : 'Representative Atom 1', }
    )
    
    # ----------------------------
    schema.tables["ihm_predicted_contact_restraint"].columns["rep_atom_2"].display.update(
        {'name' : 'Representative Atom 2', }
    )
    
    # ----------------------------
    schema.tables["ihm_predicted_contact_restraint"].foreign_keys[(schema,"ihm_predicted_contact_restraint_asym_id_1_fkey")].foreign_key.update({
        'template_engine' :  'handlebars',
        'domain_filter_pattern' :  '{{#if _structure_id}}structure_id={{{_structure_id}}}{{/if}}',
    })

    # ----------------------------
    schema.tables["ihm_predicted_contact_restraint"].foreign_keys[(schema,"ihm_predicted_contact_restraint_software_id_fk")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })

    # ----------------------------
    schema.tables["ihm_predicted_contact_restraint"].foreign_keys[(schema,"ihm_predicted_contact_restraint_dataset_list_id_fkey")].foreign_key.update({
        'template_engine' :  'handlebars',
        'domain_filter_pattern' :  '{{#if _structure_id}}structure_id={{{_structure_id}}}{{/if}}',
    })

    # ----------------------------
    schema.tables["ihm_predicted_contact_restraint"].foreign_keys[(schema,"ihm_predicted_contact_restraint_asym_id_2_fkey")].foreign_key.update({
        'template_engine' :  'handlebars',
        'domain_filter_pattern' :  '{{#if _structure_id}}structure_id={{{_structure_id}}}{{/if}}',
    })

    # ----------------------------
    schema.tables["ihm_predicted_contact_restraint"].foreign_keys[(schema,"ihm_predicted_contact_restraint_mm_poly_res_label_2_fkey")].foreign_key.update({
        'from_name' :  'Ihm Predicted Contact Restraint Label 2',
        'template_engine' :  'handlebars',
        'domain_filter_pattern' :  '{{#if _structure_id}}structure_id={{{_structure_id}}}{{/if}}',
    })

    # ----------------------------
    schema.tables["ihm_predicted_contact_restraint"].foreign_keys[(schema,"ihm_predicted_contact_restraint_software_id_fkey")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })
    
    # ----------------------------
    schema.tables["ihm_predicted_contact_restraint"].foreign_keys[(schema,"ihm_predicted_contact_restraint_mm_poly_res_label_1_fkey")].foreign_key.update({
        'from_name' :  'Ihm Predicted Contact Restraint Label 1',
        'template_engine' :  'handlebars',
        'domain_filter_pattern' :  '{{#if _structure_id}}structure_id={{{_structure_id}}}{{/if}}',
    })


# -- -----------------------------------------------------------------------------
def update_PDB_ihm_probe_list(model):
    schema = model.schemas["PDB"]
    table = schema.tables["ihm_probe_list"]
    # ----------------------------
    schema.tables["ihm_probe_list"].display.update(
        {'name' : 'Molecular Probes', 'comment_display' : {'*': {'table_comment_display': 'inline'}}, }
    )

    # ----------------------------
    schema.tables["ihm_probe_list"].visible_columns.update({
        '*' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_probe_list_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'probe_id', 
            'probe_name', 
            ['PDB', 'ihm_probe_list_reactive_probe_flag_fkey'], 
            'reactive_probe_name', 
            ['PDB', 'ihm_probe_list_probe_origin_fkey'], 
            ['PDB', 'ihm_probe_list_probe_link_type_fkey'], 
            {
                'source' : [{'outbound': ['PDB', 'ihm_probe_list_probe_chem_comp_descriptor_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_chemical_component_descriptor.id.',
                'markdown_name' : 'Probe Chemical Component Descriptor Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_probe_list_reactive_probe_chem_comp_descriptor_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_chemical_component_descriptor.id.',
                'markdown_name' : 'Reactive Probe Chemical Component Descriptor Id',
            },
        ],
        'entry' :  [
            {
                'source' : [{'outbound': ['PDB', 'ihm_probe_list_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'probe_id', 
            'probe_name', 
            ['PDB', 'ihm_probe_list_reactive_probe_flag_fkey'], 
            'reactive_probe_name', 
            ['PDB', 'ihm_probe_list_probe_origin_fkey'], 
            ['PDB', 'ihm_probe_list_probe_link_type_fkey'], 
            {
                'source' : [{'outbound': ['PDB', 'ihm_probe_list_probe_chem_comp_descriptor_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_chemical_component_descriptor.id.',
                'markdown_name' : 'Probe Chemical Component Descriptor Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_probe_list_reactive_probe_chem_comp_descriptor_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_chemical_component_descriptor.id.',
                'markdown_name' : 'Reactive Probe Chemical Component Descriptor Id',
            },
        ],
        'detailed' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_probe_list_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'probe_id', 
            'probe_name', 
            ['PDB', 'ihm_probe_list_reactive_probe_flag_fkey'], 
            'reactive_probe_name', 
            ['PDB', 'ihm_probe_list_probe_origin_fkey'], 
            ['PDB', 'ihm_probe_list_probe_link_type_fkey'], 
            {
                'source' : [{'outbound': ['PDB', 'ihm_probe_list_probe_chem_comp_descriptor_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_chemical_component_descriptor.id.',
                'markdown_name' : 'Probe Chemical Component Descriptor Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_probe_list_reactive_probe_chem_comp_descriptor_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_chemical_component_descriptor.id.',
                'markdown_name' : 'Reactive Probe Chemical Component Descriptor Id',
            },
            ['PDB', 'ihm_probe_list_RCB_fkey'], 
            ['PDB', 'ihm_probe_list_RMB_fkey'], 
            'RCT', 
            'RMT', 
            ['PDB', 'ihm_probe_list_Owner_fkey'], 
        ],
    })

    # ----------------------------
    schema.tables["ihm_probe_list"].visible_foreign_keys.update(
    {
        'filter' :  'detailed',
        'detailed' :  [
            ['PDB', 'ihm_poly_probe_conjugate_probe_id_fkey'], 
            ['PDB', 'ihm_ligand_probe_probe_id_fkey'], 
        ],
    })

    # ----------------------------
    schema.tables["ihm_probe_list"].foreign_keys[(schema,"ihm_probe_list_probe_chem_comp_descriptor_id_fkey")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })

    # ----------------------------
    schema.tables["ihm_probe_list"].foreign_keys[(schema,"ihm_probe_list_probe_chem_comp_descriptor_id_fk")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })

    # ----------------------------
    schema.tables["ihm_probe_list"].foreign_keys[(schema,"ihm_probe_list_reactive_probe_chem_comp_descriptor_id_fkey")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })

    # ----------------------------
    schema.tables["ihm_probe_list"].foreign_keys[(schema,"ihm_probe_list_reactive_probe_chem_comp_descriptor_id_fk")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })


# -- -----------------------------------------------------------------------------
def update_PDB_ihm_pseudo_site(model):
    schema = model.schemas["PDB"]
    table = schema.tables["ihm_pseudo_site"]
    # ----------------------------
    schema.tables["ihm_pseudo_site"].display.update(
        {'name' : 'Pseudo Site Coordinates', 'comment_display' : {'*': {'table_comment_display': 'inline'}}, }
    )

    # ----------------------------
    schema.tables["ihm_pseudo_site"].visible_columns.update({
        '*' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_pseudo_site_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'id', 
            'Cartn_x', 
            'Cartn_y', 
            'Cartn_z', 
            'radius', 
            'description', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_pseudo_site_Entry_Related_File_fkey']}, 'RID'],
                'comment' : 'A reference to the uploaded restraint file in the table Entry_Related_File.id.',
                'markdown_name' : 'Uploaded Restraint File',
            },
        ],
        'entry' :  [
            {
                'source' : [{'outbound': ['PDB', 'ihm_pseudo_site_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'id', 
            'Cartn_x', 
            'Cartn_y', 
            'Cartn_z', 
            'radius', 
            'description', 
        ],
        'detailed' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_pseudo_site_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'id', 
            'Cartn_x', 
            'Cartn_y', 
            'Cartn_z', 
            'radius', 
            'description', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_pseudo_site_Entry_Related_File_fkey']}, 'RID'],
                'comment' : 'A reference to the uploaded restraint file in the table Entry_Related_File.id.',
                'markdown_name' : 'Uploaded Restraint File',
            },
            ['PDB', 'ihm_pseudo_site_RCB_fkey'], 
            ['PDB', 'ihm_pseudo_site_RMB_fkey'], 
            'RCT', 
            'RMT', 
            ['PDB', 'ihm_pseudo_site_Owner_fkey'], 
        ],
    })

    # ----------------------------
    schema.tables["ihm_pseudo_site"].visible_foreign_keys.update({
        'filter' :  'detailed',
        'detailed' :  [
            ['PDB', 'ihm_cross_link_pseudo_site_ihm_pseudo_site_combo1_fkey'], 
            ['PDB', 'ihm_pseudo_site_feature_ihm_pseudo_site_combo1_fkey'], 
        ],
    })


# -- -----------------------------------------------------------------------------
def update_PDB_ihm_pseudo_site_feature(model):
    schema = model.schemas["PDB"]
    table = schema.tables["ihm_pseudo_site_feature"]
    # ----------------------------
    schema.tables["ihm_pseudo_site_feature"].display.update(
        {'name' : 'Molecular Features - Pseudo Sites', 'comment_display' : {'*': {'table_comment_display': 'inline'}}, }
    )

    # ----------------------------
    schema.tables["ihm_pseudo_site_feature"].visible_columns.update({
        '*' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_pseudo_site_feature_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_pseudo_site_feature_ihm_feature_list_combo1_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_feature_list.feature_id.',
                'markdown_name' : 'Feature Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_pseudo_site_feature_ihm_pseudo_site_combo1_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_pseudo_site.id.',
                'markdown_name' : 'Pseudo Site Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_pseudo_site_feature_Entry_Related_File_fkey']}, 'RID'],
                'comment' : 'A reference to the uploaded restraint file in the table Entry_Related_File.id.',
                'markdown_name' : 'Uploaded Restraint File',
            },
        ],
        'entry' :  [
            {
                'source' : [{'outbound': ['PDB', 'ihm_pseudo_site_feature_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_pseudo_site_feature_ihm_feature_list_combo1_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_feature_list.feature_id.',
                'markdown_name' : 'Feature Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_pseudo_site_feature_ihm_pseudo_site_combo1_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_pseudo_site.id.',
                'markdown_name' : 'Pseudo Site Id',
            },
        ],
        'detailed' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_pseudo_site_feature_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_pseudo_site_feature_ihm_feature_list_combo1_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_feature_list.feature_id.',
                'markdown_name' : 'Feature Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_pseudo_site_feature_ihm_pseudo_site_combo1_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_pseudo_site.id.',
                'markdown_name' : 'Pseudo Site Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_pseudo_site_feature_Entry_Related_File_fkey']}, 'RID'],
                'comment' : 'A reference to the uploaded restraint file in the table Entry_Related_File.id.',
                'markdown_name' : 'Uploaded Restraint File',
            },
            ['PDB', 'ihm_pseudo_site_feature_RCB_fkey'], 
            ['PDB', 'ihm_pseudo_site_feature_RMB_fkey'], 
            'RCT', 
            'RMT', 
            ['PDB', 'ihm_pseudo_site_feature_Owner_fkey'], 
        ],
    })

    # ----------------------------
    schema.tables["ihm_pseudo_site_feature"].foreign_keys[(schema,"ihm_pseudo_site_feature_ihm_pseudo_site_combo1_fkey")].foreign_key.update({
        'template_engine' :  'handlebars',
        'domain_filter_pattern' :  '{{#if _structure_id}}structure_id={{{_structure_id}}}{{/if}}',
    })

    # ----------------------------
    schema.tables["ihm_pseudo_site_feature"].foreign_keys[(schema,"ihm_pseudo_site_feature_ihm_feature_list_combo1_fkey")].foreign_key.update({
        'template_engine' :  'handlebars',
        'domain_filter_pattern' :  '{{#if _structure_id}}structure_id={{{_structure_id}}}{{/if}}',
    })


# -- -----------------------------------------------------------------------------
def update_PDB_ihm_related_datasets(model):
    schema = model.schemas["PDB"]
    table = schema.tables["ihm_related_datasets"]
    # ----------------------------
    schema.tables["ihm_related_datasets"].display.update(
        {'name' : 'Datasets Derived from Another', 'comment_display' : {'*': {'table_comment_display': 'inline'}}, }
    )
    
    # ----------------------------
    schema.tables["ihm_related_datasets"].visible_columns.update({
        '*' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_related_datasets_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_related_datasets_dataset_list_id_derived_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_dataset_list.id.',
                'markdown_name' : 'Derived Dataset List Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_related_datasets_dataset_list_id_primary_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_dataset_list.id.',
                'markdown_name' : 'Primary Dataset List Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_related_datasets_ihm_data_transformation_combo2_fkey']}, 'RID'],
                'comment' : 'Identifier corresponding to the transformation matrix to be applied to the derived dataset in order to transform it to the primary dataset',
                'markdown_name' : 'Data Transformation Id',
            },
        ],
        'entry' :  [
            {
                'source' : [{'outbound': ['PDB', 'ihm_related_datasets_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_related_datasets_dataset_list_id_derived_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_dataset_list.id.',
                'markdown_name' : 'Derived Dataset List Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_related_datasets_dataset_list_id_primary_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_dataset_list.id.',
                'markdown_name' : 'Primary Dataset List Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_related_datasets_ihm_data_transformation_combo2_fkey']}, 'RID'],
                'comment' : 'Identifier corresponding to the transformation matrix to be applied to the derived dataset in order to transform it to the primary dataset',
                'markdown_name' : 'Data Transformation Id',
            },
        ],
        'detailed' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_related_datasets_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_related_datasets_dataset_list_id_derived_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_dataset_list.id.',
                'markdown_name' : 'Derived Dataset List Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_related_datasets_dataset_list_id_primary_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_dataset_list.id.',
                'markdown_name' : 'Primary Dataset List Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_related_datasets_ihm_data_transformation_combo2_fkey']}, 'RID'],
                'comment' : 'Identifier corresponding to the transformation matrix to be applied to the derived dataset in order to transform it to the primary dataset',
                'markdown_name' : 'Data Transformation Id',
            },
            ['PDB', 'ihm_related_datasets_RCB_fkey'], 
            ['PDB', 'ihm_related_datasets_RMB_fkey'], 
            'RCT', 
            'RMT', 
            ['PDB', 'ihm_related_datasets_Owner_fkey'], 
        ],
    })

    # ----------------------------
    schema.tables["ihm_related_datasets"].foreign_keys[(schema,"ihm_related_datasets_dataset_list_id_derived_fkey")].foreign_key.update({
        'template_engine' :  'handlebars',
        'domain_filter_pattern' :  '{{#if _structure_id}}structure_id={{{_structure_id}}}{{/if}}',
    })

    # ----------------------------
    schema.tables["ihm_related_datasets"].foreign_keys[(schema,"ihm_related_datasets_ihm_data_transformation_combo2_fkey")].foreign_key.update({
        'template_engine' :  'handlebars',
        'domain_filter_pattern' :  '{{#if _structure_id}}structure_id={{{_structure_id}}}{{/if}}',
    })

    # ----------------------------
    schema.tables["ihm_related_datasets"].foreign_keys[(schema,"ihm_related_datasets_dataset_list_id_primary_fkey")].foreign_key.update({
        'template_engine' :  'handlebars',
        'domain_filter_pattern' :  '{{#if _structure_id}}structure_id={{{_structure_id}}}{{/if}}',
    })


# -- -----------------------------------------------------------------------------
def update_PDB_ihm_relaxation_time(model):
    schema = model.schemas["PDB"]
    table = schema.tables["ihm_relaxation_time"]
    # ----------------------------
    schema.tables["ihm_relaxation_time"].display.update(
        {'name' : 'Relaxation times from Biophysical Experiments', 'comment_display' : {'*': {'table_comment_display': 'inline'}}, }
    )
    
    # ----------------------------
    schema.tables["ihm_relaxation_time"].visible_columns.update({
        '*' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_relaxation_time_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'id', 
            'value', 
            ['PDB', 'ihm_relaxation_time_unit_fkey'], 
            'amplitude', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_relaxation_time_ihm_external_files_combo2_fkey']}, 'RID'],
                'comment' : 'Identifier for the external file corresponding to the relaxation time measurement',
                'markdown_name' : 'External File Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_relaxation_time_ihm_dataset_group_combo1_fkey']}, 'RID'],
                'comment' : 'Identifier for the dataset group from which the multi-state scheme is obtained',
                'markdown_name' : 'Dataset Group Id',
            },
            'details', 
        ],
        'entry' :  [
            {
                'source' : [{'outbound': ['PDB', 'ihm_relaxation_time_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'id', 
            'value', 
            ['PDB', 'ihm_relaxation_time_unit_fkey'], 
            'amplitude', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_relaxation_time_ihm_external_files_combo2_fkey']}, 'RID'],
                'comment' : 'Identifier for the external file corresponding to the relaxation time measurement',
                'markdown_name' : 'External File Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_relaxation_time_ihm_dataset_group_combo1_fkey']}, 'RID'],
                'comment' : 'Identifier for the dataset group from which the multi-state scheme is obtained',
                'markdown_name' : 'Dataset Group Id',
            },
            'details', 
        ],
        'detailed' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_relaxation_time_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'id', 
            'value', 
            ['PDB', 'ihm_relaxation_time_unit_fkey'], 
            'amplitude', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_relaxation_time_ihm_external_files_combo2_fkey']}, 'RID'],
                'comment' : 'Identifier for the external file corresponding to the relaxation time measurement',
                'markdown_name' : 'External File Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_relaxation_time_ihm_dataset_group_combo1_fkey']}, 'RID'],
                'comment' : 'Identifier for the dataset group from which the multi-state scheme is obtained',
                'markdown_name' : 'Dataset Group Id',
            },
            'details', 
            ['PDB', 'ihm_relaxation_time_RCB_fkey'], 
            ['PDB', 'ihm_relaxation_time_RMB_fkey'], 
            'RCT', 
            'RMT', 
            ['PDB', 'ihm_relaxation_time_Owner_fkey'], 
        ],
    })

    # ----------------------------
    schema.tables["ihm_relaxation_time"].visible_foreign_keys.update({
        'filter' :  'detailed',
        'detailed' :  [
            ['PDB', 'ihm_relaxation_time_multi_state_scheme_time_combo1_fkey'], 
        ],
    })

    # ----------------------------
    schema.tables["ihm_relaxation_time"].foreign_keys[(schema,"ihm_relaxation_time_ihm_external_files_combo2_fkey")].foreign_key.update({
        'template_engine' :  'handlebars',
        'domain_filter_pattern' :  '{{#if _structure_id}}structure_id={{{_structure_id}}}{{/if}}',
    })
    
    # ----------------------------
    schema.tables["ihm_relaxation_time"].foreign_keys[(schema,"ihm_relaxation_time_ihm_dataset_group_combo1_fkey")].foreign_key.update({
        'template_engine' :  'handlebars',
        'domain_filter_pattern' :  '{{#if _structure_id}}structure_id={{{_structure_id}}}{{/if}}',
    })



# -- -----------------------------------------------------------------------------
def update_PDB_ihm_relaxation_time_multi_state_scheme(model):
    schema = model.schemas["PDB"]
    table = schema.tables["ihm_relaxation_time_multi_state_scheme"]
    # ----------------------------
    schema.tables["ihm_relaxation_time_multi_state_scheme"].display.update(
        {'name' : 'Mapping experimentally measured relaxation times with multi-state schemes', 'comment_display' : {'*': {'table_comment_display': 'inline'}}, }
    )
    
    # ----------------------------
    schema.tables["ihm_relaxation_time_multi_state_scheme"].visible_columns.update({
        '*' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_relaxation_time_multi_state_scheme_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'id', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_relaxation_time_multi_state_scheme_scheme_combo1_fkey']}, 'RID'],
                'comment' : 'Identifier for the multi-state scheme',
                'markdown_name' : 'Scheme Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'relaxation_time_multi_state_scheme_connectivity_combo2_fkey']}, 'RID'],
                'comment' : 'Identifier for the multi-state scheme connectivity',
                'markdown_name' : 'Scheme Connectivity Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_relaxation_time_multi_state_scheme_time_combo1_fkey']}, 'RID'],
                'comment' : 'Identifier for the relaxation time',
                'markdown_name' : 'Relaxation Time Id',
            },
            'details', 
        ],
        'entry' :  [
            {
                'source' : [{'outbound': ['PDB', 'ihm_relaxation_time_multi_state_scheme_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'id', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_relaxation_time_multi_state_scheme_scheme_combo1_fkey']}, 'RID'],
                'comment' : 'Identifier for the multi-state scheme',
                'markdown_name' : 'Scheme Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'relaxation_time_multi_state_scheme_connectivity_combo2_fkey']}, 'RID'],
                'comment' : 'Identifier for the multi-state scheme connectivity',
                'markdown_name' : 'Scheme Connectivity Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_relaxation_time_multi_state_scheme_time_combo1_fkey']}, 'RID'],
                'comment' : 'Identifier for the relaxation time',
                'markdown_name' : 'Relaxation Time Id',
            },
            'details', 
        ],
        'detailed' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_relaxation_time_multi_state_scheme_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'id', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_relaxation_time_multi_state_scheme_scheme_combo1_fkey']}, 'RID'],
                'comment' : 'Identifier for the multi-state scheme',
                'markdown_name' : 'Scheme Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'relaxation_time_multi_state_scheme_connectivity_combo2_fkey']}, 'RID'],
                'comment' : 'Identifier for the multi-state scheme connectivity',
                'markdown_name' : 'Scheme Connectivity Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_relaxation_time_multi_state_scheme_time_combo1_fkey']}, 'RID'],
                'comment' : 'Identifier for the relaxation time',
                'markdown_name' : 'Relaxation Time Id',
            },
            'details', 
            ['PDB', 'ihm_relaxation_time_multi_state_scheme_RCB_fkey'], 
            ['PDB', 'ihm_relaxation_time_multi_state_scheme_RMB_fkey'], 
            'RCT', 
            'RMT', 
            ['PDB', 'ihm_relaxation_time_multi_state_scheme_Owner_fkey'], 
        ],
    })

    # ----------------------------
    schema.tables["ihm_relaxation_time_multi_state_scheme"].foreign_keys[(schema,"ihm_relaxation_time_multi_state_scheme_scheme_combo1_fkey")].foreign_key.update({
        'template_engine' :  'handlebars',
        'domain_filter_pattern' :  '{{#if _structure_id}}structure_id={{{_structure_id}}}{{/if}}',
    })

    # ----------------------------
    schema.tables["ihm_relaxation_time_multi_state_scheme"].foreign_keys[(schema,"relaxation_time_multi_state_scheme_connectivity_combo2_fkey")].foreign_key.update({
        'template_engine' :  'handlebars',
        'domain_filter_pattern' :  '{{#if _structure_id}}structure_id={{{_structure_id}}}{{/if}}',
    })

    # ----------------------------
    schema.tables["ihm_relaxation_time_multi_state_scheme"].foreign_keys[(schema,"ihm_relaxation_time_multi_state_scheme_time_combo1_fkey")].foreign_key.update({
        'template_engine' :  'handlebars',
        'domain_filter_pattern' :  '{{#if _structure_id}}structure_id={{{_structure_id}}}{{/if}}',
    })


# -- -----------------------------------------------------------------------------
def update_PDB_ihm_residues_not_modeled(model):
    schema = model.schemas["PDB"]
    table = schema.tables["ihm_residues_not_modeled"]
    # ----------------------------
    schema.tables["ihm_residues_not_modeled"].display.update(
        {'name' : 'Residues Not Modeled', 'comment_display' : {'*': {'table_comment_display': 'inline'}}, }
    )

    # ----------------------------
    schema.tables["ihm_residues_not_modeled"].visible_columns.update({
        '*' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_residues_not_modeled_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'id', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_residues_not_modeled_model_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_model_list.model_id.',
                'markdown_name' : 'Model Id',
            },
            'entity_description', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_residues_not_modeled_mm_poly_res_label_begin_fkey']}, 'entity_id'],
                'comment' : 'A reference to table entity_poly_seq.entity_id.',
                'markdown_name' : 'Entity Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_residues_not_modeled_asym_id_fkey']}, 'RID'],
                'comment' : 'A reference to table struct_asym.id.',
                'markdown_name' : 'Asym Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_residues_not_modeled_mm_poly_res_label_begin_fkey']}, 'num'],
                'comment' : 'A reference to table entity_poly_seq.num.',
                'markdown_name' : 'Sequence Id Begin',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_residues_not_modeled_mm_poly_res_label_end_fkey']}, 'num'],
                'comment' : 'A reference to table entity_poly_seq.num.',
                'markdown_name' : 'Sequence Id End',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_residues_not_modeled_mm_poly_res_label_begin_fkey']}, 'mon_id'],
                'comment' : 'A reference to table entity_poly_seq.mon_id.',
                'markdown_name' : 'Component Id Begin',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_residues_not_modeled_mm_poly_res_label_end_fkey']}, 'mon_id'],
                'comment' : 'A reference to table entity_poly_seq.mon_id.',
                'markdown_name' : 'Component Id End',
            },
            ['PDB', 'ihm_residues_not_modeled_reason_fkey'], 
            'details', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_residues_not_modeled_mm_poly_res_label_begin_fkey']}, 'RID'],
                'comment' : 'Refers to a combination of Entity Id, Sequence Id and Component Id in the entity_poly_seq table.',
                'markdown_name' : 'Polymeric Residue Begin',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_residues_not_modeled_mm_poly_res_label_end_fkey']}, 'RID'],
                'comment' : 'Refers to a combination of Entity Id, Sequence Id and Component Id in the entity_poly_seq table.',
                'markdown_name' : 'Polymeric Residue End',
            },
        ],
        'entry' :  [
            {
                'source' : [{'outbound': ['PDB', 'ihm_residues_not_modeled_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'id', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_residues_not_modeled_model_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_model_list.model_id.',
                'markdown_name' : 'Model Id',
            },
            'entity_description', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_residues_not_modeled_mm_poly_res_label_begin_fkey']}, 'entity_id'],
                'comment' : 'A reference to table entity_poly_seq.entity_id.',
                'markdown_name' : 'Entity Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_residues_not_modeled_asym_id_fkey']}, 'RID'],
                'comment' : 'A reference to table struct_asym.id.',
                'markdown_name' : 'Asym Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_residues_not_modeled_mm_poly_res_label_begin_fkey']}, 'num'],
                'comment' : 'A reference to table entity_poly_seq.num.',
                'markdown_name' : 'Sequence Id Begin',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_residues_not_modeled_mm_poly_res_label_end_fkey']}, 'num'],
                'comment' : 'A reference to table entity_poly_seq.num.',
                'markdown_name' : 'Sequence Id End',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_residues_not_modeled_mm_poly_res_label_begin_fkey']}, 'mon_id'],
                'comment' : 'A reference to table entity_poly_seq.mon_id.',
                'markdown_name' : 'Component Id Begin',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_residues_not_modeled_mm_poly_res_label_end_fkey']}, 'mon_id'],
                'comment' : 'A reference to table entity_poly_seq.mon_id.',
                'markdown_name' : 'Component Id End',
            },
            ['PDB', 'ihm_residues_not_modeled_reason_fkey'], 
            'details', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_residues_not_modeled_mm_poly_res_label_begin_fkey']}, 'RID'],
                'comment' : 'Refers to a combination of Entity Id, Sequence Id and Component Id in the entity_poly_seq table.',
                'markdown_name' : 'Polymeric Residue Begin',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_residues_not_modeled_mm_poly_res_label_end_fkey']}, 'RID'],
                'comment' : 'Refers to a combination of Entity Id, Sequence Id and Component Id in the entity_poly_seq table.',
                'markdown_name' : 'Polymeric Residue End',
            },
        ],
        'detailed' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_residues_not_modeled_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'id', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_residues_not_modeled_model_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_model_list.model_id.',
                'markdown_name' : 'Model Id',
            },
            'entity_description', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_residues_not_modeled_mm_poly_res_label_begin_fkey']}, 'entity_id'],
                'comment' : 'A reference to table entity_poly_seq.entity_id.',
                'markdown_name' : 'Entity Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_residues_not_modeled_asym_id_fkey']}, 'RID'],
                'comment' : 'A reference to table struct_asym.id.',
                'markdown_name' : 'Asym Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_residues_not_modeled_mm_poly_res_label_begin_fkey']}, 'num'],
                'comment' : 'A reference to table entity_poly_seq.num.',
                'markdown_name' : 'Sequence Id Begin',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_residues_not_modeled_mm_poly_res_label_end_fkey']}, 'num'],
                'comment' : 'A reference to table entity_poly_seq.num.',
                'markdown_name' : 'Sequence Id End',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_residues_not_modeled_mm_poly_res_label_begin_fkey']}, 'mon_id'],
                'comment' : 'A reference to table entity_poly_seq.mon_id.',
                'markdown_name' : 'Component Id Begin',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_residues_not_modeled_mm_poly_res_label_end_fkey']}, 'mon_id'],
                'comment' : 'A reference to table entity_poly_seq.mon_id.',
                'markdown_name' : 'Component Id End',
            },
            ['PDB', 'ihm_residues_not_modeled_reason_fkey'], 
            'details', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_residues_not_modeled_mm_poly_res_label_begin_fkey']}, 'RID'],
                'comment' : 'Refers to a combination of Entity Id, Sequence Id and Component Id in the entity_poly_seq table.',
                'markdown_name' : 'Polymeric Residue Begin',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_residues_not_modeled_mm_poly_res_label_end_fkey']}, 'RID'],
                'comment' : 'Refers to a combination of Entity Id, Sequence Id and Component Id in the entity_poly_seq table.',
                'markdown_name' : 'Polymeric Residue End',
            },
            ['PDB', 'ihm_residues_not_modeled_RCB_fkey'], 
            ['PDB', 'ihm_residues_not_modeled_RMB_fkey'], 
            'RCT', 
            'RMT', 
            ['PDB', 'ihm_residues_not_modeled_Owner_fkey'], 
        ],
    })

    # ----------------------------
    schema.tables["ihm_residues_not_modeled"].foreign_keys[(schema,"ihm_residues_not_modeled_model_id_fkey")].foreign_key.update({
        'template_engine' :  'handlebars',
        'domain_filter_pattern' :  '{{#if _structure_id}}structure_id={{{_structure_id}}}{{/if}}',
    })

    # ----------------------------
    schema.tables["ihm_residues_not_modeled"].foreign_keys[(schema,"ihm_residues_not_modeled_asym_id_fkey")].foreign_key.update({
        'template_engine' :  'handlebars',
        'domain_filter_pattern' :  '{{#if _structure_id}}structure_id={{{_structure_id}}}{{/if}}',
    })
    # ----------------------------
    schema.tables["ihm_residues_not_modeled"].foreign_keys[(schema,"ihm_residues_not_modeled_mm_poly_res_label_begin_fkey")].foreign_key.update({
        'from_name' :  'Ihm Residues Not Modeled Begin',
        'template_engine' :  'handlebars',
        'domain_filter_pattern' :  '{{#if _structure_id}}structure_id={{{_structure_id}}}{{/if}}',
    })

    # ----------------------------
    schema.tables["ihm_residues_not_modeled"].foreign_keys[(schema,"ihm_residues_not_modeled_mm_poly_res_label_end_fkey")].foreign_key.update({
        'from_name' :  'Ihm Residues Not Modeled End',
        'template_engine' :  'handlebars',
        'domain_filter_pattern' :  '{{#if _structure_id}}structure_id={{{_structure_id}}}{{/if}}',
    })

# -- -----------------------------------------------------------------------------
def update_PDB_ihm_sas_restraint(model):
    schema = model.schemas["PDB"]
    table = schema.tables["ihm_sas_restraint"]
    # ----------------------------
    schema.tables["ihm_sas_restraint"].display.update(
        {'name' : 'SAS Restraints', 'comment_display' : {'*': {'table_comment_display': 'inline'}}, }
    )

    # ----------------------------
    schema.tables["ihm_sas_restraint"].visible_columns.update({
        '*' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_sas_restraint_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'id', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_sas_restraint_model_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_model_list.model_id.',
                'markdown_name' : 'Model Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_sas_restraint_struct_assembly_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_struct_assembly.id.',
                'markdown_name' : 'Struct Assembly Id',
            },
            ['PDB', 'ihm_sas_restraint_profile_segment_flag_fkey'], 
            'fitting_atom_type', 
            'fitting_method', 
            ['PDB', 'ihm_sas_restraint_fitting_state_fkey'], 
            'radius_of_gyration', 
            'chi_value', 
            'details', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_sas_restraint_dataset_list_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_dataset_list.id.',
                'markdown_name' : 'Dataset List Id',
            },
        ],
        'entry' :  [
            {
                'source' : [{'outbound': ['PDB', 'ihm_sas_restraint_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'id', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_sas_restraint_model_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_model_list.model_id.',
                'markdown_name' : 'Model Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_sas_restraint_struct_assembly_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_struct_assembly.id.',
                'markdown_name' : 'Struct Assembly Id',
            },
            ['PDB', 'ihm_sas_restraint_profile_segment_flag_fkey'], 
            'fitting_atom_type', 
            'fitting_method', 
            ['PDB', 'ihm_sas_restraint_fitting_state_fkey'], 
            'radius_of_gyration', 
            'chi_value', 
            'details', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_sas_restraint_dataset_list_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_dataset_list.id.',
                'markdown_name' : 'Dataset List Id',
            },
        ],
        'detailed' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_sas_restraint_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'id', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_sas_restraint_model_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_model_list.model_id.',
                'markdown_name' : 'Model Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_sas_restraint_struct_assembly_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_struct_assembly.id.',
                'markdown_name' : 'Struct Assembly Id',
            },
            ['PDB', 'ihm_sas_restraint_profile_segment_flag_fkey'], 
            'fitting_atom_type', 
            'fitting_method', 
            ['PDB', 'ihm_sas_restraint_fitting_state_fkey'], 
            'radius_of_gyration', 
            'chi_value', 
            'details', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_sas_restraint_dataset_list_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_dataset_list.id.',
                'markdown_name' : 'Dataset List Id',
            },
            ['PDB', 'ihm_sas_restraint_RCB_fkey'], 
            ['PDB', 'ihm_sas_restraint_RMB_fkey'], 
            'RCT', 
            'RMT', 
            ['PDB', 'ihm_sas_restraint_Owner_fkey'], 
        ],
    })

    # ----------------------------
    schema.tables["ihm_sas_restraint"].foreign_keys[(schema,"ihm_sas_restraint_model_id_fkey")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })

    # ----------------------------
    schema.tables["ihm_sas_restraint"].foreign_keys[(schema,"ihm_sas_restraint_struct_assembly_id_fkey")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })

    # ----------------------------
    schema.tables["ihm_sas_restraint"].foreign_keys[(schema,"ihm_sas_restraint_dataset_list_id_fkey")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })


# -- -----------------------------------------------------------------------------
def update_PDB_ihm_starting_comparative_models(model):
    schema = model.schemas["PDB"]
    table = schema.tables["ihm_starting_comparative_models"]
    # ----------------------------
    schema.tables["ihm_starting_comparative_models"].display.update(
        {'name' : 'Starting Comparative Models', 'comment_display' : {'*': {'table_comment_display': 'inline'}}, }
    )
    
    # ----------------------------
    schema.tables["ihm_starting_comparative_models"].visible_columns.update({
        '*' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_starting_comparative_models_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'id', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_starting_comparative_models_starting_model_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_starting_model_details.starting_model_id.',
                'markdown_name' : 'Starting Model Id',
            },
            'starting_model_auth_asym_id', 
            'starting_model_seq_id_begin', 
            'starting_model_seq_id_end', 
            'template_auth_asym_id', 
            'template_seq_id_begin', 
            'template_seq_id_end', 
            'template_sequence_identity', 
            ['PDB', 'starting_comparative_models_template_sequence_id_denom_fkey'], 
            {
                'source' : [{'outbound': ['PDB', 'ihm_starting_comparative_models_template_dataset_list_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_dataset_list.id.',
                'markdown_name' : 'Template Dataset List Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_starting_comparative_models_alignment_file_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_external_files.id.',
                'markdown_name' : 'Alignment File Id',
            },
            'details', 
        ],
        'entry' :  [
            {
                'source' : [{'outbound': ['PDB', 'ihm_starting_comparative_models_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'id', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_starting_comparative_models_starting_model_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_starting_model_details.starting_model_id.',
                'markdown_name' : 'Starting Model Id',
            },
            'starting_model_auth_asym_id', 
            'starting_model_seq_id_begin', 
            'starting_model_seq_id_end', 
            'template_auth_asym_id', 
            'template_seq_id_begin', 
            'template_seq_id_end', 
            'template_sequence_identity', 
            ['PDB', 'starting_comparative_models_template_sequence_id_denom_fkey'], 
            {
                'source' : [{'outbound': ['PDB', 'ihm_starting_comparative_models_template_dataset_list_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_dataset_list.id.',
                'markdown_name' : 'Template Dataset List Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_starting_comparative_models_alignment_file_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_external_files.id.',
                'markdown_name' : 'Alignment File Id',
            },
            'details', 
        ],
        'detailed' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_starting_comparative_models_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'id', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_starting_comparative_models_starting_model_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_starting_model_details.starting_model_id.',
                'markdown_name' : 'Starting Model Id',
            },
            'starting_model_auth_asym_id', 
            'starting_model_seq_id_begin', 
            'starting_model_seq_id_end', 
            'template_auth_asym_id', 
            'template_seq_id_begin', 
            'template_seq_id_end', 
            'template_sequence_identity', 
            ['PDB', 'starting_comparative_models_template_sequence_id_denom_fkey'], 
            {
                'source' : [{'outbound': ['PDB', 'ihm_starting_comparative_models_template_dataset_list_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_dataset_list.id.',
                'markdown_name' : 'Template Dataset List Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_starting_comparative_models_alignment_file_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_external_files.id.',
                'markdown_name' : 'Alignment File Id',
            },
            'details', 
            ['PDB', 'ihm_starting_comparative_models_RCB_fkey'], 
            ['PDB', 'ihm_starting_comparative_models_RMB_fkey'], 
            'RCT', 
            'RMT', 
            ['PDB', 'ihm_starting_comparative_models_Owner_fkey'], 
        ],
    })

    # ----------------------------
    schema.tables["ihm_starting_comparative_models"].columns["starting_model_auth_asym_id"].display.update(
        {'name' : 'Author Provided Chain Id for the Starting Model', }
    )

    # ----------------------------
    schema.tables["ihm_starting_comparative_models"].columns["starting_model_seq_id_begin"].display.update(
        {'name' : 'Beginning Sequence Id for the Starting Model', }
    )
    
    # ----------------------------
    schema.tables["ihm_starting_comparative_models"].columns["starting_model_seq_id_end"].display.update(
        {'name' : 'Ending Sequence Id for the Starting Model', }
    )
    
    # ----------------------------
    schema.tables["ihm_starting_comparative_models"].columns["template_auth_asym_id"].display.update(
        {'name' : 'Author Provided Chain Id for the Template', }
    )
    
    # ----------------------------
    schema.tables["ihm_starting_comparative_models"].columns["template_seq_id_begin"].display.update(
        {'name' : 'Beginning Sequence Id for the Template', }
    )
    
    # ----------------------------
    schema.tables["ihm_starting_comparative_models"].columns["template_seq_id_end"].display.update(
        {'name' : 'Ending Sequence Id for the Template', }
    )
    
    # ----------------------------
    schema.tables["ihm_starting_comparative_models"].foreign_keys[(schema,"ihm_starting_comparative_models_alignment_file_id_fkey")].foreign_key.update({
            'domain_filter_pattern' :  'structure_id={{structure_id}}',
        })

    # ----------------------------
    schema.tables["ihm_starting_comparative_models"].foreign_keys[(schema,"ihm_starting_comparative_models_template_dataset_list_id_fkey")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })

    # ----------------------------
    schema.tables["ihm_starting_comparative_models"].foreign_keys[(schema,"ihm_starting_comparative_models_alignment_file_id_fk")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })

    # ----------------------------
    schema.tables["ihm_starting_comparative_models"].foreign_keys[(schema,"ihm_starting_comparative_models_starting_model_id_fkey")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })


# -- -----------------------------------------------------------------------------
def update_PDB_ihm_starting_computational_models(model):
    schema = model.schemas["PDB"]
    table = schema.tables["ihm_starting_computational_models"]
    # ----------------------------
    schema.tables["ihm_starting_computational_models"].display.update(
        {'name' : 'Starting Computational Models', 'comment_display' : {'*': {'table_comment_display': 'inline'}}, }
    )

    # ----------------------------
    schema.tables["ihm_starting_computational_models"].visible_columns.update({
        '*' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_starting_computational_models_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_starting_computational_models_starting_model_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_starting_model_details.starting_model_id.',
                'markdown_name' : 'Starting Model Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_starting_computational_models_script_file_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_external_files.id.',
                'markdown_name' : 'Script File Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_starting_computational_models_software_id_fkey']}, 'RID'],
                'comment' : 'A reference to table software.pdbx_ordinal.',
                'markdown_name' : 'Software Id',
            },
        ],
        'entry' :  [
            {
                'source' : [{'outbound': ['PDB', 'ihm_starting_computational_models_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_starting_computational_models_starting_model_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_starting_model_details.starting_model_id.',
                'markdown_name' : 'Starting Model Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_starting_computational_models_script_file_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_external_files.id.',
                'markdown_name' : 'Script File Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_starting_computational_models_software_id_fkey']}, 'RID'],
                'comment' : 'A reference to table software.pdbx_ordinal.',
                'markdown_name' : 'Software Id',
            },
        ],
        'detailed' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_starting_computational_models_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_starting_computational_models_starting_model_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_starting_model_details.starting_model_id.',
                'markdown_name' : 'Starting Model Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_starting_computational_models_script_file_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_external_files.id.',
                'markdown_name' : 'Script File Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_starting_computational_models_software_id_fkey']}, 'RID'],
                'comment' : 'A reference to table software.pdbx_ordinal.',
                'markdown_name' : 'Software Id',
            },
            ['PDB', 'ihm_starting_computational_models_RCB_fkey'], 
            ['PDB', 'ihm_starting_computational_models_RMB_fkey'], 
            'RCT', 
            'RMT', 
            ['PDB', 'ihm_starting_computational_models_Owner_fkey'], 
        ],
    })

    # ----------------------------
    schema.tables["ihm_starting_computational_models"].foreign_keys[(schema,"ihm_starting_computational_models_software_id_fkey")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })

    # ----------------------------
    schema.tables["ihm_starting_computational_models"].foreign_keys[(schema,"ihm_starting_computational_models_starting_model_id_fkey")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })

    # ----------------------------
    schema.tables["ihm_starting_computational_models"].foreign_keys[(schema,"ihm_starting_computational_models_script_file_id_fkey")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })


# -- -----------------------------------------------------------------------------
def update_PDB_ihm_starting_model_details(model):
    schema = model.schemas["PDB"]
    table = schema.tables["ihm_starting_model_details"]
    # ----------------------------
    schema.tables["ihm_starting_model_details"].display.update(
        {'markdown_name' : 'Starting Structural Models^*^', 'comment_display' : {'*': {'table_comment_display': 'inline'}}, }
    )

    # ----------------------------
    schema.tables["ihm_starting_model_details"].table_display.update({
        'row_name' : { 'row_markdown_pattern' : '{{{starting_model_id}}}', },
    })

    # ----------------------------
    schema.tables["ihm_starting_model_details"].visible_columns.update({
        '*' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_starting_model_details_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'starting_model_id', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_starting_model_details_entity_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entity.id.',
                'markdown_name' : 'Entity Id',
            },
            'entity_description', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_starting_model_details_asym_id_fkey']}, 'RID'],
                'comment' : 'A reference to table struct_asym.id.',
                'markdown_name' : 'Asym Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_starting_model_details_entity_poly_segment_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_entity_poly_segment.id.',
                'markdown_name' : 'Entity Poly Segment Id',
            },
            ['PDB', 'ihm_starting_model_details_starting_model_source_fkey'], 
            'starting_model_auth_asym_id', 
            'starting_model_sequence_offset', 
            'description', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_starting_model_details_dataset_list_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_dataset_list.id.',
                'markdown_name' : 'Dataset List Id',
            },
            'mmCIF_File_URL', 
        ],
        'entry' :  [
            {
                'source' : [{'outbound': ['PDB', 'ihm_starting_model_details_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'starting_model_id', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_starting_model_details_entity_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entity.id.',
                'markdown_name' : 'Entity Id',
            },
            'entity_description', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_starting_model_details_asym_id_fkey']}, 'RID'],
                'comment' : 'A reference to table struct_asym.id.',
                'markdown_name' : 'Asym Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_starting_model_details_entity_poly_segment_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_entity_poly_segment.id.',
                'markdown_name' : 'Entity Poly Segment Id',
            },
            ['PDB', 'ihm_starting_model_details_starting_model_source_fkey'], 
            'starting_model_auth_asym_id', 
            'starting_model_sequence_offset', 
            'description', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_starting_model_details_dataset_list_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_dataset_list.id.',
                'markdown_name' : 'Dataset List Id',
            },
            'mmCIF_File_URL', 
        ],
        'detailed' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_starting_model_details_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'starting_model_id', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_starting_model_details_entity_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entity.id.',
                'markdown_name' : 'Entity Id',
            },
            'entity_description', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_starting_model_details_asym_id_fkey']}, 'RID'],
                'comment' : 'A reference to table struct_asym.id.',
                'markdown_name' : 'Asym Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_starting_model_details_entity_poly_segment_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_entity_poly_segment.id.',
                'markdown_name' : 'Entity Poly Segment Id',
            },
            ['PDB', 'ihm_starting_model_details_starting_model_source_fkey'], 
            'starting_model_auth_asym_id', 
            'starting_model_sequence_offset', 
            'description', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_starting_model_details_dataset_list_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_dataset_list.id.',
                'markdown_name' : 'Dataset List Id',
            },
            'mmCIF_File_URL', 
            {'source' : 'mmCIF_File_Bytes', 'markdown_name' : 'mmCIF File Size (Bytes)', },
            ['PDB', 'ihm_starting_model_details_RCB_fkey'], 
            ['PDB', 'ihm_starting_model_details_RMB_fkey'], 
            'RCT', 
            'RMT', 
            ['PDB', 'ihm_starting_model_details_Owner_fkey'], 
        ],
    })

    # ----------------------------
    schema.tables["ihm_starting_model_details"].visible_foreign_keys.update(
    {
        'filter' :  'detailed',
        'detailed' :  [
            ['PDB', 'ihm_starting_comparative_models_starting_model_id_fkey'], 
            ['PDB', 'ihm_starting_computational_models_starting_model_id_fkey'], 
            ['PDB', 'ihm_starting_model_seq_dif_starting_model_id_fkey'], 
            ['PDB', 'ihm_model_representation_details_starting_model_id_fkey'], 
        ],
    })

    # ----------------------------
    schema.tables["ihm_starting_model_details"].columns["starting_model_auth_asym_id"].display.update(
        {'name' : 'Author Provided Chain Id for the Starting Model', }
    )

    # ----------------------------
    schema.tables["ihm_starting_model_details"].columns["mmCIF_File_URL"].display.update(
        {'name' : 'mmCIF File for the Starting Model', }
    )

    # ----------------------------
    schema.tables["ihm_starting_model_details"].foreign_keys[(schema,"ihm_starting_model_details_entity_id_fkey")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })

    # ----------------------------
    schema.tables["ihm_starting_model_details"].foreign_keys[(schema,"ihm_starting_model_details_asym_id_fkey")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })

    # ----------------------------
    schema.tables["ihm_starting_model_details"].foreign_keys[(schema,"ihm_starting_model_details_entity_poly_segment_id_fkey")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })

    # ----------------------------
    schema.tables["ihm_starting_model_details"].foreign_keys[(schema,"ihm_starting_model_details_dataset_list_id_fkey")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })

    # ----------------------------
    schema.tables["ihm_starting_model_details"].foreign_keys[(schema,"ihm_starting_model_details_entity_poly_segment_id_fk")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })


# -- -----------------------------------------------------------------------------
def update_PDB_ihm_starting_model_seq_dif(model):
    schema = model.schemas["PDB"]
    table = schema.tables["ihm_starting_model_seq_dif"]
    # ----------------------------
    schema.tables["ihm_starting_model_seq_dif"].display.update(
        {'name' : 'Point Differences in the Sequences of Starting Models', 'comment_display' : {'*': {'table_comment_display': 'inline'}}, }
    )

    # ----------------------------
    schema.tables["ihm_starting_model_seq_dif"].visible_columns.update({
        '*' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_starting_model_seq_dif_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'id', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_starting_model_seq_dif_mm_poly_res_label_fkey']}, 'entity_id'],
                'comment' : 'A reference to table entity_poly_seq.entity_id.',
                'markdown_name' : 'Entity Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_starting_model_seq_dif_asym_id_fkey']}, 'RID'],
                'comment' : 'A reference to table struct_asym.id.',
                'markdown_name' : 'Asym Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_starting_model_seq_dif_mm_poly_res_label_fkey']}, 'num'],
                'comment' : 'A reference to table entity_poly_seq.num.',
                'markdown_name' : 'Sequence Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_starting_model_seq_dif_mm_poly_res_label_fkey']}, 'mon_id'],
                'comment' : 'A reference to table entity_poly_seq.mon_id.',
                'markdown_name' : 'Component Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_starting_model_seq_dif_starting_model_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_starting_model_details.starting_model_id.',
                'markdown_name' : 'Starting Model Id',
            },
            'db_asym_id', 
            'db_seq_id', 
            'db_comp_id', 
            'db_entity_id', 
            'details', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_starting_model_seq_dif_mm_poly_res_label_fkey']}, 'RID'],
                'comment' : 'Refers to a combination of Entity Id, Sequence Id and Component Id in the entity_poly_seq table.',
                'markdown_name' : 'Polymeric Residue',
            },
        ],
        'entry' :  [
            {
                'source' : [{'outbound': ['PDB', 'ihm_starting_model_seq_dif_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'id', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_starting_model_seq_dif_mm_poly_res_label_fkey']}, 'entity_id'],
                'comment' : 'A reference to table entity_poly_seq.entity_id.',
                'markdown_name' : 'Entity Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_starting_model_seq_dif_asym_id_fkey']}, 'RID'],
                'comment' : 'A reference to table struct_asym.id.',
                'markdown_name' : 'Asym Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_starting_model_seq_dif_mm_poly_res_label_fkey']}, 'num'],
                'comment' : 'A reference to table entity_poly_seq.num.',
                'markdown_name' : 'Sequence Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_starting_model_seq_dif_mm_poly_res_label_fkey']}, 'mon_id'],
                'comment' : 'A reference to table entity_poly_seq.mon_id.',
                'markdown_name' : 'Component Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_starting_model_seq_dif_starting_model_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_starting_model_details.starting_model_id.',
                'markdown_name' : 'Starting Model Id',
            },
            'db_asym_id', 
            'db_seq_id', 
            'db_comp_id', 
            'db_entity_id', 
            'details', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_starting_model_seq_dif_mm_poly_res_label_fkey']}, 'RID'],
                'comment' : 'Refers to a combination of Entity Id, Sequence Id and Component Id in the entity_poly_seq table.',
                'markdown_name' : 'Polymeric Residue',
            },
        ],
        'detailed' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_starting_model_seq_dif_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'id', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_starting_model_seq_dif_mm_poly_res_label_fkey']}, 'entity_id'],
                'comment' : 'A reference to table entity_poly_seq.entity_id.',
                'markdown_name' : 'Entity Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_starting_model_seq_dif_asym_id_fkey']}, 'RID'],
                'comment' : 'A reference to table struct_asym.id.',
                'markdown_name' : 'Asym Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_starting_model_seq_dif_mm_poly_res_label_fkey']}, 'num'],
                'comment' : 'A reference to table entity_poly_seq.num.',
                'markdown_name' : 'Sequence Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_starting_model_seq_dif_mm_poly_res_label_fkey']}, 'mon_id'],
                'comment' : 'A reference to table entity_poly_seq.mon_id.',
                'markdown_name' : 'Component Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_starting_model_seq_dif_starting_model_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_starting_model_details.starting_model_id.',
                'markdown_name' : 'Starting Model Id',
            },
            'db_asym_id', 
            'db_seq_id', 
            'db_comp_id', 
            'db_entity_id', 
            'details', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_starting_model_seq_dif_mm_poly_res_label_fkey']}, 'RID'],
                'comment' : 'Refers to a combination of Entity Id, Sequence Id and Component Id in the entity_poly_seq table.',
                'markdown_name' : 'Polymeric Residue',
            },
            ['PDB', 'ihm_starting_model_seq_dif_RCB_fkey'], 
            ['PDB', 'ihm_starting_model_seq_dif_RMB_fkey'], 
            'RCT', 
            'RMT', 
            ['PDB', 'ihm_starting_model_seq_dif_Owner_fkey'], 
        ],
    })

    # ----------------------------
    schema.tables["ihm_starting_model_seq_dif"].columns["db_asym_id"].display.update(
        {'name' : 'Database Asym Id', }
    )

    # ----------------------------
    schema.tables["ihm_starting_model_seq_dif"].columns["db_comp_id"].display.update(
        {'name' : 'Database Component Id', }
    )

    # ----------------------------
    schema.tables["ihm_starting_model_seq_dif"].columns["db_entity_id"].display.update(
        {'name' : 'Database Entity Id', }
    )

    # ----------------------------
    schema.tables["ihm_starting_model_seq_dif"].columns["db_seq_id"].display.update(
        {'name' : 'Database Sequence Id', }
    )
    
    # ----------------------------
    schema.tables["ihm_starting_model_seq_dif"].foreign_keys[(schema,"ihm_starting_model_seq_dif_mm_poly_res_label_fkey")].foreign_key.update({
        'from_name' :  'Ihm Starting Model Seq Dif',
        'template_engine' :  'handlebars',
        'domain_filter_pattern' :  '{{#if _structure_id}}structure_id={{{_structure_id}}}{{/if}}',
    })

    # ----------------------------
    schema.tables["ihm_starting_model_seq_dif"].foreign_keys[(schema,"ihm_starting_model_seq_dif_asym_id_fkey")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })

    # ----------------------------
    schema.tables["ihm_starting_model_seq_dif"].foreign_keys[(schema,"ihm_starting_model_seq_dif_starting_model_id_fkey")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })

# -- -----------------------------------------------------------------------------
def update_PDB_ihm_struct_assembly(model):
    schema = model.schemas["PDB"]
    table = schema.tables["ihm_struct_assembly"]
    # ----------------------------
    schema.tables["ihm_struct_assembly"].display.update(
        {'markdown_name' : 'Structural Assemblies^*^', 'comment_display' : {'*': {'table_comment_display': 'inline'}}, }
    )

    # ----------------------------
    schema.tables["ihm_struct_assembly"].table_display.update({
        'row_name' : { 'row_markdown_pattern' : '{{{id}}}', },
    })

    # ----------------------------
    schema.tables["ihm_struct_assembly"].visible_columns.update({
        '*' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_struct_assembly_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'id', 
            'name', 
            'description', 
        ],
        'entry' :  [
            {
                'source' : [{'outbound': ['PDB', 'ihm_struct_assembly_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'id', 
            'name', 
            'description', 
        ],
        'detailed' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_struct_assembly_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'id', 
            'name', 
            'description', 
            ['PDB', 'ihm_struct_assembly_RCB_fkey'], 
            ['PDB', 'ihm_struct_assembly_RMB_fkey'], 
            'RCT', 
            'RMT', 
            ['PDB', 'ihm_struct_assembly_Owner_fkey'], 
        ],
    })

    # ----------------------------
    schema.tables["ihm_struct_assembly"].visible_foreign_keys.update({
        'filter' :  'detailed',
        'detailed' :  [
            ['PDB', 'ihm_struct_assembly_details_assembly_id_fkey'], 
            ['PDB', 'ihm_struct_assembly_details_parent_assembly_id_fkey'], 
            ['PDB', 'ihm_struct_assembly_class_link_assembly_id_fkey'], 
            ['PDB', 'ihm_modeling_protocol_details_struct_assembly_id_fkey'], 
            ['PDB', 'ihm_modeling_post_process_struct_assembly_id_fkey'], 
            ['PDB', 'ihm_model_list_assembly_id_fkey'], 
            ['PDB', 'ihm_2dem_class_average_restraint_struct_assembly_id_fkey'], 
            ['PDB', 'ihm_3dem_restraint_struct_assembly_id_fkey'], 
            ['PDB', 'ihm_sas_restraint_struct_assembly_id_fkey'], 
        ],
    })


# -- -----------------------------------------------------------------------------
def update_PDB_ihm_struct_assembly_class(model):
    schema = model.schemas["PDB"]
    table = schema.tables["ihm_struct_assembly_class"]
    # ----------------------------
    schema.tables["ihm_struct_assembly_class"].display.update(
        {'name' : 'Structural Assembly Classes', 'comment_display' : {'*': {'table_comment_display': 'inline'}}, }
    )

    # ----------------------------
    schema.tables["ihm_struct_assembly_class"].table_display.update({
        'row_name' : { 'row_markdown_pattern' : '{{{id}}}', },
    })

    # ----------------------------
    schema.tables["ihm_struct_assembly_class"].visible_columns.update({
        '*' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_struct_assembly_class_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'id', 
            'name', 
            ['PDB', 'ihm_struct_assembly_class_type_fkey'], 
            'description', 
        ],
        'entry' :  [
            {
                'source' : [{'outbound': ['PDB', 'ihm_struct_assembly_class_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'id', 
            'name', 
            ['PDB', 'ihm_struct_assembly_class_type_fkey'], 
            'description', 
        ],
        'detailed' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_struct_assembly_class_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'id', 
            'name', 
            ['PDB', 'ihm_struct_assembly_class_type_fkey'], 
            'description', 
            ['PDB', 'ihm_struct_assembly_class_RCB_fkey'], 
            ['PDB', 'ihm_struct_assembly_class_RMB_fkey'], 
            'RCT', 
            'RMT', 
            ['PDB', 'ihm_struct_assembly_class_Owner_fkey'], 
        ],
    })

    # ----------------------------
    schema.tables["ihm_struct_assembly_class"].visible_foreign_keys.update({
        'filter' :  'detailed',
        'detailed' :  [
            ['PDB', 'ihm_struct_assembly_class_link_class_id_fkey'], 
        ],
    })


# -- -----------------------------------------------------------------------------
def update_PDB_ihm_struct_assembly_class_link(model):
    schema = model.schemas["PDB"]
    table = schema.tables["ihm_struct_assembly_class_link"]
    # ----------------------------
    schema.tables["ihm_struct_assembly_class_link"].display.update(
        {'name' : 'Structural Assemblies Belonging to Classes', 'comment_display' : {'*': {'table_comment_display': 'inline'}}, }
    )
    
    # ----------------------------
    schema.tables["ihm_struct_assembly_class_link"].visible_columns.update({
        '*' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_struct_assembly_class_link_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_struct_assembly_class_link_assembly_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_struct_assembly.id.',
                'markdown_name' : 'Assembly Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_struct_assembly_class_link_class_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_struct_assembly_class.id.',
                'markdown_name' : 'Class Id',
            },
        ],
        'entry' :  [
            {
                'source' : [{'outbound': ['PDB', 'ihm_struct_assembly_class_link_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_struct_assembly_class_link_assembly_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_struct_assembly.id.',
                'markdown_name' : 'Assembly Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_struct_assembly_class_link_class_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_struct_assembly_class.id.',
                'markdown_name' : 'Class Id',
            },
        ],
        'detailed' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_struct_assembly_class_link_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_struct_assembly_class_link_assembly_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_struct_assembly.id.',
                'markdown_name' : 'Assembly Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_struct_assembly_class_link_class_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_struct_assembly_class.id.',
                'markdown_name' : 'Class Id',
            },
            ['PDB', 'ihm_struct_assembly_class_link_RCB_fkey'], 
            ['PDB', 'ihm_struct_assembly_class_link_RMB_fkey'], 
            'RCT', 
            'RMT', 
            ['PDB', 'ihm_struct_assembly_class_link_Owner_fkey'], 
        ],
    })

    # ----------------------------
    schema.tables["ihm_struct_assembly_class_link"].foreign_keys[(schema,"ihm_struct_assembly_class_link_class_id_fkey")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })

    # ----------------------------
    schema.tables["ihm_struct_assembly_class_link"].foreign_keys[(schema,"ihm_struct_assembly_class_link_assembly_id_fkey")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })


# -- -----------------------------------------------------------------------------
def update_PDB_ihm_struct_assembly_details(model):
    schema = model.schemas["PDB"]
    table = schema.tables["ihm_struct_assembly_details"]
    # ----------------------------
    schema.tables["ihm_struct_assembly_details"].display.update(
        {'markdown_name' : 'Details of Structural Assemblies^*^', 'comment_display' : {'*': {'table_comment_display': 'inline'}}, }
    )

    # ----------------------------
    schema.tables["ihm_struct_assembly_details"].visible_columns.update({
        '*' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_struct_assembly_details_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'id', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_struct_assembly_details_assembly_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_struct_assembly.id.',
                'markdown_name' : 'Assembly Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_struct_assembly_details_parent_assembly_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_struct_assembly.id.',
                'markdown_name' : 'Parent Assembly Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_struct_assembly_details_entity_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entity.id.',
                'markdown_name' : 'Entity Id',
            },
            'entity_description', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_struct_assembly_details_asym_id_fkey']}, 'RID'],
                'comment' : 'A reference to table struct_asym.id.',
                'markdown_name' : 'Asym Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_struct_assembly_details_entity_poly_segment_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_entity_poly_segment.id.',
                'markdown_name' : 'Entity Poly Segment Id',
            },
        ],
        'entry' :  [
            {
                'source' : [{'outbound': ['PDB', 'ihm_struct_assembly_details_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'id', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_struct_assembly_details_assembly_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_struct_assembly.id.',
                'markdown_name' : 'Assembly Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_struct_assembly_details_parent_assembly_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_struct_assembly.id.',
                'markdown_name' : 'Parent Assembly Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_struct_assembly_details_entity_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entity.id.',
                'markdown_name' : 'Entity Id',
            },
            'entity_description', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_struct_assembly_details_asym_id_fkey']}, 'RID'],
                'comment' : 'A reference to table struct_asym.id.',
                'markdown_name' : 'Asym Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_struct_assembly_details_entity_poly_segment_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_entity_poly_segment.id.',
                'markdown_name' : 'Entity Poly Segment Id',
            },
        ],
        'detailed' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_struct_assembly_details_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'id', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_struct_assembly_details_assembly_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_struct_assembly.id.',
                'markdown_name' : 'Assembly Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_struct_assembly_details_parent_assembly_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_struct_assembly.id.',
                'markdown_name' : 'Parent Assembly Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_struct_assembly_details_entity_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entity.id.',
                'markdown_name' : 'Entity Id',
            },
            'entity_description', 
            {
                'source' : [{'outbound': ['PDB', 'ihm_struct_assembly_details_asym_id_fkey']}, 'RID'],
                'comment' : 'A reference to table struct_asym.id.',
                'markdown_name' : 'Asym Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'ihm_struct_assembly_details_entity_poly_segment_id_fkey']}, 'RID'],
                'comment' : 'A reference to table ihm_entity_poly_segment.id.',
                'markdown_name' : 'Entity Poly Segment Id',
            },
            ['PDB', 'ihm_struct_assembly_details_RCB_fkey'], 
            ['PDB', 'ihm_struct_assembly_details_RMB_fkey'], 
            'RCT', 
            'RMT', 
            ['PDB', 'ihm_struct_assembly_details_Owner_fkey'], 
        ],
    })

    # ----------------------------
    schema.tables["ihm_struct_assembly_details"].foreign_keys[(schema,"ihm_struct_assembly_details_parent_assembly_id_fkey")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })

    # ----------------------------
    schema.tables["ihm_struct_assembly_details"].foreign_keys[(schema,"ihm_struct_assembly_details_entity_poly_segment_id_fkey")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })

    # ----------------------------
    schema.tables["ihm_struct_assembly_details"].foreign_keys[(schema,"ihm_struct_assembly_details_entity_id_fkey")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })

    # ----------------------------
    schema.tables["ihm_struct_assembly_details"].foreign_keys[(schema,"ihm_struct_assembly_details_assembly_id_fkey")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })

    # ----------------------------
    schema.tables["ihm_struct_assembly_details"].foreign_keys[(schema,"ihm_struct_assembly_details_entity_poly_segment_id_fk")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })

    # ----------------------------
    schema.tables["ihm_struct_assembly_details"].foreign_keys[(schema,"ihm_struct_assembly_details_asym_id_fkey")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })


# -- -----------------------------------------------------------------------------

# -- -----------------------------------------------------------------------------

# -- -----------------------------------------------------------------------------

# -- -----------------------------------------------------------------------------

# -- -----------------------------------------------------------------------------


# -- ==========================================================================================================    
def update_PDB_ihm_annotations(model):

    # -- list of specific tables

    update_PDB_ihm_2dem_class_average_fitting(model)
    update_PDB_ihm_2dem_class_average_restraint(model)
    update_PDB_ihm_3dem_restraint(model)
    update_PDB_ihm_chemical_component_descriptor(model)
    update_PDB_ihm_cross_link_list(model)
    update_PDB_ihm_cross_link_pseudo_site(model)
    update_PDB_ihm_cross_link_restraint(model)
    update_PDB_ihm_cross_link_result(model)
    update_PDB_ihm_cross_link_result_parameters(model)
    update_PDB_ihm_data_transformation(model)
    update_PDB_ihm_dataset_external_reference(model)
    update_PDB_ihm_dataset_group(model)
    update_PDB_ihm_dataset_group_link(model)
    update_PDB_ihm_dataset_list(model)
    update_PDB_ihm_dataset_related_db_reference(model)
    update_PDB_ihm_derived_angle_restraint(model)
    update_PDB_ihm_derived_dihedral_restraint(model)
    update_PDB_ihm_derived_distance_restraint(model)
    update_PDB_ihm_ensemble_info(model)
    update_PDB_ihm_ensemble_sub_sample(model)
    update_PDB_ihm_entity_poly_segment(model)
    update_PDB_ihm_entry_collection(model)
    update_PDB_ihm_entry_collection_mapping(model)
    update_PDB_ihm_epr_restraint(model)
    update_PDB_ihm_external_files(model)
    update_PDB_ihm_external_reference_info(model)
    update_PDB_ihm_feature_list(model)
    update_PDB_ihm_geometric_object_axis(model)
    update_PDB_ihm_geometric_object_center(model)
    update_PDB_ihm_geometric_object_distance_restraint(model)
    update_PDB_ihm_geometric_object_half_torus(model)
    update_PDB_ihm_geometric_object_list(model)
    update_PDB_ihm_geometric_object_plane(model)
    update_PDB_ihm_geometric_object_sphere(model)
    update_PDB_ihm_geometric_object_torus(model)
    update_PDB_ihm_geometric_object_transformation(model)
    update_PDB_ihm_hdx_restraint(model)
    update_PDB_ihm_hydroxyl_radical_fp_restraint(model)
    update_PDB_ihm_interface_residue_feature(model)
    update_PDB_ihm_kinetic_rate(model)
    update_PDB_ihm_ligand_probe(model)
    update_PDB_ihm_localization_density_files(model)
    update_PDB_ihm_model_group(model)
    update_PDB_ihm_model_group_link(model)
    update_PDB_ihm_model_list(model)
    update_PDB_ihm_model_representation(model)
    update_PDB_ihm_model_representation_details(model)
    update_PDB_ihm_model_representative(model)
    update_PDB_ihm_modeling_post_process(model)
    update_PDB_ihm_modeling_protocol(model)
    update_PDB_ihm_modeling_protocol_details(model)
    update_PDB_ihm_multi_state_model_group_link(model)
    update_PDB_ihm_multi_state_modeling(model)
    update_PDB_ihm_multi_state_scheme(model)
    update_PDB_ihm_multi_state_scheme_connectivity(model)
    update_PDB_ihm_non_poly_feature(model)
    update_PDB_ihm_ordered_ensemble(model)
    update_PDB_ihm_ordered_model(model)
    update_PDB_ihm_poly_atom_feature(model)
    update_PDB_ihm_poly_probe_conjugate(model)
    update_PDB_ihm_poly_probe_position(model)
    update_PDB_ihm_poly_residue_feature(model)
    update_PDB_ihm_predicted_contact_restraint(model)
    update_PDB_ihm_probe_list(model)
    update_PDB_ihm_pseudo_site(model)
    update_PDB_ihm_pseudo_site_feature(model)
    update_PDB_ihm_related_datasets(model)
    update_PDB_ihm_relaxation_time(model)
    update_PDB_ihm_relaxation_time_multi_state_scheme(model)
    update_PDB_ihm_residues_not_modeled(model)
    update_PDB_ihm_sas_restraint(model)
    update_PDB_ihm_starting_comparative_models(model)
    update_PDB_ihm_starting_computational_models(model)
    update_PDB_ihm_starting_model_details(model)
    update_PDB_ihm_starting_model_seq_dif(model)
    update_PDB_ihm_struct_assembly(model)
    update_PDB_ihm_struct_assembly_class(model)
    update_PDB_ihm_struct_assembly_class_link(model)
    update_PDB_ihm_struct_assembly_details(model)
    

# -- =================================================================================    
def main(server_name, catalog_id, credentials, args):
    server = DerivaServer('https', server_name, credentials)
    catalog = server.connect_ermrest(catalog_id)
    catalog.dcctx['cid'] = DCCTX["annotation"]
    model = catalog.getCatalogModel()
    schema_name = "PDB"
    
    if args.pre_print:
        print_schema_annotations(model, schema_name)

    update_PDB_ihm_annotations(model)
    
    return
    if args.post_print:
        print_schema_annotations(model, schema_name)

    if not args.dry_run:
        #model.apply()
        pass


# -- =================================================================================

if __name__ == '__main__':
    cli = PDBDEV_CLI("PDB_Dev", None, 1)
    cli.parser.add_argument('--schema', metavar='<schema>', help="print catalog acl script without applying", default=False)
    cli.parser.add_argument('--table', metavar='<table>', help="print catalog acl script without applying", default=False)
    args = cli.parse_cli()
    credentials = get_credential(args.host, args.credential_file)
    print(credentials)

    if args.debug:
        init_logging(level=logging.DEBUG)
    
    main(args.host, args.catalog_id, credentials, args)
