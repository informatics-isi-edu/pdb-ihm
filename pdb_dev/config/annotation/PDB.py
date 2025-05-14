import json
from deriva.core import ErmrestCatalog, AttrDict, get_credential, DEFAULT_CREDENTIAL_FILE, tag, urlquote, DerivaServer, get_credential, BaseCLI
from deriva.core.ermrest_model import builtin_types, Schema, Table, Column, Key, ForeignKey
from deriva.core import urlquote, urlunquote
import requests.exceptions
from ...utils.shared import DCCTX, PDBDEV_CLI
from deriva.utils.extras.model import print_schema_model_extras, print_table_model_extras, print_schema_annotations, per_schema_annotation_tags, clear_schema_annotations, tag2name
from .PDB_base import update_PDB_base_annotations
from .PDB_ihm import update_PDB_ihm_annotations


# -- =================================================================================
# -- schema level annotation
# TODO: In progress. Still need to be tested
def update_PDB(model):
    schema = model.schemas["PDB"]
    print("update_PDB")
    
    schema.display.update({
        'name_style' : { 'title_case' : True, 'underline_space' : True, },
    })

    """
    for tname, table in schema.tables.items():
        for fkey in table.foreign_keys:
            from_cols = {c.name for c in fkey.column_map.keys()}
            to_cols = {c.name for c in fkey.column_map.values()}
            if len(from_cols) > 1 and "structure_id" in from_cols:
                fkey.foreign_key.update({
                    "domain_filter_pattern": "%s/structure_id={{{structure_id}}}"
                })
    """
        
    # -- make sure all fkeys containing structure_id are updated with domain_filter_pattern
    '''
    schema.tables["Experiment"].foreign_keys[(schema,"Experiment_Growth_Protocol_Reference_fkey")].foreign_key.update({
        "from_name": "Experiment Growth Protocol",
        "domain_filter_pattern": "Category=any({{#encode 'Growth protocol'}}{{/encode}},{{#encode 'Overall sequencing'}}{{/encode}})"        
    })
    '''

    
