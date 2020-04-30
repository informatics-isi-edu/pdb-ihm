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

table_name = 'ihm_probe_list'

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
    'probe_chem_comp_descriptor_id': {},
    'probe_id': {},
    'probe_link_type': {},
    'probe_name': {},
    'probe_origin': {},
    'reactive_probe_chem_comp_descriptor_id': {},
    'reactive_probe_flag': {},
    'reactive_probe_name': {},
    'Owner': {}
}

column_comment = {
    'structure_id': 'A reference to table entry.id.',
    'probe_chem_comp_descriptor_id': 'A reference to table ihm_chemical_component_descriptor.id.',
    'probe_id': 'type:int4\nA unique identifier for the category.',
    'probe_link_type': 'type:text\nThe type of link between the probe and the biomolecule.',
    'probe_name': 'type:text\nAuthor provided name for the probe.',
    'probe_origin': 'type:text\nThe origin of the probe.',
    'reactive_probe_chem_comp_descriptor_id': 'A reference to table ihm_chemical_component_descriptor.id.',
    'reactive_probe_flag': 'type:text\nIndicate whether the probe has a reactive form.',
    'reactive_probe_name': 'type:text\nAuthor provided name for the reactive_probe, if applicable.',
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
        'probe_chem_comp_descriptor_id',
        em.builtin_types['int4'],
        comment=column_comment['probe_chem_comp_descriptor_id'],
    ),
    em.Column.define(
        'probe_id', em.builtin_types['int4'], nullok=False, comment=column_comment['probe_id'],
    ),
    em.Column.define(
        'probe_link_type',
        em.builtin_types['text'],
        nullok=False,
        comment=column_comment['probe_link_type'],
    ),
    em.Column.define(
        'probe_name',
        em.builtin_types['text'],
        nullok=False,
        comment=column_comment['probe_name'],
    ),
    em.Column.define(
        'probe_origin',
        em.builtin_types['text'],
        nullok=False,
        comment=column_comment['probe_origin'],
    ),
    em.Column.define(
        'reactive_probe_chem_comp_descriptor_id',
        em.builtin_types['int4'],
        comment=column_comment['reactive_probe_chem_comp_descriptor_id'],
    ),
    em.Column.define(
        'reactive_probe_flag',
        em.builtin_types['text'],
        comment=column_comment['reactive_probe_flag'],
    ),
    em.Column.define(
        'reactive_probe_name',
        em.builtin_types['text'],
        comment=column_comment['reactive_probe_name'],
    ),
    em.Column.define('Owner', em.builtin_types['text'], comment=column_comment['Owner'],
                     ),
]

