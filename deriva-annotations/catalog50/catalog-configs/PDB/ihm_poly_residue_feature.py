import argparse
from deriva.core import ErmrestCatalog, AttrDict, get_credential
import deriva.core.ermrest_model as em
from deriva.core.ermrest_config import tag as chaise_tags
from deriva.utils.catalog.manage.update_catalog import CatalogUpdater, parse_args

groups = {}

table_name = 'ihm_poly_residue_feature'

schema_name = 'PDB'

column_annotations = {
    'structure_id': {},
    'asym_id': {},
    'comp_id_begin': {},
    'comp_id_end': {},
    'entity_id': {},
    'feature_id': {},
    'interface_residue_flag': {},
    'ordinal_id': {},
    'rep_atom': {},
    'residue_range_granularity': {},
    'seq_id_begin': {},
    'seq_id_end': {},
    'Owner': {}
}

column_comment = {
    'structure_id': 'A reference to table entry.id.',
    'asym_id': 'A reference to table struct_asym.id.',
    'comp_id_begin': 'A reference to table entity_poly_seq.mon_id.',
    'comp_id_end': 'A reference to table entity_poly_seq.mon_id.',
    'entity_id': 'A reference to table entity_poly_seq.entity_id.',
    'feature_id': 'A reference to table ihm_feature_list.feature_id.',
    'interface_residue_flag': 'type:text\nA flag to indicate if the feature is an interface residue, identified by experiments and\n therefore, used to build spatial restraints during modeling.',
    'ordinal_id': 'type:int4\nA unique identifier for the category.',
    'rep_atom': 'type:text\nIf _ihm_poly_residue_feature.granularity is by-residue, then indicate the atom used to represent \n the residue in three-dimension. Default is the C-alpha atom.',
    'residue_range_granularity': 'type:text\nThe coarse-graining information, if the feature is a residue range.',
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
    em.Column.define('asym_id', em.builtin_types['text'], comment=column_comment['asym_id'],
                     ),
    em.Column.define(
        'comp_id_begin', em.builtin_types['text'], comment=column_comment['comp_id_begin'],
    ),
    em.Column.define(
        'comp_id_end', em.builtin_types['text'], comment=column_comment['comp_id_end'],
    ),
    em.Column.define(
        'entity_id', em.builtin_types['text'], nullok=False, comment=column_comment['entity_id'],
    ),
    em.Column.define(
        'feature_id',
        em.builtin_types['int4'],
        nullok=False,
        comment=column_comment['feature_id'],
    ),
    em.Column.define(
        'interface_residue_flag',
        em.builtin_types['text'],
        comment=column_comment['interface_residue_flag'],
    ),
    em.Column.define(
        'ordinal_id',
        em.builtin_types['int4'],
        nullok=False,
        comment=column_comment['ordinal_id'],
    ),
    em.Column.define('rep_atom', em.builtin_types['text'], comment=column_comment['rep_atom'],
                     ),
    em.Column.define(
        'residue_range_granularity',
        em.builtin_types['text'],
        comment=column_comment['residue_range_granularity'],
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
    em.Column.define('Entry_Related_File', em.builtin_types['text'],
                     ),
    em.Column.define('Asym_RID', em.builtin_types['text'],
                     ),
]

visible_columns = {
    '*': [
        'RID', {
            'source': [{
                'outbound': ['PDB', 'ihm_poly_residue_feature_structure_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table entry.id.',
            'markdown_name': 'structure id'
        }, 'ordinal_id', {
            'source': [{
                'outbound': ['PDB', 'ihm_poly_residue_feature_feature_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table ihm_feature_list.feature_id.',
            'markdown_name': 'feature id'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_poly_residue_feature_mm_poly_res_label_begin_fkey']
                }, 'entity_id'
            ],
            'comment': 'A reference to table entity_poly_seq.entity_id',
            'markdown_name': 'entity id'
        }, {
            'source': [{
                'outbound': ['PDB', 'ihm_poly_residue_feature_asym_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table struct_asym.id.',
            'markdown_name': 'asym id'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_poly_residue_feature_mm_poly_res_label_begin_fkey']
                }, 'mon_id'
            ],
            'comment': 'A reference to table entity_poly_seq.mon_id',
            'markdown_name': 'comp id begin'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_poly_residue_feature_mm_poly_res_label_end_fkey']
                }, 'mon_id'
            ],
            'comment': 'A reference to table entity_poly_seq.mon_id',
            'markdown_name': 'comp id end'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_poly_residue_feature_mm_poly_res_label_begin_fkey']
                }, 'num'
            ],
            'comment': 'A reference to table entity_poly_seq.num',
            'markdown_name': 'seq id begin'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_poly_residue_feature_mm_poly_res_label_end_fkey']
                }, 'num'
            ],
            'comment': 'A reference to table entity_poly_seq.num',
            'markdown_name': 'seq id end'
        }, ['PDB', 'ihm_poly_residue_feature_rep_atom_fkey'],
        ['PDB', 'ihm_poly_residue_feature_residue_range_granularity_fkey'],
        ['PDB', 'ihm_poly_residue_feature_interface_residue_flag_fkey'], {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_poly_residue_feature_mm_poly_res_label_begin_fkey']
                }, 'RID'
            ],
            'markdown_name': 'polymeric residue begin'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_poly_residue_feature_mm_poly_res_label_end_fkey']
                }, 'RID'
            ],
            'markdown_name': 'polymeric residue end'
        }, ['PDB', 'ihm_poly_residue_feature_Entry_Related_File_fkey']
    ],
    'entry': [
        {
            'source': [{
                'outbound': ['PDB', 'ihm_poly_residue_feature_structure_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table entry.id.',
            'markdown_name': 'structure id'
        }, 'ordinal_id', {
            'source': [{
                'outbound': ['PDB', 'ihm_poly_residue_feature_feature_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table ihm_feature_list.feature_id.',
            'markdown_name': 'feature id'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_poly_residue_feature_mm_poly_res_label_begin_fkey']
                }, 'entity_id'
            ],
            'comment': 'A reference to table entity_poly_seq.entity_id',
            'markdown_name': 'entity id'
        }, {
            'source': [{
                'outbound': ['PDB', 'ihm_poly_residue_feature_asym_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table struct_asym.id.',
            'markdown_name': 'asym id'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_poly_residue_feature_mm_poly_res_label_begin_fkey']
                }, 'mon_id'
            ],
            'comment': 'A reference to table entity_poly_seq.mon_id',
            'markdown_name': 'comp id begin'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_poly_residue_feature_mm_poly_res_label_end_fkey']
                }, 'mon_id'
            ],
            'comment': 'A reference to table entity_poly_seq.mon_id',
            'markdown_name': 'comp id end'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_poly_residue_feature_mm_poly_res_label_begin_fkey']
                }, 'num'
            ],
            'comment': 'A reference to table entity_poly_seq.num',
            'markdown_name': 'seq id begin'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_poly_residue_feature_mm_poly_res_label_end_fkey']
                }, 'num'
            ],
            'comment': 'A reference to table entity_poly_seq.num',
            'markdown_name': 'seq id end'
        }, ['PDB', 'ihm_poly_residue_feature_rep_atom_fkey'],
        ['PDB', 'ihm_poly_residue_feature_residue_range_granularity_fkey'],
        ['PDB', 'ihm_poly_residue_feature_interface_residue_flag_fkey'], {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_poly_residue_feature_mm_poly_res_label_begin_fkey']
                }, 'RID'
            ],
            'markdown_name': 'polymeric residue begin'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_poly_residue_feature_mm_poly_res_label_end_fkey']
                }, 'RID'
            ],
            'markdown_name': 'polymeric residue end'
        }
    ],
    'detailed': [
        'RID', {
            'source': [{
                'outbound': ['PDB', 'ihm_poly_residue_feature_structure_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table entry.id.',
            'markdown_name': 'structure id'
        }, 'ordinal_id', {
            'source': [{
                'outbound': ['PDB', 'ihm_poly_residue_feature_feature_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table ihm_feature_list.feature_id.',
            'markdown_name': 'feature id'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_poly_residue_feature_mm_poly_res_label_begin_fkey']
                }, 'entity_id'
            ],
            'comment': 'A reference to table entity_poly_seq.entity_id',
            'markdown_name': 'entity id'
        }, {
            'source': [{
                'outbound': ['PDB', 'ihm_poly_residue_feature_asym_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table struct_asym.id.',
            'markdown_name': 'asym id'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_poly_residue_feature_mm_poly_res_label_begin_fkey']
                }, 'mon_id'
            ],
            'comment': 'A reference to table entity_poly_seq.mon_id',
            'markdown_name': 'comp id begin'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_poly_residue_feature_mm_poly_res_label_end_fkey']
                }, 'mon_id'
            ],
            'comment': 'A reference to table entity_poly_seq.mon_id',
            'markdown_name': 'comp id end'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_poly_residue_feature_mm_poly_res_label_begin_fkey']
                }, 'num'
            ],
            'comment': 'A reference to table entity_poly_seq.num',
            'markdown_name': 'seq id begin'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_poly_residue_feature_mm_poly_res_label_end_fkey']
                }, 'num'
            ],
            'comment': 'A reference to table entity_poly_seq.num',
            'markdown_name': 'seq id end'
        }, ['PDB', 'ihm_poly_residue_feature_rep_atom_fkey'],
        ['PDB', 'ihm_poly_residue_feature_residue_range_granularity_fkey'],
        ['PDB', 'ihm_poly_residue_feature_interface_residue_flag_fkey'], {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_poly_residue_feature_mm_poly_res_label_begin_fkey']
                }, 'RID'
            ],
            'markdown_name': 'polymeric residue begin'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_poly_residue_feature_mm_poly_res_label_end_fkey']
                }, 'RID'
            ],
            'markdown_name': 'polymeric residue end'
        }, ['PDB', 'ihm_poly_residue_feature_Entry_Related_File_fkey'],
        ['PDB', 'ihm_poly_residue_feature_RCB_fkey'], ['PDB', 'ihm_poly_residue_feature_RMB_fkey'],
        'RCT', 'RMT', ['PDB', 'ihm_poly_residue_feature_Owner_fkey']
    ]
}

