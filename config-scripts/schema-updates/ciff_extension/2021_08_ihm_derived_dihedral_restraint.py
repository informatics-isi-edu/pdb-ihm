import sys
import json
from deriva.core import ErmrestCatalog, AttrDict, get_credential, DEFAULT_CREDENTIAL_FILE, tag, urlquote, DerivaServer, get_credential, BaseCLI
from deriva.core.ermrest_model import builtin_types, Schema, Table, Column, Key, ForeignKey, DomainType, ArrayType
import utils


# ========================================================
# -- create a table that is not a Vocab structure
def define_tdoc_ihm_derived_dihedral_restraint():
    table_name='ihm_derived_dihedral_restraint'
    comment='Details of dihedral restraints used in integrative modeling; can be uploaded as CSV/TSV file above; mmCIF category: ihm_derived_dihedral_restraint'

    column_defs = [
        Column.define(
            "id",
            builtin_types.int8,
            comment='An identifier for the dihedral restraint',
            nullok=False
        ),
        Column.define(
            "group_id",
            builtin_types.int8,
            comment='An identifier to group the dihedral restraints',
            nullok=True
        ),
        Column.define(
            "feature_id_1",
            builtin_types.int8,
            comment='The feature identifier for the first partner in the dihedral restraint',
            nullok=False
        ),
        Column.define(
            "feature_id_2",
            builtin_types.int8,
            comment='The feature identifier for the second partner in the dihedral restraint',
            nullok=False
        ),
        Column.define(
            "feature_id_3",
            builtin_types.int8,
            comment='The feature identifier for the third partner in the dihedral restraint',
            nullok=False
        ),
        Column.define(
            "feature_id_4",
            builtin_types.int8,
            comment='The feature identifier for the fourth partner in the dihedral restraint',
            nullok=False
        ),
        Column.define(
            "group_conditionality",
            builtin_types.text,
            comment='If a group of dihedrals are restrained together, this data item defines the conditionality based on which the restraint is applied in the modeling',
            nullok=True
        ),
        Column.define(
            "dihedral_lower_limit",
            builtin_types.float8,
            comment='The lower limit to the threshold applied to this dihedral restraint',
            nullok=True
        ),
        Column.define(
            "dihedral_upper_limit",
            builtin_types.float8,
            comment='The upper limit to the threshold applied to this dihedral restraint',
            nullok=True
        ),
        Column.define(
            "dihedral_lower_limit_esd",
            builtin_types.float8,
            comment='The estimated standard deviation of the lower limit dihedral threshold applied',
            nullok=True
        ),
        Column.define(
            "dihedral_upper_limit_esd",
            builtin_types.float8,
            comment='The estimated standard deviation of the upper limit dihedral threshold applied',
            nullok=True
        ),
        Column.define(
            "probability",
            builtin_types.float8,
            comment='The probability that the dihedral restraint is correct',
            nullok=True
        ),
        Column.define(
            "restraint_type",
            builtin_types.text,
            comment='The type of dihedral restraint applied',
            nullok=False
        ),
        Column.define(
            "dihedral_threshold_mean",
            builtin_types.float8,
            comment='The dihedral threshold mean applied to the restraint',
            nullok=True
        ),
        Column.define(
            "dihedral_threshold_mean_esd",
            builtin_types.float8,
            comment='The estimated standard deviation of the dihedral threshold mean applied to the restraint',
            nullok=True
        ),
        Column.define(
            "dataset_list_id",
            builtin_types.int8,
            comment='Identifier to the input data from which the dihedral restraint is derived',
            nullok=False
        ),
        Column.define(
            "Entry_Related_File",
            builtin_types.text,
            comment='A reference to the uploaded restraint file in the table Entry_Related_File.id.',
            nullok=True
        ),
        Column.define(
            "structure_id",
            builtin_types.text,
            comment='Structure identifier',
            nullok=False
        ),
        # HT: to use for Chaise
        Column.define(
            "Feature_Id_1_RID",
            builtin_types.text,
            comment='Identifier to the feature 1 RID',
            nullok=False
        ),
        Column.define(
            "Feature_Id_2_RID",
            builtin_types.text,
            comment='Identifier to the feature 2 RID',
            nullok=False
        ),
        Column.define(
            "Feature_Id_3_RID",
            builtin_types.text,
            comment='Identifier to the feature 3 RID',
            nullok=False
        ),
        Column.define(
            "Feature_Id_4_RID",
            builtin_types.text,
            comment='Identifier to the feature 4 RID',
            nullok=False
        ),
        Column.define(
            "Dataset_List_RID",
            builtin_types.text,
            comment='Identifier to the dataset list RID',
            nullok=False
        )
    ]
    #BV: This is a leaf table; so no combo1/combo2 keys required
    key_defs = [
        Key.define(["structure_id", "id"], constraint_names=[["PDB", "ihm_derived_dihedral_restraint_primary_key"]] ),
        Key.define(["RID"], constraint_names=[["PDB", "ihm_derived_dihedral_restraint_RID_key"]] ),
    ]

    # @brinda: add fk pseudo-definition
    fkey_defs = [
        # HT: it own fk to Entry table
        ForeignKey.define(["structure_id"], "PDB", "entry", ["id"],
                          constraint_names=[["PDB", "ihm_derived_dihedral_restraint_structure_id_fkey"]],
                          on_update="CASCADE",
                          on_delete="NO ACTION"
        ),
        # HT: In annotation, apply domain_filter to filter the RID list by constraining structure_id        
        ForeignKey.define(["Feature_Id_1_RID", "structure_id", "feature_id_1"], "PDB", "ihm_feature_list", ["RID", "structure_id", "feature_id"],
                          constraint_names=[["PDB", "ihm_derived_dihedral_restraint_ihm_feature_list_1_combo1_fkey"]],
                          on_update="CASCADE",
                          on_delete="NO ACTION"
        ),
        ForeignKey.define(["Feature_Id_2_RID", "structure_id", "feature_id_2"], "PDB", "ihm_feature_list", ["RID", "structure_id", "feature_id"],
                          constraint_names=[["PDB", "ihm_derived_dihedral_restraint_ihm_feature_list_2_combo1_fkey"]],
                          on_update="CASCADE",
                          on_delete="NO ACTION"
        ),
        ForeignKey.define(["Feature_Id_3_RID", "structure_id", "feature_id_3"], "PDB", "ihm_feature_list", ["RID", "structure_id", "feature_id"],
                          constraint_names=[["PDB", "ihm_derived_dihedral_restraint_ihm_feature_list_3_combo1_fkey"]],
                          on_update="CASCADE",
                          on_delete="NO ACTION"
        ),
        ForeignKey.define(["Feature_Id_4_RID", "structure_id", "feature_id_4"], "PDB", "ihm_feature_list", ["RID", "structure_id", "feature_id"],
                          constraint_names=[["PDB", "ihm_derived_dihedral_restraint_ihm_feature_list_4_combo1_fkey"]],
                          on_update="CASCADE",
                          on_delete="NO ACTION"
        ),
        ForeignKey.define(["Dataset_List_RID", "structure_id", "dataset_list_id"], "PDB", "ihm_dataset_list", ["RID", "structure_id", "id"],
                          constraint_names=[["PDB", "ihm_derived_dihedral_restraint_ihm_dataset_list_combo1_fkey"]],
                          on_update="CASCADE",
                          on_delete="NO ACTION"
        ),
        ForeignKey.define(["group_conditionality"], "Vocab", "ihm_derived_dihedral_restraint_group_conditionality", ["Name"],
                          constraint_names=[ ["Vocab", "ihm_derived_dihedral_restraint_group_conditionality_fkey"] ],
                          on_update="CASCADE",
                          on_delete="NO ACTION"
        ),
        ForeignKey.define(["restraint_type"], "Vocab", "ihm_derived_dihedral_restraint_restraint_type", ["Name"],
                          constraint_names=[ ["Vocab", "ihm_derived_dihedral_restraint_restraint_type_fkey"] ],
                          on_update="CASCADE",
                          on_delete="NO ACTION"
        ),
        ForeignKey.define(["Entry_Related_File"], "PDB", "Entry_Related_File", ["RID"],
                          constraint_names=[["PDB", "ihm_derived_dihedral_restraint_Entry_Related_File_fkey"]],
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
# update vocab table
def add_rows_to_Vocab_ihm_derived_dihedral_restraint_group_conditionality(catalog):

    rows =[
        {'Name': 'ALL', 'Description': 'All dihedrals in the group are required to be satisfied'},
        {'Name': 'ANY', 'Description': 'Any one of the dihedrals in the group could be satisfied'}
    ]
    
    pb = catalog.getPathBuilder()
    schema = pb.Vocab
    ihm_derived_dihedral_restraint_group_conditionality = schema.ihm_derived_dihedral_restraint_group_conditionality
    ihm_derived_dihedral_restraint_group_conditionality.insert(rows, defaults=['ID', 'URI'])

# -----------------------------------
def add_rows_to_Vocab_ihm_derived_dihedral_restraint_restraint_type(catalog):

    rows =[
        {'Name': 'lower bound', 'Description': 'lower bound'},
        {'Name': 'upper bound', 'Description': 'upper bound'},
        {'Name': 'lower and upper bound', 'Description': 'lower and upper bound'},
        {'Name': 'harmonic', 'Description': 'harmonic'}
    ]

    pb = catalog.getPathBuilder()
    schema = pb.Vocab
    ihm_derived_dihedral_restraint_restraint_type = schema.ihm_derived_dihedral_restraint_restraint_type
    ihm_derived_dihedral_restraint_restraint_type.insert(rows, defaults=['ID', 'URI'])


# ============================================================
def main(server_name, catalog_id, credentials):
    server = DerivaServer('https', server_name, credentials)
    catalog = server.connect_ermrest(catalog_id)
    catalog.dcctx['cid'] = "oneoff/model"
    model = catalog.getCatalogModel()
    
    #-- clean up
    if False:
        drop_table(catalog, 'PDB', 'ihm_derived_dihedral_restraint') 
    
    # new changes
    if True:
        model = catalog.getCatalogModel()    
    
        #utils.create_table_if_not_exist(model, "Vocab",  utils.define_Vocab_table('ihm_derived_dihedral_restraint_group_conditionality', 'Conditionality of a group of dihedrals restrained together'))
        #utils.create_table_if_not_exist(model, "Vocab",  utils.define_Vocab_table('ihm_derived_dihedral_restraint_restraint_type', 'The type of dihedral restraint'))
        #add_rows_to_Vocab_ihm_derived_dihedral_restraint_group_conditionality(catalog)
        #add_rows_to_Vocab_ihm_derived_dihedral_restraint_restraint_type(catalog)
        utils.create_table_if_not_exist(model, "PDB",  define_tdoc_ihm_derived_dihedral_restraint())
        
    # vocab
    #if False:
    #    add_rows_to_Vocab_ihm_derived_dihedral_restraint_group_conditionality(catalog)
    #    add_rows_to_Vocab_ihm_derived_dihedral_restraint_restraint_type(catalog)
    

# ===================================================    

if __name__ == '__main__':
    args = BaseCLI("ad-hoc table creation tool", None, 1).parse_cli()
    credentials = get_credential(args.host, args.credential_file)
#    if args.catalog is None:
#        catalog_id = 99

    main(args.host, 99, credentials)
    
