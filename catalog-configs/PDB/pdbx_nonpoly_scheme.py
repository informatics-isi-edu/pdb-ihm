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

table_name = 'pdbx_nonpoly_scheme'

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
    'auth_mon_id': {},
    'auth_seq_num': {},
    'entity_id': {},
    'mon_id': {},
    'ndb_seq_num': {},
    'pdb_mon_id': {},
    'pdb_seq_num': {},
    'pdb_strand_id': {},
    'Owner': {}
}

column_comment = {
    'structure_id': 'type:text\nThe value of _entry.id identifies the data block.\n\n Note that this item need not be a number; it can be any unique\n identifier.',
    'asym_id': 'type:text\nThe value of _struct_asym.id must uniquely identify a record in\n the STRUCT_ASYM list.\n\n Note that this item need not be a number; it can be any unique\n identifier.',
    'auth_mon_id': 'type:text\nAuthor provided residue identifier.   This value may differ from the PDB residue\n identifier and may not correspond to residue identification within the coordinate records.',
    'auth_seq_num': 'type:text\nAuthor provided residue numbering.   This value may differ from the PDB residue\n number and may not correspond to residue numbering within the coordinate records.\n',
    'entity_id': 'type:text\nThe value of _entity.id must uniquely identify a record in the\n ENTITY list.\n\n Note that this item need not be a number; it can be any unique\n identifier.',
    'mon_id': 'type:text\nThe value of _chem_comp.id must uniquely identify each item in\n the CHEM_COMP list.\n\n For protein polymer entities, this is the three-letter code for\n the amino acid.\n\n For nucleic acid polymer entities, this is the one-letter code\n for the base.',
    'ndb_seq_num': 'type:text\nNDB/RCSB residue number.',
    'pdb_mon_id': 'type:text\nPDB residue identifier.',
    'pdb_seq_num': 'type:text\nPDB residue number.',
    'pdb_strand_id': 'type:text\nPDB strand/chain id.',
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
        'auth_mon_id', em.builtin_types['text'], comment=column_comment['auth_mon_id'],
    ),
    em.Column.define(
        'auth_seq_num', em.builtin_types['text'], comment=column_comment['auth_seq_num'],
    ),
    em.Column.define('entity_id', em.builtin_types['text'], comment=column_comment['entity_id'],
                     ),
    em.Column.define('mon_id', em.builtin_types['text'], comment=column_comment['mon_id'],
                     ),
    em.Column.define(
        'ndb_seq_num',
        em.builtin_types['text'],
        nullok=False,
        comment=column_comment['ndb_seq_num'],
    ),
    em.Column.define(
        'pdb_mon_id', em.builtin_types['text'], comment=column_comment['pdb_mon_id'],
    ),
    em.Column.define(
        'pdb_seq_num', em.builtin_types['text'], comment=column_comment['pdb_seq_num'],
    ),
    em.Column.define(
        'pdb_strand_id', em.builtin_types['text'], comment=column_comment['pdb_strand_id'],
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
    em.Key.define(['RID'], constraint_names=[('PDB', 'pdbx_nonpoly_scheme_RIDkey1')],
                  ),
    em.Key.define(
        ['structure_id', 'asym_id', 'ndb_seq_num'],
        constraint_names=[('PDB', 'pdbx_nonpoly_scheme_primary_key')],
    ),
]

fkey_defs = [
    em.ForeignKey.define(
        ['Owner'],
        'public',
        'Catalog_Group', ['ID'],
        constraint_names=[('PDB', 'pdbx_nonpoly_scheme_Owner_fkey')],
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
        constraint_names=[('PDB', 'pdbx_nonpoly_scheme_RCB_fkey')],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
    ),
    em.ForeignKey.define(
        ['RMB'],
        'public',
        'ERMrest_Client', ['ID'],
        constraint_names=[('PDB', 'pdbx_nonpoly_scheme_RMB_fkey')],
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

