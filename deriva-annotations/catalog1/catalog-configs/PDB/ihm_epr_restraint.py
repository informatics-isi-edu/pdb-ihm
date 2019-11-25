import argparse
from deriva.core import ErmrestCatalog, AttrDict, get_credential, DerivaPathError
from deriva.utils.catalog.components.deriva_model import DerivaCatalog
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

table_name = 'ihm_epr_restraint'

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
    'chi_value': {},
    'dataset_list_id': {},
    'details': {},
    'fitting_method': {},
    'fitting_method_citation_id': {},
    'fitting_particle_type': {},
    'fitting_software_id': {},
    'fitting_state': {},
    'model_id': {},
    'ordinal_id': {},
    'Owner': {}
}

column_comment = {
    'structure_id': 'A reference to table entry.id.',
    'chi_value': 'type:float4\nThe chi value resulting from fitting the model to the EPR data.',
    'dataset_list_id': 'A reference to table ihm_dataset_list.id.',
    'details': 'type:text\nAdditional details regarding the EPR restraint used.',
    'fitting_method': 'type:text\nThe method used for fitting the model to the EPR data.\nexamples:Spin label rotamer refinement using DEER/PELDOR data',
    'fitting_method_citation_id': 'A reference to table citation.id.',
    'fitting_particle_type': 'type:text\nThe type of particle fit to the EPR data.\nexamples:Unpaired electrons of the probe',
    'fitting_software_id': 'A reference to table software.pdbx_ordinal.',
    'fitting_state': 'type:text\nAn indicator to single or multiple state fitting.',
    'model_id': 'A reference to table ihm_model_list.model_id.',
    'ordinal_id': 'type:int4\nA unique identifier for the EPR restraint description.',
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
        'chi_value', em.builtin_types['float4'], comment=column_comment['chi_value'],
    ),
    em.Column.define(
        'dataset_list_id',
        em.builtin_types['int4'],
        nullok=False,
        comment=column_comment['dataset_list_id'],
    ),
    em.Column.define('details', em.builtin_types['text'], comment=column_comment['details'],
                     ),
    em.Column.define(
        'fitting_method', em.builtin_types['text'], comment=column_comment['fitting_method'],
    ),
    em.Column.define(
        'fitting_method_citation_id',
        em.builtin_types['text'],
        comment=column_comment['fitting_method_citation_id'],
    ),
    em.Column.define(
        'fitting_particle_type',
        em.builtin_types['text'],
        comment=column_comment['fitting_particle_type'],
    ),
    em.Column.define(
        'fitting_software_id',
        em.builtin_types['int4'],
        nullok=False,
        comment=column_comment['fitting_software_id'],
    ),
    em.Column.define(
        'fitting_state', em.builtin_types['text'], comment=column_comment['fitting_state'],
    ),
    em.Column.define(
        'model_id', em.builtin_types['int4'], nullok=False, comment=column_comment['model_id'],
    ),
    em.Column.define(
        'ordinal_id',
        em.builtin_types['int4'],
        nullok=False,
        comment=column_comment['ordinal_id'],
    ),
    em.Column.define('Owner', em.builtin_types['text'], comment=column_comment['Owner'],
                     ),
]

