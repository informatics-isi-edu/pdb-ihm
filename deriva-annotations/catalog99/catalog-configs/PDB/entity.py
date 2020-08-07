import argparse
from deriva.core import ErmrestCatalog, AttrDict, get_credential
import deriva.core.ermrest_model as em
from deriva.core.ermrest_config import tag as chaise_tags
from deriva.utils.catalog.manage.update_catalog import CatalogUpdater, parse_args

groups = {}

table_name = 'entity'

schema_name = 'PDB'

column_annotations = {
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
    'structure_id': 'A reference to table entry.id.',
    'details': 'type:text\nA description of special aspects of the entity.',
    'formula_weight': 'type:float4\nFormula mass in daltons of the entity.',
    'id': 'type:text\nThe value of _entity.id must uniquely identify a record in the\n ENTITY list.\n\n Note that this item need not be a number; it can be any unique\n identifier.',
    'pdbx_description': "type:text\nA description of the entity.\n\n Corresponds to the compound name in the PDB format.\nexamples:Green fluorescent protein,DNA (5'-D(*GP*(CH3)CP*GP*(CH3)CP*GP*C)-3'),PROFLAVINE,PROTEIN (DEOXYRIBONUCLEASE I (E.C.3.1.21.1))",
    'pdbx_number_of_molecules': 'type:int4\nA place holder for the number of molecules of the entity in\n the entry.\nexamples:1,2,3',
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
        em.builtin_types['int4'],
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
        'RID', {
            'source': [{
                'outbound': ['PDB', 'entity_structure_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table entry.id.',
            'markdown_name': 'structure id'
        }, 'id', ['PDB', 'entity_type_fkey'], ['PDB', 'entity_src_method_fkey'], 'pdbx_description',
        'formula_weight', 'pdbx_number_of_molecules', 'details'
    ],
    'entry': [
        {
            'source': [{
                'outbound': ['PDB', 'entity_structure_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table entry.id.',
            'markdown_name': 'structure id'
        }, 'id', ['PDB', 'entity_type_fkey'], ['PDB', 'entity_src_method_fkey'], 'pdbx_description',
        'formula_weight', 'pdbx_number_of_molecules', 'details'
    ]
}

visible_foreign_keys = {
    'filter': 'detailed',
    'detailed': [
        ['PDB', 'entity_name_com_entity_id_fkey'], ['PDB', 'entity_name_sys_entity_id_fkey'],
        ['PDB', 'entity_src_gen_entity_id_fkey'], ['PDB', 'entity_poly_entity_id_fkey'],
        ['PDB', 'pdbx_entity_nonpoly_entity_id_fkey'], ['PDB', 'struct_asym_entity_id_fkey'],
        ['PDB', 'ihm_model_representation_details_entity_id_fkey'],
        ['PDB', 'ihm_struct_assembly_details_entity_id_fkey'],
        ['PDB', 'ihm_starting_model_details_entity_id_fkey'],
        ['PDB', 'ihm_ligand_probe_entity_id_fkey'], ['PDB', 'ihm_non_poly_feature_entity_id_fkey'],
        ['PDB', 'ihm_interface_residue_feature_binding_partner_entity_id_fkey'],
        ['PDB', 'ihm_localization_density_files_entity_id_fkey'],
        ['PDB', 'pdbx_entity_poly_na_type_entity_id_fkey']
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

table_acl_bindings = {}

key_defs = [
    em.Key.define(['id', 'structure_id'], constraint_names=[['PDB', 'entity_primary_key']],
                  ),
    em.Key.define(['RID'], constraint_names=[['PDB', 'entity_RIDkey1']],
                  ),
    em.Key.define(['RID', 'id'], constraint_names=[['PDB', 'entity_id_RID_key']],
                  ),
]

fkey_defs = [
    em.ForeignKey.define(
        ['RMB'],
        'public',
        'ERMrest_Client', ['ID'],
        constraint_names=[['PDB', 'entity_RMB_fkey']],
    ),
    em.ForeignKey.define(
        ['RCB'],
        'public',
        'ERMrest_Client', ['ID'],
        constraint_names=[['PDB', 'entity_RCB_fkey']],
    ),
    em.ForeignKey.define(
        ['type'],
        'Vocab',
        'entity_type', ['Name'],
        constraint_names=[['PDB', 'entity_type_fkey']],
    ),
    em.ForeignKey.define(
        ['src_method'],
        'Vocab',
        'entity_src_method', ['Name'],
        constraint_names=[['PDB', 'entity_src_method_fkey']],
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