# -- ---------------------------------------------------------------------------------
def update_PDB_entry(model):
    schema = model.schemas["PDB"]
    table = schema.tables["entry"]

    table.display.update({'markdown_name' :  'Entry^*^', })
    
    table.table_display.update({
        'compact' : { 'row_order' : [{'column': 'RCT', 'descending': True}], },
        'row_name' : { 'row_markdown_pattern' : '{{{id}}}', },
    })

    table.visible_columns.update({
        '*' :  [
            'RID', 
            'id', 
            'mmCIF_File_URL', 
            'Submitter_Flag_Date', 
            'Image_File_URL', 
            ['PDB', 'entry_Accession_Code_fkey'], 
            ['PDB', 'entry_Workflow_Status_fkey'], 
            'Process_Status', 
            {
                'entity' : True,
                'source' : [{'inbound': ['PDB', 'Entry_Error_File_Entry_RID_fkey']}, 'RID'],
                'display' : {'template_engine' : 'handlebars', 'markdown_pattern' : '{{#if _Record_Status_Detail}}{{{Record_Status_Detail}}}\n{{#each $self}}- [{{{this.rowName}}}]({{{this.uri.detailed}}}) \n{{/each}}{{/if}}',  },
                'aggregate' : 'array_d',
                'markdown_name' : 'Record Status Detail',
            },
            {
                'entity' : True,
                'source' : [{'inbound': ['PDB', 'Entry_Generated_File_Structure_Id_fkey']}, 'RID'],
                'display' : {'template_engine' : 'handlebars', 'markdown_pattern' : '{{#each $self}}- {{{this.rowName}}} \n{{/each}}',  },
                'aggregate' : 'array_d',
                'markdown_name' : 'System Generated Files',
            },
            'Deposit_Date', 
            'Release_Date', 
            'Method_Details', 
            #'New_Chem_Comp_Pending', 
            'Manual_Processing', 
            { 'source' : [{'outbound': ['PDB', 'entry_RCB_fkey']}, 'Full_Name'], 'markdown_name' : 'RCB',  },
            { 'source' : [{'outbound': ['PDB', 'entry_RMB_fkey']}, 'Full_Name'], 'markdown_name' : 'RMB',  },
            'RCT', 
            'RMT', 
        ],
        'entry' :  [
            'mmCIF_File_URL', 
            'Image_File_URL', 
            ['PDB', 'entry_Workflow_Status_fkey'], 
            'Method_Details', 
            #'New_Chem_Comp_Pending', 
            'Manual_Processing', 
            'Notes', 
        ],
        'filter' :  {
            'and' :  [
                {
                    'source' : [{'outbound': ['PDB', 'entry_Accession_Code_fkey']}, 'RID'],
                    'markdown_name' : 'Accession Code',
                    'hide_null_choice' : False,
                    'hide_not_null_choice' : False,
                },
                {
                    'source' : [{'outbound': ['PDB', 'entry_RCB_fkey']}, 'Full_Name'],
                    'markdown_name' : 'Created By',
                    'hide_null_choice' : True,
                    'hide_not_null_choice' : True,
                },
                { 'source' : 'Deposit_Date', 'markdown_name' : 'Deposit Date',  },
                { 'source' : 'Release_Date', 'markdown_name' : 'Release Date',  },
                { 'source' : 'Submitter_Flag_Date', 'markdown_name' : 'Last Communicated',  },
                {
                    'source' : [{'outbound': ['PDB', 'entry_Workflow_Status_fkey']}, 'RID'],
                    'markdown_name' : 'Workflow Status',
                    'hide_null_choice' : True,
                    'hide_not_null_choice' : True,
                },
                { 'source' : [{'inbound': ['PDB', 'citation_author_structure_id_fkey']}, 'RID'], 'markdown_name' : 'Authors',  },
                { 'source' : [{'inbound': ['PDB', 'citation_structure_id_fkey']}, 'RID'], 'markdown_name' : 'Citations',  },
                { 'source' : [{'inbound': ['PDB', 'software_structure_id_fkey']}, 'RID'], 'markdown_name' : 'Software',  },
                #{ 'source' : 'New_Chem_Comp_Pending', 'markdown_name' : 'New Chem Comp Pending',  },
                { 'source' : 'Manual_Processing', 'markdown_name' : 'Manual Processing',  },
            ],
        },
        'detailed' :  [
            'RID', 
            'id', 
            { 'sourcekey' : 'entry_RCB',  },
            { 'source' : [{'outbound': ['PDB', 'entry_RMB_fkey']}, 'Full_Name'], 'markdown_name' : 'RMB',  },
            'mmCIF_File_URL', 
            { 'source' : 'mmCIF_File_Bytes', 'markdown_name' : 'mmCIF File Size (Bytes)',  },
            'Image_File_URL', 
            { 'source' : 'Image_File_Bytes', 'markdown_name' : 'Image File Size (Bytes)',  },
            ['PDB', 'entry_Accession_Code_fkey'], 
            ['PDB', 'entry_Workflow_Status_fkey'], 
            'Process_Status', 
            {
                'entity' : True,
                'source' : [{'inbound': ['PDB', 'Entry_Error_File_Entry_RID_fkey']}, 'RID'],
                'display' : {'template_engine' : 'handlebars', 'markdown_pattern' : '{{#if _Record_Status_Detail}}{{{Record_Status_Detail}}}\n{{#each $self}}- [{{{this.rowName}}}]({{{this.uri.detailed}}}) \n{{/each}}{{/if}}',  },
                'aggregate' : 'array_d',
                'markdown_name' : 'Record Status Detail',
            },
            'Deposit_Date', 
            'Release_Date', 
            'Method_Details', 
            'Submitter_Flag', 
            'Submitter_Flag_Date', 
            #'New_Chem_Comp_Pending', 
            'Manual_Processing', 
            'Notes', 
            { 'display' : {'wait_for': ['molstar_image'], 'template_engine': 'handlebars', 'markdown_pattern': '{{#if (or (eq Workflow_Status "mmCIF CREATED") (eq Workflow_Status "SUBMISSION COMPLETE") (eq Workflow_Status "HOLD") (eq Workflow_Status "REL") (eq Workflow_Status "REL"))}} {{#each molstar_image}}::: iframe [](/molstar/embedded.html?url={{this.values.File_URL}}){style="min-width:800px; min-height:700px; height:70vh;" class=chaise-autofill  } \n :::{{/each}}{{else}}Not Available{{/if}}'}, 'markdown_name' : '3D Visualization',  },
            ['PDB', 'entry_Owner_fkey'], 
        ],
        'entry/edit' :  [
            'mmCIF_File_URL', 
            'Image_File_URL', 
            ['PDB', 'entry_Workflow_Status_fkey'], 
            'Method_Details', 
            'Deposit_Date', 
            'Release_Date', 
            'Submitter_Flag', 
            'Submitter_Flag_Date', 
            #'New_Chem_Comp_Pending', 
            'Manual_Processing', 
            'Notes', 
        ],
        'export/compact' :  [
            'RID', 
            'id', 
            'mmCIF_File_Name', 
            'mmCIF_File_URL', 
            'Image_File_Name', 
            'Image_File_URL', 
            'Workflow_Status', 
            'Accession_Code', 
            'Deposit_Date', 
            'Release_Date', 
            'Method_Details', 
            'Submitter_Flag', 
            'Submitter_Flag_Date', 
            'Record_Status_Detail', 
        ],
    })

    table.source_definitions.update({
        'fkeys' :  [],
        'columns' :  True,
        'sources' : {
            'entry_RCB' : {
                'entity' : True,
                'source' : [{'outbound': ['PDB', 'entry_RCB_fkey']}, 'RID'],
                'display' : { 'template_engine' : 'handlebars', 'markdown_pattern' : '{{{$self.values.Full_Name}}} ({{{$self.values.Email}}})', },
                'markdown_name' : 'RCB',
            },
            'entry_RMB' : {
                'entity' : True,
                'source' : [{'outbound': ['PDB', 'entry_RMB_fkey']}, 'RID'],
                'display' : { 'template_engine' : 'handlebars', 'markdown_pattern' : '{{{$self.values.Full_Name}}} ({{{$self.values.Email}}})', },
                'markdown_name' : 'RMB',
            },
            'molstar_image' : {
                'entity' : True,
                'source' : [{'inbound': ['PDB', 'Entry_Generated_File_Structure_Id_fkey']}, {'filter': 'File_Type', 'operand_pattern': 'mmCIF'}, 'RID'],
            },
            'Accession_Code_RCB' : {
                'entity' : True,
                'source' : [{'outbound': ['PDB', 'Accession_Code_RCB_fkey']}, 'RID'],
                'display' : { 'template_engine' : 'handlebars', 'markdown_pattern' : '{{{$self.values.Full_Name}}} ({{{$self.values.Email}}})', },
                'markdown_name' : 'RCB',
            },
        },
    })

    table.visible_foreign_keys.update({
        'filter' :  'detailed',     
        'detailed' :  [
            ['PDB', 'Entry_Generated_File_Structure_Id_fkey'], 
            ['PDB', 'struct_entry_id_fkey'], 
            ['PDB', 'audit_author_structure_id_fkey'], 
            ['PDB', 'citation_structure_id_fkey'], 
            ['PDB', 'citation_author_structure_id_fkey'], 
            ['PDB', 'software_structure_id_fkey'], 
            ['PDB', 'chem_comp_structure_id_fkey'], 
            ['PDB', 'entity_structure_id_fkey'], 
            ['PDB', 'entity_name_com_structure_id_fkey'], 
            ['PDB', 'entity_name_sys_structure_id_fkey'], 
            ['PDB', 'entity_src_gen_structure_id_fkey'], 
            ['PDB', 'struct_ref_structure_id_fkey'], 
            ['PDB', 'struct_ref_seq_structure_id_fkey'], 
            ['PDB', 'struct_ref_seq_dif_structure_id_fkey'], 
            ['PDB', 'entity_poly_structure_id_fkey'], 
            ['PDB', 'pdbx_entity_nonpoly_structure_id_fkey'], 
            ['PDB', 'entity_poly_seq_structure_id_fkey'], 
            ['PDB', 'atom_type_structure_id_fkey'], 
            ['PDB', 'struct_asym_structure_id_fkey'], 
            ['PDB', 'ihm_dataset_list_structure_id_fkey'], 
            ['PDB', 'ihm_dataset_group_structure_id_fkey'], 
            ['PDB', 'ihm_dataset_group_link_structure_id_fkey'], 
            ['PDB', 'ihm_data_transformation_structure_id_fkey'], 
            ['PDB', 'ihm_related_datasets_structure_id_fkey'], 
            ['PDB', 'ihm_dataset_related_db_reference_structure_id_fkey'], 
            ['PDB', 'ihm_external_reference_info_structure_id_fkey'], 
            ['PDB', 'ihm_external_files_structure_id_fkey'], 
            ['PDB', 'ihm_dataset_external_reference_structure_id_fkey'], 
            ['PDB', 'ihm_entity_poly_segment_structure_id_fkey'], 
            ['PDB', 'ihm_struct_assembly_structure_id_fkey'], 
            ['PDB', 'ihm_struct_assembly_details_structure_id_fkey'], 
            ['PDB', 'ihm_struct_assembly_class_structure_id_fkey'], 
            ['PDB', 'ihm_struct_assembly_class_link_structure_id_fkey'], 
            ['PDB', 'ihm_starting_model_details_structure_id_fkey'], 
            ['PDB', 'ihm_starting_comparative_models_structure_id_fkey'], 
            ['PDB', 'ihm_starting_computational_models_structure_id_fkey'], 
            ['PDB', 'ihm_starting_model_seq_dif_structure_id_fkey'], 
            ['PDB', 'ihm_model_representation_structure_id_fkey'], 
            ['PDB', 'ihm_model_representation_details_structure_id_fkey'], 
            ['PDB', 'ihm_modeling_protocol_structure_id_fkey'], 
            ['PDB', 'ihm_modeling_protocol_details_structure_id_fkey'], 
            ['PDB', 'ihm_modeling_post_process_structure_id_fkey'], 
            ['PDB', 'ihm_model_list_structure_id_fkey'], 
            ['PDB', 'ihm_model_group_structure_id_fkey'], 
            ['PDB', 'ihm_model_group_link_structure_id_fkey'], 
            ['PDB', 'ihm_model_representative_structure_id_fkey'], 
            ['PDB', 'ihm_residues_not_modeled_structure_id_fkey'], 
            ['PDB', 'ihm_multi_state_modeling_structure_id_fkey'], 
            ['PDB', 'ihm_multi_state_model_group_link_structure_id_fkey'], 
            ['PDB', 'ihm_ordered_model_structure_id_fkey'], 
            ['PDB', 'ihm_ordered_ensemble_structure_id_fkey'], 
            ['PDB', 'ihm_ensemble_info_structure_id_fkey'], 
            ['PDB', 'ihm_ensemble_sub_sample_structure_id_fkey'], 
            ['PDB', 'ihm_localization_density_files_structure_id_fkey'], 
            ['PDB', 'ihm_2dem_class_average_restraint_structure_id_fkey'], 
            ['PDB', 'ihm_2dem_class_average_fitting_structure_id_fkey'], 
            ['PDB', 'ihm_3dem_restraint_structure_id_fkey'], 
            ['PDB', 'ihm_sas_restraint_structure_id_fkey'], 
            ['PDB', 'ihm_epr_restraint_structure_id_fkey'], 
            ['PDB', 'ihm_chemical_component_descriptor_structure_id_fkey'], 
            ['PDB', 'ihm_probe_list_structure_id_fkey'], 
            ['PDB', 'ihm_poly_probe_position_structure_id_fkey'], 
            ['PDB', 'ihm_poly_probe_conjugate_structure_id_fkey'], 
            ['PDB', 'ihm_ligand_probe_structure_id_fkey'], 
            ['PDB', 'ihm_geometric_object_list_structure_id_fkey'], 
            ['PDB', 'ihm_geometric_object_center_structure_id_fkey'], 
            ['PDB', 'ihm_geometric_object_transformation_structure_id_fkey'], 
            ['PDB', 'ihm_geometric_object_sphere_structure_id_fkey'], 
            ['PDB', 'ihm_geometric_object_torus_structure_id_fkey'], 
            ['PDB', 'ihm_geometric_object_half_torus_structure_id_fkey'], 
            ['PDB', 'ihm_geometric_object_axis_structure_id_fkey'], 
            ['PDB', 'ihm_geometric_object_plane_structure_id_fkey'], 
            ['PDB', 'Entry_Related_File_entry_id_fkey'], 
            ['PDB', 'ihm_pseudo_site_structure_id_fkey'], 
            ['PDB', 'ihm_cross_link_list_structure_id_fkey'], 
            ['PDB', 'ihm_cross_link_restraint_structure_id_fkey'], 
            ['PDB', 'ihm_cross_link_pseudo_site_structure_id_fkey'], 
            ['PDB', 'ihm_cross_link_result_structure_id_fkey'], 
            ['PDB', 'ihm_cross_link_result_parameters_structure_id_fkey'], 
            ['PDB', 'ihm_predicted_contact_restraint_structure_id_fkey'], 
            ['PDB', 'ihm_hydroxyl_radical_fp_restraint_structure_id_fkey'], 
            ['PDB', 'ihm_hdx_restraint_structure_id_fkey'], 
            ['PDB', 'ihm_feature_list_structure_id_fkey'], 
            ['PDB', 'ihm_poly_atom_feature_structure_id_fkey'], 
            ['PDB', 'ihm_poly_residue_feature_structure_id_fkey'], 
            ['PDB', 'ihm_non_poly_feature_structure_id_fkey'], 
            ['PDB', 'ihm_interface_residue_feature_structure_id_fkey'], 
            ['PDB', 'ihm_pseudo_site_feature_structure_id_fkey'], 
            ['PDB', 'ihm_derived_distance_restraint_structure_id_fkey'], 
            ['PDB', 'ihm_derived_angle_restraint_structure_id_fkey'], 
            ['PDB', 'ihm_derived_dihedral_restraint_structure_id_fkey'], 
            ['PDB', 'ihm_geometric_object_distance_restraint_structure_id_fkey'], 
            ['PDB', 'ihm_multi_state_scheme_structure_id_fkey'], 
            ['PDB', 'ihm_multi_state_scheme_connectivity_structure_id_fkey'], 
            ['PDB', 'ihm_kinetic_rate_structure_id_fkey'], 
            ['PDB', 'ihm_relaxation_time_structure_id_fkey'], 
            ['PDB', 'ihm_relaxation_time_multi_state_scheme_structure_id_fkey'], 
            {
                'source' : [{'inbound': ['PDB', 'ihm_entry_collection_mapping_entry_id_fkey']}, {'outbound': ['PDB', 'ihm_entry_collection_mapping_collection_id_fkey']}, 'RID'],
                'comment' : 'Collections to which the entry belongs',
                'markdown_name' : 'Entry Collections',
            },
            { 'source' : [{'inbound': ['PDB', 'Curation_Log_Entry_fkey']}, 'RID'], 'markdown_name' : 'Curation Log',  },
            ['PDB', 'audit_conform_structure_id_fkey'], 
            ['PDB', 'pdbx_entity_poly_na_type_structure_id_fkey'], 
        ],
    })
    
    
   # ----------------------------
    schema.tables["entry"].columns["Image_File_URL"].display.update(
        {'name' : 'User Provided Image File', }
    )

    # ----------------------------
    schema.tables["entry"].columns["Image_File_URL"].column_display.update({
        'compact' : {
            'template_engine' : 'handlebars',
            'markdown_pattern' : '{{#if Image_File_URL }}[![{{Image_File_Name}}]({{{Image_File_URL}}}){width=auto height=100}]({{{Image_File_URL}}}){target=_blank}{{/if}}',
        },
        'detailed' : {
            'template_engine' : 'handlebars',
            'markdown_pattern' : '{{#if Image_File_URL }}[![{{Image_File_Name}}]({{{Image_File_URL}}}){width=auto height=200}]({{{Image_File_URL}}}){target=_blank}{{/if}}', },
    })
    
    # ----------------------------
    schema.tables["entry"].columns["mmCIF_File_URL"].display.update(
        {'name' : 'User Provided mmCIF File', }
    )
    
    # ----------------------------
    schema.tables["entry"].columns["Submitter_Flag_Date"].display.update(
        {'name' : 'Last Communicated', }
    )
    
    # ----------------------------
    schema.tables["entry"].columns["Method_Details"].display.update(
        {'name' : 'User Provided Method Details', }
    )

