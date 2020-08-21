import argparse
from deriva.core import ErmrestCatalog, AttrDict, get_credential
import deriva.core.ermrest_model as em
from deriva.core.ermrest_config import tag as chaise_tags
from deriva.utils.catalog.manage.update_catalog import CatalogUpdater, parse_args

groups = {}

table_name = 'ihm_hydroxyl_radical_fp_restraint'

schema_name = 'PDB'

column_annotations = {
    'structure_id': {},
    'asym_id': {},
    'comp_id': {},
    'dataset_list_id': {},
    'entity_description': {},
    'entity_id': {},
    'fp_rate': {},
    'fp_rate_error': {},
    'group_id': {},
    'id': {},
    'log_pf': {},
    'log_pf_error': {},
    'predicted_sasa': {},
    'seq_id': {},
    'software_id': {},
    'Owner': {}
}

column_comment = {
    'structure_id': 'A reference to table entry.id.',
    'asym_id': 'A reference to table struct_asym.id.',
    'comp_id': 'A reference to table entity_poly_seq.mon_id',
    'dataset_list_id': 'A reference to table ihm_dataset_list.id.',
    'entity_description': 'type:text\nA text description of the molecular entity. \n',
    'entity_id': 'A reference to table entity_poly_seq.entity_id',
    'fp_rate': 'type:float4\nThe footprinting rate.',
    'fp_rate_error': 'type:float4\nThe footprinting rate error.',
    'group_id': 'type:int4\nAn identifier to group the hydroxyl radical footprinting restraints.',
    'id': 'type:int4\nA unique identifier for the hydroxyl radical footprinting restraint.',
    'log_pf': 'type:float4\nLog (base 10) protection factor.',
    'log_pf_error': 'type:float4\nError of Log (base 10) protection factor.',
    'predicted_sasa': 'type:float4\nThe predicted solvent accessible surface area.',
    'seq_id': 'A reference to table entity_poly_seq.num.',
    'software_id': 'A reference to table software.pdbx_ordinal.',
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
        'comp_id', em.builtin_types['text'], nullok=False, comment=column_comment['comp_id'],
    ),
    em.Column.define(
        'dataset_list_id',
        em.builtin_types['int4'],
        nullok=False,
        comment=column_comment['dataset_list_id'],
    ),
    em.Column.define(
        'entity_description',
        em.builtin_types['text'],
        comment=column_comment['entity_description'],
    ),
    em.Column.define(
        'entity_id', em.builtin_types['text'], nullok=False, comment=column_comment['entity_id'],
    ),
    em.Column.define('fp_rate', em.builtin_types['float4'], comment=column_comment['fp_rate'],
                     ),
    em.Column.define(
        'fp_rate_error', em.builtin_types['float4'], comment=column_comment['fp_rate_error'],
    ),
    em.Column.define('group_id', em.builtin_types['int4'], comment=column_comment['group_id'],
                     ),
    em.Column.define('id', em.builtin_types['int4'], nullok=False, comment=column_comment['id'],
                     ),
    em.Column.define('log_pf', em.builtin_types['float4'], comment=column_comment['log_pf'],
                     ),
    em.Column.define(
        'log_pf_error', em.builtin_types['float4'], comment=column_comment['log_pf_error'],
    ),
    em.Column.define(
        'predicted_sasa',
        em.builtin_types['float4'],
        nullok=False,
        comment=column_comment['predicted_sasa'],
    ),
    em.Column.define(
        'seq_id', em.builtin_types['int4'], nullok=False, comment=column_comment['seq_id'],
    ),
    em.Column.define(
        'software_id', em.builtin_types['int4'], comment=column_comment['software_id'],
    ),
    em.Column.define('Owner', em.builtin_types['text'], comment=column_comment['Owner'],
                     ),
    em.Column.define('Entry_Related_File', em.builtin_types['text'],
                     ),
    em.Column.define('Software_RID', em.builtin_types['text'],
                     ),
]

