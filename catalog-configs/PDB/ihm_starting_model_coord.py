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

table_name = 'ihm_starting_model_coord'

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
    'B_iso_or_equiv': {},
    'Cartn_x': {},
    'Cartn_y': {},
    'Cartn_z': {},
    'asym_id': {},
    'atom_id': {},
    'comp_id': {},
    'entity_id': {},
    'formal_charge': {},
    'group_PDB': {},
    'id': {},
    'ordinal_id': {
        chaise_tags.generated: None
    },
    'seq_id': {},
    'starting_model_id': {},
    'type_symbol': {},
    'Owner': {}
}

column_comment = {
    'structure_id': 'type:text\nThe value of _entry.id identifies the data block.\n\n Note that this item need not be a number; it can be any unique\n identifier.',
    'B_iso_or_equiv': 'type:float4\nThe isotropic temperature factor corresponding to this coordinate position.',
    'Cartn_x': 'type:float4\nThe Cartesian X component corresponding to this coordinate position.',
    'Cartn_y': 'type:float4\nThe Cartesian Y component corresponding to this coordinate position.',
    'Cartn_z': 'type:float4\nThe Cartesian Z component corresponding to this coordinate position.',
    'asym_id': 'type:text\nThe value of _struct_asym.id must uniquely identify a record in\n the STRUCT_ASYM list.\n\n Note that this item need not be a number; it can be any unique\n identifier.',
    'atom_id': 'type:text\nThe atom identifier/name corresponding to this coordinate position.\n This data item is a pointer to _chem_comp_atom.atom_id in the \n CHEM_COMP_ATOM category.',
    'comp_id': 'type:text\nThe value of _chem_comp.id must uniquely identify each item in\n the CHEM_COMP list.\n\n For protein polymer entities, this is the three-letter code for\n the amino acid.\n\n For nucleic acid polymer entities, this is the one-letter code\n for the base.',
    'entity_id': 'type:text\nThe value of _entity.id must uniquely identify a record in the\n ENTITY list.\n\n Note that this item need not be a number; it can be any unique\n identifier.',
    'formal_charge': 'type:int4\nThe formal charge corresponding to this coordinate position.',
    'group_PDB': 'type:text\nThe group of atoms to which the atom site in the starting model belongs. This data\n item is provided for compatibility with the original Protein Data Bank format, \n and only for that purpose.',
    'id': 'type:int4\nThe serial number for this coordinate position.',
    'ordinal_id': 'type:int4\nA unique identifier for this coordinate position.',
    'seq_id': 'type:int4\nThe value of _entity_poly_seq.num must uniquely and sequentially\n identify a record in the ENTITY_POLY_SEQ list.\n\n Note that this item must be a number and that the sequence\n numbers must progress in increasing numerical order.',
    'starting_model_id': 'type:text\nA unique identifier for the starting structural model.',
    'type_symbol': 'type:text\nThe atom type symbol(element symbol) corresponding to this coordinate position.',
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
        'B_iso_or_equiv', em.builtin_types['float4'], comment=column_comment['B_iso_or_equiv'],
    ),
    em.Column.define(
        'Cartn_x', em.builtin_types['float4'], nullok=False, comment=column_comment['Cartn_x'],
    ),
    em.Column.define(
        'Cartn_y', em.builtin_types['float4'], nullok=False, comment=column_comment['Cartn_y'],
    ),
    em.Column.define(
        'Cartn_z', em.builtin_types['float4'], nullok=False, comment=column_comment['Cartn_z'],
    ),
    em.Column.define(
        'asym_id', em.builtin_types['text'], nullok=False, comment=column_comment['asym_id'],
    ),
    em.Column.define(
        'atom_id', em.builtin_types['text'], nullok=False, comment=column_comment['atom_id'],
    ),
    em.Column.define(
        'comp_id', em.builtin_types['text'], nullok=False, comment=column_comment['comp_id'],
    ),
    em.Column.define(
        'entity_id', em.builtin_types['text'], nullok=False, comment=column_comment['entity_id'],
    ),
    em.Column.define(
        'formal_charge', em.builtin_types['int4'], comment=column_comment['formal_charge'],
    ),
    em.Column.define('group_PDB', em.builtin_types['text'], comment=column_comment['group_PDB'],
                     ),
    em.Column.define('id', em.builtin_types['int4'], nullok=False, comment=column_comment['id'],
                     ),
    em.Column.define(
        'ordinal_id',
        em.builtin_types['int4'],
        nullok=False,
        annotations=column_annotations['ordinal_id'],
        comment=column_comment['ordinal_id'],
    ),
    em.Column.define(
        'seq_id', em.builtin_types['int4'], nullok=False, comment=column_comment['seq_id'],
    ),
    em.Column.define(
        'starting_model_id',
        em.builtin_types['text'],
        nullok=False,
        comment=column_comment['starting_model_id'],
    ),
    em.Column.define(
        'type_symbol',
        em.builtin_types['text'],
        nullok=False,
        comment=column_comment['type_symbol'],
    ),
    em.Column.define('Owner', em.builtin_types['text'], comment=column_comment['Owner'],
                     ),
]