# -- ==================================================================================================

# -- ---------------------------------------------------------------------------------
def update_PDB_Accession_Code(model):
    schema = model.schemas["PDB"]
    table = schema.tables["Accession_Code"]
    # ----------------------------
    schema.tables["Accession_Code"].visible_columns.update({
        '*' :  [
            'RID', 
            'Accession_Serial', 
            'Accession_Code', 
            {'source' : 'PDBDEV_Accession_Code', 'markdown_name' : 'PDBDEV Accession Code', },
            {'source' : 'PDB_Extended_Code', 'markdown_name' : 'PDB Extended Code', },
            {'source' : 'PDB_Code', 'markdown_name' : 'PDB Code', },
            {'source' : 'PDB_Accession_Code', 'markdown_name' : 'PDB Accession Code', },
            {'source' : [{'outbound': ['PDB', 'Accession_Code_Entry_fkey']}, 'RID'], 'markdown_name' : 'Entry', },
            {'source' : [{'outbound': ['PDB', 'Accession_Code_Entry_fkey']}, {'outbound': ['PDB', 'entry_Workflow_Status_fkey']}, 'Name'],
             'markdown_name' : 'Workflow Status', },
            'Notes', 
            {'source' : [{'outbound': ['PDB', 'Accession_Code_RCB_fkey']}, 'Full_Name'], 'markdown_name' : 'RCB', },
            {'source' : [{'outbound': ['PDB', 'Accession_Code_RMB_fkey']}, 'Full_Name'], 'markdown_name' : 'RMB', },
            'RCT', 
            'RMT', 
            ['PDB', 'Accession_Code_Owner_fkey'], 
        ],
        'entry' :  [
            {'source' : [{'outbound': ['PDB', 'Accession_Code_Entry_fkey']}, 'RID'], 'markdown_name' : 'Entry', },
            'Accession_Serial', 
            'Accession_Code', 
            {'source' : 'PDBDEV_Accession_Code', 'markdown_name' : 'PDBDEV Accession Code', },
            {'source' : 'PDB_Extended_Code', 'markdown_name' : 'PDB Extended Code', },
            {'source' : 'PDB_Code', 'markdown_name' : 'PDB Code', },
            {'source' : 'PDB_Accession_Code', 'markdown_name' : 'PDB Accession Code', },
            'Notes', 
        ],
        'filter' :  {
            'and' :  [
                {'source' : 'Accession_Serial', 'markdown_name' : 'Accession Serial', },
                {'source' : 'Accession_Code', 'markdown_name' : 'Accession Code', },
                {'source' : 'PDBDEV_Accession_Code', 'markdown_name' : 'PDBDEV Accession Code', },
                {'source' : 'PDB_Extended_Code', 'markdown_name' : 'PDB Extended Code', },
                {'source' : 'PDB_Code', 'markdown_name' : 'PDB Code', },
                {'source' : 'PDB_Accession_Code', 'markdown_name' : 'PDB Accession Code', },
                {
                    'source' : [{'outbound': ['PDB', 'Accession_Code_Entry_fkey']}, 'RID'],
                    'markdown_name' : 'Entry',
                    'hide_null_choice' : False,
                    'hide_not_null_choice' : False,
                },
                {'source' : [{'outbound': ['PDB', 'Accession_Code_Entry_fkey']}, {'outbound': ['PDB', 'entry_Workflow_Status_fkey']}, 'Name'],
                 'markdown_name' : 'Workflow Status', },
            ],
        },
        'detailed' :  [
            'RID', 
            {'source' : [{'outbound': ['PDB', 'Accession_Code_RCB_fkey']}, 'Full_Name'], 'markdown_name' : 'RCB', },
            {'source' : [{'outbound': ['PDB', 'Accession_Code_RMB_fkey']}, 'Full_Name'], 'markdown_name' : 'RMB', },
            'Accession_Serial', 
            'Accession_Code', 
            {'source' : 'PDBDEV_Accession_Code', 'markdown_name' : 'PDBDEV Accession Code', },
            {'source' : 'PDB_Extended_Code', 'markdown_name' : 'PDB Extended Code', },
            {'source' : 'PDB_Code', 'markdown_name' : 'PDB Code', },
            {'source' : 'PDB_Accession_Code', 'markdown_name' : 'PDB Accession Code', },
            'Notes', 
            {'source' : [{'outbound': ['PDB', 'Accession_Code_Entry_fkey']}, 'RID'], 'markdown_name' : 'Entry', },
            {'source' : [{'outbound': ['PDB', 'Accession_Code_Entry_fkey']}, {'outbound': ['PDB', 'entry_Workflow_Status_fkey']}, 'Name'],
             'markdown_name' : 'Workflow Status', },
        ],
        'entry/edit' :  [
            {'source' : [{'outbound': ['PDB', 'Accession_Code_Entry_fkey']}, 'RID'], 'markdown_name' : 'Entry', },
            'Accession_Serial', 
            'Accession_Code', 
            {'source' : 'PDBDEV_Accession_Code', 'markdown_name' : 'PDBDEV Accession Code', },
            {'source' : 'PDB_Extended_Code', 'markdown_name' : 'PDB Extended Code', },
            {'source' : 'PDB_Code', 'markdown_name' : 'PDB Code', },
            {'source' : 'PDB_Accession_Code', 'markdown_name' : 'PDB Accession Code', },
            'Notes', 
        ],
    })

