import argparse
from deriva.core import ErmrestCatalog, AttrDict, get_credential
import deriva.core.ermrest_model as em
from deriva.core.ermrest_config import tag as chaise_tags
from deriva.utils.catalog.manage.update_catalog import CatalogUpdater, parse_args

groups = {}

table_name = 'ihm_struct_assembly_class_link'

schema_name = 'PDB'

column_annotations = {'structure_id': {}, 'assembly_id': {}, 'class_id': {}, 'Owner': {}}

column_comment = {
    'structure_id': 'A reference to table entry.id.',
    'assembly_id': 'A reference to table ihm_struct_assembly.id.',
    'class_id': 'A reference to table ihm_struct_assembly_class.id.',
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
        'assembly_id',
        em.builtin_types['int4'],
        nullok=False,
        comment=column_comment['assembly_id'],
    ),
    em.Column.define(
        'class_id', em.builtin_types['int4'], nullok=False, comment=column_comment['class_id'],
    ),
    em.Column.define('Owner', em.builtin_types['text'], comment=column_comment['Owner'],
                     ),
]

visible_columns = {
    '*': [
        'RID', {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_struct_assembly_class_link_structure_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table entry.id.',
            'markdown_name': 'structure id'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_struct_assembly_class_link_assembly_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table ihm_struct_assembly.id.',
            'markdown_name': 'assembly id'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_struct_assembly_class_link_class_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table ihm_struct_assembly_class.id.',
            'markdown_name': 'class id'
        }
    ],
    'entry': [
        {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_struct_assembly_class_link_structure_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table entry.id.',
            'markdown_name': 'structure id'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_struct_assembly_class_link_assembly_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table ihm_struct_assembly.id.',
            'markdown_name': 'assembly id'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_struct_assembly_class_link_class_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table ihm_struct_assembly_class.id.',
            'markdown_name': 'class id'
        }
    ],
    'detailed': [
        'RID', {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_struct_assembly_class_link_structure_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table entry.id.',
            'markdown_name': 'structure id'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_struct_assembly_class_link_assembly_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table ihm_struct_assembly.id.',
            'markdown_name': 'assembly id'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_struct_assembly_class_link_class_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table ihm_struct_assembly_class.id.',
            'markdown_name': 'class id'
        }, ['PDB', 'ihm_struct_assembly_class_link_RCB_fkey'],
        ['PDB', 'ihm_struct_assembly_class_link_RMB_fkey'], 'RCT', 'RMT',
        ['PDB', 'ihm_struct_assembly_class_link_Owner_fkey']
    ]
}

table_annotations = {chaise_tags.visible_columns: visible_columns, }

table_comment = None

table_acls = {}

table_acl_bindings = {}

key_defs = [
    em.Key.define(
        ['assembly_id', 'class_id', 'structure_id'],
        constraint_names=[['PDB', 'ihm_struct_assembly_class_link_primary_key']],
    ),
    em.Key.define(['RID'], constraint_names=[['PDB', 'ihm_struct_assembly_class_link_RIDkey1']],
                  ),
]

fkey_defs = [
    em.ForeignKey.define(
        ['RCB'],
        'public',
        'ERMrest_Client', ['ID'],
        constraint_names=[['PDB', 'ihm_struct_assembly_class_link_RCB_fkey']],
    ),
    em.ForeignKey.define(
        ['RMB'],
        'public',
        'ERMrest_Client', ['ID'],
        constraint_names=[['PDB', 'ihm_struct_assembly_class_link_RMB_fkey']],
    ),
    em.ForeignKey.define(
        ['class_id', 'structure_id'],
        'PDB',
        'ihm_struct_assembly_class', ['id', 'structure_id'],
        constraint_names=[['PDB', 'ihm_struct_assembly_class_link_class_id_fkey']],
        annotations={
            chaise_tags.foreign_key: {
                'domain_filter_pattern': 'structure_id={{structure_id}}'
            }
        },
        on_update='CASCADE',
        on_delete='SET NULL',
    ),
    em.ForeignKey.define(
        ['structure_id', 'assembly_id'],
        'PDB',
        'ihm_struct_assembly', ['structure_id', 'id'],
        constraint_names=[['PDB', 'ihm_struct_assembly_class_link_assembly_id_fkey']],
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
    catalog_id = 99
    mode, replace, host, catalog_id = parse_args(host, catalog_id, is_table=True)
    catalog = ErmrestCatalog('https', host, catalog_id=catalog_id, credentials=get_credential(host))
    main(catalog, mode, replace)
