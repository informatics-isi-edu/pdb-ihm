import argparse
from deriva.core import ErmrestCatalog, AttrDict, get_credential
import deriva.core.ermrest_model as em
from deriva.core.ermrest_config import tag as chaise_tags
from deriva.utils.catalog.manage.update_catalog import CatalogUpdater, parse_args

groups = {}

table_name = 'ihm_model_representation_details'

schema_name = 'PDB'

column_annotations = {
    'structure_id': {},
    'description': {},
    'entity_asym_id': {},
    'entity_description': {},
    'entity_id': {},
    'entity_poly_segment_id': {},
    'id': {},
    'model_granularity': {},
    'model_mode': {},
    'model_object_count': {},
    'model_object_primitive': {},
    'representation_id': {},
    'starting_model_id': {},
    'Owner': {}
}

column_comment = {
    'structure_id': 'A reference to table entry.id.',
    'description': 'type:text\nAdditional description regarding the model representation.',
    'entity_asym_id': 'A reference to table struct_asym.id.',
    'entity_description': 'type:text\nA text description of the molecular entity',
    'entity_id': 'A reference to table entity.id.',
    'entity_poly_segment_id': 'A reference to table ihm_entity_poly_segment.id.',
    'id': 'type:int4\nA unique identifier for the category.',
    'model_granularity': 'type:text\nThe level of detail at which model primitive objects are applied to the structure.',
    'model_mode': 'type:text\nThe manner in which the segment is modeled.',
    'model_object_count': "type:int4\nThe number of primitive objects used to model a feature in the case of 'by-feature' granularity.",
    'model_object_primitive': 'type:text\nThe primitive object used to model this segment.',
    'representation_id': 'A reference to table ihm_model_representation.id.',
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
        'description', em.builtin_types['text'], comment=column_comment['description'],
    ),
    em.Column.define(
        'entity_asym_id',
        em.builtin_types['text'],
        nullok=False,
        comment=column_comment['entity_asym_id'],
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
        'model_granularity',
        em.builtin_types['text'],
        comment=column_comment['model_granularity'],
    ),
    em.Column.define(
        'model_mode', em.builtin_types['text'], comment=column_comment['model_mode'],
    ),
    em.Column.define(
        'model_object_count',
        em.builtin_types['int4'],
        comment=column_comment['model_object_count'],
    ),
    em.Column.define(
        'model_object_primitive',
        em.builtin_types['text'],
        comment=column_comment['model_object_primitive'],
    ),
    em.Column.define(
        'representation_id',
        em.builtin_types['int4'],
        nullok=False,
        comment=column_comment['representation_id'],
    ),
    em.Column.define(
        'starting_model_id',
        em.builtin_types['text'],
        comment=column_comment['starting_model_id'],
    ),
    em.Column.define('Owner', em.builtin_types['text'], comment=column_comment['Owner'],
                     ),
    em.Column.define('Starting_model_RID', em.builtin_types['text'],
                     ),
    em.Column.define('Entity_poly_segment_RID', em.builtin_types['text'],
                     ),
]

visible_columns = {
    '*': [
        'RID', {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_model_representation_details_structure_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table entry.id.',
            'markdown_name': 'structure id'
        }, 'id', {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_model_representation_details_representation_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table ihm_model_representation.id.',
            'markdown_name': 'representation id'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_model_representation_details_entity_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table entity.id.',
            'markdown_name': 'entity id'
        }, 'entity_description', {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_model_representation_details_entity_asym_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table struct_asym.id.',
            'markdown_name': 'entity asym id'
        }, {
            'source': [
                {
                    'outbound': [
                        'PDB', 'ihm_model_representation_details_entity_poly_segment_id_fkey'
                    ]
                }, 'RID'
            ],
            'comment': 'A reference to table ihm_entity_poly_segment.id.',
            'markdown_name': 'entity poly segment id'
        }, ['PDB', 'ihm_model_representation_details_model_granularity_fkey'],
        ['PDB', 'ihm_model_representation_details_model_mode_fkey'], 'model_object_count',
        ['PDB', 'model_representation_details_model_object_primitive_fkey'], {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_model_representation_details_starting_model_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table ihm_starting_model_details.starting_model_id.',
            'markdown_name': 'starting model id'
        }, 'description'
    ],
    'entry': [
        {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_model_representation_details_structure_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table entry.id.',
            'markdown_name': 'structure id'
        }, 'id', {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_model_representation_details_representation_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table ihm_model_representation.id.',
            'markdown_name': 'representation id'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_model_representation_details_entity_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table entity.id.',
            'markdown_name': 'entity id'
        }, 'entity_description', {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_model_representation_details_entity_asym_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table struct_asym.id.',
            'markdown_name': 'entity asym id'
        }, {
            'source': [
                {
                    'outbound': [
                        'PDB', 'ihm_model_representation_details_entity_poly_segment_id_fkey'
                    ]
                }, 'RID'
            ],
            'comment': 'A reference to table ihm_entity_poly_segment.id.',
            'markdown_name': 'entity poly segment id'
        }, ['PDB', 'ihm_model_representation_details_model_granularity_fkey'],
        ['PDB', 'ihm_model_representation_details_model_mode_fkey'], 'model_object_count',
        ['PDB', 'model_representation_details_model_object_primitive_fkey'], {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_model_representation_details_starting_model_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table ihm_starting_model_details.starting_model_id.',
            'markdown_name': 'starting model id'
        }, 'description'
    ],
    'detailed': [
        'RID', {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_model_representation_details_structure_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table entry.id.',
            'markdown_name': 'structure id'
        }, 'id', {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_model_representation_details_representation_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table ihm_model_representation.id.',
            'markdown_name': 'representation id'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_model_representation_details_entity_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table entity.id.',
            'markdown_name': 'entity id'
        }, 'entity_description', {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_model_representation_details_entity_asym_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table struct_asym.id.',
            'markdown_name': 'entity asym id'
        }, {
            'source': [
                {
                    'outbound': [
                        'PDB', 'ihm_model_representation_details_entity_poly_segment_id_fkey'
                    ]
                }, 'RID'
            ],
            'comment': 'A reference to table ihm_entity_poly_segment.id.',
            'markdown_name': 'entity poly segment id'
        }, ['PDB', 'ihm_model_representation_details_model_granularity_fkey'],
        ['PDB', 'ihm_model_representation_details_model_mode_fkey'], 'model_object_count',
        ['PDB', 'model_representation_details_model_object_primitive_fkey'], {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_model_representation_details_starting_model_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table ihm_starting_model_details.starting_model_id.',
            'markdown_name': 'starting model id'
        }, 'description', ['PDB', 'ihm_model_representation_details_RCB_fkey'],
        ['PDB', 'ihm_model_representation_details_RMB_fkey'], 'RCT', 'RMT',
        ['PDB', 'ihm_model_representation_details_Owner_fkey']
    ]
}