# -- -----------------------------------------------------------------------------
def update_PDB_Curation_Log(model):
    schema = model.schemas["PDB"]
    table = schema.tables["Curation_Log"]
    # ----------------------------
    schema.tables["Curation_Log"].display.update(
        {'name' : 'Curation Log', 'comment_display' : {'*': {'table_comment_display': 'inline'}}, }
    )
    
    # ----------------------------
    schema.tables["Curation_Log"].visible_columns.update({
        '*' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'Curation_Log_Entry_fkey']}, 'id'],
                'comment' : 'Entry Id',
                'markdown_name' : 'Entry Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'Curation_Log_Entry_fkey']}, 'Accession_Code'],
                'comment' : 'Entry Accession Code',
                'markdown_name' : 'Accession Code',
            },
            'Log_Date', 
            'Details', 
            'Submitter_Allow', 
            {'source' : [{'outbound': ['PDB', 'Curation_Log_RCB_fkey']}, 'Full_Name'], 'markdown_name' : 'RCB', },
            {'source' : [{'outbound': ['PDB', 'Curation_Log_RMB_fkey']}, 'Full_Name'], 'markdown_name' : 'RMB', },
            'RCT', 
            'RMT', 
        ],
        'entry' :  [
            {
                'source' : [{'outbound': ['PDB', 'Curation_Log_Entry_fkey']}, 'id'],
                'comment' : 'Entry Id',
                'markdown_name' : 'Entry Id',
            },
            'Log_Date', 
            'Details', 
            'Submitter_Allow', 
        ],
        'detailed' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'Curation_Log_Entry_fkey']}, 'id'],
                'comment' : 'Entry Id',
                'markdown_name' : 'Entry Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'Curation_Log_Entry_fkey']}, 'Accession_Code'],
                'comment' : 'Entry Accession Code',
                'markdown_name' : 'Accession Code',
            },
            'Log_Date', 
            'Details', 
            'Submitter_Allow', 
            {'source' : [{'outbound': ['PDB', 'Curation_Log_RCB_fkey']}, 'Full_Name'], 'markdown_name' : 'RCB', },
            {'source' : [{'outbound': ['PDB', 'Curation_Log_RMB_fkey']}, 'Full_Name'], 'markdown_name' : 'RMB', },
            'RCT', 
            'RMT', 
        ],
    })

