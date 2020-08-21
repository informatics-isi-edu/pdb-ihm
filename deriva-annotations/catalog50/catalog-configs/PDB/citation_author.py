import argparse
from deriva.core import ErmrestCatalog, AttrDict, get_credential
import deriva.core.ermrest_model as em
from deriva.core.ermrest_config import tag as chaise_tags
from deriva.utils.catalog.manage.update_catalog import CatalogUpdater, parse_args

groups = {}

table_name = 'citation_author'

schema_name = 'PDB'

column_annotations = {'structure_id': {}, 'citation_id': {}, 'name': {}, 'ordinal': {}, 'Owner': {}}

column_comment = {
    'structure_id': 'A reference to table entry.id.',
    'citation_id': 'A reference to table citation.id.',
    'name': "type:text\nName of an author of the citation; relevant for journal\n articles, books and book chapters.\n\n The family name(s), followed by a comma and including any\n dynastic components, precedes the first name(s) or initial(s).\nexamples:Jones, T.J.,Bleary, Percival R.,O'Neil, F.K.,Van den Bossche, G.,Yang, D.-L.,Simonov, Yu.A",
    'ordinal': "type:int4\nThis data item defines the order of the author's name in the\n list of authors of a citation.",
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
        'citation_id',
        em.builtin_types['text'],
        nullok=False,
        comment=column_comment['citation_id'],
    ),
    em.Column.define(
        'name', em.builtin_types['text'], nullok=False, comment=column_comment['name'],
    ),
    em.Column.define(
        'ordinal', em.builtin_types['int4'], nullok=False, comment=column_comment['ordinal'],
    ),
    em.Column.define('Owner', em.builtin_types['text'], comment=column_comment['Owner'],
                     ),
]

visible_columns = {
    '*': [
        'RID', {
            'source': [{
                'outbound': ['PDB', 'citation_author_structure_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table entry.id.',
            'markdown_name': 'structure id'
        }, {
            'source': [{
                'outbound': ['PDB', 'citation_author_citation_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table citation.id.',
            'markdown_name': 'citation id'
        }, 'ordinal', 'name'
    ],
    'entry': [
        {
            'source': [{
                'outbound': ['PDB', 'citation_author_structure_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table entry.id.',
            'markdown_name': 'structure id'
        }, {
            'source': [{
                'outbound': ['PDB', 'citation_author_citation_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table citation.id.',
            'markdown_name': 'citation id'
        }, 'ordinal', 'name'
    ]
}

table_annotations = {chaise_tags.visible_columns: visible_columns, }

table_comment = 'Authors associated with citations in the citation list'

table_acls = {}

table_acl_bindings = {}

key_defs = [
    em.Key.define(
        ['citation_id', 'structure_id', 'name', 'ordinal'],
        constraint_names=[['PDB', 'citation_author_primary_key']],
    ),
    em.Key.define(['RID'], constraint_names=[['PDB', 'citation_author_RIDkey1']],
                  ),
]

fkey_defs = [
    em.ForeignKey.define(
        ['RCB'],
        'public',
        'ERMrest_Client', ['ID'],
        constraint_names=[['PDB', 'citation_author_RCB_fkey']],
    ),
    em.ForeignKey.define(
        ['citation_id', 'structure_id'],
        'PDB',
        'citation', ['id', 'structure_id'],
        constraint_names=[['PDB', 'citation_author_citation_id_fkey']],
        annotations={
            chaise_tags.foreign_key: {
                'domain_filter_pattern': 'structure_id={{structure_id}}'
            }
        },
        on_update='CASCADE',
        on_delete='SET NULL',
    ),
    em.ForeignKey.define(
        ['RMB'],
        'public',
        'ERMrest_Client', ['ID'],
        constraint_names=[['PDB', 'citation_author_RMB_fkey']],
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
