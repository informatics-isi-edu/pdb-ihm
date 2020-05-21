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
    'isrd-staff': 'https://auth.globus.org/176baec4-ed26-11e5-8e88-22000ab4b42b',
    'pdb-submitter': 'https://auth.globus.org/99da042e-64a6-11ea-ad5f-0ef992ed7ca1'
}

table_name = 'citation'

schema_name = 'PDB'

column_annotations = {
    'structure_id': {},
    'country': {},
    'id': {},
    'journal_abbrev': {},
    'journal_id_ASTM': {},
    'journal_id_CSD': {},
    'journal_id_ISSN': {},
    'journal_issue': {},
    'journal_volume': {},
    'page_first': {},
    'page_last': {},
    'pdbx_database_id_DOI': {
        chaise_tags.column_display: {
            '*': {
                'markdown_pattern': '{{#pdbx_database_id_DOI}}[{{_pdbx_database_id_DOI}}](https://doi.org/{{_pdbx_database_id_DOI}}){{/pdbx_database_id_DOI}}'
            }
        }
    },
    'pdbx_database_id_PubMed': {
        chaise_tags.column_display: {
            '*': {
                'markdown_pattern': '{{_pdbx_database_id_PubMed}}'
            }
        }
    },
    'title': {},
    'year': {
        chaise_tags.column_display: {
            '*': {
                'markdown_pattern': '{{_year}}'
            }
        }
    },
    'Owner': {}
}

column_comment = {
    'structure_id': 'A reference to table entry.id.',
    'country': 'type:text\nThe country/region of publication; relevant for books\n and book chapters.',
    'id': "type:text\nThe value of _citation.id must uniquely identify a record in the\n CITATION list.\n\n The _citation.id 'primary' should be used to indicate the\n citation that the author(s) consider to be the most pertinent to\n the contents of the data block.\n\n Note that this item need not be a number; it can be any unique\n identifier.\nexamples:primary,1,2",
    'journal_abbrev': 'type:text\nAbbreviated name of the cited journal as given in the\n Chemical Abstracts Service Source Index.\nexamples:J.Mol.Biol.,J. Mol. Biol.',
    'journal_id_ASTM': 'type:text\nThe American Society for Testing and Materials (ASTM) code\n assigned to the journal cited (also referred to as the CODEN\n designator of the Chemical Abstracts Service); relevant for\n journal articles.',
    'journal_id_CSD': 'type:text\nThe Cambridge Structural Database (CSD) code assigned to the\n journal cited; relevant for journal articles. This is also the\n system used at the Protein Data Bank (PDB).\nexamples:0070',
    'journal_id_ISSN': 'type:text\nThe International Standard Serial Number (ISSN) code assigned to\n the journal cited; relevant for journal articles.',
    'journal_issue': 'type:text\nIssue number of the journal cited; relevant for journal\n articles.\nexamples:2',
    'journal_volume': 'type:text\nVolume number of the journal cited; relevant for journal\n articles.\nexamples:174',
    'page_first': 'type:text\nThe first page of the citation; relevant for journal\n articles, books and book chapters.',
    'page_last': 'type:text\nThe last page of the citation; relevant for journal\n articles, books and book chapters.',
    'pdbx_database_id_DOI': 'type:text\nDocument Object Identifier used by doi.org to uniquely\n specify bibliographic entry.\nexamples:10.2345/S1384107697000225',
    'pdbx_database_id_PubMed': 'type:int4\nAscession number used by PubMed to categorize a specific\n bibliographic entry.\nexamples:12627512',
    'title': 'type:text\nThe title of the citation; relevant for journal articles, books\n and book chapters.\nexamples:Structure of diferric duck ovotransferrin\n                                  at 2.35 Angstroms resolution.',
    'year': 'type:int4\nThe year of the citation; relevant for journal articles, books\n and book chapters.\nexamples:1984',
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
    em.Column.define('country', em.builtin_types['text'], comment=column_comment['country'],
                     ),
    em.Column.define('id', em.builtin_types['text'], nullok=False, comment=column_comment['id'],
                     ),
    em.Column.define(
        'journal_abbrev', em.builtin_types['text'], comment=column_comment['journal_abbrev'],
    ),
    em.Column.define(
        'journal_id_ASTM', em.builtin_types['text'], comment=column_comment['journal_id_ASTM'],
    ),
    em.Column.define(
        'journal_id_CSD', em.builtin_types['text'], comment=column_comment['journal_id_CSD'],
    ),
    em.Column.define(
        'journal_id_ISSN', em.builtin_types['text'], comment=column_comment['journal_id_ISSN'],
    ),
    em.Column.define(
        'journal_issue', em.builtin_types['text'], comment=column_comment['journal_issue'],
    ),
    em.Column.define(
        'journal_volume', em.builtin_types['text'], comment=column_comment['journal_volume'],
    ),
    em.Column.define(
        'page_first', em.builtin_types['text'], comment=column_comment['page_first'],
    ),
    em.Column.define('page_last', em.builtin_types['text'], comment=column_comment['page_last'],
                     ),
    em.Column.define(
        'pdbx_database_id_DOI',
        em.builtin_types['text'],
        annotations=column_annotations['pdbx_database_id_DOI'],
        comment=column_comment['pdbx_database_id_DOI'],
    ),
    em.Column.define(
        'pdbx_database_id_PubMed',
        em.builtin_types['int4'],
        annotations=column_annotations['pdbx_database_id_PubMed'],
        comment=column_comment['pdbx_database_id_PubMed'],
    ),
    em.Column.define('title', em.builtin_types['text'], comment=column_comment['title'],
                     ),
    em.Column.define(
        'year',
        em.builtin_types['int4'],
        annotations=column_annotations['year'],
        comment=column_comment['year'],
    ),
    em.Column.define('Owner', em.builtin_types['text'], comment=column_comment['Owner'],
                     ),
]

