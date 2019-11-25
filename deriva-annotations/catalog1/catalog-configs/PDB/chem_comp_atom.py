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

table_name = 'chem_comp_atom'

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
    'alt_atom_id': {},
    'atom_id': {},
    'charge': {},
    'comp_id': {},
    'model_Cartn_x': {},
    'model_Cartn_x_esd': {},
    'model_Cartn_y': {},
    'model_Cartn_y_esd': {},
    'model_Cartn_z': {},
    'model_Cartn_z_esd': {},
    'partial_charge': {},
    'pdbx_align': {},
    'pdbx_alt_atom_id': {},
    'pdbx_alt_comp_id': {},
    'pdbx_aromatic_flag': {},
    'pdbx_component_atom_id': {},
    'pdbx_component_comp_id': {},
    'pdbx_component_entity_id': {},
    'pdbx_component_id': {},
    'pdbx_leaving_atom_flag': {},
    'pdbx_model_Cartn_x_ideal': {},
    'pdbx_model_Cartn_y_ideal': {},
    'pdbx_model_Cartn_z_ideal': {},
    'pdbx_ordinal': {},
    'pdbx_polymer_type': {},
    'pdbx_ref_id': {},
    'pdbx_residue_numbering': {},
    'pdbx_stereo_config': {},
    'pdbx_stnd_atom_id': {},
    'substruct_code': {},
    'type_symbol': {},
    'Owner': {}
}

