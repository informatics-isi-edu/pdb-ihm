import sys
import json
from deriva.core import ErmrestCatalog, AttrDict, get_credential, DEFAULT_CREDENTIAL_FILE, tag, urlquote, DerivaServer, get_credential, BaseCLI
from deriva.core.ermrest_model import builtin_types, Schema, Table, Column, Key, ForeignKey, DomainType, ArrayType


# add table if not exist or update if exist
def create_table_if_not_exist(model, schema_name, tdoc):

    schema = model.schemas[schema_name]
    if tdoc["table_name"] not in schema.tables:
        schema.create_table(tdoc)


# add a column
def add_column(tdoc, schema_name, table_name, column_name, column_type, default_value, nullok):
    tdoc.table(schema_name, table_name).create_column(Column.define(column_name, column_type, default=default_value, nullok=nullok)) 

# create a foreign key
def create_fkey(tdoc, schema_name, table_name, column_name, reference_schema, reference_table, reference_column, constraint_name, on_update, on_delete):
    fkey_def = ForeignKey.define([column_name], reference_schema, reference_table, [reference_column], 
                                 on_update=on_update,
                                 on_delete=on_delete,
                                 constraint_names=[ [schema_name, constraint_name] ])
    tdoc.table(schema_name, table_name).create_fkey(fkey_def)

# remove a column
def remove_column_if_exist(tdoc, schema_name, table_name, column_name):
    if schema_name in tdoc.schemas.keys():
        schema = tdoc.schemas[schema_name]
        if table_name in schema.tables.keys():
            table = schema.tables[table_name]
            if column_name in table.column_definitions.elements.keys():
                column = table.column_definitions[column_name]
                column.drop()


