import argparse
from deriva.core import ErmrestCatalog, AttrDict, get_credential
import deriva.core.ermrest_model as em
from deriva.core.ermrest_config import tag as chaise_tags
from deriva.utils.catalog.manage.update_catalog import CatalogUpdater, parse_args

groups = {}

table_name = 'struct_asym'

schema_name = 'PDB'

column_annotations = {
    'structure_id': {},
    'details': {},
    'entity_id': {},
    'id': {},
    'pdbx_PDB_id': {},
    'pdbx_alt_id': {},
    'pdbx_blank_PDB_chainid_flag': {},
    'pdbx_modified': {},
    'pdbx_order': {},
    'pdbx_type': {},
    'Owner': {}
}

column_comment = {
    'structure_id': 'A reference to table entry.id.',
    'details': 'type:text\nA description of special aspects of this portion of the contents\n of the asymmetric unit.\nexamples:The drug binds to this enzyme in two roughly\n                                  twofold symmetric modes. Hence this\n                                  biological unit (3) is roughly twofold\n                                  symmetric to biological unit (2). Disorder in\n                                  the protein chain indicated with alternative\n                                  ID 2 should be used with this biological unit.',
    'entity_id': 'A reference to table entity.id.',
    'id': 'type:text\nThe value of _struct_asym.id must uniquely identify a record in\n the STRUCT_ASYM list.\n\n Note that this item need not be a number; it can be any unique\n identifier.\nexamples:1,A,2B3',
    'pdbx_PDB_id': 'type:text\nThis data item is a pointer to _atom_site.pdbx_PDB_strand_id the\n ATOM_SITE category.\nexamples:1ABC',
    'pdbx_alt_id': 'type:text\nThis data item is a pointer to _atom_site.ndb_alias_strand_id the\n ATOM_SITE category.',
    'pdbx_blank_PDB_chainid_flag': 'type:text\nA flag indicating that this entity was originally labeled\n with a blank PDB chain id.',
    'pdbx_modified': 'type:text\nThis data item indicates whether the structural elements are modified.\nexamples:y',
    'pdbx_order': 'type:int4\nThis data item gives the order of the structural elements in the\n ATOM_SITE category.',
    'pdbx_type': 'type:text\nThis data item describes the general type of the structural elements\n in the ATOM_SITE category.',
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
    em.Column.define('details', em.builtin_types['text'], comment=column_comment['details'],
                     ),
    em.Column.define(
        'entity_id', em.builtin_types['text'], nullok=False, comment=column_comment['entity_id'],
    ),
    em.Column.define('id', em.builtin_types['text'], nullok=False, comment=column_comment['id'],
                     ),
    em.Column.define(
        'pdbx_PDB_id', em.builtin_types['text'], comment=column_comment['pdbx_PDB_id'],
    ),
    em.Column.define(
        'pdbx_alt_id', em.builtin_types['text'], comment=column_comment['pdbx_alt_id'],
    ),
    em.Column.define(
        'pdbx_blank_PDB_chainid_flag',
        em.builtin_types['text'],
        comment=column_comment['pdbx_blank_PDB_chainid_flag'],
    ),
    em.Column.define(
        'pdbx_modified', em.builtin_types['text'], comment=column_comment['pdbx_modified'],
    ),
    em.Column.define(
        'pdbx_order', em.builtin_types['int4'], comment=column_comment['pdbx_order'],
    ),
    em.Column.define('pdbx_type', em.builtin_types['text'], comment=column_comment['pdbx_type'],
                     ),
    em.Column.define('Owner', em.builtin_types['text'], comment=column_comment['Owner'],
                     ),
]

generated = None

