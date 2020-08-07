import argparse
from deriva.core import ErmrestCatalog, AttrDict, get_credential
import deriva.core.ermrest_model as em
from deriva.core.ermrest_config import tag as chaise_tags
from deriva.utils.catalog.manage.update_catalog import CatalogUpdater, parse_args

groups = {}

table_name = 'ihm_starting_model_details'

schema_name = 'PDB'

column_annotations = {
    'structure_id': {},
    'asym_id': {},
    'dataset_list_id': {},
    'description': {},
    'entity_description': {},
    'entity_id': {},
    'entity_poly_segment_id': {},
    'starting_model_auth_asym_id': {},
    'starting_model_id': {},
    'starting_model_sequence_offset': {},
    'starting_model_source': {},
    'Owner': {},
    'mmCIF_File_URL': {
        chaise_tags.asset: {
            'md5': 'mmCIF_File_MD5',
            'url_pattern': '/hatrac/pdb/mmCIF/{{$moment.year}}/{{{mmCIF_File_MD5}}}',
            'filename_column': 'mmCIF_File_Name',
            'byte_count_column': 'mmCIF_File_Bytes'
        }
    }
}

column_comment = {
    'structure_id': 'A reference to table entry.id.',
    'asym_id': 'A reference to table struct_asym.id.',
    'dataset_list_id': 'A reference to table ihm_dataset_list.id.',
    'description': 'type:text\nAdditional description regarding the starting model.',
    'entity_description': 'type:text\nA text description of the molecular entity\n',
    'entity_id': 'A reference to table entity.id.',
    'entity_poly_segment_id': 'A reference to table ihm_entity_poly_segment.id.',
    'starting_model_auth_asym_id': 'type:text\nThe author assigned chainId/auth_asym_id corresponding to this starting model. \n This corresponds to the chainId/auth_asym_id of the experimental models in the\n PDB or comparative models in the Model Archive or the starting models referenced\n via a DOI. If starting models are included in IHM_STARTING_MODEL_COORD, then\n this will be the same as _ihm_starting_model_details.asym_id.',
    'starting_model_id': 'type:text\nA unique identifier for the starting structural model.',
    'starting_model_sequence_offset': 'type:int4\nThe offset in residue numbering between the starting model and the deposited I/H model, if applicable. \n I/H model residue number = Starting model residue number + offset',
    'starting_model_source': 'type:text\nThe source of the starting model.',
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
        'dataset_list_id',
        em.builtin_types['int4'],
        nullok=False,
        comment=column_comment['dataset_list_id'],
    ),
    em.Column.define(
        'description', em.builtin_types['text'], comment=column_comment['description'],
    ),
    em.Column.define(
        'entity_description',
        em.builtin_types['text'],
        comment=column_comment['entity_description'],
    ),
    em.Column.define(
        'entity_id', em.builtin_types['text'], nullok=False, comment=column_comment['entity_id'],
    ),
    em.Column.define(
        'entity_poly_segment_id',
        em.builtin_types['int4'],
        comment=column_comment['entity_poly_segment_id'],
    ),
    em.Column.define(
        'starting_model_auth_asym_id',
        em.builtin_types['text'],
        nullok=False,
        comment=column_comment['starting_model_auth_asym_id'],
    ),
    em.Column.define(
        'starting_model_id',
        em.builtin_types['text'],
        nullok=False,
        comment=column_comment['starting_model_id'],
    ),
    em.Column.define(
        'starting_model_sequence_offset',
        em.builtin_types['int4'],
        comment=column_comment['starting_model_sequence_offset'],
    ),
    em.Column.define(
        'starting_model_source',
        em.builtin_types['text'],
        nullok=False,
        comment=column_comment['starting_model_source'],
    ),
    em.Column.define('Owner', em.builtin_types['text'], comment=column_comment['Owner'],
                     ),
    em.Column.define(
        'mmCIF_File_URL',
        em.builtin_types['text'],
        annotations=column_annotations['mmCIF_File_URL'],
    ),
    em.Column.define('mmCIF_File_Name', em.builtin_types['text'],
                     ),
    em.Column.define('mmCIF_File_MD5', em.builtin_types['text'],
                     ),
    em.Column.define('mmCIF_File_Bytes', em.builtin_types['int8'],
                     ),
    em.Column.define('Entity_poly_segment_RID', em.builtin_types['text'],
                     ),
]

