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

table_name = 'ihm_residues_not_modeled'

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
    'asym_id': {},
    'comp_id_begin': {},
    'comp_id_end': {},
    'details': {},
    'entity_description': {},
    'entity_id': {},
    'id': {},
    'model_id': {},
    'reason': {},
    'seq_id_begin': {},
    'seq_id_end': {},
    'Owner': {}
}

column_comment = {
    'structure_id': 'A reference to table entry.id.',
    'asym_id': 'A reference to table struct_asym.id.',
    'comp_id_begin': 'A reference to table entity_poly_seq.mon_id.',
    'comp_id_end': 'A reference to table entity_poly_seq.mon_id.',
    'details': 'type:text\nAdditional details regarding the missing segments.',
    'entity_description': 'type:text\nA text description of the molecular entity, whose residues are not modeled. \n This data item is a pointer to _entity.pdbx_description in the ENTITY category.',
    'entity_id': 'A reference to table entity_poly_seq.entity_id.',
    'id': 'type:int4\nA unique identifier for the category.',
    'model_id': 'A reference to table ihm_model_list.model_id.',
    'reason': 'type:text\nThe reason why the residues are missing in the structural model.',
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
        'asym_id', em.builtin_types['text'], nullok=False, comment=column_comment['asym_id'],
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
    em.Column.define('details', em.builtin_types['text'], comment=column_comment['details'],
                     ),
    em.Column.define(
        'entity_description',
        em.builtin_types['text'],
        comment=column_comment['entity_description'],
    ),
    em.Column.define(
        'entity_id', em.builtin_types['text'], nullok=False, comment=column_comment['entity_id'],
    ),
    em.Column.define('id', em.builtin_types['int4'], nullok=False, comment=column_comment['id'],
                     ),
    em.Column.define(
        'model_id', em.builtin_types['int4'], nullok=False, comment=column_comment['model_id'],
    ),
    em.Column.define('reason', em.builtin_types['text'], comment=column_comment['reason'],
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
]

visible_columns = {
    '*': [
        'RID', {
            'source': [{
                'outbound': ['PDB', 'ihm_residues_not_modeled_structure_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table entry.id.',
            'markdown_name': 'structure id'
        }, 'id', {
            'source': [{
                'outbound': ['PDB', 'ihm_residues_not_modeled_model_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table ihm_model_list.model_id.',
            'markdown_name': 'model id'
        }, 'entity_description', {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_residues_not_modeled_mm_poly_res_label_begin_fkey']
                }, 'entity_id'
            ],
            'comment': 'A reference to table entity_poly_seq.entity_id.',
            'markdown_name': 'entity id'
        }, {
            'source': [{
                'outbound': ['PDB', 'ihm_residues_not_modeled_asym_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table struct_asym.id.',
            'markdown_name': 'asym id'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_residues_not_modeled_mm_poly_res_label_begin_fkey']
                }, 'num'
            ],
            'comment': 'A reference to table entity_poly_seq.num.',
            'markdown_name': 'seq id begin'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_residues_not_modeled_mm_poly_res_label_end_fkey']
                }, 'num'
            ],
            'comment': 'A reference to table entity_poly_seq.num.',
            'markdown_name': 'seq id end'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_residues_not_modeled_mm_poly_res_label_begin_fkey']
                }, 'mon_id'
            ],
            'comment': 'A reference to table entity_poly_seq.mon_id.',
            'markdown_name': 'comp id begin'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_residues_not_modeled_mm_poly_res_label_end_fkey']
                }, 'mon_id'
            ],
            'comment': 'A reference to table entity_poly_seq.mon_id.',
            'markdown_name': 'comp id end'
        }, ['PDB', 'ihm_residues_not_modeled_reason_fkey'], 'details', {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_residues_not_modeled_mm_poly_res_label_begin_fkey']
                }, 'RID'
            ],
            'comment': 'Composite key to identify a polymeric residue',
            'markdown_name': 'polymeric residue begin'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_residues_not_modeled_mm_poly_res_label_end_fkey']
                }, 'RID'
            ],
            'comment': 'Composite key to identify a polymeric residue',
            'markdown_name': 'polymeric residue end'
        }
    ],
    'entry': [
        {
            'source': [{
                'outbound': ['PDB', 'ihm_residues_not_modeled_structure_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table entry.id.',
            'markdown_name': 'structure id'
        }, 'id', {
            'source': [{
                'outbound': ['PDB', 'ihm_residues_not_modeled_model_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table ihm_model_list.model_id.',
            'markdown_name': 'model id'
        }, 'entity_description', {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_residues_not_modeled_mm_poly_res_label_begin_fkey']
                }, 'entity_id'
            ],
            'comment': 'A reference to table entity_poly_seq.entity_id.',
            'markdown_name': 'entity id'
        }, {
            'source': [{
                'outbound': ['PDB', 'ihm_residues_not_modeled_asym_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table struct_asym.id.',
            'markdown_name': 'asym id'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_residues_not_modeled_mm_poly_res_label_begin_fkey']
                }, 'num'
            ],
            'comment': 'A reference to table entity_poly_seq.num.',
            'markdown_name': 'seq id begin'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_residues_not_modeled_mm_poly_res_label_end_fkey']
                }, 'num'
            ],
            'comment': 'A reference to table entity_poly_seq.num.',
            'markdown_name': 'seq id end'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_residues_not_modeled_mm_poly_res_label_begin_fkey']
                }, 'mon_id'
            ],
            'comment': 'A reference to table entity_poly_seq.mon_id.',
            'markdown_name': 'comp id begin'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_residues_not_modeled_mm_poly_res_label_end_fkey']
                }, 'mon_id'
            ],
            'comment': 'A reference to table entity_poly_seq.mon_id.',
            'markdown_name': 'comp id end'
        }, ['PDB', 'ihm_residues_not_modeled_reason_fkey'], 'details', {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_residues_not_modeled_mm_poly_res_label_begin_fkey']
                }, 'RID'
            ],
            'comment': 'Composite key to identify a polymeric residue',
            'markdown_name': 'polymeric residue begin'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_residues_not_modeled_mm_poly_res_label_end_fkey']
                }, 'RID'
            ],
            'comment': 'Composite key to identify a polymeric residue',
            'markdown_name': 'polymeric residue end'
        }
    ],
    'detailed': [
        'RID', {
            'source': [{
                'outbound': ['PDB', 'ihm_residues_not_modeled_structure_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table entry.id.',
            'markdown_name': 'structure id'
        }, 'id', {
            'source': [{
                'outbound': ['PDB', 'ihm_residues_not_modeled_model_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table ihm_model_list.model_id.',
            'markdown_name': 'model id'
        }, 'entity_description', {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_residues_not_modeled_mm_poly_res_label_begin_fkey']
                }, 'entity_id'
            ],
            'comment': 'A reference to table entity_poly_seq.entity_id.',
            'markdown_name': 'entity id'
        }, {
            'source': [{
                'outbound': ['PDB', 'ihm_residues_not_modeled_asym_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table struct_asym.id.',
            'markdown_name': 'asym id'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_residues_not_modeled_mm_poly_res_label_begin_fkey']
                }, 'num'
            ],
            'comment': 'A reference to table entity_poly_seq.num.',
            'markdown_name': 'seq id begin'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_residues_not_modeled_mm_poly_res_label_end_fkey']
                }, 'num'
            ],
            'comment': 'A reference to table entity_poly_seq.num.',
            'markdown_name': 'seq id end'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_residues_not_modeled_mm_poly_res_label_begin_fkey']
                }, 'mon_id'
            ],
            'comment': 'A reference to table entity_poly_seq.mon_id.',
            'markdown_name': 'comp id begin'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_residues_not_modeled_mm_poly_res_label_end_fkey']
                }, 'mon_id'
            ],
            'comment': 'A reference to table entity_poly_seq.mon_id.',
            'markdown_name': 'comp id end'
        }, ['PDB', 'ihm_residues_not_modeled_reason_fkey'], 'details', {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_residues_not_modeled_mm_poly_res_label_begin_fkey']
                }, 'RID'
            ],
            'comment': 'Composite key to identify a polymeric residue',
            'markdown_name': 'polymeric residue begin'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_residues_not_modeled_mm_poly_res_label_end_fkey']
                }, 'RID'
            ],
            'comment': 'Composite key to identify a polymeric residue',
            'markdown_name': 'polymeric residue end'
        }, ['PDB', 'ihm_residues_not_modeled_RCB_fkey'],
        ['PDB', 'ihm_residues_not_modeled_RMB_fkey'], 'RCT', 'RMT',
        ['PDB', 'ihm_residues_not_modeled_Owner_fkey']
    ]
}

