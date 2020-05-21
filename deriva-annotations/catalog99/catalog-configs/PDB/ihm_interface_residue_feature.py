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

table_name = 'ihm_interface_residue_feature'

schema_name = 'PDB'

column_annotations = {
    'structure_id': {},
    'binding_partner_asym_id': {},
    'binding_partner_entity_id': {},
    'dataset_list_id': {},
    'details': {},
    'feature_id': {},
    'ordinal_id': {},
    'Owner': {}
}

column_comment = {
    'structure_id': 'A reference to table entry.id.',
    'binding_partner_asym_id': 'A reference to table struct_asym.id.',
    'binding_partner_entity_id': 'A reference to table entity.id.',
    'dataset_list_id': 'A reference to table ihm_dataset_list.id.',
    'details': 'type:text\nAdditional details regarding the interface residue.',
    'feature_id': 'A reference to table ihm_feature_list.feature_id.',
    'ordinal_id': 'type:int4\nA unique identifier for the category.',
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
        'binding_partner_asym_id',
        em.builtin_types['text'],
        comment=column_comment['binding_partner_asym_id'],
    ),
    em.Column.define(
        'binding_partner_entity_id',
        em.builtin_types['text'],
        nullok=False,
        comment=column_comment['binding_partner_entity_id'],
    ),
    em.Column.define(
        'dataset_list_id', em.builtin_types['int4'], comment=column_comment['dataset_list_id'],
    ),
    em.Column.define('details', em.builtin_types['text'], comment=column_comment['details'],
                     ),
    em.Column.define(
        'feature_id',
        em.builtin_types['int4'],
        nullok=False,
        comment=column_comment['feature_id'],
    ),
    em.Column.define(
        'ordinal_id',
        em.builtin_types['int4'],
        nullok=False,
        comment=column_comment['ordinal_id'],
    ),
    em.Column.define('Owner', em.builtin_types['text'], comment=column_comment['Owner'],
                     ),
    em.Column.define('Entry_Related_File', em.builtin_types['text'],
                     ),
]

visible_columns = {
    '*': [
        'RID', {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_interface_residue_feature_structure_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table entry.id.',
            'markdown_name': 'structure id'
        }, 'ordinal_id', {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_interface_residue_feature_feature_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table ihm_feature_list.feature_id.',
            'markdown_name': 'feature id'
        }, {
            'source': [
                {
                    'outbound': [
                        'PDB', 'ihm_interface_residue_feature_binding_partner_entity_id_fkey'
                    ]
                }, 'RID'
            ],
            'comment': 'A reference to table entity.id.',
            'markdown_name': 'binding partner entity id'
        }, {
            'source': [
                {
                    'outbound': [
                        'PDB', 'ihm_interface_residue_feature_binding_partner_asym_id_fkey'
                    ]
                }, 'RID'
            ],
            'comment': 'A reference to table struct_asym.id.',
            'markdown_name': 'binding partner asym id'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_interface_residue_feature_dataset_list_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table ihm_dataset_list.id.',
            'markdown_name': 'dataset list id'
        }, 'details', ['PDB', 'ihm_interface_residue_feature_Entry_Related_File_fkey']
    ],
    'entry': [
        {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_interface_residue_feature_structure_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table entry.id.',
            'markdown_name': 'structure id'
        }, 'ordinal_id', {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_interface_residue_feature_feature_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table ihm_feature_list.feature_id.',
            'markdown_name': 'feature id'
        }, {
            'source': [
                {
                    'outbound': [
                        'PDB', 'ihm_interface_residue_feature_binding_partner_entity_id_fkey'
                    ]
                }, 'RID'
            ],
            'comment': 'A reference to table entity.id.',
            'markdown_name': 'binding partner entity id'
        }, {
            'source': [
                {
                    'outbound': [
                        'PDB', 'ihm_interface_residue_feature_binding_partner_asym_id_fkey'
                    ]
                }, 'RID'
            ],
            'comment': 'A reference to table struct_asym.id.',
            'markdown_name': 'binding partner asym id'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_interface_residue_feature_dataset_list_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table ihm_dataset_list.id.',
            'markdown_name': 'dataset list id'
        }, 'details'
    ],
    'detailed': [
        'RID', {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_interface_residue_feature_structure_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table entry.id.',
            'markdown_name': 'structure id'
        }, 'ordinal_id', {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_interface_residue_feature_feature_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table ihm_feature_list.feature_id.',
            'markdown_name': 'feature id'
        }, {
            'source': [
                {
                    'outbound': [
                        'PDB', 'ihm_interface_residue_feature_binding_partner_entity_id_fkey'
                    ]
                }, 'RID'
            ],
            'comment': 'A reference to table entity.id.',
            'markdown_name': 'binding partner entity id'
        }, {
            'source': [
                {
                    'outbound': [
                        'PDB', 'ihm_interface_residue_feature_binding_partner_asym_id_fkey'
                    ]
                }, 'RID'
            ],
            'comment': 'A reference to table struct_asym.id.',
            'markdown_name': 'binding partner asym id'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_interface_residue_feature_dataset_list_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table ihm_dataset_list.id.',
            'markdown_name': 'dataset list id'
        }, 'details', ['PDB', 'ihm_interface_residue_feature_Entry_Related_File_fkey'],
        ['PDB', 'ihm_interface_residue_feature_RCB_fkey'],
        ['PDB', 'ihm_interface_residue_feature_RMB_fkey'], 'RCT', 'RMT',
        ['PDB', 'ihm_interface_residue_feature_Owner_fkey']
    ]
}