column_comment = {
    'structure_id': 'A reference to table entry.id.',
    'alt_atom_id': 'type:text\nAn alternative identifier for the atom. This data item would be\n used in cases where alternative nomenclatures exist for labelling\n atoms in a group.',
    'atom_id': 'type:text\nThe value of _chem_comp_atom.atom_id must uniquely identify\n each atom in each monomer in the CHEM_COMP_ATOM list.\n\n The atom identifiers need not be unique over all atoms in the\n data block; they need only be unique for each atom in a\n component.\n\n Note that this item need not be a number; it can be any unique\n identifier.',
    'charge': 'type:int4\nThe net integer charge assigned to this atom. This is the\n formal charge assignment normally found in chemical diagrams.\nexamples:1,-1',
    'comp_id': 'A reference to table chem_comp.id.',
    'model_Cartn_x': 'type:float4\nThe x component of the coordinates for this atom in this\n component specified as orthogonal angstroms. The choice of\n reference axis frame for the coordinates is arbitrary.\n\n The set of coordinates input for the entity here is intended to\n correspond to the atomic model used to generate restraints for\n structure refinement, not to atom sites in the ATOM_SITE\n list.',
    'model_Cartn_x_esd': 'type:float4\nThe standard uncertainty (estimated standard deviation)\n of _chem_comp_atom.model_Cartn_x.',
    'model_Cartn_y': 'type:float4\nThe y component of the coordinates for this atom in this\n component specified as orthogonal angstroms. The choice of\n reference axis frame for the coordinates is arbitrary.\n\n The set of coordinates input for the entity here is intended to\n correspond to the atomic model used to generate restraints for\n structure refinement, not to atom sites in the ATOM_SITE\n list.',
    'model_Cartn_y_esd': 'type:float4\nThe standard uncertainty (estimated standard deviation)\n of _chem_comp_atom.model_Cartn_y.',
    'model_Cartn_z': 'type:float4\nThe z component of the coordinates for this atom in this\n component specified as orthogonal angstroms. The choice of\n reference axis frame for the coordinates is arbitrary.\n\n The set of coordinates input for the entity here is intended to\n correspond to the atomic model used to generate restraints for\n structure refinement, not to atom sites in the ATOM_SITE\n list.',
    'model_Cartn_z_esd': 'type:float4\nThe standard uncertainty (estimated standard deviation)\n of _chem_comp_atom.model_Cartn_z.',
    'partial_charge': 'type:float4\nThe partial charge assigned to this atom.',
    'pdbx_align': 'type:int4\nAtom name alignment offset in PDB atom field.',
    'pdbx_alt_atom_id': 'type:text\nAn alternative identifier for the atom. This data item would be\n used in cases where alternative nomenclatures exist for labelling\n atoms in a group.',
    'pdbx_alt_comp_id': 'type:text\nAn alternative identifier for the atom. This data item would be\n used in cases where alternative nomenclatures exist for labelling\n atoms in a group.',
    'pdbx_aromatic_flag': 'type:text\nA flag indicating an aromatic atom.',
    'pdbx_component_atom_id': 'type:text\nThe atom identifier in the subcomponent where a  \n larger component has been divided subcomponents.\nexamples:CB,CA,CG',
    'pdbx_component_comp_id': 'type:text\nThe component identifier for the subcomponent where a  \n larger component has been divided subcomponents.\nexamples:HIS,PRO',
    'pdbx_component_entity_id': 'type:int4\nA reference to entity identifier in data  category \n pdbx_chem_comp_subcomponent_entity_list.',
    'pdbx_component_id': 'type:int4\nA reference to _pdbx_reference_entity_list.component_id',
    'pdbx_leaving_atom_flag': 'type:text\nA flag indicating a leaving atom.',
    'pdbx_model_Cartn_x_ideal': 'type:float4\nAn alternative x component of the coordinates for this atom in this\n component specified as orthogonal angstroms.',
    'pdbx_model_Cartn_y_ideal': 'type:float4\nAn alternative y component of the coordinates for this atom in this\n component specified as orthogonal angstroms.',
    'pdbx_model_Cartn_z_ideal': 'type:float4\nAn alternative z component of the coordinates for this atom in this\n component specified as orthogonal angstroms.',
    'pdbx_ordinal': 'type:int4\nOrdinal index for the component atom list.',
    'pdbx_polymer_type': 'type:text\nIs the atom in a polymer or non-polymer subcomponent in the BIRD definition.',
    'pdbx_ref_id': 'type:text\nA reference to _pdbx_reference_entity_list.ref_entity_id',
    'pdbx_residue_numbering': 'type:int4\nPreferred residue numbering in the BIRD definition.',
    'pdbx_stereo_config': 'type:text\nThe chiral configuration of the atom that is a chiral center.',
    'pdbx_stnd_atom_id': 'type:text\nA standard identifier for the atom. This data item is used when\n IUPAC/IUBMB nomenclature exists for labeling atoms.',
    'substruct_code': 'type:text\nThis data item assigns the atom to a substructure of the\n component, if appropriate.',
    'type_symbol': 'type:text\nThe code used to identify the atom species representing \n this atom type. Normally this code is the element\n symbol.\nexamples:C,N,O',
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
        'alt_atom_id', em.builtin_types['text'], comment=column_comment['alt_atom_id'],
    ),
    em.Column.define(
        'atom_id', em.builtin_types['text'], nullok=False, comment=column_comment['atom_id'],
    ),
    em.Column.define('charge', em.builtin_types['int4'], comment=column_comment['charge'],
                     ),
    em.Column.define(
        'comp_id', em.builtin_types['text'], nullok=False, comment=column_comment['comp_id'],
    ),
    em.Column.define(
        'model_Cartn_x', em.builtin_types['float4'], comment=column_comment['model_Cartn_x'],
    ),
    em.Column.define(
        'model_Cartn_x_esd',
        em.builtin_types['float4'],
        comment=column_comment['model_Cartn_x_esd'],
    ),
    em.Column.define(
        'model_Cartn_y', em.builtin_types['float4'], comment=column_comment['model_Cartn_y'],
    ),
    em.Column.define(
        'model_Cartn_y_esd',
        em.builtin_types['float4'],
        comment=column_comment['model_Cartn_y_esd'],
    ),
    em.Column.define(
        'model_Cartn_z', em.builtin_types['float4'], comment=column_comment['model_Cartn_z'],
    ),
    em.Column.define(
        'model_Cartn_z_esd',
        em.builtin_types['float4'],
        comment=column_comment['model_Cartn_z_esd'],
    ),
    em.Column.define(
        'partial_charge', em.builtin_types['float4'], comment=column_comment['partial_charge'],
    ),
    em.Column.define(
        'pdbx_align', em.builtin_types['int4'], comment=column_comment['pdbx_align'],
    ),
    em.Column.define(
        'pdbx_alt_atom_id', em.builtin_types['text'], comment=column_comment['pdbx_alt_atom_id'],
    ),
    em.Column.define(
        'pdbx_alt_comp_id', em.builtin_types['text'], comment=column_comment['pdbx_alt_comp_id'],
    ),
    em.Column.define(
        'pdbx_aromatic_flag',
        em.builtin_types['text'],
        comment=column_comment['pdbx_aromatic_flag'],
    ),
    em.Column.define(
        'pdbx_component_atom_id',
        em.builtin_types['text'],
        comment=column_comment['pdbx_component_atom_id'],
    ),
    em.Column.define(
        'pdbx_component_comp_id',
        em.builtin_types['text'],
        comment=column_comment['pdbx_component_comp_id'],
    ),
    em.Column.define(
        'pdbx_component_entity_id',
        em.builtin_types['int4'],
        comment=column_comment['pdbx_component_entity_id'],
    ),
    em.Column.define(
        'pdbx_component_id',
        em.builtin_types['int4'],
        comment=column_comment['pdbx_component_id'],
    ),
    em.Column.define(
        'pdbx_leaving_atom_flag',
        em.builtin_types['text'],
        comment=column_comment['pdbx_leaving_atom_flag'],
    ),
    em.Column.define(
        'pdbx_model_Cartn_x_ideal',
        em.builtin_types['float4'],
        comment=column_comment['pdbx_model_Cartn_x_ideal'],
    ),
    em.Column.define(
        'pdbx_model_Cartn_y_ideal',
        em.builtin_types['float4'],
        comment=column_comment['pdbx_model_Cartn_y_ideal'],
    ),
    em.Column.define(
        'pdbx_model_Cartn_z_ideal',
        em.builtin_types['float4'],
        comment=column_comment['pdbx_model_Cartn_z_ideal'],
    ),
    em.Column.define(
        'pdbx_ordinal', em.builtin_types['int4'], comment=column_comment['pdbx_ordinal'],
    ),
    em.Column.define(
        'pdbx_polymer_type',
        em.builtin_types['text'],
        comment=column_comment['pdbx_polymer_type'],
    ),
    em.Column.define(
        'pdbx_ref_id', em.builtin_types['text'], comment=column_comment['pdbx_ref_id'],
    ),
    em.Column.define(
        'pdbx_residue_numbering',
        em.builtin_types['int4'],
        comment=column_comment['pdbx_residue_numbering'],
    ),
    em.Column.define(
        'pdbx_stereo_config',
        em.builtin_types['text'],
        comment=column_comment['pdbx_stereo_config'],
    ),
    em.Column.define(
        'pdbx_stnd_atom_id',
        em.builtin_types['text'],
        comment=column_comment['pdbx_stnd_atom_id'],
    ),
    em.Column.define(
        'substruct_code', em.builtin_types['text'], comment=column_comment['substruct_code'],
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
        'RID', {
            'source': [{
                'outbound': ['PDB', 'chem_comp_atom_structure_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table entry.id.',
            'markdown_name': 'structure id'
        }, 'alt_atom_id', 'atom_id', 'charge', {
            'source': [{
                'outbound': ['PDB', 'chem_comp_atom_comp_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table chem_comp.id.',
            'markdown_name': 'comp id'
        }, 'model_Cartn_x', 'model_Cartn_x_esd', 'model_Cartn_y', 'model_Cartn_y_esd',
        'model_Cartn_z', 'model_Cartn_z_esd', 'partial_charge', 'pdbx_align',
        'pdbx_alt_atom_id', 'pdbx_alt_comp_id',
        ['PDB', 'chem_comp_atom_pdbx_aromatic_flag_term_fkey'], 'pdbx_component_atom_id',
        'pdbx_component_comp_id', 'pdbx_component_entity_id', 'pdbx_component_id',
        ['PDB', 'chem_comp_atom_pdbx_leaving_atom_flag_term_fkey'], 'pdbx_model_Cartn_x_ideal',
        'pdbx_model_Cartn_y_ideal', 'pdbx_model_Cartn_z_ideal', 'pdbx_ordinal',
        ['PDB',
         'chem_comp_atom_pdbx_polymer_type_term_fkey'], 'pdbx_ref_id', 'pdbx_residue_numbering',
        ['PDB', 'chem_comp_atom_pdbx_stereo_config_term_fkey'], 'pdbx_stnd_atom_id',
        ['PDB', 'chem_comp_atom_substruct_code_term_fkey'], 'type_symbol',
        ['PDB', 'chem_comp_atom_RCB_fkey'], ['PDB', 'chem_comp_atom_RMB_fkey'], 'RCT', 'RMT',
        ['PDB', 'chem_comp_atom_Owner_fkey']
    ],
    'entry': [
        {
            'source': [{
                'outbound': ['PDB', 'chem_comp_atom_structure_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table entry.id.',
            'markdown_name': 'structure id'
        }, 'alt_atom_id', 'atom_id', 'charge', {
            'source': [{
                'outbound': ['PDB', 'chem_comp_atom_comp_id_fkey']
            }, 'RID'],
            'comment': 'A reference to table chem_comp.id.',
            'markdown_name': 'comp id'
        }, 'model_Cartn_x', 'model_Cartn_x_esd', 'model_Cartn_y', 'model_Cartn_y_esd',
        'model_Cartn_z', 'model_Cartn_z_esd', 'partial_charge', 'pdbx_align',
        'pdbx_alt_atom_id', 'pdbx_alt_comp_id',
        ['PDB', 'chem_comp_atom_pdbx_aromatic_flag_term_fkey'], 'pdbx_component_atom_id',
        'pdbx_component_comp_id', 'pdbx_component_entity_id', 'pdbx_component_id',
        ['PDB', 'chem_comp_atom_pdbx_leaving_atom_flag_term_fkey'], 'pdbx_model_Cartn_x_ideal',
        'pdbx_model_Cartn_y_ideal', 'pdbx_model_Cartn_z_ideal', 'pdbx_ordinal',
        ['PDB',
         'chem_comp_atom_pdbx_polymer_type_term_fkey'], 'pdbx_ref_id', 'pdbx_residue_numbering',
        ['PDB', 'chem_comp_atom_pdbx_stereo_config_term_fkey'], 'pdbx_stnd_atom_id',
        ['PDB', 'chem_comp_atom_substruct_code_term_fkey'], 'type_symbol'
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
    em.Key.define(['RID'], constraint_names=[('PDB', 'chem_comp_atom_RIDkey1')],
                  ),
    em.Key.define(
        ['structure_id', 'atom_id', 'comp_id'],
        constraint_names=[('PDB', 'chem_comp_atom_primary_key')],
    ),
]

fkey_defs = [
    em.ForeignKey.define(
        ['pdbx_aromatic_flag'],
        'Vocab',
        'chem_comp_atom_pdbx_aromatic_flag_term', ['ID'],
        constraint_names=[('PDB', 'chem_comp_atom_pdbx_aromatic_flag_term_fkey')],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
        on_update='CASCADE',
        on_delete='SET NULL',
    ),
    em.ForeignKey.define(
        ['pdbx_leaving_atom_flag'],
        'Vocab',
        'chem_comp_atom_pdbx_leaving_atom_flag_term', ['ID'],
        constraint_names=[('PDB', 'chem_comp_atom_pdbx_leaving_atom_flag_term_fkey')],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
        on_update='CASCADE',
        on_delete='SET NULL',
    ),
    em.ForeignKey.define(
        ['pdbx_polymer_type'],
        'Vocab',
        'chem_comp_atom_pdbx_polymer_type_term', ['ID'],
        constraint_names=[('PDB', 'chem_comp_atom_pdbx_polymer_type_term_fkey')],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
        on_update='CASCADE',
        on_delete='SET NULL',
    ),
    em.ForeignKey.define(
        ['pdbx_stereo_config'],
        'Vocab',
        'chem_comp_atom_pdbx_stereo_config_term', ['ID'],
        constraint_names=[('PDB', 'chem_comp_atom_pdbx_stereo_config_term_fkey')],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
        on_update='CASCADE',
        on_delete='SET NULL',
    ),
    em.ForeignKey.define(
        ['substruct_code'],
        'Vocab',
        'chem_comp_atom_substruct_code_term', ['ID'],
        constraint_names=[('PDB', 'chem_comp_atom_substruct_code_term_fkey')],
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
        constraint_names=[('PDB', 'chem_comp_atom_Owner_fkey')],
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
        constraint_names=[('PDB', 'chem_comp_atom_RCB_fkey')],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
    ),
    em.ForeignKey.define(
        ['RMB'],
        'public',
        'ERMrest_Client', ['ID'],
        constraint_names=[('PDB', 'chem_comp_atom_RMB_fkey')],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
    ),
    em.ForeignKey.define(
        ['structure_id'],
        'PDB',
        'entry', ['id'],
        constraint_names=[('PDB', 'chem_comp_atom_structure_id_fkey')],
        acls={
            'insert': ['*'],
            'update': ['*']
        },
        on_update='CASCADE',
        on_delete='SET NULL',
    ),
    em.ForeignKey.define(
        ['structure_id', 'comp_id'],
        'PDB',
        'chem_comp', ['structure_id', 'id'],
        constraint_names=[('PDB', 'chem_comp_atom_comp_id_fkey')],
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
    table_def['column_annotations'] = column_annotations
    table_def['column_comment'] = column_comment
    updater.update_table(mode, schema_name, table_def, replace=replace, really=really)


if __name__ == "__main__":
    host = 'pdb.isrd.isi.edu'
    catalog_id = 1
    mode, replace, host, catalog_id = parse_args(host, catalog_id, is_table=True)
    catalog = DerivaCatalog(host, catalog_id=catalog_id, validate=False)
    main(catalog, mode, replace)
