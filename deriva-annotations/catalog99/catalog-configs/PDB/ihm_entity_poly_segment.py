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

table_name = 'ihm_entity_poly_segment'

schema_name = 'PDB'

column_annotations = {
    'structure_id': {},
    'comp_id_begin': {},
    'comp_id_end': {},
    'entity_id': {},
    'id': {},
    'seq_id_begin': {},
    'seq_id_end': {},
    'Owner': {}
}

column_comment = {
    'structure_id': 'A reference to table entry.id.',
    'comp_id_begin': 'A reference to table chem_comp.id.',
    'comp_id_end': 'A reference to table chem_comp.id.',
    'entity_id': 'A reference to table entity.id.',
    'id': 'type:int4\nA unique identifier for the polymeric segment.',
    'seq_id_begin': 'A reference to table entity_poly_seq.num.',
    'seq_id_end': 'A reference to table entity_poly_seq.num.',
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
        'comp_id_begin',
        em.builtin_types['text'],
        nullok=False,
        comment=column_comment['comp_id_begin'],
    ),
    em.Column.define(
        'comp_id_end',
        em.builtin_types['text'],
        nullok=False,
        comment=column_comment['comp_id_end'],
    ),
    em.Column.define(
        'entity_id', em.builtin_types['text'], nullok=False, comment=column_comment['entity_id'],
    ),
    em.Column.define('id', em.builtin_types['int4'], nullok=False, comment=column_comment['id'],
                     ),
    em.Column.define(
        'seq_id_begin',
        em.builtin_types['int4'],
        nullok=False,
        comment=column_comment['seq_id_begin'],
    ),
    em.Column.define(
        'seq_id_end',
        em.builtin_types['int4'],
        nullok=False,
        comment=column_comment['seq_id_end'],
    ),
    em.Column.define('Owner', em.builtin_types['text'], comment=column_comment['Owner'],
                     ),
    em.Column.define('Entity_Poly_Seq_RID_Begin', em.builtin_types['text'], nullok=False,
                     ),
    em.Column.define('Entity_Poly_Seq_RID_End', em.builtin_types['text'], nullok=False,
                     ),
]

display = {'name': 'Segments of Polymeric Entities'}

visible_columns = {
    '*': [
        {
            'source': 'RID'
        }, {
            'source': [{
                'outbound': ['PDB', 'ihm_entity_poly_segment_structure_id_fkey']
            }, 'RID']
        }, {
            'source': 'id'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_entity_poly_segment_mm_poly_res_label_begin_fkey']
                }, 'entity_id'
            ],
            'markdown_name': 'entity id'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_entity_poly_segment_mm_poly_res_label_begin_fkey']
                }, 'mon_id'
            ],
            'markdown_name': 'comp id begin'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_entity_poly_segment_mm_poly_res_label_end_fkey']
                }, 'mon_id'
            ],
            'markdown_name': 'comp id end'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_entity_poly_segment_mm_poly_res_label_begin_fkey']
                }, 'num'
            ],
            'markdown_name': 'seq id begin'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_entity_poly_segment_mm_poly_res_label_end_fkey']
                }, 'num'
            ],
            'markdown_name': 'seq id end'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_entity_poly_segment_mm_poly_res_label_begin_fkey']
                }, 'RID'
            ],
            'markdown_name': 'polymeric residue begin'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_entity_poly_segment_mm_poly_res_label_end_fkey']
                }, 'RID'
            ],
            'markdown_name': 'polymeric residue end'
        }
    ],
    'entry': [
        {
            'source': [{
                'outbound': ['PDB', 'ihm_entity_poly_segment_structure_id_fkey']
            }, 'RID']
        }, {
            'source': 'id'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_entity_poly_segment_mm_poly_res_label_begin_fkey']
                }, 'entity_id'
            ],
            'markdown_name': 'entity id'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_entity_poly_segment_mm_poly_res_label_begin_fkey']
                }, 'mon_id'
            ],
            'markdown_name': 'comp id begin'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_entity_poly_segment_mm_poly_res_label_end_fkey']
                }, 'mon_id'
            ],
            'markdown_name': 'comp id end'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_entity_poly_segment_mm_poly_res_label_begin_fkey']
                }, 'num'
            ],
            'markdown_name': 'seq id begin'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_entity_poly_segment_mm_poly_res_label_end_fkey']
                }, 'num'
            ],
            'markdown_name': 'seq id end'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_entity_poly_segment_mm_poly_res_label_begin_fkey']
                }, 'RID'
            ],
            'markdown_name': 'polymeric residue begin'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_entity_poly_segment_mm_poly_res_label_end_fkey']
                }, 'RID'
            ],
            'markdown_name': 'polymeric residue end'
        }
    ],
    'detailed': [
        {
            'source': 'RID'
        }, {
            'source': [{
                'outbound': ['PDB', 'ihm_entity_poly_segment_structure_id_fkey']
            }, 'RID']
        }, {
            'source': 'id'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_entity_poly_segment_mm_poly_res_label_begin_fkey']
                }, 'entity_id'
            ],
            'markdown_name': 'entity id'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_entity_poly_segment_mm_poly_res_label_begin_fkey']
                }, 'mon_id'
            ],
            'markdown_name': 'comp id begin'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_entity_poly_segment_mm_poly_res_label_end_fkey']
                }, 'mon_id'
            ],
            'markdown_name': 'comp id end'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_entity_poly_segment_mm_poly_res_label_begin_fkey']
                }, 'num'
            ],
            'markdown_name': 'seq id begin'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_entity_poly_segment_mm_poly_res_label_end_fkey']
                }, 'num'
            ],
            'markdown_name': 'seq id end'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_entity_poly_segment_mm_poly_res_label_begin_fkey']
                }, 'RID'
            ],
            'markdown_name': 'polymeric residue begin'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_entity_poly_segment_mm_poly_res_label_end_fkey']
                }, 'RID'
            ],
            'markdown_name': 'polymeric residue end'
        }, {
            'source': 'RCT'
        }, {
            'source': 'RMT'
        }, {
            'source': [{
                'outbound': ['PDB', 'ihm_entity_poly_segment_RCB_fkey']
            }, 'RID']
        }, {
            'source': [{
                'outbound': ['PDB', 'ihm_entity_poly_segment_RMB_fkey']
            }, 'RID']
        }, {
            'source': [{
                'outbound': ['PDB', 'ihm_entity_poly_segment_Owner_fkey']
            }, 'RID']
        }
    ]
}

