import argparse
from deriva.core import ErmrestCatalog, AttrDict, get_credential
import deriva.core.ermrest_model as em
from deriva.core.ermrest_config import tag as chaise_tags
from deriva.utils.catalog.manage.update_catalog import CatalogUpdater, parse_args

groups = {}

table_name = 'ihm_probe_list'

schema_name = 'PDB'

column_annotations = {
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
    em.Column.define('Probe_chem_comp_descriptor_RID', em.builtin_types['text'],
                     ),
    em.Column.define('Reactive_probe_chem_comp_descriptor_RID', em.builtin_types['text'],
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

table_acl_bindings = {}

key_defs = [
    em.Key.define(
        ['structure_id', 'probe_id'], constraint_names=[['PDB', 'ihm_probe_list_primary_key']],
    ),
    em.Key.define(['RID'], constraint_names=[['PDB', 'ihm_probe_list_RIDkey1']],
                  ),
]

fkey_defs = [
    em.ForeignKey.define(
        ['probe_link_type'],
        'Vocab',
        'ihm_probe_list_probe_link_type', ['Name'],
        constraint_names=[['PDB', 'ihm_probe_list_probe_link_type_fkey']],
    ),
    em.ForeignKey.define(
        ['probe_origin'],
        'Vocab',
        'ihm_probe_list_probe_origin', ['Name'],
        constraint_names=[['PDB', 'ihm_probe_list_probe_origin_fkey']],
    ),
    em.ForeignKey.define(
        ['reactive_probe_flag'],
        'Vocab',
        'ihm_probe_list_reactive_probe_flag', ['Name'],
        constraint_names=[['PDB', 'ihm_probe_list_reactive_probe_flag_fkey']],
    ),
    em.ForeignKey.define(
        ['probe_chem_comp_descriptor_id', 'structure_id'],
        'PDB',
        'ihm_chemical_component_descriptor', ['id', 'structure_id'],
        constraint_names=[['PDB', 'ihm_probe_list_probe_chem_comp_descriptor_id_fk']],
        annotations={
            chaise_tags.foreign_key: {
                'domain_filter_pattern': 'structure_id={{structure_id}}'
            }
        },
        on_update='CASCADE',
        on_delete='SET NULL',
    ),
    em.ForeignKey.define(
        ['probe_chem_comp_descriptor_id', 'Probe_chem_comp_descriptor_RID'],
        'PDB',
        'ihm_chemical_component_descriptor', ['id', 'RID'],
        constraint_names=[['PDB', 'ihm_probe_list_probe_chem_comp_descriptor_id_fkey']],
        annotations={
            chaise_tags.foreign_key: {
                'domain_filter_pattern': 'structure_id={{structure_id}}'
            }
        },
        on_update='CASCADE',
        on_delete='SET NULL',
    ),
    em.ForeignKey.define(
        ['reactive_probe_chem_comp_descriptor_id', 'structure_id'],
        'PDB',
        'ihm_chemical_component_descriptor', ['id', 'structure_id'],
        constraint_names=[['PDB', 'ihm_probe_list_reactive_probe_chem_comp_descriptor_id_fk']],
        annotations={
            chaise_tags.foreign_key: {
                'domain_filter_pattern': 'structure_id={{structure_id}}'
            }
        },
        on_update='CASCADE',
        on_delete='SET NULL',
    ),
    em.ForeignKey.define(
        ['reactive_probe_chem_comp_descriptor_id', 'Reactive_probe_chem_comp_descriptor_RID'],
        'PDB',
        'ihm_chemical_component_descriptor', ['id', 'RID'],
        constraint_names=[['PDB', 'ihm_probe_list_reactive_probe_chem_comp_descriptor_id_fkey']],
        annotations={
            chaise_tags.foreign_key: {
                'domain_filter_pattern': 'structure_id={{structure_id}}'
            }
        },
        on_update='CASCADE',
        on_delete='SET NULL',
    ),
    em.ForeignKey.define(
        ['RCB'],
        'public',
        'ERMrest_Client', ['ID'],
        constraint_names=[['PDB', 'ihm_probe_list_RCB_fkey']],
    ),
    em.ForeignKey.define(
        ['RMB'],
        'public',
        'ERMrest_Client', ['ID'],
        constraint_names=[['PDB', 'ihm_probe_list_RMB_fkey']],
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
