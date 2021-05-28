import sys
import json
from deriva.core import ErmrestCatalog, AttrDict, get_credential, DEFAULT_CREDENTIAL_FILE, tag, urlquote, DerivaServer, get_credential, BaseCLI
from deriva.core.ermrest_model import builtin_types, Schema, Table, Column, Key, ForeignKey, DomainType, ArrayType
import utils

"""
This script will be run after:
    - 2021_11_update_vocab.py
"""

# ========================================================
# -- create a table that is not a Vocab structure
def define_tdoc_ihm_data_transformation():
    table_name='ihm_data_transformation'
    comment='Details of rotation matrix and translation vector that can be applied to transform data; mmCIF category: ihm_data_transformation'

    column_defs = [
        Column.define(
            'id',
            builtin_types.int8,
            comment='An identifier to the transformation matrix',
            nullok=False
        ),
        Column.define(
            'rot_matrix[1][1]',
            builtin_types.float8,
            comment='Data item [1][1] of the rotation matrix used in the transformation',
            nullok=True
        ),
        Column.define(
            'rot_matrix[2][1]',
            builtin_types.float8,
            comment='Data item [2][1] of the rotation matrix used in the transformation',
            nullok=True
        ),
        Column.define(
            'rot_matrix[3][1]',
            builtin_types.float8,
            comment='Data item [3][1] of the rotation matrix used in the transformation',
            nullok=True
        ),
        Column.define(
            'rot_matrix[1][2]',
            builtin_types.float8,
            comment='Data item [1][2] of the rotation matrix used in the transformation',
            nullok=True
        ),
        Column.define(
            'rot_matrix[2][2]',
            builtin_types.float8,
            comment='Data item [2][2] of the rotation matrix used in the transformation',
            nullok=True
        ),
        Column.define(
            'rot_matrix[3][2]',
            builtin_types.float8,
            comment='Data item [3][2] of the rotation matrix used in the transformation',
            nullok=True
        ),
        Column.define(
            'rot_matrix[1][3]',
            builtin_types.float8,
            comment='Data item [1][3] of the rotation matrix used in the transformation',
            nullok=True
        ),
        Column.define(
            'rot_matrix[2][3]',
            builtin_types.float8,
            comment='Data item [2][3] of the rotation matrix used in the transformation',
            nullok=True
        ),
        Column.define(
            'rot_matrix[3][3]',
            builtin_types.float8,
            comment='Data item [3][3] of the rotation matrix used in the transformation',
            nullok=True
        ),
        Column.define(
            'tr_vector[1]',
            builtin_types.float8,
            comment='Data item [1] of the translation vector used in the transformation',
            nullok=True
        ),
        Column.define(
            'tr_vector[2]',
            builtin_types.float8,
            comment='Data item [2] of the translation vector used in the transformation',
            nullok=True
        ),
        Column.define(
            'tr_vector[3]',
            builtin_types.float8,
            comment='Data item [3] of the translation vector used in the transformation',
            nullok=True
        ),
        Column.define(
            'structure_id',
            builtin_types.text,
            comment='Structure identifier',
            nullok=False
        )
    ]
    #BV: This is a parent table with optional columns in the child table; so combo2 key is defined
    key_defs = [
        Key.define(['structure_id', 'id'], constraint_names=[['PDB', 'ihm_data_transformation_primary_key']] ),
        Key.define(['RID'], constraint_names=[['PDB', 'ihm_data_transformation_RID_key']] ),        
        Key.define(['RID', 'id'], constraint_names=[['PDB', 'ihm_data_transformation_combo2_key']] )
    ]

    # @brinda: add fk pseudo-definition
    #BV: No outgoing fkeys other than structure_id
    fkey_defs = [
        ForeignKey.define(['structure_id'], 'PDB', 'entry', ['id'],
                          constraint_names=[['PDB', 'ihm_data_transformation_structure_id_fkey']],
                          on_update='CASCADE',
                          on_delete='NO ACTION'   
        )
        
    ]
    
    table_def = Table.define(
        table_name,
        column_defs,
        key_defs=key_defs,
        fkey_defs=fkey_defs,
        comment=comment,
        provide_system=True
    )
    
    return table_def

# -------------------------------------------
def update_PDB_ihm_related_datasets(model):
    # -- add columns
    utils.create_column_if_not_exist(model, 'PDB', 'ihm_related_datasets', 
                                     Column.define(
                                        'transformation_id',
                                        builtin_types.int8,
                                        comment='Identifier corresponding to the transformation matrix to be applied to the derived dataset in order to transform it to the primary dataset',
                                        nullok=True
                                    ))
    utils.create_column_if_not_exist(model, 'PDB', 'ihm_related_datasets', 
                                     Column.define(
                                        'Transformation_RID',
                                        builtin_types.text,
                                        comment='Identifier to the transformation RID',
                                        nullok=True
                                    ))

    # -- add fk
    utils.create_foreign_key_if_not_exists(model, 'PDB', 'ihm_related_datasets', 'ihm_related_datasets_ihm_data_transformation_combo2_fkey', 
                                            ForeignKey.define(['Transformation_RID', 'transformation_id'], 'PDB', 'ihm_data_transformation', ['RID', 'id'],
                                                constraint_names=[ ['PDB', 'ihm_related_datasets_ihm_data_transformation_combo2_fkey'] ],
                                                on_update='CASCADE',
                                                on_delete='NO ACTION')
                                           )


# ============================================================
def main(server_name, catalog_id, credentials):
    server = DerivaServer('https', server_name, credentials)
    catalog = server.connect_ermrest(catalog_id)
    catalog.dcctx['cid'] = 'oneoff/model'
    model = catalog.getCatalogModel()

    """
    Create table
    """
    utils.create_table_if_not_exist(model, 'PDB',  define_tdoc_ihm_data_transformation())

    """
    Update existing model
    """    
    update_PDB_ihm_related_datasets(model) #Requires ihm_data_transformation

# ===================================================    

if __name__ == '__main__':
    args = BaseCLI('ad-hoc table creation tool', None, 1).parse_cli()
    credentials = get_credential(args.host, args.credential_file)
#    if args.catalog is None:
#        catalog_id = 99

    main(args.host, 99, credentials)
    