visible_columns = {
    '*': [
        'RID',
        {
            'source': [{
                'outbound': ['PDB', 'ihm_starting_model_coord_structure_id_fkey']
            }, 'RID'],
            'comment': 'type:text\nThe value of _entry.id identifies the data block.\n\n Note that this item need not be a number; it can be any unique\n identifier.',
            'markdown_name': 'structure id'
        }, 'B_iso_or_equiv', 'Cartn_x', 'Cartn_y', 'Cartn_z',
        {
            'source': [{
                'outbound': ['PDB', 'ihm_starting_model_coord_asym_id_fkey']
            }, 'RID'],
            'comment': 'type:text\nThe value of _struct_asym.id must uniquely identify a record in\n the STRUCT_ASYM list.\n\n Note that this item need not be a number; it can be any unique\n identifier.',
            'markdown_name': 'asym id'
        }, 'atom_id',
        {
            'source': [{
                'outbound': ['PDB', 'ihm_starting_model_coord_comp_id_fkey']
            }, 'RID'],
            'comment': 'type:text\nThe value of _chem_comp.id must uniquely identify each item in\n the CHEM_COMP list.\n\n For protein polymer entities, this is the three-letter code for\n the amino acid.\n\n For nucleic acid polymer entities, this is the one-letter code\n for the base.',
            'markdown_name': 'comp id'
        },
        {
            'source': [{
                'outbound': ['PDB', 'ihm_starting_model_coord_entity_id_fkey']
            }, 'RID'],
            'comment': 'type:text\nThe value of _entity.id must uniquely identify a record in the\n ENTITY list.\n\n Note that this item need not be a number; it can be any unique\n identifier.',
            'markdown_name': 'entity id'
        }, 'formal_charge', ['PDB', 'ihm_starting_model_coord_group_PDB_term_fkey'], 'id',
        'ordinal_id',
        {
            'source': [{
                'outbound': ['PDB', 'ihm_starting_model_coord_seq_id_fkey']
            }, 'RID'],
            'comment': 'type:int4\nThe value of _entity_poly_seq.num must uniquely and sequentially\n identify a record in the ENTITY_POLY_SEQ list.\n\n Note that this item must be a number and that the sequence\n numbers must progress in increasing numerical order.',
            'markdown_name': 'seq id'
        },
        {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_starting_model_coord_starting_model_id_fkey']
                }, 'RID'
            ],
            'comment': 'type:text\nA unique identifier for the starting structural model.',
            'markdown_name': 'starting model id'
        }, 'type_symbol', ['PDB', 'ihm_starting_model_coord_RCB_fkey'],
        ['PDB', 'ihm_starting_model_coord_RMB_fkey'], 'RCT', 'RMT',
        ['PDB', 'ihm_starting_model_coord_Owner_fkey']
    ],
    'entry': [
        {
            'source': [{
                'outbound': ['PDB', 'ihm_starting_model_coord_structure_id_fkey']
            }, 'RID'],
            'comment': 'type:text\nThe value of _entry.id identifies the data block.\n\n Note that this item need not be a number; it can be any unique\n identifier.',
            'markdown_name': 'structure id'
        }, 'B_iso_or_equiv', 'Cartn_x', 'Cartn_y', 'Cartn_z',
        {
            'source': [{
                'outbound': ['PDB', 'ihm_starting_model_coord_asym_id_fkey']
            }, 'RID'],
            'comment': 'type:text\nThe value of _struct_asym.id must uniquely identify a record in\n the STRUCT_ASYM list.\n\n Note that this item need not be a number; it can be any unique\n identifier.',
            'markdown_name': 'asym id'
        }, 'atom_id',
        {
            'source': [{
                'outbound': ['PDB', 'ihm_starting_model_coord_comp_id_fkey']
            }, 'RID'],
            'comment': 'type:text\nThe value of _chem_comp.id must uniquely identify each item in\n the CHEM_COMP list.\n\n For protein polymer entities, this is the three-letter code for\n the amino acid.\n\n For nucleic acid polymer entities, this is the one-letter code\n for the base.',
            'markdown_name': 'comp id'
        },
        {
            'source': [{
                'outbound': ['PDB', 'ihm_starting_model_coord_entity_id_fkey']
            }, 'RID'],
            'comment': 'type:text\nThe value of _entity.id must uniquely identify a record in the\n ENTITY list.\n\n Note that this item need not be a number; it can be any unique\n identifier.',
            'markdown_name': 'entity id'
        }, 'formal_charge', ['PDB', 'ihm_starting_model_coord_group_PDB_term_fkey'], 'id',
        'ordinal_id',
        {
            'source': [{
                'outbound': ['PDB', 'ihm_starting_model_coord_seq_id_fkey']
            }, 'RID'],
            'comment': 'type:int4\nThe value of _entity_poly_seq.num must uniquely and sequentially\n identify a record in the ENTITY_POLY_SEQ list.\n\n Note that this item must be a number and that the sequence\n numbers must progress in increasing numerical order.',
            'markdown_name': 'seq id'
        },
        {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_starting_model_coord_starting_model_id_fkey']
                }, 'RID'
            ],
            'comment': 'type:text\nA unique identifier for the starting structural model.',
            'markdown_name': 'starting model id'
        }, 'type_symbol'
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
    em.Key.define(['RID'], constraint_names=[('PDB', 'ihm_starting_model_coord_RIDkey1')],
                  ),
    em.Key.define(
        ['structure_id', 'ordinal_id'],
        constraint_names=[('PDB', 'ihm_starting_model_coord_primary_key')],
    ),
]

