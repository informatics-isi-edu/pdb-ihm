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

table_name = 'pdbx_poly_seq_scheme'

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
    'hetero': {},
    'mon_id': {},
    'ndb_seq_num': {},
    'pdb_mon_id': {},
    'pdb_seq_num': {},
    'pdb_strand_id': {},
    'seq_id': {},
    'Owner': {}
}

column_comment = {
    'structure_id': 'type:text\nThe value of _entry.id identifies the data block.\n\n Note that this item need not be a number; it can be any unique\n identifier.',
    'asym_id': 'type:text\nThe value of _struct_asym.id must uniquely identify a record in\n the STRUCT_ASYM list.\n\n Note that this item need not be a number; it can be any unique\n identifier.',
    'auth_mon_id': 'type:text\nAuthor provided residue identifier.   This value may differ from the PDB residue\n identifier and may not correspond to residue identifier within the coordinate records.',
    'auth_seq_num': 'type:text\nAuthor provided residue number.   This value may differ from the PDB residue\n number and may not correspond to residue numbering within the coordinate records.\n',
    'entity_id': 'type:text\nThe value of _entity.id must uniquely identify a record in the\n ENTITY list.\n\n Note that this item need not be a number; it can be any unique\n identifier.',
    'hetero': 'type:text\nPointer to _entity_poly_seq.hetero',
    'mon_id': 'type:text\nThe value of _chem_comp.id must uniquely identify each item in\n the CHEM_COMP list.\n\n For protein polymer entities, this is the three-letter code for\n the amino acid.\n\n For nucleic acid polymer entities, this is the one-letter code\n for the base.',
    'ndb_seq_num': 'type:int4\nNDB residue number.',
    'pdb_mon_id': 'type:text\nPDB residue identifier.',
    'pdb_seq_num': 'type:text\nPDB residue number.',
    'pdb_strand_id': 'type:text\nPDB strand/chain id.',
    'seq_id': 'type:int4\nThe value of _entity_poly_seq.num must uniquely and sequentially\n identify a record in the ENTITY_POLY_SEQ list.\n\n Note that this item must be a number and that the sequence\n numbers must progress in increasing numerical order.',
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
    em.Column.define(
        'entity_id', em.builtin_types['text'], nullok=False, comment=column_comment['entity_id'],
    ),
    em.Column.define('hetero', em.builtin_types['text'], comment=column_comment['hetero'],
                     ),
    em.Column.define(
        'mon_id', em.builtin_types['text'], nullok=False, comment=column_comment['mon_id'],
    ),
    em.Column.define(
        'ndb_seq_num', em.builtin_types['int4'], comment=column_comment['ndb_seq_num'],
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
    em.Column.define(
        'seq_id', em.builtin_types['int4'], nullok=False, comment=column_comment['seq_id'],
    ),
    em.Column.define('Owner', em.builtin_types['text'], comment=column_comment['Owner'],
                     ),
]

visible_columns = {
    '*': [
        'RID',
        {
            'source': [{
                'outbound': ['PDB', 'pdbx_poly_seq_scheme_structure_id_fkey']
            }, 'RID'],
            'comment': 'type:text\nThe value of _entry.id identifies the data block.\n\n Note that this item need not be a number; it can be any unique\n identifier.',
            'markdown_name': 'structure id'
        },
        {
            'source': [{
                'outbound': ['PDB', 'pdbx_poly_seq_scheme_asym_id_fkey']
            }, 'RID'],
            'comment': 'type:text\nThe value of _struct_asym.id must uniquely identify a record in\n the STRUCT_ASYM list.\n\n Note that this item need not be a number; it can be any unique\n identifier.',
            'markdown_name': 'asym id'
        }, 'auth_mon_id', 'auth_seq_num',
        {
            'source': [{
                'outbound': ['PDB', 'pdbx_poly_seq_scheme_entity_id_fkey']
            }, 'RID'],
            'comment': 'type:text\nThe value of _entity.id must uniquely identify a record in the\n ENTITY list.\n\n Note that this item need not be a number; it can be any unique\n identifier.',
            'markdown_name': 'entity id'
        }, ['PDB', 'pdbx_poly_seq_scheme_hetero_term_fkey'],
        {
            'source': [{
                'outbound': ['PDB', 'pdbx_poly_seq_scheme_mon_id_fkey']
            }, 'RID'],
            'comment': 'type:text\nThe value of _chem_comp.id must uniquely identify each item in\n the CHEM_COMP list.\n\n For protein polymer entities, this is the three-letter code for\n the amino acid.\n\n For nucleic acid polymer entities, this is the one-letter code\n for the base.',
            'markdown_name': 'mon id'
        }, 'ndb_seq_num', 'pdb_mon_id', 'pdb_seq_num', 'pdb_strand_id',
        {
            'source': [{
                'outbound': ['PDB', 'pdbx_poly_seq_scheme_seq_id_fkey']
            }, 'RID'],
            'comment': 'type:int4\nThe value of _entity_poly_seq.num must uniquely and sequentially\n identify a record in the ENTITY_POLY_SEQ list.\n\n Note that this item must be a number and that the sequence\n numbers must progress in increasing numerical order.',
            'markdown_name': 'seq id'
        }, ['PDB', 'pdbx_poly_seq_scheme_RCB_fkey'], ['PDB', 'pdbx_poly_seq_scheme_RMB_fkey'],
        'RCT', 'RMT', ['PDB', 'pdbx_poly_seq_scheme_Owner_fkey']
    ],
    'entry': [
        {
            'source': [{
                'outbound': ['PDB', 'pdbx_poly_seq_scheme_structure_id_fkey']
            }, 'RID'],
            'comment': 'type:text\nThe value of _entry.id identifies the data block.\n\n Note that this item need not be a number; it can be any unique\n identifier.',
            'markdown_name': 'structure id'
        },
        {
            'source': [{
                'outbound': ['PDB', 'pdbx_poly_seq_scheme_asym_id_fkey']
            }, 'RID'],
            'comment': 'type:text\nThe value of _struct_asym.id must uniquely identify a record in\n the STRUCT_ASYM list.\n\n Note that this item need not be a number; it can be any unique\n identifier.',
            'markdown_name': 'asym id'
        }, 'auth_mon_id', 'auth_seq_num',
        {
            'source': [{
                'outbound': ['PDB', 'pdbx_poly_seq_scheme_entity_id_fkey']
            }, 'RID'],
            'comment': 'type:text\nThe value of _entity.id must uniquely identify a record in the\n ENTITY list.\n\n Note that this item need not be a number; it can be any unique\n identifier.',
            'markdown_name': 'entity id'
        }, ['PDB', 'pdbx_poly_seq_scheme_hetero_term_fkey'],
        {
            'source': [{
                'outbound': ['PDB', 'pdbx_poly_seq_scheme_mon_id_fkey']
            }, 'RID'],
            'comment': 'type:text\nThe value of _chem_comp.id must uniquely identify each item in\n the CHEM_COMP list.\n\n For protein polymer entities, this is the three-letter code for\n the amino acid.\n\n For nucleic acid polymer entities, this is the one-letter code\n for the base.',
            'markdown_name': 'mon id'
        }, 'ndb_seq_num', 'pdb_mon_id', 'pdb_seq_num', 'pdb_strand_id',
        {
            'source': [{
                'outbound': ['PDB', 'pdbx_poly_seq_scheme_seq_id_fkey']
            }, 'RID'],
            'comment': 'type:int4\nThe value of _entity_poly_seq.num must uniquely and sequentially\n identify a record in the ENTITY_POLY_SEQ list.\n\n Note that this item must be a number and that the sequence\n numbers must progress in increasing numerical order.',
            'markdown_name': 'seq id'
        }
    ]
}

table_annotations = {chaise_tags.visible_columns: visible_columns, }

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
    em.Key.define(['RID'], constraint_names=[('PDB', 'pdbx_poly_seq_scheme_RIDkey1')],
                  ),
    em.Key.define(
        ['structure_id', 'asym_id', 'entity_id', 'mon_id', 'seq_id'],
        constraint_names=[('PDB', 'pdbx_poly_seq_scheme_primary_key')],
    ),
]

