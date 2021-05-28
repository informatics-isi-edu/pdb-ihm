import sys
import json
from deriva.core import ErmrestCatalog, AttrDict, get_credential, DEFAULT_CREDENTIAL_FILE, tag, urlquote, DerivaServer, get_credential, BaseCLI
from deriva.core.ermrest_model import builtin_types, Schema, Table, Column, Key, ForeignKey, DomainType, ArrayType
import utils

"""
This script will be run after:
    - 2021_11_update_vocab.py
    - 2021_04_ihm_data_transformation.py
"""

# ========================================================
# -- create a table that is not a Vocab structure
# -- define ihm_pseudo_site table --> Brida reviewed
def define_tdoc_ihm_pseudo_site():
    table_name='ihm_pseudo_site'
    comment='Details of pseudo sites that may be used in the restraints or model representation; can be uploaded as CSV/TSV file above; mmCIF category: ihm_pseudo_site'

    column_defs = [
        Column.define(
            'id',
            builtin_types.int8,
            comment='An identifier to the pseudo site',                        
            nullok=False
        ),
        Column.define(
            'Cartn_x',
            builtin_types.float8,
            comment='Cartesian X component corresponding to this pseudo site',
            nullok=False
        ),
        Column.define(
            'Cartn_y',
            builtin_types.float8,
            comment='Cartesian Y component corresponding to this pseudo site',
            nullok=False
        ),
        Column.define(
            'Cartn_z',
            builtin_types.float8,
            comment='Cartesian Z component corresponding to this pseudo site',
            nullok=False
        ),
        Column.define(
            'radius',
            builtin_types.float8,
            comment='Radius associated with the pseudo site',
            nullok=True
        ),
        Column.define(
            'description',
            builtin_types.text,
            comment='Additional description about the pseudo site',
            nullok=True
        ),
        Column.define(
            'Entry_Related_File',
            builtin_types.text,
            comment='A reference to the uploaded restraint file in the table Entry_Related_File.id.',
            nullok=True
        ),
        Column.define(
            'structure_id',
            builtin_types.text,
            comment='Structure identifier',
            nullok=False
        )
    ]
    #BV: This is a parent table with mandatory columns in the child table; so combo1 key is defined
    key_defs = [
        Key.define(['structure_id', 'id'], constraint_names=[['PDB', 'ihm_pseudo_site_primary_key']] ),
        Key.define(['RID'], constraint_names=[['PDB', 'ihm_pseudo_site_RID_key']] ),        
        Key.define(['RID', 'structure_id', 'id'], constraint_names=[['PDB', 'ihm_pseudo_site_combo1_key']] )
    ]

    # @brinda: add fk pseudo-definition
    #BV: No outgoing fkeys other than structure_id and Entry_Related_File
    fkey_defs = [
        ForeignKey.define(['structure_id'], 'PDB', 'entry', ['id'],
                          constraint_names=[['PDB', 'ihm_pseudo_site_structure_id_fkey']],
                          on_update='CASCADE',
                          on_delete='NO ACTION'   
        ),
        ForeignKey.define(['Entry_Related_File'], 'PDB', 'Entry_Related_File', ['RID'],
                          constraint_names=[['PDB', 'ihm_pseudo_site_Entry_Related_File_fkey']],
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

# --------------------------------------------------------------
def update_PDB_ihm_cross_link_restraint(model):
    # Add the PDB.ihm_cross_link_restraint.pseudo_site_flag column    
    utils.create_column_if_not_exist(model, 'PDB', 'ihm_cross_link_restraint', 
                                     Column.define(
                                        'pseudo_site_flag',
                                        builtin_types.text,
                                        comment='A flag indicating if the cross link involves a pseudo site that is not part of the model representation',
                                        nullok=True
                                    ))

    # Create the foreign key PDB.ihm_cross_link_restraint.pseudo_site_flag references Vocab.pseudo_site_flag.Name
    utils.create_foreign_key_if_not_exists(model, 'PDB', 'ihm_cross_link_restraint', 'ihm_cross_link_restraint_pseudo_site_flag_fkey', 
                                            ForeignKey.define(['pseudo_site_flag'], 'Vocab', 'pseudo_site_flag', ['Name'],
                                              constraint_names=[ ['Vocab', 'ihm_cross_link_restraint_pseudo_site_flag_fkey'] ],
                                              on_update='CASCADE',
                                              on_delete='NO ACTION')
                                           )

    # Create combo1 key
    utils.create_key_if_not_exists(model, 'PDB', 'ihm_cross_link_restraint', ['RID', 'structure_id', 'id'], 'ihm_cross_link_restraint_combo1_key')

def update_PDB_ihm_pseudo_site_feature(model):
    # Drop fkeys from ihm_pseudo_site_feature
    utils.drop_fkey_if_exist(model, 'PDB', 'ihm_pseudo_site_feature', 'ihm_pseudo_site_feature_feature_id_fkey')

    # -- Remove columns from the PDB.ihm_pseudo_site_feature table
    utils.drop_column_if_exist(model, 'PDB', 'ihm_pseudo_site_feature', 'Cartn_x')
    utils.drop_column_if_exist(model, 'PDB', 'ihm_pseudo_site_feature', 'Cartn_y')
    utils.drop_column_if_exist(model, 'PDB', 'ihm_pseudo_site_feature', 'Cartn_z')
    utils.drop_column_if_exist(model, 'PDB', 'ihm_pseudo_site_feature', 'radius')
    utils.drop_column_if_exist(model, 'PDB', 'ihm_pseudo_site_feature', 'description')
    
    # -- add columns
    utils.create_column_if_not_exist(model, 'PDB', 'ihm_pseudo_site_feature', 
                                     Column.define(
                                        'pseudo_site_id',
                                        builtin_types.int8,
                                        comment='Pseudo site identifier corresponding to this feature',
                                        nullok=False
                                    ))
    utils.create_column_if_not_exist(model, 'PDB', 'ihm_pseudo_site_feature', 
                                     Column.define(
                                        'Pseudo_Site_RID',
                                        builtin_types.text,
                                        comment='Identifier to the pseudo site RID',
                                        nullok=False
                                    ))
    utils.create_column_if_not_exist(model, 'PDB', 'ihm_pseudo_site_feature', 
                                     Column.define(
                                        'Feature_RID',
                                        builtin_types.text,
                                        comment='Identifier to the feature RID',
                                        nullok=False
                                    ))

    # -- add fk
    utils.create_foreign_key_if_not_exists(model, 'PDB', 'ihm_pseudo_site_feature', 'ihm_pseudo_site_feature_ihm_pseudo_site_combo1_fkey', 
                                            ForeignKey.define(['Pseudo_Site_RID', 'structure_id', 'pseudo_site_id'], 'PDB', 'ihm_pseudo_site', ['RID', 'structure_id', 'id'],
                                                            constraint_names=[ ['PDB', 'ihm_pseudo_site_feature_ihm_pseudo_site_combo1_fkey'] ],
                                                            on_update='CASCADE',
                                                            on_delete='NO ACTION')
                                           )

    utils.create_foreign_key_if_not_exists(model, 'PDB', 'ihm_pseudo_site_feature', 'ihm_pseudo_site_feature_ihm_feature_list_combo1_fkey', 
                                            ForeignKey.define(['Feature_RID', 'structure_id', 'feature_id'], 'PDB', 'ihm_feature_list', ['RID', 'structure_id', 'feature_id'],
                                                            constraint_names=[ ['PDB', 'ihm_pseudo_site_feature_ihm_feature_list_combo1_fkey'] ],
                                                            on_update='CASCADE',
                                                            on_delete='NO ACTION')  # won't allow delete until there is no reference
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
    utils.create_table_if_not_exist(model, 'PDB',  define_tdoc_ihm_pseudo_site())
    
    """
    Create combo1/combo2 keys in existing tables
    """
    utils.create_key_if_not_exists(model, 'PDB', 'ihm_model_list', ['RID', 'model_id'], 'ihm_model_list_combo2_key')
    utils.create_key_if_not_exists(model, 'PDB', 'ihm_feature_list', ['RID', 'structure_id', 'feature_id'], 'ihm_feature_list_combo1_key')
    utils.create_key_if_not_exists(model, 'PDB', 'ihm_dataset_list', ['RID', 'structure_id', 'id'], 'ihm_dataset_list_combo1_key')
    
    """
    Update existing model
    """
    update_PDB_ihm_cross_link_restraint(model) #Requires pseudo_site_flag
    update_PDB_ihm_pseudo_site_feature(model) #Requires ihm_pseudo_site and ihm_feature_list_combo1_key
    
    """
    Rename primary keys
    """
    utils.rename_key_if_exist(model, 'PDB', 'ihm_model_group', 'ihm_model_group_RID_id_key', 'ihm_model_group_combo2_key')
    utils.rename_key_if_exist(model, 'PDB', 'ihm_external_files', 'ihm_external_files_id_RID_key', 'ihm_external_files_combo2_key')
    
# ===================================================    

if __name__ == '__main__':
    args = BaseCLI('ad-hoc table creation tool', None, 1).parse_cli()
    credentials = get_credential(args.host, args.credential_file)

    main(args.host, 99, credentials)
    
