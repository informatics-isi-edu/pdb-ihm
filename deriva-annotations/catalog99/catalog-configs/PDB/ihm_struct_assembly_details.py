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

table_name = 'ihm_struct_assembly_details'

schema_name = 'PDB'

column_annotations = {
    'structure_id': {},
    'assembly_id': {},
    'asym_id': {},
    'entity_description': {},
    'entity_id': {},
    'entity_poly_segment_id': {},
    'id': {},
    'parent_assembly_id': {},
    'Owner': {}
}

column_comment = {
    'structure_id': 'A reference to table entry.id.',
    'assembly_id': 'A reference to table ihm_struct_assembly.id.',
    'asym_id': 'A reference to table struct_asym.id.',
    'entity_description': 'type:text\nA text description of the molecular entity',
    'entity_id': 'A reference to table entity.id.',
    'entity_poly_segment_id': 'A reference to table ihm_entity_poly_segment.id.',
    'id': 'type:int4\nA unique identifier for the structural assembly description.',
    'parent_assembly_id': 'A reference to table ihm_struct_assembly.id.',
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
        'asym_id', em.builtin_types['text'], nullok=False, comment=column_comment['asym_id'],
    ),
    em.Column.define(
        'entity_description',
        em.builtin_types['text'],
        comment=column_comment['entity_description'],
    ),
    em.Column.define(
        'entity_id', em.builtin_types['text'], nullok=False, comment=column_comment['entity_id'],
    ),
    em.Column.define(
        'entity_poly_segment_id',
        em.builtin_types['int4'],
        comment=column_comment['entity_poly_segment_id'],
    ),
    em.Column.define('id', em.builtin_types['int4'], nullok=False, comment=column_comment['id'],
                     ),
    em.Column.define(
        'parent_assembly_id',
        em.builtin_types['int4'],
        nullok=False,
        comment=column_comment['parent_assembly_id'],
    ),
    em.Column.define('Owner', em.builtin_types['text'], comment=column_comment['Owner'],
                     ),
    em.Column.define('Entity_poly_segment_RID', em.builtin_types['text'],
                     ),
]

display = {'name': 'Details of Structural Assemblies'}

