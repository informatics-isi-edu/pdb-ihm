import argparse
from deriva.core import ErmrestCatalog, AttrDict, get_credential
import deriva.core.ermrest_model as em
from deriva.core.ermrest_config import tag as chaise_tags
from deriva.utils.catalog.manage.update_catalog import CatalogUpdater, parse_args

groups = {}

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
    em.Column.define('Binding_partner_asym_RID', em.builtin_types['text'],
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

table_acls = {}

table_acl_bindings = {}

key_defs = [
    em.Key.define(
        ['structure_id', 'ordinal_id'],
        constraint_names=[['PDB', 'ihm_interface_residue_feature_primary_key']],
    ),
    em.Key.define(['RID'], constraint_names=[['PDB', 'ihm_interface_residue_feature_RIDkey1']],
                  ),
]

fkey_defs = [
    em.ForeignKey.define(
        ['structure_id', 'binding_partner_asym_id'],
        'PDB',
        'struct_asym', ['structure_id', 'id'],
        constraint_names=[['PDB', 'ihm_interface_residue_feature_binding_partner_asym_id_fk']],
        annotations={
            chaise_tags.foreign_key: {
                'domain_filter_pattern': 'structure_id={{structure_id}}'
            }
        },
        on_update='CASCADE',
        on_delete='SET NULL',
    ),
    em.ForeignKey.define(
        ['Binding_partner_asym_RID', 'binding_partner_asym_id'],
        'PDB',
        'struct_asym', ['RID', 'id'],
        constraint_names=[['PDB', 'ihm_interface_residue_feature_binding_partner_asym_id_fkey']],
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
        constraint_names=[['PDB', 'ihm_interface_residue_feature_RMB_fkey']],
    ),
    em.ForeignKey.define(
        ['RCB'],
        'public',
        'ERMrest_Client', ['ID'],
        constraint_names=[['PDB', 'ihm_interface_residue_feature_RCB_fkey']],
    ),
    em.ForeignKey.define(
        ['structure_id', 'binding_partner_entity_id'],
        'PDB',
        'entity', ['structure_id', 'id'],
        constraint_names=[['PDB', 'ihm_interface_residue_feature_binding_partner_entity_id_fkey']],
        annotations={
            chaise_tags.foreign_key: {
                'domain_filter_pattern': 'structure_id={{structure_id}}'
            }
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
        on_update='CASCADE',
        on_delete='SET NULL',
    ),
    em.ForeignKey.define(
        ['structure_id', 'feature_id'],
        'PDB',
        'ihm_feature_list', ['structure_id', 'feature_id'],
        constraint_names=[['PDB', 'ihm_interface_residue_feature_feature_id_fkey']],
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
