import sys
import json
from deriva.core import ErmrestCatalog, AttrDict, get_credential, DEFAULT_CREDENTIAL_FILE, tag, urlquote, DerivaServer, get_credential, BaseCLI
from deriva.core.ermrest_model import builtin_types, Schema, Table, Column, Key, ForeignKey, DomainType, ArrayType

class ApplicationClient (BaseCLI):
    def __init__(self, description, epilog, version=None, hostname_required=False, config_file_required=False):
        if version == None:
            super(ApplicationClient, self).__init__(description, epilog, hostname_required, config_file_required)
        else:
            super(ApplicationClient, self).__init__(description, epilog, version, hostname_required, config_file_required)
        self.parser.add_argument('--catalog_id', action='store', type=int, required=True, help='The catalog number.')

# ========================================================
# utility

# set nullok for a column
def set_default_column_if_exists(model, schema_name, table_name, column_name, default_value):
    if schema_name in model.schemas.keys():
        schema = model.schemas[schema_name]
        if table_name in schema.tables:
            table = model.schemas[schema_name].tables[table_name]
            if column_name in table.column_definitions.elements:
                table.column_definitions[column_name].alter(default=default_value)
                print('Set default={} in column {}:{}:{}'.format(default_value, schema_name, table_name, column_name))

def set_nullok_column_if_exists(model, schema_name, table_name, column_name, nullok):
    if schema_name in model.schemas.keys():
        schema = model.schemas[schema_name]
        if table_name in schema.tables:
            table = model.schemas[schema_name].tables[table_name]
            if column_name in table.column_definitions.elements:
                table.column_definitions[column_name].alter(nullok=nullok)
                print('Set nullok={} in column {}:{}:{}'.format(nullok, schema_name, table_name, column_name))

# rename a table
def rename_table_if_exists(model, schema_name, table_name, new_name):
    if schema_name in model.schemas.keys():
        schema = model.schemas[schema_name]
        if table_name in schema.tables:
            table = model.schemas[schema_name].tables[table_name]
            table.alter(table_name=new_name)
            print('Renamed table {}:{} to {}'.format(schema_name, table_name, new_name))

# rename a column
def rename_column_if_exists(model, schema_name, table_name, old_name, new_name):
    if schema_name in model.schemas.keys():
        schema = model.schemas[schema_name]
        if table_name in schema.tables:
            table = model.schemas[schema_name].tables[table_name]
            if old_name in table.column_definitions.elements:
                table.column_definitions[old_name].alter(name=new_name)
                print('Renamed in table {}:{} column {} to {}'.format(schema_name, table_name, old_name, new_name))

# rename a key
# the key parameter is provided as as a name
# usage example: rename_key(model, 'PDB', 'ihm_model_group', 'ihm_model_group_RID_id_key', 'ihm_model_group_combo1_key')
def rename_key_if_exist(model, schema_name, table_name, old_key_name, new_key_name):
    schema = model.schemas[schema_name]
    table = schema.tables[table_name]
    
    if (schema, old_key_name) in table.keys.elements:
        table.keys[(schema, old_key_name)].alter(constraint_name=new_key_name)
        print("Rename key %s.%s key:%s -> %s" % (schema_name, table_name, old_key_name, new_key_name))

# ---------------------------------------
# check if a key is defined in a table based on column name.
# The main function is Table.key_by_columns(columns, raise_nomatch=True) takes a list (iterable) of Column instances or column name strings and returns the Key instance.
# The option flag changes whether it raises KeyError or returns None if no key is found for those columns.
def exist_key_by_columns(model, schema_name, table_name, key_column_names):
    table = model.schemas[schema_name].tables[table_name]
    return table.key_by_columns(key_column_names, raise_nomatch=False) is not None

# ---------------------------------------
def exist_key_by_name(model, schema_name, table_name, key_name):
    schema = model.schemas[schema_name]
    table = schema.tables[table_name]
    return (schema, key_name) in table.keys.elements