visible_foreign_keys = {
    'filter': 'detailed',
    'detailed': [
        ['PDB', 'ihm_model_representation_details_entity_poly_segment_id_fkey'],
        ['PDB', 'ihm_struct_assembly_details_entity_poly_segment_id_fkey'],
        ['PDB', 'ihm_starting_model_details_entity_poly_segment_id_fkey'],
        ['PDB', 'ihm_localization_density_files_entity_poly_segment_id_fkey']
    ]
}

table_display = {'row_name': {'row_markdown_pattern': '{{{id}}}'}}

table_annotations = {
    chaise_tags.display: display,
    chaise_tags.table_display: table_display,
    chaise_tags.visible_columns: visible_columns,
    chaise_tags.visible_foreign_keys: visible_foreign_keys,
}

table_comment = 'Segments of polymeric entities; specifies sequence ranges for use in other tables'

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
        'projection': [{
            'outbound': ['PDB', 'ihm_entity_poly_segment_structure_id_fkey']
        }, 'RCB'],
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
                'outbound': ['PDB', 'ihm_entity_poly_segment_structure_id_fkey']
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
    em.Key.define(['RID'], constraint_names=[['PDB', 'ihm_entity_poly_segment_RIDkey1']],
                  ),
    em.Key.define(
        ['id', 'structure_id'], constraint_names=[['PDB', 'ihm_entity_poly_segment_primary_key']],
    ),
    em.Key.define(
        ['id', 'RID'], constraint_names=[['PDB', 'ihm_entity_poly_segment_RID_id_key']],
    ),
]

fkey_defs = [
    em.ForeignKey.define(
        ['RMB'],
        'public',
        'ERMrest_Client', ['ID'],
        constraint_names=[['PDB', 'ihm_entity_poly_segment_RMB_fkey']],
    ),
    em.ForeignKey.define(
        ['RCB'],
        'public',
        'ERMrest_Client', ['ID'],
        constraint_names=[['PDB', 'ihm_entity_poly_segment_RCB_fkey']],
    ),
    em.ForeignKey.define(
        ['structure_id'],
        'PDB',
        'entry', ['id'],
        constraint_names=[['PDB', 'ihm_entity_poly_segment_structure_id_fkey']],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
        on_update='CASCADE',
        on_delete='CASCADE',
    ),
    em.ForeignKey.define(
        ['Owner'],
        'public',
        'Catalog_Group', ['ID'],
        constraint_names=[['PDB', 'ihm_entity_poly_segment_Owner_fkey']],
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
        ['structure_id', 'Entity_Poly_Seq_RID_Begin', 'seq_id_begin', 'entity_id', 'comp_id_begin'],
        'PDB',
        'entity_poly_seq', ['structure_id', 'RID', 'num', 'entity_id', 'mon_id'],
        constraint_names=[['PDB', 'ihm_entity_poly_segment_mm_poly_res_label_begin_fkey']],
        annotations={
            chaise_tags.foreign_key: {
                'template_engine': 'handlebars',
                'domain_filter_pattern': '{{#if _structure_id}}structure_id={{{_structure_id}}}{{/if}}'
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
        ['Entity_Poly_Seq_RID_End', 'structure_id', 'seq_id_end', 'comp_id_end', 'entity_id'],
        'PDB',
        'entity_poly_seq', ['RID', 'structure_id', 'num', 'mon_id', 'entity_id'],
        constraint_names=[['PDB', 'ihm_entity_poly_segment_mm_poly_res_label_end_fkey']],
        annotations={
            chaise_tags.foreign_key: {
                'template_engine': 'handlebars',
                'domain_filter_pattern': '{{#if _structure_id}}structure_id={{{_structure_id}}}{{/if}}'
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
