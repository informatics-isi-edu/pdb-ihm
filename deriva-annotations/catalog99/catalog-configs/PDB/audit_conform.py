import argparse
from deriva.core import ErmrestCatalog, AttrDict, get_credential
import deriva.core.ermrest_model as em
from deriva.core.ermrest_config import tag as chaise_tags
from deriva.utils.catalog.manage.update_catalog import CatalogUpdater, parse_args

groups = {}

table_name = 'audit_conform'

schema_name = 'PDB'

column_annotations = {
    'structure_id': {},
    'dict_location': {},
    'dict_name': {},
    'dict_version': {},
    'Owner': {}
}

column_comment = {
    'structure_id': 'A reference to table entry.id.',
    'dict_location': 'type:text\nA file name or uniform resource locator (URL) for the\n dictionary to which the current data block conforms.',
    'dict_name': 'type:text\nThe string identifying the highest-level dictionary defining\n data names used in this file.',
    'dict_version': 'type:text\nThe version number of the dictionary to which the current\n data block conforms.',
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
        'dict_location', em.builtin_types['text'], comment=column_comment['dict_location'],
    ),
    em.Column.define(
        'dict_name', em.builtin_types['text'], nullok=False, comment=column_comment['dict_name'],
    ),
    em.Column.define(
        'dict_version',
        em.builtin_types['text'],
        nullok=False,
        comment=column_comment['dict_version'],
    ),
    em.Column.define('Owner', em.builtin_types['text'], comment=column_comment['Owner'],
                     ),
]

visible_columns = {
    '*': [
        'RID', {
            'source': [{
                'outbound': ['PDB', 'audit_conform_structure_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table entry.id.',
            'markdown_name': 'structure id'
        }, 'dict_name', 'dict_location', 'dict_version'
    ],
    'entry': [
        {
            'source': [{
                'outbound': ['PDB', 'audit_conform_structure_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table entry.id.',
            'markdown_name': 'structure id'
        }, 'dict_name', 'dict_location', 'dict_version'
    ],
    'detailed': [
        'RID', {
            'source': [{
                'outbound': ['PDB', 'audit_conform_structure_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table entry.id.',
            'markdown_name': 'structure id'
        }, 'dict_name', 'dict_location', 'dict_version', ['PDB', 'audit_conform_RCB_fkey'],
        ['PDB', 'audit_conform_RMB_fkey'], 'RCT', 'RMT', ['PDB', 'audit_conform_Owner_fkey']
    ]
}

table_annotations = {chaise_tags.visible_columns: visible_columns, }

table_comment = 'Dictionary versions against which the data items in the current data block are conformant'

table_acls = {}

table_acl_bindings = {}

key_defs = [
    em.Key.define(
        ['dict_name', 'structure_id', 'dict_version'],
        constraint_names=[['PDB', 'audit_conform_primary_key']],
    ),
    em.Key.define(['RID'], constraint_names=[['PDB', 'audit_conform_RIDkey1']],
                  ),
]

fkey_defs = [
    em.ForeignKey.define(
        ['RMB'],
        'public',
        'ERMrest_Client', ['ID'],
        constraint_names=[['PDB', 'audit_conform_RMB_fkey']],
    ),
    em.ForeignKey.define(
        ['RCB'],
        'public',
        'ERMrest_Client', ['ID'],
        constraint_names=[['PDB', 'audit_conform_RCB_fkey']],
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
