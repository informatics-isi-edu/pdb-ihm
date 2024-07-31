import sys
import json
from deriva.core import ErmrestCatalog, AttrDict, get_credential, DEFAULT_CREDENTIAL_FILE, tag, urlquote, DerivaServer, get_credential, BaseCLI
from deriva.core.ermrest_model import builtin_types, Schema, Table, Column, Key, ForeignKey, DomainType, ArrayType
import utils

"""
This script will be run after:
    - 
"""

# ========================================================
# -- create a table that is not a Vocab structure
def define_tdoc_ihm_multi_state_scheme():
    table_name='ihm_multi_state_scheme'
    comment='Details about multiple states that can form a connected/ordered scheme; mmCIF category: ihm_multi_state_scheme'

    column_defs = [
        Column.define(
            'id',
            builtin_types.int8,
            comment='A unique identifier for the multi-state scheme',                        
            nullok=False
        ),
        Column.define(
            'name',
            builtin_types.text,
            comment='Name for the multi-state scheme',
            nullok=True
        ),
        Column.define(
            'details',
            builtin_types.text,
            comment='Details about the multi-state scheme',
            nullok=True
        ),
        Column.define(
            "structure_id",
            builtin_types.text,
            comment='Structure identifier',
            nullok=False
        )
    ]
    key_defs = [
        Key.define(["structure_id", "id"], constraint_names=[["PDB", "ihm_multi_state_scheme_primary_key"]] ),
        Key.define(["RID"], constraint_names=[["PDB", "ihm_multi_state_scheme_RID_key"]] ),
        Key.define(["RID", "structure_id", "id"], constraint_names=[["PDB", "ihm_multi_state_scheme_combo1_key"]] )
    ]

    fkey_defs = [
        ForeignKey.define(["structure_id"], "PDB", "entry", ["id"],
                          constraint_names=[["PDB", "ihm_multi_state_scheme_structure_id_fkey"]],
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

# --------------------------------------------------------------
def define_tdoc_ihm_multi_state_scheme_connectivity():
    table_name='ihm_multi_state_scheme_connectivity'
    comment='Details about the ordered connectivities among states in a multi-state scheme; mmCIF category: ihm_multi_state_scheme_connectivity'

    column_defs = [
        Column.define(
            'id',
            builtin_types.int8,
            comment='A unique identifier for the multi-state scheme connectivity',
            nullok=False
        ),
        Column.define(
            'scheme_id',
            builtin_types.int8,
            comment='Identifier for the multi-state scheme',
            nullok=False
        ),
        Column.define(
            'begin_state_id',
            builtin_types.int8,
            comment='Identifier for the starting state in the multi-state scheme',
            nullok=False
        ),
        Column.define(
            'end_state_id',
            builtin_types.int8,
            comment='Identifier for the ending state in the multi-state scheme',
            nullok=True
        ),
        Column.define(
            'dataset_group_id',
            builtin_types.int8,
            comment='Identifier for the dataset group from which the multi-state scheme is obtained',
            nullok=False
        ),
        Column.define(
            "details",
            builtin_types.text,
            comment='Details about the multi-state scheme connectivity',
            nullok=True
        ),
        Column.define(
            "structure_id",
            builtin_types.text,
            comment='Structure identifier',
            nullok=False
        ),
        Column.define(
            "Scheme_RID",
            builtin_types.text,
            comment='Identifier to the multi-state scheme RID',
            nullok=False
        ),
        Column.define(
            "State_RID",
            builtin_types.text,
            comment='Identifier to the multi-state modeling state RID',
            nullok=False
        ),
        Column.define(
            "Dataset_Group_RID",
            builtin_types.text,
            comment='Identifier to the dataset group RID',
            nullok=False
        )
    ]
    key_defs = [
        Key.define(["structure_id", "id"], constraint_names=[["PDB", "ihm_multi_state_scheme_connectivity_primary_key"]] ),
        Key.define(["RID"], constraint_names=[["PDB", "ihm_multi_state_scheme_connectivity_RID_key"]] ),
        Key.define(["RID", "structure_id", "id"], constraint_names=[["PDB", "ihm_multi_state_scheme_connectivity_combo1_key"]] ),
        Key.define(["RID", "id"], constraint_names=[["PDB", "ihm_multi_state_scheme_connectivity_combo2_key"]] )
    ]

    fkey_defs = [
        ForeignKey.define(["structure_id"], "PDB", "entry", ["id"],
                          constraint_names=[["PDB", "ihm_multi_state_scheme_connectivity_structure_id_fkey"]],
                          on_update="CASCADE",
                          on_delete="NO ACTION"
        ), 
        ForeignKey.define(["Scheme_RID", "structure_id", "scheme_id"], "PDB", "ihm_multi_state_scheme", ["RID", "structure_id", "id"],
                          constraint_names=[["PDB", "ihm_multi_state_scheme_connectivity_scheme_combo1_fkey"]],
                          on_update="CASCADE",
                          on_delete="NO ACTION"
        ),
        ForeignKey.define(["State_RID", "structure_id", "begin_state_id"], "PDB", "ihm_multi_state_modeling", ["RID", "structure_id", "state_id"],
                          constraint_names=[["PDB", "ihm_multi_state_scheme_connectivity_modeling_1_combo1_fkey"]],
                          on_update="CASCADE",
                          on_delete="NO ACTION"
        ),
        ForeignKey.define(["State_RID", "end_state_id"], "PDB", "ihm_multi_state_modeling", ["RID", "state_id"],
                          constraint_names=[["PDB", "ihm_multi_state_scheme_connectivity_modeling_2_combo2_fkey"]],
                          on_update="CASCADE",
                          on_delete="NO ACTION"
        ),
        ForeignKey.define(["Dataset_Group_RID", "structure_id", "dataset_group_id"], "PDB", "ihm_dataset_group", ["RID", "structure_id", "id"],
                          constraint_names=[["PDB", "multi_state_scheme_connectivity_dataset_group_combo1_fkey"]],
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

# --------------------------------------------------------------
def define_tdoc_ihm_kinetic_rate():
    table_name='ihm_kinetic_rate'
    comment='Details about the kinetic rates obtained from biophysical experiments; mmCIF category: ihm_kinetic_rate'

    column_defs = [
        Column.define(
            'id',
            builtin_types.int8,
            comment='A unique identifier for the kinetic rate',
            nullok=False
        ),
        Column.define(
            'transition_rate_constant',
            builtin_types.float8,
            comment='The transition rate constant per second; unit = reciprocal seconds',
            nullok=True
        ),
        Column.define(
            'equilibrium_constant',
            builtin_types.float8,
            comment='The equilibrium constant',
            nullok=True
        ),
        Column.define(
            'equilibrium_constant_determination_method',
            builtin_types.text,
            comment='Method used to determine the equilibrium constant',
            nullok=True
        ),
        Column.define(
            'equilibrium_constant_unit',
            builtin_types.text,
            comment='Unit of the equilibrium constant, if applicable',
            nullok=True
        ),
        Column.define(
            'scheme_connectivity_id',
            builtin_types.int8,
            comment='Identifier for the multi-state scheme connectivity',
            nullok=False
        ),
        Column.define(
            'external_file_id',
            builtin_types.int8,
            comment='Identifier for the external file corresponding to the kinetic rate measurement',
            nullok=True
        ),
        Column.define(
            'dataset_group_id',
            builtin_types.int8,
            comment='Identifier for the dataset group from which the kinetic rate is obtained',
            nullok=False
        ),
        Column.define(
            "details",
            builtin_types.text,
            comment='Details about the kinetic rate',
            nullok=True
        ),
        Column.define(
            "structure_id",
            builtin_types.text,
            comment='Structure identifier',
            nullok=False
        ),
        Column.define(
            "Scheme_Connectivity_RID",
            builtin_types.text,
            comment='Identifier to the multi-state scheme connectivity RID',
            nullok=False
        ),
        Column.define(
            "External_File_RID",
            builtin_types.text,
            comment='Identifier to the external file RID',
            nullok=True
        ),
        Column.define(
            "Dataset_Group_RID",
            builtin_types.text,
            comment='Identifier to the dataset group RID',
            nullok=False
        )
    ]
    key_defs = [
        Key.define(["structure_id", "id"], constraint_names=[["PDB", "ihm_kinetic_rate_primary_key"]] ),
        Key.define(["RID"], constraint_names=[["PDB", "ihm_kinetic_rate_RID_key"]] )
    ]

    fkey_defs = [
        ForeignKey.define(["structure_id"], "PDB", "entry", ["id"],
                          constraint_names=[["PDB", "ihm_kinetic_rate_structure_id_fkey"]],
                          on_update="CASCADE",
                          on_delete="NO ACTION"
        ), 
        ForeignKey.define(["Scheme_Connectivity_RID", "structure_id", "scheme_connectivity_id"], "PDB", "ihm_multi_state_scheme_connectivity", ["RID", "structure_id", "id"],
                          constraint_names=[["PDB", "ihm_kinetic_rate_multi_state_scheme_connectivity_combo1_fkey"]],
                          on_update="CASCADE",
                          on_delete="NO ACTION"
        ),
        ForeignKey.define(["External_File_RID", "external_file_id"], "PDB", "ihm_external_files", ["RID", "id"],
                          constraint_names=[["PDB", "ihm_kinetic_rate_ihm_external_files_combo2_fkey"]],
                          on_update="CASCADE",
                          on_delete="NO ACTION"
        ),
        ForeignKey.define(["Dataset_Group_RID", "structure_id", "dataset_group_id"], "PDB", "ihm_dataset_group", ["RID", "structure_id", "id"],
                          constraint_names=[["PDB", "ihm_kinetic_rate_ihm_dataset_group_combo1_fkey"]],
                          on_update="CASCADE",
                          on_delete="NO ACTION"
        ),
        ForeignKey.define(['equilibrium_constant_determination_method'], 'Vocab', 'ihm_equilibrium_constant_determination_method', ['Name'],
                          constraint_names=[ ['Vocab', 'ihm_equilibrium_constant_determination_method_fkey'] ],
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
def define_tdoc_ihm_relaxation_time():
    table_name='ihm_relaxation_time'
    comment='Details about the relaxation_times obtained from biophysical experiments; mmCIF category: ihm_relaxation_time'

    column_defs = [
        Column.define(
            'id',
            builtin_types.int8,
            comment='A unique identifier for the relaxation time',
            nullok=False
        ),
        Column.define(
            'value',
            builtin_types.float8,
            comment='The relaxation time value',
            nullok=False
        ),
        Column.define(
            'unit',
            builtin_types.text,
            comment='The relaxation time unit',
            nullok=False
        ),
        Column.define(
            'amplitude',
            builtin_types.float8,
            comment='The relaxation time amplitude',
            nullok=True
        ),
        Column.define(
            'external_file_id',
            builtin_types.int8,
            comment='Identifier for the external file corresponding to the relaxation time measurement',
            nullok=True
        ),
        Column.define(
            'dataset_group_id',
            builtin_types.int8,
            comment='Identifier for the dataset group from which the relaxation time is obtained',
            nullok=False
        ),
        Column.define(
            "details",
            builtin_types.text,
            comment='Details about the relaxation time',
            nullok=True
        ),
        Column.define(
            "structure_id",
            builtin_types.text,
            comment='Structure identifier',
            nullok=False
        ),
        Column.define(
            "External_File_RID",
            builtin_types.text,
            comment='Identifier to the external file RID',
            nullok=True
        ),
        Column.define(
            "Dataset_Group_RID",
            builtin_types.text,
            comment='Identifier to the dataset group RID',
            nullok=False
        )
    ]
    key_defs = [
        Key.define(["structure_id", "id"], constraint_names=[["PDB", "ihm_relaxation_time_primary_key"]] ),
        Key.define(["RID"], constraint_names=[["PDB", "ihm_relaxation_time_RID_key"]] ),
        Key.define(["RID", "structure_id", "id"], constraint_names=[["PDB", "ihm_relaxation_time_combo1_key"]] )
    ]

    fkey_defs = [
        ForeignKey.define(["structure_id"], "PDB", "entry", ["id"],
                          constraint_names=[["PDB", "ihm_relaxation_time_structure_id_fkey"]],
                          on_update="CASCADE",
                          on_delete="NO ACTION"
        ), 
        ForeignKey.define(["External_File_RID", "external_file_id"], "PDB", "ihm_external_files", ["RID", "id"],
                          constraint_names=[["PDB", "ihm_relaxation_time_ihm_external_files_combo2_fkey"]],
                          on_update="CASCADE",
                          on_delete="NO ACTION"
        ),
        ForeignKey.define(["Dataset_Group_RID", "structure_id", "dataset_group_id"], "PDB", "ihm_dataset_group", ["RID", "structure_id", "id"],
                          constraint_names=[["PDB", "ihm_relaxation_time_ihm_dataset_group_combo1_fkey"]],
                          on_update="CASCADE",
                          on_delete="NO ACTION"
        ),
        ForeignKey.define(['unit'], 'Vocab', 'ihm_relaxation_time_unit', ['Name'],
                          constraint_names=[ ['Vocab', 'ihm_relaxation_time_unit_fkey'] ],
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
def define_tdoc_ihm_relaxation_time_multi_state_scheme():
    table_name='ihm_relaxation_time_multi_state_scheme'
    comment='Details about mapping the experimentally measured relaxation times with the multi-state schemes; mmCIF category: ihm_relaxation_time_multi_state_scheme'

    column_defs = [
        Column.define(
            'id',
            builtin_types.int8,
            comment='A unique identifier for mapping the relaxation time with the multi-state scheme',
            nullok=False
        ),
        Column.define(
            'relaxation_time_id',
            builtin_types.int8,
            comment='Identifier for the relaxation time',
            nullok=False
        ),
        Column.define(
            'scheme_id',
            builtin_types.int8,
            comment='Identifier for the multi-state scheme',
            nullok=False
        ),
        Column.define(
            'scheme_connectivity_id',
            builtin_types.int8,
            comment='Identifier for the multi-state scheme connectivity',
            nullok=True
        ),
        Column.define(
            "details",
            builtin_types.text,
            comment='Details about the relaxation time measurement',
            nullok=True
        ),
        Column.define(
            "structure_id",
            builtin_types.text,
            comment='Structure identifier',
            nullok=False
        ),
        Column.define(
            "Scheme_Connectivity_RID",
            builtin_types.text,
            comment='Identifier to the multi-state scheme connectivity RID',
            nullok=True
        ),
        Column.define(
            "Scheme_RID",
            builtin_types.text,
            comment='Identifier to the multi-state scheme RID',
            nullok=False
        ),
        Column.define(
            "Relaxation_Time_RID",
            builtin_types.text,
            comment='Identifier to the relaxation time RID',
            nullok=False
        )
    ]
    key_defs = [
        Key.define(["structure_id", "id"], constraint_names=[["PDB", "ihm_relaxation_time_multi_state_scheme_primary_key"]] ),
        Key.define(["RID"], constraint_names=[["PDB", "ihm_relaxation_time_multi_state_scheme_RID_key"]] )
    ]

    fkey_defs = [
        ForeignKey.define(["structure_id"], "PDB", "entry", ["id"],
                          constraint_names=[["PDB", "ihm_relaxation_time_multi_state_scheme_structure_id_fkey"]],
                          on_update="CASCADE",
                          on_delete="NO ACTION"
        ), 
        ForeignKey.define(["Scheme_Connectivity_RID", "scheme_connectivity_id"], "PDB", "ihm_multi_state_scheme_connectivity", ["RID", "id"],
                          constraint_names=[["PDB", "relaxation_time_multi_state_scheme_connectivity_combo2_fkey"]],
                          on_update="CASCADE",
                          on_delete="NO ACTION"
        ),
        ForeignKey.define(["Scheme_RID", "structure_id", "scheme_id"], "PDB", "ihm_multi_state_scheme", ["RID", "structure_id", "id"],
                          constraint_names=[["PDB", "ihm_relaxation_time_multi_state_scheme_scheme_combo1_fkey"]],
                          on_update="CASCADE",
                          on_delete="NO ACTION"
        ),
        ForeignKey.define(["Relaxation_Time_RID", "structure_id", "relaxation_time_id"], "PDB", "ihm_relaxation_time", ["RID", "structure_id", "id"],
                          constraint_names=[["PDB", "ihm_relaxation_time_multi_state_scheme_time_combo1_fkey"]],
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

# --------------------------------------------------------------
def update_PDB_existing_tables(model):

    #Create new columns in existing tables
    utils.create_column_if_not_exist(model, 'PDB', 'struct',
                                     Column.define(
                                        'pdbx_structure_determination_methodology',
                                        builtin_types.text,
                                        comment='Indicates if the structure was determined using experimental, computational, or integrative methods',
                                        nullok=True,
                                        default="integrative"
                                    ))

    # Create fkeys to Vocab tables
    utils.create_foreign_key_if_not_exists(model, 'PDB', 'struct', 'struct_pdbx_structure_determination_methodology_fkey',
                                            ForeignKey.define(['pdbx_structure_determination_methodology'], 'Vocab', 'struct_pdbx_structure_determination_methodology', ['Name'],
                                              constraint_names=[ ['Vocab', 'struct_pdbx_structure_determination_methodology_fkey'] ],
                                              on_update='CASCADE',
                                              on_delete='NO ACTION')
                                           )

    # Create/rename combo1 and combo2 keys in existing tables
    utils.create_key_if_not_exists(model, 'PDB', 'ihm_multi_state_modeling', ['RID', 'structure_id', 'state_id'], 'ihm_multi_state_modeling_combo1_key')
    utils.create_key_if_not_exists(model, 'PDB', 'ihm_multi_state_modeling', ['RID', 'state_id'], 'ihm_multi_state_modeling_combo2_key')
    utils.create_key_if_not_exists(model, 'PDB', 'ihm_dataset_group', ['RID', 'structure_id', 'id'], 'ihm_dataset_group_combo1_key')
    utils.rename_key_if_exist(model, 'PDB', 'ihm_dataset_group', 'ihm_dataset_group_RID_id_key', 'ihm_dataset_group_combo2_key')

# ============================================================
def main(server_name, catalog_id, credentials):
    server = DerivaServer('https', server_name, credentials)
    catalog = server.connect_ermrest(catalog_id)
    catalog.dcctx['cid'] = 'oneoff/model'
    model = catalog.getCatalogModel()

    """
    Update existing model
    """
    update_PDB_existing_tables(model)

    """
    Create table
    """
    utils.create_table_if_not_exist(model, 'PDB',  define_tdoc_ihm_multi_state_scheme())
    utils.create_table_if_not_exist(model, 'PDB',  define_tdoc_ihm_multi_state_scheme_connectivity())
    utils.create_table_if_not_exist(model, 'PDB',  define_tdoc_ihm_kinetic_rate())
    utils.create_table_if_not_exist(model, 'PDB',  define_tdoc_ihm_relaxation_time())
    utils.create_table_if_not_exist(model, 'PDB',  define_tdoc_ihm_relaxation_time_multi_state_scheme())

# ===================================================    

if __name__ == '__main__':
    args = BaseCLI('ad-hoc table creation tool', None, 1).parse_cli()
    credentials = get_credential(args.host, args.credential_file)

    main(args.host, 1, credentials)
    
