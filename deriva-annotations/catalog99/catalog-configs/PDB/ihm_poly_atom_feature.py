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

table_name = 'ihm_poly_atom_feature'

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
    'atom_id': {},
    'comp_id': {},
    'entity_id': {},
    'feature_id': {},
    'ordinal_id': {},
    'seq_id': {},
    'Owner': {}
}

column_comment = {
    'structure_id': 'A reference to table entry.id.',
    'asym_id': 'A reference to table struct_asym.id.',
    'atom_id': 'The identifier of the atom.',
    'comp_id': 'A reference to table entity_poly_seq.mon_id.',
    'entity_id': 'A reference to table entity_poly_seq.entity_id.',
    'feature_id': 'A reference to table ihm_feature_list.feature_id.',
    'ordinal_id': 'type:int4\nA unique identifier for the category.',
    'seq_id': 'A reference to table entity_poly_seq.num.',
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
    em.Column.define('asym_id', em.builtin_types['text'], comment=column_comment['asym_id'],
                     ),
    em.Column.define('atom_id', em.builtin_types['text'], comment=column_comment['atom_id'],
                     ),
    em.Column.define(
        'comp_id', em.builtin_types['text'], nullok=False, comment=column_comment['comp_id'],
    ),
    em.Column.define(
        'entity_id', em.builtin_types['text'], nullok=False, comment=column_comment['entity_id'],
    ),
    em.Column.define(
        'feature_id',
        em.builtin_types['int4'],
        nullok=False,
        comment=column_comment['feature_id'],
    ),
    em.Column.define(
        'ordinal_id',
        em.builtin_types['int4'],
        nullok=False,
        comment=column_comment['ordinal_id'],
    ),
    em.Column.define(
        'seq_id', em.builtin_types['int4'], nullok=False, comment=column_comment['seq_id'],
    ),
    em.Column.define('Owner', em.builtin_types['text'], comment=column_comment['Owner'],
                     ),
    em.Column.define('Entry_Related_File', em.builtin_types['text'],
                     ),
]

