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

table_name = 'atom_site'

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
    'B_iso_or_equiv': {},
    'Cartn_x': {},
    'Cartn_y': {},
    'Cartn_z': {},
    'auth_asym_id': {},
    'auth_atom_id': {},
    'auth_comp_id': {},
    'auth_seq_id': {},
    'group_PDB': {},
    'id': {},
    'ihm_model_id': {},
    'label_alt_id': {},
    'label_asym_id': {},
    'label_atom_id': {},
    'label_comp_id': {},
    'label_entity_id': {},
    'label_seq_id': {},
    'occupancy': {},
    'pdbx_PDB_model_num': {},
    'pdbx_auth_asym_id': {},
    'pdbx_auth_atom_name': {},
    'pdbx_auth_comp_id': {},
    'pdbx_auth_seq_id': {},
    'pdbx_formal_charge': {},
    'pdbx_label_seq_num': {},
    'type_symbol': {},
    'Owner': {}
}

column_comment = {
    'structure_id': 'type:text\nThe value of _entry.id identifies the data block.\n\n Note that this item need not be a number; it can be any unique\n identifier.',
    'B_iso_or_equiv': 'type:float4\nIsotropic atomic displacement parameter, or equivalent isotropic\n atomic displacement parameter, B~eq~, calculated from the\n anisotropic displacement parameters.\n\n B~eq~ = (1/3) sum~i~[sum~j~(B^ij^ A~i~ A~j~ a*~i~ a*~j~)]\n\n A     = the real space cell lengths\n a*    = the reciprocal space cell lengths\n B^ij^ = 8 pi^2^ U^ij^\n\n Ref: Fischer, R. X. & Tillmanns, E. (1988). Acta Cryst. C44,\n      775-776.\n\n The IUCr Commission on Nomenclature recommends against the use\n of B for reporting atomic displacement parameters. U, being\n directly proportional to B, is preferred.\n\n Note -\n\n The particular type of ADP stored in this item is qualified\n by item _refine.pdbx_adp_type.\n',
    'Cartn_x': 'type:float4\nThe x atom-site coordinate in angstroms specified according to\n a set of orthogonal Cartesian axes related to the cell axes as\n specified by the description given in\n _atom_sites.Cartn_transform_axes.',
    'Cartn_y': 'type:float4\nThe y atom-site coordinate in angstroms specified according to\n a set of orthogonal Cartesian axes related to the cell axes as\n specified by the description given in\n _atom_sites.Cartn_transform_axes.',
    'Cartn_z': 'type:float4\nThe z atom-site coordinate in angstroms specified according to\n a set of orthogonal Cartesian axes related to the cell axes as\n specified by the description given in\n _atom_sites.Cartn_transform_axes.',
    'auth_asym_id': 'type:text\nAn alternative identifier for _atom_site.label_asym_id that\n may be provided by an author in order to match the identification\n used in the publication that describes the structure.',
    'auth_atom_id': 'type:text\nAn alternative identifier for _atom_site.label_atom_id that\n may be provided by an author in order to match the identification\n used in the publication that describes the structure.',
    'auth_comp_id': 'type:text\nAn alternative identifier for _atom_site.label_comp_id that\n may be provided by an author in order to match the identification\n used in the publication that describes the structure.',
    'auth_seq_id': 'type:text\nAn alternative identifier for _atom_site.label_seq_id that\n may be provided by an author in order to match the identification\n used in the publication that describes the structure.\n\n Note that this is not necessarily a number, that the values do\n not have to be positive, and that the value does not have to\n correspond to the value of _atom_site.label_seq_id. The value\n of _atom_site.label_seq_id is required to be a sequential list\n of positive integers.\n\n The author may assign values to _atom_site.auth_seq_id in any\n desired way. For instance, the values may be used to relate\n this structure to a numbering scheme in a homologous structure,\n including sequence gaps or insertion codes. Alternatively, a\n scheme may be used for a truncated polymer that maintains the\n numbering scheme of the full length polymer. In all cases, the\n scheme used here must match the scheme used in the publication\n that describes the structure.',
    'group_PDB': 'type:text\nThe group of atoms to which the atom site belongs. This data\n item is provided for compatibility with the original Protein\n Data Bank format, and only for that purpose.',
    'id': 'type:text\nThe value of _atom_site.id must uniquely identify a record in the\n ATOM_SITE list.\n\n Note that this item need not be a number; it can be any unique\n identifier.\n\n This data item was introduced to provide compatibility between\n small-molecule and macromolecular CIFs. In a small-molecule\n CIF, _atom_site_label is the identifier for the atom. In a\n macromolecular CIF, the atom identifier is the aggregate of\n _atom_site.label_alt_id, _atom_site.label_asym_id,\n _atom_site.label_atom_id, _atom_site.label_comp_id and\n _atom_site.label_seq_id. For the two types of files to be\n compatible, a formal identifier for the category had to be\n introduced that was independent of the different modes of\n identifying the atoms. For compatibility with older CIFs,\n _atom_site_label is aliased to _atom_site.id.\nexamples:5,C12,Ca3g28,Fe3+17,H*251,boron2a,C_a_phe_83_a_0,Zn_Zn_301_A_0',
    'ihm_model_id': 'type:int4\nA unique identifier for the structural model being deposited.',
    'label_alt_id': 'type:text\nA component of the identifier for this atom site.\n For further details, see the definition of the ATOM_SITE_ALT\n category.\n\n This data item is a pointer to _atom_sites_alt.id in the\n ATOM_SITES_ALT category.',
    'label_asym_id': 'type:text\nThe value of _struct_asym.id must uniquely identify a record in\n the STRUCT_ASYM list.\n\n Note that this item need not be a number; it can be any unique\n identifier.',
    'label_atom_id': 'type:text\nA component of the identifier for this atom site.\n\n This data item is a pointer to _chem_comp_atom.atom_id in the\n CHEM_COMP_ATOM category.',
    'label_comp_id': 'type:text\nThe value of _chem_comp.id must uniquely identify each item in\n the CHEM_COMP list.\n\n For protein polymer entities, this is the three-letter code for\n the amino acid.\n\n For nucleic acid polymer entities, this is the one-letter code\n for the base.',
    'label_entity_id': 'type:text\nThe value of _entity.id must uniquely identify a record in the\n ENTITY list.\n\n Note that this item need not be a number; it can be any unique\n identifier.',
    'label_seq_id': 'type:int4\nThis data item is a pointer to _entity_poly_seq.num in the\n ENTITY_POLY_SEQ category.',
    'occupancy': 'type:float4\nThe fraction of the atom type present at this site.\n The sum of the occupancies of all the atom types at this site\n may not significantly exceed 1.0 unless it is a dummy site.',
    'pdbx_PDB_model_num': 'type:int4\nA unique identifier for the structural model being deposited.',
    'pdbx_auth_asym_id': "type:text\nAuthor's strand id.",
    'pdbx_auth_atom_name': "type:text\nAuthor's atom name.",
    'pdbx_auth_comp_id': "type:text\nAuthor's residue name.",
    'pdbx_auth_seq_id': "type:text\nAuthor's sequence identifier.",
    'pdbx_formal_charge': 'type:int4\nThe net integer charge assigned to this atom. This is the\n formal charge assignment normally found in chemical diagrams.\nexamples:1,-1',
    'pdbx_label_seq_num': 'type:text\nSequential residue number used by NDB.',
    'type_symbol': 'type:text\nThe code used to identify the atom species (singular or plural)\n representing this atom type. Normally this code is the element\n symbol. The code may be composed of any character except\n an underscore with the additional proviso that digits designate\n an oxidation state and must be followed by a + or - character.',
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
        'B_iso_or_equiv', em.builtin_types['float4'], comment=column_comment['B_iso_or_equiv'],
    ),
    em.Column.define('Cartn_x', em.builtin_types['float4'], comment=column_comment['Cartn_x'],
                     ),
    em.Column.define('Cartn_y', em.builtin_types['float4'], comment=column_comment['Cartn_y'],
                     ),
    em.Column.define('Cartn_z', em.builtin_types['float4'], comment=column_comment['Cartn_z'],
                     ),
    em.Column.define(
        'auth_asym_id',
        em.builtin_types['text'],
        nullok=False,
        comment=column_comment['auth_asym_id'],
    ),
    em.Column.define(
        'auth_atom_id', em.builtin_types['text'], comment=column_comment['auth_atom_id'],
    ),
    em.Column.define(
        'auth_comp_id', em.builtin_types['text'], comment=column_comment['auth_comp_id'],
    ),
    em.Column.define(
        'auth_seq_id', em.builtin_types['text'], comment=column_comment['auth_seq_id'],
    ),
    em.Column.define('group_PDB', em.builtin_types['text'], comment=column_comment['group_PDB'],
                     ),
    em.Column.define('id', em.builtin_types['text'], nullok=False, comment=column_comment['id'],
                     ),
    em.Column.define(
        'ihm_model_id', em.builtin_types['int4'], comment=column_comment['ihm_model_id'],
    ),
    em.Column.define(
        'label_alt_id',
        em.builtin_types['text'],
        nullok=False,
        comment=column_comment['label_alt_id'],
    ),
    em.Column.define(
        'label_asym_id',
        em.builtin_types['text'],
        nullok=False,
        comment=column_comment['label_asym_id'],
    ),
    em.Column.define(
        'label_atom_id',
        em.builtin_types['text'],
        nullok=False,
        comment=column_comment['label_atom_id'],
    ),
    em.Column.define(
        'label_comp_id',
        em.builtin_types['text'],
        nullok=False,
        comment=column_comment['label_comp_id'],
    ),
    em.Column.define(
        'label_entity_id',
        em.builtin_types['text'],
        nullok=False,
        comment=column_comment['label_entity_id'],
    ),
    em.Column.define(
        'label_seq_id',
        em.builtin_types['int4'],
        nullok=False,
        comment=column_comment['label_seq_id'],
    ),
    em.Column.define(
        'occupancy', em.builtin_types['float4'], comment=column_comment['occupancy'],
    ),
    em.Column.define(
        'pdbx_PDB_model_num',
        em.builtin_types['int4'],
        comment=column_comment['pdbx_PDB_model_num'],
    ),
    em.Column.define(
        'pdbx_auth_asym_id',
        em.builtin_types['text'],
        comment=column_comment['pdbx_auth_asym_id'],
    ),
    em.Column.define(
        'pdbx_auth_atom_name',
        em.builtin_types['text'],
        comment=column_comment['pdbx_auth_atom_name'],
    ),
    em.Column.define(
        'pdbx_auth_comp_id',
        em.builtin_types['text'],
        comment=column_comment['pdbx_auth_comp_id'],
    ),
    em.Column.define(
        'pdbx_auth_seq_id', em.builtin_types['text'], comment=column_comment['pdbx_auth_seq_id'],
    ),
    em.Column.define(
        'pdbx_formal_charge',
        em.builtin_types['int4'],
        comment=column_comment['pdbx_formal_charge'],
    ),
    em.Column.define(
        'pdbx_label_seq_num',
        em.builtin_types['text'],
        comment=column_comment['pdbx_label_seq_num'],
    ),
    em.Column.define(
        'type_symbol',
        em.builtin_types['text'],
        nullok=False,
        comment=column_comment['type_symbol'],
    ),
    em.Column.define('Owner', em.builtin_types['text'], comment=column_comment['Owner'],
                     ),
]

