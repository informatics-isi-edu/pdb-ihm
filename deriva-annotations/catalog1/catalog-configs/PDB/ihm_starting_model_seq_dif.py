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

table_name = 'ihm_starting_model_seq_dif'

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
    'asym_id': {},
    'comp_id': {},
    'db_asym_id': {},
    'db_comp_id': {},
    'db_entity_id': {},
    'db_seq_id': {},
    'details': {},
    'entity_id': {},
    'id': {},
    'seq_id': {},
    'starting_model_id': {},
    'Owner': {}
}

column_comment = {
    'structure_id': 'A reference to table entry.id.',
    'asym_id': 'A reference to table struct_asym.id.',
    'comp_id': 'A reference to table chem_comp.id.',
    'db_asym_id': 'type:text\nThe asym/strand identifier for the entity molecule of the database starting model.',
    'db_comp_id': 'type:text\nThe correspinding component identifier for the residue in the database starting model.',
    'db_entity_id': 'type:text\nThe molecular entity of the database starting model.',
    'db_seq_id': 'type:int4\nThe corresponding residue index of the database starting model.',
    'details': 'type:text\nA description of special aspects of the point differences\n between the sequence of the entity or biological unit described\n in the data block and that in the starting model referenced \n from a database.\nexamples:Conversion of modified residue MSE to MET,Point change of PHE to GLU',
    'entity_id': 'A reference to table entity.id.',
    'id': 'type:int4\nA unique identifier for the entry.',
    'seq_id': 'A reference to table entity_poly_seq.num.',
    'starting_model_id': 'A reference to table ihm_starting_model_details.starting_model_id.',
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
        'asym_id', em.builtin_types['text'], nullok=False, comment=column_comment['asym_id'],
    ),
    em.Column.define(
        'comp_id', em.builtin_types['text'], nullok=False, comment=column_comment['comp_id'],
    ),
    em.Column.define(
        'db_asym_id',
        em.builtin_types['text'],
        nullok=False,
        comment=column_comment['db_asym_id'],
    ),
    em.Column.define(
        'db_comp_id',
        em.builtin_types['text'],
        nullok=False,
        comment=column_comment['db_comp_id'],
    ),
    em.Column.define(
        'db_entity_id', em.builtin_types['text'], comment=column_comment['db_entity_id'],
    ),
    em.Column.define(
        'db_seq_id', em.builtin_types['int4'], nullok=False, comment=column_comment['db_seq_id'],
    ),
    em.Column.define('details', em.builtin_types['text'], comment=column_comment['details'],
                     ),
    em.Column.define(
        'entity_id', em.builtin_types['text'], nullok=False, comment=column_comment['entity_id'],
    ),
    em.Column.define('id', em.builtin_types['int4'], nullok=False, comment=column_comment['id'],
                     ),
    em.Column.define(
        'seq_id', em.builtin_types['int4'], nullok=False, comment=column_comment['seq_id'],
    ),
    em.Column.define(
        'starting_model_id',
        em.builtin_types['text'],
        nullok=False,
        comment=column_comment['starting_model_id'],
    ),
    em.Column.define('Owner', em.builtin_types['text'], comment=column_comment['Owner'],
                     ),
]

visible_columns = {
    '*': [
        'RID', {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_starting_model_seq_dif_structure_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table entry.id.',
            'markdown_name': 'structure id'
        }, {
            'source': [{
                'outbound': ['PDB', 'ihm_starting_model_seq_dif_asym_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table struct_asym.id.',
            'markdown_name': 'asym id'
        }, {
            'source': [{
                'outbound': ['PDB', 'ihm_starting_model_seq_dif_comp_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table chem_comp.id.',
            'markdown_name': 'comp id'
        }, 'db_asym_id', 'db_comp_id', 'db_entity_id', 'db_seq_id', 'details', {
            'source': [{
                'outbound': ['PDB', 'ihm_starting_model_seq_dif_entity_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table entity.id.',
            'markdown_name': 'entity id'
        }, 'id', {
            'source': [{
                'outbound': ['PDB', 'ihm_starting_model_seq_dif_seq_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table entity_poly_seq.num.',
            'markdown_name': 'seq id'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_starting_model_seq_dif_starting_model_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table ihm_starting_model_details.starting_model_id.',
            'markdown_name': 'starting model id'
        }, ['PDB', 'ihm_starting_model_seq_dif_RCB_fkey'],
        ['PDB', 'ihm_starting_model_seq_dif_RMB_fkey'], 'RCT', 'RMT',
        ['PDB', 'ihm_starting_model_seq_dif_Owner_fkey']
    ],
    'entry': [
        {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_starting_model_seq_dif_structure_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table entry.id.',
            'markdown_name': 'structure id'
        }, {
            'source': [{
                'outbound': ['PDB', 'ihm_starting_model_seq_dif_asym_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table struct_asym.id.',
            'markdown_name': 'asym id'
        }, {
            'source': [{
                'outbound': ['PDB', 'ihm_starting_model_seq_dif_comp_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table chem_comp.id.',
            'markdown_name': 'comp id'
        }, 'db_asym_id', 'db_comp_id', 'db_entity_id', 'db_seq_id', 'details', {
            'source': [{
                'outbound': ['PDB', 'ihm_starting_model_seq_dif_entity_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table entity.id.',
            'markdown_name': 'entity id'
        }, 'id', {
            'source': [{
                'outbound': ['PDB', 'ihm_starting_model_seq_dif_seq_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table entity_poly_seq.num.',
            'markdown_name': 'seq id'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_starting_model_seq_dif_starting_model_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table ihm_starting_model_details.starting_model_id.',
            'markdown_name': 'starting model id'
        }
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
    em.Key.define(['RID'], constraint_names=[('PDB', 'ihm_starting_model_seq_dif_RIDkey1')],
                  ),
    em.Key.define(
        ['structure_id', 'id'],
        constraint_names=[('PDB', 'ihm_starting_model_seq_dif_primary_key')],
    ),
]

fkey_defs = [
    em.ForeignKey.define(
        ['Owner'],
        'public',
        'Catalog_Group', ['ID'],
        constraint_names=[('PDB', 'ihm_starting_model_seq_dif_Owner_fkey')],
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
        constraint_names=[('PDB', 'ihm_starting_model_seq_dif_RCB_fkey')],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
    ),
    em.ForeignKey.define(
        ['RMB'],
        'public',
        'ERMrest_Client', ['ID'],
        constraint_names=[('PDB', 'ihm_starting_model_seq_dif_RMB_fkey')],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
    ),
    em.ForeignKey.define(
        ['structure_id'],
        'PDB',
        'entry', ['id'],
        constraint_names=[('PDB', 'ihm_starting_model_seq_dif_structure_id_fkey')],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
        on_update='CASCADE',
        on_delete='SET NULL',
    ),
    em.ForeignKey.define(
        ['structure_id', 'asym_id'],
        'PDB',
        'struct_asym', ['structure_id', 'id'],
        constraint_names=[('PDB', 'ihm_starting_model_seq_dif_asym_id_fkey')],
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
        ['structure_id', 'starting_model_id'],
        'PDB',
        'ihm_starting_model_details', ['structure_id', 'starting_model_id'],
        constraint_names=[('PDB', 'ihm_starting_model_seq_dif_starting_model_id_fkey')],
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
        ['structure_id', 'comp_id', 'entity_id', 'seq_id'],
        'PDB',
        'entity_poly_seq', ['structure_id', 'mon_id', 'entity_id', 'num'],
        constraint_names=[('PDB', 'ihm_starting_model_seq_dif_mm_poly_res_label_fkey')],
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
