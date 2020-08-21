import argparse
from deriva.core import ErmrestCatalog, AttrDict, get_credential
import deriva.core.ermrest_model as em
from deriva.core.ermrest_config import tag as chaise_tags
from deriva.utils.catalog.manage.update_catalog import CatalogUpdater, parse_args

groups = {}

table_name = 'ihm_external_files'

schema_name = 'PDB'

column_annotations = {
    'structure_id': {},
    'content_type': {},
    'details': {},
    'file_format': {},
    'file_path': {},
    'file_size_bytes': {},
    'id': {},
    'reference_id': {},
    'Owner': {}
}

column_comment = {
    'structure_id': 'A reference to table entry.id.',
    'content_type': 'type:text\nThe type of content in the file.',
    'details': 'type:text\nAdditional textual details regarding the external file.\nexamples:Readme file,Nup84 multiple sequence alignment file,Nup84 starting comparative model file',
    'file_format': 'type:text\nFormat of the external file.',
    'file_path': 'type:text\nThe relative path (including filename) for each external file. \n Absolute paths (starting with "/") are not permitted. \n This is required for identifying individual files from within\n a tar-zipped archive file or for identifying supplementary local\n files organized within a directory structure.\n This data item assumes a POSIX-like directory structure or file path.\nexamples:integrativemodeling-nup84-a69f895/outputs/localization/cluster1/nup84.mrc,integrativemodeling-nup84-a69f895/scripts/MODELLER_scripts/Nup84/all_align_final2.ali,nup145.mrc,data/EDC_XL_122013.dat',
    'file_size_bytes': 'type:float4\nStorage size of the external file in bytes.',
    'id': 'type:int4\nA unique identifier for each external file.',
    'reference_id': 'A reference to table ihm_external_reference_info.reference_id.',
    'Owner': 'Group that can update the record.'
}

column_acls = {}

column_acl_bindings = {}

column_defs = [
    em.Column.define(
        'structure_id',
        em.builtin_types['text'],
        nullok=False,
        comment=column_comment['structure_id'],
    ),
    em.Column.define(
        'content_type',
        em.builtin_types['text'],
        nullok=False,
        comment=column_comment['content_type'],
    ),
    em.Column.define('details', em.builtin_types['text'], comment=column_comment['details'],
                     ),
    em.Column.define(
        'file_format', em.builtin_types['text'], comment=column_comment['file_format'],
    ),
    em.Column.define('file_path', em.builtin_types['text'], comment=column_comment['file_path'],
                     ),
    em.Column.define(
        'file_size_bytes', em.builtin_types['float4'], comment=column_comment['file_size_bytes'],
    ),
    em.Column.define('id', em.builtin_types['int4'], nullok=False, comment=column_comment['id'],
                     ),
    em.Column.define(
        'reference_id',
        em.builtin_types['int4'],
        nullok=False,
        comment=column_comment['reference_id'],
    ),
    em.Column.define('Owner', em.builtin_types['text'], comment=column_comment['Owner'],
                     ),
]

