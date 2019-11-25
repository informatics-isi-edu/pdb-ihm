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

table_name = 'ihm_poly_probe_conjugate'

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
    'ambiguous_stoichiometry_flag': {},
    'chem_comp_descriptor_id': {},
    'dataset_list_id': {},
    'details': {},
    'id': {},
    'position_id': {},
    'probe_id': {},
    'probe_stoichiometry': {},
    'Owner': {}
}

column_comment = {
    'structure_id': 'A reference to table entry.id.',
    'ambiguous_stoichiometry_flag': 'type:text\nIndicate whether there is ambiguity regarding the stoichiometry of the labeled site.',
    'chem_comp_descriptor_id': 'A reference to table ihm_chemical_component_descriptor.id.',
    'dataset_list_id': 'A reference to table ihm_dataset_list.id.',
    'details': 'type:text\nAdditional details regarding the conjugate.',
    'id': 'type:int4\nA unique identifier for the category.',
    'position_id': 'A reference to table ihm_poly_probe_position.id.',
    'probe_id': 'A reference to table ihm_probe_list.probe_id.',
    'probe_stoichiometry': 'type:float4\nThe stoichiometry of the probe labeling site, if known.',
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
        'ambiguous_stoichiometry_flag',
        em.builtin_types['text'],
        comment=column_comment['ambiguous_stoichiometry_flag'],
    ),
    em.Column.define(
        'chem_comp_descriptor_id',
        em.builtin_types['int4'],
        comment=column_comment['chem_comp_descriptor_id'],
    ),
    em.Column.define(
        'dataset_list_id',
        em.builtin_types['int4'],
        nullok=False,
        comment=column_comment['dataset_list_id'],
    ),
    em.Column.define('details', em.builtin_types['text'], comment=column_comment['details'],
                     ),
    em.Column.define('id', em.builtin_types['int4'], nullok=False, comment=column_comment['id'],
                     ),
    em.Column.define(
        'position_id',
        em.builtin_types['int4'],
        nullok=False,
        comment=column_comment['position_id'],
    ),
    em.Column.define(
        'probe_id', em.builtin_types['int4'], nullok=False, comment=column_comment['probe_id'],
    ),
    em.Column.define(
        'probe_stoichiometry',
        em.builtin_types['float4'],
        comment=column_comment['probe_stoichiometry'],
    ),
    em.Column.define('Owner', em.builtin_types['text'], comment=column_comment['Owner'],
                     ),
]

visible_columns = {
    '*': [
        'RID', {
            'source': [{
                'outbound': ['PDB', 'ihm_poly_probe_conjugate_structure_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table entry.id.',
            'markdown_name': 'structure id'
        }, ['PDB', '_probe_conjugate_ambiguous_stoichiometry_flag_term_fkey'], {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_poly_probe_conjugate_chem_comp_descriptor_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table ihm_chemical_component_descriptor.id.',
            'markdown_name': 'chem comp descriptor id'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_poly_probe_conjugate_dataset_list_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table ihm_dataset_list.id.',
            'markdown_name': 'dataset list id'
        }, 'details', 'id', {
            'source': [{
                'outbound': ['PDB', 'ihm_poly_probe_conjugate_position_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table ihm_poly_probe_position.id.',
            'markdown_name': 'position id'
        }, {
            'source': [{
                'outbound': ['PDB', 'ihm_poly_probe_conjugate_probe_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table ihm_probe_list.probe_id.',
            'markdown_name': 'probe id'
        }, 'probe_stoichiometry', ['PDB', 'ihm_poly_probe_conjugate_RCB_fkey'],
        ['PDB', 'ihm_poly_probe_conjugate_RMB_fkey'], 'RCT', 'RMT',
        ['PDB', 'ihm_poly_probe_conjugate_Owner_fkey']
    ],
    'entry': [
        {
            'source': [{
                'outbound': ['PDB', 'ihm_poly_probe_conjugate_structure_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table entry.id.',
            'markdown_name': 'structure id'
        }, ['PDB', '_probe_conjugate_ambiguous_stoichiometry_flag_term_fkey'], {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_poly_probe_conjugate_chem_comp_descriptor_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table ihm_chemical_component_descriptor.id.',
            'markdown_name': 'chem comp descriptor id'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_poly_probe_conjugate_dataset_list_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table ihm_dataset_list.id.',
            'markdown_name': 'dataset list id'
        }, 'details', 'id', {
            'source': [{
                'outbound': ['PDB', 'ihm_poly_probe_conjugate_position_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table ihm_poly_probe_position.id.',
            'markdown_name': 'position id'
        }, {
            'source': [{
                'outbound': ['PDB', 'ihm_poly_probe_conjugate_probe_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table ihm_probe_list.probe_id.',
            'markdown_name': 'probe id'
        }, 'probe_stoichiometry'
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
    em.Key.define(['RID'], constraint_names=[('PDB', 'ihm_poly_probe_conjugate_RIDkey1')],
                  ),
    em.Key.define(
        ['structure_id', 'id'],
        constraint_names=[('PDB', 'ihm_poly_probe_conjugate_primary_key')],
    ),
]

fkey_defs = [
    em.ForeignKey.define(
        ['ambiguous_stoichiometry_flag'],
        'Vocab',
        '_probe_conjugate_ambiguous_stoichiometry_flag_term', ['ID'],
        constraint_names=[('PDB', '_probe_conjugate_ambiguous_stoichiometry_flag_term_fkey')],
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
        constraint_names=[('PDB', 'ihm_poly_probe_conjugate_Owner_fkey')],
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
        constraint_names=[('PDB', 'ihm_poly_probe_conjugate_RCB_fkey')],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
    ),
    em.ForeignKey.define(
        ['RMB'],
        'public',
        'ERMrest_Client', ['ID'],
        constraint_names=[('PDB', 'ihm_poly_probe_conjugate_RMB_fkey')],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
    ),
    em.ForeignKey.define(
        ['structure_id'],
        'PDB',
        'entry', ['id'],
        constraint_names=[('PDB', 'ihm_poly_probe_conjugate_structure_id_fkey')],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
        on_update='CASCADE',
        on_delete='SET NULL',
    ),
    em.ForeignKey.define(
        ['structure_id', 'chem_comp_descriptor_id'],
        'PDB',
        'ihm_chemical_component_descriptor', ['structure_id', 'id'],
        constraint_names=[('PDB', 'ihm_poly_probe_conjugate_chem_comp_descriptor_id_fkey')],
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
        ['structure_id', 'dataset_list_id'],
        'PDB',
        'ihm_dataset_list', ['structure_id', 'id'],
        constraint_names=[('PDB', 'ihm_poly_probe_conjugate_dataset_list_id_fkey')],
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
        ['structure_id', 'position_id'],
        'PDB',
        'ihm_poly_probe_position', ['structure_id', 'id'],
        constraint_names=[('PDB', 'ihm_poly_probe_conjugate_position_id_fkey')],
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
        ['structure_id', 'probe_id'],
        'PDB',
        'ihm_probe_list', ['structure_id', 'probe_id'],
        constraint_names=[('PDB', 'ihm_poly_probe_conjugate_probe_id_fkey')],
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
