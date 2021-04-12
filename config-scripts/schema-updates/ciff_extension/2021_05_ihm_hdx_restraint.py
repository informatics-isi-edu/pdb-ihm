import sys
import json
from deriva.core import ErmrestCatalog, AttrDict, get_credential, DEFAULT_CREDENTIAL_FILE, tag, urlquote, DerivaServer, get_credential, BaseCLI
from deriva.core.ermrest_model import builtin_types, Schema, Table, Column, Key, ForeignKey, DomainType, ArrayType
import utils


# ========================================================
# -- create a table that is not a Vocab structure
def define_tdoc_ihm_hdx_restraint():
    table_name='ihm_hdx_restraint'
    comment='Details of restraint derived from hydrogen-deuterium (H/D) exchange experiments; can be uploaded as CSV/TSV file above; mmCIF category: ihm_hdx_restraint'

    column_defs = [
        Column.define(
            "id",
            builtin_types.int8,
            comment='A unique id for the H/D exchange restraint',
            nullok=False
        ),
        Column.define(
            "feature_id",
            builtin_types.int8,
            comment='An identifier for the peptide / residue feature',
            nullok=False
        ),
        Column.define(
            "feature_RID",
            builtin_types.text,
            comment='Identifier to the feature RID',
            nullok=False
        ),
        Column.define(
            "protection_factor",
            builtin_types.float8,
            comment='The value of the protection factor determined from H/D exchange experiments',
            nullok=True
        ),
        Column.define(
            "dataset_list_id",
            builtin_types.int8,
            comment='Identifier to the H/D exchange input data from which the restraints are derived',
            nullok=False
        ),
        Column.define(
            "dataset_list_RID",
            builtin_types.text,
            comment='Identifier to the dataset list RID',
            nullok=False
        ),
        Column.define(
            "details",
            builtin_types.text,
            comment='Additional details regarding the H/D exchange restraint',
            nullok=True
        ),
        Column.define(
            "structure_id",
            builtin_types.text,
            comment='Structure identifier',
            nullok=False
        ),
        Column.define(
            "Entry_Related_File",
            builtin_types.text,
            comment='A reference to the uploaded restraint file in the table Entry_Related_File.id',
            nullok=True
        )
    ]
    key_defs = [
        Key.define(["structure_id", "id"], constraint_names=[["PDB", "ihm_hdx_restraint_primary_key"]] ),
        Key.define(["RID"], constraint_names=[["PDB", "ihm_hdx_restraint_RID_key"]] ),
    ]

    fkey_defs = [
        ForeignKey.define(["structure_id"], "PDB", "entry", ["id"],
                          constraint_names=[["PDB", "ihm_hdx_restraint_structure_id_fkey"]],
                          on_update="CASCADE",
                          on_delete="NO ACTION"
        ),
        ForeignKey.define(["feature_RID", "structure_id", "feature_id"], "PDB", "ihm_feature_list", ["RID", "structure_id", "feature_id"],
                          constraint_names=[["PDB", "ihm_hdx_restraint_ihm_feature_list_combo1_fkey"]],
                          on_update="CASCADE",
                          on_delete="NO ACTION"
        ),
        ForeignKey.define(["dataset_list_RID", "structure_id", "dataset_list_id"], "PDB", "ihm_dataset_list", ["RID", "structure_id", "id"],
                          constraint_names=[["PDB", "ihm_hdx_restraint_ihm_dataset_list_combo1_fkey"]],
                          on_update="CASCADE",
                          on_delete="NO ACTION"
        ),
        ForeignKey.define(["Entry_Related_File"], "PDB", "Entry_Related_File", ["RID"],
                          constraint_names=[["PDB", "ihm_hdx_restraint_Entry_Related_File_fkey"]],
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
def update_PDB_ihm_derived_distance_restraint(model):
    table = model.schemas['PDB'].tables['ihm_derived_distance_restraint']
    
    # -- add columns
    if 'distance_threshold_mean' not in table.columns.elements:
        table.create_column(
            Column.define(
                'distance_threshold_mean',
                builtin_types.float8,
                comment='The distance threshold mean applied to the restraint',
                nullok=True
            )
        )
    if 'distance_threshold_esd' not in table.columns.elements:
        table.create_column(
            Column.define(
                'distance_threshold_esd',
                builtin_types.float8,
                comment='The estimated standard deviation of the distance threshold applied to the restraint',
                nullok=True
            )
        )


# ==========================================================================
# upload vocab table



# ============================================================
def main(server_name, catalog_id, credentials):
    server = DerivaServer('https', server_name, credentials)
    catalog = server.connect_ermrest(catalog_id)
    catalog.dcctx['cid'] = "oneoff/model"
    model = catalog.getCatalogModel()

    
    #-- clean up
    create_table_if_not_exist(model, "PDB", define_tdoc_ihm_hdx_restraint())

    #update_PDB_ihm_derived_distance_restraint(model)
    

# ===================================================    

if __name__ == '__main__':
    args = BaseCLI("ad-hoc table creation tool", None, 1).parse_cli()
    credentials = get_credential(args.host, args.credential_file)
#    if args.catalog is None:
#        catalog_id = 99

    main(args.host, 99, credentials)
    
