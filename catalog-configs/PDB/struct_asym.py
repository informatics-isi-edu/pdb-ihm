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

table_name = 'struct_asym'

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
    'details': {},
    'entity_id': {},
    'id': {},
    'pdbx_PDB_id': {},
    'pdbx_alt_id': {},
    'pdbx_blank_PDB_chainid_flag': {},
    'pdbx_modified': {},
    'pdbx_order': {},
    'pdbx_type': {},
    'Owner': {}
}

column_comment = {
    'structure_id': 'type:text\nThe value of _entry.id identifies the data block.\n\n Note that this item need not be a number; it can be any unique\n identifier.',
    'details': 'type:text\nA description of special aspects of this portion of the contents\n of the asymmetric unit.\nexamples:The drug binds to this enzyme in two roughly\n                                  twofold symmetric modes. Hence this\n                                  biological unit (3) is roughly twofold\n                                  symmetric to biological unit (2). Disorder in\n                                  the protein chain indicated with alternative\n                                  ID 2 should be used with this biological unit.',
    'entity_id': 'type:text\nThe value of _entity.id must uniquely identify a record in the\n ENTITY list.\n\n Note that this item need not be a number; it can be any unique\n identifier.',
    'id': 'type:text\nThe value of _struct_asym.id must uniquely identify a record in\n the STRUCT_ASYM list.\n\n Note that this item need not be a number; it can be any unique\n identifier.\nexamples:1,A,2B3',
    'pdbx_PDB_id': 'type:text\nThis data item is a pointer to _atom_site.pdbx_PDB_strand_id the\n ATOM_SITE category.\nexamples:1ABC',
    'pdbx_alt_id': 'type:text\nThis data item is a pointer to _atom_site.ndb_alias_strand_id the\n ATOM_SITE category.',
    'pdbx_blank_PDB_chainid_flag': 'type:text\nA flag indicating that this entity was originally labeled\n with a blank PDB chain id.',
    'pdbx_modified': 'type:text\nThis data item indicates whether the structural elements are modified.\nexamples:y',
    'pdbx_order': 'type:int4\nThis data item gives the order of the structural elements in the\n ATOM_SITE category.',
    'pdbx_type': 'type:text\nThis data item describes the general type of the structural elements\n in the ATOM_SITE category.',
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
    em.Column.define('details', em.builtin_types['text'], comment=column_comment['details'],
                     ),
    em.Column.define(
        'entity_id', em.builtin_types['text'], nullok=False, comment=column_comment['entity_id'],
    ),
    em.Column.define('id', em.builtin_types['text'], nullok=False, comment=column_comment['id'],
                     ),
    em.Column.define(
        'pdbx_PDB_id', em.builtin_types['text'], comment=column_comment['pdbx_PDB_id'],
    ),
    em.Column.define(
        'pdbx_alt_id', em.builtin_types['text'], comment=column_comment['pdbx_alt_id'],
    ),
    em.Column.define(
        'pdbx_blank_PDB_chainid_flag',
        em.builtin_types['text'],
        comment=column_comment['pdbx_blank_PDB_chainid_flag'],
    ),
    em.Column.define(
        'pdbx_modified', em.builtin_types['text'], comment=column_comment['pdbx_modified'],
    ),
    em.Column.define(
        'pdbx_order', em.builtin_types['int4'], comment=column_comment['pdbx_order'],
    ),
    em.Column.define('pdbx_type', em.builtin_types['text'], comment=column_comment['pdbx_type'],
                     ),
    em.Column.define('Owner', em.builtin_types['text'], comment=column_comment['Owner'],
                     ),
]

visible_columns = {
    '*': [
        'RID',
        {
            'source': [{
                'outbound': ['PDB', 'struct_asym_structure_id_fkey']
            }, 'RID'],
            'comment': 'type:text\nThe value of _entry.id identifies the data block.\n\n Note that this item need not be a number; it can be any unique\n identifier.',
            'markdown_name': 'structure id'
        }, 'details',
        {
            'source': [{
                'outbound': ['PDB', 'struct_asym_entity_id_fkey']
            }, 'RID'],
            'comment': 'type:text\nThe value of _entity.id must uniquely identify a record in the\n ENTITY list.\n\n Note that this item need not be a number; it can be any unique\n identifier.',
            'markdown_name': 'entity id'
        }, 'id', 'pdbx_PDB_id', 'pdbx_alt_id',
        ['PDB', 'struct_asym_pdbx_blank_PDB_chainid_flag_term_fkey'], 'pdbx_modified', 'pdbx_order',
        ['PDB', 'struct_asym_pdbx_type_term_fkey'], ['PDB', 'struct_asym_RCB_fkey'],
        ['PDB', 'struct_asym_RMB_fkey'], 'RCT', 'RMT', ['PDB', 'struct_asym_Owner_fkey']
    ],
    'entry': [
        {
            'source': [{
                'outbound': ['PDB', 'struct_asym_structure_id_fkey']
            }, 'RID'],
            'comment': 'type:text\nThe value of _entry.id identifies the data block.\n\n Note that this item need not be a number; it can be any unique\n identifier.',
            'markdown_name': 'structure id'
        }, 'details',
        {
            'source': [{
                'outbound': ['PDB', 'struct_asym_entity_id_fkey']
            }, 'RID'],
            'comment': 'type:text\nThe value of _entity.id must uniquely identify a record in the\n ENTITY list.\n\n Note that this item need not be a number; it can be any unique\n identifier.',
            'markdown_name': 'entity id'
        }, 'id', 'pdbx_PDB_id', 'pdbx_alt_id',
        ['PDB', 'struct_asym_pdbx_blank_PDB_chainid_flag_term_fkey'], 'pdbx_modified', 'pdbx_order',
        ['PDB', 'struct_asym_pdbx_type_term_fkey']
    ]
}

