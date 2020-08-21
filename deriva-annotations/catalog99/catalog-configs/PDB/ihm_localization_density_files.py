import argparse
from deriva.core import ErmrestCatalog, AttrDict, get_credential
import deriva.core.ermrest_model as em
from deriva.core.ermrest_config import tag as chaise_tags
from deriva.utils.catalog.manage.update_catalog import CatalogUpdater, parse_args

groups = {}

table_name = 'ihm_localization_density_files'

schema_name = 'PDB'

column_annotations = {
    'structure_id': {},
    'asym_id': {},
    'ensemble_id': {},
    'entity_id': {},
    'entity_poly_segment_id': {},
    'file_id': {},
    'id': {},
    'Owner': {}
}

column_comment = {
    'structure_id': 'A reference to table entry.id.',
    'asym_id': 'A reference to table struct_asym.id.',
    'ensemble_id': 'A reference to table ihm_ensemble_info.ensemble_id.',
    'entity_id': 'A reference to table entity.id.',
    'entity_poly_segment_id': 'A reference to table ihm_entity_poly_segment.id.',
    'file_id': 'A reference to table ihm_external_files.id.',
    'id': 'type:int4\nA unique identifier.',
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
    em.Column.define('asym_id', em.builtin_types['text'], comment=column_comment['asym_id'],
                     ),
    em.Column.define(
        'ensemble_id',
        em.builtin_types['int4'],
        nullok=False,
        comment=column_comment['ensemble_id'],
    ),
    em.Column.define('entity_id', em.builtin_types['text'], comment=column_comment['entity_id'],
                     ),
    em.Column.define(
        'entity_poly_segment_id',
        em.builtin_types['int4'],
        comment=column_comment['entity_poly_segment_id'],
    ),
    em.Column.define(
        'file_id', em.builtin_types['int4'], nullok=False, comment=column_comment['file_id'],
    ),
    em.Column.define('id', em.builtin_types['int4'], nullok=False, comment=column_comment['id'],
                     ),
    em.Column.define('Owner', em.builtin_types['text'], comment=column_comment['Owner'],
                     ),
    em.Column.define('Asym_RID', em.builtin_types['text'],
                     ),
    em.Column.define('Entity_poly_segment_RID', em.builtin_types['text'],
                     ),
    em.Column.define('Entity_RID', em.builtin_types['text'],
                     ),
]

