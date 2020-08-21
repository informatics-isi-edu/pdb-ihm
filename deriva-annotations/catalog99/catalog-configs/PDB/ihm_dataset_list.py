import argparse
from deriva.core import ErmrestCatalog, AttrDict, get_credential
import deriva.core.ermrest_model as em
from deriva.core.ermrest_config import tag as chaise_tags
from deriva.utils.catalog.manage.update_catalog import CatalogUpdater, parse_args

groups = {}

table_name = 'ihm_dataset_list'

schema_name = 'PDB'

column_annotations = {
    'structure_id': {},
    'data_type': {},
    'database_hosted': {},
    'details': {},
    'id': {},
    'Owner': {}
}

column_comment = {
    'structure_id': 'A reference to table entry.id.',
    'data_type': 'type:text\nThe type of data held in the dataset.',
    'database_hosted': 'type:text\nA flag that indicates whether the dataset is archived in \n an IHM related database or elsewhere.',
    'details': 'type:text\nDetails regarding the dataset, especially those types not listed in\n _ihm_dataset_list.data_type.',
    'id': 'type:int4\nA unique identifier for the dataset.',
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
        'data_type', em.builtin_types['text'], nullok=False, comment=column_comment['data_type'],
    ),
    em.Column.define(
        'database_hosted',
        em.builtin_types['text'],
        nullok=False,
        comment=column_comment['database_hosted'],
    ),
    em.Column.define('details', em.builtin_types['text'], comment=column_comment['details'],
                     ),
    em.Column.define('id', em.builtin_types['int4'], nullok=False, comment=column_comment['id'],
                     ),
    em.Column.define('Owner', em.builtin_types['text'], comment=column_comment['Owner'],
                     ),
]

visible_columns = {
    '*': [
        'RID', {
            'source': [{
                'outbound': ['PDB', 'ihm_dataset_list_structure_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table entry.id.',
            'markdown_name': 'structure id'
        }, 'id', ['PDB', 'ihm_dataset_list_data_type_fkey'],
        ['PDB', 'ihm_dataset_list_database_hosted_fkey'], 'details'
    ],
    'entry': [
        {
            'source': [{
                'outbound': ['PDB', 'ihm_dataset_list_structure_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table entry.id.',
            'markdown_name': 'structure id'
        }, 'id', ['PDB', 'ihm_dataset_list_data_type_fkey'],
        ['PDB', 'ihm_dataset_list_database_hosted_fkey'], 'details'
    ],
    'detailed': [
        'RID', {
            'source': [{
                'outbound': ['PDB', 'ihm_dataset_list_structure_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table entry.id.',
            'markdown_name': 'structure id'
        }, 'id', ['PDB', 'ihm_dataset_list_data_type_fkey'],
        ['PDB', 'ihm_dataset_list_database_hosted_fkey'], 'details',
        ['PDB', 'ihm_dataset_list_RCB_fkey'], ['PDB', 'ihm_dataset_list_RMB_fkey'], 'RCT', 'RMT',
        ['PDB', 'ihm_dataset_list_Owner_fkey']
    ]
}

visible_foreign_keys = {
    'filter': 'detailed',
    'detailed': [
        ['PDB', 'ihm_dataset_group_link_dataset_list_id_fkey'],
        ['PDB', 'ihm_dataset_related_db_reference_dataset_list_id_fkey'],
        ['PDB', 'ihm_dataset_external_reference_dataset_list_id_fkey'],
        ['PDB', 'ihm_related_datasets_dataset_list_id_derived_fkey'],
        ['PDB', 'ihm_related_datasets_dataset_list_id_primary_fkey'],
        ['PDB', 'ihm_starting_model_details_dataset_list_id_fkey'],
        ['PDB', 'ihm_starting_comparative_models_template_dataset_list_id_fkey'],
        ['PDB', 'ihm_poly_probe_conjugate_dataset_list_id_fkey'],
        ['PDB', 'ihm_ligand_probe_dataset_list_id_fkey'],
        ['PDB', 'ihm_cross_link_list_dataset_list_id_fkey'],
        ['PDB', 'ihm_2dem_class_average_restraint_dataset_list_id_fkey'],
        ['PDB', 'ihm_3dem_restraint_dataset_list_id_fkey'],
        ['PDB', 'ihm_sas_restraint_dataset_list_id_fkey'],
        ['PDB', 'ihm_epr_restraint_dataset_list_id_fkey'],
        ['PDB', 'ihm_hydroxyl_radical_fp_restraint_dataset_list_id_fkey'],
        ['PDB', 'ihm_predicted_contact_restraint_dataset_list_id_fkey'],
        ['PDB', 'ihm_interface_residue_feature_dataset_list_id_fkey'],
        ['PDB', 'ihm_derived_distance_restraint_dataset_list_id_fkey'],
        ['PDB', 'ihm_geometric_object_distance_restraint_dataset_list_id_fkey']
    ]
}

table_display = {'row_name': {'row_markdown_pattern': '{{{id}}}'}}

table_annotations = {
    chaise_tags.table_display: table_display,
    chaise_tags.visible_columns: visible_columns,
    chaise_tags.visible_foreign_keys: visible_foreign_keys,
}

table_comment = 'List of all input datasets used in the integrative modeling study'

table_acls = {}

table_acl_bindings = {}

key_defs = [
    em.Key.define(['RID'], constraint_names=[['PDB', 'ihm_dataset_list_RIDkey1']],
                  ),
    em.Key.define(
        ['id', 'structure_id'], constraint_names=[['PDB', 'ihm_dataset_list_primary_key']],
    ),
]

fkey_defs = [
    em.ForeignKey.define(
        ['RCB'],
        'public',
        'ERMrest_Client', ['ID'],
        constraint_names=[['PDB', 'ihm_dataset_list_RCB_fkey']],
    ),
    em.ForeignKey.define(
        ['RMB'],
        'public',
        'ERMrest_Client', ['ID'],
        constraint_names=[['PDB', 'ihm_dataset_list_RMB_fkey']],
    ),
    em.ForeignKey.define(
        ['data_type'],
        'Vocab',
        'ihm_dataset_list_data_type', ['Name'],
        constraint_names=[['PDB', 'ihm_dataset_list_data_type_fkey']],
    ),
    em.ForeignKey.define(
        ['database_hosted'],
        'Vocab',
        'ihm_dataset_list_database_hosted', ['Name'],
        constraint_names=[['PDB', 'ihm_dataset_list_database_hosted_fkey']],
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