visible_foreign_keys = {
    'filter': 'detailed',
    'detailed': [
        ['PDB', 'pdbx_poly_seq_scheme_asym_id_fkey'],
        ['PDB', 'ihm_model_representation_details_entity_asym_id_fkey'],
        ['PDB', 'ihm_struct_assembly_details_asym_id_fkey'],
        ['PDB', 'ihm_starting_model_details_asym_id_fkey'],
        ['PDB', 'ihm_starting_model_seq_dif_asym_id_fkey'],
        ['PDB', 'ihm_cross_link_restraint_asym_id_1_fkey'],
        ['PDB', 'ihm_cross_link_restraint_asym_id_2_fkey'],
        ['PDB', 'ihm_predicted_contact_restraint_asym_id_1_fkey'],
        ['PDB', 'ihm_predicted_contact_restraint_asym_id_2_fkey'],
        ['PDB', 'ihm_hydroxyl_radical_fp_restraint_asym_id_fkey'],
        ['PDB', 'ihm_poly_atom_feature_asym_id_fkey'],
        ['PDB', 'ihm_poly_residue_feature_asym_id_fkey'],
        ['PDB', 'ihm_non_poly_feature_asym_id_fkey'],
        ['PDB', 'ihm_interface_residue_feature_binding_partner_asym_id_fkey'],
        ['PDB', 'ihm_residues_not_modeled_asym_id_fkey'], ['PDB', 'atom_site_label_asym_id_fkey'],
        ['PDB', 'ihm_sphere_obj_site_asym_id_fkey'], ['PDB', 'ihm_gaussian_obj_site_asym_id_fkey'],
        ['PDB', 'ihm_starting_model_coord_asym_id_fkey'],
        ['PDB', 'ihm_localization_density_files_asym_id_fkey'],
        ['PDB', 'ihm_gaussian_obj_ensemble_asym_id_fkey']
    ]
}

table_display = {'row_name': {'row_markdown_pattern': '{{{id}}}'}}

table_annotations = {
    chaise_tags.table_display: table_display,
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
    em.Key.define(['RID'], constraint_names=[('PDB', 'struct_asym_RIDkey1')],
                  ),
    em.Key.define(['structure_id', 'id'], constraint_names=[('PDB', 'struct_asym_primary_key')],
                  ),
]

fkey_defs = [
    em.ForeignKey.define(
        ['pdbx_blank_PDB_chainid_flag'],
        'Vocab',
        'struct_asym_pdbx_blank_PDB_chainid_flag_term', ['ID'],
        constraint_names=[('PDB', 'struct_asym_pdbx_blank_PDB_chainid_flag_term_fkey')],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
        on_update='CASCADE',
        on_delete='SET NULL',
    ),
    em.ForeignKey.define(
        ['pdbx_type'],
        'Vocab',
        'struct_asym_pdbx_type_term', ['ID'],
        constraint_names=[('PDB', 'struct_asym_pdbx_type_term_fkey')],
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
        constraint_names=[('PDB', 'struct_asym_Owner_fkey')],
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
        constraint_names=[('PDB', 'struct_asym_RCB_fkey')],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
    ),
    em.ForeignKey.define(
        ['RMB'],
        'public',
        'ERMrest_Client', ['ID'],
        constraint_names=[('PDB', 'struct_asym_RMB_fkey')],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
    ),
    em.ForeignKey.define(
        ['structure_id'],
        'PDB',
        'entry', ['id'],
        constraint_names=[('PDB', 'struct_asym_structure_id_fkey')],
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
        constraint_names=[('PDB', 'struct_asym_entity_id_fkey')],
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

