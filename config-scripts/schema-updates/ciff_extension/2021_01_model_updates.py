import sys
import json
from deriva.core import ErmrestCatalog, AttrDict, get_credential, DEFAULT_CREDENTIAL_FILE, tag, urlquote, DerivaServer, get_credential, BaseCLI
from deriva.core.ermrest_model import builtin_types, Schema, Table, Column, Key, ForeignKey, DomainType, ArrayType

# ========================================================
# utility

# drop a table together with the associated reference keys
def drop_table(model, schema_name, table_name):
    if schema_name in model.schemas.keys():
        schema = model.schemas[schema_name]
        if table_name in schema.tables:
            table = model.schemas[schema_name].tables[table_name]
            for foreign_key in table.referenced_by:
                foreign_key.drop()
            table.drop()


# create a vocabulary table if it does not exixt
def create_vocabulary_table_if_not_exist(model, schema_name, table_name, comment):

    schema = model.schemas[schema_name]
    if table_name not in schema.tables:
        schema.create_table(Table.define_vocabulary(table_name, 'PDB:{RID}', comment=comment))

# add table if not exist or update if exist
def create_table_if_not_exist(model, schema_name, tdoc):

    schema = model.schemas[schema_name]
    if tdoc["table_name"] not in schema.tables:
        schema.create_table(tdoc)

# ---------------------------------------
# add a column
# HT: recommend delete this function as it is doesn't add any value and harder to read
def add_column(model, schema_name, table_name, column_name, column_type, default_value, nullok):
    model.table(schema_name, table_name).create_column(Column.define(column_name, column_type, default=default_value, nullok=nullok)) 

# create a foreign key
# HT: recommend delete this function as it is doesn't add any value and harder to read. This is also incomplete as it doesn't support composite-fks    
def add_fkey(model, schema_name, table_name, column_name, reference_schema, reference_table, reference_column, constraint_name, on_update, on_delete):
    fkey_def = ForeignKey.define([column_name], reference_schema, reference_table, [reference_column], 
                                 on_update=on_update,
                                 on_delete=on_delete,
                                 constraint_names=[ [schema_name, constraint_name] ])
    model.table(schema_name, table_name).create_fkey(fkey_def)

# ---------------------------------------
# remove a column
def remove_column_if_exist(model, schema_name, table_name, column_name):
    if table_name in model.schemas[schema_name].tables:
        table = model.schemas[schema_name].tables[table_name]
        if column_name in table.columns.elements:
            #table[column_name].drop()
            table.column_definitions[column_name].drop()
            print("Dropped column %s.%s.%s" % (schema_name, table_name, column_name))

# ---------------------------------------
# define a vocabulary table (with specific structure)
def define_Vocab_table(table_name, table_comment):
    column_defs = [
        Column.define(
            "ID",
            builtin_types.ermrest_curie,
            comment='The preferred Compact URI (CURIE) for this term.',                        
            nullok=False,
            default="PDB:{RID}"
        ),
        Column.define(
            "URI",
            builtin_types.ermrest_uri,            
            nullok=False,
            default="/id/{RID}",
            comment="The preferred URI for this term."
        ),
        Column.define(
            "Name",
            builtin_types.text,
            nullok=False
        ),
        Column.define(
            "Description",
            builtin_types.markdown,
            nullok=False
        ),
        Column.define(
            "Synonyms",
            builtin_types["text[]"],
            nullok=True,
            comment="Alternate human-readable names for this term."
        ),
        Column.define(
            "Owner",
            builtin_types.text,
            comment='Group that can update the record.',                        
            nullok=True
        )
    ]
    
    key_defs = [
        Key.define(["URI"],
                   constraint_names=[["Vocab", '{}_URI_key'.format(table_name)]]
        ),
        Key.define(["Name"],
                   constraint_names=[["Vocab", '{}_Name_key'.format(table_name)]]
        ),
        Key.define(["ID"],
                   constraint_names=[["Vocab", '{}_ID_key'.format(table_name)]]
        ),
        Key.define(["RID"],
                   constraint_names=[["Vocab", '{}_RID_key'.format(table_name)]]
        )
    ]

    fkey_defs = [
        ForeignKey.define(["RCB"], "public", "ERMrest_Client", ["ID"],
                          constraint_names=[["Vocab", '{}_RCB_fkey'.format(table_name)]],
                          on_update="NO ACTION",
                          on_delete="NO ACTION"   
        ),
        ForeignKey.define(["RMB"], "public", "ERMrest_Client", ["ID"],
                          constraint_names=[["Vocab", '{}_RMB_fkey'.format(table_name)]],
                          on_update="NO ACTION",
                          on_delete="NO ACTION"   
        ),
        ForeignKey.define(["Owner"], "public", "Catalog_Group", ["ID"],
                          constraint_names=[["Vocab", '{}_Owner_fkey'.format(table_name)]],
                          on_update="NO ACTION",
                          on_delete="NO ACTION"   
        )
    ]

    table_def = Table.define(
        table_name,
        column_defs,
        key_defs=key_defs,
        fkey_defs=fkey_defs,
        comment=table_comment,
        provide_system=True
    )
    
    return table_def

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
    
    key_defs = [
        Key.define(["structure_id", "id"], constraint_names=[["PDB", "ihm_pseudo_site_primary_key"]] ),
        Key.define(["RID"], constraint_names=[["PDB", "ihm_pseudo_site_RID_key"]] ),        
    ]

    # @brinda: add fk pseudo-definition
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

