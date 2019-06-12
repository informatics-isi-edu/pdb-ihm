import argparse
from attrdict import AttrDict
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
from deriva.utils.catalog.components.deriva_model import DerivaCatalog
import deriva.core.ermrest_model as em
from deriva.core.ermrest_config import tag as chaise_tags
from deriva.utils.catalog.manage.update_catalog import CatalogUpdater, parse_args

groups = {
    'pdb-admin': 'https://auth.globus.org/0b98092c-3c41-11e9-a8c8-0ee7d80087ee',
    'pdb-reader': 'https://auth.globus.org/8875a770-3c40-11e9-a8c8-0ee7d80087ee',
    'pdb-writer': 'https://auth.globus.org/c94a1e5c-3c40-11e9-a5d1-0aacc65bfe9a',
    'pdb-curator': 'https://auth.globus.org/eef3e02a-3c40-11e9-9276-0edc9bdd56a6',
    'isrd-staff': 'https://auth.globus.org/176baec4-ed26-11e5-8e88-22000ab4b42b'
}

table_name = 'ihm_starting_comparative_models'

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
    'alignment_file_id': {},
    'id': {
        chaise_tags.generated: None
    },
    'starting_model_auth_asym_id': {},
    'starting_model_id': {},
    'starting_model_seq_id_begin': {},
    'starting_model_seq_id_end': {},
    'template_auth_asym_id': {},
    'template_dataset_list_id': {},
    'template_seq_id_begin': {},
    'template_seq_id_end': {},
    'template_sequence_identity': {},
    'template_sequence_identity_denominator': {},
    'Owner': {}
}

column_comment = {
    'structure_id': 'type:text\nThe value of _entry.id identifies the data block.\n\n Note that this item need not be a number; it can be any unique\n identifier.',
    'alignment_file_id': 'type:int4\nA unique identifier for each external file.',
    'id': 'type:int4\nA unique identifier for the starting comparative model.',
    'starting_model_auth_asym_id': 'type:text\nThe chainId/auth_asym_id corresponding to the starting model.',
    'starting_model_id': 'type:text\nA unique identifier for the starting structural model.',
    'starting_model_seq_id_begin': 'type:int4\nThe starting residue index of the starting model.',
    'starting_model_seq_id_end': 'type:int4\nThe ending residue index of the starting model.',
    'template_auth_asym_id': 'type:text\nThe chainId/auth_asym_id corresponding to the template.',
    'template_dataset_list_id': 'type:int4\nA unique identifier for the dataset.',
    'template_seq_id_begin': 'type:int4\nThe starting residue index of the template.',
    'template_seq_id_end': 'type:int4\nThe ending residue index of the template.',
    'template_sequence_identity': 'type:float4\nThe percentage sequence identity between the template sequence and the comparative model sequence.',
    'template_sequence_identity_denominator': 'type:int4\nThe denominator used while calculating the sequence identity provided in \n _ihm_starting_comparative_models.template_sequence_identity.',
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
        'alignment_file_id',
        em.builtin_types['int4'],
        comment=column_comment['alignment_file_id'],
    ),
    em.Column.define(
        'id',
        em.builtin_types['int4'],
        nullok=False,
        annotations=column_annotations['id'],
        comment=column_comment['id'],
    ),
    em.Column.define(
        'starting_model_auth_asym_id',
        em.builtin_types['text'],
        nullok=False,
        comment=column_comment['starting_model_auth_asym_id'],
    ),
    em.Column.define(
        'starting_model_id',
        em.builtin_types['text'],
        nullok=False,
        comment=column_comment['starting_model_id'],
    ),
    em.Column.define(
        'starting_model_seq_id_begin',
        em.builtin_types['int4'],
        comment=column_comment['starting_model_seq_id_begin'],
    ),
    em.Column.define(
        'starting_model_seq_id_end',
        em.builtin_types['int4'],
        comment=column_comment['starting_model_seq_id_end'],
    ),
    em.Column.define(
        'template_auth_asym_id',
        em.builtin_types['text'],
        nullok=False,
        comment=column_comment['template_auth_asym_id'],
    ),
    em.Column.define(
        'template_dataset_list_id',
        em.builtin_types['int4'],
        nullok=False,
        comment=column_comment['template_dataset_list_id'],
    ),
    em.Column.define(
        'template_seq_id_begin',
        em.builtin_types['int4'],
        comment=column_comment['template_seq_id_begin'],
    ),
    em.Column.define(
        'template_seq_id_end',
        em.builtin_types['int4'],
        comment=column_comment['template_seq_id_end'],
    ),
    em.Column.define(
        'template_sequence_identity',
        em.builtin_types['float4'],
        comment=column_comment['template_sequence_identity'],
    ),
    em.Column.define(
        'template_sequence_identity_denominator',
        em.builtin_types['int4'],
        comment=column_comment['template_sequence_identity_denominator'],
    ),
    em.Column.define('Owner', em.builtin_types['text'], comment=column_comment['Owner'],
                     ),
]

