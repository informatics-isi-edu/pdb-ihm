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

Validation_File_Type_rows =[
        {'Name': 'validation_diag_log', 'Description': 'Validation log file with mmCIF diagnostic errors'},
        {'Name': 'validation_parser_log', 'Description': 'Validation log file with mmCIF parser errors'},
        {'Name': 'mmCIF', 'Description': 'mmCIF file generated based on the data in the database prior to the validation'}
    ]


def main(server_name, catalog_id, credentials):
    server = DerivaServer('https', server_name, credentials)
    catalog = server.connect_ermrest(catalog_id)
    catalog.dcctx['cid'] = "oneoff/model"
    model = catalog.getCatalogModel()
    
    """
    Create the new vocabulary tables
    """
    utils.create_table_if_not_exist(model, 'Vocab', utils.define_Vocab_table('Validation_File_Type', 'Validation for the generated mmCIF file'))

    """
    Check if the new values already exist
    """
    predicate = []
    for row in Validation_File_Type_rows:
        predicate.append('Name={}'.format(row['Name']))
    url = '/entity/Vocab:Validation_File_Type/{}'.format(';'.join(predicate))
    resp = catalog.get(
        url
    )
    resp.raise_for_status()
    deleted_rows = resp.json()
    if len(deleted_rows) > 0:
        """
        Delete the new values
        """
        url = '/entity/Vocab:Validation_File_Type/{}'.format(';'.join(predicate))
        resp = catalog.delete(
            url
        )
        resp.raise_for_status()
        deleted_values = []
        
        for row in deleted_rows:
            deleted_values.append(row['Name'])
            
        print('Deleted values from the Vocab.Validation_File_Type table: "{}"'.format(', '.join(deleted_values)))

    """
    Load data into the new vocabulary tables
    """
    utils.add_rows_to_vocab_table(catalog, 'Validation_File_Type', Validation_File_Type_rows)

    """
    Create the acls bindings
    """
    utils.set_table_acl_bindings(catalog, 'Vocab', 'Validation_File_Type', acl_bindings)

if __name__ == '__main__':
    args = BaseCLI("ad-hoc table creation tool", None, 1).parse_cli()
    credentials = get_credential(args.host, args.credential_file)

    main(args.host, 1, credentials)
    