visible_columns = {
    '*': [
        'RID', {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_struct_assembly_details_structure_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table entry.id.',
            'markdown_name': 'structure id'
        }, 'id', {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_struct_assembly_details_assembly_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table ihm_struct_assembly.id.',
            'markdown_name': 'assembly id'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_struct_assembly_details_parent_assembly_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table ihm_struct_assembly.id.',
            'markdown_name': 'parent assembly id'
        }, {
            'source': [{
                'outbound': ['PDB', 'ihm_struct_assembly_details_entity_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table entity.id.',
            'markdown_name': 'entity id'
        }, 'entity_description', {
            'source': [{
                'outbound': ['PDB', 'ihm_struct_assembly_details_asym_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table struct_asym.id.',
            'markdown_name': 'asym id'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_struct_assembly_details_entity_poly_segment_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table ihm_entity_poly_segment.id.',
            'markdown_name': 'entity poly segment id'
        }
    ],
    'entry': [
        {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_struct_assembly_details_structure_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table entry.id.',
            'markdown_name': 'structure id'
        }, 'id', {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_struct_assembly_details_assembly_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table ihm_struct_assembly.id.',
            'markdown_name': 'assembly id'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_struct_assembly_details_parent_assembly_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table ihm_struct_assembly.id.',
            'markdown_name': 'parent assembly id'
        }, {
            'source': [{
                'outbound': ['PDB', 'ihm_struct_assembly_details_entity_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table entity.id.',
            'markdown_name': 'entity id'
        }, 'entity_description', {
            'source': [{
                'outbound': ['PDB', 'ihm_struct_assembly_details_asym_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table struct_asym.id.',
            'markdown_name': 'asym id'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_struct_assembly_details_entity_poly_segment_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table ihm_entity_poly_segment.id.',
            'markdown_name': 'entity poly segment id'
        }
    ],
    'detailed': [
        'RID', {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_struct_assembly_details_structure_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table entry.id.',
            'markdown_name': 'structure id'
        }, 'id', {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_struct_assembly_details_assembly_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table ihm_struct_assembly.id.',
            'markdown_name': 'assembly id'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_struct_assembly_details_parent_assembly_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table ihm_struct_assembly.id.',
            'markdown_name': 'parent assembly id'
        }, {
            'source': [{
                'outbound': ['PDB', 'ihm_struct_assembly_details_entity_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table entity.id.',
            'markdown_name': 'entity id'
        }, 'entity_description', {
            'source': [{
                'outbound': ['PDB', 'ihm_struct_assembly_details_asym_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table struct_asym.id.',
            'markdown_name': 'asym id'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_struct_assembly_details_entity_poly_segment_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table ihm_entity_poly_segment.id.',
            'markdown_name': 'entity poly segment id'
        }, ['PDB', 'ihm_struct_assembly_details_RCB_fkey'],
        ['PDB', 'ihm_struct_assembly_details_RMB_fkey'], 'RCT', 'RMT',
        ['PDB', 'ihm_struct_assembly_details_Owner_fkey']
    ]
}

table_annotations = {chaise_tags.display: display, chaise_tags.visible_columns: visible_columns, }

table_comment = 'Details of structural assemblies in the models submitted'

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
                'outbound': ['PDB', 'ihm_struct_assembly_details_structure_id_fkey']
            }, 'RCB'
        ],
        'projection_type': 'acl'
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
                'outbound': ['PDB', 'ihm_struct_assembly_details_structure_id_fkey']
            }, {
                'or': [
                    {
                        'filter': 'Workflow_Status',
                        'operand': 'DRAFT',
                        'operator': '='
                    }, {
                        'filter': 'Workflow_Status',
                        'operand': 'DEPO',
                        'operator': '='
                    }, {
                        'filter': 'Workflow_Status',
                        'operand': 'RECORD READY',
                        'operator': '='
                    }, {
                        'filter': 'Workflow_Status',
                        'operand': 'ERROR',
                        'operator': '='
                    }
                ]
            }, 'RCB'
        ],
        'projection_type': 'acl'
    }
}

key_defs = [
    em.Key.define(
        ['id', 'structure_id'],
        constraint_names=[['PDB', 'ihm_struct_assembly_details_primary_key']],
    ),
    em.Key.define(['RID'], constraint_names=[['PDB', 'ihm_struct_assembly_details_RIDkey1']],
                  ),
]

fkey_defs = [
    em.ForeignKey.define(
        ['RCB'],
        'public',
        'ERMrest_Client', ['ID'],
        constraint_names=[['PDB', 'ihm_struct_assembly_details_RCB_fkey']],
    ),
    em.ForeignKey.define(
        ['RMB'],
        'public',
        'ERMrest_Client', ['ID'],
        constraint_names=[['PDB', 'ihm_struct_assembly_details_RMB_fkey']],
    ),
    em.ForeignKey.define(
        ['structure_id'],
        'PDB',
        'entry', ['id'],
        constraint_names=[['PDB', 'ihm_struct_assembly_details_structure_id_fkey']],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
        on_update='CASCADE',
        on_delete='CASCADE',
    ),
    em.ForeignKey.define(
        ['entity_id', 'structure_id'],
        'PDB',
        'entity', ['id', 'structure_id'],
        constraint_names=[['PDB', 'ihm_struct_assembly_details_entity_id_fkey']],
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
        ['structure_id', 'asym_id'],
        'PDB',
        'struct_asym', ['structure_id', 'id'],
        constraint_names=[['PDB', 'ihm_struct_assembly_details_asym_id_fkey']],
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
        ['structure_id', 'parent_assembly_id'],
        'PDB',
        'ihm_struct_assembly', ['structure_id', 'id'],
        constraint_names=[['PDB', 'ihm_struct_assembly_details_parent_assembly_id_fkey']],
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
        ['structure_id', 'assembly_id'],
        'PDB',
        'ihm_struct_assembly', ['structure_id', 'id'],
        constraint_names=[['PDB', 'ihm_struct_assembly_details_assembly_id_fkey']],
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
        constraint_names=[['PDB', 'ihm_struct_assembly_details_Owner_fkey']],
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
        ['entity_poly_segment_id', 'structure_id'],
        'PDB',
        'ihm_entity_poly_segment', ['id', 'structure_id'],
        constraint_names=[['PDB', 'ihm_struct_assembly_details_entity_poly_segment_id_fk']],
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
        ['entity_poly_segment_id', 'Entity_poly_segment_RID'],
        'PDB',
        'ihm_entity_poly_segment', ['id', 'RID'],
        constraint_names=[['PDB', 'ihm_struct_assembly_details_entity_poly_segment_id_fkey']],
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