# -- -----------------------------------------------------------------------------
def update_PDB_Data_Dictionary(model):
    schema = model.schemas["PDB"]
    table = schema.tables["Data_Dictionary"]
    # ----------------------------
    schema.tables["Data_Dictionary"].table_display.update({
        'row_name' : { 'row_markdown_pattern' : '{{{Name}}} (v {{{Version}}})', },
    })

    # ----------------------------
    schema.tables["Data_Dictionary"].visible_columns.update({
        '*' :  [
            'RID', 
            ['PDB', 'Data_Dictionary_Name_fkey'], 
            ['PDB', 'Data_Dictionary_Category_fkey'], 
            'Version', 
            'Location', 
            'RCT', 
            'RMT', 
        ],
        'entry' :  [
            ['PDB', 'Data_Dictionary_Name_fkey'], 
            ['PDB', 'Data_Dictionary_Category_fkey'], 
            'Version', 
            'Location', 
        ],
        'detailed' :  [
            'RID', 
            ['PDB', 'Data_Dictionary_Name_fkey'], 
            ['PDB', 'Data_Dictionary_Category_fkey'], 
            'Version', 
            'Location', 
        ],
    })

    # ----------------------------
    schema.tables["Data_Dictionary"].columns["Location"].column_display.update({
        '*' : { 'markdown_pattern' : '[{{{Name}}} (v {{{Version}}})]({{{Location}}})', },
    })

# -- -----------------------------------------------------------------------------
def update_PDB_Entry_Error_File(model):
    schema = model.schemas["PDB"]
    table = schema.tables["Entry_Error_File"]
    # ----------------------------
    schema.tables["Entry_Error_File"].display.update(
        {'name' : 'System Generated mmCIF Validation Error Files', 'comment_display' : {'*': {'table_comment_display': 'inline'}}, }
    )
    
    # ----------------------------
    schema.tables["Entry_Error_File"].table_display.update({
        'row_name' : { 'row_markdown_pattern' : '{{{File_Name}}}', },
    })

    # ----------------------------
    schema.tables["Entry_Error_File"].visible_columns.update({
        '*' :  [
            'RID', 
            ['PDB', 'Entry_Error_File_Entry_RID_fkey'], 
            'File_Name', 
            'File_URL', 
            ['PDB', 'Entry_Error_File_System_Generated_File_Type_fkey'], 
        ],
        'entry' :  [
            'File_URL', 
            ['PDB', 'Entry_Error_File_Entry_RID_fkey'], 
            ['PDB', 'Entry_Error_File_System_Generated_File_Type_fkey'], 
        ],
        'detailed' :  [
            'RID', 
            ['PDB', 'Entry_Error_File_Entry_RID_fkey'], 
            'File_Name', 
            'File_Bytes', 
            'File_MD5', 
            'File_URL', 
            ['PDB', 'Entry_Error_File_System_Generated_File_Type_fkey'], 
        ],
    })

    # ----------------------------
    schema.tables["Entry_Error_File"].columns["File_URL"].display.update(
        {'name' : 'System Generated mmCIF Validation Error Files', }
    )

    # ----------------------------
    schema.tables["Entry_Error_File"].columns["File_URL"].column_display.update({
        '*' : { 'markdown_pattern' : '[{{{File_Name}}}]({{{File_URL}}})', },
    })