visible_columns = {
    '*': [
        'RID', {
            'source': [{
                'outbound': ['PDB', 'citation_structure_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table entry.id.',
            'markdown_name': 'structure id'
        }, 'id', 'title', 'year', 'journal_abbrev', 'journal_volume', 'journal_issue', 'page_first',
        'page_last', 'pdbx_database_id_DOI', 'pdbx_database_id_PubMed', 'journal_id_ASTM',
        'journal_id_CSD', 'journal_id_ISSN', 'country'
    ],
    'entry': [
        {
            'source': [{
                'outbound': ['PDB', 'citation_structure_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table entry.id.',
            'markdown_name': 'structure id'
        }, 'id', 'title', 'year', 'journal_abbrev', 'journal_volume', 'journal_issue', 'page_first',
        'page_last', 'pdbx_database_id_DOI', 'pdbx_database_id_PubMed', 'journal_id_ASTM',
        'journal_id_CSD', 'journal_id_ISSN', 'country'
    ]
}

visible_foreign_keys = {
    'filter': 'detailed',
    'detailed': [
        ['PDB', 'citation_author_citation_id_fkey'], ['PDB', 'software_citation_id_fkey'],
        ['PDB', 'ihm_3dem_restraint_fitting_method_citation_id_fkey'],
        ['PDB', 'ihm_epr_restraint_fitting_method_citation_id_fkey']
    ]
}

table_display = {'row_name': {'row_markdown_pattern': '{{{id}}}'}}

table_annotations = {
    chaise_tags.table_display: table_display,
    chaise_tags.visible_columns: visible_columns,
    chaise_tags.visible_foreign_keys: visible_foreign_keys,
}

table_comment = 'Citation information for the primary publication as well as other relevant software and methodology.'

table_acls = {
    'owner': [groups['pdb-admin'], groups['isrd-staff']],
    'write': [],
    'delete': [groups['pdb-curator']],
    'insert': [groups['pdb-curator'], groups['pdb-writer'], groups['pdb-submitter']],
    'select': [groups['pdb-writer'], groups['pdb-reader']],
    'update': [groups['pdb-curator']],
    'enumerate': ['*']
}

table_acl_bindings = {
    'released_reader': {
        'types': ['select'],
        'scope_acl': [groups['pdb-submitter']],
        'projection': [
            {
                'outbound': ['PDB', 'citation_structure_id_fkey']
            }, {
                'outbound': ['PDB', 'entry_workflow_status_fkey']
            }, {
                'filter': 'Name',
                'operand': 'REL',
                'operator': '='
            }, 'RID'
        ],
        'projection_type': 'nonnull'
    },
    'self_service_group': {
        'types': ['update', 'delete'],
        'scope_acl': ['*'],
        'projection': ['Owner'],
        'projection_type': 'acl'
    },
    'self_service_creator': {
        'types': ['update', 'delete'],
        'scope_acl': [groups['pdb-submitter']],
        'projection': [
            {
                'outbound': ['PDB', 'citation_structure_id_fkey']
            }, {
                'outbound': ['PDB', 'entry_workflow_status_fkey']
            }, {
                'or': [
                    {
                        'filter': 'Name',
                        'operand': 'DRAFT',
                        'operator': '='
                    }, {
                        'filter': 'Name',
                        'operand': 'DEPO',
                        'operator': '='
                    }
                ]
            }, 'RCB'
        ],
        'projection_type': 'acl'
    }
}

key_defs = [
    em.Key.define(['structure_id', 'id'], constraint_names=[['PDB', 'citation_primary_key']],
                  ),
    em.Key.define(['RID'], constraint_names=[['PDB', 'citation_RIDkey1']],
                  ),
]

fkey_defs = [
    em.ForeignKey.define(
        ['RMB'],
        'public',
        'ERMrest_Client', ['ID'],
        constraint_names=[['PDB', 'citation_RMB_fkey']],
    ),
    em.ForeignKey.define(
        ['RCB'],
        'public',
        'ERMrest_Client', ['ID'],
        constraint_names=[['PDB', 'citation_RCB_fkey']],
    ),
    em.ForeignKey.define(
        ['Owner'],
        'public',
        'Catalog_Group', ['ID'],
        constraint_names=[['PDB', 'citation_Owner_fkey']],
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
        constraint_names=[['PDB', 'citation_structure_id_fkey']],
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