visible_columns = {
    '*': [
        'RID',
        {
            'source': [{
                'outbound': ['PDB', 'atom_site_structure_id_fkey']
            }, 'RID'],
            'comment': 'type:text\nThe value of _entry.id identifies the data block.\n\n Note that this item need not be a number; it can be any unique\n identifier.',
            'markdown_name': 'structure id'
        }, 'B_iso_or_equiv', 'Cartn_x', 'Cartn_y', 'Cartn_z', 'auth_asym_id', 'auth_atom_id',
        'auth_comp_id', 'auth_seq_id', ['PDB', 'atom_site_group_PDB_term_fkey'], 'id',
        {
            'source': [{
                'outbound': ['PDB', 'atom_site_ihm_model_id_fkey']
            }, 'RID'],
            'comment': 'type:int4\nA unique identifier for the structural model being deposited.',
            'markdown_name': 'ihm model id'
        }, 'label_alt_id',
        {
            'source': [{
                'outbound': ['PDB', 'atom_site_label_asym_id_fkey']
            }, 'RID'],
            'comment': 'type:text\nThe value of _struct_asym.id must uniquely identify a record in\n the STRUCT_ASYM list.\n\n Note that this item need not be a number; it can be any unique\n identifier.',
            'markdown_name': 'label asym id'
        }, 'label_atom_id',
        {
            'source': [{
                'outbound': ['PDB', 'atom_site_label_comp_id_fkey']
            }, 'RID'],
            'comment': 'type:text\nThe value of _chem_comp.id must uniquely identify each item in\n the CHEM_COMP list.\n\n For protein polymer entities, this is the three-letter code for\n the amino acid.\n\n For nucleic acid polymer entities, this is the one-letter code\n for the base.',
            'markdown_name': 'label comp id'
        },
        {
            'source': [{
                'outbound': ['PDB', 'atom_site_label_entity_id_fkey']
            }, 'RID'],
            'comment': 'type:text\nThe value of _entity.id must uniquely identify a record in the\n ENTITY list.\n\n Note that this item need not be a number; it can be any unique\n identifier.',
            'markdown_name': 'label entity id'
        }, 'label_seq_id', 'occupancy',
        {
            'source': [{
                'outbound': ['PDB', 'atom_site_pdbx_PDB_model_num_fkey']
            }, 'RID'],
            'comment': 'type:int4\nA unique identifier for the structural model being deposited.',
            'markdown_name': 'pdbx PDB model num'
        }, 'pdbx_auth_asym_id', 'pdbx_auth_atom_name', 'pdbx_auth_comp_id', 'pdbx_auth_seq_id',
        'pdbx_formal_charge', 'pdbx_label_seq_num',
        {
            'source': [{
                'outbound': ['PDB', 'atom_site_type_symbol_fkey']
            }, 'RID'],
            'comment': 'type:text\nThe code used to identify the atom species (singular or plural)\n representing this atom type. Normally this code is the element\n symbol. The code may be composed of any character except\n an underscore with the additional proviso that digits designate\n an oxidation state and must be followed by a + or - character.',
            'markdown_name': 'type symbol'
        }, ['PDB', 'atom_site_RCB_fkey'], ['PDB', 'atom_site_RMB_fkey'], 'RCT', 'RMT',
        ['PDB', 'atom_site_Owner_fkey']
    ],
    'entry': [
        {
            'source': [{
                'outbound': ['PDB', 'atom_site_structure_id_fkey']
            }, 'RID'],
            'comment': 'type:text\nThe value of _entry.id identifies the data block.\n\n Note that this item need not be a number; it can be any unique\n identifier.',
            'markdown_name': 'structure id'
        }, 'B_iso_or_equiv', 'Cartn_x', 'Cartn_y', 'Cartn_z', 'auth_asym_id', 'auth_atom_id',
        'auth_comp_id', 'auth_seq_id', ['PDB', 'atom_site_group_PDB_term_fkey'], 'id',
        {
            'source': [{
                'outbound': ['PDB', 'atom_site_ihm_model_id_fkey']
            }, 'RID'],
            'comment': 'type:int4\nA unique identifier for the structural model being deposited.',
            'markdown_name': 'ihm model id'
        }, 'label_alt_id',
        {
            'source': [{
                'outbound': ['PDB', 'atom_site_label_asym_id_fkey']
            }, 'RID'],
            'comment': 'type:text\nThe value of _struct_asym.id must uniquely identify a record in\n the STRUCT_ASYM list.\n\n Note that this item need not be a number; it can be any unique\n identifier.',
            'markdown_name': 'label asym id'
        }, 'label_atom_id',
        {
            'source': [{
                'outbound': ['PDB', 'atom_site_label_comp_id_fkey']
            }, 'RID'],
            'comment': 'type:text\nThe value of _chem_comp.id must uniquely identify each item in\n the CHEM_COMP list.\n\n For protein polymer entities, this is the three-letter code for\n the amino acid.\n\n For nucleic acid polymer entities, this is the one-letter code\n for the base.',
            'markdown_name': 'label comp id'
        },
        {
            'source': [{
                'outbound': ['PDB', 'atom_site_label_entity_id_fkey']
            }, 'RID'],
            'comment': 'type:text\nThe value of _entity.id must uniquely identify a record in the\n ENTITY list.\n\n Note that this item need not be a number; it can be any unique\n identifier.',
            'markdown_name': 'label entity id'
        }, 'label_seq_id', 'occupancy',
        {
            'source': [{
                'outbound': ['PDB', 'atom_site_pdbx_PDB_model_num_fkey']
            }, 'RID'],
            'comment': 'type:int4\nA unique identifier for the structural model being deposited.',
            'markdown_name': 'pdbx PDB model num'
        }, 'pdbx_auth_asym_id', 'pdbx_auth_atom_name', 'pdbx_auth_comp_id', 'pdbx_auth_seq_id',
        'pdbx_formal_charge', 'pdbx_label_seq_num',
        {
            'source': [{
                'outbound': ['PDB', 'atom_site_type_symbol_fkey']
            }, 'RID'],
            'comment': 'type:text\nThe code used to identify the atom species (singular or plural)\n representing this atom type. Normally this code is the element\n symbol. The code may be composed of any character except\n an underscore with the additional proviso that digits designate\n an oxidation state and must be followed by a + or - character.',
            'markdown_name': 'type symbol'
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
    em.Key.define(['structure_id', 'id'], constraint_names=[('PDB', 'atom_site_primary_key')],
                  ),
    em.Key.define(['RID'], constraint_names=[('PDB', 'atom_site_RIDkey1')],
                  ),
]

fkey_defs = [
    em.ForeignKey.define(
        ['group_PDB'],
        'Vocab',
        'atom_site_group_PDB_term', ['ID'],
        constraint_names=[('PDB', 'atom_site_group_PDB_term_fkey')],
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
        constraint_names=[('PDB', 'atom_site_Owner_fkey')],
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
        constraint_names=[('PDB', 'atom_site_RCB_fkey')],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
    ),
    em.ForeignKey.define(
        ['RMB'],
        'public',
        'ERMrest_Client', ['ID'],
        constraint_names=[('PDB', 'atom_site_RMB_fkey')],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
    ),
    em.ForeignKey.define(
        ['structure_id'],
        'PDB',
        'entry', ['id'],
        constraint_names=[('PDB', 'atom_site_structure_id_fkey')],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
        on_update='CASCADE',
        on_delete='SET NULL',
    ),
    em.ForeignKey.define(
        ['structure_id', 'ihm_model_id'],
        'PDB',
        'ihm_model_list', ['structure_id', 'model_id'],
        constraint_names=[('PDB', 'atom_site_ihm_model_id_fkey')],
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
        ['structure_id', 'label_asym_id'],
        'PDB',
        'struct_asym', ['structure_id', 'id'],
        constraint_names=[('PDB', 'atom_site_label_asym_id_fkey')],
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
        ['structure_id', 'label_comp_id'],
        'PDB',
        'chem_comp', ['structure_id', 'id'],
        constraint_names=[('PDB', 'atom_site_label_comp_id_fkey')],
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
        ['structure_id', 'label_entity_id'],
        'PDB',
        'entity', ['structure_id', 'id'],
        constraint_names=[('PDB', 'atom_site_label_entity_id_fkey')],
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
        ['structure_id', 'pdbx_PDB_model_num'],
        'PDB',
        'ihm_model_list', ['structure_id', 'model_id'],
        constraint_names=[('PDB', 'atom_site_pdbx_PDB_model_num_fkey')],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
        on_update='CASCADE',
        on_delete='SET NULL',
    ),
    em.ForeignKey.define(
        ['structure_id', 'type_symbol'],
        'PDB',
        'atom_type', ['structure_id', 'symbol'],
        constraint_names=[('PDB', 'atom_site_type_symbol_fkey')],
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