# -- -----------------------------------------------------------------------------
def update_PDB_Entry_Generated_File(model):
    schema = model.schemas["PDB"]
    table = schema.tables["Entry_Generated_File"]
    # ----------------------------
    schema.tables["Entry_Generated_File"].display.update(
        {'name' : 'System Generated Files', 'comment_display' : {'*': {'table_comment_display': 'inline'}}, }
    )
    
    # ----------------------------
    schema.tables["Entry_Generated_File"].table_display.update({
        'row_name' : { 'row_markdown_pattern' : '[{{{File_Name}}}]({{{File_URL}}})', },
    })

    # ----------------------------
    schema.tables["Entry_Generated_File"].visible_columns.update({
        '*' :  [
            'RID', 
            'File_URL', 
            ['PDB', 'Entry_Generated_File_System_Generated_File_Type_fkey'], 
            {
                'entity' : True,
                'source' : [{'inbound': ['PDB', 'Conform_Dictionary_Entry_Generated_File_fkey']}, {'outbound': ['PDB', 'Conform_Dictionary_Data_Dictionary_fkey']}, 'RID'],
                'display' : { 'array_ux_mode' : 'ulist', },
                'aggregate' : 'array_d',
                'array_options' : { 'order' : [{'column': 'Name', 'descending': False}, {'column': 'Version', 'descending': False}], },
                'markdown_name' : 'Conform Dictionary',
            },
            ['PDB', 'Entry_Generated_File_Structure_Id_fkey'], 
            'RCT', 
            'RMT', 
        ],
        'entry' :  [
            'File_URL', 
            ['PDB', 'Entry_Generated_File_System_Generated_File_Type_fkey'], 
            ['PDB', 'Entry_Generated_File_Structure_Id_Entry_RCB_fkey'], 
        ],
        'detailed' :  [
            'RID', 
            'File_URL', 
            ['PDB', 'Entry_Generated_File_System_Generated_File_Type_fkey'], 
            {
                'entity' : True,
                'source' : [{'inbound': ['PDB', 'Conform_Dictionary_Entry_Generated_File_fkey']}, {'outbound': ['PDB', 'Conform_Dictionary_Data_Dictionary_fkey']}, 'RID'],
                'display' : { 'array_ux_mode' : 'ulist', },
                'aggregate' : 'array_d',
                'array_options' : { 'order' : [{'column': 'Name', 'descending': False}, {'column': 'Version', 'descending': False}], },
                'markdown_name' : 'Conform Dictionary',
            },
            ['PDB', 'Entry_Generated_File_Structure_Id_fkey'], 
            'File_Bytes', 
            'File_MD5', 
            'RCT', 
            'RMT', 
        ],
        'entry/edit' :  [
            'File_URL', 
            ['PDB', 'Entry_Generated_File_System_Generated_File_Type_fkey'], 
            ['PDB', 'Entry_Generated_File_Structure_Id_Entry_RCB_fkey'], 
        ],
    })

    # ----------------------------
    schema.tables["Entry_Generated_File"].columns["File_URL"].display.update(
        {'name' : 'System Generated File', }
    )
    
    # ----------------------------
    schema.tables["Entry_Generated_File"].columns["File_URL"].column_display.update({
        '*' : { 'markdown_pattern' : '[{{{File_Name}}}]({{{File_URL}}})', },
    })

# -- -----------------------------------------------------------------------------
def update_PDB_Entry_Latest_Archive(model):
    schema = model.schemas["PDB"]
    table = schema.tables["Entry_Latest_Archive"]
    # ----------------------------
    schema.tables["Entry_Latest_Archive"].visible_columns.update({
        '*' :  [
            'RID', 
            {'source' : [{'outbound': ['PDB', 'Entry_Latest_Archive_Entry_fkey']}, 'RID'], 'markdown_name' : 'Entry', },
            {'source' : [{'outbound': ['PDB', 'Entry_Latest_Archive_Archive_Submission_Time_fkey']}, 'RID'], 'markdown_name' : 'Archive', },
            'mmCIF_URL', 
            {'source' : [{'outbound': ['PDB', 'Entry_Latest_Archive_Entry_fkey']}, 'Accession_Code'], 'markdown_name' : 'Accession Code', },
            {'source' : [{'outbound': ['PDB', 'Entry_Latest_Archive_Entry_fkey']}, 'Workflow_Status'], 'markdown_name' : 'Workflow Status', },
            'Submitted_Files', 
            'Submission_Time', 
            'Submission_History', 
            {'source' : [{'outbound': ['PDB', 'Entry_Latest_Archive_RCB_fkey']}, 'Full_Name'], 'markdown_name' : 'RCB', },
            {'source' : [{'outbound': ['PDB', 'Entry_Latest_Archive_RMB_fkey']}, 'Full_Name'], 'markdown_name' : 'RMB', },
            'RCT', 
            'RMT', 
        ],
        'entry' :  [
            'Submission_Time', 
            {'source' : [{'outbound': ['PDB', 'Entry_Latest_Archive_Entry_fkey']}, 'RID'], 'markdown_name' : 'Entry', },
            {'source' : [{'outbound': ['PDB', 'Entry_Latest_Archive_Archive_Submission_Time_fkey']}, 'RID'], 'markdown_name' : 'Archive', },
        ],
        'filter' :  {
            'and' :  [
                {'source' : 'Submission_Time', 'markdown_name' : 'Submission Date', },
            ],
        },
        'detailed' :  [
            'RID', 
            'Submission_Time', 
            {'source' : [{'outbound': ['PDB', 'Entry_Latest_Archive_Entry_fkey']}, 'Accession_Code'], 'markdown_name' : 'Accession Code', },
            {'source' : [{'outbound': ['PDB', 'Entry_Latest_Archive_Entry_fkey']}, 'Workflow_Status'], 'markdown_name' : 'Workflow Status', },
            'Submitted_Files', 
            'mmCIF_URL', 
            'Submission_History', 
            {'source' : [{'outbound': ['PDB', 'Entry_Latest_Archive_Entry_fkey']}, 'RID'], 'markdown_name' : 'Entry', },
            {'source' : [{'outbound': ['PDB', 'Entry_Latest_Archive_Archive_Submission_Time_fkey']}, 'RID'], 'markdown_name' : 'Archive', },
            {'source' : [{'outbound': ['PDB', 'Entry_Latest_Archive_RCB_fkey']}, 'Full_Name'], 'markdown_name' : 'RCB', },
            {'source' : [{'outbound': ['PDB', 'Entry_Latest_Archive_RMB_fkey']}, 'Full_Name'], 'markdown_name' : 'RMB', },
        ],
        'entry/edit' :  [
            {'source' : [{'outbound': ['PDB', 'Entry_Latest_Archive_Entry_fkey']}, 'RID'], 'markdown_name' : 'Entry', },
            {'source' : [{'outbound': ['PDB', 'Entry_Latest_Archive_Archive_Submission_Time_fkey']}, 'RID'], 'markdown_name' : 'Archive', },
        ],
    })

    # ----------------------------
    schema.tables["Entry_Latest_Archive"].columns["mmCIF_URL"].display.update(
        {'name' : 'mmCIF', }
    )

    # ----------------------------
    schema.tables["Entry_Latest_Archive"].columns["mmCIF_URL"].column_display.update({
        '*' : { 'markdown_pattern' : '[{{Entry}}]({{#encode}}{{{mmCIF_URL}}}{{/encode}})', },
    })

