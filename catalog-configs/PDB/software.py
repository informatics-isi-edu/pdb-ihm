import argparse
from attrdict import AttrDict
from deriva.core import ErmrestCatalog, get_credential, DerivaPathError
from deriva.utils.catalog.components.deriva_model import DerivaCatalog
import deriva.core.ermrest_model as em
from deriva.core.ermrest_config import tag as chaise_tags
from deriva.utils.catalog.manage.update_catalog import CatalogUpdater, parse_args

groups = {
    'pdb-admin': 'https://auth.globus.org/0b98092c-3c41-11e9-a8c8-0ee7d80087ee',
    'pdb-reader': 'https://auth.globus.org/8875a770-3c40-11e9-a8c8-0ee7d80087ee',
    'pdb-writer': 'https://auth.globus.org/c94a1e5c-3c40-11e9-a5d1-0aacc65bfe9a',
    'pdb-curator': 'https://auth.globus.org/eef3e02a-3c40-11e9-9276-0edc9bdd56a6',
    'isrd-staff': 'https://auth.globus.org/176baec4-ed26-11e5-8e88-22000ab4b42b'
}

table_name = 'software'

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
    'citation_id': {},
    'classification': {},
    'description': {},
    'location': {},
    'name': {},
    'pdbx_ordinal': {
        chaise_tags.generated: None
    },
    'type': {},
    'version': {},
    'Owner': {}
}

column_comment = {
    'structure_id': 'type:text\nThe value of _entry.id identifies the data block.\n\n Note that this item need not be a number; it can be any unique\n identifier.',
    'citation_id': "type:text\nThe value of _citation.id must uniquely identify a record in the\n CITATION list.\n\n The _citation.id 'primary' should be used to indicate the\n citation that the author(s) consider to be the most pertinent to\n the contents of the data block.\n\n Note that this item need not be a number; it can be any unique\n identifier.",
    'classification': 'type:text\nThe classification of the program according to its\n major function.\nexamples:data collection,data reduction,phasing,model building,refinement,validation,other',
    'description': 'type:text\nDescription of the software.\nexamples:Uses method of restrained least squares',
    'location': 'type:text\nThe URL for an Internet address at which\n details of the software can be found.\nexamples:http://rosebud.sdsc.edu/projects/pb/IUCr/software.html,ftp://ftp.sdsc.edu/pub/sdsc/biology/',
    'name': 'type:text\nThe name of the software.\nexamples:Merlot,O,Xengen,X-plor',
    'pdbx_ordinal': 'type:int4\n\nAn ordinal index for this category\nexamples:1,2',
    'type': 'type:text\nThe classification of the software according to the most\n common types.',
    'version': 'type:text\nThe version of the software.\nexamples:v1.0,beta,3.1-2,unknown',
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
        'citation_id', em.builtin_types['text'], comment=column_comment['citation_id'],
    ),
    em.Column.define(
        'classification',
        em.builtin_types['text'],
        nullok=False,
        comment=column_comment['classification'],
    ),
    em.Column.define(
        'description', em.builtin_types['text'], comment=column_comment['description'],
    ),
    em.Column.define('location', em.builtin_types['text'], comment=column_comment['location'],
                     ),
    em.Column.define(
        'name', em.builtin_types['text'], nullok=False, comment=column_comment['name'],
    ),
    em.Column.define(
        'pdbx_ordinal',
        em.builtin_types['int4'],
        nullok=False,
        annotations=column_annotations['pdbx_ordinal'],
        comment=column_comment['pdbx_ordinal'],
    ),
    em.Column.define('type', em.builtin_types['text'], comment=column_comment['type'],
                     ),
    em.Column.define('version', em.builtin_types['text'], comment=column_comment['version'],
                     ),
    em.Column.define('Owner', em.builtin_types['text'], comment=column_comment['Owner'],
                     ),
]

