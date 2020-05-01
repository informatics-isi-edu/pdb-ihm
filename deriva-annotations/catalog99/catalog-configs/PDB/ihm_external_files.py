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
    'isrd-staff': 'https://auth.globus.org/176baec4-ed26-11e5-8e88-22000ab4b42b'
}

table_name = 'ihm_external_files'

schema_name = 'PDB'

column_annotations = {
    'RCT': {
        chaise_tags.display: {
            'name': 'Creation Time'
        },
        chaise_tags.generated: None,
        chaise_tags.immutable: None
    },
    'RMT': {
        chaise_tags.display: {
            'name': 'Last Modified Time'
        },
        chaise_tags.generated: None,
        chaise_tags.immutable: None
    },
    'RCB': {
        chaise_tags.display: {
            'name': 'Created By'
        },
        chaise_tags.generated: None,
        chaise_tags.immutable: None
    },
    'RMB': {
        chaise_tags.display: {
            'name': 'Modified By'
        },
        chaise_tags.generated: None,
        chaise_tags.immutable: None
    },
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

table_acl_bindings = {
    'self_service_group': {
        'types': ['update', 'delete'],
        'scope_acl': ['*'],
        'projection': ['Owner'],
        'projection_type': 'acl'
    },
    'self_service_creator': {
        'types': ['update', 'delete'],
        'scope_acl': ['*'],
        'projection': ['RCB'],
        'projection_type': 'acl'
    }
}

key_defs = [
    em.Key.define(
        ['id', 'structure_id'], constraint_names=[['PDB', 'ihm_external_files_primary_key']],
    ),
    em.Key.define(['RID'], constraint_names=[['PDB', 'ihm_external_files_RIDkey1']],
                  ),
]

fkey_defs = [
    em.ForeignKey.define(
        ['Owner'],
        'public',
        'Catalog_Group', ['ID'],
        constraint_names=[['PDB', 'ihm_external_files_Owner_fkey']],
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
    em.ForeignKey.define(
        ['content_type'],
        'Vocab',
        'ihm_external_files_content_type', ['ID'],
        constraint_names=[['PDB', 'ihm_external_files_content_type_fkey']],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
    ),
    em.ForeignKey.define(
        ['RCB'],
        'public',
        'ERMrest_Client', ['ID'],
        constraint_names=[['PDB', 'ihm_external_files_RCB_fkey']],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
    ),
    em.ForeignKey.define(
        ['structure_id'],
        'PDB',
        'entry', ['id'],
        constraint_names=[['PDB', 'ihm_external_files_structure_id_fkey']],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
        on_update='CASCADE',
        on_delete='SET NULL',
    ),
    em.ForeignKey.define(
        ['RMB'],
        'public',
        'ERMrest_Client', ['ID'],
        constraint_names=[['PDB', 'ihm_external_files_RMB_fkey']],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
    ),
    em.ForeignKey.define(
        ['file_format'],
        'Vocab',
        'ihm_external_files_file_format', ['ID'],
        constraint_names=[['PDB', 'ihm_external_files_file_format_fkey']],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
    ),
    em.ForeignKey.define(
        ['reference_id', 'structure_id'],
        'PDB',
        'ihm_external_reference_info', ['reference_id', 'structure_id'],
        constraint_names=[['PDB', 'ihm_external_files_reference_id_fkey']],
        annotations={
            chaise_tags.foreign_key: {
                'domain_filter_pattern': 'structure_id={{structure_id}}'
            }
        },
        acls={
            'insert': ['*'],
            'update': ['*']
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
    catalog_id = 99
    mode, replace, host, catalog_id = parse_args(host, catalog_id, is_table=True)
    catalog = ErmrestCatalog('https', host, catalog_id=catalog_id, credentials=get_credential(host))
    main(catalog, mode, replace)