# -- -----------------------------------------------------------------------------
def update_PDB_Entry_Related_File(model):
    schema = model.schemas["PDB"]
    table = schema.tables["Entry_Related_File"]
    # ----------------------------
    schema.tables["Entry_Related_File"].display.update(
        {'name' : 'Uploaded Restraint Files', 'comment_display' : {'*': {'table_comment_display': 'inline'}}, }
    )

    # ----------------------------
    schema.tables["Entry_Related_File"].visible_columns.update({
        '*' :  [
            'RID', 
            ['PDB', 'Entry_Related_File_entry_id_fkey'], 
            ['PDB', 'Entry_Related_File_File_Type_fkey'], 
            ['PDB', 'Entry_Related_File_File_Format_fkey'], 
            'File_URL', 
            'File_Bytes', 
            'File_MD5', 
            'Description', 
            ['PDB', 'Entry_Related_File_Restraint_Workflow_Status_fkey'], 
            'Restraint_Process_Status', 
            'Record_Status_Detail', 
        ],
        'entry' :  [
            ['PDB', 'Entry_Related_File_entry_id_fkey'], 
            ['PDB', 'Entry_Related_File_File_Type_fkey'], 
            ['PDB', 'Entry_Related_File_File_Format_fkey'], 
            'File_Name', 
            'File_URL', 
            'File_Bytes', 
            'File_MD5', 
            'Description', 
            ['PDB', 'Entry_Related_File_Restraint_Workflow_Status_fkey'], 
        ],
        'detailed' :  [
            'RID', 
            ['PDB', 'Entry_Related_File_entry_id_fkey'], 
            ['PDB', 'Entry_Related_File_File_Type_fkey'], 
            ['PDB', 'Entry_Related_File_File_Format_fkey'], 
            'File_URL', 
            'File_Bytes', 
            'File_MD5', 
            'Description', 
            ['PDB', 'Entry_Related_File_Restraint_Workflow_Status_fkey'], 
            'Restraint_Process_Status', 
            'Record_Status_Detail', 
            ['PDB', 'Entry_Related_File_RCB_fkey'], 
            ['PDB', 'Entry_Related_File_RMB_fkey'], 
            'RCT', 
            'RMT', 
            ['PDB', 'Entry_Related_File_Owner_fkey'], 
        ],
    })

    # ----------------------------
    schema.tables["Entry_Related_File"].columns["File_URL"].display.update(
        {'name' : 'Uploaded File', }
    )

    # ----------------------------
    schema.tables["Entry_Related_File"].foreign_keys[(schema,"Entry_Related_File_Restraint_Workflow_Status_fkey")].foreign_key.update({
        'domain_filter_pattern' :  'Restraint_Status=True',
    })

# -- -----------------------------------------------------------------------------
def update_PDB_Entry_Related_File_Templates(model):
    schema = model.schemas["PDB"]
    table = schema.tables["Entry_Related_File_Templates"]
    # ----------------------------
    schema.tables["Entry_Related_File_Templates"].display.update(
        {'name' : 'CSV Templates for Restraint Files', }
    )

    # ----------------------------
    schema.tables["Entry_Related_File_Templates"].visible_columns.update({
        '*' :  [
            'RID', 
            ['PDB', 'Entry_Template_File_File_Type_fkey'], 
            'File_URL', 
            'Description', 
        ],
        'entry' :  [
            ['PDB', 'Entry_Template_File_File_Type_fkey'], 
            'File_URL', 
            'Description', 
        ],
        'detailed' :  [
            'RID', 
            ['PDB', 'Entry_Template_File_File_Type_fkey'], 
            'File_URL', 
            'File_Bytes', 
            'File_MD5', 
            'Description', 
            ['PDB', 'Entry_Template_File_RMB_fkey'], 
            'RCT', 
            'RMT', 
            ['PDB', 'Entry_Template_File_Owner_fkey'], 
        ],
    })

# -- -----------------------------------------------------------------------------
def update_PDB_PDB_Archive(model):
    schema = model.schemas["PDB"]
    table = schema.tables["PDB_Archive"]
    # ----------------------------
    schema.tables["PDB_Archive"].display.update(
        {'name' : 'PDB Archive', 'comment_display' : {'*': {'table_comment_display': 'inline'}}, }
    )

    # ----------------------------
    schema.tables["PDB_Archive"].visible_columns.update({
        '*' :  [
            'RID', 
            'Submission_Time', 
            'Submitted_Entries', 
            'New_Released_Entries', 
            'Re_Released_Entries', 
            'Current_File_Holdings_URL', 
            'Released_Structures_LMD_URL', 
            'Unreleased_Entries_URL', 
            {'source' : [{'outbound': ['PDB', 'PDB_Archive_RCB_fkey']}, 'Full_Name'], 'markdown_name' : 'RCB', },
            {'source' : [{'outbound': ['PDB', 'PDB_Archive_RMB_fkey']}, 'Full_Name'], 'markdown_name' : 'RMB', },
            'RCT', 
            'RMT', 
        ],
        'entry' :  [
            'Submission_Time', 
            'Submitted_Entries', 
            'New_Released_Entries', 
            'Re_Released_Entries', 
            'Current_File_Holdings_URL', 
            'Released_Structures_LMD_URL', 
            'Unreleased_Entries_URL', 
        ],
        'filter' :  {
            'and' :  [
                {'source' : 'Submission_Time', 'markdown_name' : 'Submission Date', },
                {'source' : 'Submitted_Entries', 'markdown_name' : 'Submitted Entries', },
                {'source' : 'New_Released_Entries', 'markdown_name' : 'New Released Entries', },
                {'source' : 'Re_Released_Entries', 'markdown_name' : 'Re-Released Entries', },
            ],
        },
        'detailed' :  [
            'RID', 
            'Submission_Time', 
            'Submitted_Entries', 
            'New_Released_Entries', 
            'Re_Released_Entries', 
            'Current_File_Holdings_URL', 
            {'source' : 'Current_File_Holdings_Bytes', 'markdown_name' : 'Current File Holdings Size (Bytes)', },
            'Released_Structures_LMD_URL', 
            {'source' : 'Released_Structures_LMD_Bytes', 'markdown_name' : 'Released Structures LMD Size (Bytes)', },
            'Unreleased_Entries_URL', 
            {'source' : 'Unreleased_Entries_Bytes', 'markdown_name' : 'Unreleased Entries Bytes Size (Bytes)', },
            {'source' : [{'outbound': ['PDB', 'PDB_Archive_RCB_fkey']}, 'Full_Name'], 'markdown_name' : 'RCB', },
            {'source' : [{'outbound': ['PDB', 'PDB_Archive_RMB_fkey']}, 'Full_Name'], 'markdown_name' : 'RMB', },
        ],
        'entry/edit' :  [
            'Submission_Time', 
            'Submitted_Entries', 
            'New_Released_Entries', 
            'Re_Released_Entries', 
            'Current_File_Holdings_URL', 
            'Released_Structures_LMD_URL', 
            'Unreleased_Entries_URL', 
        ],
    })

    # ----------------------------
    schema.tables["PDB_Archive"].columns["Current_File_Holdings_URL"].display.update(
        {'name' : 'Current File Holdings', }
    )

    # ----------------------------
    schema.tables["PDB_Archive"].columns["Current_File_Holdings_MD5"].display.update(
        {'name' : 'Current File Holdings MD5', }
    )

    # ----------------------------
    schema.tables["PDB_Archive"].columns["Released_Structures_LMD_Name"].display.update(
        {'name' : 'Released Structures LMD Name', }
    )
    
    # ----------------------------
    schema.tables["PDB_Archive"].columns["Released_Structures_LMD_URL"].display.update(
        {'name' : 'Released Structures LMD', }
    )

    # ----------------------------
    schema.tables["PDB_Archive"].columns["Released_Structures_LMD_MD5"].display.update(
        {'name' : 'Released Structures LMD MD5', }
    )

    # ----------------------------
    schema.tables["PDB_Archive"].columns["Unreleased_Entries_URL"].display.update(
        {'name' : 'Unreleased Entries', }
    )

    # ----------------------------
    schema.tables["PDB_Archive"].columns["Unreleased_Entries_MD5"].display.update(
        {'name' : 'Unreleased Entries MD5', }
    )