visible_columns = {
    '*': [
        'RID', {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_hydroxyl_radical_fp_restraint_structure_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table entry.id.',
            'markdown_name': 'structure id'
        }, 'id', 'group_id', 'entity_description', {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_hydroxyl_radical_fp_restraint_mm_poly_res_label_fkey']
                }, 'entity_id'
            ],
            'comment': 'A reference to table entity_poly_seq.entity_id',
            'markdown_name': 'entity id'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_hydroxyl_radical_fp_restraint_asym_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table struct_asym.id.',
            'markdown_name': 'asym id'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_hydroxyl_radical_fp_restraint_mm_poly_res_label_fkey']
                }, 'mon_id'
            ],
            'comment': 'A reference to table entity_poly_seq.mon_id',
            'markdown_name': 'comp id'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_hydroxyl_radical_fp_restraint_mm_poly_res_label_fkey']
                }, 'num'
            ],
            'comment': 'A reference to table entity_poly_seq.num.',
            'markdown_name': 'seq id'
        }, 'fp_rate', 'fp_rate_error', 'log_pf', 'log_pf_error', 'predicted_sasa', {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_hydroxyl_radical_fp_restraint_software_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table software.pdbx_ordinal.',
            'markdown_name': 'software id'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_hydroxyl_radical_fp_restraint_dataset_list_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table ihm_dataset_list.id.',
            'markdown_name': 'dataset list id'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_hydroxyl_radical_fp_restraint_mm_poly_res_label_fkey']
                }, 'RID'
            ],
            'markdown_name': 'polymeric residue'
        }, ['PDB', 'ihm_hydroxyl_radical_fp_restraint_Entry_Related_File_fkey']
    ],
    'entry': [
        {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_hydroxyl_radical_fp_restraint_structure_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table entry.id.',
            'markdown_name': 'structure id'
        }, 'id', 'group_id', 'entity_description', {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_hydroxyl_radical_fp_restraint_mm_poly_res_label_fkey']
                }, 'entity_id'
            ],
            'comment': 'A reference to table entity_poly_seq.entity_id',
            'markdown_name': 'entity id'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_hydroxyl_radical_fp_restraint_asym_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table struct_asym.id.',
            'markdown_name': 'asym id'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_hydroxyl_radical_fp_restraint_mm_poly_res_label_fkey']
                }, 'mon_id'
            ],
            'comment': 'A reference to table entity_poly_seq.mon_id',
            'markdown_name': 'comp id'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_hydroxyl_radical_fp_restraint_mm_poly_res_label_fkey']
                }, 'num'
            ],
            'comment': 'A reference to table entity_poly_seq.num.',
            'markdown_name': 'seq id'
        }, 'fp_rate', 'fp_rate_error', 'log_pf', 'log_pf_error', 'predicted_sasa', {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_hydroxyl_radical_fp_restraint_software_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table software.pdbx_ordinal.',
            'markdown_name': 'software id'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_hydroxyl_radical_fp_restraint_dataset_list_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table ihm_dataset_list.id.',
            'markdown_name': 'dataset list id'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_hydroxyl_radical_fp_restraint_mm_poly_res_label_fkey']
                }, 'RID'
            ],
            'markdown_name': 'polymeric residue'
        }
    ],
    'detailed': [
        'RID', {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_hydroxyl_radical_fp_restraint_structure_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table entry.id.',
            'markdown_name': 'structure id'
        }, 'id', 'group_id', 'entity_description', {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_hydroxyl_radical_fp_restraint_mm_poly_res_label_fkey']
                }, 'entity_id'
            ],
            'comment': 'A reference to table entity_poly_seq.entity_id',
            'markdown_name': 'entity id'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_hydroxyl_radical_fp_restraint_asym_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table struct_asym.id.',
            'markdown_name': 'asym id'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_hydroxyl_radical_fp_restraint_mm_poly_res_label_fkey']
                }, 'mon_id'
            ],
            'comment': 'A reference to table entity_poly_seq.mon_id',
            'markdown_name': 'comp id'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_hydroxyl_radical_fp_restraint_mm_poly_res_label_fkey']
                }, 'num'
            ],
            'comment': 'A reference to table entity_poly_seq.num.',
            'markdown_name': 'seq id'
        }, 'fp_rate', 'fp_rate_error', 'log_pf', 'log_pf_error', 'predicted_sasa', {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_hydroxyl_radical_fp_restraint_software_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table software.pdbx_ordinal.',
            'markdown_name': 'software id'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_hydroxyl_radical_fp_restraint_dataset_list_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table ihm_dataset_list.id.',
            'markdown_name': 'dataset list id'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_hydroxyl_radical_fp_restraint_mm_poly_res_label_fkey']
                }, 'RID'
            ],
            'markdown_name': 'polymeric residue'
        }, ['PDB', 'ihm_hydroxyl_radical_fp_restraint_Entry_Related_File_fkey'],
        ['PDB', 'ihm_hydroxyl_radical_fp_restraint_RCB_fkey'],
        ['PDB', 'ihm_hydroxyl_radical_fp_restraint_RMB_fkey'], 'RCT', 'RMT',
        ['PDB', 'ihm_hydroxyl_radical_fp_restraint_Owner_fkey']
    ]
}

