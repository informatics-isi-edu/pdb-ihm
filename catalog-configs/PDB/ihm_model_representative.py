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

table_name = 'ihm_model_representative'

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
    'id': {
        chaise_tags.generated: None
    },
    'model_group_id': {},
    'model_id': {},
    'selection_criteria': {},
    'Owner': {}
}

column_comment = {
    'structure_id': 'type:text\nThe value of _entry.id identifies the data block.\n\n Note that this item need not be a number; it can be any unique\n identifier.',
    'id': 'type:int4\nA unique identifier for the representative of the model group.',
    'model_group_id': 'type:int4\nA unique identifier for a collection or group of structural models. \n This data item can be used to group models into structural clusters\n or using other criteria based on experimental data or other\n relationships such as those belonging to the same state or time stamp.\n An ensemble of models and its representative can either be grouped together\n or can be separate groups in the ihm_model_group table. The choice between\n the two options should be decided based on how the modeling was carried out\n and how the representative was chosen. If the representative is a member of\n the ensemble (i.e., best scoring model), then it is recommended that the\n representative and the ensemble belong to the same model group. If the\n representative is calculated from the ensemble (i.e., centroid), then it is\n recommended that the representative be separated into a different group.',
    'model_id': 'type:int4\nA unique identifier for the structural model being deposited.',
    'selection_criteria': 'type:text\nThe selection criteria based on which the representative is chosen.',
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
        'id',
        em.builtin_types['int4'],
        nullok=False,
        annotations=column_annotations['id'],
        comment=column_comment['id'],
    ),
    em.Column.define(
        'model_group_id',
        em.builtin_types['int4'],
        nullok=False,
        comment=column_comment['model_group_id'],
    ),
    em.Column.define(
        'model_id', em.builtin_types['int4'], nullok=False, comment=column_comment['model_id'],
    ),
    em.Column.define(
        'selection_criteria',
        em.builtin_types['text'],
        nullok=False,
        comment=column_comment['selection_criteria'],
    ),
    em.Column.define('Owner', em.builtin_types['text'], comment=column_comment['Owner'],
                     ),
]

visible_columns = {
    '*': [
        'RID',
        {
            'source': [{
                'outbound': ['PDB', 'ihm_model_representative_structure_id_fkey']
            }, 'RID'],
            'comment': 'type:text\nThe value of _entry.id identifies the data block.\n\n Note that this item need not be a number; it can be any unique\n identifier.',
            'markdown_name': 'structure id'
        }, 'id',
        {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_model_representative_model_group_id_fkey']
                }, 'RID'
            ],
            'comment': 'type:int4\nA unique identifier for a collection or group of structural models. \n This data item can be used to group models into structural clusters\n or using other criteria based on experimental data or other\n relationships such as those belonging to the same state or time stamp.\n An ensemble of models and its representative can either be grouped together\n or can be separate groups in the ihm_model_group table. The choice between\n the two options should be decided based on how the modeling was carried out\n and how the representative was chosen. If the representative is a member of\n the ensemble (i.e., best scoring model), then it is recommended that the\n representative and the ensemble belong to the same model group. If the\n representative is calculated from the ensemble (i.e., centroid), then it is\n recommended that the representative be separated into a different group.',
            'markdown_name': 'model group id'
        },
        {
            'source': [{
                'outbound': ['PDB', 'ihm_model_representative_model_id_fkey']
            }, 'RID'],
            'comment': 'type:int4\nA unique identifier for the structural model being deposited.',
            'markdown_name': 'model id'
        }, ['PDB', 'ihm_model_representative_selection_criteria_term_fkey'],
        ['PDB', 'ihm_model_representative_RCB_fkey'], ['PDB', 'ihm_model_representative_RMB_fkey'],
        'RCT', 'RMT', ['PDB', 'ihm_model_representative_Owner_fkey']
    ],
    'entry': [
        {
            'source': [{
                'outbound': ['PDB', 'ihm_model_representative_structure_id_fkey']
            }, 'RID'],
            'comment': 'type:text\nThe value of _entry.id identifies the data block.\n\n Note that this item need not be a number; it can be any unique\n identifier.',
            'markdown_name': 'structure id'
        }, 'id',
        {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_model_representative_model_group_id_fkey']
                }, 'RID'
            ],
            'comment': 'type:int4\nA unique identifier for a collection or group of structural models. \n This data item can be used to group models into structural clusters\n or using other criteria based on experimental data or other\n relationships such as those belonging to the same state or time stamp.\n An ensemble of models and its representative can either be grouped together\n or can be separate groups in the ihm_model_group table. The choice between\n the two options should be decided based on how the modeling was carried out\n and how the representative was chosen. If the representative is a member of\n the ensemble (i.e., best scoring model), then it is recommended that the\n representative and the ensemble belong to the same model group. If the\n representative is calculated from the ensemble (i.e., centroid), then it is\n recommended that the representative be separated into a different group.',
            'markdown_name': 'model group id'
        },
        {
            'source': [{
                'outbound': ['PDB', 'ihm_model_representative_model_id_fkey']
            }, 'RID'],
            'comment': 'type:int4\nA unique identifier for the structural model being deposited.',
            'markdown_name': 'model id'
        }, ['PDB', 'ihm_model_representative_selection_criteria_term_fkey']
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
    em.Key.define(['RID'], constraint_names=[('PDB', 'ihm_model_representative_RIDkey1')],
                  ),
    em.Key.define(
        ['structure_id', 'id'],
        constraint_names=[('PDB', 'ihm_model_representative_primary_key')],
    ),
]

fkey_defs = [
    em.ForeignKey.define(
        ['selection_criteria'],
        'Vocab',
        'ihm_model_representative_selection_criteria_term', ['ID'],
        constraint_names=[('PDB', 'ihm_model_representative_selection_criteria_term_fkey')],
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
        constraint_names=[('PDB', 'ihm_model_representative_Owner_fkey')],
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
        constraint_names=[('PDB', 'ihm_model_representative_RCB_fkey')],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
    ),
    em.ForeignKey.define(
        ['RMB'],
        'public',
        'ERMrest_Client', ['ID'],
        constraint_names=[('PDB', 'ihm_model_representative_RMB_fkey')],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
    ),
    em.ForeignKey.define(
        ['structure_id'],
        'PDB',
        'entry', ['id'],
        constraint_names=[('PDB', 'ihm_model_representative_structure_id_fkey')],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
        on_update='CASCADE',
        on_delete='SET NULL',
    ),
    em.ForeignKey.define(
        ['structure_id', 'model_group_id'],
        'PDB',
        'ihm_model_group', ['structure_id', 'id'],
        constraint_names=[('PDB', 'ihm_model_representative_model_group_id_fkey')],
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
        constraint_names=[('PDB', 'ihm_model_representative_model_id_fkey')],
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

