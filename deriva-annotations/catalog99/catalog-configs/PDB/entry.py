import argparse
from deriva.core import ErmrestCatalog, AttrDict, get_credential
import deriva.core.ermrest_model as em
from deriva.core.ermrest_config import tag as chaise_tags
from deriva.utils.catalog.manage.update_catalog import CatalogUpdater, parse_args

groups = {
    'pdb-reader': 'https://auth.globus.org/8875a770-3c40-11e9-a8c8-0ee7d80087ee',
    'pdb-writer': 'https://auth.globus.org/c94a1e5c-3c40-11e9-a5d1-0aacc65bfe9a',
    'pdb-admin': 'https://auth.globus.org/0b98092c-3c41-11e9-a8c8-0ee7d80087ee',
    'pdb-curator': 'https://auth.globus.org/eef3e02a-3c40-11e9-9276-0edc9bdd56a6',
    'isrd-staff': 'https://auth.globus.org/176baec4-ed26-11e5-8e88-22000ab4b42b',
    'pdb-submitter': 'https://auth.globus.org/99da042e-64a6-11ea-ad5f-0ef992ed7ca1'
}

table_name = 'entry'

schema_name = 'PDB'

column_annotations = {
    'id': {
        chaise_tags.generated: None
    },
    'Owner': {},
    'Image_File_URL': {
        chaise_tags.asset: {
            'md5': 'Image_File_MD5',
            'url_pattern': '/hatrac/pdb/image/{{$moment.year}}/{{{Image_File_MD5}}}',
            'filename_column': 'Image_File_Name',
            'byte_count_column': 'Image_File_Bytes'
        }
    },
    'mmCIF_File_URL': {
        chaise_tags.asset: {
            'md5': 'mmCIF_File_MD5',
            'url_pattern': '/hatrac/pdb/mmCIF/{{$moment.year}}/{{{mmCIF_File_MD5}}}',
            'filename_column': 'mmCIF_File_Name',
            'byte_count_column': 'mmCIF_File_Bytes'
        }
    }
}

column_comment = {
    'id': 'type:text\nThe value of _entry.id identifies the data block.\n\n Note that this item need not be a number; it can be any unique\n identifier.',
    'Owner': 'Group that can update the record.'
}

column_acls = {}

column_acl_bindings = {}

column_defs = [
    em.Column.define(
        'id',
        em.builtin_types['text'],
        nullok=False,
        annotations=column_annotations['id'],
        comment=column_comment['id'],
    ),
    em.Column.define('Owner', em.builtin_types['text'], comment=column_comment['Owner'],
                     ),
    em.Column.define(
        'Image_File_URL',
        em.builtin_types['text'],
        annotations=column_annotations['Image_File_URL'],
    ),
    em.Column.define('Image_File_Name', em.builtin_types['text'],
                     ),
    em.Column.define('Image_File_MD5', em.builtin_types['text'],
                     ),
    em.Column.define('Image_File_Bytes', em.builtin_types['int8'],
                     ),
    em.Column.define(
        'mmCIF_File_URL',
        em.builtin_types['text'],
        annotations=column_annotations['mmCIF_File_URL'],
    ),
    em.Column.define('mmCIF_File_Name', em.builtin_types['text'],
                     ),
    em.Column.define('mmCIF_File_MD5', em.builtin_types['text'],
                     ),
    em.Column.define('mmCIF_File_Bytes', em.builtin_types['int8'],
                     ),
    em.Column.define('Workflow_Status', em.builtin_types['text'],
                     ),
    em.Column.define('Process_Status', em.builtin_types['text'], default='New',
                     ),
    em.Column.define('Record_Status_Detail', em.builtin_types['text'],
                     ),
    em.Column.define('accession_code', em.builtin_types['text'],
                     ),
]

