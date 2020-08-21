import argparse
from deriva.core import ErmrestCatalog, AttrDict, get_credential
import deriva.core.ermrest_model as em
from deriva.core.ermrest_config import tag as chaise_tags
from deriva.utils.catalog.manage.update_catalog import CatalogUpdater, parse_args

groups = {}

table_name = 'ihm_starting_comparative_models'

schema_name = 'PDB'

column_annotations = {
    'structure_id': {},
    'alignment_file_id': {},
    'details': {},
    'id': {},
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
    'structure_id': 'A reference to table entry.id.',
    'alignment_file_id': 'A reference to table ihm_external_files.id.',
    'details': 'type:text\nAdditional details regarding the starting comparative models.',
    'id': 'type:int4\nA unique identifier for the starting comparative model.',
    'starting_model_auth_asym_id': 'type:text\nThe chainId/auth_asym_id corresponding to the starting model.',
    'starting_model_id': 'A reference to table ihm_starting_model_details.starting_model_id.',
    'starting_model_seq_id_begin': 'type:int4\nThe starting residue index of the starting model.',
    'starting_model_seq_id_end': 'type:int4\nThe ending residue index of the starting model.',
    'template_auth_asym_id': 'type:text\nThe chainId/auth_asym_id corresponding to the template.',
    'template_dataset_list_id': 'A reference to table ihm_dataset_list.id.',
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
    em.Column.define('details', em.builtin_types['text'], comment=column_comment['details'],
                     ),
    em.Column.define('id', em.builtin_types['int4'], nullok=False, comment=column_comment['id'],
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
        em.builtin_types['text'],
        comment=column_comment['template_sequence_identity_denominator'],
    ),
    em.Column.define('Owner', em.builtin_types['text'], comment=column_comment['Owner'],
                     ),
    em.Column.define('Alignment_file_RID', em.builtin_types['text'],
                     ),
]

visible_columns = {
    '*': [
        'RID', {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_starting_comparative_models_structure_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table entry.id.',
            'markdown_name': 'structure id'
        }, 'id', {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_starting_comparative_models_starting_model_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table ihm_starting_model_details.starting_model_id.',
            'markdown_name': 'starting model id'
        }, 'starting_model_auth_asym_id', 'starting_model_seq_id_begin',
        'starting_model_seq_id_end', 'template_auth_asym_id', 'template_seq_id_begin',
        'template_seq_id_end', 'template_sequence_identity',
        ['PDB', 'starting_comparative_models_template_sequence_id_denom_fkey'], {
            'source': [
                {
                    'outbound': [
                        'PDB', 'ihm_starting_comparative_models_template_dataset_list_id_fkey'
                    ]
                }, 'RID'
            ],
            'comment': 'A reference to table ihm_dataset_list.id.',
            'markdown_name': 'template dataset list id'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_starting_comparative_models_alignment_file_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table ihm_external_files.id.',
            'markdown_name': 'alignment file id'
        }, 'details'
    ],
    'entry': [
        {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_starting_comparative_models_structure_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table entry.id.',
            'markdown_name': 'structure id'
        }, 'id', {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_starting_comparative_models_starting_model_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table ihm_starting_model_details.starting_model_id.',
            'markdown_name': 'starting model id'
        }, 'starting_model_auth_asym_id', 'starting_model_seq_id_begin',
        'starting_model_seq_id_end', 'template_auth_asym_id', 'template_seq_id_begin',
        'template_seq_id_end', 'template_sequence_identity',
        ['PDB', 'starting_comparative_models_template_sequence_id_denom_fkey'], {
            'source': [
                {
                    'outbound': [
                        'PDB', 'ihm_starting_comparative_models_template_dataset_list_id_fkey'
                    ]
                }, 'RID'
            ],
            'comment': 'A reference to table ihm_dataset_list.id.',
            'markdown_name': 'template dataset list id'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_starting_comparative_models_alignment_file_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table ihm_external_files.id.',
            'markdown_name': 'alignment file id'
        }, 'details'
    ],
    'detailed': [
        'RID', {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_starting_comparative_models_structure_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table entry.id.',
            'markdown_name': 'structure id'
        }, 'id', {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_starting_comparative_models_starting_model_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table ihm_starting_model_details.starting_model_id.',
            'markdown_name': 'starting model id'
        }, 'starting_model_auth_asym_id', 'starting_model_seq_id_begin',
        'starting_model_seq_id_end', 'template_auth_asym_id', 'template_seq_id_begin',
        'template_seq_id_end', 'template_sequence_identity',
        ['PDB', 'starting_comparative_models_template_sequence_id_denom_fkey'], {
            'source': [
                {
                    'outbound': [
                        'PDB', 'ihm_starting_comparative_models_template_dataset_list_id_fkey'
                    ]
                }, 'RID'
            ],
            'comment': 'A reference to table ihm_dataset_list.id.',
            'markdown_name': 'template dataset list id'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_starting_comparative_models_alignment_file_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table ihm_external_files.id.',
            'markdown_name': 'alignment file id'
        }, 'details', ['PDB', 'ihm_starting_comparative_models_RCB_fkey'],
        ['PDB', 'ihm_starting_comparative_models_RMB_fkey'], 'RCT', 'RMT',
        ['PDB', 'ihm_starting_comparative_models_Owner_fkey']
    ]
}