# ---------------------------------------
def exist_fkey_by_name(model, schema_name, table_name, fkey_name):
    schema = model.schemas[schema_name]
    table = schema.tables[table_name]
    return (schema, fkey_name) in table.foreign_keys.elements    


# ---------------------------------------
# check if a foreign key is defined or not in a table
# the key parameter is provided as a list of columns names
# WARNING: HT: This function doesn't do a proper fk checking. DON'T USE
def exist_foreign_key_in_table(model, schema_name, table_name, key):
    if schema_name in model.schemas.keys():
        schema = model.schemas[schema_name]
        if table_name in schema.tables:
            key = sorted(key)
            table = model.schemas[schema_name].tables[table_name]
            for fk in table.foreign_keys:
                foreign_key_columns_names = []
                for col in fk.foreign_key_columns:
                    foreign_key_columns_names.append(col.name)
                if key == sorted(foreign_key_columns_names):
                    return True
    return False

# ---------------------------------------
# drop a table together with the associated reference keys
# WARNING: ONLY USE THIS FUNCTION FOR NEWLY CREATED TABLE
def drop_table(catalog, schema_name, table_name):
    model = catalog.getCatalogModel()
    if schema_name in model.schemas.keys():
        schema = model.schemas[schema_name]
        if table_name in schema.tables:
            ready = False
            while ready == False:
                model = catalog.getCatalogModel()
                table = model.schemas[schema_name].tables[table_name]
                if len(table.referenced_by) == 0:
                    ready = True
                else:
                    for foreign_key in table.referenced_by:
                        foreign_key.drop()
            model = catalog.getCatalogModel()
            table = model.schemas[schema_name].tables[table_name]
            table.drop()
            print('Dropped table {}:{}'.format(schema_name, table_name))

# ---------------------------------------
# create a vocabulary table if it does not exixt
def create_vocabulary_table_if_not_exist(model, schema_name, table_name, comment):
    schema = model.schemas[schema_name]
    if table_name not in schema.tables:
        schema.create_table(Table.define_vocabulary(table_name, 'PDB:{RID}', comment=comment))
        print('Created table {}:{}'.format(schema_name, table_name))

# ---------------------------------------
# add table if not exist or update if exist
def create_table_if_not_exist(model, schema_name, tdoc):
    schema = model.schemas[schema_name]
    if tdoc["table_name"] not in schema.tables:
        schema.create_table(tdoc)
        print('Created table {}:{}'.format(schema_name, tdoc["table_name"]))

# add table if not exist or update if exist
def set_table_comment_if_exist(model, schema_name, table_name, comment):
    if schema_name in model.schemas.keys():
        schema = model.schemas[schema_name]
        if table_name in schema.tables:
            table = schema.tables[table_name]
            table.comment = comment
            model.apply()
            print('Set comment for table {}:{}'.format(schema_name, table_name))

# set column comment if exist
def set_column_comment_if_exist(model, schema_name, table_name, column_name, comment):
    if schema_name in model.schemas.keys():
        schema = model.schemas[schema_name]
        if table_name in schema.tables:
            table = schema.tables[table_name]
            if column_name in table.column_definitions.elements:
                table.column_definitions[column_name].comment = comment
                model.apply()
                print('Set comment for column {}:{}:{}'.format(schema_name, table_name, column_name))

# ---------------------------------------
# remove a column if it exists
# if schema_name and table_name are not in the model, throw an error.
def drop_column_if_exist(model, schema_name, table_name, column_name):
    schema = model.schemas[schema_name]
    table = schema.tables[table_name]

    try:
        table.columns[column_name].drop()
        print("Dropped column %s.%s.%s" % (schema_name, table_name, column_name))        
    except KeyError:
        pass

