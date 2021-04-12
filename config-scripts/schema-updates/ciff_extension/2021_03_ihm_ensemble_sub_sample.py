import sys
import json
from deriva.core import ErmrestCatalog, AttrDict, get_credential, DEFAULT_CREDENTIAL_FILE, tag, urlquote, DerivaServer, get_credential, BaseCLI
from deriva.core.ermrest_model import builtin_types, Schema, Table, Column, Key, ForeignKey, DomainType, ArrayType
import utils


# ========================================================
# -- create a table that is not a Vocab structure
def define_tdoc_ihm_ensemble_sub_sample():
    table_name='ihm_ensemble_sub_sample'
    comment='Details of the sub samples within the ensembles; mmCIF category: ihm_ensemble_sub_sample'

    column_defs = [
        Column.define(
            "id",
            builtin_types.int8,
            comment='A unique id for the ensemble sub sample',
            nullok=False
        ),
        Column.define(
            "sample_name",
            builtin_types.text,
            comment='A name for the ensemble sub sample',
            nullok=True
        ),
        Column.define(
            "ensemble_id",
            builtin_types.int8,
            comment='The ensemble identifier corresponding to the sub sample',
            nullok=False
        ),
        Column.define(
            "num_models",
            builtin_types.int8,
            comment='The number of models in the ensemble sub sample',
            nullok=False
        ),
        Column.define(
            "num_models_deposited",
            builtin_types.int8,
            comment='The number of models in the sub sample that are deposited',
            nullok=True
        ),
        Column.define(
            "model_group_id",
            builtin_types.int8,
            comment='The model group identifier corresponding to the sub sample',
            nullok=True
        ),
        Column.define(
            "file_id",
            builtin_types.int8,
            comment='A reference to the external file containing the structural models in the sub sample',
            nullok=True
        ),
        Column.define(
            "structure_id",
            builtin_types.text,
            comment='Structure identifier',
            nullok=False
        ),
        Column.define(
            "Ensemble_RID",
            builtin_types.text,
            comment='Identifier to the ensemble RID',
            nullok=False
        ),
        Column.define(
            "Model_Group_RID",
            builtin_types.text,
            comment='Identifier to the model group RID',
            nullok=True
        ),
        Column.define(
            "File_RID",
            builtin_types.text,
            comment='Identifier to the external file RID',
            nullok=True
        )
    ]
    #BV: This is a leaf table; so no combo1/combo2 keys required
    key_defs = [
        Key.define(["structure_id", "id"], constraint_names=[["PDB", "ihm_ensemble_sub_sample_primary_key"]] ),
        Key.define(["RID"], constraint_names=[["PDB", "ihm_ensemble_sub_sample_RID_key"]] ),
    ]

    # @brinda: add fk pseudo-definition
    fkey_defs = [
        ForeignKey.define(["structure_id"], "PDB", "entry", ["id"],
                          constraint_names=[["PDB", "ihm_ensemble_sub_sample_structure_id_fkey"]],
                          on_update="CASCADE",
                          on_delete="NO ACTION"
        ),
        ForeignKey.define(["Ensemble_RID", "structure_id", "ensemble_id"], "PDB", "ihm_ensemble_info", ["RID", "structure_id", "ensemble_id"],
                          constraint_names=[["PDB", "ihm_ensemble_sub_sample_ihm_ensemble_info_combo1_fkey"]],
                          on_update="CASCADE",
                          on_delete="NO ACTION"
        ),
        ForeignKey.define(["Model_Group_RID", "model_group_id"], "PDB", "ihm_model_group", ["RID", "id"],
                          constraint_names=[["PDB", "ihm_ensemble_sub_sample_ihm_model_group_combo2_fkey"]],
                          on_update="CASCADE",
                          on_delete="NO ACTION"
        ),
        ForeignKey.define(["File_RID", "file_id"], "PDB", "ihm_external_files", ["RID", "id"],
                          constraint_names=[["PDB", "ihm_ensemble_sub_sample_ihm_external_files_combo2_fkey"]],
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



# ==========================================================================
# update existing table

# ---------------
def update_PDB_ihm_ensemble_info(model):
    table = model.schemas['PDB'].tables['ihm_ensemble_info']

    # Add the PDB.ihm_ensemble_info.sub_sample_flag and PDB.ihm_ensemble_info.sub_sampling_type columns   
    #table.create_column(
    #    Column.define(
    #        "sub_sample_flag",
    #        builtin_types.text,
    #        comment='A flag that indicates whether the ensemble consists of sub samples',
    #        nullok=True
    #    )
    #)
    #table.create_column(
    #    Column.define(
    #        "sub_sampling_type",
    #        builtin_types.text,
    #        comment='Type of sub sampling',
    #        nullok=True
    #    )
    #)

    # Create the foreign keys
    #table.create_fkey(
    #    ForeignKey.define(["sub_sample_flag"], "Vocab", "sub_sample_flag", ["Name"],
    #                      constraint_names=[ ["Vocab", "ihm_ensemble_info_sub_sample_flag_fkey"] ],
    #                      on_update="CASCADE",
    #                      on_delete="NO ACTION")
    #    )
    #table.create_fkey(
    #    ForeignKey.define(["sub_sampling_type"], "Vocab", "sub_sampling_type", ["Name"],
    #                      constraint_names=[ ["Vocab", "ihm_ensemble_info_sub_sampling_type_fkey"] ],
    #                      on_update="CASCADE",
    #                      on_delete="NO ACTION")
    #)

    table.create_key(
        Key.define(["RID", "structure_id", "ensemble_id"], constraint_names=[["PDB", "ihm_ensemble_info_combo1_key"]] )
    )

# ==========================================================================
# upload vocab table

# -----------------------------------
# add rows to Vocab.sub_sample_flag
def add_rows_to_Vocab_sub_sample_flag(catalog):    #@serban to review

    rows =[
        {'Name': 'Yes', 'Description': 'Ensemble consists of sub samples'},
        {'Name': 'No', 'Description': 'Ensemble does not consist of sub samples'}
    ]
    
    pb = catalog.getPathBuilder()
    schema = pb.Vocab
    sub_sample_flag = schema.sub_sample_flag
    sub_sample_flag.insert(rows, defaults=['ID', 'URI'])


# -----------------------------------
# add rows to Vocab.sub_sampling_type
def add_rows_to_Vocab_sub_sampling_type(catalog):    #@serban to review

    rows =[
        {'Name': 'random', 'Description': 'sub samples generated by randomly partitioning all structures in the group'},
        {'Name': 'independent', 'Description': 'each sub sample generated in the same fashion but in independent simulations'},
        {'Name': 'other', 'Description': 'other type of sub sampling'}
    ]
    
    pb = catalog.getPathBuilder()
    schema = pb.Vocab
    sub_sampling_type = schema.sub_sampling_type
    sub_sampling_type.insert(rows, defaults=['ID', 'URI'])


# ============================================================
def main(server_name, catalog_id, credentials):
    server = DerivaServer('https', server_name, credentials)
    catalog = server.connect_ermrest(catalog_id)
    catalog.dcctx['cid'] = "oneoff/model"
    model = catalog.getCatalogModel()

    
    #-- clean up
    #drop_table(catalog, 'PDB', 'ihm_ensemble_sub_sample')
    
    # Rename existing keys
    #rename_key(model, 'PDB', 'ihm_model_group', 'ihm_model_group_RID_id_key', 'ihm_model_group_combo2_key')
    #rename_key(model, 'PDB', 'ihm_external_files', 'ihm_external_files_id_RID_key', 'ihm_external_files_combo2_key')

    #create_table_if_not_exist(model, "Vocab",  define_Vocab_table('sub_sample_flag', 'Flag for ensembles consisting of sub samples'))
    #create_table_if_not_exist(model, "PDB",  define_tdoc_ihm_ensemble_sub_sample())

    #update_PDB_ihm_ensemble_info(model)
    
    #add_rows_to_Vocab_sub_sample_flag(catalog)
    #add_rows_to_Vocab_sub_sampling_type(catalog)

    

# ===================================================    

if __name__ == '__main__':
    args = BaseCLI("ad-hoc table creation tool", None, 1).parse_cli()
    credentials = get_credential(args.host, args.credential_file)
#    if args.catalog is None:
#        catalog_id = 99

    main(args.host, 99, credentials)
    