table_annotations = {chaise_tags.visible_columns: visible_columns, }

table_comment = 'Details of model representations used; addresses representations of multi-scale models with atomic and coarse-grained representations'

table_acls = {}

table_acl_bindings = {}

key_defs = [
    em.Key.define(
        ['RID'], constraint_names=[['PDB', 'ihm_model_representation_details_RIDkey1']],
    ),
    em.Key.define(
        ['structure_id', 'id'],
        constraint_names=[['PDB', 'ihm_model_representation_details_primary_key']],
    ),
]

fkey_defs = [
    em.ForeignKey.define(
        ['model_granularity'],
        'Vocab',
        'ihm_model_representation_details_model_granularity', ['Name'],
        constraint_names=[['PDB', 'ihm_model_representation_details_model_granularity_fkey']],
    ),
    em.ForeignKey.define(
        ['model_mode'],
        'Vocab',
        'ihm_model_representation_details_model_mode', ['Name'],
        constraint_names=[['PDB', 'ihm_model_representation_details_model_mode_fkey']],
    ),
    em.ForeignKey.define(
        ['model_object_primitive'],
        'Vocab',
        'model_representation_details_model_object_primitive', ['Name'],
        constraint_names=[['PDB', 'model_representation_details_model_object_primitive_fkey']],
    ),
    em.ForeignKey.define(
        ['structure_id', 'starting_model_id'],
        'PDB',
        'ihm_starting_model_details', ['structure_id', 'starting_model_id'],
        constraint_names=[['PDB', 'ihm_model_representation_details_starting_model_id_fk']],
        annotations={
            chaise_tags.foreign_key: {
                'domain_filter_pattern': 'structure_id={{structure_id}}'
            }
        },
        on_update='CASCADE',
        on_delete='SET NULL',
    ),
    em.ForeignKey.define(
        ['Starting_model_RID', 'starting_model_id'],
        'PDB',
        'ihm_starting_model_details', ['RID', 'starting_model_id'],
        constraint_names=[['PDB', 'ihm_model_representation_details_starting_model_id_fkey']],
        annotations={
            chaise_tags.foreign_key: {
                'domain_filter_pattern': 'structure_id={{structure_id}}'
            }
        },
        on_update='CASCADE',
        on_delete='SET NULL',
    ),
    em.ForeignKey.define(
        ['structure_id', 'entity_poly_segment_id'],
        'PDB',
        'ihm_entity_poly_segment', ['structure_id', 'id'],
        constraint_names=[['PDB', 'ihm_model_representation_details_entity_poly_segment_id_fk']],
        annotations={
            chaise_tags.foreign_key: {
                'domain_filter_pattern': 'structure_id={{structure_id}}'
            }
        },
        on_update='CASCADE',
        on_delete='SET NULL',
    ),
    em.ForeignKey.define(
        ['entity_poly_segment_id', 'Entity_poly_segment_RID'],
        'PDB',
        'ihm_entity_poly_segment', ['id', 'RID'],
        constraint_names=[['PDB', 'ihm_model_representation_details_entity_poly_segment_id_fkey']],
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
        constraint_names=[['PDB', 'ihm_model_representation_details_RMB_fkey']],
    ),
    em.ForeignKey.define(
        ['structure_id', 'representation_id'],
        'PDB',
        'ihm_model_representation', ['structure_id', 'id'],
        constraint_names=[['PDB', 'ihm_model_representation_details_representation_id_fkey']],
        annotations={
            chaise_tags.foreign_key: {
                'domain_filter_pattern': 'structure_id={{structure_id}}'
            }
        },
        on_update='CASCADE',
        on_delete='SET NULL',
    ),
    em.ForeignKey.define(
        ['structure_id', 'entity_id'],
        'PDB',
        'entity', ['structure_id', 'id'],
        constraint_names=[['PDB', 'ihm_model_representation_details_entity_id_fkey']],
        annotations={
            chaise_tags.foreign_key: {
                'domain_filter_pattern': 'structure_id={{structure_id}}'
            }
        },
        on_update='CASCADE',
        on_delete='SET NULL',
    ),
    em.ForeignKey.define(
        ['entity_asym_id', 'structure_id'],
        'PDB',
        'struct_asym', ['id', 'structure_id'],
        constraint_names=[['PDB', 'ihm_model_representation_details_entity_asym_id_fkey']],
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
        constraint_names=[['PDB', 'ihm_model_representation_details_RCB_fkey']],
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
