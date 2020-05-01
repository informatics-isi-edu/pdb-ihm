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

table_name = 'entity_poly'

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
    'entity_id': {},
    'nstd_chirality': {},
    'nstd_linkage': {},
    'nstd_monomer': {},
    'pdbx_seq_one_letter_code': {},
    'pdbx_seq_one_letter_code_can': {},
    'pdbx_sequence_evidence_code': {},
    'pdbx_strand_id': {},
    'type': {},
    'Owner': {}
}

column_comment = {
    'structure_id': 'A reference to table entry.id.',
    'entity_id': 'A reference to table entity.id.',
    'nstd_chirality': 'type:text\nA flag to indicate whether the polymer contains at least\n one monomer unit with chirality different from that specified in\n _entity_poly.type.',
    'nstd_linkage': 'type:text\nA flag to indicate whether the polymer contains at least\n one monomer-to-monomer link different from that implied by\n _entity_poly.type.',
    'nstd_monomer': 'type:text\nA flag to indicate whether the polymer contains at least\n one monomer that is not considered standard.',
    'pdbx_seq_one_letter_code': 'type:text\nChemical sequence expressed as string of one-letter\n amino acid codes. Modifications and non-standard\n amino acids are coded as X.\nexamples:HHHH(MSE)AKQRSG or AUCGGAAU,A  for alanine or adenine\nB  for ambiguous asparagine/aspartic-acid\nR  for arginine\nN  for asparagine\nD  for aspartic-acid\nC  for cysteine or cystine or cytosine\nQ  for glutamine\nE  for glutamic-acid\nZ  for ambiguous glutamine/glutamic acid\nG  for glycine or guanine\nH  for histidine\nI  for isoleucine\nL  for leucine\nK  for lysine\nM  for methionine\nF  for phenylalanine\nP  for proline\nS  for serine\nT  for threonine or thymine\nW  for tryptophan\nY  for tyrosine\nV  for valine\nU  for uracil\nO  for water\nX  for other',
    'pdbx_seq_one_letter_code_can': 'type:text\nCannonical chemical sequence expressed as string of\n               one-letter amino acid codes. Modifications are coded\n               as the parent amino acid where possible.\n\nA  for alanine or adenine\nB  for ambiguous asparagine/aspartic-acid\nR  for arginine\nN  for asparagine\nD  for aspartic-acid\nC  for cysteine or cystine or cytosine\nQ  for glutamine\nE  for glutamic-acid\nZ  for ambiguous glutamine/glutamic acid\nG  for glycine or guanine\nH  for histidine\nI  for isoleucine\nL  for leucine\nK  for lysine\nM  for methionine\nF  for phenylalanine\nP  for proline\nS  for serine\nT  for threonine or thymine\nW  for tryptophan\nY  for tyrosine\nV  for valine\nU  for uracil\nexamples:MSHHWGYGKHNGPEHWHKDFPIAKGERQSPVDIDTHTAKYDPSLKPLSVSYDQATSLRILNNGAAFNVEFD',
    'pdbx_sequence_evidence_code': 'type:text\nEvidence for the assignment of the polymer sequence.',
    'pdbx_strand_id': 'type:text\nThe PDB strand/chain id(s) corresponding to this polymer entity.\nexamples:A,B,A,B,A,B,C',
    'type': 'type:text\nThe type of the polymer.',
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
        'entity_id', em.builtin_types['text'], nullok=False, comment=column_comment['entity_id'],
    ),
    em.Column.define(
        'nstd_chirality', em.builtin_types['text'], comment=column_comment['nstd_chirality'],
    ),
    em.Column.define(
        'nstd_linkage', em.builtin_types['text'], comment=column_comment['nstd_linkage'],
    ),
    em.Column.define(
        'nstd_monomer', em.builtin_types['text'], comment=column_comment['nstd_monomer'],
    ),
    em.Column.define(
        'pdbx_seq_one_letter_code',
        em.builtin_types['text'],
        comment=column_comment['pdbx_seq_one_letter_code'],
    ),
    em.Column.define(
        'pdbx_seq_one_letter_code_can',
        em.builtin_types['text'],
        comment=column_comment['pdbx_seq_one_letter_code_can'],
    ),
    em.Column.define(
        'pdbx_sequence_evidence_code',
        em.builtin_types['text'],
        comment=column_comment['pdbx_sequence_evidence_code'],
    ),
    em.Column.define(
        'pdbx_strand_id', em.builtin_types['text'], comment=column_comment['pdbx_strand_id'],
    ),
    em.Column.define('type', em.builtin_types['text'], comment=column_comment['type'],
                     ),
    em.Column.define('Owner', em.builtin_types['text'], comment=column_comment['Owner'],
                     ),
]