# define a vocabulary table
def define_vocab_table(table_name, comment):
    column_defs = [
        Column.define(
            "ID",
            DomainType(
                {
                    "typename": "ermrest_curie",
                    "base_type": {
                      "typename": "text"
                    }
                }
            ),
            comment='The preferred Compact URI (CURIE) for this term.',                        
            nullok=False,
            default="PDB:{RID}"
        ),
        Column.define(
            "URI",
            DomainType(
                {
                    "typename": "ermrest_uri",
                    "base_type": {
                      "typename": "text"
                    }
                }
            ),
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
            DomainType(
                {
                    "typename": "markdown",
                    "base_type": {
                      "typename": "text"
                    }
                }
            ),
            nullok=False
        ),
        Column.define(
            "Synonyms",
            ArrayType(
                {
                    "typename": "text[]",
                    "base_type": {
                      "typename": "text"
                    }
                }
            ),
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
        comment=comment,
        provide_system=True
    )
    
    return table_def

# define ihm_pseudo_site table
def define_tdoc_ihm_pseudo_site():
    table_name='ihm_pseudo_site'
    comment='...'

    
    column_defs = [
        Column.define(
            "id",
            builtin_types.int8,
            comment='...',                        
            nullok=False
        ),
        Column.define(
            "Cartn_x",
            builtin_types.float8,
            nullok=False
        ),
        Column.define(
            "Cartn_y",
            builtin_types.float8,
            nullok=False
        ),
        Column.define(
            "Cartn_z",
            builtin_types.float8,
            nullok=False
        ),
        Column.define(
            "radius",
            builtin_types.float8,
            nullok=False
        ),
        Column.define(
            "description",
            builtin_types.text,
            nullok=True
        )
    ]
    
    key_defs = [
       Key.define(["id"],
                   constraint_names=[["PDB", "ihm_pseudo_site_id_key"]]
        )
    ]

    fkey_defs = [
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

# add rows to Vocab.ihm_cross_link_list_linker_type table
def add_rows_to_vocab_ihm_cross_link_list_linker_type(catalog):

    rows =[
        {'Name': 'CYS', 'Description': '...'},
        {'Name': 'BMSO', 'Description': '...'},
        {'Name': 'DHSO', 'Description': '...'}
        ]
            
    pb = catalog.getPathBuilder()
    schema = pb.Vocab
    ihm_cross_link_list_linker_type = schema.ihm_cross_link_list_linker_type
    ihm_cross_link_list_linker_type.insert(rows)

# add rows to Vocab.pseudo_site_flag table
def add_rows_to_vocab_pseudo_site_flag(catalog):

    rows =[
        {'Name': 'Yes', 'Description': '...'},
        {'Name': 'No', 'Description': '...'}
        ]
            
    pb = catalog.getPathBuilder()
    schema = pb.Vocab
    pseudo_site_flag = schema.pseudo_site_flag
    pseudo_site_flag.insert(rows)

def main(server_name, catalog_id, credentials):
    server = DerivaServer('https', server_name, credentials)
    catalog = server.connect_ermrest(catalog_id)
    catalog.dcctx['cid'] = "oneoff/model"
    model = catalog.getCatalogModel()
    
    """
    Add rows to the Vocab.ihm_cross_link_list_linker_type table
    """
    add_rows_to_vocab_ihm_cross_link_list_linker_type(catalog)
    
    """
    Create the PDBihm_pseudo_site table
    """
    create_table_if_not_exist(model, "PDB",  define_tdoc_ihm_pseudo_site())
    
    """
    Add the PDB.ihm_pseudo_site_feature.pseudo_site_id column
    """
    add_column(model, 'PDB', 'ihm_pseudo_site_feature', 'pseudo_site_id', builtin_types.int8, None, True)
    
    """
    Create the foreign key PDB.ihm_pseudo_site_feature.pseudo_site_id references PDB.ihm_pseudo_site.id
    """
    create_fkey(model,
                'PDB', 'ihm_pseudo_site_feature', 'pseudo_site_id', 
                'PDB', 'ihm_pseudo_site', 'id', 
                'ihm_pseudo_site_feature_pseudo_site_id_fkey', 'CASCADE', 'SET NULL')
    
    """
    Remove columns from the PDB.ihm_pseudo_site_feature table
    """
    remove_column_if_exist(model, 'PDB', 'ihm_pseudo_site_feature', 'Cartn_x')
    remove_column_if_exist(model, 'PDB', 'ihm_pseudo_site_feature', 'Cartn_y')
    remove_column_if_exist(model, 'PDB', 'ihm_pseudo_site_feature', 'Cartn_z')
    remove_column_if_exist(model, 'PDB', 'ihm_pseudo_site_feature', 'radius')
    remove_column_if_exist(model, 'PDB', 'ihm_pseudo_site_feature', 'description')
    
    """
    Create the vocabulary table pseudo_site_flag
    """
    create_table_if_not_exist(model, "Vocab",  define_vocab_table('pseudo_site_flag', '...'))
    
    """
    Add rows to the Vocab.pseudo_site_flag table
    """
    add_rows_to_vocab_pseudo_site_flag(catalog)
    
    """
    Add the PDB.ihm_cross_link_restraint.pseudo_site_flag column
    """
    add_column(model, 'PDB', 'ihm_cross_link_restraint', 'pseudo_site_flag', builtin_types.text, None, True)

    """
    Create the foreign key PDB.ihm_cross_link_restraint.pseudo_site_flag references Vocab.pseudo_site_flag.Name
    """
    create_fkey(model,
                'PDB', 'ihm_cross_link_restraint', 'pseudo_site_flag', 
                'Vocab', 'pseudo_site_flag', 'Name', 
                'ihm_cross_link_restraint_pseudo_site_flag__Name_fkey', 'CASCADE', 'SET NULL')


# ===================================================    

if __name__ == '__main__':
    args = BaseCLI("ad-hoc table creation tool", None, 1).parse_cli()
    credentials = get_credential(args.host, args.credential_file)
#    if args.catalog is None:
#        catalog_id = 99

    main(args.host, 99, credentials)
    
