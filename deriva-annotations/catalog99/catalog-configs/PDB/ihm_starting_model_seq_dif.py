import argparse
from deriva.core import ErmrestCatalog, AttrDict, get_credential
import deriva.core.ermrest_model as em
from deriva.core.ermrest_config import tag as chaise_tags
from deriva.utils.catalog.manage.update_catalog import CatalogUpdater, parse_args

groups = {}

table_name = 'ihm_starting_model_seq_dif'

schema_name = 'PDB'

column_annotations = {
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
        }, 'id', {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_starting_model_seq_dif_mm_poly_res_label_fkey']
                }, 'entity_id'
            ],
            'comment': 'A reference to table entity_poly_seq.entity_id.',
            'markdown_name': 'entity id'
        }, {
            'source': [{
                'outbound': ['PDB', 'ihm_starting_model_seq_dif_asym_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table struct_asym.id.',
            'markdown_name': 'asym id'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_starting_model_seq_dif_mm_poly_res_label_fkey']
                }, 'num'
            ],
            'comment': 'A reference to table entity_poly_seq.num.',
            'markdown_name': 'seq id'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_starting_model_seq_dif_mm_poly_res_label_fkey']
                }, 'mon_id'
            ],
            'comment': 'A reference to table entity_poly_seq.mon_id.',
            'markdown_name': 'comp id'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_starting_model_seq_dif_starting_model_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table ihm_starting_model_details.starting_model_id.',
            'markdown_name': 'starting model id'
        }, 'db_asym_id', 'db_seq_id', 'db_comp_id', 'db_entity_id', 'details', {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_starting_model_seq_dif_mm_poly_res_label_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to the polymeric residue composite key',
            'markdown_name': 'polymeric residue'
        }
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
        }, 'id', {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_starting_model_seq_dif_mm_poly_res_label_fkey']
                }, 'entity_id'
            ],
            'comment': 'A reference to table entity_poly_seq.entity_id.',
            'markdown_name': 'entity id'
        }, {
            'source': [{
                'outbound': ['PDB', 'ihm_starting_model_seq_dif_asym_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table struct_asym.id.',
            'markdown_name': 'asym id'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_starting_model_seq_dif_mm_poly_res_label_fkey']
                }, 'num'
            ],
            'comment': 'A reference to table entity_poly_seq.num.',
            'markdown_name': 'seq id'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_starting_model_seq_dif_mm_poly_res_label_fkey']
                }, 'mon_id'
            ],
            'comment': 'A reference to table entity_poly_seq.mon_id.',
            'markdown_name': 'comp id'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_starting_model_seq_dif_starting_model_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table ihm_starting_model_details.starting_model_id.',
            'markdown_name': 'starting model id'
        }, 'db_asym_id', 'db_seq_id', 'db_comp_id', 'db_entity_id', 'details', {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_starting_model_seq_dif_mm_poly_res_label_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to the polymeric residue composite key',
            'markdown_name': 'polymeric residue'
        }
    ],
    'detailed': [
        'RID', {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_starting_model_seq_dif_structure_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table entry.id.',
            'markdown_name': 'structure id'
        }, 'id', {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_starting_model_seq_dif_mm_poly_res_label_fkey']
                }, 'entity_id'
            ],
            'comment': 'A reference to table entity_poly_seq.entity_id.',
            'markdown_name': 'entity id'
        }, {
            'source': [{
                'outbound': ['PDB', 'ihm_starting_model_seq_dif_asym_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table struct_asym.id.',
            'markdown_name': 'asym id'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_starting_model_seq_dif_mm_poly_res_label_fkey']
                }, 'num'
            ],
            'comment': 'A reference to table entity_poly_seq.num.',
            'markdown_name': 'seq id'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_starting_model_seq_dif_mm_poly_res_label_fkey']
                }, 'mon_id'
            ],
            'comment': 'A reference to table entity_poly_seq.mon_id.',
            'markdown_name': 'comp id'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_starting_model_seq_dif_starting_model_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table ihm_starting_model_details.starting_model_id.',
            'markdown_name': 'starting model id'
        }, 'db_asym_id', 'db_seq_id', 'db_comp_id', 'db_entity_id', 'details', {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_starting_model_seq_dif_mm_poly_res_label_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to the polymeric residue composite key',
            'markdown_name': 'polymeric residue'
        }, ['PDB', 'ihm_starting_model_seq_dif_RCB_fkey'],
        ['PDB', 'ihm_starting_model_seq_dif_RMB_fkey'], 'RCT', 'RMT',
        ['PDB', 'ihm_starting_model_seq_dif_Owner_fkey']
    ]
}

table_annotations = {chaise_tags.visible_columns: visible_columns, }

table_comment = 'Point mutations in the sequence of the starting model'

table_acls = {}

table_acl_bindings = {}

key_defs = [
    em.Key.define(
        ['id', 'structure_id'],
        constraint_names=[['PDB', 'ihm_starting_model_seq_dif_primary_key']],
    ),
    em.Key.define(['RID'], constraint_names=[['PDB', 'ihm_starting_model_seq_dif_RIDkey1']],
                  ),
]

fkey_defs = [
    em.ForeignKey.define(
        ['RMB'],
        'public',
        'ERMrest_Client', ['ID'],
        constraint_names=[['PDB', 'ihm_starting_model_seq_dif_RMB_fkey']],
    ),
    em.ForeignKey.define(
        ['RCB'],
        'public',
        'ERMrest_Client', ['ID'],
        constraint_names=[['PDB', 'ihm_starting_model_seq_dif_RCB_fkey']],
    ),
    em.ForeignKey.define(
        ['structure_id', 'starting_model_id'],
        'PDB',
        'ihm_starting_model_details', ['structure_id', 'starting_model_id'],
        constraint_names=[['PDB', 'ihm_starting_model_seq_dif_starting_model_id_fkey']],
        annotations={
            chaise_tags.foreign_key: {
                'domain_filter_pattern': 'structure_id={{structure_id}}'
            }
        },
        on_update='CASCADE',
        on_delete='SET NULL',
    ),
    em.ForeignKey.define(
        ['asym_id', 'structure_id'],
        'PDB',
        'struct_asym', ['id', 'structure_id'],
        constraint_names=[['PDB', 'ihm_starting_model_seq_dif_asym_id_fkey']],
        annotations={
            chaise_tags.foreign_key: {
                'domain_filter_pattern': 'structure_id={{structure_id}}'
            }
        },
        on_update='CASCADE',
        on_delete='SET NULL',
    ),
    em.ForeignKey.define(
        ['structure_id', 'seq_id', 'comp_id', 'entity_id'],
        'PDB',
        'entity_poly_seq', ['structure_id', 'num', 'mon_id', 'entity_id'],
        constraint_names=[['PDB', 'ihm_starting_model_seq_dif_mm_poly_res_label_fkey']],
        annotations={
            chaise_tags.foreign_key: {
                'from_name': 'Ihm Starting Model Seq Dif',
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
