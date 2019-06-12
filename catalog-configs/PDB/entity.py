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

table_name = 'entity'

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
    'formula_weight': {},
    'id': {},
    'pdbx_description': {},
    'pdbx_number_of_molecules': {},
    'src_method': {},
    'type': {},
    'Owner': {}
}

column_comment = {
    'structure_id': 'type:text\nThe value of _entry.id identifies the data block.\n\n Note that this item need not be a number; it can be any unique\n identifier.',
    'details': 'type:text\nA description of special aspects of the entity.',
    'formula_weight': 'type:float4\nFormula mass in daltons of the entity.',
    'id': 'type:text\nThe value of _entity.id must uniquely identify a record in the\n ENTITY list.\n\n Note that this item need not be a number; it can be any unique\n identifier.',
    'pdbx_description': "type:text\nA description of the entity.\n\n Corresponds to the compound name in the PDB format.\nexamples:DNA (5'-D(*GP*(CH3)CP*GP*(CH3)CP*GP*C)-3'),PROFLAVINE,PROTEIN (DEOXYRIBONUCLEASE I (E.C.3.1.21.1))",
    'pdbx_number_of_molecules': 'type:float4\nA place holder for the number of molecules of the entity in\n the entry.\nexamples:1.0,2.0,3.0',
    'src_method': 'type:text\nThe method by which the sample for the entity was produced.\n Entities isolated directly from natural sources (tissues, soil\n samples etc.) are expected to have further information in the\n ENTITY_SRC_NAT category. Entities isolated from genetically\n manipulated sources are expected to have further information in\n the ENTITY_SRC_GEN category.',
    'type': 'type:text\nDefines the type of the entity.\n\n Polymer entities are expected to have corresponding\n ENTITY_POLY and associated entries.\n\n Non-polymer entities are expected to have corresponding\n CHEM_COMP and associated entries.\n\n Water entities are not expected to have corresponding\n entries in the ENTITY category.',
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
        'formula_weight', em.builtin_types['float4'], comment=column_comment['formula_weight'],
    ),
    em.Column.define('id', em.builtin_types['text'], nullok=False, comment=column_comment['id'],
                     ),
    em.Column.define(
        'pdbx_description', em.builtin_types['text'], comment=column_comment['pdbx_description'],
    ),
    em.Column.define(
        'pdbx_number_of_molecules',
        em.builtin_types['float4'],
        comment=column_comment['pdbx_number_of_molecules'],
    ),
    em.Column.define(
        'src_method', em.builtin_types['text'], comment=column_comment['src_method'],
    ),
    em.Column.define('type', em.builtin_types['text'], comment=column_comment['type'],
                     ),
    em.Column.define('Owner', em.builtin_types['text'], comment=column_comment['Owner'],
                     ),
]

visible_columns = {
    '*': [
        'RID',
        {
            'source': [{
                'outbound': ['PDB', 'entity_structure_id_fkey']
            }, 'RID'],
            'comment': 'type:text\nThe value of _entry.id identifies the data block.\n\n Note that this item need not be a number; it can be any unique\n identifier.',
            'markdown_name': 'structure id'
        }, 'details', 'formula_weight', 'id', 'pdbx_description', 'pdbx_number_of_molecules',
        ['PDB', 'entity_src_method_term_fkey'], ['PDB', 'entity_type_term_fkey'],
        ['PDB', 'entity_RCB_fkey'], ['PDB', 'entity_RMB_fkey'], 'RCT', 'RMT',
        ['PDB', 'entity_Owner_fkey']
    ],
    'entry': [
        {
            'source': [{
                'outbound': ['PDB', 'entity_structure_id_fkey']
            }, 'RID'],
            'comment': 'type:text\nThe value of _entry.id identifies the data block.\n\n Note that this item need not be a number; it can be any unique\n identifier.',
            'markdown_name': 'structure id'
        }, 'details', 'formula_weight', 'id', 'pdbx_description', 'pdbx_number_of_molecules',
        ['PDB', 'entity_src_method_term_fkey'], ['PDB', 'entity_type_term_fkey']
    ]
}

visible_foreign_keys = {
    'filter': 'detailed',
    'detailed': [
        ['PDB', 'entity_poly_entity_id_fkey'], ['PDB', 'pdbx_entity_nonpoly_entity_id_fkey'],
        ['PDB', 'struct_asym_entity_id_fkey'],
        ['PDB', 'ihm_model_representation_details_entity_id_fkey'],
        ['PDB', 'ihm_struct_assembly_details_entity_id_fkey'],
        ['PDB', 'ihm_starting_model_details_entity_id_fkey'],
        ['PDB', 'ihm_non_poly_feature_entity_id_fkey'],
        ['PDB', 'ihm_interface_residue_feature_binding_partner_entity_id_fkey'],
        ['PDB', 'atom_site_label_entity_id_fkey'], ['PDB', 'ihm_sphere_obj_site_entity_id_fkey'],
        ['PDB', 'ihm_gaussian_obj_site_entity_id_fkey'],
        ['PDB', 'ihm_starting_model_coord_entity_id_fkey'],
        ['PDB', 'ihm_localization_density_files_entity_id_fkey'],
        ['PDB', 'ihm_gaussian_obj_ensemble_entity_id_fkey']
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
    em.Key.define(['RID'], constraint_names=[('PDB', 'entity_RIDkey1')],
                  ),
    em.Key.define(['structure_id', 'id'], constraint_names=[('PDB', 'entity_primary_key')],
                  ),
]

fkey_defs = [
    em.ForeignKey.define(
        ['src_method'],
        'Vocab',
        'entity_src_method_term', ['ID'],
        constraint_names=[('PDB', 'entity_src_method_term_fkey')],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
        on_update='CASCADE',
        on_delete='SET NULL',
    ),
    em.ForeignKey.define(
        ['type'],
        'Vocab',
        'entity_type_term', ['ID'],
        constraint_names=[('PDB', 'entity_type_term_fkey')],
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
        constraint_names=[('PDB', 'entity_Owner_fkey')],
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
        constraint_names=[('PDB', 'entity_RCB_fkey')],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
    ),
    em.ForeignKey.define(
        ['RMB'],
        'public',
        'ERMrest_Client', ['ID'],
        constraint_names=[('PDB', 'entity_RMB_fkey')],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
    ),
    em.ForeignKey.define(
        ['structure_id'],
        'PDB',
        'entry', ['id'],
        constraint_names=[('PDB', 'entity_structure_id_fkey')],
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

