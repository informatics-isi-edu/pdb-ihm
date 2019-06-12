import argparse
from attrdict import AttrDict
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
from deriva.utils.catalog.components.deriva_model import DerivaCatalog
import deriva.core.ermrest_model as em
from deriva.core.ermrest_config import tag as chaise_tags
from deriva.utils.catalog.manage.update_catalog import CatalogUpdater, parse_args

groups = {
    'pdb-admin': 'https://auth.globus.org/0b98092c-3c41-11e9-a8c8-0ee7d80087ee',
    'pdb-reader': 'https://auth.globus.org/8875a770-3c40-11e9-a8c8-0ee7d80087ee',
    'pdb-writer': 'https://auth.globus.org/c94a1e5c-3c40-11e9-a5d1-0aacc65bfe9a',
    'pdb-curator': 'https://auth.globus.org/eef3e02a-3c40-11e9-9276-0edc9bdd56a6',
    'isrd-staff': 'https://auth.globus.org/176baec4-ed26-11e5-8e88-22000ab4b42b'
}

table_name = 'pdbx_unobs_or_zero_occ_residues'

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
    'PDB_model_num': {},
    'auth_asym_id': {},
    'auth_comp_id': {},
    'auth_seq_id': {},
    'id': {},
    'label_asym_id': {},
    'label_comp_id': {},
    'label_seq_id': {},
    'occupancy_flag': {},
    'polymer_flag': {},
    'Owner': {}
}

column_comment = {
    'structure_id': 'type:text\nThe value of _entry.id identifies the data block.\n\n Note that this item need not be a number; it can be any unique\n identifier.',
    'PDB_model_num': 'type:int4\nA unique identifier for the structural model being deposited.',
    'auth_asym_id': 'type:text\nPart of the identifier for the unobserved or zero occupancy residue.\n\n This data item is a pointer to _atom_site.auth_asym_id in the\n ATOM_SITE category.',
    'auth_comp_id': 'type:text\nThe value of _chem_comp.id must uniquely identify each item in\n the CHEM_COMP list.\n\n For protein polymer entities, this is the three-letter code for\n the amino acid.\n\n For nucleic acid polymer entities, this is the one-letter code\n for the base.',
    'auth_seq_id': 'type:text\nPart of the identifier for the unobserved or zero occupancy residue.\n\n This data item is a pointer to _atom_site.auth_seq_id in the\n ATOM_SITE category.',
    'id': 'type:int4\nThe value of _pdbx_unobs_or_zero_occ_residues.id must uniquely identify\n  each item in the PDBX_UNOBS_OR_ZERO_OCC_RESIDUES list.\n\n  This is an integer serial number.',
    'label_asym_id': 'type:text\nThe value of _struct_asym.id must uniquely identify a record in\n the STRUCT_ASYM list.\n\n Note that this item need not be a number; it can be any unique\n identifier.',
    'label_comp_id': 'type:text\nThe value of _chem_comp.id must uniquely identify each item in\n the CHEM_COMP list.\n\n For protein polymer entities, this is the three-letter code for\n the amino acid.\n\n For nucleic acid polymer entities, this is the one-letter code\n for the base.',
    'label_seq_id': 'type:int4\nPart of the identifier for the unobserved or zero occupancy residue.\n\n This data item is a pointer to _atom_site.label_seq_id in the\n ATOM_SITE category.',
    'occupancy_flag': 'type:int4\nThe value of occupancy flag indicates whether the residue\n is unobserved (= 1) or the coordinates have an occupancy of zero (=0)',
    'polymer_flag': 'type:text\nThe value of polymer flag indicates whether the unobserved or\n zero occupancy residue is part of a polymer chain or not',
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
        'PDB_model_num',
        em.builtin_types['int4'],
        nullok=False,
        comment=column_comment['PDB_model_num'],
    ),
    em.Column.define(
        'auth_asym_id',
        em.builtin_types['text'],
        nullok=False,
        comment=column_comment['auth_asym_id'],
    ),
    em.Column.define(
        'auth_comp_id',
        em.builtin_types['text'],
        nullok=False,
        comment=column_comment['auth_comp_id'],
    ),
    em.Column.define(
        'auth_seq_id',
        em.builtin_types['text'],
        nullok=False,
        comment=column_comment['auth_seq_id'],
    ),
    em.Column.define('id', em.builtin_types['int4'], nullok=False, comment=column_comment['id'],
                     ),
    em.Column.define(
        'label_asym_id', em.builtin_types['text'], comment=column_comment['label_asym_id'],
    ),
    em.Column.define(
        'label_comp_id', em.builtin_types['text'], comment=column_comment['label_comp_id'],
    ),
    em.Column.define(
        'label_seq_id', em.builtin_types['int4'], comment=column_comment['label_seq_id'],
    ),
    em.Column.define(
        'occupancy_flag',
        em.builtin_types['int4'],
        nullok=False,
        comment=column_comment['occupancy_flag'],
    ),
    em.Column.define(
        'polymer_flag',
        em.builtin_types['text'],
        nullok=False,
        comment=column_comment['polymer_flag'],
    ),
    em.Column.define('Owner', em.builtin_types['text'], comment=column_comment['Owner'],
                     ),
]

table_annotations = {}

table_comment = None

table_acls = {}

table_acl_bindings = {
    'self_service_group': {
        'types': ['update', 'delete'],
        'projection': ['Owner'],
        'projection_type': 'acl',
        'scope_acl': ['*']
    },
    'self_service_creator': {
        'types': ['update', 'delete'],
        'projection': ['RCB'],
        'projection_type': 'acl',
        'scope_acl': ['*']
    }
}

key_defs = [
    em.Key.define(['RID'], constraint_names=[('PDB', 'pdbx_unobs_or_zero_occ_residues_RIDkey1')],
                  ),
    em.Key.define(
        ['structure_id', 'id'],
        constraint_names=[('PDB', 'pdbx_unobs_or_zero_occ_residues_primary_key')],
    ),
]

fkey_defs = [
    em.ForeignKey.define(
        ['polymer_flag'],
        'Vocab',
        'pdbx_unobs_or_zero_occ_residues_polymer_flag_term', ['ID'],
        constraint_names=[('PDB', 'pdbx_unobs_or_zero_occ_residues_polymer_flag_term_fkey')],
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
        constraint_names=[('PDB', 'pdbx_unobs_or_zero_occ_residues_Owner_fkey')],
        acls={
            'insert': [groups['pdb-curator']],
            'update': [groups['pdb-curator']]
        },
        acl_bindings={
            'set_owner': {
                'types': ['update', 'insert'],
                'projection': ['ID'],
                'projection_type': 'acl',
                'scope_acl': ['*']
            }
        },
    ),
    em.ForeignKey.define(
        ['RCB'],
        'public',
        'ERMrest_Client', ['ID'],
        constraint_names=[('PDB', 'pdbx_unobs_or_zero_occ_residues_RCB_fkey')],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
    ),
    em.ForeignKey.define(
        ['RMB'],
        'public',
        'ERMrest_Client', ['ID'],
        constraint_names=[('PDB', 'pdbx_unobs_or_zero_occ_residues_RMB_fkey')],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
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
    updater.update_table(mode, schema_name, table_def, replace=replace, really=really)


if __name__ == "__main__":
    host = 'pdb.isrd.isi.edu'
    catalog_id = 5
    mode, replace, host, catalog_id = parse_args(host, catalog_id, is_table=True)
    catalog = DerivaCatalog(host, catalog_id=catalog_id, validate=False)
    main(catalog, mode, replace)

