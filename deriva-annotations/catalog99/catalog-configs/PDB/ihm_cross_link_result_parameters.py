import argparse
from deriva.core import ErmrestCatalog, AttrDict, get_credential
import deriva.core.ermrest_model as em
from deriva.core.ermrest_config import tag as chaise_tags
from deriva.utils.catalog.manage.update_catalog import CatalogUpdater, parse_args

groups = {}

table_name = 'ihm_cross_link_result_parameters'

schema_name = 'PDB'

column_annotations = {
    'structure_id': {},
    'id': {},
    'model_id': {},
    'psi': {},
    'restraint_id': {},
    'sigma_1': {},
    'sigma_2': {},
    'Owner': {}
}

column_comment = {
    'structure_id': 'A reference to table entry.id.',
    'id': 'type:int4\nA unique identifier for the restraint/model combination.',
    'model_id': 'A reference to table ihm_model_list.model_id.',
    'psi': 'type:float4\nThe uncertainty in the crosslinking experimental data;\n May be approximated to the false positive rate.',
    'restraint_id': 'A reference to table ihm_cross_link_restraint.id.',
    'sigma_1': 'type:float4\nThe uncertainty in the position of residue 1 in the crosslink\n arising due to the multi-scale nature of the model represention.',
    'sigma_2': 'type:float4\nThe uncertainty in the position of residue 2 in the crosslink\n arising due to the multi-scale nature of the model represention.',
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
    em.Column.define('id', em.builtin_types['int4'], nullok=False, comment=column_comment['id'],
                     ),
    em.Column.define(
        'model_id', em.builtin_types['int4'], nullok=False, comment=column_comment['model_id'],
    ),
    em.Column.define('psi', em.builtin_types['float4'], comment=column_comment['psi'],
                     ),
    em.Column.define(
        'restraint_id',
        em.builtin_types['int4'],
        nullok=False,
        comment=column_comment['restraint_id'],
    ),
    em.Column.define('sigma_1', em.builtin_types['float4'], comment=column_comment['sigma_1'],
                     ),
    em.Column.define('sigma_2', em.builtin_types['float4'], comment=column_comment['sigma_2'],
                     ),
    em.Column.define('Owner', em.builtin_types['text'], comment=column_comment['Owner'],
                     ),
    em.Column.define('Entry_Related_File', em.builtin_types['text'],
                     ),
]

visible_columns = {
    '*': [
        'RID', {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_cross_link_result_parameters_structure_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table entry.id.',
            'markdown_name': 'structure id'
        }, 'id', {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_cross_link_result_parameters_restraint_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table ihm_cross_link_restraint.id.',
            'markdown_name': 'restraint id'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_cross_link_result_parameters_model_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table ihm_model_list.model_id.',
            'markdown_name': 'model id'
        }, 'psi', 'sigma_1', 'sigma_2',
        ['PDB', 'ihm_cross_link_result_parameters_Entry_Related_File_fkey']
    ],
    'entry': [
        {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_cross_link_result_parameters_structure_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table entry.id.',
            'markdown_name': 'structure id'
        }, 'id', {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_cross_link_result_parameters_restraint_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table ihm_cross_link_restraint.id.',
            'markdown_name': 'restraint id'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_cross_link_result_parameters_model_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table ihm_model_list.model_id.',
            'markdown_name': 'model id'
        }, 'psi', 'sigma_1', 'sigma_2'
    ],
    'detailed': [
        'RID', {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_cross_link_result_parameters_structure_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table entry.id.',
            'markdown_name': 'structure id'
        }, 'id', {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_cross_link_result_parameters_restraint_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table ihm_cross_link_restraint.id.',
            'markdown_name': 'restraint id'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_cross_link_result_parameters_model_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table ihm_model_list.model_id.',
            'markdown_name': 'model id'
        }, 'psi', 'sigma_1', 'sigma_2',
        ['PDB', 'ihm_cross_link_result_parameters_Entry_Related_File_fkey'],
        ['PDB', 'ihm_cross_link_result_parameters_RCB_fkey'],
        ['PDB', 'ihm_cross_link_result_parameters_RMB_fkey'], 'RCT', 'RMT',
        ['PDB', 'ihm_cross_link_result_parameters_Owner_fkey']
    ]
}

table_annotations = {chaise_tags.visible_columns: visible_columns, }

table_comment = 'Parameters related to the results of crosslinking restraints'

table_acls = {}

table_acl_bindings = {}

key_defs = [
    em.Key.define(
        ['structure_id', 'id'],
        constraint_names=[['PDB', 'ihm_cross_link_result_parameters_primary_key']],
    ),
    em.Key.define(
        ['RID'], constraint_names=[['PDB', 'ihm_cross_link_result_parameters_RIDkey1']],
    ),
]

fkey_defs = [
    em.ForeignKey.define(
        ['RCB'],
        'public',
        'ERMrest_Client', ['ID'],
        constraint_names=[['PDB', 'ihm_cross_link_result_parameters_RCB_fkey']],
    ),
    em.ForeignKey.define(
        ['RMB'],
        'public',
        'ERMrest_Client', ['ID'],
        constraint_names=[['PDB', 'ihm_cross_link_result_parameters_RMB_fkey']],
    ),
    em.ForeignKey.define(
        ['structure_id', 'model_id'],
        'PDB',
        'ihm_model_list', ['structure_id', 'model_id'],
        constraint_names=[['PDB', 'ihm_cross_link_result_parameters_model_id_fkey']],
        annotations={
            chaise_tags.foreign_key: {
                'domain_filter_pattern': 'structure_id={{structure_id}}'
            }
        },
        on_update='CASCADE',
        on_delete='SET NULL',
    ),
    em.ForeignKey.define(
        ['restraint_id', 'structure_id'],
        'PDB',
        'ihm_cross_link_restraint', ['id', 'structure_id'],
        constraint_names=[['PDB', 'ihm_cross_link_result_parameters_restraint_id_fkey']],
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