visible_columns = {
    '*': [
        'RID',
        {
            'source': [{
                'outbound': ['PDB', 'software_structure_id_fkey']
            }, 'RID'],
            'comment': 'type:text\nThe value of _entry.id identifies the data block.\n\n Note that this item need not be a number; it can be any unique\n identifier.',
            'markdown_name': 'structure id'
        },
        {
            'source': [{
                'outbound': ['PDB', 'software_citation_id_fkey']
            }, 'RID'],
            'comment': "type:text\nThe value of _citation.id must uniquely identify a record in the\n CITATION list.\n\n The _citation.id 'primary' should be used to indicate the\n citation that the author(s) consider to be the most pertinent to\n the contents of the data block.\n\n Note that this item need not be a number; it can be any unique\n identifier.",
            'markdown_name': 'citation id'
        }, 'classification', 'description', 'location', 'name', 'pdbx_ordinal',
        ['PDB', 'software_type_term_fkey'], 'version', ['PDB', 'software_RCB_fkey'],
        ['PDB', 'software_RMB_fkey'], 'RCT', 'RMT', ['PDB', 'software_Owner_fkey']
    ],
    'entry': [
        {
            'source': [{
                'outbound': ['PDB', 'software_structure_id_fkey']
            }, 'RID'],
            'comment': 'type:text\nThe value of _entry.id identifies the data block.\n\n Note that this item need not be a number; it can be any unique\n identifier.',
            'markdown_name': 'structure id'
        },
        {
            'source': [{
                'outbound': ['PDB', 'software_citation_id_fkey']
            }, 'RID'],
            'comment': "type:text\nThe value of _citation.id must uniquely identify a record in the\n CITATION list.\n\n The _citation.id 'primary' should be used to indicate the\n citation that the author(s) consider to be the most pertinent to\n the contents of the data block.\n\n Note that this item need not be a number; it can be any unique\n identifier.",
            'markdown_name': 'citation id'
        }, 'classification', 'description', 'location', 'name', 'pdbx_ordinal',
        ['PDB', 'software_type_term_fkey'], 'version'
    ]
}

visible_foreign_keys = {
    'filter': 'detailed',
    'detailed': [
        ['PDB', 'ihm_modeling_protocol_details_software_id_fkey'],
        ['PDB', 'ihm_modeling_post_process_software_id_fkey'],
        ['PDB', 'ihm_starting_computational_models_software_id_fkey'],
        ['PDB', 'ihm_predicted_contact_restraint_software_id_fkey'],
        ['PDB', 'ihm_hydroxyl_radical_fp_restraint_software_id_fkey']
    ]
}

table_display = {'row_name': {'row_markdown_pattern': '{{{pdbx_ordinal}}}'}}

table_annotations = {
    chaise_tags.table_display: table_display,
    chaise_tags.visible_columns: visible_columns,
    chaise_tags.visible_foreign_keys: visible_foreign_keys,
}

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
    em.Key.define(['RID'], constraint_names=[('PDB', 'software_RIDkey1')],
                  ),
    em.Key.define(
        ['structure_id', 'pdbx_ordinal'], constraint_names=[('PDB', 'software_primary_key')],
    ),
]

fkey_defs = [
    em.ForeignKey.define(
        ['type'],
        'Vocab',
        'software_type_term', ['ID'],
        constraint_names=[('PDB', 'software_type_term_fkey')],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
        on_update='CASCADE',
        on_delete='SET NULL',
    ),
    em.ForeignKey.define(
        ['Owner'],
        'public',
        'Catalog_Group', ['ID'],
        constraint_names=[('PDB', 'software_Owner_fkey')],
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
        ['RCB'],
        'public',
        'ERMrest_Client', ['ID'],
        constraint_names=[('PDB', 'software_RCB_fkey')],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
    ),
    em.ForeignKey.define(
        ['RMB'],
        'public',
        'ERMrest_Client', ['ID'],
        constraint_names=[('PDB', 'software_RMB_fkey')],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
    ),
    em.ForeignKey.define(
        ['structure_id'],
        'PDB',
        'entry', ['id'],
        constraint_names=[('PDB', 'software_structure_id_fkey')],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
        on_update='CASCADE',
        on_delete='SET NULL',
    ),
    em.ForeignKey.define(
        ['structure_id', 'citation_id'],
        'PDB',
        'citation', ['structure_id', 'id'],
        constraint_names=[('PDB', 'software_citation_id_fkey')],
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
    updater.update_table(mode, schema_name, table_def, replace=replace, really=really)


if __name__ == "__main__":
    host = 'pdb.isrd.isi.edu'
    catalog_id = 5
    mode, replace, host, catalog_id = parse_args(host, catalog_id, is_table=True)
    catalog = DerivaCatalog(host, catalog_id=catalog_id, validate=False)
    main(catalog, mode, replace)

