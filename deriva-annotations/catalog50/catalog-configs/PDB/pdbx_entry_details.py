import argparse
from deriva.core import ErmrestCatalog, AttrDict, get_credential
import deriva.core.ermrest_model as em
from deriva.core.ermrest_config import tag as chaise_tags
from deriva.utils.catalog.manage.update_catalog import CatalogUpdater, parse_args

groups = {}

table_name = 'pdbx_entry_details'

schema_name = 'PDB'

column_annotations = {'structure_id': {}, 'entry_id': {}, 'sequence_details': {}, 'Owner': {}}

column_comment = {
    'structure_id': 'A reference to table entry.id.',
    'entry_id': 'A reference to table entry.id.',
    'sequence_details': 'type:text\nAdditional details about the sequence or sequence database correspondences\n for this entry.',
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
        'entry_id', em.builtin_types['text'], nullok=False, comment=column_comment['entry_id'],
    ),
    em.Column.define(
        'sequence_details', em.builtin_types['text'], comment=column_comment['sequence_details'],
    ),
    em.Column.define('Owner', em.builtin_types['text'], comment=column_comment['Owner'],
                     ),
]

visible_columns = {
    '*': [
        'RID', {
            'source': [{
                'outbound': ['PDB', 'pdbx_entry_details_structure_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table entry.id.',
            'markdown_name': 'structure id'
        }, {
            'source': [{
                'outbound': ['PDB', 'pdbx_entry_details_entry_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table entry.id.',
            'markdown_name': 'entry id'
        }, 'sequence_details'
    ],
    'entry': [
        {
            'source': [{
                'outbound': ['PDB', 'pdbx_entry_details_structure_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table entry.id.',
            'markdown_name': 'structure id'
        }, {
            'source': [{
                'outbound': ['PDB', 'pdbx_entry_details_entry_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table entry.id.',
            'markdown_name': 'entry id'
        }, 'sequence_details'
    ],
    'detailed': [
        'RID', {
            'source': [{
                'outbound': ['PDB', 'pdbx_entry_details_structure_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table entry.id.',
            'markdown_name': 'structure id'
        }, {
            'source': [{
                'outbound': ['PDB', 'pdbx_entry_details_entry_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table entry.id.',
            'markdown_name': 'entry id'
        }, 'sequence_details', ['PDB', 'pdbx_entry_details_RCB_fkey'],
        ['PDB', 'pdbx_entry_details_RMB_fkey'], 'RCT', 'RMT',
        ['PDB', 'pdbx_entry_details_Owner_fkey']
    ]
}

table_annotations = {chaise_tags.visible_columns: visible_columns, }

table_comment = 'Additional details about the entry'

table_acls = {}

table_acl_bindings = {}

key_defs = [
    em.Key.define(
        ['structure_id', 'entry_id'],
        constraint_names=[['PDB', 'pdbx_entry_details_primary_key']],
    ),
    em.Key.define(['RID'], constraint_names=[['PDB', 'pdbx_entry_details_RIDkey1']],
                  ),
]

fkey_defs = [
    em.ForeignKey.define(
        ['RMB'],
        'public',
        'ERMrest_Client', ['ID'],
        constraint_names=[['PDB', 'pdbx_entry_details_RMB_fkey']],
    ),
    em.ForeignKey.define(
        ['RCB'],
        'public',
        'ERMrest_Client', ['ID'],
        constraint_names=[['PDB', 'pdbx_entry_details_RCB_fkey']],
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
