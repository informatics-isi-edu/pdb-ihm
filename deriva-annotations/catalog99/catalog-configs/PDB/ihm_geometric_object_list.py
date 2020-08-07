import argparse
from deriva.core import ErmrestCatalog, AttrDict, get_credential
import deriva.core.ermrest_model as em
from deriva.core.ermrest_config import tag as chaise_tags
from deriva.utils.catalog.manage.update_catalog import CatalogUpdater, parse_args

groups = {}

table_name = 'ihm_geometric_object_list'

schema_name = 'PDB'

column_annotations = {
    'structure_id': {},
    'object_description': {},
    'object_id': {},
    'object_name': {},
    'object_type': {},
    'Owner': {}
}

column_comment = {
    'structure_id': 'A reference to table entry.id.',
    'object_description': 'type:text\nBrief description of the geometric object.\nexamples:Half-torus representing the nuclear membrane',
    'object_id': 'type:int4\nA unique identifier for the geometric object.',
    'object_name': 'type:text\nUser-provided name for the object.\nexamples:Nuclear membrane',
    'object_type': 'type:text\nThe type of geomtric object.',
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
        'object_description',
        em.builtin_types['text'],
        comment=column_comment['object_description'],
    ),
    em.Column.define(
        'object_id', em.builtin_types['int4'], nullok=False, comment=column_comment['object_id'],
    ),
    em.Column.define(
        'object_name', em.builtin_types['text'], comment=column_comment['object_name'],
    ),
    em.Column.define(
        'object_type',
        em.builtin_types['text'],
        nullok=False,
        comment=column_comment['object_type'],
    ),
    em.Column.define('Owner', em.builtin_types['text'], comment=column_comment['Owner'],
                     ),
]

visible_columns = {
    '*': [
        'RID', {
            'source': [{
                'outbound': ['PDB', 'ihm_geometric_object_list_structure_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table entry.id.',
            'markdown_name': 'structure id'
        }, 'object_id', ['PDB', 'ihm_geometric_object_list_object_type_fkey'], 'object_name',
        'object_description'
    ],
    'entry': [
        {
            'source': [{
                'outbound': ['PDB', 'ihm_geometric_object_list_structure_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table entry.id.',
            'markdown_name': 'structure id'
        }, 'object_id', ['PDB', 'ihm_geometric_object_list_object_type_fkey'], 'object_name',
        'object_description'
    ],
    'detailed': [
        'RID', {
            'source': [{
                'outbound': ['PDB', 'ihm_geometric_object_list_structure_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table entry.id.',
            'markdown_name': 'structure id'
        }, 'object_id', ['PDB', 'ihm_geometric_object_list_object_type_fkey'], 'object_name',
        'object_description', ['PDB', 'ihm_geometric_object_list_RCB_fkey'],
        ['PDB', 'ihm_geometric_object_list_RMB_fkey'], 'RCT', 'RMT',
        ['PDB', 'ihm_geometric_object_list_Owner_fkey']
    ]
}

visible_foreign_keys = {
    'filter': 'detailed',
    'detailed': [
        ['PDB', 'ihm_geometric_object_sphere_object_id_fkey'],
        ['PDB', 'ihm_geometric_object_torus_object_id_fkey'],
        ['PDB', 'ihm_geometric_object_axis_object_id_fkey'],
        ['PDB', 'ihm_geometric_object_plane_object_id_fkey'],
        ['PDB', 'ihm_geometric_object_distance_restraint_object_id_fkey']
    ]
}

table_display = {'row_name': {'row_markdown_pattern': '{{{object_id}}}'}}

table_annotations = {
    chaise_tags.table_display: table_display,
    chaise_tags.visible_columns: visible_columns,
    chaise_tags.visible_foreign_keys: visible_foreign_keys,
}

table_comment = 'List of geometric objects used as restraints in modeling'

table_acls = {}

table_acl_bindings = {}

key_defs = [
    em.Key.define(['RID'], constraint_names=[['PDB', 'ihm_geometric_object_list_RIDkey1']],
                  ),
    em.Key.define(
        ['object_id', 'structure_id'],
        constraint_names=[['PDB', 'ihm_geometric_object_list_primary_key']],
    ),
]

fkey_defs = [
    em.ForeignKey.define(
        ['RCB'],
        'public',
        'ERMrest_Client', ['ID'],
        constraint_names=[['PDB', 'ihm_geometric_object_list_RCB_fkey']],
    ),
    em.ForeignKey.define(
        ['RMB'],
        'public',
        'ERMrest_Client', ['ID'],
        constraint_names=[['PDB', 'ihm_geometric_object_list_RMB_fkey']],
    ),
    em.ForeignKey.define(
        ['object_type'],
        'Vocab',
        'ihm_geometric_object_list_object_type', ['Name'],
        constraint_names=[['PDB', 'ihm_geometric_object_list_object_type_fkey']],
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