table_annotations = {chaise_tags.visible_columns: visible_columns, }

table_comment = 'Additional information regarding comparative models used as starting structural models'

table_acls = {}

table_acl_bindings = {}

key_defs = [
    em.Key.define(
        ['structure_id', 'id'],
        constraint_names=[['PDB', 'ihm_starting_comparative_models_primary_key']],
    ),
    em.Key.define(['RID'], constraint_names=[['PDB', 'ihm_starting_comparative_models_RIDkey1']],
                  ),
]

fkey_defs = [
    em.ForeignKey.define(
        ['template_sequence_identity_denominator'],
        'Vocab',
        'starting_comparative_models_template_sequence_id_denom', ['Name'],
        constraint_names=[['PDB', 'starting_comparative_models_template_sequence_id_denom_fkey']],
    ),
    em.ForeignKey.define(
        ['alignment_file_id', 'structure_id'],
        'PDB',
        'ihm_external_files', ['id', 'structure_id'],
        constraint_names=[['PDB', 'ihm_starting_comparative_models_alignment_file_id_fk']],
        annotations={
            chaise_tags.foreign_key: {
                'domain_filter_pattern': 'structure_id={{structure_id}}'
            }
        },
        on_update='CASCADE',
        on_delete='SET NULL',
    ),
    em.ForeignKey.define(
        ['Alignment_file_RID', 'alignment_file_id'],
        'PDB',
        'ihm_external_files', ['RID', 'id'],
        constraint_names=[['PDB', 'ihm_starting_comparative_models_alignment_file_id_fkey']],
        annotations={
            chaise_tags.foreign_key: {
                'domain_filter_pattern': 'structure_id={{structure_id}}'
            }
        },
        on_update='CASCADE',
        on_delete='SET NULL',
    ),
    em.ForeignKey.define(
        ['structure_id', 'template_dataset_list_id'],
        'PDB',
        'ihm_dataset_list', ['structure_id', 'id'],
        constraint_names=[['PDB', 'ihm_starting_comparative_models_template_dataset_list_id_fkey']],
        annotations={
            chaise_tags.foreign_key: {
                'domain_filter_pattern': 'structure_id={{structure_id}}'
            }
        },
        on_update='CASCADE',
        on_delete='SET NULL',
    ),
    em.ForeignKey.define(
        ['structure_id', 'starting_model_id'],
        'PDB',
        'ihm_starting_model_details', ['structure_id', 'starting_model_id'],
        constraint_names=[['PDB', 'ihm_starting_comparative_models_starting_model_id_fkey']],
        annotations={
            chaise_tags.foreign_key: {
                'domain_filter_pattern': 'structure_id={{structure_id}}'
            }
        },
        on_update='CASCADE',
        on_delete='SET NULL',
    ),
    em.ForeignKey.define(
        ['RMB'],
        'public',
        'ERMrest_Client', ['ID'],
        constraint_names=[['PDB', 'ihm_starting_comparative_models_RMB_fkey']],
    ),
    em.ForeignKey.define(
        ['RCB'],
        'public',
        'ERMrest_Client', ['ID'],
        constraint_names=[['PDB', 'ihm_starting_comparative_models_RCB_fkey']],
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
