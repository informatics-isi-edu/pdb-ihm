import sys
import json
from deriva.core import ErmrestCatalog, AttrDict, get_credential, DEFAULT_CREDENTIAL_FILE, tag, urlquote, DerivaServer, get_credential, BaseCLI
from deriva.core.ermrest_model import builtin_types, Schema, Table, Column, Key, ForeignKey, DomainType, ArrayType
import utils

# ========================================================

# ============================================================

def main(server_name, catalog_id, credentials):
    server = DerivaServer('https', server_name, credentials)
    catalog = server.connect_ermrest(catalog_id)
    catalog.dcctx['cid'] = 'oneoff/model'
    model = catalog.getCatalogModel()

    utils.alter_on_update_fkey_if_exist(model, 'PDB', 'Entry_Related_File', 'Entry_Related_File_File_Type_fkey', 'CASCADE')

    utils.create_column_if_not_exist(model, 'PDB', 'ihm_starting_computational_models',
                                     Column.define(
                                        'External_Files_RID',
                                        builtin_types.text,
                                        comment='Identifier to the external files RID',
                                        nullok=True
                                    ))
    utils.create_column_if_not_exist(model, 'PDB', 'ihm_starting_computational_models',
                                     Column.define(
                                        'Software_RID',
                                        builtin_types.text,
                                        comment='Identifier to the software RID',
                                        nullok=True
                                    ))
    utils.create_column_if_not_exist(model, 'PDB', 'ihm_interface_residue_feature',
                                     Column.define(
                                        'Dataset_List_RID',
                                        builtin_types.text,
                                        comment='Identifier to the dataset list RID',
                                        nullok=True
                                    ))
    utils.create_column_if_not_exist(model, 'PDB', 'ihm_derived_distance_restraint',
                                     Column.define(
                                        'Dataset_List_RID',
                                        builtin_types.text,
                                        comment='Identifier to the dataset list RID',
                                        nullok=True
                                    ))
    utils.create_column_if_not_exist(model, 'PDB', 'ihm_geometric_object_distance_restraint',
                                     Column.define(
                                        'Dataset_List_RID',
                                        builtin_types.text,
                                        comment='Identifier to the dataset list RID',
                                        nullok=True
                                    ))

    utils.rename_fkey_if_exist(model, 'PDB', 'ihm_starting_computational_models', 'ihm_starting_computational_models_script_file_id_fkey', 'ihm_starting_computational_models_script_file_id_fk')
    utils.rename_fkey_if_exist(model, 'PDB', 'ihm_starting_computational_models', 'ihm_starting_computational_models_software_id_fkey', 'ihm_starting_computational_models_software_id_fk')
    utils.rename_fkey_if_exist(model, 'PDB', 'ihm_interface_residue_feature', 'ihm_interface_residue_feature_dataset_list_id_fkey', 'ihm_interface_residue_feature_dataset_list_id_fk')
    utils.rename_fkey_if_exist(model, 'PDB', 'ihm_derived_distance_restraint', 'ihm_derived_distance_restraint_dataset_list_id_fkey', 'ihm_derived_distance_restraint_dataset_list_id_fk')
    utils.rename_fkey_if_exist(model, 'PDB', 'ihm_geometric_object_distance_restraint', 'ihm_geometric_object_distance_restraint_dataset_list_id_fkey', 'ihm_geometric_object_distance_restraint_dataset_list_id_fk')

    utils.create_key_if_not_exists(model, 'PDB', 'ihm_dataset_list', ['RID', 'id'], 'ihm_dataset_list_combo2_key')

    model = catalog.getCatalogModel()
    utils.create_foreign_key_if_not_exists(model, 'PDB', 'ihm_starting_computational_models', 'ihm_starting_computational_models_script_file_id_fkey', 
                                            ForeignKey.define(['External_Files_RID', 'script_file_id'], 'PDB', 'ihm_external_files', ['RID', 'id'],
                                                                                            constraint_names=[ ['PDB', 'ihm_starting_computational_models_script_file_id_fkey'] ],
                                                                                            on_update='CASCADE',
                                                                                            on_delete='NO ACTION')
                                                )
    model = catalog.getCatalogModel()
    utils.create_foreign_key_if_not_exists(model, 'PDB', 'ihm_starting_computational_models', 'ihm_starting_computational_models_software_id_fkey', 
                                            ForeignKey.define(['Software_RID', 'software_id'], 'PDB', 'software', ['RID', 'pdbx_ordinal'],
                                                                                            constraint_names=[ ['PDB', 'ihm_starting_computational_models_software_id_fkey'] ],
                                                                                            on_update='CASCADE',
                                                                                            on_delete='NO ACTION')
                                                )
    model = catalog.getCatalogModel()
    utils.create_foreign_key_if_not_exists(model, 'PDB', 'ihm_interface_residue_feature', 'ihm_interface_residue_feature_dataset_list_id_fkey', 
                                            ForeignKey.define(['Dataset_List_RID', 'dataset_list_id'], 'PDB', 'ihm_dataset_list', ['RID', 'id'],
                                                                                            constraint_names=[ ['PDB', 'ihm_interface_residue_feature_dataset_list_id_fkey'] ],
                                                                                            on_update='CASCADE',
                                                                                            on_delete='NO ACTION')
                                                )
    model = catalog.getCatalogModel()
    utils.create_foreign_key_if_not_exists(model, 'PDB', 'ihm_derived_distance_restraint', 'ihm_derived_distance_restraint_dataset_list_id_fkey', 
                                            ForeignKey.define(['Dataset_List_RID', 'dataset_list_id'], 'PDB', 'ihm_dataset_list', ['RID', 'id'],
                                                                                            constraint_names=[ ['PDB', 'ihm_derived_distance_restraint_dataset_list_id_fkey'] ],
                                                                                            on_update='CASCADE',
                                                                                            on_delete='NO ACTION')
                                                )
    model = catalog.getCatalogModel()
    utils.create_foreign_key_if_not_exists(model, 'PDB', 'ihm_geometric_object_distance_restraint', 'ihm_geometric_object_distance_restraint_dataset_list_id_fkey', 
                                            ForeignKey.define(['Dataset_List_RID', 'dataset_list_id'], 'PDB', 'ihm_dataset_list', ['RID', 'id'],
                                                                                            constraint_names=[ ['PDB', 'ihm_geometric_object_distance_restraint_dataset_list_id_fkey'] ],
                                                                                            on_update='CASCADE',
                                                                                            on_delete='NO ACTION')
                                                )
    

# ===================================================    

if __name__ == '__main__':
    args = BaseCLI('ad-hoc table creation tool', None, 1).parse_cli()
    credentials = get_credential(args.host, args.credential_file)
#    if args.catalog is None:
#        catalog_id = 99

    main(args.host, 99, credentials)
    
