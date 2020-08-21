import argparse
from deriva.core import ErmrestCatalog, AttrDict, get_credential
import deriva.core.ermrest_model as em
from deriva.core.ermrest_config import tag as chaise_tags
from deriva.utils.catalog.manage.update_catalog import CatalogUpdater, parse_args

groups = {}

table_name = 'struct'

schema_name = 'PDB'

column_annotations = {
    'entry_id': {},
    'pdbx_CASP_flag': {},
    'pdbx_descriptor': {},
    'pdbx_details': {},
    'pdbx_model_details': {},
    'pdbx_model_type_details': {},
    'title': {},
    'Owner': {}
}

column_comment = {
    'entry_id': 'A reference to table entry.id.',
    'pdbx_CASP_flag': 'type:text\nThe item indicates whether the entry is a CASP target, a CASD-NMR target,\n or similar target participating in methods development experiments.\nexamples:Y',
    'pdbx_descriptor': "type:text\nAn automatically generated descriptor for an NDB structure or\n the unstructured content of the PDB COMPND record.\nexamples:5'-D(*CP*GP*CP*(HYD)AP*AP*AP*TP*TP*TP*GP*CP*G)-3'",
    'pdbx_details': 'type:text\nAdditional remarks related to this structure deposition that have not\nbeen included in details data items elsewhere.\nexamples:Hydrogen bonds between peptide chains follow the Rich and Crick\nmodel II for collagen.',
    'pdbx_model_details': 'type:text\nText description of the methodology which produced this\n model structure.\nexamples:This model was produced from a 10 nanosecond Amber/MD simulation\nstarting from PDB structure ID 1ABC.',
    'pdbx_model_type_details': 'type:text\nA description of the type of structure model.\nexamples:MINIMIZED AVERAGE',
    'title': "type:text\nA title for the data block. The author should attempt to convey\n the essence of the structure archived in the CIF in the title,\n and to distinguish this structural result from others.\nexamples:T4 lysozyme mutant - S32A,5'-D(*(I)CP*CP*GP*G)-3,T4 lysozyme mutant - S32A,hen egg white lysozyme at -30 degrees C,quail egg white lysozyme at 2 atmospheres",
    'Owner': 'Group that can update the record.'
}

column_acls = {}

column_acl_bindings = {}

column_defs = [
    em.Column.define(
        'entry_id', em.builtin_types['text'], nullok=False, comment=column_comment['entry_id'],
    ),
    em.Column.define(
        'pdbx_CASP_flag', em.builtin_types['text'], comment=column_comment['pdbx_CASP_flag'],
    ),
    em.Column.define(
        'pdbx_descriptor', em.builtin_types['text'], comment=column_comment['pdbx_descriptor'],
    ),
    em.Column.define(
        'pdbx_details', em.builtin_types['text'], comment=column_comment['pdbx_details'],
    ),
    em.Column.define(
        'pdbx_model_details',
        em.builtin_types['text'],
        comment=column_comment['pdbx_model_details'],
    ),
    em.Column.define(
        'pdbx_model_type_details',
        em.builtin_types['text'],
        comment=column_comment['pdbx_model_type_details'],
    ),
    em.Column.define('title', em.builtin_types['text'], comment=column_comment['title'],
                     ),
    em.Column.define('Owner', em.builtin_types['text'], comment=column_comment['Owner'],
                     ),
]

visible_columns = {
    '*': [
        'RID', {
            'source': [{
                'outbound': ['PDB', 'struct_entry_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table entry.id.',
            'markdown_name': 'entry id'
        }, 'title', 'pdbx_descriptor', 'pdbx_details', 'pdbx_model_details',
        'pdbx_model_type_details', ['PDB', 'struct_pdbx_CASP_flag_fkey']
    ],
    'entry': [
        {
            'source': [{
                'outbound': ['PDB', 'struct_entry_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table entry.id.',
            'markdown_name': 'entry id'
        }, 'title', 'pdbx_descriptor', 'pdbx_details', 'pdbx_model_details',
        'pdbx_model_type_details', ['PDB', 'struct_pdbx_CASP_flag_fkey']
    ],
    'detailed': [
        'RID', {
            'source': [{
                'outbound': ['PDB', 'struct_entry_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table entry.id.',
            'markdown_name': 'entry id'
        }, 'title', 'pdbx_descriptor', 'pdbx_details',
        'pdbx_model_details', 'pdbx_model_type_details', ['PDB', 'struct_pdbx_CASP_flag_fkey'],
        ['PDB', 'struct_RCB_fkey'], ['PDB', 'struct_RMB_fkey'], 'RCT', 'RMT',
        ['PDB', 'struct_Owner_fkey']
    ]
}

table_annotations = {chaise_tags.visible_columns: visible_columns, }

table_comment = 'Description of the structure'

table_acls = {}

table_acl_bindings = {}

key_defs = [em.Key.define(['RID'], constraint_names=[['PDB', 'struct_RIDkey1']], ), ]

fkey_defs = [
    em.ForeignKey.define(
        ['pdbx_CASP_flag'],
        'Vocab',
        'struct_pdbx_CASP_flag', ['Name'],
        constraint_names=[['PDB', 'struct_pdbx_CASP_flag_fkey']],
    ),
    em.ForeignKey.define(
        ['RCB'],
        'public',
        'ERMrest_Client', ['ID'],
        constraint_names=[['PDB', 'struct_RCB_fkey']],
    ),
    em.ForeignKey.define(
        ['RMB'],
        'public',
        'ERMrest_Client', ['ID'],
        constraint_names=[['PDB', 'struct_RMB_fkey']],
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
    catalog_id = 50
    mode, replace, host, catalog_id = parse_args(host, catalog_id, is_table=True)
    catalog = ErmrestCatalog('https', host, catalog_id=catalog_id, credentials=get_credential(host))
    main(catalog, mode, replace)
