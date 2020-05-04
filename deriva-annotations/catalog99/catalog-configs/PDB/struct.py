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

table_name = 'struct'

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
    'structure_id': 'A reference to table entry.id.',
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
        'structure_id',
        em.builtin_types['text'],
        nullok=False,
        comment=column_comment['structure_id'],
    ),
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
    em.Key.define(['RID'], constraint_names=[['PDB', 'struct_RIDkey1']],
                  ),
    em.Key.define(['structure_id', 'entry_id'], constraint_names=[['PDB', 'struct_primary_key']],
                  ),
]

fkey_defs = [
    em.ForeignKey.define(
        ['RCB'],
        'public',
        'ERMrest_Client', ['ID'],
        constraint_names=[['PDB', 'struct_RCB_fkey']],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
    ),
    em.ForeignKey.define(
        ['Owner'],
        'public',
        'Catalog_Group', ['ID'],
        constraint_names=[['PDB', 'struct_Owner_fkey']],
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
        ['entry_id'],
        'PDB',
        'entry', ['id'],
        constraint_names=[['PDB', 'struct_entry_id_fkey']],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
        on_update='CASCADE',
        on_delete='SET NULL',
    ),
    em.ForeignKey.define(
        ['pdbx_CASP_flag'],
        'Vocab',
        'struct_pdbx_CASP_flag', ['ID'],
        constraint_names=[['PDB', 'struct_pdbx_CASP_flag_fkey']],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
    ),
    em.ForeignKey.define(
        ['RMB'],
        'public',
        'ERMrest_Client', ['ID'],
        constraint_names=[['PDB', 'struct_RMB_fkey']],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
    ),
    em.ForeignKey.define(
        ['structure_id'],
        'PDB',
        'entry', ['id'],
        constraint_names=[['PDB', 'struct_structure_id_fkey']],
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