visible_columns = {
    '*': [
        'RID', {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_localization_density_files_structure_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table entry.id.',
            'markdown_name': 'structure id'
        }, 'id', {
            'source': [{
                'outbound': ['PDB', 'ihm_localization_density_files_file_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table ihm_external_files.id.',
            'markdown_name': 'file id'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_localization_density_files_ensemble_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table ihm_ensemble_info.ensemble_id.',
            'markdown_name': 'ensemble id'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_localization_density_files_entity_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table entity.id.',
            'markdown_name': 'entity id'
        }, {
            'source': [{
                'outbound': ['PDB', 'ihm_localization_density_files_asym_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table struct_asym.id.',
            'markdown_name': 'asym id'
        }, {
            'source': [
                {
                    'outbound': [
                        'PDB', 'ihm_localization_density_files_entity_poly_segment_id_fkey'
                    ]
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
                    'outbound': ['PDB', 'ihm_localization_density_files_structure_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table entry.id.',
            'markdown_name': 'structure id'
        }, 'id', {
            'source': [{
                'outbound': ['PDB', 'ihm_localization_density_files_file_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table ihm_external_files.id.',
            'markdown_name': 'file id'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_localization_density_files_ensemble_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table ihm_ensemble_info.ensemble_id.',
            'markdown_name': 'ensemble id'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_localization_density_files_entity_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table entity.id.',
            'markdown_name': 'entity id'
        }, {
            'source': [{
                'outbound': ['PDB', 'ihm_localization_density_files_asym_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table struct_asym.id.',
            'markdown_name': 'asym id'
        }, {
            'source': [
                {
                    'outbound': [
                        'PDB', 'ihm_localization_density_files_entity_poly_segment_id_fkey'
                    ]
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
                    'outbound': ['PDB', 'ihm_localization_density_files_structure_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table entry.id.',
            'markdown_name': 'structure id'
        }, 'id', {
            'source': [{
                'outbound': ['PDB', 'ihm_localization_density_files_file_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table ihm_external_files.id.',
            'markdown_name': 'file id'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_localization_density_files_ensemble_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table ihm_ensemble_info.ensemble_id.',
            'markdown_name': 'ensemble id'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_localization_density_files_entity_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table entity.id.',
            'markdown_name': 'entity id'
        }, {
            'source': [{
                'outbound': ['PDB', 'ihm_localization_density_files_asym_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table struct_asym.id.',
            'markdown_name': 'asym id'
        }, {
            'source': [
                {
                    'outbound': [
                        'PDB', 'ihm_localization_density_files_entity_poly_segment_id_fkey'
                    ]
                }, 'RID'
            ],
            'comment': 'A reference to table ihm_entity_poly_segment.id.',
            'markdown_name': 'entity poly segment id'
        }, ['PDB', 'ihm_localization_density_files_RCB_fkey'],
        ['PDB', 'ihm_localization_density_files_RMB_fkey'], 'RCT', 'RMT',
        ['PDB', 'ihm_localization_density_files_Owner_fkey']
    ]
}

table_annotations = {chaise_tags.visible_columns: visible_columns, }

table_comment = 'Details of external files that provide information regarding localization densities of ensembles'

table_acls = {}

table_acl_bindings = {}

key_defs = [
    em.Key.define(
        ['structure_id', 'id'],
        constraint_names=[['PDB', 'ihm_localization_density_files_primary_key']],
    ),
    em.Key.define(['RID'], constraint_names=[['PDB', 'ihm_localization_density_files_RIDkey1']],
                  ),
]

fkey_defs = [
    em.ForeignKey.define(
        ['RMB'],
        'public',
        'ERMrest_Client', ['ID'],
        constraint_names=[['PDB', 'ihm_localization_density_files_RMB_fkey']],
    ),
    em.ForeignKey.define(
        ['RCB'],
        'public',
        'ERMrest_Client', ['ID'],
        constraint_names=[['PDB', 'ihm_localization_density_files_RCB_fkey']],
    ),
    em.ForeignKey.define(
        ['structure_id', 'ensemble_id'],
        'PDB',
        'ihm_ensemble_info', ['structure_id', 'ensemble_id'],
        constraint_names=[['PDB', 'ihm_localization_density_files_ensemble_id_fkey']],
        annotations={
            chaise_tags.foreign_key: {
                'domain_filter_pattern': 'structure_id={{structure_id}}'
            }
        },
        on_update='CASCADE',
        on_delete='SET NULL',
    ),
    em.ForeignKey.define(
        ['structure_id', 'file_id'],
        'PDB',
        'ihm_external_files', ['structure_id', 'id'],
        constraint_names=[['PDB', 'ihm_localization_density_files_file_id_fkey']],
        annotations={
            chaise_tags.foreign_key: {
                'domain_filter_pattern': 'structure_id={{structure_id}}'
            }
        },
        on_update='CASCADE',
        on_delete='SET NULL',
    ),
    em.ForeignKey.define(
        ['structure_id', 'asym_id'],
        'PDB',
        'struct_asym', ['structure_id', 'id'],
        constraint_names=[['PDB', 'ihm_localization_density_files_asym_id_fk']],
        annotations={
            chaise_tags.foreign_key: {
                'domain_filter_pattern': 'structure_id={{structure_id}}'
            }
        },
        on_update='CASCADE',
        on_delete='SET NULL',
    ),
    em.ForeignKey.define(
        ['asym_id', 'Asym_RID'],
        'PDB',
        'struct_asym', ['id', 'RID'],
        constraint_names=[['PDB', 'ihm_localization_density_files_asym_id_fkey']],
        annotations={
            chaise_tags.foreign_key: {
                'domain_filter_pattern': 'structure_id={{structure_id}}'
            }
        },
        on_update='CASCADE',
        on_delete='SET NULL',
    ),
    em.ForeignKey.define(
        ['entity_poly_segment_id', 'structure_id'],
        'PDB',
        'ihm_entity_poly_segment', ['id', 'structure_id'],
        constraint_names=[['PDB', 'ihm_localization_density_files_entity_poly_segment_id_fk']],
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
        constraint_names=[['PDB', 'ihm_localization_density_files_entity_poly_segment_id_fkey']],
        annotations={
            chaise_tags.foreign_key: {
                'domain_filter_pattern': 'structure_id={{structure_id}}'
            }
        },
        on_update='CASCADE',
        on_delete='SET NULL',
    ),
    em.ForeignKey.define(
        ['entity_id', 'structure_id'],
        'PDB',
        'entity', ['id', 'structure_id'],
        constraint_names=[['PDB', 'ihm_localization_density_files_entity_id_fk']],
        annotations={
            chaise_tags.foreign_key: {
                'domain_filter_pattern': 'structure_id={{structure_id}}'
            }
        },
        on_update='CASCADE',
        on_delete='SET NULL',
    ),
    em.ForeignKey.define(
        ['entity_id', 'Entity_RID'],
        'PDB',
        'entity', ['id', 'RID'],
        constraint_names=[['PDB', 'ihm_localization_density_files_entity_id_fkey']],
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