# add a column if it does not exist
def create_column_if_not_exist(model, schema_name, table_name, column):
    if schema_name in model.schemas.keys():
        schema = model.schemas[schema_name]
        if table_name in schema.tables:
            table = schema.tables[table_name]
            if column['name'] not in table.columns.elements:
                table.create_column(column)
                print("Added column {}:{}:{}".format(schema_name, table_name, column['name']))

    # these approach doesn't validate the schema and table names
    #if table_name in model.schemas[schema_name].tables:
    #    table = model.schemas[schema_name].tables[table_name]
    #    if column_name in table.columns.elements:
    #        table.column_definitions[column_name].drop()
    #        print("Dropped column %s.%s.%s" % (schema_name, table_name, column_name))

# ----------------------------------------
# alter on update fkey if exist
# if schema_name and table_name are not in the model, throw an error.
def alter_on_update_fkey_if_exist(model, schema_name, table_name, fkey_name, value):

    schema = model.schemas[schema_name]
    table = schema.tables[table_name]
    try:
        table.foreign_keys[(schema, fkey_name)].alter(on_update=value)
        print("Altered fkey %s of table %s.%s on_update=%s" % (fkey_name, schema_name, table_name, value))
    except KeyError:
        pass

# ----------------------------------------
# alter on delete fkey if exist
# if schema_name and table_name are not in the model, throw an error.
def alter_on_delete_fkey_if_exist(model, schema_name, table_name, fkey_name, value):

    schema = model.schemas[schema_name]
    table = schema.tables[table_name]
    try:
        table.foreign_keys[(schema, fkey_name)].alter(on_delete=value)
        print("Altered fkey %s of table %s.%s on_delete=%s" % (fkey_name, schema_name, table_name, value))
    except KeyError:
        pass

# ----------------------------------------
# rename fkey if exist
# if schema_name and table_name are not in the model, throw an error.
def rename_fkey_if_exist(model, schema_name, table_name, old_key_name, new_key_name):

    schema = model.schemas[schema_name]
    table = schema.tables[table_name]
    try:
        table.foreign_keys[(schema, old_key_name)].alter(constraint_name=new_key_name)
        print("Renamed fkey %s of table %s.%s to %s" % (old_key_name, schema_name, table_name, new_key_name))
    except KeyError:
        pass

# ----------------------------------------
# drop fkey if exist
# if schema_name and table_name are not in the model, throw an error.
def drop_fkey_if_exist(model, schema_name, table_name, fkey_name):

    schema = model.schemas[schema_name]
    table = schema.tables[table_name]
    try:
        table.foreign_keys[(schema, fkey_name)].drop()
        print("Dropped fkey %s.%s fkey:%s" % (schema_name, table_name, fkey_name))
    except KeyError:
        pass

# ----------------------------------------
# drop key if exist
def drop_key_if_exist(model, schema_name, table_name, key_name):

    schema = model.schemas[schema_name]
    table = schema.tables[table_name]
    try:
        table.keys[(schema, key_name)].drop()
        print("Dropped key %s.%s key:%s" % (schema_name, table_name, key_name))
    except KeyError:
        pass


def create_key_if_not_exists(model, schema_name, table_name, columns, constraint_name):
    if schema_name in model.schemas.keys():
        schema = model.schemas[schema_name]
        if table_name in schema.tables:
            table = schema.tables[table_name]
            if table.key_by_columns(columns, raise_nomatch=False) is None:
                table.create_key(   
                    Key.define(columns, constraint_names=[[schema_name, constraint_name]] )
                )
                print('Created Key {} for table {}:{}'.format(constraint_name, schema_name, table_name))
    
def create_foreign_key_if_not_exists(model, schema_name, table_name, constraint_name, foreign_key):
    if schema_name in model.schemas.keys():
        schema = model.schemas[schema_name]
        if table_name in schema.tables:
            table = schema.tables[table_name]
            if (schema, constraint_name) not in table.foreign_keys.elements:
                table.create_fkey(foreign_key)
                print('Created Foreign Key {} for table {}:{}'.format(constraint_name, schema_name, table_name))

    
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

