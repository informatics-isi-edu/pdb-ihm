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

table_name = 'entity_poly_seq'

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
    chaise_tags.visible_columns: visible_columns,
    chaise_tags.visible_foreign_keys: visible_foreign_keys,
}

table_comment = None

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
    em.Key.define(['RID'], constraint_names=[['PDB', 'entity_poly_seq_RIDkey1']],
                  ),
    em.Key.define(
        ['entity_id', 'structure_id', 'num', 'mon_id'],
        constraint_names=[['PDB', 'entity_poly_seq_primary_key']],
    ),
]

fkey_defs = [
    em.ForeignKey.define(
        ['hetero'],
        'Vocab',
        'entity_poly_seq_hetero', ['ID'],
        constraint_names=[['PDB', 'entity_poly_seq_hetero_fkey']],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
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
        constraint_names=[['PDB', 'entity_poly_seq_Owner_fkey']],
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
        ['structure_id', 'mon_id'],
        'PDB',
        'chem_comp', ['structure_id', 'id'],
        constraint_names=[['PDB', 'entity_poly_seq_mon_id_fkey']],
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
        constraint_names=[['PDB', 'entity_poly_seq_RMB_fkey']],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
    ),
    em.ForeignKey.define(
        ['RCB'],
        'public',
        'ERMrest_Client', ['ID'],
        constraint_names=[['PDB', 'entity_poly_seq_RCB_fkey']],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
    ),
    em.ForeignKey.define(
        ['structure_id'],
        'PDB',
        'entry', ['id'],
        constraint_names=[['PDB', 'entity_poly_seq_structure_id_fkey']],
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
