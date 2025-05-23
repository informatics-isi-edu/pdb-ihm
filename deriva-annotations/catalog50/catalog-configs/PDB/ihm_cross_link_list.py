import argparse
from deriva.core import ErmrestCatalog, AttrDict, get_credential
import deriva.core.ermrest_model as em
from deriva.core.ermrest_config import tag as chaise_tags
from deriva.utils.catalog.manage.update_catalog import CatalogUpdater, parse_args

groups = {}

table_name = 'ihm_cross_link_list'

schema_name = 'PDB'

column_annotations = {
    'structure_id': {},
    'comp_id_1': {},
    'comp_id_2': {},
    'dataset_list_id': {},
    'details': {},
    'entity_description_1': {},
    'entity_description_2': {},
    'entity_id_1': {},
    'entity_id_2': {},
    'group_id': {},
    'id': {},
    'linker_chem_comp_descriptor_id': {},
    'linker_type': {},
    'seq_id_1': {},
    'seq_id_2': {},
    'Owner': {}
}

column_comment = {
    'structure_id': 'A reference to table entry.id.',
    'comp_id_1': 'A reference to table chem_comp.id.',
    'comp_id_2': 'A reference to table chem_comp.id.',
    'dataset_list_id': 'A reference to table ihm_dataset_list.id.',
    'details': 'type:text\nAdditional details regarding the cross link or the cross linking agent.',
    'entity_description_1': 'type:text\nA text description of molecular entity 1. \n',
    'entity_description_2': 'type:text\nA text description of molecular entity 2. \n',
    'entity_id_1': 'A reference to table entity.id.',
    'entity_id_2': 'A reference to table entity.id.',
    'group_id': 'type:int4\nAn identifier for a set of ambiguous crosslink restraints. \n Handles experimental uncertainties in the identities of \n crosslinked residues.',
    'id': 'type:int4\nA unique identifier for the cross link restraint.',
    'linker_chem_comp_descriptor_id': 'A reference to table ihm_chemical_component_descriptor.id.',
    'linker_type': 'type:text\nThe type of crosslinker used.',
    'seq_id_1': 'A reference to table entity_poly_seq.num.',
    'seq_id_2': 'A reference to table entity_poly_seq.num.',
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
        'comp_id_1', em.builtin_types['text'], nullok=False, comment=column_comment['comp_id_1'],
    ),
    em.Column.define(
        'comp_id_2', em.builtin_types['text'], nullok=False, comment=column_comment['comp_id_2'],
    ),
    em.Column.define(
        'dataset_list_id',
        em.builtin_types['int4'],
        nullok=False,
        comment=column_comment['dataset_list_id'],
    ),
    em.Column.define('details', em.builtin_types['text'], comment=column_comment['details'],
                     ),
    em.Column.define(
        'entity_description_1',
        em.builtin_types['text'],
        comment=column_comment['entity_description_1'],
    ),
    em.Column.define(
        'entity_description_2',
        em.builtin_types['text'],
        comment=column_comment['entity_description_2'],
    ),
    em.Column.define(
        'entity_id_1',
        em.builtin_types['text'],
        nullok=False,
        comment=column_comment['entity_id_1'],
    ),
    em.Column.define(
        'entity_id_2',
        em.builtin_types['text'],
        nullok=False,
        comment=column_comment['entity_id_2'],
    ),
    em.Column.define(
        'group_id', em.builtin_types['int4'], nullok=False, comment=column_comment['group_id'],
    ),
    em.Column.define('id', em.builtin_types['int4'], nullok=False, comment=column_comment['id'],
                     ),
    em.Column.define(
        'linker_chem_comp_descriptor_id',
        em.builtin_types['int4'],
        comment=column_comment['linker_chem_comp_descriptor_id'],
    ),
    em.Column.define(
        'linker_type',
        em.builtin_types['text'],
        nullok=False,
        comment=column_comment['linker_type'],
    ),
    em.Column.define(
        'seq_id_1', em.builtin_types['int4'], nullok=False, comment=column_comment['seq_id_1'],
    ),
    em.Column.define(
        'seq_id_2', em.builtin_types['int4'], nullok=False, comment=column_comment['seq_id_2'],
    ),
    em.Column.define('Owner', em.builtin_types['text'], comment=column_comment['Owner'],
                     ),
    em.Column.define('Entry_Related_File', em.builtin_types['text'],
                     ),
    em.Column.define('Linker_chem_comp_descriptor_RID', em.builtin_types['text'],
                     ),
]