fkey_defs = [
    em.ForeignKey.define(
        ['hetero'],
        'Vocab',
        'pdbx_poly_seq_scheme_hetero_term', ['ID'],
        constraint_names=[('PDB', 'pdbx_poly_seq_scheme_hetero_term_fkey')],
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
        constraint_names=[('PDB', 'pdbx_poly_seq_scheme_Owner_fkey')],
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
        ['RCB'],
        'public',
        'ERMrest_Client', ['ID'],
        constraint_names=[('PDB', 'pdbx_poly_seq_scheme_RCB_fkey')],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
    ),
    em.ForeignKey.define(
        ['RMB'],
        'public',
        'ERMrest_Client', ['ID'],
        constraint_names=[('PDB', 'pdbx_poly_seq_scheme_RMB_fkey')],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
    ),
    em.ForeignKey.define(
        ['structure_id'],
        'PDB',
        'entry', ['id'],
        constraint_names=[('PDB', 'pdbx_poly_seq_scheme_structure_id_fkey')],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
        on_update='CASCADE',
        on_delete='SET NULL',
    ),
    em.ForeignKey.define(
        ['structure_id', 'asym_id'],
        'PDB',
        'struct_asym', ['structure_id', 'id'],
        constraint_names=[('PDB', 'pdbx_poly_seq_scheme_asym_id_fkey')],
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
        ['structure_id', 'entity_id', 'mon_id', 'seq_id'],
        'PDB',
        'entity_poly_seq', ['structure_id', 'entity_id', 'mon_id', 'num'],
        constraint_names=[('PDB', 'pdbx_poly_seq_scheme_composite_fkey')],
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
    updater.update_table(mode, schema_name, table_def, replace=replace, really=really)


if __name__ == "__main__":
    host = 'pdb.isrd.isi.edu'
    catalog_id = 5
    mode, replace, host, catalog_id = parse_args(host, catalog_id, is_table=True)
    catalog = DerivaCatalog(host, catalog_id=catalog_id, validate=False)
    main(catalog, mode, replace)

