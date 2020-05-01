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
    'isrd-staff': 'https://auth.globus.org/176baec4-ed26-11e5-8e88-22000ab4b42b'
}

table_name = 'ihm_geometric_object_plane'

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
    'object_id': {},
    'plane_type': {},
    'transformation_id': {},
    'Owner': {}
}

column_comment = {
    'structure_id': 'A reference to table entry.id.',
    'object_id': 'A reference to table ihm_geometric_object_list.object_id.',
    'plane_type': 'type:text\nThe type of plane.',
    'transformation_id': 'A reference to table ihm_geometric_object_transformation.id.',
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
        'object_id', em.builtin_types['int4'], nullok=False, comment=column_comment['object_id'],
    ),
    em.Column.define(
        'plane_type',
        em.builtin_types['text'],
        nullok=False,
        comment=column_comment['plane_type'],
    ),
    em.Column.define(
        'transformation_id',
        em.builtin_types['int4'],
        comment=column_comment['transformation_id'],
    ),
    em.Column.define('Owner', em.builtin_types['text'], comment=column_comment['Owner'],
                     ),
]

visible_columns = {
    '*': [
        'RID', {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_geometric_object_plane_structure_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table entry.id.',
            'markdown_name': 'structure id'
        }, {
            'source': [{
                'outbound': ['PDB', 'ihm_geometric_object_plane_object_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table ihm_geometric_object_list.object_id.',
            'markdown_name': 'object id'
        }, ['PDB', 'ihm_geometric_object_plane_plane_type_fkey'], {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_geometric_object_plane_transformation_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table ihm_geometric_object_transformation.id.',
            'markdown_name': 'transformation id'
        }
    ],
    'entry': [
        {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_geometric_object_plane_structure_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table entry.id.',
            'markdown_name': 'structure id'
        }, {
            'source': [{
                'outbound': ['PDB', 'ihm_geometric_object_plane_object_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table ihm_geometric_object_list.object_id.',
            'markdown_name': 'object id'
        }, ['PDB', 'ihm_geometric_object_plane_plane_type_fkey'], {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_geometric_object_plane_transformation_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table ihm_geometric_object_transformation.id.',
            'markdown_name': 'transformation id'
        }
    ],
    'detailed': [
        'RID', {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_geometric_object_plane_structure_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table entry.id.',
            'markdown_name': 'structure id'
        }, {
            'source': [{
                'outbound': ['PDB', 'ihm_geometric_object_plane_object_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table ihm_geometric_object_list.object_id.',
            'markdown_name': 'object id'
        }, ['PDB', 'ihm_geometric_object_plane_plane_type_fkey'], {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_geometric_object_plane_transformation_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table ihm_geometric_object_transformation.id.',
            'markdown_name': 'transformation id'
        }, ['PDB', 'ihm_geometric_object_plane_RCB_fkey'],
        ['PDB', 'ihm_geometric_object_plane_RMB_fkey'], 'RCT', 'RMT',
        ['PDB', 'ihm_geometric_object_plane_Owner_fkey']
    ]
}

table_annotations = {chaise_tags.visible_columns: visible_columns, }

table_comment = 'Geomtric object plane'

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
    em.Key.define(['RID'], constraint_names=[['PDB', 'ihm_geometric_object_plane_RIDkey1']],
                  ),
    em.Key.define(
        ['structure_id', 'object_id'],
        constraint_names=[['PDB', 'ihm_geometric_object_plane_primary_key']],
    ),
]

fkey_defs = [
    em.ForeignKey.define(
        ['transformation_id', 'structure_id'],
        'PDB',
        'ihm_geometric_object_transformation', ['id', 'structure_id'],
        constraint_names=[['PDB', 'ihm_geometric_object_plane_transformation_id_fkey']],
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
        ['Owner'],
        'public',
        'Catalog_Group', ['ID'],
        constraint_names=[['PDB', 'ihm_geometric_object_plane_Owner_fkey']],
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
        ['RMB'],
        'public',
        'ERMrest_Client', ['ID'],
        constraint_names=[['PDB', 'ihm_geometric_object_plane_RMB_fkey']],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
    ),
    em.ForeignKey.define(
        ['plane_type'],
        'Vocab',
        'ihm_geometric_object_plane_plane_type', ['ID'],
        constraint_names=[['PDB', 'ihm_geometric_object_plane_plane_type_fkey']],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
    ),
    em.ForeignKey.define(
        ['structure_id'],
        'PDB',
        'entry', ['id'],
        constraint_names=[['PDB', 'ihm_geometric_object_plane_structure_id_fkey']],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
        on_update='CASCADE',
        on_delete='SET NULL',
    ),
    em.ForeignKey.define(
        ['structure_id', 'object_id'],
        'PDB',
        'ihm_geometric_object_list', ['structure_id', 'object_id'],
        constraint_names=[['PDB', 'ihm_geometric_object_plane_object_id_fkey']],
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
        ['RCB'],
        'public',
        'ERMrest_Client', ['ID'],
        constraint_names=[['PDB', 'ihm_geometric_object_plane_RCB_fkey']],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
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