visible_columns = {
    '*': [
        'RID', {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_starting_model_details_structure_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table entry.id.',
            'markdown_name': 'structure id'
        }, 'starting_model_id', {
            'source': [{
                'outbound': ['PDB', 'ihm_starting_model_details_entity_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table entity.id.',
            'markdown_name': 'entity id'
        }, 'entity_description', {
            'source': [{
                'outbound': ['PDB', 'ihm_starting_model_details_asym_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table struct_asym.id.',
            'markdown_name': 'asym id'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_starting_model_details_entity_poly_segment_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table ihm_entity_poly_segment.id.',
            'markdown_name': 'entity poly segment id'
        }, ['PDB', 'ihm_starting_model_details_starting_model_source_fkey'],
        'starting_model_auth_asym_id', 'starting_model_sequence_offset', 'description', {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_starting_model_details_dataset_list_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table ihm_dataset_list.id.',
            'markdown_name': 'dataset list id'
        }, 'mmCIF_File_URL'
    ],
    'entry': [
        {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_starting_model_details_structure_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table entry.id.',
            'markdown_name': 'structure id'
        }, 'starting_model_id', {
            'source': [{
                'outbound': ['PDB', 'ihm_starting_model_details_entity_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table entity.id.',
            'markdown_name': 'entity id'
        }, 'entity_description', {
            'source': [{
                'outbound': ['PDB', 'ihm_starting_model_details_asym_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table struct_asym.id.',
            'markdown_name': 'asym id'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_starting_model_details_entity_poly_segment_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table ihm_entity_poly_segment.id.',
            'markdown_name': 'entity poly segment id'
        }, ['PDB', 'ihm_starting_model_details_starting_model_source_fkey'],
        'starting_model_auth_asym_id', 'starting_model_sequence_offset', 'description', {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_starting_model_details_dataset_list_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table ihm_dataset_list.id.',
            'markdown_name': 'dataset list id'
        }, 'mmCIF_File_URL'
    ],
    'detailed': [
        'RID', {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_starting_model_details_structure_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table entry.id.',
            'markdown_name': 'structure id'
        }, 'starting_model_id', {
            'source': [{
                'outbound': ['PDB', 'ihm_starting_model_details_entity_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table entity.id.',
            'markdown_name': 'entity id'
        }, 'entity_description', {
            'source': [{
                'outbound': ['PDB', 'ihm_starting_model_details_asym_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table struct_asym.id.',
            'markdown_name': 'asym id'
        }, {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_starting_model_details_entity_poly_segment_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table ihm_entity_poly_segment.id.',
            'markdown_name': 'entity poly segment id'
        }, ['PDB', 'ihm_starting_model_details_starting_model_source_fkey'],
        'starting_model_auth_asym_id', 'starting_model_sequence_offset', 'description', {
            'source': [
                {
                    'outbound': ['PDB', 'ihm_starting_model_details_dataset_list_id_fkey']
                }, 'RID'
            ],
            'comment': 'A reference to table ihm_dataset_list.id.',
            'markdown_name': 'dataset list id'
        }, 'mmCIF_File_URL', {
            'source': 'mmCIF_File_Bytes',
            'markdown_name': 'mmCIF File Size (Bytes)'
        }, ['PDB', 'ihm_starting_model_details_RCB_fkey'],
        ['PDB', 'ihm_starting_model_details_RMB_fkey'], 'RCT', 'RMT',
        ['PDB', 'ihm_starting_model_details_Owner_fkey']
    ]
}

visible_foreign_keys = {
    'filter': 'detailed',
    'detailed': [
        ['PDB', 'ihm_starting_comparative_models_starting_model_id_fkey'],
        ['PDB', 'ihm_starting_computational_models_starting_model_id_fkey'],
        ['PDB', 'ihm_starting_model_seq_dif_starting_model_id_fkey'],
        ['PDB', 'ihm_model_representation_details_starting_model_id_fkey']
    ]
}

table_display = {'row_name': {'row_markdown_pattern': '{{{starting_model_id}}}'}}

table_annotations = {
    chaise_tags.table_display: table_display,
    chaise_tags.visible_columns: visible_columns,
    chaise_tags.visible_foreign_keys: visible_foreign_keys,
}

table_comment = 'Starting structural models used in integrative modeling'

table_acls = {}

table_acl_bindings = {}

key_defs = [
    em.Key.define(
        ['structure_id', 'starting_model_id'],
        constraint_names=[['PDB', 'ihm_starting_model_details_primary_key']],
    ),
    em.Key.define(['RID'], constraint_names=[['PDB', 'ihm_starting_model_details_RIDkey1']],
                  ),
    em.Key.define(
        ['RID', 'starting_model_id'],
        constraint_names=[['PDB', 'ihm_starting_model_details_RID_starting_model_id_key']],
    ),
]

fkey_defs = [
    em.ForeignKey.define(
        ['RMB'],
        'public',
        'ERMrest_Client', ['ID'],
        constraint_names=[['PDB', 'ihm_starting_model_details_RMB_fkey']],
    ),
    em.ForeignKey.define(
        ['RCB'],
        'public',
        'ERMrest_Client', ['ID'],
        constraint_names=[['PDB', 'ihm_starting_model_details_RCB_fkey']],
    ),
    em.ForeignKey.define(
        ['starting_model_source'],
        'Vocab',
        'ihm_starting_model_details_starting_model_source', ['Name'],
        constraint_names=[['PDB', 'ihm_starting_model_details_starting_model_source_fkey']],
    ),
    em.ForeignKey.define(
        ['structure_id', 'asym_id'],
        'PDB',
        'struct_asym', ['structure_id', 'id'],
        constraint_names=[['PDB', 'ihm_starting_model_details_asym_id_fkey']],
        annotations={
            chaise_tags.foreign_key: {
                'domain_filter_pattern': 'structure_id={{structure_id}}'
            }
        },
        on_update='CASCADE',
        on_delete='SET NULL',
    ),
    em.ForeignKey.define(
        ['dataset_list_id', 'structure_id'],
        'PDB',
        'ihm_dataset_list', ['id', 'structure_id'],
        constraint_names=[['PDB', 'ihm_starting_model_details_dataset_list_id_fkey']],
        annotations={
            chaise_tags.foreign_key: {
                'domain_filter_pattern': 'structure_id={{structure_id}}'
            }
        },
        on_update='CASCADE',
        on_delete='SET NULL',
    ),
    em.ForeignKey.define(
        ['structure_id', 'entity_id'],
        'PDB',
        'entity', ['structure_id', 'id'],
        constraint_names=[['PDB', 'ihm_starting_model_details_entity_id_fkey']],
        annotations={
            chaise_tags.foreign_key: {
                'domain_filter_pattern': 'structure_id={{structure_id}}'
            }
        },
        on_update='CASCADE',
        on_delete='SET NULL',
    ),
    em.ForeignKey.define(
        ['structure_id', 'entity_poly_segment_id'],
        'PDB',
        'ihm_entity_poly_segment', ['structure_id', 'id'],
        constraint_names=[['PDB', 'ihm_starting_model_details_entity_poly_segment_id_fk']],
        annotations={
            chaise_tags.foreign_key: {
                'domain_filter_pattern': 'structure_id={{structure_id}}'
            }
        },
        on_update='CASCADE',
        on_delete='SET NULL',
    ),
    em.ForeignKey.define(
        ['entity_poly_segment_id', 'Entity_poly_segment_RID'],
        'PDB',
        'ihm_entity_poly_segment', ['id', 'RID'],
        constraint_names=[['PDB', 'ihm_starting_model_details_entity_poly_segment_id_fkey']],
        annotations={
            chaise_tags.foreign_key: {
                'domain_filter_pattern': 'structure_id={{structure_id}}'
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