visible_columns = {
    '*': [
        'RID', {
            'source': [{
                'outbound': ['PDB', 'struct_asym_structure_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table entry.id.',
            'markdown_name': 'structure id'
        }, 'id', {
            'source': [{
                'outbound': ['PDB', 'struct_asym_entity_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table entity.id.',
            'markdown_name': 'entity id'
        }, 'pdbx_PDB_id', 'pdbx_alt_id', ['PDB', 'struct_asym_pdbx_blank_PDB_chainid_flag_fkey'],
        'pdbx_modified', 'pdbx_order', ['PDB', 'struct_asym_pdbx_type_fkey'], 'details'
    ],
    'entry': [
        {
            'source': [{
                'outbound': ['PDB', 'struct_asym_structure_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table entry.id.',
            'markdown_name': 'structure id'
        }, 'id', {
            'source': [{
                'outbound': ['PDB', 'struct_asym_entity_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table entity.id.',
            'markdown_name': 'entity id'
        }, 'pdbx_PDB_id', 'pdbx_alt_id', ['PDB', 'struct_asym_pdbx_blank_PDB_chainid_flag_fkey'],
        'pdbx_modified', 'pdbx_order', ['PDB', 'struct_asym_pdbx_type_fkey'], 'details'
    ]
}

visible_foreign_keys = {
    'filter': 'detailed',
    'detailed': [
        ['PDB', 'ihm_model_representation_details_entity_asym_id_fkey'],
        ['PDB', 'ihm_struct_assembly_details_asym_id_fkey'],
        ['PDB', 'ihm_starting_model_details_asym_id_fkey'],
        ['PDB', 'ihm_starting_model_seq_dif_asym_id_fkey'],
        ['PDB', 'ihm_cross_link_restraint_asym_id_1_fkey'],
        ['PDB', 'ihm_cross_link_restraint_asym_id_2_fkey'],
        ['PDB', 'ihm_hydroxyl_radical_fp_restraint_asym_id_fkey'],
        ['PDB', 'ihm_predicted_contact_restraint_asym_id_1_fkey'],
        ['PDB', 'ihm_predicted_contact_restraint_asym_id_2_fkey'],
        ['PDB', 'ihm_poly_atom_feature_asym_id_fkey'],
        ['PDB', 'ihm_poly_residue_feature_asym_id_fkey'],
        ['PDB', 'ihm_non_poly_feature_asym_id_fkey'],
        ['PDB', 'ihm_interface_residue_feature_binding_partner_asym_id_fkey'],
        ['PDB', 'ihm_residues_not_modeled_asym_id_fkey'],
        ['PDB', 'ihm_localization_density_files_asym_id_fkey']
    ]
}

table_display = {'row_name': {'row_markdown_pattern': '{{{id}}}'}}

table_annotations = {
    chaise_tags.generated: generated,
    chaise_tags.table_display: table_display,
    chaise_tags.visible_columns: visible_columns,
    chaise_tags.visible_foreign_keys: visible_foreign_keys,
}

table_comment = 'Instances of entities, both polymeric and non-polymeric'

table_acls = {}

table_acl_bindings = {}

key_defs = [
    em.Key.define(['RID'], constraint_names=[['PDB', 'struct_asym_RIDkey1']],
                  ),
    em.Key.define(['id', 'structure_id'], constraint_names=[['PDB', 'struct_asym_primary_key']],
                  ),
    em.Key.define(['id', 'RID'], constraint_names=[['PDB', 'struct_asym_RID_id_key']],
                  ),
]

fkey_defs = [
    em.ForeignKey.define(
        ['RCB'],
        'public',
        'ERMrest_Client', ['ID'],
        constraint_names=[['PDB', 'struct_asym_RCB_fkey']],
    ),
    em.ForeignKey.define(
        ['RMB'],
        'public',
        'ERMrest_Client', ['ID'],
        constraint_names=[['PDB', 'struct_asym_RMB_fkey']],
    ),
    em.ForeignKey.define(
        ['pdbx_type'],
        'Vocab',
        'struct_asym_pdbx_type', ['Name'],
        constraint_names=[['PDB', 'struct_asym_pdbx_type_fkey']],
    ),
    em.ForeignKey.define(
        ['pdbx_blank_PDB_chainid_flag'],
        'Vocab',
        'struct_asym_pdbx_blank_PDB_chainid_flag', ['Name'],
        constraint_names=[['PDB', 'struct_asym_pdbx_blank_PDB_chainid_flag_fkey']],
    ),
    em.ForeignKey.define(
        ['structure_id', 'entity_id'],
        'PDB',
        'entity', ['structure_id', 'id'],
        constraint_names=[['PDB', 'struct_asym_entity_id_fkey']],
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