visible_columns = {
    '*': [
        'RID', {
            'source': [{
                'outbound': ['PDB', 'ihm_external_files_structure_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table entry.id.',
            'markdown_name': 'structure id'
        }, 'id', {
            'source': [{
                'outbound': ['PDB', 'ihm_external_files_reference_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table ihm_external_reference_info.reference_id.',
            'markdown_name': 'reference id'
        }, 'file_path', ['PDB', 'ihm_external_files_file_format_fkey'],
        ['PDB', 'ihm_external_files_content_type_fkey'], 'file_size_bytes', 'details'
    ],
    'entry': [
        {
            'source': [{
                'outbound': ['PDB', 'ihm_external_files_structure_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table entry.id.',
            'markdown_name': 'structure id'
        }, 'id', {
            'source': [{
                'outbound': ['PDB', 'ihm_external_files_reference_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table ihm_external_reference_info.reference_id.',
            'markdown_name': 'reference id'
        }, 'file_path', ['PDB', 'ihm_external_files_file_format_fkey'],
        ['PDB', 'ihm_external_files_content_type_fkey'], 'file_size_bytes', 'details'
    ],
    'detailed': [
        'RID', {
            'source': [{
                'outbound': ['PDB', 'ihm_external_files_structure_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table entry.id.',
            'markdown_name': 'structure id'
        }, 'id', {
            'source': [{
                'outbound': ['PDB', 'ihm_external_files_reference_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table ihm_external_reference_info.reference_id.',
            'markdown_name': 'reference id'
        }, 'file_path', ['PDB', 'ihm_external_files_file_format_fkey'],
        ['PDB', 'ihm_external_files_content_type_fkey'], 'file_size_bytes', 'details',
        ['PDB', 'ihm_external_files_RCB_fkey'], ['PDB', 'ihm_external_files_RMB_fkey'], 'RCT',
        'RMT', ['PDB', 'ihm_external_files_Owner_fkey']
    ]
}

visible_foreign_keys = {
    'filter': 'detailed',
    'detailed': [
        ['PDB', 'ihm_dataset_external_reference_file_id_fkey'],
        ['PDB', 'ihm_modeling_protocol_details_script_file_id_fkey'],
        ['PDB', 'ihm_modeling_post_process_script_file_id_fkey'],
        ['PDB', 'ihm_starting_comparative_models_alignment_file_id_fkey'],
        ['PDB', 'ihm_starting_computational_models_script_file_id_fkey'],
        ['PDB', 'ihm_ensemble_info_ensemble_file_id_fkey'],
        ['PDB', 'ihm_localization_density_files_file_id_fkey']
    ]
}

table_display = {'row_name': {'row_markdown_pattern': '{{{id}}}'}}

table_annotations = {
    chaise_tags.table_display: table_display,
    chaise_tags.visible_columns: visible_columns,
    chaise_tags.visible_foreign_keys: visible_foreign_keys,
}

table_comment = 'External files available from the external references provided in Ihm External Reference Info'

table_acls = {}

table_acl_bindings = {}

key_defs = [
    em.Key.define(['RID'], constraint_names=[['PDB', 'ihm_external_files_RIDkey1']],
                  ),
    em.Key.define(
        ['id', 'structure_id'], constraint_names=[['PDB', 'ihm_external_files_primary_key']],
    ),
    em.Key.define(['id', 'RID'], constraint_names=[['PDB', 'ihm_external_files_id_RID_key']],
                  ),
]

fkey_defs = [
    em.ForeignKey.define(
        ['content_type'],
        'Vocab',
        'ihm_external_files_content_type', ['Name'],
        constraint_names=[['PDB', 'ihm_external_files_content_type_fkey']],
    ),
    em.ForeignKey.define(
        ['file_format'],
        'Vocab',
        'ihm_external_files_file_format', ['Name'],
        constraint_names=[['PDB', 'ihm_external_files_file_format_fkey']],
    ),
    em.ForeignKey.define(
        ['RCB'],
        'public',
        'ERMrest_Client', ['ID'],
        constraint_names=[['PDB', 'ihm_external_files_RCB_fkey']],
    ),
    em.ForeignKey.define(
        ['RMB'],
        'public',
        'ERMrest_Client', ['ID'],
        constraint_names=[['PDB', 'ihm_external_files_RMB_fkey']],
    ),
    em.ForeignKey.define(
        ['structure_id', 'reference_id'],
        'PDB',
        'ihm_external_reference_info', ['structure_id', 'reference_id'],
        constraint_names=[['PDB', 'ihm_external_files_reference_id_fkey']],
        annotations={
            chaise_tags.foreign_key: {
                'domain_filter_pattern': 'structure_id={{structure_id}}'
            }
        },
        on_update='CASCADE',
        on_delete='SET NULL',
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
    catalog_id = 50
    mode, replace, host, catalog_id = parse_args(host, catalog_id, is_table=True)
    catalog = ErmrestCatalog('https', host, catalog_id=catalog_id, credentials=get_credential(host))
    main(catalog, mode, replace)