"""
add rows to a table
"""
def add_rows_to_vocab_table(catalog, table_name, rows):
    pb = catalog.getPathBuilder()
    schema = pb.Vocab
    table = schema.__getattr__(table_name)
    table.insert(rows, defaults=['ID', 'URI'])
    print('Added rows to the vocabulary table {}'.format(table_name))

"""
get the table acl_bindings
"""
def get_table_acl_bindings(catalog, schema_name, table_name):
    model = catalog.getCatalogModel()
    schema = model.schemas[schema_name]
    table = model.schemas[schema_name].tables[table_name]
    acl_bindings = {'acl_bindings': table.acl_bindings}
    print('acl_bindings for table {}:{}\n{}'.format(schema_name, table_name, json.dumps(acl_bindings, indent=4)))

"""
set the table acl_bindings
"""
def set_table_acl_bindings(catalog, schema_name, table_name, acl_bindings):
    model = catalog.getCatalogModel()
    schema = model.schemas[schema_name]
    table = model.schemas[schema_name].tables[table_name]
    table.acl_bindings = acl_bindings
    model.apply()
    print('Set acl_bindings for table {}:{}'.format(schema_name, table_name))

"""
set the column acl_bindings
"""
def set_column_acl_bindings(catalog, schema_name, table_name, column_name, acl_bindings):
    model = catalog.getCatalogModel()
    schema = model.schemas[schema_name]
    table = schema.tables[table_name]
    if column_name in table.column_definitions.elements:
        table.column_definitions[column_name].acl_bindings = acl_bindings
        model.apply()
        print('Set acl_bindings for the column {}:{}:{}'.format(schema_name, table_name, column_name))

"""
set the table acls
"""
def set_table_acls(catalog, schema_name, table_name, acls):
    model = catalog.getCatalogModel()
    schema = model.schemas[schema_name]
    table = model.schemas[schema_name].tables[table_name]
    table.acls = acls
    model.apply()
    print('Set acls for table {}:{}'.format(schema_name, table_name))

"""
get the foreign key acl_bindings
"""
def get_foreign_key_acl_bindings(catalog, schema_name, table_name, constraint_name):
    model = catalog.getCatalogModel()
    schema = model.schemas[schema_name]
    table = model.schemas[schema_name].tables[table_name]
    fk = table.foreign_keys.__getitem__((schema, constraint_name))
    acl_bindings = {'acl_bindings': fk.acl_bindings}
    print('acl_bindings for table {}:{}, FK: {}\n{}'.format(schema_name, table_name, constraint_name, json.dumps(acl_bindings, indent=4)))

"""
set the foreign key acl_bindings
"""
def set_foreign_key_acl_bindings(catalog, schema_name, table_name, constraint_name, acl_bindings):
    model = catalog.getCatalogModel()
    schema = model.schemas[schema_name]
    table = model.schemas[schema_name].tables[table_name]
    fk = table.foreign_keys.__getitem__((schema, constraint_name))
    fk.acl_bindings = acl_bindings
    model.apply()
    print('Set acl_bindings for the foreign key {} of the table {}:{}'.format(constraint_name, schema_name, table_name))

"""
set the foreign key acls
"""
def set_foreign_key_acls(catalog, schema_name, table_name, constraint_name, acls):
    model = catalog.getCatalogModel()
    schema = model.schemas[schema_name]
    table = model.schemas[schema_name].tables[table_name]
    fk = table.foreign_keys.__getitem__((schema, constraint_name))
    fk.acls = acls
    model.apply()
    print('Set acls for the foreign key {} of the table {}:{}'.format(constraint_name, schema_name, table_name))

"""
set the column acls
"""
def set_column_acls(catalog, schema_name, table_name, column_name, acls):
    model = catalog.getCatalogModel()
    schema = model.schemas[schema_name]
    table = schema.tables[table_name]
    if column_name in table.column_definitions.elements:
        table.column_definitions[column_name].acls = acls
        model.apply()
        print('Set acls for the column {}:{}:{}'.format(schema_name, table_name, column_name))

