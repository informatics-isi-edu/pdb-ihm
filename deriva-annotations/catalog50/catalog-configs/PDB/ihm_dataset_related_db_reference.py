import argparse
from deriva.core import ErmrestCatalog, AttrDict, get_credential
import deriva.core.ermrest_model as em
from deriva.core.ermrest_config import tag as chaise_tags
from deriva.utils.catalog.manage.update_catalog import CatalogUpdater, parse_args

groups = {}

table_name = 'ihm_dataset_related_db_reference'

schema_name = 'PDB'

column_annotations = {
    'structure_id': {},
    'accession_code': {},
    'dataset_list_id': {},
    'db_name': {},
    'details': {},
    'id': {},
    'version': {},
    'Owner': {}
}

column_comment = {
    'structure_id': 'A reference to table entry.id.',
    'accession_code': 'type:text\nThe accession code for the database entry.\nexamples:5FM1,25766,EMD-2799,10049,SASDA82,PXD003381,MA-CO2KC',
    'dataset_list_id': 'A reference to table ihm_dataset_list.id.',
    'db_name': 'type:text\nThe name of the database containing the dataset entry.',
    'details': 'type:text\nDetails regarding the dataset entry.\nexamples:Structural Analysis of a Prokaryotic Ribosome Using a Novel Amidinating Cross-Linker and Mass Spectrometry',
    'id': 'type:int4\nA unique identifier for the related database entry.',
    'version': 'type:text\nVersion of the database entry, if the database allows versioning.',
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
        'accession_code',
        em.builtin_types['text'],
        nullok=False,
        comment=column_comment['accession_code'],
    ),
    em.Column.define(
        'dataset_list_id',
        em.builtin_types['int4'],
        nullok=False,
        comment=column_comment['dataset_list_id'],
    ),
    em.Column.define(
        'db_name', em.builtin_types['text'], nullok=False, comment=column_comment['db_name'],
    ),
    em.Column.define('details', em.builtin_types['text'], comment=column_comment['details'],
                     ),
    em.Column.define('id', em.builtin_types['int4'], nullok=False, comment=column_comment['id'],
                     ),
    em.Column.define('version', em.builtin_types['text'], comment=column_comment['version'],
                     ),
    em.Column.define('Owner', em.builtin_types['text'], comment=column_comment['Owner'],
                     ),
]

visible_columns = {
    '*': [
        'RID', {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_dataset_related_db_reference_structure_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table entry.id.',
            'markdown_name': 'structure id'
        }, 'id', {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_dataset_related_db_reference_dataset_list_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table ihm_dataset_list.id.',
            'markdown_name': 'dataset list id'
        }, ['PDB', 'ihm_dataset_related_db_reference_db_name_fkey'], 'accession_code', 'version',
        'details'
    ],
    'entry': [
        {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_dataset_related_db_reference_structure_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table entry.id.',
            'markdown_name': 'structure id'
        }, 'id', {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_dataset_related_db_reference_dataset_list_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table ihm_dataset_list.id.',
            'markdown_name': 'dataset list id'
        }, ['PDB', 'ihm_dataset_related_db_reference_db_name_fkey'], 'accession_code', 'version',
        'details'
    ],
    'detailed': [
        'RID', {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_dataset_related_db_reference_structure_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table entry.id.',
            'markdown_name': 'structure id'
        }, 'id', {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_dataset_related_db_reference_dataset_list_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table ihm_dataset_list.id.',
            'markdown_name': 'dataset list id'
        }, ['PDB', 'ihm_dataset_related_db_reference_db_name_fkey'], 'accession_code', 'version',
        'details', ['PDB', 'ihm_dataset_related_db_reference_RCB_fkey'],
        ['PDB', 'ihm_dataset_related_db_reference_RMB_fkey'], 'RCT', 'RMT',
        ['PDB', 'ihm_dataset_related_db_reference_Owner_fkey']
    ]
}

table_annotations = {chaise_tags.visible_columns: visible_columns, }

table_comment = 'Input datasets archived in other repositories'

table_acls = {}

table_acl_bindings = {}

key_defs = [
    em.Key.define(
        ['structure_id', 'id'],
        constraint_names=[['PDB', 'ihm_dataset_related_db_reference_primary_key']],
    ),
    em.Key.define(
        ['RID'], constraint_names=[['PDB', 'ihm_dataset_related_db_reference_RIDkey1']],
    ),
]

fkey_defs = [
    em.ForeignKey.define(
        ['db_name'],
        'Vocab',
        'ihm_dataset_related_db_reference_db_name', ['Name'],
        constraint_names=[['PDB', 'ihm_dataset_related_db_reference_db_name_fkey']],
    ),
    em.ForeignKey.define(
        ['RMB'],
        'public',
        'ERMrest_Client', ['ID'],
        constraint_names=[['PDB', 'ihm_dataset_related_db_reference_RMB_fkey']],
    ),
    em.ForeignKey.define(
        ['RCB'],
        'public',
        'ERMrest_Client', ['ID'],
        constraint_names=[['PDB', 'ihm_dataset_related_db_reference_RCB_fkey']],
    ),
    em.ForeignKey.define(
        ['structure_id', 'dataset_list_id'],
        'PDB',
        'ihm_dataset_list', ['structure_id', 'id'],
        constraint_names=[['PDB', 'ihm_dataset_related_db_reference_dataset_list_id_fkey']],
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