visible_columns = {
    '*': [
        'RID', 'id', 'mmCIF_File_URL', 'Image_File_URL', ['PDB', 'entry_workflow_status_fkey'],
        'Record_Status_Detail', 'accession_code', ['PDB', 'entry_RCB_fkey'],
        ['PDB', 'entry_RMB_fkey'], 'RCT', 'RMT', ['PDB', 'entry_Owner_fkey']
    ],
    'entry': [
        'mmCIF_File_URL', 'Image_File_URL', ['PDB', 'entry_workflow_status_fkey'], 'accession_code'
    ],
    'detailed': [
        'RID', 'id', 'mmCIF_File_URL', {
            'source': 'mmCIF_File_Bytes',
            'markdown_name': 'mmCIF File Size (Bytes)'
        }, 'Image_File_URL', {
            'source': 'Image_File_Bytes',
            'markdown_name': 'Image File Size (Bytes)'
        }, ['PDB', 'entry_workflow_status_fkey'], 'Record_Status_Detail', 'accession_code',
        ['PDB', 'entry_RCB_fkey'], ['PDB', 'entry_RMB_fkey'], 'RCT', 'RMT',
        ['PDB', 'entry_Owner_fkey']
    ]
}

visible_foreign_keys = {
    'filter': 'detailed',
    'detailed': [
        ['PDB', 'struct_entry_id_fkey'], ['PDB', 'audit_author_structure_id_fkey'],
        ['PDB', 'citation_structure_id_fkey'], ['PDB', 'citation_author_structure_id_fkey'],
        ['PDB', 'software_structure_id_fkey'], ['PDB', 'chem_comp_structure_id_fkey'],
        ['PDB', 'chem_comp_atom_structure_id_fkey'], ['PDB', 'entity_structure_id_fkey'],
        ['PDB', 'entity_name_com_structure_id_fkey'], ['PDB', 'entity_name_sys_structure_id_fkey'],
        ['PDB', 'entity_src_gen_structure_id_fkey'], ['PDB', 'entity_poly_structure_id_fkey'],
        ['PDB', 'pdbx_entity_nonpoly_structure_id_fkey'],
        ['PDB', 'entity_poly_seq_structure_id_fkey'], ['PDB', 'atom_type_structure_id_fkey'],
        ['PDB', 'struct_asym_structure_id_fkey'],
        ['PDB', 'ihm_entity_poly_segment_structure_id_fkey'],
        ['PDB', 'ihm_model_representation_structure_id_fkey'],
        ['PDB', 'ihm_model_representation_details_structure_id_fkey'],
        ['PDB', 'ihm_struct_assembly_structure_id_fkey'],
        ['PDB', 'ihm_struct_assembly_details_structure_id_fkey'],
        ['PDB', 'ihm_struct_assembly_class_structure_id_fkey'],
        ['PDB', 'ihm_struct_assembly_class_link_structure_id_fkey'],
        ['PDB',
         'ihm_dataset_list_structure_id_fkey'], ['PDB', 'ihm_dataset_group_structure_id_fkey'],
        ['PDB', 'ihm_dataset_group_link_structure_id_fkey'],
        ['PDB', 'ihm_dataset_related_db_reference_structure_id_fkey'],
        ['PDB', 'ihm_external_reference_info_structure_id_fkey'],
        ['PDB', 'ihm_external_files_structure_id_fkey'],
        ['PDB', 'ihm_dataset_external_reference_structure_id_fkey'],
        ['PDB', 'ihm_related_datasets_structure_id_fkey'],
        ['PDB', 'ihm_starting_model_details_structure_id_fkey'],
        ['PDB', 'ihm_starting_comparative_models_structure_id_fkey'],
        ['PDB', 'ihm_starting_computational_models_structure_id_fkey'],
        ['PDB', 'ihm_starting_model_seq_dif_structure_id_fkey'],
        ['PDB', 'ihm_chemical_component_descriptor_structure_id_fkey'],
        ['PDB', 'Entry_Related_File_entry_id_fkey'],
        ['PDB', 'ihm_probe_list_structure_id_fkey'],
        ['PDB', 'ihm_poly_probe_position_structure_id_fkey'],
        ['PDB', 'ihm_poly_probe_conjugate_structure_id_fkey'],
        ['PDB', 'ihm_ligand_probe_structure_id_fkey'],
        ['PDB', 'ihm_cross_link_list_structure_id_fkey'],
        ['PDB', 'ihm_cross_link_restraint_structure_id_fkey'],
        ['PDB', 'ihm_2dem_class_average_restraint_structure_id_fkey'],
        ['PDB', 'ihm_hydroxyl_radical_fp_restraint_structure_id_fkey'],
        ['PDB', 'ihm_predicted_contact_restraint_structure_id_fkey'],
        ['PDB', 'ihm_feature_list_structure_id_fkey'],
        ['PDB', 'ihm_poly_atom_feature_structure_id_fkey'],
        ['PDB', 'ihm_poly_residue_feature_structure_id_fkey'],
        ['PDB', 'ihm_non_poly_feature_structure_id_fkey'],
        ['PDB', 'ihm_interface_residue_feature_structure_id_fkey'],
        ['PDB', 'ihm_pseudo_site_feature_structure_id_fkey'],
        ['PDB', 'ihm_derived_distance_restraint_structure_id_fkey'],
        ['PDB', 'ihm_geometric_object_list_structure_id_fkey'],
        ['PDB', 'ihm_geometric_object_center_structure_id_fkey'],
        ['PDB', 'ihm_geometric_object_transformation_structure_id_fkey'],
        ['PDB', 'ihm_geometric_object_sphere_structure_id_fkey'],
        ['PDB', 'ihm_geometric_object_torus_structure_id_fkey'],
        ['PDB', 'ihm_geometric_object_half_torus_structure_id_fkey'],
        ['PDB', 'ihm_geometric_object_axis_structure_id_fkey'],
        ['PDB', 'ihm_geometric_object_plane_structure_id_fkey'],
        ['PDB', 'ihm_geometric_object_distance_restraint_structure_id_fkey'],
        ['PDB', 'ihm_modeling_protocol_structure_id_fkey'],
        ['PDB', 'ihm_modeling_protocol_details_structure_id_fkey'],
        ['PDB', 'ihm_modeling_post_process_structure_id_fkey'],
        ['PDB', 'ihm_model_list_structure_id_fkey'], ['PDB', 'ihm_model_group_structure_id_fkey'],
        ['PDB', 'ihm_model_group_link_structure_id_fkey'],
        ['PDB', 'ihm_model_representative_structure_id_fkey'],
        ['PDB', 'ihm_residues_not_modeled_structure_id_fkey'],
        ['PDB', 'ihm_cross_link_result_structure_id_fkey'],
        ['PDB', 'ihm_cross_link_result_parameters_structure_id_fkey'],
        ['PDB', 'ihm_2dem_class_average_fitting_structure_id_fkey'],
        ['PDB', 'ihm_3dem_restraint_structure_id_fkey'],
        ['PDB', 'ihm_sas_restraint_structure_id_fkey'],
        ['PDB', 'ihm_epr_restraint_structure_id_fkey'],
        ['PDB', 'ihm_multi_state_modeling_structure_id_fkey'],
        ['PDB', 'ihm_multi_state_model_group_link_structure_id_fkey'],
        ['PDB', 'ihm_ordered_ensemble_structure_id_fkey'],
        ['PDB', 'ihm_ensemble_info_structure_id_fkey'],
        ['PDB', 'ihm_localization_density_files_structure_id_fkey'],
        ['PDB', 'audit_conform_structure_id_fkey'],
        ['PDB', 'pdbx_entity_poly_na_type_structure_id_fkey'],
        ['PDB',
         'pdbx_entry_details_structure_id_fkey'], ['PDB', 'pdbx_entry_details_entry_id_fkey'],
        ['PDB', 'pdbx_inhibitor_info_structure_id_fkey'],
        ['PDB', 'pdbx_ion_info_structure_id_fkey'], ['PDB', 'pdbx_protein_info_structure_id_fkey']
    ]
}

