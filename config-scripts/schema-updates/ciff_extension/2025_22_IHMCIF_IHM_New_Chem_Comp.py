import sys
import json
from deriva.core import ErmrestCatalog, AttrDict, get_credential, DEFAULT_CREDENTIAL_FILE, tag, urlquote, DerivaServer, BaseCLI
from deriva.core.ermrest_model import builtin_types, Schema, Table, Column, Key, ForeignKey, DomainType, ArrayType
import utils

# ========================================================
# -- create a table to track new chem comps (https://github.com/informatics-isi-edu/pdb-ihm/issues/274)
def define_tdoc_IHM_New_Chem_Comp():
    table_name='IHM_New_Chem_Comp'
    comment='Details of new chemical components needed / created for PDB-IHM'

    column_defs = [
        Column.define(
            'comp_id',
            builtin_types.text,
            comment='An identifier for the new chemical component',
            nullok=False
        ),
        Column.define(
            'pdbx_release_status',
            builtin_types.text,
            comment='Current release status of the chemical component',
            nullok=False
        ),
        Column.define(
            'pdbx_processing_site',
            builtin_types.text,
            comment='Deposition site that processed this chemical component definition',
            nullok=False
        ),
        Column.define(
            'Created_For',
            builtin_types.text,
            comment='Resource for which the chemical component definition was created for',
            nullok=False
        ),
        Column.define(
            'Creation_Date',
            builtin_types.date,
            comment='Creation date of the chemical component definition',
            nullok=False
        ),
        Column.define(
            'First_IHM_Entry_RID',
            builtin_types.text,
            comment='Entry RID of the first IHM entry for which the chemical component defintion was created',
            nullok=True
        ),
        Column.define(
            'First_PDB_Entry_ID',
            builtin_types.text,
            comment='Entry ID of the first PDB entry for which the chemical component defintion was created',
            nullok=True
        ),
        Column.define(
            'Release_IHM_Entry_RID',
            builtin_types.text,
            comment='Entry RID of the first released IHM entry with which the chemical component defintion was released',
            nullok=True
        ),
        Column.define(
            'Release_PDB_Entry_ID',
            builtin_types.text,
            comment='Entry ID of the first released PDB entry with which the chemical component defintion was released',
            nullok=True
        ),
        Column.define(
            'Release_Date',
            builtin_types.date,
            comment='Release date of the chemical component definition',
            nullok=True
        ),
        Column.define(
            'Notes',
            builtin_types.markdown,
            comment='Curator notes about the chemical component',
            nullok=True
        ),
        Column.define(
            'chem_comp_type',
            builtin_types.text,
            comment='Type of chemical component',
            nullok=False
        ),
        Column.define(
            'CCD_CIF_File_URL',
            builtin_types.text,
            comment='File URL of the CCD CIF file generated by the OneDep standalone ligand module',
            nullok=True
        ),
        Column.define(
            'CCD_CIF_File_Name',
            builtin_types.text,
            comment='File name of the CCD CIF file generated by the OneDep standalone ligand module',
            nullok=True
        ),
        Column.define(
            'CCD_CIF_File_MD5',
            builtin_types.text,
            comment='MD5 of the CCD CIF file generated by the OneDep standalone ligand module',
            nullok=True
        ),
        Column.define(
            'CCD_CIF_File_Bytes',
            builtin_types.int8,
            comment='File size in bytes of the CCD CIF file generated by the OneDep standalone ligand module',
            nullok=True
        )
    ]
    key_defs = [
        Key.define(['comp_id'], constraint_names=[['PDB', 'IHM_New_Chem_Comp_primary_key']] ),
        Key.define(['RID'], constraint_names=[['PDB', 'IHM_New_Chem_Comp_RID_key']] ),
        Key.define(['CCD_CIF_File_MD5'], constraint_names=[['PDB', 'IHM_New_Chem_Comp_CCD_CIF_File_MD5_key']] )
    ]

    fkey_defs = [
        ForeignKey.define(['First_IHM_Entry_RID'], 'PDB', 'entry', ['RID'],
                          constraint_names=[['PDB', 'IHM_New_Chem_Comp_First_entry_fkey']],
                          on_update='CASCADE',
                          on_delete='NO ACTION'
        ),
        ForeignKey.define(['Release_IHM_Entry_RID'], 'PDB', 'entry', ['RID'],
                          constraint_names=[['PDB', 'IHM_New_Chem_Comp_Release_entry_fkey']],
                          on_update='CASCADE',
                          on_delete='NO ACTION'
        ),
        ForeignKey.define(["pdbx_release_status"], "Vocab", "chem_comp_pdbx_release_status", ["Name"],
                          constraint_names=[ ["Vocab", "IHM_New_Chem_Comp_pdbx_release_status_fkey"] ],
                          on_update="CASCADE",
                          on_delete="NO ACTION"
        ),
        ForeignKey.define(["pdbx_processing_site"], "Vocab", "chem_comp_pdbx_processing_site", ["Name"],
                          constraint_names=[ ["Vocab", "IHM_New_Chem_Comp_pdbx_processing_site_fkey"] ],
                          on_update="CASCADE",
                          on_delete="NO ACTION"
        ),
        ForeignKey.define(["Created_For"], "Vocab", "chem_comp_ihm_created_for", ["Name"],
                          constraint_names=[ ["Vocab", "IHM_New_Chem_Comp_Created_For_fkey"] ],
                          on_update="CASCADE",
                          on_delete="NO ACTION"
        ),
        ForeignKey.define(["chem_comp_type"], "Vocab", "chem_comp_type", ["Name"],
                          constraint_names=[ ["Vocab", "IHM_New_Chem_Comp_Type_fkey"] ],
                          on_update="CASCADE",
                          on_delete="NO ACTION"
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

# Update ihm_cross_link_result and ihm_ensemble_info to support IHMCIF v1.28 (https://github.com/informatics-isi-edu/pdb-ihm/issues/275)
def update_PDB_ihm_cross_link_result(model):
    utils.create_column_if_not_exist(model, 'PDB', 'ihm_cross_link_result',
                                     Column.define(
                                        'Model_Group_RID',
                                        builtin_types.text,
                                        comment='Identifier to the model group RID',
                                        nullok=True
                                    ))
    utils.create_column_if_not_exist(model, 'PDB', 'ihm_cross_link_result',
                                     Column.define(
                                        'model_group_id',
                                        builtin_types.int8,
                                        comment='An identifier for the group of structure models whose results are described',
                                        nullok=True
                                    ))

    utils.create_foreign_key_if_not_exists(model, 'PDB', 'ihm_cross_link_result', 'ihm_cross_link_result_model_group_combo2_fkey',
                                            ForeignKey.define(['Model_Group_RID', 'model_group_id'], 'PDB', 'ihm_model_group', ['RID', 'id'],
                                              constraint_names=[ ['PDB', 'ihm_cross_link_result_model_group_combo2_fkey'] ],
                                              on_update='CASCADE',
                                              on_delete='NO ACTION')
                                          )

    utils.create_column_if_not_exist(model, 'PDB', 'ihm_cross_link_result',
                                     Column.define(
                                        'Ensemble_RID',
                                        builtin_types.text,
                                        comment='Identifier to the ensemble RID',
                                        nullok=True
                                    ))

    utils.drop_fkey_if_exist(model, 'PDB', 'ihm_cross_link_result', 'ihm_cross_link_result_ensemble_id_fkey')

    utils.create_key_if_not_exists(model, 'PDB', 'ihm_ensemble_info', ['RID', 'ensemble_id'], 'ihm_ensemble_info_combo2_key')

    utils.create_foreign_key_if_not_exists(model, 'PDB', 'ihm_cross_link_result', 'ihm_cross_link_result_ensemble_info_combo2_fkey',
                                            ForeignKey.define(['Ensemble_RID', 'ensemble_id'], 'PDB', 'ihm_ensemble_info', ['RID', 'ensemble_id'],
                                              constraint_names=[ ['PDB', 'ihm_cross_link_result_ensemble_info_combo2_fkey'] ],
                                              on_update='CASCADE',
                                              on_delete='NO ACTION')
                                           )

    utils.create_column_if_not_exist(model, 'PDB', 'ihm_cross_link_result',
                                     Column.define(
                                        'Restraint_RID',
                                        builtin_types.text,
                                        comment='Identifier to the crosslink restraint RID',
                                        nullok=True
                                    ))

    utils.create_key_if_not_exists(model, 'PDB', 'ihm_cross_link_restraint', ['RID', 'id', 'structure_id'], 'ihm_cross_link_restraint_combo1_key')

    utils.drop_fkey_if_exist(model, 'PDB', 'ihm_cross_link_result', 'ihm_cross_link_result_restraint_id_fkey')

    utils.create_foreign_key_if_not_exists(model, 'PDB', 'ihm_cross_link_result', 'ihm_cross_link_result_cross_link_restraint_combo1_fkey',
                                            ForeignKey.define(['Restraint_RID', 'restraint_id', 'structure_id'], 'PDB', 'ihm_cross_link_restraint', ['RID', 'id', 'structure_id'],
                                              constraint_names=[ ['PDB', 'ihm_cross_link_result_cross_link_restraint_combo1_fkey'] ],
                                              on_update='CASCADE',
                                              on_delete='NO ACTION')
                                          )

def update_PDB_entry(model):
    utils.create_column_if_not_exist(model, 'PDB', 'entry',
                                     Column.define(
                                        'New_Chem_Comp_Pending',
                                        builtin_types.boolean,
                                        comment='Indicates if a new chemical component associated with the entry is pending release',
                                        nullok=True,
                                        default=False
                                    ))

# Add BMRbig to support IHMCIF v1.28 (https://github.com/informatics-isi-edu/pdb-ihm/issues/275)
ihm_dataset_related_db_reference_db_name_rows = [
    {'Name': 'BMRbig', 'Description': 'BMRbig'}
    ]

chem_comp_pdbx_release_status_rows = [
        {'Name': 'HOLD', 'Description': 'On hold until yyyy-mm-dd'},
        {'Name': 'HPUB', 'Description': 'On hold until publication'},
        {'Name': 'REL', 'Description': 'Released'},
        {'Name': 'OBS', 'Description': 'Component defintion has been obsoleted and replaced by another entry'},
        {'Name': 'DEL', 'Description': 'Component definition has been deleted'},
        {'Name': 'REF_ONLY', 'Description': 'Component definition is provided for reference only and will not be used in released entries'}
    ]

chem_comp_pdbx_processing_site_rows = [
        {'Name': 'RCSB', 'Description': 'RCSB PDB'},
        {'Name': 'PDBE', 'Description': 'PDBE'},
        {'Name': 'PDBJ', 'Description': 'PDBJ'},
        {'Name': 'PDBC', 'Description': 'PDBC'},
        {'Name': 'EBI', 'Description': 'EBI'}
    ]

chem_comp_ihm_created_for_rows = [ 
        {'Name': 'PDB', 'Description': 'PDB'},
        {'Name': 'PDB-IHM', 'Description': 'PDB-IHM'}
    ]

def main(server_name, catalog_id, credentials):
    server = DerivaServer('https', server_name, credentials)
    catalog = server.connect_ermrest(catalog_id)
    catalog.dcctx['cid'] = "oneoff/model"
    model = catalog.getCatalogModel()

    if True:
        """
        Create new Vocab tables
        """
        utils.create_table_if_not_exist(model, 'Vocab', utils.define_Vocab_table('chem_comp_pdbx_release_status', 'Chemical Component Release Status'))
        utils.create_table_if_not_exist(model, 'Vocab', utils.define_Vocab_table('chem_comp_pdbx_processing_site', 'Chemical Component Processing Site'))
        utils.create_table_if_not_exist(model, 'Vocab', utils.define_Vocab_table('chem_comp_ihm_created_for', 'Chemical Component Created For'))

        """
        Load data into new and existing vocabulary tables
        """
        utils.add_rows_to_vocab_table(catalog, 'ihm_dataset_related_db_reference_db_name', ihm_dataset_related_db_reference_db_name_rows)
        utils.add_rows_to_vocab_table(catalog, 'chem_comp_pdbx_release_status', chem_comp_pdbx_release_status_rows)
        utils.add_rows_to_vocab_table(catalog, 'chem_comp_pdbx_processing_site', chem_comp_pdbx_processing_site_rows)
        utils.add_rows_to_vocab_table(catalog, 'chem_comp_ihm_created_for', chem_comp_ihm_created_for_rows)

        """
        Alter nullok for columns in existing table
        """
        utils.set_nullok_column_if_exists(model, 'PDB', 'ihm_cross_link_result', 'ensemble_id', True)
        utils.set_nullok_column_if_exists(model, 'PDB', 'ihm_cross_link_result', 'num_models', True)

        """
        Update existing tables
        """
        update_PDB_ihm_cross_link_result(model)
        update_PDB_entry(model)

        """
        Create IHM_New_Chem_Comp table
        """
        utils.create_table_if_not_exist(model, 'PDB',  define_tdoc_IHM_New_Chem_Comp())

    # To be applied after data is fixed in PDB:ihm_cross_link_result.Restraint_RID column
    if False:
        utils.set_nullok_column_if_exists(model, 'PDB', 'ihm_cross_link_result', 'Restraint_RID', False)

if __name__ == '__main__':
    args = BaseCLI("ad-hoc table creation tool", None, 1).parse_cli()
    credentials = get_credential(args.host, args.credential_file)

    main(args.host, 99, credentials)
    