visible_columns = {
    '*': [
        {
            'source': 'RID'
        }, {
            'source': [{
                'outbound': ['PDB', 'ihm_cross_link_list_structure_id_fkey']
            }, 'RID']
        }, 'id', 'group_id', 'entity_description_1', 'entity_description_2', {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_cross_link_list_mm_poly_res_label_1_fkey']
                }, 'entity_id'
            ],
            'markdown_name': 'entity id 1'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_cross_link_list_mm_poly_res_label_2_fkey']
                }, 'entity_id'
            ],
            'markdown_name': 'entity id 2'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_cross_link_list_mm_poly_res_label_1_fkey']
                }, 'mon_id'
            ],
            'markdown_name': 'comp id 1'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_cross_link_list_mm_poly_res_label_2_fkey']
                }, 'mon_id'
            ],
            'markdown_name': 'comp id 2'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_cross_link_list_mm_poly_res_label_1_fkey']
                }, 'num'
            ],
            'markdown_name': 'seq id 1'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_cross_link_list_mm_poly_res_label_2_fkey']
                }, 'num'
            ],
            'markdown_name': 'seq id 2'
        }, ['PDB', 'ihm_cross_link_list_linker_type_fkey'], {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_cross_link_list_linker_chem_comp_descriptor_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table ihm_chemical_component_descriptor.id for the cross linker.',
            'markdown_name': 'linker chem comp descriptor id'
        }, 'details', ['PDB', 'ihm_cross_link_list_dataset_list_id_fkey'], {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_cross_link_list_mm_poly_res_label_1_fkey']
                }, 'RID'
            ],
            'markdown_name': 'polymeric residue 1'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_cross_link_list_mm_poly_res_label_2_fkey']
                }, 'RID'
            ],
            'markdown_name': 'polymeric residue 2'
        }, ['PDB', 'ihm_cross_link_list_Entry_Related_File_fkey']
    ],
    'entry': [
        {
            'source': [{
                'outbound': ['PDB', 'ihm_cross_link_list_structure_id_fkey']
            }, 'RID']
        }, 'id', 'group_id', 'entity_description_1', 'entity_description_2', {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_cross_link_list_mm_poly_res_label_1_fkey']
                }, 'entity_id'
            ],
            'markdown_name': 'entity id 1'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_cross_link_list_mm_poly_res_label_2_fkey']
                }, 'entity_id'
            ],
            'markdown_name': 'entity id 2'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_cross_link_list_mm_poly_res_label_1_fkey']
                }, 'mon_id'
            ],
            'markdown_name': 'comp id 1'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_cross_link_list_mm_poly_res_label_2_fkey']
                }, 'mon_id'
            ],
            'markdown_name': 'comp id 2'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_cross_link_list_mm_poly_res_label_1_fkey']
                }, 'num'
            ],
            'markdown_name': 'seq id 1'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_cross_link_list_mm_poly_res_label_2_fkey']
                }, 'num'
            ],
            'markdown_name': 'seq id 2'
        }, ['PDB', 'ihm_cross_link_list_linker_type_fkey'], {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_cross_link_list_linker_chem_comp_descriptor_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table ihm_chemical_component_descriptor.id for the cross linker.',
            'markdown_name': 'linker chem comp descriptor id'
        }, 'details', ['PDB', 'ihm_cross_link_list_dataset_list_id_fkey'], {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_cross_link_list_mm_poly_res_label_1_fkey']
                }, 'RID'
            ],
            'markdown_name': 'polymeric residue 1'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_cross_link_list_mm_poly_res_label_2_fkey']
                }, 'RID'
            ],
            'markdown_name': 'polymeric residue 2'
        }
    ],
    'detailed': [
        {
            'source': 'RID'
        }, {
            'source': [{
                'outbound': ['PDB', 'ihm_cross_link_list_structure_id_fkey']
            }, 'RID']
        }, 'id', 'group_id', 'entity_description_1', 'entity_description_2', {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_cross_link_list_mm_poly_res_label_1_fkey']
                }, 'entity_id'
            ],
            'markdown_name': 'entity id 1'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_cross_link_list_mm_poly_res_label_2_fkey']
                }, 'entity_id'
            ],
            'markdown_name': 'entity id 2'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_cross_link_list_mm_poly_res_label_1_fkey']
                }, 'mon_id'
            ],
            'markdown_name': 'comp id 1'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_cross_link_list_mm_poly_res_label_2_fkey']
                }, 'mon_id'
            ],
            'markdown_name': 'comp id 2'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_cross_link_list_mm_poly_res_label_1_fkey']
                }, 'num'
            ],
            'markdown_name': 'seq id 1'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_cross_link_list_mm_poly_res_label_2_fkey']
                }, 'num'
            ],
            'markdown_name': 'seq id 2'
        }, ['PDB', 'ihm_cross_link_list_linker_type_fkey'], {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_cross_link_list_linker_chem_comp_descriptor_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table ihm_chemical_component_descriptor.id for the cross linker.',
            'markdown_name': 'linker chem comp descriptor id'
        }, 'details', ['PDB', 'ihm_cross_link_list_dataset_list_id_fkey'], {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_cross_link_list_mm_poly_res_label_1_fkey']
                }, 'RID'
            ],
            'markdown_name': 'polymeric residue 1'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_cross_link_list_mm_poly_res_label_2_fkey']
                }, 'RID'
            ],
            'markdown_name': 'polymeric residue 2'
        }, ['PDB', 'ihm_cross_link_list_Entry_Related_File_fkey'], {
            'source': 'RCT'
        }, {
            'source': 'RMT'
        }, {
            'source': [{
                'outbound': ['PDB', 'ihm_cross_link_list_RCB_fkey']
            }, 'RID']
        }, {
            'source': [{
                'outbound': ['PDB', 'ihm_cross_link_list_RMB_fkey']
            }, 'RID']
        }, {
            'source': [{
                'outbound': ['PDB', 'ihm_cross_link_list_Owner_fkey']
            }, 'RID']
        }
    ]
}