table_annotations = {chaise_tags.visible_columns: visible_columns, }

table_comment = 'Data from hydroxyl radical footprinting experiments used as restraint in modeling'

table_acls = {}

table_acl_bindings = {}

key_defs = [
    em.Key.define(
        ['RID'], constraint_names=[['PDB', 'ihm_hydroxyl_radical_fp_restraint_RIDkey1']],
    ),
    em.Key.define(
        ['id', 'structure_id'],
        constraint_names=[['PDB', 'ihm_hydroxyl_radical_fp_restraint_primary_key']],
    ),
]

fkey_defs = [
    em.ForeignKey.define(
        ['structure_id', 'software_id'],
        'PDB',
        'software', ['structure_id', 'pdbx_ordinal'],
        constraint_names=[['PDB', 'ihm_hydroxyl_radical_fp_restraint_software_id_fk']],
        annotations={
            chaise_tags.foreign_key: {
                'domain_filter_pattern': 'structure_id={{structure_id}}'
            }
        },
        on_update='CASCADE',
        on_delete='SET NULL',
    ),
    em.ForeignKey.define(
        ['software_id', 'Software_RID'],
        'PDB',
        'software', ['pdbx_ordinal', 'RID'],
        constraint_names=[['PDB', 'ihm_hydroxyl_radical_fp_restraint_software_id_fkey']],
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
        constraint_names=[['PDB', 'ihm_hydroxyl_radical_fp_restraint_RMB_fkey']],
    ),
    em.ForeignKey.define(
        ['structure_id', 'dataset_list_id'],
        'PDB',
        'ihm_dataset_list', ['structure_id', 'id'],
        constraint_names=[['PDB', 'ihm_hydroxyl_radical_fp_restraint_dataset_list_id_fkey']],
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
        constraint_names=[['PDB', 'ihm_hydroxyl_radical_fp_restraint_RCB_fkey']],
    ),
    em.ForeignKey.define(
        ['structure_id', 'asym_id'],
        'PDB',
        'struct_asym', ['structure_id', 'id'],
        constraint_names=[['PDB', 'ihm_hydroxyl_radical_fp_restraint_asym_id_fkey']],
        annotations={
            chaise_tags.foreign_key: {
                'domain_filter_pattern': 'structure_id={{structure_id}}'
            }
        },
        on_update='CASCADE',
        on_delete='SET NULL',
    ),
    em.ForeignKey.define(
        ['entity_id', 'seq_id', 'comp_id', 'structure_id'],
        'PDB',
        'entity_poly_seq', ['entity_id', 'num', 'mon_id', 'structure_id'],
        constraint_names=[['PDB', 'ihm_hydroxyl_radical_fp_restraint_mm_poly_res_label_fkey']],
        annotations={
            chaise_tags.foreign_key: {
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