table_annotations = {chaise_tags.visible_columns: visible_columns, }

table_comment = 'Details of polymeric residue features'

table_acls = {}

table_acl_bindings = {}

key_defs = [
    em.Key.define(
        ['structure_id', 'ordinal_id'],
        constraint_names=[['PDB', 'ihm_poly_residue_feature_primary_key']],
    ),
    em.Key.define(['RID'], constraint_names=[['PDB', 'ihm_poly_residue_feature_RIDkey1']],
                  ),
]

fkey_defs = [
    em.ForeignKey.define(
        ['interface_residue_flag'],
        'Vocab',
        'ihm_poly_residue_feature_interface_residue_flag', ['Name'],
        constraint_names=[['PDB', 'ihm_poly_residue_feature_interface_residue_flag_fkey']],
    ),
    em.ForeignKey.define(
        ['rep_atom'],
        'Vocab',
        'ihm_poly_residue_feature_rep_atom', ['Name'],
        constraint_names=[['PDB', 'ihm_poly_residue_feature_rep_atom_fkey']],
    ),
    em.ForeignKey.define(
        ['residue_range_granularity'],
        'Vocab',
        'ihm_poly_residue_feature_residue_range_granularity', ['Name'],
        constraint_names=[['PDB', 'ihm_poly_residue_feature_residue_range_granularity_fkey']],
    ),
    em.ForeignKey.define(
        ['asym_id', 'structure_id'],
        'PDB',
        'struct_asym', ['id', 'structure_id'],
        constraint_names=[['PDB', 'ihm_poly_residue_feature_asym_id_fk']],
        annotations={
            chaise_tags.foreign_key: {
                'domain_filter_pattern': 'structure_id={{structure_id}}'
            }
        },
        on_update='CASCADE',
        on_delete='SET NULL',
    ),
    em.ForeignKey.define(
        ['Asym_RID', 'asym_id'],
        'PDB',
        'struct_asym', ['RID', 'id'],
        constraint_names=[['PDB', 'ihm_poly_residue_feature_asym_id_fkey']],
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
        constraint_names=[['PDB', 'ihm_poly_residue_feature_RCB_fkey']],
    ),
    em.ForeignKey.define(
        ['structure_id', 'comp_id_begin', 'seq_id_begin', 'entity_id'],
        'PDB',
        'entity_poly_seq', ['structure_id', 'mon_id', 'num', 'entity_id'],
        constraint_names=[['PDB', 'ihm_poly_residue_feature_mm_poly_res_label_begin_fkey']],
        annotations={
            chaise_tags.foreign_key: {
                'from_name': 'Ihm Poly Contact Residue Feature Begin',
                'template_engine': 'handlebars',
                'domain_filter_pattern': '{{#if _structure_id}}structure_id={{{_structure_id}}}{{/if}}'
            }
        },
        on_update='CASCADE',
        on_delete='SET NULL',
    ),
    em.ForeignKey.define(
        ['RMB'],
        'public',
        'ERMrest_Client', ['ID'],
        constraint_names=[['PDB', 'ihm_poly_residue_feature_RMB_fkey']],
    ),
    em.ForeignKey.define(
        ['feature_id', 'structure_id'],
        'PDB',
        'ihm_feature_list', ['feature_id', 'structure_id'],
        constraint_names=[['PDB', 'ihm_poly_residue_feature_feature_id_fkey']],
        annotations={
            chaise_tags.foreign_key: {
                'template_engine': 'handlebars',
                'domain_filter_pattern': '{{#if _structure_id}}structure_id={{{_structure_id}}}{{/if}}'
            }
        },
        on_update='CASCADE',
        on_delete='SET NULL',
    ),
    em.ForeignKey.define(
        ['structure_id', 'comp_id_end', 'entity_id', 'seq_id_end'],
        'PDB',
        'entity_poly_seq', ['structure_id', 'mon_id', 'entity_id', 'num'],
        constraint_names=[['PDB', 'ihm_poly_residue_feature_mm_poly_res_label_end_fkey']],
        annotations={
            chaise_tags.foreign_key: {
                'from_name': 'Ihm Poly Contact Residue Feature End',
                'template_engine': 'handlebars',
                'domain_filter_pattern': '{{#if _structure_id}}structure_id={{{_structure_id}}}{{/if}}'
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
    catalog_id = 50
    mode, replace, host, catalog_id = parse_args(host, catalog_id, is_table=True)
    catalog = ErmrestCatalog('https', host, catalog_id=catalog_id, credentials=get_credential(host))
    main(catalog, mode, replace)