fkey_defs = [
    em.ForeignKey.define(
        ['group_PDB'],
        'Vocab',
        'ihm_starting_model_coord_group_PDB_term', ['ID'],
        constraint_names=[('PDB', 'ihm_starting_model_coord_group_PDB_term_fkey')],
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
        constraint_names=[('PDB', 'ihm_starting_model_coord_Owner_fkey')],
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
        constraint_names=[('PDB', 'ihm_starting_model_coord_RCB_fkey')],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
    ),
    em.ForeignKey.define(
        ['RMB'],
        'public',
        'ERMrest_Client', ['ID'],
        constraint_names=[('PDB', 'ihm_starting_model_coord_RMB_fkey')],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
    ),
    em.ForeignKey.define(
        ['structure_id'],
        'PDB',
        'entry', ['id'],
        constraint_names=[('PDB', 'ihm_starting_model_coord_structure_id_fkey')],
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
        constraint_names=[('PDB', 'ihm_starting_model_coord_asym_id_fkey')],
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
        ['structure_id', 'comp_id'],
        'PDB',
        'chem_comp', ['structure_id', 'id'],
        constraint_names=[('PDB', 'ihm_starting_model_coord_comp_id_fkey')],
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
        ['structure_id', 'entity_id'],
        'PDB',
        'entity', ['structure_id', 'id'],
        constraint_names=[('PDB', 'ihm_starting_model_coord_entity_id_fkey')],
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
        ['structure_id', 'starting_model_id'],
        'PDB',
        'ihm_starting_model_details', ['structure_id', 'starting_model_id'],
        constraint_names=[('PDB', 'ihm_starting_model_coord_starting_model_id_fkey')],
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
    updater.update_table(mode, schema_name, table_def, replace=replace, really=really)


if __name__ == "__main__":
    host = 'pdb.isrd.isi.edu'
    catalog_id = 5
    mode, replace, host, catalog_id = parse_args(host, catalog_id, is_table=True)
    catalog = DerivaCatalog(host, catalog_id=catalog_id, validate=False)
    main(catalog, mode, replace)