visible_columns = {
    '*': [
        'RID', {
            'source': [{
                'outbound': ['PDB', 'ihm_probe_list_structure_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table entry.id.',
            'markdown_name': 'structure id'
        }, 'probe_id', 'probe_name', ['PDB', 'ihm_probe_list_reactive_probe_flag_fkey'],
        'reactive_probe_name', ['PDB', 'ihm_probe_list_probe_origin_fkey'],
        ['PDB', 'ihm_probe_list_probe_link_type_fkey'], {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_probe_list_probe_chem_comp_descriptor_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table ihm_chemical_component_descriptor.id.',
            'markdown_name': 'probe chem comp descriptor id'
        }, {
            'source': [
                {
                    'outbound': [
                        'PDB', 'ihm_probe_list_reactive_probe_chem_comp_descriptor_id_fkey'
                    ]
                }, 'RID'
            ],
            'comment': 'A reference to table ihm_chemical_component_descriptor.id.',
            'markdown_name': 'reactive probe chem comp descriptor id'
        }
    ],
    'entry': [
        {
            'source': [{
                'outbound': ['PDB', 'ihm_probe_list_structure_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table entry.id.',
            'markdown_name': 'structure id'
        }, 'probe_id', 'probe_name', ['PDB', 'ihm_probe_list_reactive_probe_flag_fkey'],
        'reactive_probe_name', ['PDB', 'ihm_probe_list_probe_origin_fkey'],
        ['PDB', 'ihm_probe_list_probe_link_type_fkey'], {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_probe_list_probe_chem_comp_descriptor_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table ihm_chemical_component_descriptor.id.',
            'markdown_name': 'probe chem comp descriptor id'
        }, {
            'source': [
                {
                    'outbound': [
                        'PDB', 'ihm_probe_list_reactive_probe_chem_comp_descriptor_id_fkey'
                    ]
                }, 'RID'
            ],
            'comment': 'A reference to table ihm_chemical_component_descriptor.id.',
            'markdown_name': 'reactive probe chem comp descriptor id'
        }
    ],
    'detailed': [
        'RID', {
            'source': [{
                'outbound': ['PDB', 'ihm_probe_list_structure_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table entry.id.',
            'markdown_name': 'structure id'
        }, 'probe_id', 'probe_name', ['PDB', 'ihm_probe_list_reactive_probe_flag_fkey'],
        'reactive_probe_name', ['PDB', 'ihm_probe_list_probe_origin_fkey'],
        ['PDB', 'ihm_probe_list_probe_link_type_fkey'], {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_probe_list_probe_chem_comp_descriptor_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table ihm_chemical_component_descriptor.id.',
            'markdown_name': 'probe chem comp descriptor id'
        }, {
            'source': [
                {
                    'outbound': [
                        'PDB', 'ihm_probe_list_reactive_probe_chem_comp_descriptor_id_fkey'
                    ]
                }, 'RID'
            ],
            'comment': 'A reference to table ihm_chemical_component_descriptor.id.',
            'markdown_name': 'reactive probe chem comp descriptor id'
        }, ['PDB', 'ihm_probe_list_RCB_fkey'], ['PDB', 'ihm_probe_list_RMB_fkey'], 'RCT', 'RMT',
        ['PDB', 'ihm_probe_list_Owner_fkey']
    ]
}

visible_foreign_keys = {
    'filter': 'detailed',
    'detailed': [
        ['PDB', 'ihm_poly_probe_conjugate_probe_id_fkey'],
        ['PDB', 'ihm_ligand_probe_probe_id_fkey']
    ]
}

table_annotations = {
    chaise_tags.visible_columns: visible_columns,
    chaise_tags.visible_foreign_keys: visible_foreign_keys,
}

table_comment = 'Probes used in the experiment'

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
    em.Key.define(
        ['structure_id', 'probe_id'], constraint_names=[['PDB', 'ihm_probe_list_primary_key']],
    ),
    em.Key.define(['RID'], constraint_names=[['PDB', 'ihm_probe_list_RIDkey1']],
                  ),
]

fkey_defs = [
    em.ForeignKey.define(
        ['probe_chem_comp_descriptor_id', 'structure_id'],
        'PDB',
        'ihm_chemical_component_descriptor', ['id', 'structure_id'],
        constraint_names=[['PDB', 'ihm_probe_list_probe_chem_comp_descriptor_id_fkey']],
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
        ['Owner'],
        'public',
        'Catalog_Group', ['ID'],
        constraint_names=[['PDB', 'ihm_probe_list_Owner_fkey']],
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
        constraint_names=[['PDB', 'ihm_probe_list_RCB_fkey']],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
    ),
    em.ForeignKey.define(
        ['probe_origin'],
        'Vocab',
        'ihm_probe_list_probe_origin', ['ID'],
        constraint_names=[['PDB', 'ihm_probe_list_probe_origin_fkey']],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
    ),
    em.ForeignKey.define(
        ['reactive_probe_chem_comp_descriptor_id', 'structure_id'],
        'PDB',
        'ihm_chemical_component_descriptor', ['id', 'structure_id'],
        constraint_names=[['PDB', 'ihm_probe_list_reactive_probe_chem_comp_descriptor_id_fkey']],
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
        ['structure_id'],
        'PDB',
        'entry', ['id'],
        constraint_names=[['PDB', 'ihm_probe_list_structure_id_fkey']],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
        on_update='CASCADE',
        on_delete='SET NULL',
    ),
    em.ForeignKey.define(
        ['reactive_probe_flag'],
        'Vocab',
        'ihm_probe_list_reactive_probe_flag', ['ID'],
        constraint_names=[['PDB', 'ihm_probe_list_reactive_probe_flag_fkey']],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
    ),
    em.ForeignKey.define(
        ['RMB'],
        'public',
        'ERMrest_Client', ['ID'],
        constraint_names=[['PDB', 'ihm_probe_list_RMB_fkey']],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
    ),
    em.ForeignKey.define(
        ['probe_link_type'],
        'Vocab',
        'ihm_probe_list_probe_link_type', ['ID'],
        constraint_names=[['PDB', 'ihm_probe_list_probe_link_type_fkey']],
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
