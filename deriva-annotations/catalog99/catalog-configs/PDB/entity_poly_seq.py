import argparse
from deriva.core import ErmrestCatalog, AttrDict, get_credential
import deriva.core.ermrest_model as em
from deriva.core.ermrest_config import tag as chaise_tags
from deriva.utils.catalog.manage.update_catalog import CatalogUpdater, parse_args

groups = {}

table_name = 'entity_poly_seq'

schema_name = 'PDB'

column_annotations = {
    'structure_id': {},
    'entity_id': {},
    'hetero': {},
    'mon_id': {},
    'num': {},
    'Owner': {}
}

column_comment = {
    'structure_id': 'A reference to table entry.id.',
    'entity_id': 'A reference to table entity.id.',
    'hetero': 'type:text\nA flag to indicate whether this monomer in the polymer is\n heterogeneous in sequence.',
    'mon_id': 'A reference to table chem_comp.id.',
    'num': 'type:int4\nThe value of _entity_poly_seq.num must uniquely and sequentially\n identify a record in the ENTITY_POLY_SEQ list.\n\n Note that this item must be a number and that the sequence\n numbers must progress in increasing numerical order.',
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
        'entity_id', em.builtin_types['text'], nullok=False, comment=column_comment['entity_id'],
    ),
    em.Column.define('hetero', em.builtin_types['text'], comment=column_comment['hetero'],
                     ),
    em.Column.define(
        'mon_id', em.builtin_types['text'], nullok=False, comment=column_comment['mon_id'],
    ),
    em.Column.define(
        'num', em.builtin_types['int4'], nullok=False, comment=column_comment['num'],
    ),
    em.Column.define('Owner', em.builtin_types['text'], comment=column_comment['Owner'],
                     ),
]

generated = None

visible_columns = {
    '*': [
        'RID', {
            'source': [{
                'outbound': ['PDB', 'entity_poly_seq_structure_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table entry.id.',
            'markdown_name': 'structure id'
        }, {
            'source': [{
                'outbound': ['PDB', 'entity_poly_seq_entity_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table entity.id.',
            'markdown_name': 'entity id'
        }, {
            'source': [{
                'outbound': ['PDB', 'entity_poly_seq_mon_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table chem_comp.id.',
            'markdown_name': 'mon id'
        }, 'num', ['PDB', 'entity_poly_seq_hetero_fkey']
    ],
    'entry': [
        {
            'source': [{
                'outbound': ['PDB', 'entity_poly_seq_structure_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table entry.id.',
            'markdown_name': 'structure id'
        }, {
            'source': [{
                'outbound': ['PDB', 'entity_poly_seq_entity_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table entity.id.',
            'markdown_name': 'entity id'
        }, {
            'source': [{
                'outbound': ['PDB', 'entity_poly_seq_mon_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table chem_comp.id.',
            'markdown_name': 'mon id'
        }, 'num', ['PDB', 'entity_poly_seq_hetero_fkey']
    ]
}

visible_foreign_keys = {
    'filter': 'detailed',
    'detailed': [
        ['PDB', 'ihm_entity_poly_segment_mm_poly_res_label_begin_fkey'],
        ['PDB', 'ihm_entity_poly_segment_mm_poly_res_label_end_fkey'],
        ['PDB', 'ihm_starting_model_seq_dif_mm_poly_res_label_fkey'],
        ['PDB', 'ihm_poly_probe_position_mm_poly_res_label_fkey'],
        ['PDB', 'ihm_cross_link_list_mm_poly_res_label_1_fkey'],
        ['PDB', 'ihm_cross_link_list_mm_poly_res_label_2_fkey'],
        ['PDB', 'ihm_cross_link_restraint_mm_poly_res_label_1_fkey'],
        ['PDB', 'ihm_cross_link_restraint_mm_poly_res_label_2_fkey'],
        ['PDB', 'ihm_hydroxyl_radical_fp_restraint_mm_poly_res_label_fkey'],
        ['PDB', 'ihm_predicted_contact_restraint_mm_poly_res_label_1_fkey'],
        ['PDB', 'ihm_predicted_contact_restraint_mm_poly_res_label_2_fkey'],
        ['PDB', 'ihm_poly_atom_feature_mm_poly_res_label_fkey'],
        ['PDB', 'ihm_poly_residue_feature_mm_poly_res_label_begin_fkey'],
        ['PDB', 'ihm_poly_residue_feature_mm_poly_res_label_end_fkey'],
        ['PDB', 'ihm_residues_not_modeled_mm_poly_res_label_begin_fkey'],
        ['PDB', 'ihm_residues_not_modeled_mm_poly_res_label_end_fkey']
    ]
}

table_annotations = {
    chaise_tags.generated: generated,
    chaise_tags.visible_columns: visible_columns,
    chaise_tags.visible_foreign_keys: visible_foreign_keys,
}

table_comment = 'Sequence of monomers in polymeric entities'

table_acls = {}

table_acl_bindings = {}

key_defs = [
    em.Key.define(
        ['num', 'structure_id', 'mon_id', 'entity_id'],
        constraint_names=[['PDB', 'entity_poly_seq_primary_key']],
    ),
    em.Key.define(['RID'], constraint_names=[['PDB', 'entity_poly_seq_RIDkey1']],
                  ),
    em.Key.define(
        ['structure_id', 'RID'],
        constraint_names=[['PDB', 'entity_poly_seq_RID_structure_id_key']],
    ),
    em.Key.define(
        ['structure_id', 'RID', 'entity_id', 'mon_id', 'num'],
        constraint_names=[['PDB', 'entity_poly_seq_combo1_key']],
    ),
    em.Key.define(
        ['num', 'entity_id', 'RID', 'mon_id'],
        constraint_names=[['PDB', 'entity_poly_seq_combo2_key']],
    ),
]

fkey_defs = [
    em.ForeignKey.define(
        ['RCB'],
        'public',
        'ERMrest_Client', ['ID'],
        constraint_names=[['PDB', 'entity_poly_seq_RCB_fkey']],
    ),
    em.ForeignKey.define(
        ['RMB'],
        'public',
        'ERMrest_Client', ['ID'],
        constraint_names=[['PDB', 'entity_poly_seq_RMB_fkey']],
    ),
    em.ForeignKey.define(
        ['hetero'],
        'Vocab',
        'entity_poly_seq_hetero', ['Name'],
        constraint_names=[['PDB', 'entity_poly_seq_hetero_fkey']],
    ),
    em.ForeignKey.define(
        ['entity_id', 'structure_id'],
        'PDB',
        'entity_poly', ['entity_id', 'structure_id'],
        constraint_names=[['PDB', 'entity_poly_seq_entity_id_fkey']],
        annotations={
            chaise_tags.foreign_key: {
                'domain_filter_pattern': 'structure_id={{structure_id}}'
            }
        },
        on_update='CASCADE',
        on_delete='SET NULL',
    ),
    em.ForeignKey.define(
        ['structure_id', 'mon_id'],
        'PDB',
        'chem_comp', ['structure_id', 'id'],
        constraint_names=[['PDB', 'entity_poly_seq_mon_id_fkey']],
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
