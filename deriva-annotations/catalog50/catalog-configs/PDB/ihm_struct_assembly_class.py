import argparse
from deriva.core import ErmrestCatalog, AttrDict, get_credential
import deriva.core.ermrest_model as em
from deriva.core.ermrest_config import tag as chaise_tags
from deriva.utils.catalog.manage.update_catalog import CatalogUpdater, parse_args

groups = {}

table_name = 'ihm_struct_assembly_class'

schema_name = 'PDB'

column_annotations = {
    'structure_id': {},
    'description': {},
    'id': {},
    'name': {},
    'type': {},
    'Owner': {}
}

column_comment = {
    'structure_id': 'A reference to table entry.id.',
    'description': 'type:text\nAdditional description regarding the class.',
    'id': 'type:int4\nA unique identifier for the structural assembly class.',
    'name': 'type:text\nA user provided name for the class.\nexamples:TAD,Chromatin',
    'type': 'type:text\nThe type of classifier.',
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
        'description', em.builtin_types['text'], comment=column_comment['description'],
    ),
    em.Column.define('id', em.builtin_types['int4'], nullok=False, comment=column_comment['id'],
                     ),
    em.Column.define('name', em.builtin_types['text'], comment=column_comment['name'],
                     ),
    em.Column.define('type', em.builtin_types['text'], comment=column_comment['type'],
                     ),
    em.Column.define('Owner', em.builtin_types['text'], comment=column_comment['Owner'],
                     ),
]

visible_columns = {
    '*': [
        'RID', {
            'source': [{
                'outbound': ['PDB', 'ihm_struct_assembly_class_structure_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table entry.id.',
            'markdown_name': 'structure id'
        }, 'id', 'name', ['PDB', 'ihm_struct_assembly_class_type_fkey'], 'description'
    ],
    'entry': [
        {
            'source': [{
                'outbound': ['PDB', 'ihm_struct_assembly_class_structure_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table entry.id.',
            'markdown_name': 'structure id'
        }, 'id', 'name', ['PDB', 'ihm_struct_assembly_class_type_fkey'], 'description'
    ],
    'detailed': [
        'RID', {
            'source': [{
                'outbound': ['PDB', 'ihm_struct_assembly_class_structure_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table entry.id.',
            'markdown_name': 'structure id'
        }, 'id', 'name', ['PDB', 'ihm_struct_assembly_class_type_fkey'], 'description',
        ['PDB', 'ihm_struct_assembly_class_RCB_fkey'],
        ['PDB', 'ihm_struct_assembly_class_RMB_fkey'], 'RCT', 'RMT',
        ['PDB', 'ihm_struct_assembly_class_Owner_fkey']
    ]
}

visible_foreign_keys = {
    'filter': 'detailed',
    'detailed': [['PDB', 'ihm_struct_assembly_class_link_class_id_fkey']]
}

table_display = {'row_name': {'row_markdown_pattern': '{{{id}}}'}}

table_annotations = {
    chaise_tags.table_display: table_display,
    chaise_tags.visible_columns: visible_columns,
    chaise_tags.visible_foreign_keys: visible_foreign_keys,
}

table_comment = 'List of structural assembly classes; allows for defining hierarchical structural assemblies'

table_acls = {}

table_acl_bindings = {}

key_defs = [
    em.Key.define(['RID'], constraint_names=[['PDB', 'ihm_struct_assembly_class_RIDkey1']],
                  ),
    em.Key.define(
        ['structure_id', 'id'],
        constraint_names=[['PDB', 'ihm_struct_assembly_class_primary_key']],
    ),
]

fkey_defs = [
    em.ForeignKey.define(
        ['type'],
        'Vocab',
        'ihm_struct_assembly_class_type', ['Name'],
        constraint_names=[['PDB', 'ihm_struct_assembly_class_type_fkey']],
    ),
    em.ForeignKey.define(
        ['RCB'],
        'public',
        'ERMrest_Client', ['ID'],
        constraint_names=[['PDB', 'ihm_struct_assembly_class_RCB_fkey']],
    ),
    em.ForeignKey.define(
        ['RMB'],
        'public',
        'ERMrest_Client', ['ID'],
        constraint_names=[['PDB', 'ihm_struct_assembly_class_RMB_fkey']],
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