visible_foreign_keys = {
    'filter': 'detailed',
    'detailed': [['PDB', 'ihm_cross_link_restraint_group_id_fkey']]
}

table_display = {'row_name': {'row_markdown_pattern': '{{{id}}}'}}

table_annotations = {
    chaise_tags.table_display: table_display,
    chaise_tags.visible_columns: visible_columns,
    chaise_tags.visible_foreign_keys: visible_foreign_keys,
}

table_comment = 'List of distance restraints derived from chemical crosslinking experiments'

table_acls = {}

table_acl_bindings = {}

key_defs = [
    em.Key.define(
        ['structure_id', 'id'], constraint_names=[['PDB', 'ihm_cross_link_list_primary_key']],
    ),
    em.Key.define(['RID'], constraint_names=[['PDB', 'ihm_cross_link_list_RIDkey1']],
                  ),
]

fkey_defs = [
    em.ForeignKey.define(
        ['linker_type'],
        'Vocab',
        'ihm_cross_link_list_linker_type', ['Name'],
        constraint_names=[['PDB', 'ihm_cross_link_list_linker_type_fkey']],
    ),
    em.ForeignKey.define(
        ['linker_chem_comp_descriptor_id', 'structure_id'],
        'PDB',
        'ihm_chemical_component_descriptor', ['id', 'structure_id'],
        constraint_names=[['PDB', 'ihm_cross_link_list_linker_chem_comp_descriptor_id_fk']],
        annotations={
            chaise_tags.foreign_key: {
                'domain_filter_pattern': 'structure_id={{structure_id}}'
            }
        },
        on_update='CASCADE',
        on_delete='SET NULL',
    ),
    em.ForeignKey.define(
        ['Linker_chem_comp_descriptor_RID', 'linker_chem_comp_descriptor_id'],
        'PDB',
        'ihm_chemical_component_descriptor', ['RID', 'id'],
        constraint_names=[['PDB', 'ihm_cross_link_list_linker_chem_comp_descriptor_id_fkey']],
        annotations={
            chaise_tags.foreign_key: {
                'domain_filter_pattern': 'structure_id={{structure_id}}'
            }
        },
        on_update='CASCADE',
        on_delete='SET NULL',
    ),
    em.ForeignKey.define(
        ['structure_id', 'seq_id_1', 'comp_id_1', 'entity_id_1'],
        'PDB',
        'entity_poly_seq', ['structure_id', 'num', 'mon_id', 'entity_id'],
        constraint_names=[['PDB', 'ihm_cross_link_list_mm_poly_res_label_1_fkey']],
        annotations={
            chaise_tags.foreign_key: {
                'from_name': 'Ihm Cross Link List Label 1',
                'template_engine': 'handlebars',
                'domain_filter_pattern': '{{#if _structure_id}}structure_id={{{_structure_id}}}{{/if}}'
            }
        },
        on_update='CASCADE',
        on_delete='SET NULL',
    ),
    em.ForeignKey.define(
        ['RCB'],
        'public',
        'ERMrest_Client', ['ID'],
        constraint_names=[['PDB', 'ihm_cross_link_list_RCB_fkey']],
    ),
    em.ForeignKey.define(
        ['structure_id', 'seq_id_2', 'comp_id_2', 'entity_id_2'],
        'PDB',
        'entity_poly_seq', ['structure_id', 'num', 'mon_id', 'entity_id'],
        constraint_names=[['PDB', 'ihm_cross_link_list_mm_poly_res_label_2_fkey']],
        annotations={
            chaise_tags.foreign_key: {
                'from_name': 'Ihm Cross Link List Label 2',
                'template_engine': 'handlebars',
                'domain_filter_pattern': '{{#if _structure_id}}structure_id={{{_structure_id}}}{{/if}}'
            }
        },
        on_update='CASCADE',
        on_delete='SET NULL',
    ),
    em.ForeignKey.define(
        ['structure_id', 'dataset_list_id'],
        'PDB',
        'ihm_dataset_list', ['structure_id', 'id'],
        constraint_names=[['PDB', 'ihm_cross_link_list_dataset_list_id_fkey']],
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
        ['RMB'],
        'public',
        'ERMrest_Client', ['ID'],
        constraint_names=[['PDB', 'ihm_cross_link_list_RMB_fkey']],
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
