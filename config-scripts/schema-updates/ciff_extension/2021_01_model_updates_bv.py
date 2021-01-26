import sys
import json
from deriva.core import ErmrestCatalog, AttrDict, get_credential, DEFAULT_CREDENTIAL_FILE, tag, urlquote, DerivaServer, get_credential, BaseCLI
from deriva.core.ermrest_model import builtin_types, Schema, Table, Column, Key, ForeignKey, DomainType, ArrayType

# ========================================================
# utility

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
    comment='Details of pseudo sites that may be used in the restraints or model representation'

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
            "structure_id",
            builtin_types.text,
            comment='Structure identifier',
            nullok=False
        )
    ]
    
    key_defs = [
        Key.define(["id"], constraint_names=[["PDB", "ihm_pseudo_site_id_key"]] ),
        Key.define(["RID"], constraint_names=[["PDB", "ihm_pseudo_site_RID_key"]] ),        
    ]

    # @brinda: add fk pseudo-definition
    fkey_defs = [
        ForeignKey.define(["structure_id"], "PDB", "entry", ["id"],
                          constraint_names=[["PDB", "ihm_pseudo_site_structure_id_fkey"]],
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
    #table = model('PDB', 'ihm_pseudo_site_feature')
    table = model.schemas['PDB'].tables['ihm_pseudo_site_feature']
    
    # -- Remove columns from the PDB.ihm_pseudo_site_feature table
    remove_column_if_exist(model, 'PDB', 'ihm_pseudo_site_feature', 'Cartn_x')
    remove_column_if_exist(model, 'PDB', 'ihm_pseudo_site_feature', 'Cartn_y')
    remove_column_if_exist(model, 'PDB', 'ihm_pseudo_site_feature', 'Cartn_z')
    remove_column_if_exist(model, 'PDB', 'ihm_pseudo_site_feature', 'radius')
    remove_column_if_exist(model, 'PDB', 'ihm_pseudo_site_feature', 'description')
    
    # -- add columns
    #if table.columns['pseudo_site_id']==None:   #@serban to review
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
    #if table.foreign_keys[(model.schemas['PDB'],'ihm_pseudo_site_feature_pseudo_site_id_fkey')]==None: #@serban to review
    if (model.schemas['PDB'],'ihm_pseudo_site_feature_pseudo_site_id_fkey') not in table.foreign_keys.elements:
        table.create_fkey(
            ForeignKey.define(["pseudo_site_id"], "PDB", "ihm_pseudo_site", ["id"],
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

# ============================================================
def main(server_name, catalog_id, credentials):
    server = DerivaServer('https', server_name, credentials)
    catalog = server.connect_ermrest(catalog_id)
    catalog.dcctx['cid'] = "oneoff/model"
    model = catalog.getCatalogModel()

    # -- create tables from scratch
    create_table_if_not_exist(model, "PDB",  define_tdoc_ihm_pseudo_site())
    create_table_if_not_exist(model, "Vocab",  define_Vocab_table('pseudo_site_flag', 'Flag for crosslinks involving pseudo sites'))
    
    # -- update existing tables
    update_PDB_ihm_pseudo_site_feature(model)
    update_PDB_ihm_cross_link_restraint(model)
    
    # -- data manipulation
    #add_rows_to_Vocab_ihm_cross_link_list_linker_type(catalog)
    add_rows_to_Vocab_pseudo_site_flag(catalog)
    
# ===================================================    

if __name__ == '__main__':
    args = BaseCLI("ad-hoc table creation tool", None, 1).parse_cli()
    credentials = get_credential(args.host, args.credential_file)
#    if args.catalog is None:
#        catalog_id = 99

    main(args.host, 99, credentials)
    
