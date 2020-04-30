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

table_name = 'entity_src_gen'

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
    'entity_id': {},
    'gene_src_common_name': {},
    'gene_src_genus': {},
    'pdbx_alt_source_flag': {},
    'pdbx_gene_src_scientific_name': {},
    'pdbx_src_id': {},
    'Owner': {}
}

column_comment = {
    'structure_id': 'A reference to table entry.id.',
    'entity_id': 'A reference to table entity.id.',
    'gene_src_common_name': 'type:text\nThe common name of the natural organism from which the gene was\n obtained.\nexamples:man,yeast,bacteria',
    'gene_src_genus': 'type:text\nThe genus of the natural organism from which the gene was\n obtained.\nexamples:Homo,Saccharomyces,Escherichia',
    'pdbx_alt_source_flag': 'type:text\nThis data item identifies cases in which an alternative source\n modeled.',
    'pdbx_gene_src_scientific_name': 'type:text\nScientific name of the organism.\nexamples:Homo sapiens,ESCHERICHIA COLI\nHOMO SAPIENS\nSACCHAROMYCES CEREVISIAE',
    'pdbx_src_id': 'type:int4\nThis data item is an ordinal identifier for entity_src_gen data records.',
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
        'gene_src_common_name',
        em.builtin_types['text'],
        comment=column_comment['gene_src_common_name'],
    ),
    em.Column.define(
        'gene_src_genus', em.builtin_types['text'], comment=column_comment['gene_src_genus'],
    ),
    em.Column.define(
        'pdbx_alt_source_flag',
        em.builtin_types['text'],
        comment=column_comment['pdbx_alt_source_flag'],
    ),
    em.Column.define(
        'pdbx_gene_src_scientific_name',
        em.builtin_types['text'],
        comment=column_comment['pdbx_gene_src_scientific_name'],
    ),
    em.Column.define(
        'pdbx_src_id',
        em.builtin_types['int4'],
        nullok=False,
        comment=column_comment['pdbx_src_id'],
    ),
    em.Column.define('Owner', em.builtin_types['text'], comment=column_comment['Owner'],
                     ),
]

visible_columns = {
    '*': [
        'RID', {
            'source': [{
                'outbound': ['PDB', 'entity_src_gen_structure_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table entry.id.',
            'markdown_name': 'structure id'
        }, {
            'source': [{
                'outbound': ['PDB', 'entity_src_gen_entity_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table entity.id.',
            'markdown_name': 'entity id'
        }, 'pdbx_src_id', ['PDB', 'entity_src_gen_pdbx_alt_source_flag_fkey'],
        'gene_src_common_name', 'gene_src_genus', 'pdbx_gene_src_scientific_name'
    ],
    'entry': [
        {
            'source': [{
                'outbound': ['PDB', 'entity_src_gen_structure_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table entry.id.',
            'markdown_name': 'structure id'
        }, {
            'source': [{
                'outbound': ['PDB', 'entity_src_gen_entity_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table entity.id.',
            'markdown_name': 'entity id'
        }, 'pdbx_src_id', ['PDB', 'entity_src_gen_pdbx_alt_source_flag_fkey'],
        'gene_src_common_name', 'gene_src_genus', 'pdbx_gene_src_scientific_name'
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
    em.Key.define(['RID'], constraint_names=[['PDB', 'entity_src_gen_RIDkey1']],
                  ),
    em.Key.define(
        ['entity_id', 'pdbx_src_id', 'structure_id'],
        constraint_names=[['PDB', 'entity_src_gen_primary_key']],
    ),
]

fkey_defs = [
    em.ForeignKey.define(
        ['Owner'],
        'public',
        'Catalog_Group', ['ID'],
        constraint_names=[['PDB', 'entity_src_gen_Owner_fkey']],
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
        ['structure_id'],
        'PDB',
        'entry', ['id'],
        constraint_names=[['PDB', 'entity_src_gen_structure_id_fkey']],
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
        constraint_names=[['PDB', 'entity_src_gen_RCB_fkey']],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
    ),
    em.ForeignKey.define(
        ['pdbx_alt_source_flag'],
        'Vocab',
        'entity_src_gen_pdbx_alt_source_flag', ['ID'],
        constraint_names=[['PDB', 'entity_src_gen_pdbx_alt_source_flag_fkey']],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
    ),
    em.ForeignKey.define(
        ['entity_id', 'structure_id'],
        'PDB',
        'entity', ['id', 'structure_id'],
        constraint_names=[['PDB', 'entity_src_gen_entity_id_fkey']],
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
        ['RMB'],
        'public',
        'ERMrest_Client', ['ID'],
        constraint_names=[['PDB', 'entity_src_gen_RMB_fkey']],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
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
