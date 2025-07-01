import json
from deriva.core import ErmrestCatalog, AttrDict, get_credential, DEFAULT_CREDENTIAL_FILE, tag, urlquote, DerivaServer, get_credential, BaseCLI
from deriva.core.ermrest_model import builtin_types, Schema, Table, Column, Key, ForeignKey
from deriva.core import urlquote, urlunquote
import requests.exceptions
from ...utils.shared import DCCTX, PDBDEV_CLI
from deriva.utils.extras.model import print_schema_model_extras, print_table_model_extras, print_schema_annotations, per_schema_annotation_tags, clear_schema_annotations

# -- -----------------------------------------------------------------------------
def update_PDB_atom_type(model):
    schema = model.schemas["PDB"]
    table = schema.tables["atom_type"]
    # ----------------------------
    schema.tables["atom_type"].display.update(
        {'markdown_name' : 'Types of Atoms', 'comment_display' : {'*': {'table_comment_display': 'inline'}}, }
    )
    
    # ----------------------------
    schema.tables["atom_type"].table_display.update({
        'row_name' : { 'row_markdown_pattern' : '{{{symbol}}}', },
    })

    # ----------------------------
    schema.tables["atom_type"].visible_columns.update({
        '*' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'atom_type_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'symbol', 
        ],
        'entry' :  [
            {
                'source' : [{'outbound': ['PDB', 'atom_type_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'symbol', 
        ],
    })

# -- -----------------------------------------------------------------------------
def update_PDB_audit_author(model):
    schema = model.schemas["PDB"]
    table = schema.tables["audit_author"]
    
    # ----------------------------
    schema.tables["audit_author"].display.update(
        {'markdown_name' : 'Authors^*^', 'comment_display' : {'*': {'table_comment_display': 'inline'}}, }
    )
    
    # ----------------------------
    schema.tables["audit_author"].visible_columns.update({
        '*' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'audit_author_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'pdbx_ordinal', 
            'name', 
        ],
        'entry' :  [
            {
                'source' : [{'outbound': ['PDB', 'audit_author_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'pdbx_ordinal', 
            'name', 
        ],
        'detailed' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'audit_author_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'pdbx_ordinal', 
            'name', 
            ['PDB', 'audit_author_RCB_fkey'], 
            ['PDB', 'audit_author_RMB_fkey'], 
            'RCT', 
            'RMT', 
            ['PDB', 'audit_author_Owner_fkey'], 
        ],
    })

    # ----------------------------
    schema.tables["audit_author"].columns["pdbx_ordinal"].display.update(
        {'name' : 'Ordinal', }
    )

# -- -----------------------------------------------------------------------------
def update_PDB_audit_conform(model):
    schema = model.schemas["PDB"]
    table = schema.tables["audit_conform"]
    # ----------------------------
    schema.tables["audit_conform"].display.update(
        {'name' : 'Dictionary Versions Compliant with the Data', 'comment_display' : {'*': {'table_comment_display': 'inline'}}, }
    )

    # ----------------------------
    schema.tables["audit_conform"].visible_columns.update({
        '*' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'audit_conform_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'dict_name', 
            'dict_location', 
            'dict_version', 
        ],
        'entry' :  [
            {
                'source' : [{'outbound': ['PDB', 'audit_conform_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'dict_name', 
            'dict_location', 
            'dict_version', 
        ],
        'detailed' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'audit_conform_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'dict_name', 
            'dict_location', 
            'dict_version', 
            ['PDB', 'audit_conform_RCB_fkey'], 
            ['PDB', 'audit_conform_RMB_fkey'], 
            'RCT', 
            'RMT', 
            ['PDB', 'audit_conform_Owner_fkey'], 
        ],
    })

    # ----------------------------
    schema.tables["audit_conform"].columns["dict_location"].display.update(
        {'name' : 'Dictionary Location', }
    )

    # ----------------------------
    schema.tables["audit_conform"].columns["dict_name"].display.update(
        {'name' : 'Dictionary Name', }
    )

    # ----------------------------
    schema.tables["audit_conform"].columns["dict_version"].display.update(
        {'name' : 'Dictionary Version', }
    )

# -- -----------------------------------------------------------------------------
def update_PDB_chem_comp(model):
    schema = model.schemas["PDB"]
    table = schema.tables["chem_comp"]
    # ----------------------------
    schema.tables["chem_comp"].display.update(
        {'markdown_name' : 'Chemical Components^*^', 'comment_display' : {'*': {'table_comment_display': 'inline'}}, }
    )
    
    # ----------------------------
    schema.tables["chem_comp"].table_display.update({
        'row_name' : { 'row_markdown_pattern' : '{{{id}}}', },
    })

    # ----------------------------
    schema.tables["chem_comp"].visible_columns.update({
        '*' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'chem_comp_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'id', 
            'name', 
            ['PDB', 'chem_comp_type_fkey'], 
            'formula', 
            'formula_weight', 
            ['PDB', 'chem_comp_mon_nstd_flag_fkey'], 
            'pdbx_synonyms', 
        ],
        'entry' :  [
            {
                'source' : [{'outbound': ['PDB', 'chem_comp_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'id', 
            'name', 
            ['PDB', 'chem_comp_type_fkey'], 
            'formula', 
            'formula_weight', 
            ['PDB', 'chem_comp_mon_nstd_flag_fkey'], 
            'pdbx_synonyms', 
        ],
    })

    # ----------------------------
    schema.tables["chem_comp"].visible_foreign_keys.update({
        'filter' :  'detailed',
        'detailed' :  [
            ['PDB', 'chem_comp_atom_comp_id_fkey'], 
            ['PDB', 'entity_poly_seq_mon_id_fkey'], 
            ['PDB', 'pdbx_entity_nonpoly_comp_id_fkey'], 
            ['PDB', 'ihm_non_poly_feature_comp_id_fkey'], 
            ['PDB', 'ihm_poly_probe_position_mut_res_chem_comp_id_fkey'], 
        ],
    })

    # ----------------------------
    schema.tables["chem_comp"].columns["mon_nstd_flag"].display.update(
        {'name' : 'Monomer Non-standard Flag', }
    )

    # ----------------------------
    schema.tables["chem_comp"].columns["pdbx_synonyms"].display.update(
        {'name' : 'Synonyms', }
    )

# -- -----------------------------------------------------------------------------
def update_PDB_chem_comp_atom(model):
    schema = model.schemas["PDB"]
    table = schema.tables["chem_comp_atom"]
    # ----------------------------
    
    schema.tables["chem_comp_atom"].display.update(
        {'name' : 'Atoms in Chemical Components', 'comment_display' : {'*': {'table_comment_display': 'inline'}}, }
    )

    # ----------------------------
    schema.tables["chem_comp_atom"].visible_columns.update({
        '*' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'chem_comp_atom_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'chem_comp_atom_comp_id_fkey']}, 'RID'],
                'comment' : 'A reference to table chem_comp.id.',
                'markdown_name' : 'Component Id',
            },
            'atom_id', 
            'type_symbol', 
            'pdbx_ordinal', 
            'alt_atom_id', 
            'charge', 
            'partial_charge', 
            'model_Cartn_x', 
            'model_Cartn_x_esd', 
            'model_Cartn_y', 
            'model_Cartn_y_esd', 
            'model_Cartn_z', 
            'model_Cartn_z_esd', 
            'pdbx_model_Cartn_x_ideal', 
            'pdbx_model_Cartn_y_ideal', 
            'pdbx_model_Cartn_z_ideal', 
            'pdbx_align', 
            'pdbx_alt_atom_id', 
            'pdbx_alt_comp_id', 
            ['PDB', 'chem_comp_atom_pdbx_aromatic_flag_fkey'], 
            'pdbx_component_atom_id', 
            'pdbx_component_comp_id', 
            'pdbx_component_entity_id', 
            'pdbx_component_id', 
            ['PDB', 'chem_comp_atom_pdbx_leaving_atom_flag_fkey'], 
            ['PDB', 'chem_comp_atom_pdbx_polymer_type_fkey'], 
            'pdbx_ref_id', 
            'pdbx_residue_numbering', 
            ['PDB', 'chem_comp_atom_pdbx_stereo_config_fkey'], 
            'pdbx_stnd_atom_id', 
            ['PDB', 'chem_comp_atom_substruct_code_fkey'], 
        ],
        'entry' :  [
            {
                'source' : [{'outbound': ['PDB', 'chem_comp_atom_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'chem_comp_atom_comp_id_fkey']}, 'RID'],
                'comment' : 'A reference to table chem_comp.id.',
                'markdown_name' : 'Component Id',
            },
            'atom_id', 
            'type_symbol', 
            'pdbx_ordinal', 
            'alt_atom_id', 
            'charge', 
            'partial_charge', 
            'model_Cartn_x', 
            'model_Cartn_x_esd', 
            'model_Cartn_y', 
            'model_Cartn_y_esd', 
            'model_Cartn_z', 
            'model_Cartn_z_esd', 
            'pdbx_model_Cartn_x_ideal', 
            'pdbx_model_Cartn_y_ideal', 
            'pdbx_model_Cartn_z_ideal', 
            'pdbx_align', 
            'pdbx_alt_atom_id', 
            'pdbx_alt_comp_id', 
            ['PDB', 'chem_comp_atom_pdbx_aromatic_flag_fkey'], 
            'pdbx_component_atom_id', 
            'pdbx_component_comp_id', 
            'pdbx_component_entity_id', 
            'pdbx_component_id', 
            ['PDB', 'chem_comp_atom_pdbx_leaving_atom_flag_fkey'], 
            ['PDB', 'chem_comp_atom_pdbx_polymer_type_fkey'], 
            'pdbx_ref_id', 
            'pdbx_residue_numbering', 
            ['PDB', 'chem_comp_atom_pdbx_stereo_config_fkey'], 
            'pdbx_stnd_atom_id', 
            ['PDB', 'chem_comp_atom_substruct_code_fkey'], 
        ],
    })

    # ----------------------------
    schema.tables["chem_comp_atom"].foreign_keys[(schema,"chem_comp_atom_comp_id_fkey")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })

# -- -----------------------------------------------------------------------------
def update_PDB_citation(model):
    schema = model.schemas["PDB"]
    table = schema.tables["citation"]
    
    # ----------------------------
    schema.tables["citation"].display.update(
        {'markdown_name' : 'Citations^*^', 'comment_display' : {'*': {'table_comment_display': 'inline'}}, }
    )
    
    # ----------------------------
    schema.tables["citation"].table_display.update({
        'row_name' : { 'row_markdown_pattern' : '{{{title}}}, {{{journal_abbrev}}}, {{{year}}}', },
    })
    
    # ----------------------------
    schema.tables["citation"].visible_columns.update({
        '*' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'citation_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'id', 
            'title', 
            'year', 
            'journal_abbrev', 
            'journal_volume', 
            'journal_issue', 
            'page_first', 
            'page_last', 
            'pdbx_database_id_DOI', 
            'pdbx_database_id_PubMed', 
            'journal_id_ASTM', 
            'journal_id_CSD', 
            'journal_id_ISSN', 
            'country', 
        ],
        'entry' :  [
            {
                'source' : [{'outbound': ['PDB', 'citation_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'id', 
            'title', 
            'year', 
            'journal_abbrev', 
            'journal_volume', 
            'journal_issue', 
            'page_first', 
            'page_last', 
            'pdbx_database_id_DOI', 
            'pdbx_database_id_PubMed', 
            'journal_id_ASTM', 
            'journal_id_CSD', 
            'journal_id_ISSN', 
            'country', 
        ],
    })

    # ----------------------------
    schema.tables["citation"].visible_foreign_keys.update({
        'filter' :  'detailed',
        'detailed' :  [
            ['PDB', 'citation_author_citation_id_fkey'], 
            ['PDB', 'software_citation_id_fkey'], 
            ['PDB', 'ihm_3dem_restraint_fitting_method_citation_id_fkey'], 
            ['PDB', 'ihm_epr_restraint_fitting_method_citation_id_fkey'], 
        ],
    })

    # ----------------------------
    schema.tables["citation"].columns["journal_abbrev"].display.update(
        {'name' : 'Abbreviated Journal Name (CASSI)', }
    )

    # ----------------------------
    schema.tables["citation"].columns["journal_id_ASTM"].display.update(
        {'name' : 'ASTM Journal Id', }
    )
    
    # ----------------------------
    schema.tables["citation"].columns["journal_id_CSD"].display.update(
        {'name' : 'CSD Journal Id', }
    )

    # ----------------------------
    schema.tables["citation"].columns["journal_id_ISSN"].display.update(
        {'name' : 'ISSN Journal Id', }
    )

    # ----------------------------
    schema.tables["citation"].columns["page_first"].display.update(
        {'name' : 'First Page', }
    )

    # ----------------------------
    schema.tables["citation"].columns["page_last"].display.update(
        {'name' : 'Last Page', }
    )

    # ----------------------------
    schema.tables["citation"].columns["pdbx_database_id_DOI"].display.update(
        {'name' : 'DOI', }
    )
    
    # ----------------------------
    schema.tables["citation"].columns["pdbx_database_id_DOI"].column_display.update({
        '*' : { 'markdown_pattern' : '{{#pdbx_database_id_DOI}}[{{_pdbx_database_id_DOI}}](https://doi.org/{{_pdbx_database_id_DOI}}){{/pdbx_database_id_DOI}}', },
    })

    # ----------------------------
    schema.tables["citation"].columns["pdbx_database_id_PubMed"].display.update(
        {'name' : 'Pubmed Id', }
    )

    # ----------------------------
    schema.tables["citation"].columns["pdbx_database_id_PubMed"].column_display.update({
        '*' : { 'markdown_pattern' : '{{_pdbx_database_id_PubMed}}', },
    })

    # ----------------------------
    schema.tables["citation"].columns["year"].column_display.update({
        '*' : { 'markdown_pattern' : '{{_year}}', },
    })

# -- -----------------------------------------------------------------------------
def update_PDB_citation_author(model):
    schema = model.schemas["PDB"]
    table = schema.tables["citation_author"]
    # ----------------------------
    schema.tables["citation_author"].display.update(
        {'markdown_name' : 'Authors in Citations^*^', 'comment_display' : {'*': {'table_comment_display': 'inline'}}, }
    )
    
    # ----------------------------
    schema.tables["citation_author"].visible_columns.update({
        '*' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'citation_author_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'citation_author_citation_id_fkey']}, 'RID'],
                'comment' : 'A reference to table citation.id.',
                'markdown_name' : 'Citation Id',
            },
            'ordinal', 
            'name', 
        ],
        'entry' :  [
            {
                'source' : [{'outbound': ['PDB', 'citation_author_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'citation_author_citation_id_fkey']}, 'RID'],
                'comment' : 'A reference to table citation.id.',
                'markdown_name' : 'Citation Id',
            },
            'ordinal', 
            'name', 
        ],
    })

    # ----------------------------
    schema.tables["citation_author"].columns["citation_id"].display.update(
        {'name' : 'Citation Id', }
    )

    # ----------------------------
    schema.tables["citation_author"].foreign_keys[(schema,"citation_author_citation_id_fkey")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })

# -- -----------------------------------------------------------------------------
def update_PDB_entity(model):
    schema = model.schemas["PDB"]
    table = schema.tables["entity"]
    # ----------------------------
    schema.tables["entity"].display.update(
        {'markdown_name' : 'Molecular Entities^*^', 'comment_display' : {'*': {'table_comment_display': 'inline'}}, }
    )

    # ----------------------------
    schema.tables["entity"].table_display.update({
        'row_name' : { 'row_markdown_pattern' : '{{{id}}}', },
    })

    # ----------------------------
    schema.tables["entity"].visible_columns.update({
        '*' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'entity_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'id', 
            ['PDB', 'entity_type_fkey'], 
            ['PDB', 'entity_src_method_fkey'], 
            'pdbx_description', 
            'formula_weight', 
            'pdbx_number_of_molecules', 
            'details', 
        ],
        'entry' :  [
            {
                'source' : [{'outbound': ['PDB', 'entity_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'id', 
            ['PDB', 'entity_type_fkey'], 
            ['PDB', 'entity_src_method_fkey'], 
            'pdbx_description', 
            'formula_weight', 
            'pdbx_number_of_molecules', 
            'details', 
        ],
    })

    # ----------------------------
    schema.tables["entity"].visible_foreign_keys.update({
        'filter' :  'detailed',
        'detailed' :  [
            ['PDB', 'entity_name_com_entity_id_fkey'], 
            ['PDB', 'entity_name_sys_entity_id_fkey'], 
            ['PDB', 'entity_src_gen_entity_id_fkey'], 
            ['PDB', 'struct_ref_entity_combo1_fkey'], 
            ['PDB', 'entity_poly_entity_id_fkey'], 
            ['PDB', 'pdbx_entity_nonpoly_entity_id_fkey'], 
            ['PDB', 'struct_asym_entity_id_fkey'], 
            ['PDB', 'ihm_model_representation_details_entity_id_fkey'], 
            ['PDB', 'ihm_struct_assembly_details_entity_id_fkey'], 
            ['PDB', 'ihm_starting_model_details_entity_id_fkey'], 
            ['PDB', 'ihm_ligand_probe_entity_id_fkey'], 
            ['PDB', 'ihm_non_poly_feature_entity_id_fkey'], 
            ['PDB', 'ihm_interface_residue_feature_binding_partner_entity_id_fkey'], 
            ['PDB', 'ihm_localization_density_files_entity_id_fkey'], 
            ['PDB', 'pdbx_entity_poly_na_type_entity_id_fkey'], 
        ],
    })

    # ----------------------------
    schema.tables["entity"].columns["pdbx_description"].display.update(
        {'name' : 'Description', }
    )
    
    # ----------------------------
    schema.tables["entity"].columns["pdbx_number_of_molecules"].display.update(
        {'name' : 'Number of Molecules', }
    )

    # ----------------------------
    schema.tables["entity"].columns["src_method"].display.update(
        {'name' : 'Method for Sample Production', }
    )

# -- -----------------------------------------------------------------------------
def update_PDB_entity_name_com(model):
    schema = model.schemas["PDB"]
    table = schema.tables["entity_name_com"]
    # ----------------------------
    schema.tables["entity_name_com"].display.update(
        {'name' : 'Common Names of Entities', 'comment_display' : {'*': {'table_comment_display': 'inline'}}, }
    )

    # ----------------------------
    schema.tables["entity_name_com"].visible_columns.update({
        '*' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'entity_name_com_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'entity_name_com_entity_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entity.id.',
                'markdown_name' : 'Entity Id',
            },
            'name', 
        ],
        'entry' :  [
            {
                'source' : [{'outbound': ['PDB', 'entity_name_com_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'entity_name_com_entity_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entity.id.',
                'markdown_name' : 'Entity Id',
            },
            'name', 
        ],
    })

    # ----------------------------
    schema.tables["entity_name_com"].columns["entity_id"].display.update(
        {'name' : 'Entity Id', }
    )

    # ----------------------------
    schema.tables["entity_name_com"].foreign_keys[(schema,"entity_name_com_entity_id_fkey")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })

# -- -----------------------------------------------------------------------------
def update_PDB_entity_name_sys(model):
    schema = model.schemas["PDB"]
    table = schema.tables["entity_name_sys"]
    # ----------------------------
    schema.tables["entity_name_sys"].display.update(
        {'name' : 'Systematic Names of Entities', 'comment_display' : {'*': {'table_comment_display': 'inline'}}, }
    )

    # ----------------------------
    schema.tables["entity_name_sys"].visible_columns.update({
        '*' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'entity_name_sys_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'entity_name_sys_entity_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entity.id.',
                'markdown_name' : 'Entity Id',
            },
            'name', 
        ],
        'entry' :  [
            {
                'source' : [{'outbound': ['PDB', 'entity_name_sys_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'entity_name_sys_entity_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entity.id.',
                'markdown_name' : 'Entity Id',
            },
            'name', 
        ],
    })

    # ----------------------------
    schema.tables["entity_name_sys"].columns["entity_id"].display.update(
        {'name' : 'Entity Id', }
    )

    # ----------------------------
    schema.tables["entity_name_sys"].foreign_keys[(schema,"entity_name_sys_entity_id_fkey")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })

# -- -----------------------------------------------------------------------------
def update_PDB_entity_poly(model):
    schema = model.schemas["PDB"]
    table = schema.tables["entity_poly"]
    # ----------------------------
    schema.tables["entity_poly"].display.update({
        'markdown_name' : 'Polymeric Entities^*^',
        'comment_display' : {'*': {'table_comment_display': 'inline'}},
    })

    # ----------------------------
    schema.tables["entity_poly"].table_display.update({
        'row_name' : { 'row_markdown_pattern' : '{{{entity_id}}}', },
    })

    # ----------------------------
    schema.tables["entity_poly"].visible_columns.update({
        '*' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'entity_poly_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'entity_poly_entity_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entity.id.',
                'markdown_name' : 'Entity Id',
            },
            ['PDB', 'entity_poly_type_fkey'], 
            ['PDB', 'entity_poly_nstd_monomer_fkey'], 
            ['PDB', 'entity_poly_nstd_linkage_fkey'], 
            ['PDB', 'entity_poly_nstd_chirality_fkey'], 
            'pdbx_strand_id', 
            ['PDB', 'entity_poly_pdbx_sequence_evidence_code_fkey'], 
            'pdbx_seq_one_letter_code', 
            'pdbx_seq_one_letter_code_can', 
        ],
        'entry' :  [
            {
                'source' : [{'outbound': ['PDB', 'entity_poly_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'entity_poly_entity_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entity.id.',
                'markdown_name' : 'Entity Id',
            },
            ['PDB', 'entity_poly_type_fkey'], 
            ['PDB', 'entity_poly_nstd_monomer_fkey'], 
            ['PDB', 'entity_poly_nstd_linkage_fkey'], 
            ['PDB', 'entity_poly_nstd_chirality_fkey'], 
            'pdbx_strand_id', 
            ['PDB', 'entity_poly_pdbx_sequence_evidence_code_fkey'], 
            'pdbx_seq_one_letter_code', 
            'pdbx_seq_one_letter_code_can', 
        ],
    })

    # ----------------------------
    schema.tables["entity_poly"].visible_foreign_keys.update({
        'filter' :  'detailed',
        'detailed' :  [
            ['PDB', 'entity_poly_seq_entity_id_fkey'], 
        ],
    })

    # ----------------------------
    schema.tables["entity_poly"].columns["entity_id"].display.update(
        {'name' : 'Entity Id', }
    )

    # ----------------------------
    schema.tables["entity_poly"].columns["nstd_chirality"].display.update(
        {'name' : 'Non-standard Chirality', }
    )

    # ----------------------------
    schema.tables["entity_poly"].columns["nstd_linkage"].display.update(
        {'name' : 'Non-standard Linkage', }
    )

    # ----------------------------
    schema.tables["entity_poly"].columns["nstd_monomer"].display.update(
        {'name' : 'Non-standard Monomer', }
    )

    # ----------------------------
    schema.tables["entity_poly"].columns["pdbx_seq_one_letter_code"].display.update(
        {'name' : 'Polymer Sequence One Letter Code', }
    )

    # ----------------------------
    schema.tables["entity_poly"].columns["pdbx_seq_one_letter_code_can"].display.update(
        {'name' : 'Polymer Canonical Sequence One Letter Code', }
    )

    # ----------------------------
    schema.tables["entity_poly"].columns["pdbx_sequence_evidence_code"].display.update(
        {'name' : 'Sequence Evidence Code', }
    )

    # ----------------------------
    schema.tables["entity_poly"].columns["pdbx_strand_id"].display.update(
        {'name' : 'Chain Id', }
    )

    # ----------------------------
    schema.tables["entity_poly"].foreign_keys[(schema,"entity_poly_entity_id_fkey")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })

# -- -----------------------------------------------------------------------------
def update_PDB_entity_poly_seq(model):
    schema = model.schemas["PDB"]
    table = schema.tables["entity_poly_seq"]
    # ----------------------------
    schema.tables["entity_poly_seq"].display.update(
        {'markdown_name' : 'Sequences of Polymeric Entities^*^', 'comment_display' : {'*': {'table_comment_display': 'inline'}}, }
    )

    # ----------------------------
    schema.tables["entity_poly_seq"].visible_columns.update({
        '*' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'entity_poly_seq_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'entity_poly_seq_entity_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entity.id.',
                'markdown_name' : 'Entity Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'entity_poly_seq_mon_id_fkey']}, 'RID'],
                'comment' : 'A reference to table chem_comp.id.',
                'markdown_name' : 'Monomer Id',
            },
            'num', 
            ['PDB', 'entity_poly_seq_hetero_fkey'], 
        ],
        'entry' :  [
            {
                'source' : [{'outbound': ['PDB', 'entity_poly_seq_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'entity_poly_seq_entity_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entity.id.',
                'markdown_name' : 'Entity Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'entity_poly_seq_mon_id_fkey']}, 'RID'],
                'comment' : 'A reference to table chem_comp.id.',
                'markdown_name' : 'Monomer Id',
            },
            'num', 
            ['PDB', 'entity_poly_seq_hetero_fkey'], 
        ],
    })

    # ----------------------------
    schema.tables["entity_poly_seq"].visible_foreign_keys.update({
        'filter' :  'detailed',
        'detailed' :  [
            ['PDB', 'ihm_entity_poly_segment_mm_poly_res_label_begin_fkey'], 
            ['PDB', 'ihm_entity_poly_segment_mm_poly_res_label_end_fkey'], 
            ['PDB', 'ihm_starting_model_seq_dif_mm_poly_res_label_fkey'], 
            ['PDB', 'ihm_poly_probe_position_mm_poly_res_label_fkey'], 
            ['PDB', 'ihm_cross_link_list_mm_poly_res_label_1_fkey'], 
            ['PDB', 'ihm_cross_link_list_mm_poly_res_label_2_fkey'], 
            ['PDB', 'ihm_cross_link_restraint_mm_poly_res_label_1_fkey'], 
            ['PDB', 'ihm_cross_link_restraint_mm_poly_res_label_2_fkey'], 
            ['PDB', 'ihm_hydroxyl_radical_fp_restraint_mm_poly_res_label_fkey'], 
            ['PDB', 'ihm_predicted_contact_restraint_mm_poly_res_label_1_fkey'], 
            ['PDB', 'ihm_predicted_contact_restraint_mm_poly_res_label_2_fkey'], 
            ['PDB', 'ihm_poly_atom_feature_mm_poly_res_label_fkey'], 
            ['PDB', 'ihm_poly_residue_feature_mm_poly_res_label_begin_fkey'], 
            ['PDB', 'ihm_poly_residue_feature_mm_poly_res_label_end_fkey'], 
            ['PDB', 'ihm_residues_not_modeled_mm_poly_res_label_begin_fkey'], 
            ['PDB', 'ihm_residues_not_modeled_mm_poly_res_label_end_fkey'], 
        ],
    })

    # ----------------------------
    schema.tables["entity_poly_seq"].columns["entity_id"].display.update(
        {'name' : 'Entity Id', }
    )

    # ----------------------------
    schema.tables["entity_poly_seq"].columns["hetero"].display.update(
        {'name' : 'Heterogeneity Flag', }
    )

    # ----------------------------
    schema.tables["entity_poly_seq"].columns["mon_id"].display.update(
        {'name' : 'Chemical Component Id', }
    )

    # ----------------------------
    schema.tables["entity_poly_seq"].columns["num"].display.update(
        {'name' : 'Sequence Id of Monomer', }
    )

    # ----------------------------
    schema.tables["entity_poly_seq"].foreign_keys[(schema,"entity_poly_seq_entity_id_fkey")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })

    # ----------------------------
    schema.tables["entity_poly_seq"].foreign_keys[(schema,"entity_poly_seq_mon_id_fkey")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })

# -- -----------------------------------------------------------------------------
def update_PDB_entity_src_gen(model):
    schema = model.schemas["PDB"]
    table = schema.tables["entity_src_gen"]
    # ----------------------------
    schema.tables["entity_src_gen"].display.update(
        {'name' : 'Source of Genetically Manipulated Entities', 'comment_display' : {'*': {'table_comment_display': 'inline'}}, }
    )

    # ----------------------------
    schema.tables["entity_src_gen"].visible_columns.update({
        '*' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'entity_src_gen_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'entity_src_gen_entity_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entity.id.',
                'markdown_name' : 'Entity Id',
            },
            'pdbx_src_id', 
            ['PDB', 'entity_src_gen_pdbx_alt_source_flag_fkey'], 
            'gene_src_common_name', 
            'gene_src_genus', 
            'pdbx_gene_src_scientific_name', 
        ],
        'entry' :  [
            {
                'source' : [{'outbound': ['PDB', 'entity_src_gen_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'entity_src_gen_entity_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entity.id.',
                'markdown_name' : 'Entity Id',
            },
            'pdbx_src_id', 
            ['PDB', 'entity_src_gen_pdbx_alt_source_flag_fkey'], 
            'gene_src_common_name', 
            'gene_src_genus', 
            'pdbx_gene_src_scientific_name', 
        ],
    })

    # ----------------------------
    schema.tables["entity_src_gen"].columns["entity_id"].display.update(
        {'name' : 'Entity Id', }
    )

    # ----------------------------
    schema.tables["entity_src_gen"].columns["gene_src_common_name"].display.update(
        {'name' : 'Gene Source Common Name', }
    )

    # ----------------------------
    schema.tables["entity_src_gen"].columns["gene_src_genus"].display.update(
        {'name' : 'Gene Source Genus', }
    )

    # ----------------------------
    schema.tables["entity_src_gen"].columns["pdbx_alt_source_flag"].display.update(
        {'name' : 'Alternate Source Flag', }
    )

    # ----------------------------
    schema.tables["entity_src_gen"].columns["pdbx_gene_src_scientific_name"].display.update(
        {'name' : 'Gene Source Scientific Name', }
    )

    # ----------------------------
    schema.tables["entity_src_gen"].columns["pdbx_src_id"].display.update(
        {'name' : 'Source Id', }
    )

    # ----------------------------
    schema.tables["entity_src_gen"].foreign_keys[(schema,"entity_src_gen_entity_id_fkey")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })

# -- -----------------------------------------------------------------------------
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
def update_PDB_pdbx_entity_nonpoly(model):
    schema = model.schemas["PDB"]
    table = schema.tables["pdbx_entity_nonpoly"]
    # ----------------------------
    schema.tables["pdbx_entity_nonpoly"].display.update(
        {'name' : 'Non-polymeric Entities', 'comment_display' : {'*': {'table_comment_display': 'inline'}}, }
    )

    # ----------------------------
    schema.tables["pdbx_entity_nonpoly"].visible_columns.update({
        '*' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'pdbx_entity_nonpoly_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'pdbx_entity_nonpoly_entity_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entity.id.',
                'markdown_name' : 'Entity Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'pdbx_entity_nonpoly_comp_id_fkey']}, 'RID'],
                'comment' : 'A reference to table chem_comp.id.',
                'markdown_name' : 'Component Id',
            },
            'name', 
        ],
        'entry' :  [
            {
                'source' : [{'outbound': ['PDB', 'pdbx_entity_nonpoly_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'pdbx_entity_nonpoly_entity_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entity.id.',
                'markdown_name' : 'Entity Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'pdbx_entity_nonpoly_comp_id_fkey']}, 'RID'],
                'comment' : 'A reference to table chem_comp.id.',
                'markdown_name' : 'Component Id',
            },
            'name', 
        ],
    })

    # ----------------------------
    schema.tables["pdbx_entity_nonpoly"].columns["comp_id"].display.update(
        {'name' : 'Chemical Component Id', }
    )

    # ----------------------------
    schema.tables["pdbx_entity_nonpoly"].columns["entity_id"].display.update(
        {'name' : 'Entity Id', }
    )

    # ----------------------------
    schema.tables["pdbx_entity_nonpoly"].foreign_keys[(schema,"pdbx_entity_nonpoly_comp_id_fkey")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })

    # ----------------------------
    schema.tables["pdbx_entity_nonpoly"].foreign_keys[(schema,"pdbx_entity_nonpoly_comp_id_fk")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })

    # ----------------------------
    schema.tables["pdbx_entity_nonpoly"].foreign_keys[(schema,"pdbx_entity_nonpoly_entity_id_fkey")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })

# -- -----------------------------------------------------------------------------
def update_PDB_pdbx_entity_poly_na_type(model):
    schema = model.schemas["PDB"]
    table = schema.tables["pdbx_entity_poly_na_type"]
    # ----------------------------
    schema.tables["pdbx_entity_poly_na_type"].display.update(
        {'name' : 'Types of Polymeric Nucleic Acid Entities', 'comment_display' : {'*': {'table_comment_display': 'inline'}}, }
    )

    # ----------------------------
    schema.tables["pdbx_entity_poly_na_type"].visible_columns.update({
        '*' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'pdbx_entity_poly_na_type_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'pdbx_entity_poly_na_type_entity_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entity.id.',
                'markdown_name' : 'Entity Id',
            },
            ['PDB', 'pdbx_entity_poly_na_type_type_fkey'], 
        ],
        'entry' :  [
            {
                'source' : [{'outbound': ['PDB', 'pdbx_entity_poly_na_type_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'pdbx_entity_poly_na_type_entity_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entity.id.',
                'markdown_name' : 'Entity Id',
            },
            ['PDB', 'pdbx_entity_poly_na_type_type_fkey'], 
        ],
        'detailed' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'pdbx_entity_poly_na_type_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            {
                'source' : [{'outbound': ['PDB', 'pdbx_entity_poly_na_type_entity_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entity.id.',
                'markdown_name' : 'Entity Id',
            },
            ['PDB', 'pdbx_entity_poly_na_type_type_fkey'], 
            ['PDB', 'pdbx_entity_poly_na_type_RCB_fkey'], 
            ['PDB', 'pdbx_entity_poly_na_type_RMB_fkey'], 
            'RCT', 
            'RMT', 
            ['PDB', 'pdbx_entity_poly_na_type_Owner_fkey'], 
        ],
    })

    # ----------------------------
    schema.tables["pdbx_entity_poly_na_type"].foreign_keys[(schema,"pdbx_entity_poly_na_type_entity_id_fkey")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })

# -- -----------------------------------------------------------------------------
def update_PDB_pdbx_entry_details(model):
    schema = model.schemas["PDB"]
    table = schema.tables["pdbx_entry_details"]
    # ----------------------------
    schema.tables["pdbx_entry_details"].display.update(
        {'name' : 'Additional Details about the Entry', 'comment_display' : {'*': {'table_comment_display': 'inline'}}, }
    )

    # ----------------------------
    schema.tables["pdbx_entry_details"].visible_columns.update({
        '*' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'pdbx_entry_details_entry_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Entry Id',
            },
            'sequence_details', 
        ],
        'entry' :  [
            {
                'source' : [{'outbound': ['PDB', 'pdbx_entry_details_entry_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Entry Id',
            },
            'sequence_details', 
        ],
        'detailed' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'pdbx_entry_details_entry_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Entry Id',
            },
            'sequence_details', 
            ['PDB', 'pdbx_entry_details_RCB_fkey'], 
            ['PDB', 'pdbx_entry_details_RMB_fkey'], 
            'RCT', 
            'RMT', 
            ['PDB', 'pdbx_entry_details_Owner_fkey'], 
        ],
    })

# -- -----------------------------------------------------------------------------
def update_PDB_pdbx_inhibitor_info(model):
    schema = model.schemas["PDB"]
    table = schema.tables["pdbx_inhibitor_info"]
    # ----------------------------
    schema.tables["pdbx_inhibitor_info"].display.update(
        {'name' : 'Details of Inhibitors in the Entry', 'comment_display' : {'*': {'table_comment_display': 'inline'}}, }
    )

    # ----------------------------
    schema.tables["pdbx_inhibitor_info"].visible_columns.update({
        '*' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'pdbx_inhibitor_info_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'id', 
            'name', 
            'num_per_asym_unit', 
        ],
        'entry' :  [
            {
                'source' : [{'outbound': ['PDB', 'pdbx_inhibitor_info_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'id', 
            'name', 
            'num_per_asym_unit', 
        ],
        'detailed' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'pdbx_inhibitor_info_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'id', 
            'name', 
            'num_per_asym_unit', 
            ['PDB', 'pdbx_inhibitor_info_RCB_fkey'], 
            ['PDB', 'pdbx_inhibitor_info_RMB_fkey'], 
            'RCT', 
            'RMT', 
            ['PDB', 'pdbx_inhibitor_info_Owner_fkey'], 
        ],
    })

# -- -----------------------------------------------------------------------------
def update_PDB_pdbx_ion_info(model):
    schema = model.schemas["PDB"]
    table = schema.tables["pdbx_ion_info"]
    # ----------------------------
    schema.tables["pdbx_ion_info"].display.update(
        {'name' : 'Details of Ions in the Entry', 'comment_display' : {'*': {'table_comment_display': 'inline'}}, }
    )

    # ----------------------------
    schema.tables["pdbx_ion_info"].visible_columns.update({
        '*' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'pdbx_ion_info_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'id', 
            'name', 
            'numb_per_asym_unit', 
            ['PDB', 'pdbx_ion_info_RCB_fkey'], 
            ['PDB', 'pdbx_ion_info_RMB_fkey'], 
            'RCT', 
            'RMT', 
            ['PDB', 'pdbx_ion_info_Owner_fkey'], 
        ],
        'entry' :  [
            {
                'source' : [{'outbound': ['PDB', 'pdbx_ion_info_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'id', 
            'name', 
            'numb_per_asym_unit', 
        ],
    })

# -- -----------------------------------------------------------------------------
def update_PDB_pdbx_protein_info(model):
    schema = model.schemas["PDB"]
    table = schema.tables["pdbx_protein_info"]
    # ----------------------------
    schema.tables["pdbx_protein_info"].display.update(
        {'name' : 'Details of Proteins in the Entry', 'comment_display' : {'*': {'table_comment_display': 'inline'}}, }
    )
    
    # ----------------------------
    schema.tables["pdbx_protein_info"].visible_columns.update({
        '*' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'pdbx_protein_info_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'id', 
            'name', 
            'num_per_asym_unit', 
        ],
        'entry' :  [
            {
                'source' : [{'outbound': ['PDB', 'pdbx_protein_info_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'id', 
            'name', 
            'num_per_asym_unit', 
        ],
        'detailed' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'pdbx_protein_info_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'id', 
            'name', 
            'num_per_asym_unit', 
            ['PDB', 'pdbx_protein_info_RCB_fkey'], 
            ['PDB', 'pdbx_protein_info_RMB_fkey'], 
            'RCT', 
            'RMT', 
            ['PDB', 'pdbx_protein_info_Owner_fkey'], 
        ],
    })

# -- -----------------------------------------------------------------------------
def update_PDB_software(model):
    schema = model.schemas["PDB"]
    table = schema.tables["software"]
    # ----------------------------
    schema.tables["software"].display.update({
        'markdown_name' : 'Software^*^',
        'comment_display' : {'*': {'table_comment_display': 'inline'}},
    })

    # ----------------------------
    schema.tables["software"].table_display.update({
        'row_name' : { 'row_markdown_pattern' : '{{{name}}} {{{version}}}', },
    })

    # ----------------------------
    schema.tables["software"].visible_columns.update({
        '*' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'software_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'pdbx_ordinal', 
            'name', 
            'classification', 
            ['PDB', 'software_type_fkey'], 
            'version', 
            'location', 
            {
                'source' : [{'outbound': ['PDB', 'software_citation_id_fkey']}, 'RID'],
                'comment' : 'A reference to table citation.id.',
                'markdown_name' : 'Citation Id',
            },
            'description', 
        ],
        'entry' :  [
            {
                'source' : [{'outbound': ['PDB', 'software_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'pdbx_ordinal', 
            'name', 
            'classification', 
            ['PDB', 'software_type_fkey'], 
            'version', 
            'location', 
            {
                'source' : [{'outbound': ['PDB', 'software_citation_id_fkey']}, 'RID'],
                'comment' : 'A reference to table citation.id.',
                'markdown_name' : 'Citation Id',
            },
            'description', 
        ],
    })

    # ----------------------------
    schema.tables["software"].visible_foreign_keys.update({
        'filter' :  'detailed',
        'detailed' :  [
            ['PDB', 'ihm_modeling_protocol_details_software_id_fkey'], 
            ['PDB', 'ihm_modeling_post_process_software_id_fkey'], 
            ['PDB', 'ihm_starting_computational_models_software_id_fkey'], 
            ['PDB', 'ihm_epr_restraint_fitting_software_id_fkey'], 
            ['PDB', 'ihm_hydroxyl_radical_fp_restraint_software_id_fkey'], 
            ['PDB', 'ihm_predicted_contact_restraint_software_id_fkey'], 
        ],
    })

    # ----------------------------
    schema.tables["software"].columns["citation_id"].display.update(
        {'name' : 'Citation Id', }
    )

    # ----------------------------
    schema.tables["software"].columns["pdbx_ordinal"].display.update(
        {'name' : 'Ordinal', }
    )

    # ----------------------------
    schema.tables["software"].foreign_keys[(schema,"software_citation_id_fkey")].foreign_key.update({
        'template_engine' :  'handlebars',
        'domain_filter_pattern' :  '{{#if _structure_id}}structure_id={{{_structure_id}}}{{/if}}',
    })

# -- -----------------------------------------------------------------------------
def update_PDB_struct(model):
    schema = model.schemas["PDB"]
    table = schema.tables["struct"]
    # ----------------------------
    schema.tables["struct"].display.update(
        {'markdown_name' : 'Description of the Structure^*^', 'comment_display' : {'*': {'table_comment_display': 'inline'}}, }
    )

    # ----------------------------
    schema.tables["struct"].visible_columns.update({
        '*' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'struct_entry_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Entry Id',
            },
            'title', 
            ['PDB', 'struct_pdbx_structure_determination_methodology_fkey'], 
            'pdbx_descriptor', 
            'pdbx_details', 
            'pdbx_model_details', 
            'pdbx_model_type_details', 
            ['PDB', 'struct_pdbx_CASP_flag_fkey'], 
        ],
        'entry' :  [
            {
                'source' : [{'outbound': ['PDB', 'struct_entry_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Entry Id',
            },
            'title', 
            ['PDB', 'struct_pdbx_structure_determination_methodology_fkey'], 
            'pdbx_descriptor', 
            'pdbx_details', 
            'pdbx_model_details', 
            'pdbx_model_type_details', 
            ['PDB', 'struct_pdbx_CASP_flag_fkey'], 
        ],
        'detailed' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'struct_entry_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Entry Id',
            },
            'title', 
            ['PDB', 'struct_pdbx_structure_determination_methodology_fkey'], 
            'pdbx_descriptor', 
            'pdbx_details', 
            'pdbx_model_details', 
            'pdbx_model_type_details', 
            ['PDB', 'struct_pdbx_CASP_flag_fkey'], 
            ['PDB', 'struct_RCB_fkey'], 
            ['PDB', 'struct_RMB_fkey'], 
            'RCT', 
            'RMT', 
            ['PDB', 'struct_Owner_fkey'], 
        ],
    })

    # ----------------------------
    schema.tables["struct"].columns["pdbx_CASP_flag"].display.update(
        {'name' : 'CASP Flag', }
    )

    # ----------------------------
    schema.tables["struct"].columns["pdbx_descriptor"].display.update(
        {'name' : 'Descriptor', }
    )

    # ----------------------------
    schema.tables["struct"].columns["pdbx_details"].display.update(
        {'name' : 'Details', }
    )

    # ----------------------------
    schema.tables["struct"].columns["pdbx_model_details"].display.update(
        {'name' : 'Model Details', }
    )

    # ----------------------------
    schema.tables["struct"].columns["pdbx_model_type_details"].display.update(
        {'name' : 'Model Type Details', }
    )

# -- -----------------------------------------------------------------------------
def update_PDB_struct_asym(model):
    schema = model.schemas["PDB"]
    table = schema.tables["struct_asym"]
    # ----------------------------
    schema.tables["struct_asym"].display.update(
        {'markdown_name' : 'Instances of Molecular Entities^*^', 'comment_display' : {'*': {'table_comment_display': 'inline'}}, }
    )

    # ----------------------------
    schema.tables["struct_asym"].table_display.update({
        'row_name' : { 'row_markdown_pattern' : '{{{id}}}', },
    })

    # ----------------------------
    schema.tables["struct_asym"].visible_columns.update({
        '*' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'struct_asym_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'id', 
            {
                'source' : [{'outbound': ['PDB', 'struct_asym_entity_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entity.id.',
                'markdown_name' : 'Entity Id',
            },
            'pdbx_PDB_id', 
            'pdbx_alt_id', 
            ['PDB', 'struct_asym_pdbx_blank_PDB_chainid_flag_fkey'], 
            'pdbx_modified', 
            'pdbx_order', 
            ['PDB', 'struct_asym_pdbx_type_fkey'], 
            'details', 
        ],
        'entry' :  [
            {
                'source' : [{'outbound': ['PDB', 'struct_asym_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'id', 
            {
                'source' : [{'outbound': ['PDB', 'struct_asym_entity_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entity.id.',
                'markdown_name' : 'Entity Id',
            },
            'pdbx_PDB_id', 
            'pdbx_alt_id', 
            ['PDB', 'struct_asym_pdbx_blank_PDB_chainid_flag_fkey'], 
            'pdbx_modified', 
            'pdbx_order', 
            ['PDB', 'struct_asym_pdbx_type_fkey'], 
            'details', 
        ],
    })

    # ----------------------------
    schema.tables["struct_asym"].visible_foreign_keys.update({
        'filter' :  'detailed',
        'detailed' :  [
            ['PDB', 'ihm_model_representation_details_entity_asym_id_fkey'], 
            ['PDB', 'ihm_struct_assembly_details_asym_id_fkey'], 
            ['PDB', 'ihm_starting_model_details_asym_id_fkey'], 
            ['PDB', 'ihm_starting_model_seq_dif_asym_id_fkey'], 
            ['PDB', 'ihm_cross_link_restraint_asym_id_1_fkey'], 
            ['PDB', 'ihm_cross_link_restraint_asym_id_2_fkey'], 
            ['PDB', 'ihm_hydroxyl_radical_fp_restraint_asym_id_fkey'], 
            ['PDB', 'ihm_predicted_contact_restraint_asym_id_1_fkey'], 
            ['PDB', 'ihm_predicted_contact_restraint_asym_id_2_fkey'], 
            ['PDB', 'ihm_poly_atom_feature_asym_id_fkey'], 
            ['PDB', 'ihm_poly_residue_feature_asym_id_fkey'], 
            ['PDB', 'ihm_non_poly_feature_asym_id_fkey'], 
            ['PDB', 'ihm_interface_residue_feature_binding_partner_asym_id_fkey'], 
            ['PDB', 'ihm_residues_not_modeled_asym_id_fkey'], 
            ['PDB', 'ihm_localization_density_files_asym_id_fkey'], 
        ],
    })

    # ----------------------------
    schema.tables["struct_asym"].columns["entity_id"].display.update(
        {'name' : 'Entity Id', }
    )

    # ----------------------------
    schema.tables["struct_asym"].columns["pdbx_PDB_id"].display.update(
        {'name' : 'PDB Strand Id', }
    )

    # ----------------------------
    schema.tables["struct_asym"].columns["pdbx_alt_id"].display.update(
        {'name' : 'Alternate PDB Strand Id', }
    )

    # ----------------------------
    schema.tables["struct_asym"].columns["pdbx_blank_PDB_chainid_flag"].display.update(
        {'name' : 'Blank PDB Chainid Flag', }
    )

    # ----------------------------
    schema.tables["struct_asym"].columns["pdbx_modified"].display.update(
        {'name' : 'Modified Structural Elements', }
    )

    # ----------------------------
    schema.tables["struct_asym"].columns["pdbx_order"].display.update(
        {'name' : 'Order of Structural Elements', }
    )

    # ----------------------------
    schema.tables["struct_asym"].columns["pdbx_type"].display.update(
        {'name' : 'Type of Structural Elements', }
    )

    # ----------------------------
    schema.tables["struct_asym"].foreign_keys[(schema,"struct_asym_entity_id_fkey")].foreign_key.update({
        'domain_filter_pattern' :  'structure_id={{structure_id}}',
    })

# -- -----------------------------------------------------------------------------
def update_PDB_struct_ref(model):
    schema = model.schemas["PDB"]
    table = schema.tables["struct_ref"]
    # ----------------------------
    schema.tables["struct_ref"].display.update(
        {'markdown_name' : 'Reference sequence information^*^', 'comment_display' : {'*': {'table_comment_display': 'inline'}}, }
    )

    # ----------------------------
    schema.tables["struct_ref"].visible_columns.update({
        '*' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'struct_ref_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'id', 
            {
                'source' : [{'outbound': ['PDB', 'struct_ref_entity_combo1_fkey']}, 'RID'],
                'comment' : 'A reference to table entity.id.',
                'markdown_name' : 'Entity Id',
            },
            ['PDB', 'struct_ref_db_name_fkey'], 
            'db_code', 
            'pdbx_db_accession', 
            'pdbx_db_isoform', 
            'pdbx_align_begin', 
            'pdbx_align_end', 
            'pdbx_seq_one_letter_code', 
            'details', 
        ],
        'entry' :  [
            {
                'source' : [{'outbound': ['PDB', 'struct_ref_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'id', 
            {
                'source' : [{'outbound': ['PDB', 'struct_ref_entity_combo1_fkey']}, 'RID'],
                'comment' : 'A reference to table entity.id.',
                'markdown_name' : 'Entity Id',
            },
            ['PDB', 'struct_ref_db_name_fkey'], 
            'db_code', 
            'pdbx_db_accession', 
            'pdbx_db_isoform', 
            'pdbx_align_begin', 
            'pdbx_align_end', 
            'pdbx_seq_one_letter_code', 
            'details', 
        ],
        'detailed' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'struct_ref_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'id', 
            {
                'source' : [{'outbound': ['PDB', 'struct_ref_entity_combo1_fkey']}, 'RID'],
                'comment' : 'A reference to table entity.id.',
                'markdown_name' : 'Entity Id',
            },
            ['PDB', 'struct_ref_db_name_fkey'], 
            'db_code', 
            'pdbx_db_accession', 
            'pdbx_db_isoform', 
            'pdbx_align_begin', 
            'pdbx_align_end', 
            'pdbx_seq_one_letter_code', 
            'details', 
            ['PDB', 'struct_ref_RCB_fkey'], 
            ['PDB', 'struct_ref_RMB_fkey'], 
            'RCT', 
            'RMT', 
            ['PDB', 'struct_ref_Owner_fkey'], 
        ],
    })

    # ----------------------------
    schema.tables["struct_ref"].visible_foreign_keys.update({
        'filter' :  'detailed',
        'detailed' :  [
            ['PDB', 'struct_ref_seq_struct_ref_combo1_fkey'], 
        ],
    })

    # ----------------------------
    schema.tables["struct_ref"].columns["db_name"].display.update(
        {'name' : 'Database Name', }
    )

    # ----------------------------
    schema.tables["struct_ref"].columns["db_code"].display.update(
        {'name' : 'Database Code', }
    )

    # ----------------------------
    schema.tables["struct_ref"].columns["pdbx_db_accession"].display.update(
        {'name' : 'Database Accession Number', }
    )

    # ----------------------------
    schema.tables["struct_ref"].columns["pdbx_db_isoform"].display.update(
        {'name' : 'Database Code Sequence Isoform', }
    )

    # ----------------------------
    schema.tables["struct_ref"].columns["pdbx_align_begin"].display.update(
        {'name' : 'Database Sequence Align Begin', }
    )

    # ----------------------------
    schema.tables["struct_ref"].columns["pdbx_align_end"].display.update(
        {'name' : 'Database Sequence Align End', }
    )

    # ----------------------------
    schema.tables["struct_ref"].columns["pdbx_seq_one_letter_code"].display.update(
        {'name' : 'Sequence One Letter Code', }
    )

    # ----------------------------
    schema.tables["struct_ref"].foreign_keys[(schema,"struct_ref_entity_combo1_fkey")].foreign_key.update({
        'template_engine' :  'handlebars',
        'domain_filter_pattern' :  '{{#if _structure_id}}structure_id={{{_structure_id}}}{{/if}}',
    })

# -- -----------------------------------------------------------------------------
def update_PDB_struct_ref_seq(model):
    schema = model.schemas["PDB"]
    table = schema.tables["struct_ref_seq"]
    # ----------------------------
    schema.tables["struct_ref_seq"].display.update(
        {'markdown_name' : 'Alignment information with the reference sequence^*^', 'comment_display' : {'*': {'table_comment_display': 'inline'}}, }
    )

    # ----------------------------
    schema.tables["struct_ref_seq"].visible_columns.update({
        '*' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'struct_ref_seq_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'align_id', 
            {
                'source' : [{'outbound': ['PDB', 'struct_ref_seq_struct_ref_combo1_fkey']}, 'RID'],
                'comment' : 'A reference to table struct_ref.id.',
                'markdown_name' : 'Reference Id',
            },
            'db_align_beg', 
            'db_align_end', 
            'seq_align_beg', 
            'seq_align_end', 
            'details', 
        ],
        'entry' :  [
            {
                'source' : [{'outbound': ['PDB', 'struct_ref_seq_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'align_id', 
            {
                'source' : [{'outbound': ['PDB', 'struct_ref_seq_struct_ref_combo1_fkey']}, 'RID'],
                'comment' : 'A reference to table struct_ref.id.',
                'markdown_name' : 'Reference Id',
            },
            'db_align_beg', 
            'db_align_end', 
            'seq_align_beg', 
            'seq_align_end', 
            'details', 
        ],
        'detailed' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'struct_ref_seq_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'align_id', 
            {
                'source' : [{'outbound': ['PDB', 'struct_ref_seq_struct_ref_combo1_fkey']}, 'RID'],
                'comment' : 'A reference to table struct_ref.id.',
                'markdown_name' : 'Reference Id',
            },
            'db_align_beg', 
            'db_align_end', 
            'seq_align_beg', 
            'seq_align_end', 
            'details', 
            ['PDB', 'struct_ref_seq_RCB_fkey'], 
            ['PDB', 'struct_ref_seq_RMB_fkey'], 
            'RCT', 
            'RMT', 
            ['PDB', 'struct_ref_seq_Owner_fkey'], 
        ],
    })

    # ----------------------------
    schema.tables["struct_ref_seq"].visible_foreign_keys.update({
        'filter' :  'detailed',
        'detailed' :  [
            ['PDB', 'struct_ref_seq_dif_struct_ref_seq_combo1_fkey'], 
        ],
    })

    # ----------------------------
    schema.tables["struct_ref_seq"].columns["db_align_beg"].display.update(
        {'name' : 'Database Sequence Align Begin', }
    )

    # ----------------------------
    schema.tables["struct_ref_seq"].columns["db_align_end"].display.update(
        {'name' : 'Database Sequence Align End', }
    )

    # ----------------------------
    schema.tables["struct_ref_seq"].columns["seq_align_beg"].display.update(
        {'name' : 'Sequence Align Begin', }
    )

    # ----------------------------
    schema.tables["struct_ref_seq"].columns["seq_align_end"].display.update(
        {'name' : 'Sequence Align End', }
    )

    # ----------------------------
    schema.tables["struct_ref_seq"].foreign_keys[(schema,"struct_ref_seq_struct_ref_combo1_fkey")].foreign_key.update({
        'template_engine' :  'handlebars',
        'domain_filter_pattern' :  '{{#if _structure_id}}structure_id={{{_structure_id}}}{{/if}}',
    })

# -- -----------------------------------------------------------------------------
def update_PDB_struct_ref_seq_dif(model):
    schema = model.schemas["PDB"]
    table = schema.tables["struct_ref_seq_dif"]
    # ----------------------------
    schema.tables["struct_ref_seq_dif"].display.update(
        {'name' : 'Point differences in the alignment with the reference sequence', 'comment_display' : {'*': {'table_comment_display': 'inline'}}, }
    )

    # ----------------------------
    schema.tables["struct_ref_seq_dif"].visible_columns.update({
        '*' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'struct_ref_seq_dif_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'pdbx_ordinal', 
            {
                'source' : [{'outbound': ['PDB', 'struct_ref_seq_dif_struct_ref_seq_combo1_fkey']}, 'RID'],
                'comment' : 'A reference to table struct_ref_seq.align_id.',
                'markdown_name' : 'Align Id',
            },
            'seq_num', 
            'mon_id', 
            'db_mon_id', 
            ['PDB', 'struct_ref_seq_dif_details_fkey'], 
        ],
        'entry' :  [
            {
                'source' : [{'outbound': ['PDB', 'struct_ref_seq_dif_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'pdbx_ordinal', 
            {
                'source' : [{'outbound': ['PDB', 'struct_ref_seq_dif_struct_ref_seq_combo1_fkey']}, 'RID'],
                'comment' : 'A reference to table struct_ref_seq.align_id.',
                'markdown_name' : 'Align Id',
            },
            'seq_num', 
            'mon_id', 
            'db_mon_id', 
            ['PDB', 'struct_ref_seq_dif_details_fkey'], 
        ],
        'detailed' :  [
            'RID', 
            {
                'source' : [{'outbound': ['PDB', 'struct_ref_seq_dif_structure_id_fkey']}, 'RID'],
                'comment' : 'A reference to table entry.id.',
                'markdown_name' : 'Structure Id',
            },
            'pdbx_ordinal', 
            {
                'source' : [{'outbound': ['PDB', 'struct_ref_seq_dif_struct_ref_seq_combo1_fkey']}, 'RID'],
                'comment' : 'A reference to table struct_ref_seq.align_id.',
                'markdown_name' : 'Align Id',
            },
            'seq_num', 
            'mon_id', 
            'db_mon_id', 
            ['PDB', 'struct_ref_seq_dif_details_fkey'], 
            ['PDB', 'struct_ref_seq_dif_RCB_fkey'], 
            ['PDB', 'struct_ref_seq_dif_RMB_fkey'], 
            'RCT', 
            'RMT', 
            ['PDB', 'struct_ref_seq_dif_Owner_fkey'], 
        ],
    })

    # ----------------------------
    schema.tables["struct_ref_seq_dif"].columns["pdbx_ordinal"].display.update(
        {'name' : 'Ordinal', }
    )

    # ----------------------------
    schema.tables["struct_ref_seq_dif"].columns["seq_num"].display.update(
        {'name' : 'Residue Number', }
    )

    # ----------------------------
    schema.tables["struct_ref_seq_dif"].columns["mon_id"].display.update(
        {'name' : 'Residue Name', }
    )

    # ----------------------------
    schema.tables["struct_ref_seq_dif"].columns["db_mon_id"].display.update(
        {'name' : 'Database Residue Name', }
    )

    # ----------------------------
    schema.tables["struct_ref_seq_dif"].foreign_keys[(schema,"struct_ref_seq_dif_struct_ref_seq_combo1_fkey")].foreign_key.update({
        'template_engine' :  'handlebars',
        'domain_filter_pattern' :  '{{#if _structure_id}}structure_id={{{_structure_id}}}{{/if}}',
    })

# -- -----------------------------------------------------------------------------
def update_PDB_base_annotations(model):
    
    update_PDB_atom_type(model)
    update_PDB_audit_author(model)
    update_PDB_audit_conform(model)
    update_PDB_chem_comp(model)
    update_PDB_chem_comp_atom(model)
    update_PDB_citation(model)
    update_PDB_citation_author(model)
    update_PDB_entity(model)
    update_PDB_entity_name_com(model)
    update_PDB_entity_name_sys(model)
    update_PDB_entity_poly(model)
    update_PDB_entity_poly_seq(model)
    update_PDB_entity_src_gen(model)
    #update_PDB_entry(model)  # in PDB.py
    update_PDB_pdbx_entity_nonpoly(model)
    update_PDB_pdbx_entity_poly_na_type(model)
    update_PDB_pdbx_entry_details(model)
    update_PDB_pdbx_inhibitor_info(model)
    update_PDB_pdbx_ion_info(model)
    update_PDB_pdbx_protein_info(model)
    update_PDB_software(model)
    update_PDB_struct(model)
    update_PDB_struct_asym(model)
    update_PDB_struct_ref(model)
    update_PDB_struct_ref_seq(model)
    update_PDB_struct_ref_seq_dif(model)

# -- =================================================================================    
def main(server_name, catalog_id, credentials, args):
    server = DerivaServer('https', server_name, credentials)
    catalog = server.connect_ermrest(catalog_id)
    catalog.dcctx['cid'] = DCCTX["annotation"]
    model = catalog.getCatalogModel()
    schema_name = "PDB"
    
    if args.pre_print:
        print_schema_annotations(model, schema_name)

    update_PDB_base_annotations(model)

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
