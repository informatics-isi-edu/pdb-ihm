import sys
import json
from deriva.core import ErmrestCatalog, AttrDict, get_credential, DEFAULT_CREDENTIAL_FILE, tag, urlquote, DerivaServer, get_credential, BaseCLI
from deriva.core.ermrest_model import builtin_types, Schema, Table, Column, Key, ForeignKey, DomainType, ArrayType
import utils


# ========================================================
# -- create a table that is not a Vocab structure
# -- define ihm_pseudo_site table --> Brida reviewed
def define_tdoc_ihm_pseudo_site():
    table_name='ihm_pseudo_site'
    comment='Details of pseudo sites that may be used in the restraints or model representation; can be uploaded as CSV/TSV file above; mmCIF category: ihm_pseudo_site'

    column_defs = [
        Column.define(
            "id",
            builtin_types.int8,
            comment='An identifier to the pseudo site',                        
            nullok=False
        ),
        Column.define(
            "Cartn_x",
            builtin_types.float8,
            comment='Cartesian X component corresponding to this pseudo site',
            nullok=False
        ),
        Column.define(
            "Cartn_y",
            builtin_types.float8,
            comment='Cartesian Y component corresponding to this pseudo site',
            nullok=False
        ),
        Column.define(
            "Cartn_z",
            builtin_types.float8,
            comment='Cartesian Z component corresponding to this pseudo site',
            nullok=False
        ),
        Column.define(
            "radius",
            builtin_types.float8,
            comment='Radius associated with the pseudo site',
            nullok=True
        ),
        Column.define(
            "description",
            builtin_types.text,
            comment='Additional description about the pseudo site',
            nullok=True
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
        )
    ]
    #BV: This is a parent table with mandatory columns in the child table; so combo1 key is defined
    key_defs = [
        Key.define(["structure_id", "id"], constraint_names=[["PDB", "ihm_pseudo_site_primary_key"]] ),
        Key.define(["RID"], constraint_names=[["PDB", "ihm_pseudo_site_RID_key"]] ),        
        Key.define(["RID", "structure_id", "id"], constraint_names=[["PDB", "ihm_pseudo_site_combo1_key"]] )
    ]

    # @brinda: add fk pseudo-definition
    #BV: No outgoing fkeys other than structure_id and Entry_Related_File
    fkey_defs = [
        ForeignKey.define(["structure_id"], "PDB", "entry", ["id"],
                          constraint_names=[["PDB", "ihm_pseudo_site_structure_id_fkey"]],
                          on_update="CASCADE",
                          on_delete="NO ACTION"   
        ),
        ForeignKey.define(["Entry_Related_File"], "PDB", "Entry_Related_File", ["RID"],
                          constraint_names=[["PDB", "ihm_pseudo_site_Entry_Related_File_fkey"]],
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
def update_PDB_ihm_feature_list(model):
    table = model.schemas['PDB'].tables['ihm_feature_list']

    if table.key_by_columns(["RID", "structure_id", "feature_id"], raise_nomatch=False) is None:
        table.create_key(   
            Key.define(["RID", "structure_id", "feature_id"], constraint_names=[["PDB", "ihm_feature_list_combo1_key"]] )
        )
    

# ---------------
def undo_update_PDB_ihm_feature_list(model):
    drop_key_if_exist(model, 'PDB', 'ihm_feature_list', "ihm_feature_list_combo1_key")


# --------------------------------------------------------------
def update_PDB_ihm_pseudo_site_feature(model):
    table = model.schemas['PDB'].tables['ihm_pseudo_site_feature']

    # Drop fkeys
    if (model.schemas['PDB'],'ihm_pseudo_site_feature_feature_id_fkey') in table.foreign_keys.elements:
        table.foreign_keys[(model.schemas['PDB'], 'ihm_pseudo_site_feature_feature_id_fkey')].drop()
        
        # -- Remove columns from the PDB.ihm_pseudo_site_feature table
    drop_column_if_exist(model, 'PDB', 'ihm_pseudo_site_feature', 'Cartn_x')
    drop_column_if_exist(model, 'PDB', 'ihm_pseudo_site_feature', 'Cartn_y')
    drop_column_if_exist(model, 'PDB', 'ihm_pseudo_site_feature', 'Cartn_z')
    drop_column_if_exist(model, 'PDB', 'ihm_pseudo_site_feature', 'radius')
    drop_column_if_exist(model, 'PDB', 'ihm_pseudo_site_feature', 'description')
    
    # -- add columns
    if 'pseudo_site_id' not in table.columns.elements:
        table.create_column(
            Column.define(
                'pseudo_site_id',
                builtin_types.int8,
                comment='Pseudo site identifier corresponding to this feature',
                nullok=False
            )
        )
    if 'pseudo_site_RID' not in table.columns.elements:
        table.create_column(
            Column.define(
                'pseudo_site_RID',
                builtin_types.text,
                comment='Identifier to the pseudo site RID',
                nullok=False
            )
        )

    if 'feature_RID' not in table.columns.elements:
        table.create_column(
            Column.define(
                'feature_RID',
                builtin_types.text,
                comment='Identifier to the feature RID',
                nullok=False
            )
        )

    # -- add fk
    # Create the foreign key PDB.ihm_pseudo_site_feature.pseudo_site_id references PDB.ihm_pseudo_site.id
    if (model.schemas['PDB'], 'ihm_pseudo_site_feature_ihm_pseudo_site_combo1_fkey') not in table.foreign_keys.elements:
        table.create_fkey(
            ForeignKey.define(["pseudo_site_RID", "structure_id", "pseudo_site_id"], "PDB", "ihm_pseudo_site", ["RID", "structure_id", "id"],
                            constraint_names=[ ["PDB", "ihm_pseudo_site_feature_ihm_pseudo_site_combo1_fkey"] ],
                            on_update="CASCADE",
                            on_delete="NO ACTION")  # won't allow delete until there is no reference
        )

    if (model.schemas['PDB'],'ihm_pseudo_site_feature_ihm_feature_list_combo1_fkey') not in table.foreign_keys.elements:
        table.create_fkey(
            ForeignKey.define(["feature_RID", "structure_id", "feature_id"], "PDB", "ihm_feature_list", ["RID", "structure_id", "feature_id"],
                            constraint_names=[ ["PDB", "ihm_pseudo_site_feature_ihm_feature_list_combo1_fkey"] ],
                            on_update="CASCADE",
                            on_delete="NO ACTION")  # won't allow delete until there is no reference
        )


def undo_update_PDB_ihm_pseudo_site_feature(model):
    drop_column_if_exist(model, 'PDB', 'ihm_pseudo_site_feature', 'pseudo_site_id')    
    drop_column_if_exist(model, 'PDB', 'ihm_pseudo_site_feature', 'pseudo_site_RID')
    drop_column_if_exist(model, 'PDB', 'ihm_pseudo_site_feature', 'feature_RID')    

    drop_fkey_if_exist(model, 'PDB', 'ihm_pseudo_site_feature', "ihm_pseudo_site_feature_ihm_pseudo_site_combo1_fkey")
    drop_fkey_if_exist(model, 'PDB', 'ihm_pseudo_site_feature', "ihm_pseudo_site_feature_ihm_feature_list_combo1_fkey")

# ==========================================================================
# update all relevant comments

def update_comments(model):
    model.table("PDB", "ihm_pseudo_site").comment = "Details of pseudo sites that may be used in the restraints or model representation; can be uploaded as CSV/TSV file above; mmCIF category: ihm_pseudo_site"
    model.apply()
    


# ==========================================================================
# upload vocab table


# add rows to Vocab.pseudo_site_flag table
def add_rows_to_Vocab_pseudo_site_flag(catalog):    #@serban to review

    rows =[
        {'Name': 'Yes', 'Description': 'Crosslink involves a pseudo site'},
        {'Name': 'No', 'Description': 'Crosslink does not involve a pseudo site'}
    ]
            
    pb = catalog.getPathBuilder()
    schema = pb.Vocab
    pseudo_site_flag = schema.pseudo_site_flag
    pseudo_site_flag.insert(rows, defaults=['ID', 'URI'])

# ============================================================
def main(server_name, catalog_id, credentials):
    server = DerivaServer('https', server_name, credentials)
    catalog = server.connect_ermrest(catalog_id)
    catalog.dcctx['cid'] = "oneoff/model"
    model = catalog.getCatalogModel()

    #-- undo model eveolution to mimic the initial states
    if False:
        # undo update
        undo_update_PDB_ihm_feature_list(model)    
        undo_update_PDB_ihm_pseudo_site_feature(model)
        
        # drop table
        # drop_table(catalog, 'PDB', 'ihm_pseudo_site')
        model.schemas['PDB'].tables['ihm_pseudo_site'].drop()
    
    # new changes
    model = catalog.getCatalogModel()    
    if True:
        create_table_if_not_exist(model, "PDB",  define_tdoc_ihm_pseudo_site())
        create_table_if_not_exist(model, "Vocab",  define_Vocab_table('pseudo_site_flag', 'Flag for crosslinks involving pseudo sites'))
        
        update_PDB_ihm_feature_list(model)    
        update_PDB_ihm_pseudo_site_feature(model)
        
        update_comments(model)        
      
    # -- vocab
    if False:
        add_rows_to_Vocab_pseudo_site_flag(catalog)



# ===================================================    

if __name__ == '__main__':
    args = BaseCLI("ad-hoc table creation tool", None, 1).parse_cli()
    credentials = get_credential(args.host, args.credential_file)
#    if args.catalog is None:
#        catalog_id = 99

    main(args.host, 99, credentials)
    
