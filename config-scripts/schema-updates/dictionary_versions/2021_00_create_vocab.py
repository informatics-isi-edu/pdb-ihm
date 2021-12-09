import sys
import json
from deriva.core import get_credential, DerivaServer, BaseCLI
from deriva.core.ermrest_model import Key, Column, builtin_types
import utils

# add scripts for updating vocabs that has nothing to do with mmcif model changes.

acl_bindings = {
  "released_reader": {
    "types": [
      "select"
    ],
    "scope_acl": [
      "https://auth.globus.org/99da042e-64a6-11ea-ad5f-0ef992ed7ca1"
    ],
    "projection": [
      "RID"
    ],
    "projection_type": "nonnull"
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
      "*"
    ],
    "projection": [
      "RCB"
    ],
    "projection_type": "acl"
  }
}

Data_Dictionary_Name_rows =[
    {'Name': 'ihm-extension.dic', 'Description': 'The IHM-dictionary is the mmCIF extension for representing integrative/hybrid structures.'},
    {'Name': 'mmcif_pdbx.dic', 'Description': 'The PDBx/mmCIF dictionary provides the data standards for the PDB for archiving structures of macromolecules and their complexes.'},
    {'Name': 'flr-extension.dic', 'Description': 'The FLR-dictionary is the mmCIF extension for representing Fluorescence / FRET experiments.'}
]

Data_Dictionary_Category_rows =[
    {'Name': 'IHM-dictionary', 'Description': 'The IHM-dictionary is the mmCIF extension for representing integrative/hybrid structures.'},
    {'Name': 'PDBx/mmCIF', 'Description': 'The PDBx/mmCIF dictionary provides the data standards for the PDB for archiving structures of macromolecules and their complexes.'},
    {'Name': 'FLR-dictionary', 'Description': 'The FLR-dictionary is the mmCIF extension for representing Fluorescence / FRET experiments.'}
]

def main(server_name, catalog_id, credentials):
    server = DerivaServer('https', server_name, credentials)
    catalog = server.connect_ermrest(catalog_id)
    catalog.dcctx['cid'] = "oneoff/model"
    model = catalog.getCatalogModel()
    
    """
    Create the new vocabulary tables
    """
    utils.create_table_if_not_exist(model, 'Vocab', utils.define_Vocab_table('Data_Dictionary_Name', 'Dictionary names'))
    utils.create_table_if_not_exist(model, 'Vocab', utils.define_Vocab_table('Data_Dictionary_Category', 'Dictionary categories'))

    """
    Load data into the new vocabulary tables
    """
    utils.add_rows_to_vocab_table(catalog, 'Data_Dictionary_Name', Data_Dictionary_Name_rows)
    utils.add_rows_to_vocab_table(catalog, 'Data_Dictionary_Category', Data_Dictionary_Category_rows)
    """
    Create the acls bindings
    """
    utils.set_table_acl_bindings(catalog, 'Vocab', 'Data_Dictionary_Name', acl_bindings)
    utils.set_table_acl_bindings(catalog, 'Vocab', 'Data_Dictionary_Category', acl_bindings)

if __name__ == '__main__':
    args = BaseCLI("ad-hoc table creation tool", None, 1).parse_cli()
    credentials = get_credential(args.host, args.credential_file)

    main(args.host, 1, credentials)
    
