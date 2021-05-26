import sys
import json
from ast import literal_eval
from deriva.core import ErmrestCatalog, AttrDict, get_credential, DEFAULT_CREDENTIAL_FILE, tag, urlquote, DerivaServer, get_credential, BaseCLI
from deriva.core.ermrest_model import builtin_types, Schema, Table, Column, Key, ForeignKey, DomainType, ArrayType
import utils

table_acls = {
  "owner": [
    "https://auth.globus.org/0b98092c-3c41-11e9-a8c8-0ee7d80087ee",
    "https://auth.globus.org/176baec4-ed26-11e5-8e88-22000ab4b42b"
  ],
  "write": [],
  "delete": [
    "https://auth.globus.org/eef3e02a-3c40-11e9-9276-0edc9bdd56a6"
  ],
  "insert": [
    "https://auth.globus.org/eef3e02a-3c40-11e9-9276-0edc9bdd56a6",
    "https://auth.globus.org/c94a1e5c-3c40-11e9-a5d1-0aacc65bfe9a",
    "https://auth.globus.org/99da042e-64a6-11ea-ad5f-0ef992ed7ca1"
  ],
  "select": [
    "https://auth.globus.org/c94a1e5c-3c40-11e9-a5d1-0aacc65bfe9a",
    "https://auth.globus.org/8875a770-3c40-11e9-a8c8-0ee7d80087ee"
  ],
  "update": [
    "https://auth.globus.org/eef3e02a-3c40-11e9-9276-0edc9bdd56a6"
  ],
  "enumerate": [
    "*"
  ]
}

foreign_key_acls = {
    "insert": [
      "*"
    ],
    "update": [
      "*"
    ]
}

table_acl_bindings_pattern = """
{
  "released_reader": {
    "types": [
      "select"
    ],
    "scope_acl": [
      "https://auth.globus.org/99da042e-64a6-11ea-ad5f-0ef992ed7ca1"
    ],
    "projection": [
      {
        "outbound": [
          "PDB",
          "fkey_constraint_name"
        ]
      },
      "RCB"
    ],
    "projection_type": "acl"
  },
  "self_service_group": {
    "types": [
      "update",
      "delete"
    ],
    "scope_acl": [
      "*"
    ],
    "projection": [
      "Owner"
    ],
    "projection_type": "acl"
  },
  "self_service_creator": {
    "types": [
      "update",
      "delete"
    ],
    "scope_acl": [
      "https://auth.globus.org/99da042e-64a6-11ea-ad5f-0ef992ed7ca1"
    ],
    "projection": [
      {
        "outbound": [
          "PDB",
          "fkey_constraint_name"
        ]
      },
      {
        "or": [
          {
            "filter": "Workflow_Status",
            "operand": "DRAFT",
            "operator": "="
          },
          {
            "filter": "Workflow_Status",
            "operand": "DEPO",
            "operator": "="
          },
          {
            "filter": "Workflow_Status",
            "operand": "RECORD READY",
            "operator": "="
          },
          {
            "filter": "Workflow_Status",
            "operand": "ERROR",
            "operator": "="
          }
        ]
      },
      "RCB"
    ],
    "projection_type": "acl"
  }
}
"""

"""
ACL needs to be added for new tables as follows:

ihm_pseudo_site: ACL should mimic ihm_cross_link_restraint
ihm_cross_link_pseudo_site: ACL should mimic ihm_cross_link_restraint
ihm_ensemble_sub_sample: ACL should mimic ihm_ensemble_info
ihm_data_transformation: ACL should mimic ihm_related_datasets
ihm_hdx_restraint: ACL should mimic ihm_hydroxyl_radical_fp_restraint
ihm_derived_angle_restraint: ACL should mimic ihm_derived_distance_restraint
ihm_derived_dihedral_restraint: ACL should mimic ihm_derived_distance_restraint
struct_ref: ACL should mimic entity
struct_ref_seq: ACL should mimic entity
struct_ref_seq_dif: ACL should mimic entity
"""