# -- ---------------------------------------------------------------------------------
def update_PDB_Supported_Dictionary(model):
    schema = model.schemas["PDB"]
    table = schema.tables["Supported_Dictionary"]
    # ----------------------------
    schema.tables["Supported_Dictionary"].visible_columns.update({
        '*' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'Supported_Dictionary_fkey']}, 'RID'],
                'comment' : 'A reference to table Data_Dictionary.RID.',
                'markdown_name' : 'Data Dictionary',
            },
            {
                'source' : [{'outbound': ['PDB', 'Supported_Dictionary_fkey']}, 'Category'],
                'comment' : 'A reference to table Data_Dictionary.Category.',
                'markdown_name' : 'Category',
            },
            'RCT', 
            'RMT', 
        ],
        'entry' :  [
            {
                'source' : [{'outbound': ['PDB', 'Supported_Dictionary_fkey']}, 'RID'],
                'comment' : 'A reference to table Data_Dictionary.RID.',
                'markdown_name' : 'Data Dictionary',
            },
        ],
        'detailed' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'Supported_Dictionary_fkey']}, 'RID'],
                'comment' : 'A reference to table Data_Dictionary.RID.',
                'markdown_name' : 'Data Dictionary',
            },
            {
                'source' : [{'outbound': ['PDB', 'Supported_Dictionary_fkey']}, 'Category'],
                'comment' : 'A reference to table Data_Dictionary.Category.',
                'markdown_name' : 'Category',
            },
        ],
    })


# -- =================================================================================    
def update_PDB_annotations(model):
    update_PDB(model)
    
    # -- list of specific tables    
    update_PDB_entry(model)
    update_PDB_base_annotations(model)
    update_PDB_ihm_annotations(model)
    
    update_PDB_Accession_Code(model)
    update_PDB_Curation_Log(model)
    update_PDB_Data_Dictionary(model)
    update_PDB_Entry_Error_File(model)
    update_PDB_Entry_Generated_File(model)
    update_PDB_Entry_Latest_Archive(model)
    update_PDB_Entry_Related_File(model)
    update_PDB_Entry_Related_File_Templates(model)
    update_PDB_PDB_Archive(model)
    update_PDB_Supported_Dictionary(model)
    
# --------------------------------------------------------------
def test_formats(model):
    schema_name = "PDB"
    schema = model.schemas[schema_name]

    annotations = model.schemas["PDB"].tables["entry"].table_display
    print(annotations)
    str1 = json.dumps(annotations, indent=4)
    print(str1)    
    format_annotation = format_visible_columns(annotations, indent=4)
    #format_annotation = format_dict(annotations, flatten_limit=1, indent=4)    
    print(format_annotation)
    str2 = json.dumps(eval(format_annotation), indent=4)

    assert(str1 == str2)
    print("success")

# --------------------------------------------------------------    
def check_annotations(catalog):
    model1 = catalog.getCatalogModel()
    clear_schema_annotations(model1, "PDB", per_schema_annotation_tags)
    update_PDB_annotations(model1)
    
    model2 = catalog.getCatalogModel()    

    schema = model2.schemas["PDB"]
    for tname in sorted(schema.tables.keys()):
        table1 = model1.schemas["PDB"].tables[tname]
        table2 = model2.schemas["PDB"].tables[tname]
        for k, v in table2.annotations.items():
            #if tag2name[k] not in per_schema_annotation_tags: continue
            str1 = json.dumps(table1.annotations[k])
            str2 = json.dumps(table2.annotations[k])
            if (str1 != str2):
                print("WARNING: tname: %s : %s not the same" % (tname, k))
                print("table1: %s" % str1)
                print("\ntable2: %s" % str2)
            else:
                #print("- table: %s succeeded" % (tname))
                pass

        for cname in sorted(table2.columns.elements):
            col1 = table1.columns[cname]
            col2 = table2.columns[cname]
            str1 = json.dumps(col1.annotations)
            str2 = json.dumps(col2.annotations)
            if (str1 != str2):
                print("\n!! WARNING: tname: %s cname: %s not the same" % (tname, cname))
                print("column1: %s" % str1)
                print("\ncolumn2: %s" % str2)
            else:
                #print("- tname: %s column: %s succeeded" % (tname, cname))
                pass

        for fkey2 in table2.foreign_keys:
            schema1 = model1.schemas["PDB"]
            fkey1 = table1.foreign_keys[(schema1, fkey2.constraint_name)]
            if not fkey1.annotations and not fkey2.annotations: continue
            str1 = json.dumps(sorted(fkey1.foreign_key.items()))
            str2 = json.dumps(sorted(fkey2.foreign_key.items()))
            if (str1 != str2):
                print("\n!! WARNING: tname: %s fkey: %s not the same" % (tname, fkey2.constraint_name))
                print("fkey1: %s" % str1)
                print("\nfkey2: %s" % str2)
            else:
                #print("- tname: %s constraint_name: %s succeeded" % (tname, fkey2.constraint_name))
                pass
                        
            
    print("success")
    
# -- =================================================================================    
def main(server_name, catalog_id, credentials, args):
    server = DerivaServer('https', server_name, credentials)
    catalog = server.connect_ermrest(catalog_id)
    catalog.dcctx['cid'] = DCCTX["annotation"]
    model = catalog.getCatalogModel()
    schema_name = "PDB"

    #check_annotations(catalog)

    if args.pre_print:
        print_schema_annotations(model, schema_name)

    clear_schema_annotations(model, schema_name, per_schema_annotation_tags)
    update_PDB_annotations(model)
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
