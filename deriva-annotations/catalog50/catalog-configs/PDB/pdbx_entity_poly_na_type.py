import argparse
from deriva.core import ErmrestCatalog, AttrDict, get_credential
import deriva.core.ermrest_model as em
from deriva.core.ermrest_config import tag as chaise_tags
from deriva.utils.catalog.manage.update_catalog import CatalogUpdater, parse_args

groups = {}

table_name = 'pdbx_entity_poly_na_type'

schema_name = 'PDB'

column_annotations = {'structure_id': {}, 'entity_id': {}, 'type': {}, 'Owner': {}}

column_comment = {
    'structure_id': 'A reference to table entry.id.',
    'entity_id': 'A reference to table entity.id.',
    'type': 'type:text\nThis data item describes the nucleic acid type.',
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
        'entity_id', em.builtin_types['text'], nullok=False, comment=column_comment['entity_id'],
    ),
    em.Column.define(
        'type', em.builtin_types['text'], nullok=False, comment=column_comment['type'],
    ),
    em.Column.define('Owner', em.builtin_types['text'], comment=column_comment['Owner'],
                     ),
]

visible_columns = {
    '*': [
        'RID', {
            'source': [{
                'outbound': ['PDB', 'pdbx_entity_poly_na_type_structure_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table entry.id.',
            'markdown_name': 'structure id'
        }, {
            'source': [{
                'outbound': ['PDB', 'pdbx_entity_poly_na_type_entity_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table entity.id.',
            'markdown_name': 'entity id'
        }, ['PDB', 'pdbx_entity_poly_na_type_type_fkey']
    ],
    'entry': [
        {
            'source': [{
                'outbound': ['PDB', 'pdbx_entity_poly_na_type_structure_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table entry.id.',
            'markdown_name': 'structure id'
        }, {
            'source': [{
                'outbound': ['PDB', 'pdbx_entity_poly_na_type_entity_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table entity.id.',
            'markdown_name': 'entity id'
        }, ['PDB', 'pdbx_entity_poly_na_type_type_fkey']
    ],
    'detailed': [
        'RID', {
            'source': [{
                'outbound': ['PDB', 'pdbx_entity_poly_na_type_structure_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table entry.id.',
            'markdown_name': 'structure id'
        }, {
            'source': [{
                'outbound': ['PDB', 'pdbx_entity_poly_na_type_entity_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table entity.id.',
            'markdown_name': 'entity id'
        }, ['PDB', 'pdbx_entity_poly_na_type_type_fkey'],
        ['PDB', 'pdbx_entity_poly_na_type_RCB_fkey'], ['PDB', 'pdbx_entity_poly_na_type_RMB_fkey'],
        'RCT', 'RMT', ['PDB', 'pdbx_entity_poly_na_type_Owner_fkey']
    ]
}

table_annotations = {chaise_tags.visible_columns: visible_columns, }

table_comment = 'Type of nucleic acid polymer entities'

table_acls = {}

table_acl_bindings = {}

key_defs = [
    em.Key.define(['RID'], constraint_names=[['PDB', 'pdbx_entity_poly_na_type_RIDkey1']],
                  ),
    em.Key.define(
        ['type', 'structure_id', 'entity_id'],
        constraint_names=[['PDB', 'pdbx_entity_poly_na_type_primary_key']],
    ),
]

fkey_defs = [
    em.ForeignKey.define(
        ['type'],
        'Vocab',
        'pdbx_entity_poly_na_type_type', ['Name'],
        constraint_names=[['PDB', 'pdbx_entity_poly_na_type_type_fkey']],
    ),
    em.ForeignKey.define(
        ['RCB'],
        'public',
        'ERMrest_Client', ['ID'],
        constraint_names=[['PDB', 'pdbx_entity_poly_na_type_RCB_fkey']],
    ),
    em.ForeignKey.define(
        ['RMB'],
        'public',
        'ERMrest_Client', ['ID'],
        constraint_names=[['PDB', 'pdbx_entity_poly_na_type_RMB_fkey']],
    ),
    em.ForeignKey.define(
        ['entity_id', 'structure_id'],
        'PDB',
        'entity', ['id', 'structure_id'],
        constraint_names=[['PDB', 'pdbx_entity_poly_na_type_entity_id_fkey']],
        annotations={
            chaise_tags.foreign_key: {
                'domain_filter_pattern': 'structure_id={{structure_id}}'
            }
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
    catalog_id = 50
    mode, replace, host, catalog_id = parse_args(host, catalog_id, is_table=True)
    catalog = ErmrestCatalog('https', host, catalog_id=catalog_id, credentials=get_credential(host))
    main(catalog, mode, replace)