table_display = {'row_name': {'row_markdown_pattern': '{{{id}}}'}}

table_annotations = {
    chaise_tags.table_display: table_display,
    chaise_tags.visible_columns: visible_columns,
    chaise_tags.visible_foreign_keys: visible_foreign_keys,
}

table_comment = 'Identifier for the entry'

table_acls = {
    'owner': [groups['pdb-admin'], groups['isrd-staff']],
    'write': [],
    'delete': [groups['pdb-curator']],
    'insert': [groups['pdb-curator'], groups['pdb-writer'], groups['pdb-submitter']],
    'select': [groups['pdb-writer'], groups['pdb-reader']],
    'update': [groups['pdb-curator']],
    'enumerate': ['*']
}

table_acl_bindings = {
    'released_reader': {
        'types': ['select'],
        'scope_acl': [groups['pdb-submitter']],
        'projection': ['RCB'],
        'projection_type': 'acl'
    },
    'self_service_creator': {
        'types': ['update', 'delete'],
        'scope_acl': [groups['pdb-submitter']],
        'projection': [
            {
                'or': [
                    {
                        'filter': 'Workflow_Status',
                        'operand': 'PDB:1-MSVE',
                        'operator': '='
                    }, {
                        'filter': 'Workflow_Status',
                        'operand': 'PDB:1-MSVG',
                        'operator': '='
                    }
                ]
            }, 'RCB'
        ],
        'projection_type': 'acl'
    }
}