#====================================================
def define_tdoc_ihm_cross_link_pseudo_site():
    table_name='ihm_cross_link_pseudo_site'
    comment='Details of pseudo sites involved in crosslinks; can be uploaded as CSV/TSV file above; mmCIF category: ihm_cross_link_pseudo_site'

    column_defs = [
        Column.define(
            "id",
            builtin_types.int8,
            comment='An identifier for a pseudo site involved in a crosslink',
            nullok=False
        ),
        Column.define(
            "restraint_id",
            builtin_types.int8,
            comment='An identifier for the crosslink restraint between a pair of residues',
            nullok=False
        ),
        Column.define(
            "cross_link_partner",
            builtin_types.text,
            comment='The identity of the crosslink partner corresponding to the pseudo site',
            nullok=False
        ),
        Column.define(
            "pseudo_site_id",
            builtin_types.int8,
            comment='The pseudo site identifier corresponding to the crosslink partner',
            nullok=False
        ),
        Column.define(
            "model_id",
            builtin_types.int8,
            comment='Identifier to the model that the pseudo site corresponds to',
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
        ),
        # HT: to use for Chaise
        Column.define(
            "Model_RID",
            builtin_types.text,
            comment='Identifier to the model RID',
            nullok=True
        )
    ]

    key_defs = [
        Key.define(["structure_id", "id"], constraint_names=[["PDB", "ihm_cross_link_pseudo_site_primary_key"]] ),
        Key.define(["RID"], constraint_names=[["PDB", "ihm_cross_link_pseudo_site_RID_key"]] ),
    ]

    # @brinda: add fk pseudo-definition
    fkey_defs = [
        # HT: it own fk to Entry table
        ForeignKey.define(["structure_id"], "PDB", "entry", ["id"],
                          constraint_names=[["PDB", "ihm_cross_link_pseudo_site_structure_id_fkey"]],
                          on_update="CASCADE",
                          on_delete="NO ACTION"
        ),
        # -- begin ihm_cross_link_restraint
        # HT: In annotation, apply domain_filter to filter the RID list by constraining structure_id        
        ForeignKey.define(["structure_id", "restraint_id"], "PDB", "ihm_cross_link_restraint", ["structure_id", "id"],
                          constraint_names=[["PDB", "ihm_cross_link_pseudo_site_restraint_id_fkey"]],
                          on_update="CASCADE",
                          on_delete="NO ACTION"
        ),
        # -- end ihm_cross_link_restraint         
        # -- begin ihm_model_list table
        # HT: This is for chaise optional foreign key --> check naming convention
        # HT: In annotation, apply domain_filter to filter the RID list by constraining structure_id
        ForeignKey.define(["Model_RID"], "PDB", "ihm_model_list", ["RID"],
                          constraint_names=[["PDB", "ihm_cross_link_pseudo_site_Model_RID_fkey"]],
                          on_update="CASCADE",
                          on_delete="NO ACTION"
        ),
        # HT: equivalent fk so that Chaise will automatically fill in automatically --> check constraint naming convention
        ForeignKey.define(["Model_RID", "model_id"], "PDB", "ihm_model_list", ["RID", "id"],
                          constraint_names=[["PDB", "ihm_cross_link_pseudo_site_Model_RID_model_id_denorm_fkey"]],
                          on_update="CASCADE",
                          on_delete="NO ACTION"
        ),
        # -- end ihm_model_list table
        ForeignKey.define(["structure_id", "pseudo_site_id"], "PDB", "ihm_pseudo_site", ["structure_id", "id"],
                          constraint_names=[["PDB", "ihm_cross_link_pseudo_site_pseudo_site_id_fkey"]],
                          on_update="CASCADE",
                          on_delete="NO ACTION"
        ),
        ForeignKey.define(["cross_link_partner"], "Vocab", "cross_link_partner", ["Name"],
                          constraint_names=[ ["Vocab", "ihm_cross_link_pseudo_site_cross_link_partner_fkey"] ],
                          on_update="CASCADE",
                          on_delete="NO ACTION"
        ),
        ForeignKey.define(["Entry_Related_File"], "PDB", "Entry_Related_File", ["RID"],
                          constraint_names=[["PDB", "ihm_cross_link_pseudo_site_Entry_Related_File_fkey"]],
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

#====================================================
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
        )
    ]

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
        ForeignKey.define(["structure_id", "ensemble_id"], "PDB", "ihm_ensemble_info", ["structure_id", "ensemble_id"],
                          constraint_names=[["PDB", "ihm_ensemble_sub_sample_ensemble_id_fkey"]],
                          on_update="CASCADE",
                          on_delete="NO ACTION"
        ),
        ForeignKey.define(["structure_id", "model_group_id"], "PDB", "ihm_model_group", ["structure_id", "id"],
                          constraint_names=[["PDB", "ihm_ensemble_sub_sample_model_group_id_fkey"]],
                          on_update="CASCADE",
                          on_delete="NO ACTION"
        ),
        ForeignKey.define(["structure_id", "file_id"], "PDB", "ihm_external_files", ["structure_id", "id"],
                          constraint_names=[["PDB", "ihm_ensemble_sub_sample_file_id_fkey"]],
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

# ===================================================
# update existing table

def update_PDB_ihm_pseudo_site_feature(model):
    table = model.schemas['PDB'].tables['ihm_pseudo_site_feature']
    
    # -- Remove columns from the PDB.ihm_pseudo_site_feature table
    remove_column_if_exist(model, 'PDB', 'ihm_pseudo_site_feature', 'Cartn_x')
    remove_column_if_exist(model, 'PDB', 'ihm_pseudo_site_feature', 'Cartn_y')
    remove_column_if_exist(model, 'PDB', 'ihm_pseudo_site_feature', 'Cartn_z')
    remove_column_if_exist(model, 'PDB', 'ihm_pseudo_site_feature', 'radius')
    remove_column_if_exist(model, 'PDB', 'ihm_pseudo_site_feature', 'description')

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
    # -- add fk
    # Create the foreign key PDB.ihm_pseudo_site_feature.pseudo_site_id references PDB.ihm_pseudo_site.id
    if (model.schemas['PDB'],'ihm_pseudo_site_feature_pseudo_site_id_fkey') not in table.foreign_keys.elements:
        table.create_fkey(
            ForeignKey.define(["structure_id", "pseudo_site_id"], "PDB", "ihm_pseudo_site", ["structure_id","id"],
                            constraint_names=[ ["PDB", "ihm_pseudo_site_feature_pseudo_site_id_fkey"] ],
                            on_update="CASCADE",
                            on_delete="NO ACTION")  # won't allow delete until there is no reference
        )

# ---------------
def update_PDB_ihm_cross_link_restraint(model):
    #table = model("PDB", "ihm_cross_link_restraint")
    table = model.schemas['PDB'].tables['ihm_cross_link_restraint']
    
    # Add the PDB.ihm_cross_link_restraint.pseudo_site_flag column    
    table.create_column(
        Column.define(
            "pseudo_site_flag",
            builtin_types.text,
            comment='A flag indicating if the cross link involves a pseudo site that is not part of the model representation',
            nullok=True
        )
    )

    # Create the foreign key PDB.ihm_cross_link_restraint.pseudo_site_flag references Vocab.pseudo_site_flag.Name
    table.create_fkey(
        ForeignKey.define(["pseudo_site_flag"], "Vocab", "pseudo_site_flag", ["Name"],
                          constraint_names=[ ["Vocab", "ihm_cross_link_restraint_pseudo_site_flag_fkey"] ],
                          on_update="CASCADE",
                          on_delete="NO ACTION")
    )

# ---------------
def update_PDB_ihm_ensemble_info(model):
    table = model.schemas['PDB'].tables['ihm_ensemble_info']

    # Add the PDB.ihm_ensemble_info.sub_sample_flag and PDB.ihm_ensemble_info.sub_sampling_type columns   
    table.create_column(
        Column.define(
            "sub_sample_flag",
            builtin_types.text,
            comment='A flag that indicates whether the ensemble consists of sub samples',
            nullok=True
        )
    )
    table.create_column(
        Column.define(
            "sub_sampling_type",
            builtin_types.text,
            comment='Type of sub sampling',
            nullok=True
        )
    )

    # Create the foreign keys
    table.create_fkey(
        ForeignKey.define(["sub_sample_flag"], "Vocab", "sub_sample_flag", ["Name"],
                          constraint_names=[ ["Vocab", "ihm_ensemble_info_sub_sample_flag_fkey"] ],
                          on_update="CASCADE",
                          on_delete="NO ACTION")
        )
    table.create_fkey(
        ForeignKey.define(["sub_sampling_type"], "Vocab", "sub_sampling_type", ["Name"],
                          constraint_names=[ ["Vocab", "ihm_ensemble_info_sub_sampling_type_fkey"] ],
                          on_update="CASCADE",
                          on_delete="NO ACTION")
    )

# ---------------
def update_PDB_ihm_model_list(model):
    table = model.schemas['PDB'].tables['ihm_model_list']
    
    # create additional keys --> check key naming convention
    table.create_key(    
        Key.define(["RID", "id"], constraint_names=[["PDB", "ihm_model_list_rid_id_denorm_key"]] )
    )

# ========================================================
# add rows to Vocab.ihm_cross_link_list_linker_type table
def add_rows_to_Vocab_ihm_cross_link_list_linker_type(catalog):

    rows =[
        {'Name': 'CYS', 'Description': 'CYS'},
        {'Name': 'BMSO', 'Description': 'BMSO'},
        {'Name': 'DHSO', 'Description': 'DHSO'}
    ]
    
    pb = catalog.getPathBuilder()
    schema = pb.Vocab
    ihm_cross_link_list_linker_type = schema.ihm_cross_link_list_linker_type
    ihm_cross_link_list_linker_type.insert(rows, defaults=['ID', 'URI'])

# -----------------------------------
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

# -----------------------------------
# add rows to Vocab.cross_link_partner
def add_rows_to_Vocab_cross_link_partner(catalog):    #@serban to review

    rows =[
        {'Name': '1', 'Description': 'The first partner in the crosslink as identified in the ihm_cross_link_restraint table'},
        {'Name': '2', 'Description': 'The second partner in the crosslink as identified in the ihm_cross_link_restraint table'}
    ]

    pb = catalog.getPathBuilder()
    schema = pb.Vocab
    cross_link_partner = schema.cross_link_partner
    cross_link_partner.insert(rows, defaults=['ID', 'URI'])

#=============================================================
def update_table_comments(model):

    model.table("PDB", "ihm_pseudo_site").comment = "Details of pseudo sites that may be used in the restraints or model representation; can be uploaded as CSV/TSV file above; mmCIF category: ihm_pseudo_site"
    
# ============================================================
def main(server_name, catalog_id, credentials):
    server = DerivaServer('https', server_name, credentials)
    catalog = server.connect_ermrest(catalog_id)
    catalog.dcctx['cid'] = "oneoff/model"
    model = catalog.getCatalogModel()

    #--Drop tables
    drop_table(model, 'PDB', 'ihm_pseudo_site')
    
    #model.schemas['PDB'].tables['ihm_pseudo_site'].drop()
    #model.schemas['PDB'].tables['ihm_cross_link_pseudo_site'].drop()
    #model.schemas['PDB'].tables['ihm_ensemble_sub_sample'].drop()

    #model = catalog.getCatalogModel()         #Reload the model to create table after drop - bug

    # -- create tables from scratch
    #create_table_if_not_exist(model, "Vocab",  define_Vocab_table('cross_link_partner', 'Identity of the crosslink partner'))
    #create_table_if_not_exist(model, "Vocab",  define_Vocab_table('sub_sample_flag', 'Flag for ensembles consisting of sub samples'))
    #create_table_if_not_exist(model, "Vocab",  define_Vocab_table('sub_sampling_type', 'Types of sub samples in ensembles'))
    #create_table_if_not_exist(model, "PDB",  define_tdoc_ihm_pseudo_site())
    #create_table_if_not_exist(model, "Vocab",  define_Vocab_table('pseudo_site_flag', 'Flag for crosslinks involving pseudo sites'))
    #create_table_if_not_exist(model, "PDB",  define_tdoc_ihm_ensemble_sub_sample())
    #create_table_if_not_exist(model, "PDB",  define_tdoc_ihm_cross_link_pseudo_site())

    # -- update existing tables
    #update_PDB_ihm_pseudo_site_feature(model)
    #update_PDB_ihm_cross_link_restraint(model)
    #update_PDB_ihm_ensemble_info(model)

    # -- data manipulation
    #add_rows_to_Vocab_ihm_cross_link_list_linker_type(catalog)
    #add_rows_to_Vocab_pseudo_site_flag(catalog)
    #add_rows_to_Vocab_sub_sample_flag(catalog)
    #add_rows_to_Vocab_sub_sampling_type(catalog)
    #add_rows_to_Vocab_cross_link_partner(catalog)
    
    # -- Update table comments
    #update_table_comments(model)
    #model.apply()

# ===================================================    

if __name__ == '__main__':
    args = BaseCLI("ad-hoc table creation tool", None, 1).parse_cli()
    credentials = get_credential(args.host, args.credential_file)
#    if args.catalog is None:
#        catalog_id = 99

    main(args.host, 99, credentials)
    