visible_columns = {
    '*': [
        'RID',
        {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_starting_comparative_models_structure_id_fkey']
                }, 'RID'
            ],
            'comment': 'type:text\nThe value of _entry.id identifies the data block.\n\n Note that this item need not be a number; it can be any unique\n identifier.',
            'markdown_name': 'structure id'
        },
        {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_starting_comparative_models_alignment_file_id_fkey']
                }, 'RID'
            ],
            'comment': 'type:int4\nA unique identifier for each external file.',
            'markdown_name': 'alignment file id'
        }, 'id', 'starting_model_auth_asym_id',
        {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_starting_comparative_models_starting_model_id_fkey']
                }, 'RID'
            ],
            'comment': 'type:text\nA unique identifier for the starting structural model.',
            'markdown_name': 'starting model id'
        }, 'starting_model_seq_id_begin', 'starting_model_seq_id_end', 'template_auth_asym_id',
        {
            'source': [
                {
                    'outbound': [
                        'PDB', 'ihm_starting_comparative_models_template_dataset_list_id_fkey'
                    ]
                }, 'RID'
            ],
            'comment': 'type:int4\nA unique identifier for the dataset.',
            'markdown_name': 'template dataset list id'
        }, 'template_seq_id_begin', 'template_seq_id_end', 'template_sequence_identity',
        ['PDB', 'models_template_sequence_identity_denominator_term_fkey'],
        ['PDB', 'ihm_starting_comparative_models_RCB_fkey'],
        ['PDB', 'ihm_starting_comparative_models_RMB_fkey'], 'RCT', 'RMT',
        ['PDB', 'ihm_starting_comparative_models_Owner_fkey']
    ],
    'entry': [
        {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_starting_comparative_models_structure_id_fkey']
                }, 'RID'
            ],
            'comment': 'type:text\nThe value of _entry.id identifies the data block.\n\n Note that this item need not be a number; it can be any unique\n identifier.',
            'markdown_name': 'structure id'
        },
        {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_starting_comparative_models_alignment_file_id_fkey']
                }, 'RID'
            ],
            'comment': 'type:int4\nA unique identifier for each external file.',
            'markdown_name': 'alignment file id'
        }, 'id', 'starting_model_auth_asym_id',
        {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_starting_comparative_models_starting_model_id_fkey']
                }, 'RID'
            ],
            'comment': 'type:text\nA unique identifier for the starting structural model.',
            'markdown_name': 'starting model id'
        }, 'starting_model_seq_id_begin', 'starting_model_seq_id_end', 'template_auth_asym_id',
        {
            'source': [
                {
                    'outbound': [
                        'PDB', 'ihm_starting_comparative_models_template_dataset_list_id_fkey'
                    ]
                }, 'RID'
            ],
            'comment': 'type:int4\nA unique identifier for the dataset.',
            'markdown_name': 'template dataset list id'
        }, 'template_seq_id_begin', 'template_seq_id_end', 'template_sequence_identity',
        ['PDB', 'models_template_sequence_identity_denominator_term_fkey']
    ]
}

table_annotations = {chaise_tags.visible_columns: visible_columns, }

table_comment = None

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
    em.Key.define(['RID'], constraint_names=[('PDB', 'ihm_starting_comparative_models_RIDkey1')],
                  ),
    em.Key.define(
        ['structure_id', 'id'],
        constraint_names=[('PDB', 'ihm_starting_comparative_models_primary_key')],
    ),
]

fkey_defs = [
    em.ForeignKey.define(
        ['Owner'],
        'public',
        'Catalog_Group', ['ID'],
        constraint_names=[('PDB', 'ihm_starting_comparative_models_Owner_fkey')],
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
        ['RCB'],
        'public',
        'ERMrest_Client', ['ID'],
        constraint_names=[('PDB', 'ihm_starting_comparative_models_RCB_fkey')],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
    ),
    em.ForeignKey.define(
        ['RMB'],
        'public',
        'ERMrest_Client', ['ID'],
        constraint_names=[('PDB', 'ihm_starting_comparative_models_RMB_fkey')],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
    ),
    em.ForeignKey.define(
        ['structure_id'],
        'PDB',
        'entry', ['id'],
        constraint_names=[('PDB', 'ihm_starting_comparative_models_structure_id_fkey')],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
        on_update='CASCADE',
        on_delete='SET NULL',
    ),
    em.ForeignKey.define(
        ['structure_id', 'alignment_file_id'],
        'PDB',
        'ihm_external_files', ['structure_id', 'id'],
        constraint_names=[('PDB', 'ihm_starting_comparative_models_alignment_file_id_fkey')],
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
    em.ForeignKey.define(
        ['structure_id', 'starting_model_id'],
        'PDB',
        'ihm_starting_model_details', ['structure_id', 'starting_model_id'],
        constraint_names=[('PDB', 'ihm_starting_comparative_models_starting_model_id_fkey')],
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
    em.ForeignKey.define(
        ['structure_id', 'template_dataset_list_id'],
        'PDB',
        'ihm_dataset_list', ['structure_id', 'id'],
        constraint_names=[('PDB', 'ihm_starting_comparative_models_template_dataset_list_id_fkey')],
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
    updater.update_table(mode, schema_name, table_def, replace=replace, really=really)


if __name__ == "__main__":
    host = 'pdb.isrd.isi.edu'
    catalog_id = 5
    mode, replace, host, catalog_id = parse_args(host, catalog_id, is_table=True)
    catalog = DerivaCatalog(host, catalog_id=catalog_id, validate=False)
    main(catalog, mode, replace)

