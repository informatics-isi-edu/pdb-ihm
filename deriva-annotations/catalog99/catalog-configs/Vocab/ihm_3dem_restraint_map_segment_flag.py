import argparse
from deriva.core import ErmrestCatalog, AttrDict, get_credential
import deriva.core.ermrest_model as em
from deriva.core.ermrest_config import tag as chaise_tags
from deriva.utils.catalog.manage.update_catalog import CatalogUpdater, parse_args

groups = {}

table_name = 'ihm_3dem_restraint_map_segment_flag'

schema_name = 'Vocab'

column_annotations = {
    'ID': {},
    'URI': {},
    'Name': {},
    'Description': {},
    'Synonyms': {},
    'Owner': {}
}

column_comment = {
    'ID': 'The preferred Compact URI (CURIE) for this term.',
    'URI': 'The preferred URI for this term.',
    'Name': 'None',
    'Description': 'None',
    'Synonyms': 'Alternate human-readable names for this term.',
    'Owner': 'Group that can update the record.'
}

column_acls = {}

column_acl_bindings = {}

column_defs = [
    em.Column.define(
        'ID',
        em.builtin_types['ermrest_curie'],
        nullok=False,
        default='PDB:{RID}',
        comment=column_comment['ID'],
    ),
    em.Column.define(
        'URI',
        em.builtin_types['ermrest_uri'],
        nullok=False,
        default='/id/{RID}',
        comment=column_comment['URI'],
    ),
    em.Column.define(
        'Name', em.builtin_types['text'], nullok=False, comment=column_comment['Name'],
    ),
    em.Column.define(
        'Description',
        em.builtin_types['markdown'],
        nullok=False,
        comment=column_comment['Description'],
    ),
    em.Column.define('Synonyms', em.builtin_types['text[]'], comment=column_comment['Synonyms'],
                     ),
    em.Column.define('Owner', em.builtin_types['text'], comment=column_comment['Owner'],
                     ),
]

visible_columns = {
    '*': [
        'RID', 'Name', 'Description', 'ID', 'URI',
        ['Vocab', 'ihm_3dem_restraint_map_segment_flag_term_RCB_fkey'],
        ['Vocab', 'ihm_3dem_restraint_map_segment_flag_term_RMB_fkey'], 'RCT', 'RMT',
        ['Vocab', 'ihm_3dem_restraint_map_segment_flag_term_Owner_fkey']
    ]
}

table_display = {'row_name': {'row_markdown_pattern': '{{{Name}}}'}}

table_annotations = {
    chaise_tags.table_display: table_display,
    chaise_tags.visible_columns: visible_columns,
}

table_comment = 'A set of controlled vocabular terms.'

table_acls = {}

table_acl_bindings = {}

key_defs = [
    em.Key.define(
        ['Name'], constraint_names=[['Vocab', 'ihm_3dem_restraint_map_segment_flag_Namekey1']],
    ),
    em.Key.define(
        ['ID'], constraint_names=[['Vocab', 'ihm_3dem_restraint_map_segment_flag_term_IDkey1']],
    ),
    em.Key.define(
        ['URI'], constraint_names=[['Vocab', 'ihm_3dem_restraint_map_segment_flag_term_URIkey1']],
    ),
    em.Key.define(
        ['RID'], constraint_names=[['Vocab', 'ihm_3dem_restraint_map_segment_flag_term_RIDkey1']],
    ),
]

fkey_defs = [
    em.ForeignKey.define(
        ['RMB'],
        'public',
        'ERMrest_Client', ['ID'],
        constraint_names=[['Vocab', 'ihm_3dem_restraint_map_segment_flag_term_RMB_fkey']],
    ),
    em.ForeignKey.define(
        ['RCB'],
        'public',
        'ERMrest_Client', ['ID'],
        constraint_names=[['Vocab', 'ihm_3dem_restraint_map_segment_flag_term_RCB_fkey']],
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
