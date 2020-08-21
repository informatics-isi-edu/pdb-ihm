import argparse
from deriva.core import ErmrestCatalog, AttrDict, get_credential
import deriva.core.ermrest_model as em
from deriva.core.ermrest_config import tag as chaise_tags
from deriva.utils.catalog.manage.update_catalog import CatalogUpdater, parse_args

groups = {}

table_name = 'chem_comp'

schema_name = 'PDB'

column_annotations = {
    'structure_id': {},
    'formula': {},
    'formula_weight': {},
    'id': {},
    'mon_nstd_flag': {},
    'name': {},
    'pdbx_synonyms': {},
    'type': {},
    'Owner': {}
}

column_comment = {
    'structure_id': 'A reference to table entry.id.',
    'formula': "type:text\nThe formula for the chemical component. Formulae are written\n according to the following rules:\n\n (1) Only recognized element symbols may be used.\n\n (2) Each element symbol is followed by a 'count' number. A count\n    of '1' may be omitted.\n\n (3) A space or parenthesis must separate each cluster of\n    (element symbol + count), but in general parentheses are\n    not used.\n\n (4) The order of elements depends on whether carbon is\n    present or not. If carbon is present, the order should be:\n    C, then H, then the other elements in alphabetical order\n    of their symbol. If carbon is not present, the elements\n    are listed purely in alphabetic order of their symbol. This\n    is the 'Hill' system used by Chemical Abstracts.\nexamples:C18 H19 N7 O8 S",
    'formula_weight': 'type:float4\nFormula mass in daltons of the chemical component.',
    'id': 'type:text\nThe value of _chem_comp.id must uniquely identify each item in\n the CHEM_COMP list.\n\n For protein polymer entities, this is the three-letter code for\n the amino acid.\n\n For nucleic acid polymer entities, this is the one-letter code\n for the base.\nexamples:ALA,VAL,DG,C',
    'mon_nstd_flag': "type:text\n'yes' indicates that this is a 'standard' monomer, 'no'\n indicates that it is 'nonstandard'. Nonstandard monomers\n should be described in more detail using the\n _chem_comp.mon_nstd_parent, _chem_comp.mon_nstd_class and\n _chem_comp.mon_nstd_details data items.",
    'name': 'type:text\nThe full name of the component.\nexamples:alanine,valine,adenine,cytosine',
    'pdbx_synonyms': 'type:text\nSynonym list for the component.\nexamples:ATP',
    'type': "type:text\nFor standard polymer components, the type of the monomer.\n Note that monomers that will form polymers are of three types:\n linking monomers, monomers with some type of N-terminal (or 5')\n cap and monomers with some type of C-terminal (or 3') cap.",
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
    em.Column.define('formula', em.builtin_types['text'], comment=column_comment['formula'],
                     ),
    em.Column.define(
        'formula_weight', em.builtin_types['float4'], comment=column_comment['formula_weight'],
    ),
    em.Column.define('id', em.builtin_types['text'], nullok=False, comment=column_comment['id'],
                     ),
    em.Column.define(
        'mon_nstd_flag', em.builtin_types['text'], comment=column_comment['mon_nstd_flag'],
    ),
    em.Column.define('name', em.builtin_types['text'], comment=column_comment['name'],
                     ),
    em.Column.define(
        'pdbx_synonyms', em.builtin_types['text'], comment=column_comment['pdbx_synonyms'],
    ),
    em.Column.define(
        'type', em.builtin_types['text'], nullok=False, comment=column_comment['type'],
    ),
    em.Column.define('Owner', em.builtin_types['text'], comment=column_comment['Owner'],
                     ),
]

generated = None

visible_columns = {
    '*': [
        'RID', {
            'source': [{
                'outbound': ['PDB', 'chem_comp_structure_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table entry.id.',
            'markdown_name': 'structure id'
        }, 'id', 'name', ['PDB', 'chem_comp_type_fkey'], 'formula', 'formula_weight',
        ['PDB', 'chem_comp_mon_nstd_flag_fkey'], 'pdbx_synonyms'
    ],
    'entry': [
        {
            'source': [{
                'outbound': ['PDB', 'chem_comp_structure_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table entry.id.',
            'markdown_name': 'structure id'
        }, 'id', 'name', ['PDB', 'chem_comp_type_fkey'], 'formula', 'formula_weight',
        ['PDB', 'chem_comp_mon_nstd_flag_fkey'], 'pdbx_synonyms'
    ]
}

visible_foreign_keys = {
    'filter': 'detailed',
    'detailed': [
        ['PDB', 'chem_comp_atom_comp_id_fkey'], ['PDB', 'entity_poly_seq_mon_id_fkey'],
        ['PDB', 'pdbx_entity_nonpoly_comp_id_fkey'], ['PDB', 'ihm_non_poly_feature_comp_id_fkey'],
        ['PDB', 'ihm_poly_probe_position_mut_res_chem_comp_id_fkey']
    ]
}

table_display = {'row_name': {'row_markdown_pattern': '{{{id}}}'}}

table_annotations = {
    chaise_tags.generated: generated,
    chaise_tags.table_display: table_display,
    chaise_tags.visible_columns: visible_columns,
    chaise_tags.visible_foreign_keys: visible_foreign_keys,
}

table_comment = 'Chemical components including monomers and ligands'

table_acls = {}

table_acl_bindings = {}

key_defs = [
    em.Key.define(['id', 'structure_id'], constraint_names=[['PDB', 'chem_comp_primary_key']],
                  ),
    em.Key.define(['RID'], constraint_names=[['PDB', 'chem_comp_RIDkey1']],
                  ),
    em.Key.define(['id', 'RID'], constraint_names=[['PDB', 'chem_comp_id_RID_key']],
                  ),
]

fkey_defs = [
    em.ForeignKey.define(
        ['RMB'],
        'public',
        'ERMrest_Client', ['ID'],
        constraint_names=[['PDB', 'chem_comp_RMB_fkey']],
    ),
    em.ForeignKey.define(
        ['RCB'],
        'public',
        'ERMrest_Client', ['ID'],
        constraint_names=[['PDB', 'chem_comp_RCB_fkey']],
    ),
    em.ForeignKey.define(
        ['mon_nstd_flag'],
        'Vocab',
        'chem_comp_mon_nstd_flag', ['Name'],
        constraint_names=[['PDB', 'chem_comp_mon_nstd_flag_fkey']],
    ),
    em.ForeignKey.define(
        ['type'],
        'Vocab',
        'chem_comp_type', ['Name'],
        constraint_names=[['PDB', 'chem_comp_type_fkey']],
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