visible_columns = {
    '*': [
        'RID', {
            'source': [{
                'outbound': ['PDB', 'entity_poly_structure_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table entry.id.',
            'markdown_name': 'structure id'
        }, {
            'source': [{
                'outbound': ['PDB', 'entity_poly_entity_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table entity.id.',
            'markdown_name': 'entity id'
        }, ['PDB', 'entity_poly_type_fkey'], ['PDB', 'entity_poly_nstd_monomer_fkey'],
        ['PDB', 'entity_poly_nstd_linkage_fkey'],
        ['PDB', 'entity_poly_nstd_chirality_fkey'], 'pdbx_strand_id',
        ['PDB', 'entity_poly_pdbx_sequence_evidence_code_fkey'], 'pdbx_seq_one_letter_code',
        'pdbx_seq_one_letter_code_can'
    ],
    'entry': [
        {
            'source': [{
                'outbound': ['PDB', 'entity_poly_structure_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table entry.id.',
            'markdown_name': 'structure id'
        }, {
            'source': [{
                'outbound': ['PDB', 'entity_poly_entity_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table entity.id.',
            'markdown_name': 'entity id'
        }, ['PDB', 'entity_poly_type_fkey'], ['PDB', 'entity_poly_nstd_monomer_fkey'],
        ['PDB', 'entity_poly_nstd_linkage_fkey'],
        ['PDB', 'entity_poly_nstd_chirality_fkey'], 'pdbx_strand_id',
        ['PDB', 'entity_poly_pdbx_sequence_evidence_code_fkey'], 'pdbx_seq_one_letter_code',
        'pdbx_seq_one_letter_code_can'
    ]
}

visible_foreign_keys = {
    'filter': 'detailed',
    'detailed': [['PDB', 'entity_poly_seq_entity_id_fkey']]
}

table_display = {'row_name': {'row_markdown_pattern': '{{{entity_id}}}'}}

table_annotations = {
    chaise_tags.table_display: table_display,
    chaise_tags.visible_columns: visible_columns,
    chaise_tags.visible_foreign_keys: visible_foreign_keys,
}

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
    em.Key.define(['RID'], constraint_names=[['PDB', 'entity_poly_RIDkey1']],
                  ),
    em.Key.define(
        ['structure_id', 'entity_id'], constraint_names=[['PDB', 'entity_poly_primary_key']],
    ),
]

fkey_defs = [
    em.ForeignKey.define(
        ['nstd_linkage'],
        'Vocab',
        'entity_poly_nstd_linkage', ['ID'],
        constraint_names=[['PDB', 'entity_poly_nstd_linkage_fkey']],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
    ),
    em.ForeignKey.define(
        ['entity_id', 'structure_id'],
        'PDB',
        'entity', ['id', 'structure_id'],
        constraint_names=[['PDB', 'entity_poly_entity_id_fkey']],
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
        ['RCB'],
        'public',
        'ERMrest_Client', ['ID'],
        constraint_names=[['PDB', 'entity_poly_RCB_fkey']],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
    ),
    em.ForeignKey.define(
        ['RMB'],
        'public',
        'ERMrest_Client', ['ID'],
        constraint_names=[['PDB', 'entity_poly_RMB_fkey']],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
    ),
    em.ForeignKey.define(
        ['structure_id'],
        'PDB',
        'entry', ['id'],
        constraint_names=[['PDB', 'entity_poly_structure_id_fkey']],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
        on_update='CASCADE',
        on_delete='SET NULL',
    ),
    em.ForeignKey.define(
        ['type'],
        'Vocab',
        'entity_poly_type', ['ID'],
        constraint_names=[['PDB', 'entity_poly_type_fkey']],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
    ),
    em.ForeignKey.define(
        ['pdbx_sequence_evidence_code'],
        'Vocab',
        'entity_poly_pdbx_sequence_evidence_code', ['ID'],
        constraint_names=[['PDB', 'entity_poly_pdbx_sequence_evidence_code_fkey']],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
    ),
    em.ForeignKey.define(
        ['Owner'],
        'public',
        'Catalog_Group', ['ID'],
        constraint_names=[['PDB', 'entity_poly_Owner_fkey']],
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
        ['nstd_monomer'],
        'Vocab',
        'entity_poly_nstd_monomer', ['ID'],
        constraint_names=[['PDB', 'entity_poly_nstd_monomer_fkey']],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
    ),
    em.ForeignKey.define(
        ['nstd_chirality'],
        'Vocab',
        'entity_poly_nstd_chirality', ['ID'],
        constraint_names=[['PDB', 'entity_poly_nstd_chirality_fkey']],
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
