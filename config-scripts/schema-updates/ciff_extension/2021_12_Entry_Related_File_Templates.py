import sys
import json
from deriva.core import ErmrestCatalog, AttrDict, get_credential, DEFAULT_CREDENTIAL_FILE, tag, urlquote, DerivaServer, get_credential, BaseCLI
from deriva.core.ermrest_model import builtin_types, Schema, Table, Column, Key, ForeignKey, DomainType, ArrayType
import utils

# ========================================================
def define_tdoc_Entry_Related_File_Templates():
    table_name='Entry_Related_File_Templates'
    comment='Uploaded Restraint Files Templates'
    table_annotations = {
        'tag:misd.isi.edu,2015:display': {
          'name': 'CSV Templates for Restraint Files'
        },
        'tag:isrd.isi.edu,2016:visible-columns': {
          '*': [
            'RID',
            [
              'PDB',
              'Entry_Template_File_File_Type_fkey'
            ],
            'File_URL',
            'Description'
          ],
          'entry': [
            [
              'PDB',
              'Entry_Template_File_File_Type_fkey'
            ],
            'File_URL',
            'Description'
          ],
          'detailed': [
            'RID',
            [
              'PDB',
              'Entry_Template_File_File_Type_fkey'
            ],
            'File_URL',
            'File_Bytes',
            'File_MD5',
            'Description',
            [
              'PDB',
              'Entry_Template_File_RMB_fkey'
            ],
            'RCT',
            'RMT',
            [
              'PDB',
              'Entry_Template_File_Owner_fkey'
            ]
          ]
        }
      }
    table_acl_bindings = {
    'released_reader': {
      'types': [
        'select'
      ],
      'scope_acl': [
        'https://auth.globus.org/99da042e-64a6-11ea-ad5f-0ef992ed7ca1'
      ],
      'projection': [
        'RID'
      ],
      'projection_type': 'nonnull'
    },
    'self_service_group': {
      'types': [
        'update',
        'delete'
      ],
      'scope_acl': [
        '*'
      ],
      'projection': [
        'Owner'
      ],
      'projection_type': 'acl'
    },
    'self_service_creator': {
      'types': [
        'update',
        'delete'
      ],
      'scope_acl': [
        '*'
      ],
      'projection': [
        'RCB'
      ],
      'projection_type': 'acl'
    }
    }

    column_defs = [
        Column.define(
            'File_Type',
            builtin_types.text,
            nullok=False
        ),
        Column.define(
            'File_URL',
            builtin_types.text,
            annotations={
                'tag:isrd.isi.edu,2017:asset': {
                  'md5': 'File_MD5',
                  'url_pattern': '/hatrac/pdb/templates/{{{File_Name}}}',
                  'filename_column': 'File_Name',
                  'byte_count_column': 'File_Bytes'
                },
                'tag:isrd.isi.edu,2018:required': {}
              },
            acls={
                'select': [
                  '*'
                ]
              },
            acl_bindings={
                'no_binding': False
              },
            nullok=False
        ),
        Column.define(
            'File_Name',
            builtin_types.text,
            nullok=False
        ),
        Column.define(
            'File_MD5',
            builtin_types.text,
            nullok=False
        ),
        Column.define(
            'File_Bytes',
            builtin_types.int8,
            nullok=False
        ),
        Column.define(
            'Description',
            builtin_types.markdown,
            comment='- Description: None',
            nullok=False
        ),
        Column.define(
            'Owner',
            builtin_types.text,
            comment='- Description: Group that can update the record.',
            nullok=True
        )
    ]

    key_defs = [
    ]

    fkey_defs = [
        ForeignKey.define(['File_Type'], 'Vocab', 'File_Type', ['Name'],
                          constraint_names=[['PDB', 'Entry_Template_File_File_Type_fkey']],
                          on_update='NO ACTION',
                          on_delete='NO ACTION'   
        ),
        ForeignKey.define(['Owner'], 'public', 'Catalog_Group', ['ID'],
                          constraint_names=[['PDB', 'Entry_Template_File_Owner_fkey']],
                          on_update='NO ACTION',
                          on_delete='NO ACTION',
                          acls={
                            'insert': [
                              'https://auth.globus.org/eef3e02a-3c40-11e9-9276-0edc9bdd56a6'
                            ],
                            'update': [
                              'https://auth.globus.org/eef3e02a-3c40-11e9-9276-0edc9bdd56a6'
                            ]
                          },
                          acl_bindings={
                            'set_owner': {
                              'types': [
                                'update',
                                'insert'
                              ],
                              'scope_acl': [
                                '*'
                              ],
                              'projection': [
                                'ID'
                              ],
                              'projection_type': 'acl'
                            }
                          }
        )
    ]
    
    table_def = Table.define(
        table_name,
        column_defs,
        key_defs=key_defs,
        fkey_defs=fkey_defs,
        comment=comment,
        annotations=table_annotations,
        acl_bindings=table_acl_bindings,
        provide_system=True
    )
    
    return table_def

# ============================================================
def main(server_name, catalog_id, credentials):
    server = DerivaServer('https', server_name, credentials)
    catalog = server.connect_ermrest(catalog_id)
    catalog.dcctx['cid'] = 'oneoff/model'
    model = catalog.getCatalogModel()

    """
    Create table
    """
    utils.create_table_if_not_exist(model, 'PDB',  define_tdoc_Entry_Related_File_Templates())

# ===================================================    

if __name__ == '__main__':
    args = BaseCLI('ad-hoc table creation tool', None, 1).parse_cli()
    credentials = get_credential(args.host, args.credential_file)
#    if args.catalog is None:
#        catalog_id = 99

    main(args.host, 50, credentials)
    
