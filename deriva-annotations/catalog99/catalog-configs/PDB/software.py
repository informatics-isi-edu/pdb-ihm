import argparse
from deriva.core import ErmrestCatalog, AttrDict, get_credential
import deriva.core.ermrest_model as em
from deriva.core.ermrest_config import tag as chaise_tags
from deriva.utils.catalog.manage.update_catalog import CatalogUpdater, parse_args

groups = {}

table_name = 'software'

schema_name = 'PDB'

column_annotations = {
    'structure_id': {},
    'citation_id': {},
    'classification': {},
    'description': {},
    'location': {},
    'name': {},
    'pdbx_ordinal': {},
    'type': {},
    'version': {},
    'Owner': {}
}

column_comment = {
    'structure_id': 'A reference to table entry.id.',
    'citation_id': 'Citation corresponding to the software; a reference to the citation id in the citation table',
    'classification': 'type:text\nThe classification of the program according to its\n major function.\nexamples:data collection,data reduction,phasing,model building,refinement,validation,other',
    'description': 'type:text\nDescription of the software.\nexamples:Uses method of restrained least squares',
    'location': 'type:text\nThe URL for an Internet address at which\n details of the software can be found.\nexamples:http://rosebud.sdsc.edu/projects/pb/IUCr/software.html,ftp://ftp.sdsc.edu/pub/sdsc/biology/',
    'name': 'type:text\nThe name of the software.\nexamples:Merlot,O,Xengen,X-plor',
    'pdbx_ordinal': 'type:int4\nAn ordinal index for this category\nexamples:1,2',
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
        comment=column_comment['pdbx_ordinal'],
    ),
    em.Column.define('type', em.builtin_types['text'], comment=column_comment['type'],
                     ),
    em.Column.define('version', em.builtin_types['text'], comment=column_comment['version'],
                     ),
    em.Column.define('Owner', em.builtin_types['text'], comment=column_comment['Owner'],
                     ),
    em.Column.define('Citation_RID', em.builtin_types['text'],
                     ),
]

visible_columns = {
    '*': [
        'RID', {
            'source': [{
                'outbound': ['PDB', 'software_structure_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table entry.id.',
            'markdown_name': 'structure id'
        }, 'pdbx_ordinal', 'name', 'classification', ['PDB', 'software_type_fkey'], 'version',
        'location', {
            'source': [{
                'outbound': ['PDB', 'software_citation_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table citation.id.',
            'markdown_name': 'citation id'
        }, 'description'
    ],
    'entry': [
        {
            'source': [{
                'outbound': ['PDB', 'software_structure_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table entry.id.',
            'markdown_name': 'structure id'
        }, 'pdbx_ordinal', 'name', 'classification', ['PDB', 'software_type_fkey'], 'version',
        'location', {
            'source': [{
                'outbound': ['PDB', 'software_citation_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table citation.id.',
            'markdown_name': 'citation id'
        }, 'description'
    ]
}

visible_foreign_keys = {
    'filter': 'detailed',
    'detailed': [
        ['PDB', 'ihm_modeling_protocol_details_software_id_fkey'],
        ['PDB', 'ihm_modeling_post_process_software_id_fkey'],
        ['PDB', 'ihm_starting_computational_models_software_id_fkey'],
        ['PDB', 'ihm_epr_restraint_fitting_software_id_fkey'],
        ['PDB', 'ihm_hydroxyl_radical_fp_restraint_software_id_fkey'],
        ['PDB', 'ihm_predicted_contact_restraint_software_id_fkey']
    ]
}

table_display = {'row_name': {'row_markdown_pattern': '{{{pdbx_ordinal}}}'}}

table_annotations = {
    chaise_tags.table_display: table_display,
    chaise_tags.visible_columns: visible_columns,
    chaise_tags.visible_foreign_keys: visible_foreign_keys,
}

table_comment = 'List of software used in the modeling'

table_acls = {}

table_acl_bindings = {}

key_defs = [
    em.Key.define(
        ['pdbx_ordinal', 'structure_id'], constraint_names=[['PDB', 'software_primary_key']],
    ),
    em.Key.define(['RID'], constraint_names=[['PDB', 'software_RIDkey1']],
                  ),
    em.Key.define(
        ['RID', 'pdbx_ordinal'], constraint_names=[['PDB', 'software_RID_pdbx_ordinal_key']],
    ),
]

fkey_defs = [
    em.ForeignKey.define(
        ['RCB'],
        'public',
        'ERMrest_Client', ['ID'],
        constraint_names=[['PDB', 'software_RCB_fkey']],
    ),
    em.ForeignKey.define(
        ['RMB'],
        'public',
        'ERMrest_Client', ['ID'],
        constraint_names=[['PDB', 'software_RMB_fkey']],
    ),
    em.ForeignKey.define(
        ['type'],
        'Vocab',
        'software_type', ['Name'],
        constraint_names=[['PDB', 'software_type_fkey']],
    ),
    em.ForeignKey.define(
        ['structure_id', 'citation_id'],
        'PDB',
        'citation', ['structure_id', 'id'],
        constraint_names=[['PDB', 'software_citation_id_fk']],
        on_update='CASCADE',
        on_delete='SET NULL',
    ),
    em.ForeignKey.define(
        ['Citation_RID', 'citation_id'],
        'PDB',
        'citation', ['RID', 'id'],
        constraint_names=[['PDB', 'software_citation_id_fkey']],
        annotations={
            chaise_tags.foreign_key: {
                'template_engine': 'handlebars',
                'domain_filter_pattern': '{{#if _structure_id}}structure_id={{{_structure_id}}}{{/if}}'
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
    catalog_id = 99
    mode, replace, host, catalog_id = parse_args(host, catalog_id, is_table=True)
    catalog = ErmrestCatalog('https', host, catalog_id=catalog_id, credentials=get_credential(host))
    main(catalog, mode, replace)