visible_columns = {
    '*': [
        'RID', {
            'source': [{
                'outbound': ['PDB', 'ihm_epr_restraint_structure_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table entry.id.',
            'markdown_name': 'structure id'
        }, 'chi_value', {
            'source': [{
                'outbound': ['PDB', 'ihm_epr_restraint_dataset_list_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table ihm_dataset_list.id.',
            'markdown_name': 'dataset list id'
        }, 'details', 'fitting_method', {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_epr_restraint_fitting_method_citation_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table citation.id.',
            'markdown_name': 'fitting method citation id'
        }, 'fitting_particle_type', {
            'source': [{
                'outbound': ['PDB', 'ihm_epr_restraint_fitting_software_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table software.pdbx_ordinal.',
            'markdown_name': 'fitting software id'
        }, ['PDB', 'ihm_epr_restraint_fitting_state_term_fkey'], {
            'source': [{
                'outbound': ['PDB', 'ihm_epr_restraint_model_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table ihm_model_list.model_id.',
            'markdown_name': 'model id'
        }, 'ordinal_id',
        ['PDB', 'ihm_epr_restraint_RCB_fkey'], ['PDB', 'ihm_epr_restraint_RMB_fkey'], 'RCT', 'RMT',
        ['PDB', 'ihm_epr_restraint_Owner_fkey']
    ],
    'entry': [
        {
            'source': [{
                'outbound': ['PDB', 'ihm_epr_restraint_structure_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table entry.id.',
            'markdown_name': 'structure id'
        }, 'chi_value', {
            'source': [{
                'outbound': ['PDB', 'ihm_epr_restraint_dataset_list_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table ihm_dataset_list.id.',
            'markdown_name': 'dataset list id'
        }, 'details', 'fitting_method', {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_epr_restraint_fitting_method_citation_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table citation.id.',
            'markdown_name': 'fitting method citation id'
        }, 'fitting_particle_type', {
            'source': [{
                'outbound': ['PDB', 'ihm_epr_restraint_fitting_software_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table software.pdbx_ordinal.',
            'markdown_name': 'fitting software id'
        }, ['PDB', 'ihm_epr_restraint_fitting_state_term_fkey'], {
            'source': [{
                'outbound': ['PDB', 'ihm_epr_restraint_model_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table ihm_model_list.model_id.',
            'markdown_name': 'model id'
        }, 'ordinal_id'
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
    em.Key.define(['RID'], constraint_names=[('PDB', 'ihm_epr_restraint_RIDkey1')],
                  ),
    em.Key.define(
        ['structure_id', 'ordinal_id'],
        constraint_names=[('PDB', 'ihm_epr_restraint_primary_key')],
    ),
]

fkey_defs = [
    em.ForeignKey.define(
        ['fitting_state'],
        'Vocab',
        'ihm_epr_restraint_fitting_state_term', ['ID'],
        constraint_names=[('PDB', 'ihm_epr_restraint_fitting_state_term_fkey')],
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
        constraint_names=[('PDB', 'ihm_epr_restraint_Owner_fkey')],
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
        constraint_names=[('PDB', 'ihm_epr_restraint_RCB_fkey')],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
    ),
    em.ForeignKey.define(
        ['RMB'],
        'public',
        'ERMrest_Client', ['ID'],
        constraint_names=[('PDB', 'ihm_epr_restraint_RMB_fkey')],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
    ),
    em.ForeignKey.define(
        ['structure_id'],
        'PDB',
        'entry', ['id'],
        constraint_names=[('PDB', 'ihm_epr_restraint_structure_id_fkey')],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
        on_update='CASCADE',
        on_delete='SET NULL',
    ),
    em.ForeignKey.define(
        ['structure_id', 'dataset_list_id'],
        'PDB',
        'ihm_dataset_list', ['structure_id', 'id'],
        constraint_names=[('PDB', 'ihm_epr_restraint_dataset_list_id_fkey')],
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
        ['structure_id', 'fitting_method_citation_id'],
        'PDB',
        'citation', ['structure_id', 'id'],
        constraint_names=[('PDB', 'ihm_epr_restraint_fitting_method_citation_id_fkey')],
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
        ['structure_id', 'fitting_software_id'],
        'PDB',
        'software', ['structure_id', 'pdbx_ordinal'],
        constraint_names=[('PDB', 'ihm_epr_restraint_fitting_software_id_fkey')],
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
        ['structure_id', 'model_id'],
        'PDB',
        'ihm_model_list', ['structure_id', 'model_id'],
        constraint_names=[('PDB', 'ihm_epr_restraint_model_id_fkey')],
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
    table_def['column_annotations'] = column_annotations
    table_def['column_comment'] = column_comment
    updater.update_table(mode, schema_name, table_def, replace=replace, really=really)


if __name__ == "__main__":
    host = 'pdb.isrd.isi.edu'
    catalog_id = 1
    mode, replace, host, catalog_id = parse_args(host, catalog_id, is_table=True)
    catalog = DerivaCatalog(host, catalog_id=catalog_id, validate=False)
    main(catalog, mode, replace)