key_defs = [
    em.Key.define(['id'], constraint_names=[['PDB', 'entry_id_unique_key']],
                  ),
    em.Key.define(['RID'], constraint_names=[['PDB', 'entry_RIDkey1']],
                  ),
]

fkey_defs = [
    em.ForeignKey.define(
        ['Workflow_Status'],
        'Vocab',
        'workflow_status', ['ID'],
        constraint_names=[['PDB', 'entry_workflow_status_fkey']],
    ),
    em.ForeignKey.define(
        ['RMB'], 'public', 'ERMrest_Client', ['ID'], constraint_names=[['PDB', 'entry_RMB_fkey']],
    ),
    em.ForeignKey.define(
        ['RCB'], 'public', 'ERMrest_Client', ['ID'], constraint_names=[['PDB', 'entry_RCB_fkey']],
    ),
    em.ForeignKey.define(
        ['Owner'],
        'public',
        'Catalog_Group', ['ID'],
        constraint_names=[['PDB', 'entry_Owner_fkey']],
        acls={
            'insert': [groups['pdb-curator']],
            'update': [groups['pdb-curator']]
        },
        acl_bindings={
            'set_owner': {
                'types': ['update', 'insert'],
                'scope_acl': ['*'],
                'projection': ['ID'],
                'projection_type': 'acl'
            }
        },
    ),
]

table_def = em.Table.define(
    table_name,
    column_defs=column_defs,
    key_defs=key_defs,
    fkey_defs=fkey_defs,
    annotations=table_annotations,
    acls=table_acls,
    acl_bindings=table_acl_bindings,
    comment=table_comment,
    provide_system=True
)


def main(catalog, mode, replace=False, really=False):
    updater = CatalogUpdater(catalog)
    table_def['column_annotations'] = column_annotations
    table_def['column_comment'] = column_comment
    updater.update_table(mode, schema_name, table_def, replace=replace, really=really)


if __name__ == "__main__":
    host = 'pdb.isrd.isi.edu'
    catalog_id = 99
    mode, replace, host, catalog_id = parse_args(host, catalog_id, is_table=True)
    catalog = ErmrestCatalog('https', host, catalog_id=catalog_id, credentials=get_credential(host))
    main(catalog, mode, replace)