def main(server_name, catalog_id, credentials):
    server = DerivaServer('https', server_name, credentials)
    catalog = server.connect_ermrest(catalog_id)
    catalog.dcctx['cid'] = "oneoff/model"

    """
    set the table acls
    """
    utils.set_table_acls(catalog, 'PDB', 'ihm_pseudo_site', table_acls)
    utils.set_table_acls(catalog, 'PDB', 'ihm_cross_link_pseudo_site', table_acls)
    utils.set_table_acls(catalog, 'PDB', 'ihm_ensemble_sub_sample', table_acls)
    utils.set_table_acls(catalog, 'PDB', 'ihm_data_transformation', table_acls)
    utils.set_table_acls(catalog, 'PDB', 'ihm_derived_angle_restraint', table_acls)
    utils.set_table_acls(catalog, 'PDB', 'ihm_hdx_restraint', table_acls)
    utils.set_table_acls(catalog, 'PDB', 'ihm_derived_dihedral_restraint', table_acls)
    utils.set_table_acls(catalog, 'PDB', 'struct_ref', table_acls)
    utils.set_table_acls(catalog, 'PDB', 'struct_ref_seq', table_acls)
    utils.set_table_acls(catalog, 'PDB', 'struct_ref_seq_dif', table_acls)

    """
    set the table acl_bindings
    """
    utils.set_table_acl_bindings(catalog, 'PDB', 'ihm_pseudo_site', literal_eval(table_acl_bindings_pattern.replace('fkey_constraint_name', 'ihm_pseudo_site_structure_id_fkey')))
    utils.set_table_acl_bindings(catalog, 'PDB', 'ihm_cross_link_pseudo_site', literal_eval(table_acl_bindings_pattern.replace('fkey_constraint_name', 'ihm_cross_link_pseudo_site_structure_id_fkey')))
    utils.set_table_acl_bindings(catalog, 'PDB', 'ihm_ensemble_sub_sample', literal_eval(table_acl_bindings_pattern.replace('fkey_constraint_name', 'ihm_ensemble_sub_sample_structure_id_fkey')))
    utils.set_table_acl_bindings(catalog, 'PDB', 'ihm_data_transformation', literal_eval(table_acl_bindings_pattern.replace('fkey_constraint_name', 'ihm_data_transformation_structure_id_fkey')))
    utils.set_table_acl_bindings(catalog, 'PDB', 'ihm_hdx_restraint', literal_eval(table_acl_bindings_pattern.replace('fkey_constraint_name', 'ihm_hdx_restraint_structure_id_fkey')))
    utils.set_table_acl_bindings(catalog, 'PDB', 'ihm_derived_angle_restraint', literal_eval(table_acl_bindings_pattern.replace('fkey_constraint_name', 'ihm_derived_angle_restraint_structure_id_fkey')))
    utils.set_table_acl_bindings(catalog, 'PDB', 'ihm_derived_dihedral_restraint', literal_eval(table_acl_bindings_pattern.replace('fkey_constraint_name', 'ihm_derived_dihedral_restraint_structure_id_fkey')))
    utils.set_table_acl_bindings(catalog, 'PDB', 'struct_ref', literal_eval(table_acl_bindings_pattern.replace('fkey_constraint_name', 'struct_ref_structure_id_fkey')))
    utils.set_table_acl_bindings(catalog, 'PDB', 'struct_ref_seq', literal_eval(table_acl_bindings_pattern.replace('fkey_constraint_name', 'struct_ref_seq_structure_id_fkey')))
    utils.set_table_acl_bindings(catalog, 'PDB', 'struct_ref_seq_dif', literal_eval(table_acl_bindings_pattern.replace('fkey_constraint_name', 'struct_ref_seq_dif_structure_id_fkey')))

    """
    set the foreign key acls
    """
    utils.set_foreign_key_acls(catalog, 'PDB', 'ihm_pseudo_site', 'ihm_pseudo_site_structure_id_fkey', foreign_key_acls)
    utils.set_foreign_key_acls(catalog, 'PDB', 'ihm_cross_link_pseudo_site', 'ihm_cross_link_pseudo_site_structure_id_fkey', foreign_key_acls)
    utils.set_foreign_key_acls(catalog, 'PDB', 'ihm_ensemble_sub_sample', 'ihm_ensemble_sub_sample_structure_id_fkey', foreign_key_acls)
    utils.set_foreign_key_acls(catalog, 'PDB', 'ihm_data_transformation', 'ihm_data_transformation_structure_id_fkey', foreign_key_acls)
    utils.set_foreign_key_acls(catalog, 'PDB', 'ihm_hdx_restraint', 'ihm_hdx_restraint_structure_id_fkey', foreign_key_acls)
    utils.set_foreign_key_acls(catalog, 'PDB', 'ihm_derived_angle_restraint', 'ihm_derived_angle_restraint_structure_id_fkey', foreign_key_acls)
    utils.set_foreign_key_acls(catalog, 'PDB', 'ihm_derived_dihedral_restraint', 'ihm_derived_dihedral_restraint_structure_id_fkey', foreign_key_acls)
    utils.set_foreign_key_acls(catalog, 'PDB', 'struct_ref', 'struct_ref_structure_id_fkey', foreign_key_acls)
    utils.set_foreign_key_acls(catalog, 'PDB', 'struct_ref', 'struct_ref_db_name_fkey', foreign_key_acls)
    utils.set_foreign_key_acls(catalog, 'PDB', 'struct_ref_seq', 'struct_ref_seq_structure_id_fkey', foreign_key_acls)
    utils.set_foreign_key_acls(catalog, 'PDB', 'struct_ref_seq_dif', 'struct_ref_seq_dif_structure_id_fkey', foreign_key_acls)
    utils.set_foreign_key_acls(catalog, 'PDB', 'struct_ref_seq_dif', 'struct_ref_seq_dif_details_fkey', foreign_key_acls)

if __name__ == '__main__':
    args = BaseCLI("ad-hoc table creation tool", None, 1).parse_cli()
    credentials = get_credential(args.host, args.credential_file)

    main(args.host, 99, credentials)
    