visible_columns = {
    '*': [
        'RID', {
            'source': [{
                'outbound': ['PDB', 'ihm_poly_atom_feature_structure_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table entry.id.',
            'markdown_name': 'structure id'
        }, 'ordinal_id', {
            'source': [{
                'outbound': ['PDB', 'ihm_poly_atom_feature_feature_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table ihm_feature_list.feature_id.',
            'markdown_name': 'feature id'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_poly_atom_feature_mm_poly_res_label_fkey']
                }, 'entity_id'
            ],
            'comment': 'A reference to table entity_poly_seq.entity_id',
            'markdown_name': 'entity id'
        }, {
            'source': [{
                'outbound': ['PDB', 'ihm_poly_atom_feature_asym_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table struct_asym.id.',
            'markdown_name': 'asym id'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_poly_atom_feature_mm_poly_res_label_fkey']
                }, 'mon_id'
            ],
            'comment': 'A reference to table entity_poly_seq.mon_id',
            'markdown_name': 'comp id'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_poly_atom_feature_mm_poly_res_label_fkey']
                }, 'num'
            ],
            'comment': 'A reference to table entity_poly_seq.num',
            'markdown_name': 'seq id'
        }, 'atom_id', {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_poly_atom_feature_mm_poly_res_label_fkey']
                }, 'RID'
            ],
            'markdown_name': 'polymeric residue'
        }, ['PDB', 'ihm_poly_atom_feature_Entry_Related_File_fkey']
    ],
    'entry': [
        {
            'source': [{
                'outbound': ['PDB', 'ihm_poly_atom_feature_structure_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table entry.id.',
            'markdown_name': 'structure id'
        }, 'ordinal_id', {
            'source': [{
                'outbound': ['PDB', 'ihm_poly_atom_feature_feature_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table ihm_feature_list.feature_id.',
            'markdown_name': 'feature id'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_poly_atom_feature_mm_poly_res_label_fkey']
                }, 'entity_id'
            ],
            'comment': 'A reference to table entity_poly_seq.entity_id',
            'markdown_name': 'entity id'
        }, {
            'source': [{
                'outbound': ['PDB', 'ihm_poly_atom_feature_asym_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table struct_asym.id.',
            'markdown_name': 'asym id'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_poly_atom_feature_mm_poly_res_label_fkey']
                }, 'mon_id'
            ],
            'comment': 'A reference to table entity_poly_seq.mon_id',
            'markdown_name': 'comp id'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_poly_atom_feature_mm_poly_res_label_fkey']
                }, 'num'
            ],
            'comment': 'A reference to table entity_poly_seq.num',
            'markdown_name': 'seq id'
        }, 'atom_id', {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_poly_atom_feature_mm_poly_res_label_fkey']
                }, 'RID'
            ],
            'markdown_name': 'polymeric residue'
        }
    ],
    'detailed': [
        'RID', {
            'source': [{
                'outbound': ['PDB', 'ihm_poly_atom_feature_structure_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table entry.id.',
            'markdown_name': 'structure id'
        }, 'ordinal_id', {
            'source': [{
                'outbound': ['PDB', 'ihm_poly_atom_feature_feature_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table ihm_feature_list.feature_id.',
            'markdown_name': 'feature id'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_poly_atom_feature_mm_poly_res_label_fkey']
                }, 'entity_id'
            ],
            'comment': 'A reference to table entity_poly_seq.entity_id',
            'markdown_name': 'entity id'
        }, {
            'source': [{
                'outbound': ['PDB', 'ihm_poly_atom_feature_asym_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table struct_asym.id.',
            'markdown_name': 'asym id'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_poly_atom_feature_mm_poly_res_label_fkey']
                }, 'mon_id'
            ],
            'comment': 'A reference to table entity_poly_seq.mon_id',
            'markdown_name': 'comp id'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_poly_atom_feature_mm_poly_res_label_fkey']
                }, 'num'
            ],
            'comment': 'A reference to table entity_poly_seq.num',
            'markdown_name': 'seq id'
        }, 'atom_id', {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_poly_atom_feature_mm_poly_res_label_fkey']
                }, 'RID'
            ],
            'markdown_name': 'polymeric residue'
        }, ['PDB', 'ihm_poly_atom_feature_Entry_Related_File_fkey'],
        ['PDB', 'ihm_poly_atom_feature_RCB_fkey'], ['PDB', 'ihm_poly_atom_feature_RMB_fkey'], 'RCT',
        'RMT', ['PDB', 'ihm_poly_atom_feature_Owner_fkey']
    ]
}

table_annotations = {chaise_tags.visible_columns: visible_columns, }

table_comment = 'Details of atomic features of polymeric entities'

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
    em.Key.define(['RID'], constraint_names=[['PDB', 'ihm_poly_atom_feature_RIDkey1']],
                  ),
    em.Key.define(
        ['ordinal_id', 'structure_id'],
        constraint_names=[['PDB', 'ihm_poly_atom_feature_primary_key']],
    ),
]

fkey_defs = [
    em.ForeignKey.define(
        ['Owner'],
        'public',
        'Catalog_Group', ['ID'],
        constraint_names=[['PDB', 'ihm_poly_atom_feature_Owner_fkey']],
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
        ['feature_id', 'structure_id'],
        'PDB',
        'ihm_feature_list', ['feature_id', 'structure_id'],
        constraint_names=[['PDB', 'ihm_poly_atom_feature_feature_id_fkey']],
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
        ['RCB'],
        'public',
        'ERMrest_Client', ['ID'],
        constraint_names=[['PDB', 'ihm_poly_atom_feature_RCB_fkey']],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
    ),
    em.ForeignKey.define(
        ['structure_id', 'asym_id'],
        'PDB',
        'struct_asym', ['structure_id', 'id'],
        constraint_names=[['PDB', 'ihm_poly_atom_feature_asym_id_fkey']],
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
        ['structure_id'],
        'PDB',
        'entry', ['id'],
        constraint_names=[['PDB', 'ihm_poly_atom_feature_structure_id_fkey']],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
        on_update='CASCADE',
        on_delete='SET NULL',
    ),
    em.ForeignKey.define(
        ['structure_id', 'entity_id', 'comp_id', 'seq_id'],
        'PDB',
        'entity_poly_seq', ['structure_id', 'entity_id', 'mon_id', 'num'],
        constraint_names=[['PDB', 'ihm_poly_atom_feature_mm_poly_res_label_fkey']],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
        on_update='CASCADE',
        on_delete='SET NULL',
    ),
    em.ForeignKey.define(
        ['RMB'],
        'public',
        'ERMrest_Client', ['ID'],
        constraint_names=[['PDB', 'ihm_poly_atom_feature_RMB_fkey']],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
    ),
    em.ForeignKey.define(
        ['Entry_Related_File'],
        'PDB',
        'Entry_Related_File', ['RID'],
        constraint_names=[['PDB', 'ihm_poly_atom_feature_Entry_Related_File_fkey']],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
        on_delete='CASCADE',
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