table_annotations = {chaise_tags.visible_columns: visible_columns, }

table_comment = 'Details of residues at the binding interface'

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
        'projection': [
            {
                'outbound': ['PDB', 'ihm_interface_residue_feature_structure_id_fkey']
            }, {
                'outbound': ['PDB', 'entry_workflow_status_fkey']
            }, {
                'filter': 'Name',
                'operand': 'REL',
                'operator': '='
            }, 'RID'
        ],
        'projection_type': 'nonnull'
    },
    'self_service_group': {
        'types': ['update', 'delete'],
        'scope_acl': ['*'],
        'projection': ['Owner'],
        'projection_type': 'acl'
    },
    'self_service_creator': {
        'types': ['update', 'delete'],
        'scope_acl': [groups['pdb-submitter']],
        'projection': [
            {
                'outbound': ['PDB', 'ihm_interface_residue_feature_structure_id_fkey']
            }, {
                'outbound': ['PDB', 'entry_workflow_status_fkey']
            }, {
                'or': [
                    {
                        'filter': 'Name',
                        'operand': 'DRAFT',
                        'operator': '='
                    }, {
                        'filter': 'Name',
                        'operand': 'DEPO',
                        'operator': '='
                    }
                ]
            }, 'RCB'
        ],
        'projection_type': 'acl'
    }
}

key_defs = [
    em.Key.define(['RID'], constraint_names=[['PDB', 'ihm_interface_residue_feature_RIDkey1']],
                  ),
    em.Key.define(
        ['structure_id', 'ordinal_id'],
        constraint_names=[['PDB', 'ihm_interface_residue_feature_primary_key']],
    ),
]

fkey_defs = [
    em.ForeignKey.define(
        ['RCB'],
        'public',
        'ERMrest_Client', ['ID'],
        constraint_names=[['PDB', 'ihm_interface_residue_feature_RCB_fkey']],
    ),
    em.ForeignKey.define(
        ['RMB'],
        'public',
        'ERMrest_Client', ['ID'],
        constraint_names=[['PDB', 'ihm_interface_residue_feature_RMB_fkey']],
    ),
    em.ForeignKey.define(
        ['Entry_Related_File'],
        'PDB',
        'Entry_Related_File', ['RID'],
        constraint_names=[['PDB', 'ihm_interface_residue_feature_Entry_Related_File_fkey']],
        on_delete='CASCADE',
    ),
    em.ForeignKey.define(
        ['structure_id'],
        'PDB',
        'entry', ['id'],
        constraint_names=[['PDB', 'ihm_interface_residue_feature_structure_id_fkey']],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
        on_update='CASCADE',
        on_delete='SET NULL',
    ),
    em.ForeignKey.define(
        ['Owner'],
        'public',
        'Catalog_Group', ['ID'],
        constraint_names=[['PDB', 'ihm_interface_residue_feature_Owner_fkey']],
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
        ['structure_id', 'binding_partner_asym_id'],
        'PDB',
        'struct_asym', ['structure_id', 'id'],
        constraint_names=[['PDB', 'ihm_interface_residue_feature_binding_partner_asym_id_fkey']],
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
        ['feature_id', 'structure_id'],
        'PDB',
        'ihm_feature_list', ['feature_id', 'structure_id'],
        constraint_names=[['PDB', 'ihm_interface_residue_feature_feature_id_fkey']],
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
        ['binding_partner_entity_id', 'structure_id'],
        'PDB',
        'entity', ['id', 'structure_id'],
        constraint_names=[['PDB', 'ihm_interface_residue_feature_binding_partner_entity_id_fkey']],
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
        ['structure_id', 'dataset_list_id'],
        'PDB',
        'ihm_dataset_list', ['structure_id', 'id'],
        constraint_names=[['PDB', 'ihm_interface_residue_feature_dataset_list_id_fkey']],
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