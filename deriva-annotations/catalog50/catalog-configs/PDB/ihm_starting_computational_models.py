import argparse
from deriva.core import ErmrestCatalog, AttrDict, get_credential
import deriva.core.ermrest_model as em
from deriva.core.ermrest_config import tag as chaise_tags
from deriva.utils.catalog.manage.update_catalog import CatalogUpdater, parse_args

groups = {}

table_name = 'ihm_starting_computational_models'

schema_name = 'PDB'

column_annotations = {
    'structure_id': {},
    'script_file_id': {},
    'software_id': {},
    'starting_model_id': {},
    'Owner': {}
}

column_comment = {
    'structure_id': 'A reference to table entry.id.',
    'script_file_id': 'A reference to table ihm_external_files.id.',
    'software_id': 'A reference to table software.pdbx_ordinal.',
    'starting_model_id': 'A reference to table ihm_starting_model_details.starting_model_id.',
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
        'script_file_id', em.builtin_types['int4'], comment=column_comment['script_file_id'],
    ),
    em.Column.define(
        'software_id', em.builtin_types['int4'], comment=column_comment['software_id'],
    ),
    em.Column.define(
        'starting_model_id',
        em.builtin_types['text'],
        nullok=False,
        comment=column_comment['starting_model_id'],
    ),
    em.Column.define('Owner', em.builtin_types['text'], comment=column_comment['Owner'],
                     ),
]

visible_columns = {
    '*': [
        'RID', {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_starting_computational_models_structure_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table entry.id.',
            'markdown_name': 'structure id'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_starting_computational_models_starting_model_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table ihm_starting_model_details.starting_model_id.',
            'markdown_name': 'starting model id'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_starting_computational_models_script_file_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table ihm_external_files.id.',
            'markdown_name': 'script file id'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_starting_computational_models_software_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table software.pdbx_ordinal.',
            'markdown_name': 'software id'
        }
    ],
    'entry': [
        {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_starting_computational_models_structure_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table entry.id.',
            'markdown_name': 'structure id'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_starting_computational_models_starting_model_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table ihm_starting_model_details.starting_model_id.',
            'markdown_name': 'starting model id'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_starting_computational_models_script_file_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table ihm_external_files.id.',
            'markdown_name': 'script file id'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_starting_computational_models_software_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table software.pdbx_ordinal.',
            'markdown_name': 'software id'
        }
    ],
    'detailed': [
        'RID', {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_starting_computational_models_structure_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table entry.id.',
            'markdown_name': 'structure id'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_starting_computational_models_starting_model_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table ihm_starting_model_details.starting_model_id.',
            'markdown_name': 'starting model id'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_starting_computational_models_script_file_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table ihm_external_files.id.',
            'markdown_name': 'script file id'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_starting_computational_models_software_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table software.pdbx_ordinal.',
            'markdown_name': 'software id'
        }, ['PDB', 'ihm_starting_computational_models_RCB_fkey'],
        ['PDB', 'ihm_starting_computational_models_RMB_fkey'], 'RCT', 'RMT',
        ['PDB', 'ihm_starting_computational_models_Owner_fkey']
    ]
}

table_annotations = {chaise_tags.visible_columns: visible_columns, }

table_comment = 'Generic information regarding all computational models used as starting structural models'

table_acls = {}

table_acl_bindings = {}

key_defs = [
    em.Key.define(
        ['RID'], constraint_names=[['PDB', 'ihm_starting_computational_models_RIDkey1']],
    ),
    em.Key.define(
        ['starting_model_id', 'structure_id'],
        constraint_names=[['PDB', 'ihm_starting_computational_models_primary_key']],
    ),
]

fkey_defs = [
    em.ForeignKey.define(
        ['RMB'],
        'public',
        'ERMrest_Client', ['ID'],
        constraint_names=[['PDB', 'ihm_starting_computational_models_RMB_fkey']],
    ),
    em.ForeignKey.define(
        ['structure_id', 'software_id'],
        'PDB',
        'software', ['structure_id', 'pdbx_ordinal'],
        constraint_names=[['PDB', 'ihm_starting_computational_models_software_id_fkey']],
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
        constraint_names=[['PDB', 'ihm_starting_computational_models_starting_model_id_fkey']],
        annotations={
            chaise_tags.foreign_key: {
                'domain_filter_pattern': 'structure_id={{structure_id}}'
            }
        },
        on_update='CASCADE',
        on_delete='SET NULL',
    ),
    em.ForeignKey.define(
        ['RCB'],
        'public',
        'ERMrest_Client', ['ID'],
        constraint_names=[['PDB', 'ihm_starting_computational_models_RCB_fkey']],
    ),
    em.ForeignKey.define(
        ['script_file_id', 'structure_id'],
        'PDB',
        'ihm_external_files', ['id', 'structure_id'],
        constraint_names=[['PDB', 'ihm_starting_computational_models_script_file_id_fkey']],
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