table_annotations = {chaise_tags.visible_columns: visible_columns, }

table_comment = 'Residues that are defined in the corresponding ihm_struct_assembly item but are missing in the 3D model'

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
    em.Key.define(
        ['structure_id', 'id'],
        constraint_names=[['PDB', 'ihm_residues_not_modeled_primary_key']],
    ),
    em.Key.define(['RID'], constraint_names=[['PDB', 'ihm_residues_not_modeled_RIDkey1']],
                  ),
]

fkey_defs = [
    em.ForeignKey.define(
        ['entity_id', 'comp_id_begin', 'structure_id', 'seq_id_begin'],
        'PDB',
        'entity_poly_seq', ['entity_id', 'mon_id', 'structure_id', 'num'],
        constraint_names=[['PDB', 'ihm_residues_not_modeled_mm_poly_res_label_begin_fkey']],
        annotations={
            chaise_tags.foreign_key: {
                'from_name': 'Ihm Residues Not Modeled Begin',
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
        ['Owner'],
        'public',
        'Catalog_Group', ['ID'],
        constraint_names=[['PDB', 'ihm_residues_not_modeled_Owner_fkey']],
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
        ['structure_id'],
        'PDB',
        'entry', ['id'],
        constraint_names=[['PDB', 'ihm_residues_not_modeled_structure_id_fkey']],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
        on_update='CASCADE',
        on_delete='SET NULL',
    ),
    em.ForeignKey.define(
        ['reason'],
        'Vocab',
        'ihm_residues_not_modeled_reason', ['ID'],
        constraint_names=[['PDB', 'ihm_residues_not_modeled_reason_fkey']],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
    ),
    em.ForeignKey.define(
        ['comp_id_end', 'entity_id', 'seq_id_end', 'structure_id'],
        'PDB',
        'entity_poly_seq', ['mon_id', 'entity_id', 'num', 'structure_id'],
        constraint_names=[['PDB', 'ihm_residues_not_modeled_mm_poly_res_label_end_fkey']],
        annotations={
            chaise_tags.foreign_key: {
                'from_name': 'Ihm Residues Not Modeled End',
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
        ['asym_id', 'structure_id'],
        'PDB',
        'struct_asym', ['id', 'structure_id'],
        constraint_names=[['PDB', 'ihm_residues_not_modeled_asym_id_fkey']],
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
        ['RMB'],
        'public',
        'ERMrest_Client', ['ID'],
        constraint_names=[['PDB', 'ihm_residues_not_modeled_RMB_fkey']],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
    ),
    em.ForeignKey.define(
        ['RCB'],
        'public',
        'ERMrest_Client', ['ID'],
        constraint_names=[['PDB', 'ihm_residues_not_modeled_RCB_fkey']],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
    ),
    em.ForeignKey.define(
        ['model_id', 'structure_id'],
        'PDB',
        'ihm_model_list', ['model_id', 'structure_id'],
        constraint_names=[['PDB', 'ihm_residues_not_modeled_model_id_fkey']],
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
