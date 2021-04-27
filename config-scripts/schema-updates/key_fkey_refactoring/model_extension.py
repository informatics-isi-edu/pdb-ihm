#!/usr/bin/python3

import argparse
import json
import sys
from deriva.core import ErmrestCatalog, get_credential
from deriva.core.ermrest_model import builtin_types as typ, Table, Key, ForeignKey, Column
from deriva.core.ermrest_model import tag as chaise_tags

"""
Tool to refactor the primary keys and foreign keys of the PDB model 

usage: python3 model_extension.py <catalog_number> <schema_name> <action>

The <action> parameters can have one of the following values:
  workflow            Generates the workflow.txt file with the list of actions to be performed
  columns             Generates the columns.txt file with the list of columns that needs to be renamed or added
                      An sql.txt file is also generated with the SQL statements to initialize the new Parent_table_RID columns
  primary_keys        Generates the primary_key.txt file with the list of primary keys that needs to be renamed or added
  foreign_keys        Generates the foreign_key.txt file with the list of foreign keys that needs to be renamed, added or dropped
  duplicates          Generates the duplicates.txt file with the duplicate foreign keys names from renaming or adding foreign keys
  long_names          Generates the long_names.txt file with the list of foreign keys having a name longer than 63 characters from renaming or adding foreign keys
  fk_fkey             Generates the fk_fkey.txt file with the foreign keys name that differ just by the suffix _fk vs. fkey
  fk_annotations      Generates the fk_annotations.txt file with the annotations where the foreign keys appear
  fk_acl_bindings     Generates the fk_acl_bindings.txt file with the acl_bindings where the foreign keys appear
  mandatory           Generates the mandatory.txt file with the mandatory and optional foreign keys
  all                 Generates all the above
"""

"""
Contains the columns of the tables in a dictionary format:

{table_name: [columns_names]}
"""
columns_table_map = {}

"""
Contains the columns of the tables ito be renamed n a dictionary format:

{table_name: {old_name: new_name}}
"""
rename_columns_map = {}

"""
Contains the new columns of the tables in a dictionary format:

{table_name: [{column: column, key: foreign_key}]}
"""
add_columns_map = {}

"""
Contains the names of the primary keys
"""
pk_keys = []

"""
Contains the PK of the schema:

{constraint_name: Key}
"""
pk_map = {}

"""
Contains the PK of the table in a dictionary format:

{table_name: [Keys]}
"""
pk_table_map = {}

"""
Contains the new PK of the table in a dictionary format:

{table_name: [Keys]}
"""
add_pk_map = {}

"""
Contains the PK of the table to be renamed in a dictionary format:

{table_name: [{constraint_name: constraint_name, key: primary_key]}
"""
pk_rename = {}

"""
Contains the names of the foreign keys
"""
fk_keys_names = []

"""
Contains the FK of the schema:

{constraint_name: Key}
"""
fk_map = {}

"""
Contains the FK of the table in a dictionary format:

{table_name: [Keys]}
"""
fk_table_map = {}

"""
Contains the FK columns of the table REFERENCING the RID column in a dictionary format:

{table_name: [{column} REFERENCES {parent_table}[RID]]}
"""
fk_rid = {}

"""
Contains the new FK columns of the table REFERENCING the RID column in a dictionary format:

{table_name: [{column} REFERENCES {parent_table}[RID]]}
"""
new_fk_rid = {}

"""
Contains the new FK in a dictionary format:

{table_name: {foreign_key_name: {parent_table: parent_table, referenced_columns: referenced_columns}}
"""
new_fk_map = {}

"""
Contains the FK of the table to be renamed in a dictionary format:

{table_name: [{constraint_name: constraint_name, key: foreign_key]}
"""
fk_rename = {}

"""
Contains the new FK to be dropped in a dictionary format:

{table_name: {foreign_key_name: {parent_table: parent_table, referenced_columns: referenced_columns}}
"""
drop_fk_map = {}

max_pk_columns = 0
max_fk_columns = 0


"""
Convert a list of Columns objects to a list of columns names
"""
def columns(cols):
    ret = []
    for col in cols:
        ret.append(col.name)
    return ret

"""
Gather the columns of the tables
"""
def setColumns(schema):
    for table_name in schema.tables:
        table = schema.tables[table_name]
        columns_table_map[table_name] = columns(table.column_definitions)
                
"""
Gather the PK of the tables
"""
def setPK(schema):
    global max_pk_columns
    for table_name in schema.tables:
        table = schema.tables[table_name]
        for key_name in table.keys.elements:
            key = table.keys[key_name]
            if key.constraint_name not in pk_keys:
                pk_keys.append(key.constraint_name)
                pk_map[key.constraint_name] = key
                if table_name not in pk_table_map.keys():
                    pk_table_map[table_name] = []
                pk_table_map[table_name].append(key)
                if max_pk_columns < len(key.unique_columns):
                    max_pk_columns = len(key.unique_columns)
            else:
                print('Duplicate PK: {}'.format(key.constraint_name))
                

"""
Gather the FK of the tables
"""
def setFK(schema):
    global max_fk_columns
    for table_name in schema.tables:
        table = schema.tables[table_name]
        for key_name in table.foreign_keys.elements:
            key = table.foreign_keys[key_name]
            if key.constraint_name not in fk_keys_names:
                fk_keys_names.append(key.constraint_name)
                fk_map[key.constraint_name] = key
                if table_name not in fk_table_map.keys():
                    fk_table_map[table_name] = []
                fk_table_map[table_name].append(key)
                if max_fk_columns < len(key.foreign_key_columns):
                    max_fk_columns = len(key.foreign_key_columns)
            else:
                print('Duplicate FK: {}'.format(key.constraint_name))


                
"""
Write the FK of the tables grouped by (structure_id, RID) of the referenced columns
"""
def write_foreign_key(table_name, pk_table_name, constraint_name, structure_id, RID, foreign_key_columns, referenced_columns, fw):
    if structure_id == True and RID == True:
        if 'structure_id' in referenced_columns and 'RID' in referenced_columns:
            fw.write('{}: {}{} --> {}{}\n'.format(constraint_name, table_name, foreign_key_columns, pk_table_name, referenced_columns))
        return
    elif structure_id == True:
        if 'structure_id' in referenced_columns and 'RID' not in referenced_columns:
            fw.write('{}: {}{} --> {}{}\n'.format(constraint_name, table_name, foreign_key_columns, pk_table_name, referenced_columns))
        return
    elif RID == True:
        if 'RID' in referenced_columns and 'structure_id' not in referenced_columns:
            fw.write('{}: {}{} --> {}{}\n'.format(constraint_name, table_name, foreign_key_columns, pk_table_name, referenced_columns))
        return
    elif structure_id == False and RID == False:
        if 'structure_id' not in referenced_columns and 'RID' not in referenced_columns:
            fw.write('{}: {}{} --> {}{}\n'.format(constraint_name, table_name, foreign_key_columns, pk_table_name, referenced_columns))
        return

"""
Write the FK of the tables grouped by (structure_id, RID) of the referenced columns and the number of columns of the referenced columns
"""
def write_fk(schema_name, fw, length, structure_id=False, RID=False):
    for table_name in sorted(fk_table_map.keys()):
        for key in fk_table_map[table_name]:
            if len(key.foreign_key_columns) == length:
                if key.pk_table.schema.name == schema_name:
                    foreign_key_columns = columns(key.foreign_key_columns)
                    referenced_columns = columns(key.referenced_columns)
                    write_foreign_key(table_name, key.pk_table.name, key.constraint_name, structure_id, RID, foreign_key_columns, referenced_columns, fw)

"""
Write the PK of the tables grouped by (structure_id, RID)
"""
def write_key(table_name, constraint_name, structure_id, RID, cols, fw):
    if structure_id == True and RID == True:
        if 'structure_id' in cols and 'RID' in cols:
            fw.write('{}: {}{}\n'.format(constraint_name, table_name, cols))
        return
    elif structure_id == True:
        if 'structure_id' in cols and 'RID' not in cols:
            fw.write('{}: {}{}\n'.format(constraint_name, table_name, cols))
        return
    elif RID == True:
        if 'RID' in cols and 'structure_id' not in cols:
            fw.write('{}: {}{}\n'.format(constraint_name, table_name, cols))
        return
    elif structure_id == False and RID == False:
        if 'structure_id' not in cols and 'RID' not in cols:
            fw.write('{}: {}{}\n'.format(constraint_name, table_name, cols))
        return

"""
Write the PK of the tables grouped by (structure_id, RID) and the number of columns of the PK
"""
def write_pk(fw, length, structure_id=False, RID=False):
    for table_name in sorted(pk_table_map.keys()):
        for key in pk_table_map[table_name]:
            if len(key.unique_columns) == length:
                cols = columns(key.unique_columns)
                if length == 1:
                    if 'RID' not in cols:
                        fw.write('{}: {}{}\n'.format(key.constraint_name, table_name, cols))
                else:
                    write_key(table_name, key.constraint_name, structure_id, RID, cols, fw)

"""
Write the PK and FK of the tables
"""
def write_key_and_foreign_key():
    """
    Write the PK of the tables grouped by (structure_id, RID) and the number of columns of the PK
    """
    fw = open('pk.txt', 'w')
    
    fw.write('PRIMARY KEY WITH A COLUMN DIFFERENT FROM "RID"\n\n')
    write_pk(fw, 1)
    
    #fw.write('\nTABLES WITH 2 COLUMNS ["structure_id", "RID"]\n\n')
    write_pk(fw, 2, structure_id=True, RID=True)
    fw.write('\nPRIMARY KEY WITH 2 COLUMNS HAVING "structure_id" AND NOT "RID"\n\n')
    write_pk(fw, 2, structure_id=True)
    fw.write('\nPRIMARY KEY WITH 2 COLUMNS HAVING "RID" AND NOT "structure_id"\n\n')
    write_pk(fw, 2, RID=True)
    fw.write('\nPRIMARY KEY WITH 2 COLUMNS HAVING NOT "RID" AND NOT "structure_id"\n\n')
    write_pk(fw, 2)
    
    fw.write('\nPRIMARY KEY WITH 3 COLUMNS HAVING "structure_id" AND "RID"\n\n')
    write_pk(fw, 3, structure_id=True, RID=True)
    fw.write('\nPRIMARY KEY WITH 3 COLUMNS HAVING "structure_id" AND NOT "RID"\n\n')
    write_pk(fw, 3, structure_id=True)
    #fw.write('\nPRIMARY KEY WITH 3 COLUMNS HAVING "RID" AND NOT "structure_id"\n\n')
    write_pk(fw, 3, RID=True)
    #fw.write('\nPRIMARY KEY WITH 3 COLUMNS HAVING NOT "RID" AND NOT "structure_id"\n\n')
    write_pk(fw, 3)
    
    #fw.write('\nPRIMARY KEY WITH 4 COLUMNS HAVING ["structure_id", "RID"]\n\n')
    write_pk(fw, 4, structure_id=True, RID=True)
    fw.write('\nPRIMARY KEY WITH 4 COLUMNS HAVING "structure_id" AND NOT "RID"\n\n')
    write_pk(fw, 4, structure_id=True)
    fw.write('\nPRIMARY KEY WITH 4 COLUMNS HAVING "RID" AND NOT "structure_id"\n\n')
    write_pk(fw, 4, RID=True)
    #fw.write('\nPRIMARY KEY WITH 4 COLUMNS HAVING NOT "RID" AND NOT "structure_id"\n\n')
    write_pk(fw, 4)
    
    fw.write('\nPRIMARY KEY WITH 5 COLUMNS HAVING "structure_id" AND "RID"\n\n')
    write_pk(fw, 5, structure_id=True, RID=True)
    #fw.write('\nPRIMARY KEY WITH 5 COLUMNS HAVING "structure_id" AND NOT "RID"\n\n')
    write_pk(fw, 5, structure_id=True)
    #fw.write('\nPRIMARY KEY WITH 5 COLUMNS HAVING "RID" AND NOT "structure_id"\n\n')
    write_pk(fw, 5, RID=True)
    #fw.write('\nPRIMARY KEY WITH 5 COLUMNS HAVING NOT "RID" AND NOT "structure_id"\n\n')
    write_pk(fw, 5)
    
    fw.close()
    
    """
    Write the FK of the tables grouped by (structure_id, RID) of the referenced columns and the number of columns of the referenced columns
    """
    fw = open('fk.txt', 'w')
    #fw.write('FOREIGN KEY WITH A COLUMN HAVING "structure_id" AS REFERENCED COLUMN\n\n')
    write_fk(schema_name, fw, 1, structure_id=True)
    fw.write('\nFOREIGN KEY WITH A COLUMN HAVING "RID" AS REFERENCED COLUMN\n\n')
    write_fk(schema_name, fw, 1, RID=True)
    fw.write('\nFOREIGN KEY WITH A COLUMN HAVING NOT "RID" AND NOT "structure_id" AS REFERENCED COLUMN\n\n')
    write_fk(schema_name, fw, 1)
    
    #fw.write('\nFOREIGN KEY WITH 2 COLUMNS HAVING "structure_id" AS REFERENCED COLUMN AND "RID" AS REFERENCED COLUMN\n\n')
    write_fk(schema_name, fw, 2, structure_id=True, RID=True)
    fw.write('\nFOREIGN KEY WITH 2 COLUMNS HAVING "structure_id" AS REFERENCED COLUMN AND NOT "RID" AS REFERENCED COLUMN\n\n')
    write_fk(schema_name, fw, 2, structure_id=True)
    fw.write('\nFOREIGN KEY WITH 2 COLUMNS HAVING "RID" AS REFERENCED COLUMN AND NOT "structure_id" AS REFERENCED COLUMN\n\n')
    write_fk(schema_name, fw, 2, RID=True)
    #fw.write('\nFOREIGN KEY WITH 2 COLUMNS HAVING NOT "RID" AS REFERENCED COLUMN AND NOT "structure_id" AS REFERENCED COLUMN\n\n')
    write_fk(schema_name, fw, 2)
    
    fw.write('\nFOREIGN KEY WITH 3 COLUMNS HAVING "structure_id" AS REFERENCED COLUMN AND "RID" AS REFERENCED COLUMN\n\n')
    write_fk(schema_name, fw, 3, structure_id=True, RID=True)
    #fw.write('\nFOREIGN KEY WITH 3 COLUMNS HAVING "structure_id" AS REFERENCED COLUMN AND NOT "RID" AS REFERENCED COLUMN\n\n')
    write_fk(schema_name, fw, 3, structure_id=True)
    #fw.write('\nFOREIGN KEY WITH 3 COLUMNS HAVING "RID" AS REFERENCED COLUMN AND NOT "structure_id" AS REFERENCED COLUMN\n\n')
    write_fk(schema_name, fw, 3, RID=True)
    #fw.write('\nFOREIGN KEY WITH 3 COLUMNS HAVING NOT "RID" AS REFERENCED COLUMN AND NOT "structure_id" AS REFERENCED COLUMN\n\n')
    write_fk(schema_name, fw, 3)
    
    #fw.write('\nFOREIGN KEY WITH 4 COLUMNS HAVING "structure_id" AS REFERENCED COLUMN AND "RID" AS REFERENCED COLUMN\n\n')
    write_fk(schema_name, fw, 4, structure_id=True, RID=True)
    fw.write('\nFOREIGN KEY WITH 4 COLUMNS HAVING "structure_id" AS REFERENCED COLUMN AND NOT "RID" AS REFERENCED COLUMN\n\n')
    write_fk(schema_name, fw, 4, structure_id=True)
    #fw.write('\nFOREIGN KEY WITH 4 COLUMNS HAVING "RID" AS REFERENCED COLUMN AND NOT "structure_id" AS REFERENCED COLUMN\n\n')
    write_fk(schema_name, fw, 4, RID=True)
    #fw.write('\nFOREIGN KEY WITH 4 COLUMNS HAVING NOT "RID" AS REFERENCED COLUMN AND NOT "structure_id" AS REFERENCED COLUMN\n\n')
    write_fk(schema_name, fw, 4)
    
    fw.write('\nFOREIGN KEY WITH 5 COLUMNS HAVING "structure_id" AS REFERENCED COLUMN AND "RID" AS REFERENCED COLUMN\n\n')
    write_fk(schema_name, fw, 5, structure_id=True, RID=True)
    #fw.write('\nFOREIGN KEY WITH 5 COLUMNS HAVING "structure_id" AS REFERENCED COLUMN AND NOT "RID" AS REFERENCED COLUMN\n\n')
    write_fk(schema_name, fw, 5, structure_id=True)
    #fw.write('\nFOREIGN KEY WITH 5 COLUMNS HAVING "RID" AS REFERENCED COLUMN AND NOT "structure_id" AS REFERENCED COLUMN\n\n')
    write_fk(schema_name, fw, 5, RID=True)
    #fw.write('\nFOREIGN KEY WITH 5 COLUMNS HAVING NOT "RID" AS REFERENCED COLUMN AND NOT "structure_id" AS REFERENCED COLUMN\n\n')
    write_fk(schema_name, fw, 5)
    
    fw.close()
    
"""
Gathers the FK columns of the table REFERENCING the RID column
"""
def set_fk_rid():
    for constraint_name, key in fk_map.items():
        referenced_columns = columns(key.referenced_columns)
        foreign_key_columns = columns(key.foreign_key_columns)
        if 'RID' in referenced_columns:
            foreign_key_column = foreign_key_columns[referenced_columns.index('RID')]
            table_name = key.table.name
            pk_table_name = key.pk_table.name
            if table_name not in fk_rid.keys():
                fk_rid[table_name] = []
            fk_rid[table_name].append('{} REFERENCES {}[RID]'.format(foreign_key_column, pk_table_name))
                
"""
Gathers the FK columns of the table grouped by (structure_id, RID) of the referenced columns and based on the number of referenced columns
"""
def get_fk(length, structure_id=False, RID=False):
    ret = []
    for constraint_name, key in fk_map.items():
        referenced_columns = columns(key.referenced_columns)
        if len(referenced_columns) == length:
            if length == 2:
                if RID == False and structure_id == True:
                    if 'RID' not in referenced_columns and 'structure_id' in referenced_columns and 'combo1' not in constraint_name:
                        ret.append(key)
                elif RID == True and structure_id == False:
                    if 'RID' in referenced_columns and 'structure_id' not in referenced_columns and 'combo2' not in constraint_name:
                        ret.append(key)
            elif length == 4:
                if RID == False and structure_id == True:
                    if 'RID' not in referenced_columns and 'structure_id' in referenced_columns and 'combo1' not in constraint_name:
                        ret.append(key)
                
    return ret
                
"""
Rename a FK 
"""
def rename_foreign_key(fw, key, constraint_name):
    foreign_key_columns = columns(key.foreign_key_columns)
    referenced_columns = columns(key.referenced_columns)
    table_name = key.table.name
    fw.write('RENAME FOREIGN KEY {}: {}{} --> {}{} TO {}\n'.format(key.constraint_name, key.table.name, foreign_key_columns, key.pk_table.name, referenced_columns, constraint_name))
    if table_name not in fk_rename.keys():
        fk_rename[table_name] = {}
    if constraint_name not in fk_rename[table_name].keys():
        fk_rename[table_name][constraint_name] = []
    fk_rename[table_name][constraint_name].append({'constraint_name': constraint_name, 'parent_table': key.pk_table.name, 'foreign_key_columns': foreign_key_columns, 'referenced_columns': referenced_columns, 'old_constraint_name': key.constraint_name})

"""
Add a new FK 
"""
def add_foreign_key(fw, key, constraint_name):
    foreign_key_columns = columns(key.foreign_key_columns)
    referenced_columns = columns(key.referenced_columns)
    table_name = key.table.name
    fw.write('ADD FOREIGN KEY {}: {}{} --> {}{}\n'.format(constraint_name, key.table.name, foreign_key_columns, key.pk_table.name, referenced_columns))
    if table_name not in new_fk_map.keys():
        new_fk_map[table_name] = {}
    if constraint_name not in new_fk_map[table_name].keys():
        new_fk_map[table_name][constraint_name] = []
    new_fk_map[table_name][constraint_name].append({'parent_table': key.pk_table.name, 'foreign_key_columns': foreign_key_columns, 'referenced_columns': referenced_columns})

"""
Drop an old FK 
"""
def drop_foreign_key(fw, key):
    foreign_key_columns = columns(key.foreign_key_columns)
    referenced_columns = columns(key.referenced_columns)
    table_name = key.table.name
    constraint_name = key.constraint_name
    fw.write('DROP FOREIGN KEY {}: {}{} --> {}{}\n'.format(key.constraint_name, key.table.name, foreign_key_columns, key.pk_table.name, referenced_columns))
    if table_name not in drop_fk_map.keys():
        drop_fk_map[table_name] = {}
    if constraint_name not in drop_fk_map[table_name].keys():
        drop_fk_map[table_name][constraint_name] = []
    drop_fk_map[table_name][constraint_name].append({'parent_table': key.pk_table.name, 'foreign_key_columns': foreign_key_columns, 'referenced_columns': referenced_columns})

def get_pk(length, structure_id=False, RID=False):
    ret = []
    for constraint_name, key in pk_map.items():
        cols = columns(key.unique_columns)
        if len(cols) == length:
            if length == 1:
                if 'RID' not in cols:
                    ret.append(key)
            elif length == 2:
                if RID == True and structure_id == False:
                    if 'RID' in cols and 'structure_id' not in cols and 'combo2' not in constraint_name:
                        ret.append(key)
                
    return ret
                
"""
Check the existence of a PK based on the list of columns
"""
def exists_primary_key(table_name, cols):
    for key in pk_table_map[table_name]:
        try:
            unique_columns = columns(key.unique_columns)
        except:
            unique_columns = key['unique_columns']
        if sorted(cols) == sorted(unique_columns):
            return True
    return False
    
"""
Add a column to a table
"""
def addColumn(fw, table_name, column, key):
    if len(column) > 63:
        print('WARNING ADD COLUMN {} HAS {} CHARACTERS'.format(column, len(column)))
    fw.write('ADD COLUMN {} TO TABLE {} FOR THE NEW FOREIGN KEY {}_{}_combo1_fkey: {}{} --> {}{}\n'.format(column, table_name, table_name, key.pk_table.name, table_name, [column] + columns(key.foreign_key_columns), key.pk_table.name, ['RID'] + columns(key.referenced_columns)))
    columns_table_map[table_name].append(column)
    if table_name not in new_fk_rid.keys():
        new_fk_rid[table_name] = []
    new_fk_rid[table_name].append('{} REFERENCES {}[RID]'.format(column, column[0:-4]))
    if table_name not in add_columns_map.keys():
        add_columns_map[table_name] = []
    add_columns_map[table_name].append({'column': column,
                                        'key': key})
    
"""
Rename a PK
"""
def rename_primary_key(fw, key, constraint_name):
    cols = columns(key.unique_columns)
    table_name = key.table.name
    fw.write('RENAME PRIMARY KEY {}: {}{} TO {}\n'.format(key.constraint_name, table_name, cols, constraint_name))
    if table_name not in pk_rename.keys():
        pk_rename[table_name] = []
    pk_rename[table_name].append({'constraint_name': constraint_name,
                             'key': key})

"""
Check if a constraint exists
Print a WARNING if it exists
Appended in the list if it does not exist
"""
def check_exist(contraint_list, contraint_name, warning=True):
    if contraint_name in contraint_list:
        if warning == True:
            print('WARNING: {} ALREADY EXISTS'.format(contraint_name))
    else:
        contraint_list.append(contraint_name)

"""
Add a PK
"""
def add_primary_key(fw, table_name, contraint_name, cols):
    fw.write('ADD PRIMARY KEY {}: {}{}\n'.format(contraint_name, table_name, cols))
    pk_keys.append(contraint_name)
    key = Key.define(cols,
                   constraint_names=[['PDB', '{}'.format(contraint_name)]]
        )
    pk_table_map[table_name].append(key)
    if table_name not in add_pk_map.keys():
        add_pk_map[table_name] = []
    add_pk_map[table_name].append(key)

"""
Rename a column
"""
def rename_column(fw, table_name, fk_column_name, rid_fk_column_name, fk):
    if len(rid_fk_column_name) > 63:
        print('WARNING RENAMING {} HAS {} CHARACTERS'.format(rid_fk_column_name, len(rid_fk_column_name)))
    fw.write('RENAME COLUMN {} OF TABLE {} TO {} FOR FOREIGN KEY {}: {}{} --> {}{}\n'.format(fk_column_name, table_name, rid_fk_column_name, fk.constraint_name, table_name, columns(fk.foreign_key_columns), fk.pk_table.name, columns(fk.referenced_columns)))
    index = columns_table_map[table_name].index(fk_column_name)
    columns_table_map[table_name][index] = rid_fk_column_name

"""
Generate the file with the columns to be renamed and added
Generate the SQL script to populate the new columns
"""
def generate_columns():
    fw = open('columns.txt', 'w')
    
    """
    Gather the columns to be renamed
    """
    counter = 0
    for table_name in rename_columns_map.keys():
        for column_name, rid_column_name in rename_columns_map[table_name].items():
            fw.write('RENAME COLUMN "{}" BY "{}" IN TABLE "{}"\n'.format(column_name, rid_column_name, table_name))
            counter +=1
    fw.write('\n')

    print('{} COLUMNS TO BE RENAMED'.format(counter))

    """
    Gather the columns to be added
    """
    counter = 0
    for table_name in add_columns_map.keys():
        for value in add_columns_map[table_name]:
            fw.write('ADD COLUMN "{}" TO TABLE "{}"\n'.format(value['column'], table_name))
            counter +=1
    fw.write('\n')

    print('{} COLUMNS TO BE ADDED'.format(counter))

    fw.close()
    
    """
    Generate the SQL script to populate the new columns
    """
    fw = open('sql.txt', 'w')
    fw.write('BEGIN;\n')
    counter = 0
    for table_name in add_columns_map.keys():
        for value in add_columns_map[table_name]:
            key = value['key']
            foreign_key_columns = columns(key.foreign_key_columns)
            referenced_columns = columns(key.referenced_columns)
            sql_statement = 'update "PDB"."{}" A set "{}" = (select "RID" from "PDB"."{}" B where '.format(table_name, value['column'], key.pk_table.name)
            predicate = []
            for i in range(0,len(foreign_key_columns)):
                predicate.append(' A."{}" = B."{}" '.format(foreign_key_columns[i], referenced_columns[i]))
            predicate = 'and'.join(predicate) + ');'
            fw.write('{}{}\n'.format(sql_statement, predicate))
            counter +=1

    fw.write('COMMIT;\n')

    print('{} SQL UPDATE STATEMENTS'.format(counter))

    fw.close()    
    
"""
Generate the file with the primary keys to be renamed and added
"""
def generate_primary_keys():
    fw = open('primary_key.txt', 'w')
    
    """
    Generate the file with the primary keys to be renamed
    """
    counter = 0
    for table_name in pk_rename.keys():
        for value in pk_rename[table_name]:
            key = value['key']
            fw.write('RENAME PRIMARY KEY {} TO {} IN TABLE {}\n'.format(key.constraint_name, value['constraint_name'], table_name))
            counter +=1
    fw.write('\n')

    print('{} RENAMED PRIMARY KEYS'.format(counter))
    
    """
    Generate the file with the primary keys to be added
    """
    counter = 0
    for table_name in add_pk_map.keys():
        for key in add_pk_map[table_name]:
            fw.write('ADDED KEY {} IN TABLE {}{}\n'.format(key['names'][0][1], table_name, key['unique_columns']))
            counter +=1
    fw.write('\n')

    print('{} ADDED PRIMARY KEYS'.format(counter))
    fw.close()

"""
Generate the file with the foreign keys to be renamed, added and dropped
"""
def generate_foreign_keys():
    fw = open('foreign_key.txt', 'w')
    
    counter = 0
    for table_name in fk_rename.keys():
        for constraint_name, values in fk_rename[table_name].items():
            for value in values:
                fw.write('RENAME FOREiGN KEY {}: {}{} --> {}{} TO {}\n'.format(value['old_constraint_name'], table_name, value['foreign_key_columns'], value['parent_table'], value['referenced_columns'], constraint_name))
                counter +=1

    fw.write('\n')
    print('{} RENAMED FK'.format(counter))

    counter = 0
    for table_name in new_fk_map.keys():
        for constraint_name, values in new_fk_map[table_name].items():
            for value in values:
                fw.write('ADD FOREiGN KEY {}: {}{} --> {}{}\n'.format(constraint_name, table_name, value['foreign_key_columns'], value['parent_table'], value['referenced_columns']))
                counter +=1

    fw.write('\n')
    print('{} NEW FK'.format(counter))

    counter = 0
    for table_name in drop_fk_map.keys():
        for constraint_name, values in drop_fk_map[table_name].items():
            for value in values:
                fw.write('DROP FOREiGN KEY {}: {}{} --> {}{}\n'.format(constraint_name, table_name, value['foreign_key_columns'], value['parent_table'], value['referenced_columns']))
                counter +=1

    fw.write('\n')
    print('{} DROPPED FK'.format(counter))

    fw.close()
    
"""
Generate the file with the FK duplicates
"""
def generate_duplicates():
    fw = open('duplicates.txt', 'w')
    

    counter = 0
    for table_name in new_fk_map.keys():
        for constraint_name, values in new_fk_map[table_name].items():
            if len(values) > 1:
                counter += len(values) - 1
                for value in values:
                    fw.write('DUPLICATE FOREIGN KEY {}: {}{} --> {}{}\n'.format(constraint_name, table_name, value['foreign_key_columns'], value['parent_table'], value['referenced_columns']))
                fw.write('\n')

    for table_name in fk_rename.keys():
        for constraint_name, values in fk_rename[table_name].items():
            if len(values) > 1:
                counter += len(values) - 1
                for value in values:
                    fw.write('DUPLICATE FOREIGN KEY {}: {}{} --> {}{}\n'.format(constraint_name, table_name, value['foreign_key_columns'], value['parent_table'], value['referenced_columns']))
                fw.write('\n')

    fw.write('\n')
    print('{} DUPLICATE FK'.format(counter))

    fw.close()
    
"""
Generate the file with the primary keys to be renamed and added
"""
def generate_long_names():
    fw = open('long_names.txt', 'w')
    
    counter = 0
    for table_name in new_fk_map.keys():
        for constraint_name, values in new_fk_map[table_name].items():
            if len(constraint_name) > 63:
                for value in values:
                    fw.write('FOREIGN KEY {}: {}{} --> {}{} HAS LENGTH {}\n'.format(constraint_name, table_name, value['foreign_key_columns'], value['parent_table'], value['referenced_columns'], len(constraint_name)))
                    counter +=1

    for table_name in fk_rename.keys():
        for constraint_name, values in fk_rename[table_name].items():
            if len(constraint_name) > 63:
                for value in values:
                    fw.write('FOREIGN KEY {} HAS LENGTH {}\n'.format(constraint_name, table_name, value['foreign_key_columns'], value['parent_table'], value['referenced_columns'], len(constraint_name)))
                    counter +=1

    print('{} FK WITH LENGTh GREATER THAN 63'.format(counter))
    fw.close()
    
"""
Generate the workflow
"""
def generate_workflow():
    """
    Gathers the FK columns of the table REFERENCING the RID column
    """
    set_fk_rid()
    
    fw = open('workflow.txt', 'w')
    
    """
    Gathers the columns to be renamed from the FK having 2 columns and RID as referenced column
    """
    keys = get_fk(2, structure_id=True)
    counter = 0
    for key in keys:
        table_name = key.table.name
        parent_table = key.pk_table.name
        fk_keys = fk_table_map[table_name]
        for fk in fk_keys:
            if fk.pk_table.name == parent_table:
                if 'RID' in columns(fk.referenced_columns):
                    fk_column_name = columns(fk.foreign_key_columns)[columns(fk.referenced_columns).index('RID')]
                    rid_fk_column_name = parent_table[0].upper() + parent_table[1:] + '_RID'
                    if rid_fk_column_name != fk_column_name:
                        if table_name not in rename_columns_map.keys():
                            rename_columns_map[table_name] = {}
                        if fk_column_name not in rename_columns_map[table_name].keys():
                            rename_columns_map[table_name][fk_column_name] = rid_fk_column_name
                            rename_column(fw, table_name, fk_column_name, rid_fk_column_name, fk)
                            counter +=1
                    break

    print('{} COLUMNS TO BE RENAMED'.format(counter))

    fw.write('\n')

    """
    Gathers the columns to be added from the FK having 2 columns and RID as referenced column
    """
    counter = 0
    for key in keys:
        table_name = key.table.name
        parent_table = key.pk_table.name
        fk_keys = fk_table_map[table_name]
        found = False
        for fk in fk_keys:
            if fk.pk_table.name == parent_table:
                if 'RID' in columns(fk.referenced_columns):
                    found = True
                    break

        if found == False:
            rid_fk_column_name = parent_table[0].upper() + parent_table[1:] + '_RID'
            if rid_fk_column_name not in columns_table_map[key.table.name]:
                addColumn(fw, key.table.name, rid_fk_column_name, key)
                counter +=1

    print('{} NEW COLUMNS'.format(counter))
    
    fw.write('\n')

    check_exist(pk_keys, 'struct_primary_key')
    add_primary_key(fw, 'struct', 'struct_primary_key', ['entity_id'])

    """
    Gathers the PK to be added from the FK having 2 columns and structure_id as referenced column
    """
    keys = get_fk(2, structure_id=True)
    counter = 1
    for key in keys:
        cols = ['RID'] + columns(key.referenced_columns)
        if exists_primary_key(key.pk_table.name, cols) == False:
            constraint_name = '{}_combo1_key'.format(key.pk_table.name)
            check_exist(pk_keys, constraint_name)
            add_primary_key(fw, key.pk_table.name, constraint_name, cols)
            counter +=1

    print('{} NEW PRIMARY KEYS'.format(counter))

    fw.write('\n')

    counter = 1
    keys = get_pk(1)
    if len(keys) != 1:
        print('Unexpected number of keys with 1 column different of "RID": expected 1, got {}'.format(len(keys)))
    check_exist(pk_keys, 'entry_id_primary_key')
    rename_primary_key(fw, keys[0], 'entry_id_primary_key')

    """
    Gathers the PK to be renamed from the PK having 2 columns and RID as a column
    """
    keys = get_pk(2, RID=True)
    for key in keys:
        combo2 = '{}_combo2_key'.format(key.table.name)
        check_exist(pk_keys, combo2)
        rename_primary_key(fw, key, combo2)
        counter +=1

    print('{} RENAMED PRIMARY KEYS'.format(counter))

    for constraint_name in pk_keys:
        if len(constraint_name) > 63:
            print('{} has length = {}'.format(constraint_name, len(constraint_name)))

    fw.write('\n')

    counter = 0
    check_exist(fk_keys, 'Entry_Related_File_structure_id_fkey')
    key = fk_map['Entry_Related_File_entry_id_fkey']
    rename_foreign_key(fw, key, 'Entry_Related_File_structure_id_fkey')
    counter +=1
    
    """
    Rename the FK having 4 columns with structure_id in the referenced columns and not RID in the referenced columns to combo1
    """
    keys = get_fk(4, structure_id=True)
    for key in keys:
        combo1 = '{}_{}_combo1_fkey'.format(key.table.name, key.pk_table.name)
        check_exist(fk_keys, combo1, warning= False)
        rename_foreign_key(fw, key, combo1)
        counter +=1

    """
    Rename the FK having 2 columns with RID in the referenced columns and not structure_id in the referenced columns to combo2
    """
    keys = get_fk(2, RID=True)
    for key in keys:
        combo2 = '{}_{}_combo2_fkey'.format(key.table.name, key.pk_table.name)
        check_exist(fk_keys, combo2, warning= False)
        rename_foreign_key(fw, key, combo2)
        counter +=1

    print('{} FOREIGN KEY RENAMED'.format(counter))

    fw.write('\n')

    """
    Add the FK having 2 columns with structure_id in the referenced columns and not RID in the referenced columns to combo1
    """
    keys = get_fk(2, structure_id=True)
    counter = 0
    for key in keys:
        combo1 = '{}_{}_combo1_fkey'.format(key.table.name, key.pk_table.name)
        check_exist(fk_keys, combo1, warning= False)
        add_foreign_key(fw, key, combo1)
        counter +=1

    print('{} NEW FOREIGN KEYS'.format(counter))
    
    fw.write('\n')
    
    """
    Drop the FK having 2 columns with structure_id in the referenced columns and not RID in the referenced columns to combo1
    """
    keys = get_fk(2, structure_id=True)
    counter = 0
    for key in keys:
        drop_foreign_key(fw, key)
        counter +=1

    print('{} FOREIGN KEYS TO BE DROPPED'.format(counter))
    
    fw.write('\n')
    
    """
    Check duplicates
    """
    counter = 0
    for table_name in new_fk_map.keys():
        for constraint_name, values in new_fk_map[table_name].items():
            if len(values) > 1:
                counter += len(values) - 1
                for value in values:
                    fw.write('DUPLICATE FOREIGN KEY {}: {}{} --> {}{}\n'.format(constraint_name, table_name, value['foreign_key_columns'], value['parent_table'], value['referenced_columns']))
                fw.write('\n')

    for table_name in fk_rename.keys():
        for constraint_name, values in fk_rename[table_name].items():
            if len(values) > 1:
                counter += len(values) - 1
                for value in values:
                    fw.write('DUPLICATE FOREIGN KEY {}: {}{} --> {}{}\n'.format(constraint_name, table_name, value['foreign_key_columns'], value['parent_table'], value['referenced_columns']))
                fw.write('\n')

    print('{} DUPLICATE FOREIGN KEYS'.format(counter))
    
    """
    Check FK length
    """
    counter = 0
    for table_name in new_fk_map.keys():
        for constraint_name in new_fk_map[table_name].keys():
            if len(constraint_name) > 63:
                fw.write('FOREIGN KEY {} HAS LENGTH {}\n'.format(constraint_name, len(constraint_name)))
                counter +=1

    for table_name in fk_rename.keys():
        for constraint_name in fk_rename[table_name].keys():
            if len(constraint_name) > 63:
                fw.write('FOREIGN KEY {} HAS LENGTH {}\n'.format(constraint_name, len(constraint_name)))
                counter +=1

    print('{} FOREIGN KEYS HAVE LENGTH GREATER THAN 63'.format(counter))
    
    fw.close()

def generate_fk_fkey(schema):
    fw = open('fk_fkey.txt', 'w')
    for table_name in schema.tables:
        table = schema.tables[table_name]
        constraints = {}
        for key_name in table.foreign_keys.elements:
            key = table.foreign_keys[key_name]
            constraints[key.constraint_name] = key
        fk = []
        for key in constraints.keys():
            if key[-3:] == '_fk':
                fk.append(key)
        for key_name in fk:
            fkey = key_name + 'ey'
            if fkey in constraints.keys():
                key = constraints[key_name]
                fw.write('{}:   {}{} --> {}{}\n'.format(key_name, key.table.name, columns(key.foreign_key_columns), key.pk_table.name, columns(key.referenced_columns)))
                key = constraints[fkey]
                fw.write('{}: {}{} --> {}{}\n\n'.format(fkey, key.table.name, columns(key.foreign_key_columns), key.pk_table.name, columns(key.referenced_columns)))
    fw.close()
   

def generate_annotations_fkey(schema):
    def get_fkey_annotations(context, annotation, fkey, result, check=True):
        if type(annotation).__name__ == 'str':
            if check == True:
                if annotation == fkey:
                    result.append(' : '.join(context))
            else:
                result.append(' : '.join(context))
        elif type(annotation).__name__ == 'dict':
            for key, values in annotation.items():
                new_context = context.copy()
                new_context.extend([key])
                get_fkey_annotations(new_context, values, fkey, result, check=check)
        elif type(annotation).__name__ == 'list':
            for values in annotation:
                get_fkey_annotations(context, values, fkey, result, check=check)
                
    fw = open('fk_annotations.txt', 'w')
    constraints = {}
    fk_orphans_table_annotations = {}
    fk_orphans_annotations = {}

    for table_name in schema.tables:
        constraints[table_name] = {}
        table = schema.tables[table_name]
        for key_name in table.foreign_keys.elements:
            key = table.foreign_keys[key_name]
            if key.pk_table.schema.name == 'PDB':
                constraints[table_name][key.constraint_name] = {'key': key, 'annotations': {'Table': [], 'ForeignKey': []}}

    counter = 0
    for table_name in schema.tables:
        for fkey in constraints[table_name].keys():
            annotations = []
            get_fkey_annotations([], schema.tables[table_name].annotations, fkey, annotations)
            key = constraints[table_name][fkey]['key']
            if len(annotations) > 0:
                constraints[table_name][fkey]['annotations']['Table'] = annotations
                counter +=1
            else:
                if table_name not in fk_orphans_table_annotations.keys():
                    fk_orphans_table_annotations[table_name] = []
                fk_orphans_table_annotations[table_name].append(key)

    print('{} FOREIGN KEYS HAVE TABLE ANNOTATIONS'.format(counter))

    counter = 0
    for table_name in schema.tables:
        table = schema.tables[table_name]
        for key_name in table.foreign_keys.elements:
            key = table.foreign_keys[key_name]
            if key.pk_table.schema.name == 'PDB':
                annotations = []
                get_fkey_annotations([], key.annotations, key.constraint_name, annotations, check=False)
                if len(annotations) > 0:
                    constraints[table_name][key.constraint_name]['annotations']['ForeignKey'] = annotations
                    counter +=1
                else:
                    if table_name not in fk_orphans_table_annotations.keys() or key not in fk_orphans_table_annotations[table_name]:
                        if table_name not in fk_orphans_annotations.keys():
                            fk_orphans_annotations[table_name] = []
                        fk_orphans_annotations[table_name].append(key)

    print('{} FOREIGN KEYS ANNOTATIONS'.format(counter))

    for table_name in schema.tables:
        for constraint_name in constraints[table_name].keys():
            if (len(constraints[table_name][constraint_name]['annotations']['Table']) + len(constraints[table_name][constraint_name]['annotations']['ForeignKey'])) > 0:
                key = constraints[table_name][constraint_name]['key']
                fw.write('{}: {}{} --> {}{}\n'.format(key.constraint_name, key.table.name, columns(key.foreign_key_columns), key.pk_table.name, columns(key.referenced_columns)))
                for annotation in constraints[table_name][constraint_name]['annotations']['Table']:
                    fw.write('\tTABLE ANNOTATION: {}\n'.format(annotation))
                for annotation in constraints[table_name][constraint_name]['annotations']['ForeignKey']:
                    fw.write('\tFOREIGN KEY ANNOTATION: {}\n'.format(annotation))

    counter = 0
    fw.write('\n\nFOREIGN KEYS WITHOUT ANNOTATIONs:\n')
    for table_name, keys in fk_orphans_annotations.items():
        for key in keys:
            fw.write('\t{}: {}{} --> {}{}\n'.format(key.constraint_name, key.table.name, columns(key.foreign_key_columns), key.pk_table.name, columns(key.referenced_columns)))
            counter +=1

    print('{} FOREIGN KEYS W/O ANNOTATIONS'.format(counter))

    fw.close()
   
def generate_acl_bindings_fkey(schema):
    def get_fkey_acl_bindings(context, acl_bindings, fkey, result):
        if type(acl_bindings).__name__ == 'str':
            if acl_bindings == fkey:
                result.append(' : '.join(context))
        elif type(acl_bindings).__name__ == 'dict':
            for key, values in acl_bindings.items():
                new_context = context.copy()
                new_context.extend([key])
                get_fkey_acl_bindings(new_context, values, fkey, result)
        elif type(acl_bindings).__name__ == 'list':
            for values in acl_bindings:
                get_fkey_acl_bindings(context, values, fkey, result)
                
    fw = open('fk_acl_bindings.txt', 'w')
    constraints = {}
    for table_name in schema.tables:
        constraints[table_name] = {}
        table = schema.tables[table_name]
        for key_name in table.foreign_keys.elements:
            key = table.foreign_keys[key_name]
            if key.pk_table.schema.name == 'PDB':
                constraints[table_name][key.constraint_name] = {'key': key, 'acl_bindings': {'Table': []}}
    for table_name in schema.tables:
        for fkey in constraints[table_name].keys():
            acl_bindings = []
            get_fkey_acl_bindings([], dict (schema.tables[table_name].acl_bindings), fkey, acl_bindings)
            key = constraints[table_name][fkey]['key']
            if len(acl_bindings) > 0:
                constraints[table_name][fkey]['acl_bindings']['Table'] = acl_bindings

    for table_name in schema.tables:
        for constraint_name in constraints[table_name].keys():
            if len(constraints[table_name][constraint_name]['acl_bindings']['Table']) > 0:
                key = constraints[table_name][constraint_name]['key']
                fw.write('{}: {}{} --> {}{}\n'.format(key.constraint_name, key.table.name, columns(key.foreign_key_columns), key.pk_table.name, columns(key.referenced_columns)))
                for acl_bindings in constraints[table_name][constraint_name]['acl_bindings']['Table']:
                    fw.write('\tTABLE ACL BINDINGS: {}\n'.format(acl_bindings))
    fw.close()
   
def generate_mandatory(schema):
    fw = open('mandatory.txt', 'w')
    mandatory = {}
    not_mandatory = {}
    for table_name in schema.tables:
        table = schema.tables[table_name]
        for key_name in table.foreign_keys.elements:
            key = table.foreign_keys[key_name]
            if key.pk_table.schema.name == 'PDB':
                if 'structure_id' in columns(key.foreign_key_columns):
                    for col in key.foreign_key_columns:
                        if col.name != 'structure_id':
                            if col.nullok == False:
                                if table_name not in mandatory.keys():
                                    mandatory[table_name] = []
                                mandatory[table_name].append(key)
                            else:
                                if table_name not in not_mandatory.keys():
                                    not_mandatory[table_name] = []
                                not_mandatory[table_name].append(key)
    counter = 0
    if len(mandatory) > 0:
        fw.write('MANDATORY FOREIGN KEYS')
        for table_name, keys in mandatory.items():
            for key in keys:
                fw.write('\t{}:   {}{} --> {}{}\n'.format(key.constraint_name, key.table.name, columns(key.foreign_key_columns), key.pk_table.name, columns(key.referenced_columns)))
                counter +=1
        fw.write('\n')
    print('{} MANDATORY FOREIGN KEYS'.format(counter))

    counter = 0
    if len(not_mandatory) > 0:
        fw.write('OPTIONAL FOREIGN KEYS')
        for table_name, keys in not_mandatory.items():
            for key in keys:
                fw.write('\t{}:   {}{} --> {}{}\n'.format(key.constraint_name, key.table.name, columns(key.foreign_key_columns), key.pk_table.name, columns(key.referenced_columns)))
                counter +=1
        fw.write('\n')
    print('{} OPTIONAL FOREIGN KEYS'.format(counter))
    fw.close()
   
parser = argparse.ArgumentParser()
parser.add_argument('catalog_number')
parser.add_argument('schema_name')
parser.add_argument('action')

args = parser.parse_args()

catalog_number = args.catalog_number
schema_name = args.schema_name
action = args.action
hostname = 'pdb.isrd.isi.edu'

if action not in ['workflow', 'columns', 'primary_keys', 'foreign_keys', 'duplicates', 'long_names', 'all', 'fk_fkey', 'fk_annotations', 'fk_acl_bindings', 'mandatory']:
    print('Unknown action option: {}'.format(action))
    sys.exit(0)
    

credential = get_credential(hostname)
catalog_ermrest = ErmrestCatalog('https', hostname, catalog_number, credentials=credential)
catalog_ermrest.dcctx['cid'] = 'model'
model_root = catalog_ermrest.getCatalogModel()
schema = model_root.schemas[schema_name]

if action == 'fk_fkey':
    generate_fk_fkey(schema)
    sys.exit(0)
elif action == 'fk_annotations':
    generate_annotations_fkey(schema)
    sys.exit(0)
elif action == 'fk_acl_bindings':
    generate_acl_bindings_fkey(schema)
    sys.exit(0)
elif action == 'mandatory':
    generate_mandatory(schema)
    sys.exit(0)

setPK(schema)

setFK(schema)

setColumns(schema)

#print('max_pk_columns: {}'.format(max_pk_columns))
#print('max_fk_columns: {}'.format(max_fk_columns))

#write_key_and_foreign_key()

generate_workflow()

if action == 'columns':
    generate_columns()
elif action == 'primary_keys':
    generate_primary_keys()
elif action == 'foreign_keys':
    generate_foreign_keys()
elif action == 'duplicates':
    generate_duplicates()
elif action == 'long_names':
    generate_long_names()
elif action == 'all':
    generate_columns()
    generate_primary_keys()
    generate_foreign_keys()
    generate_duplicates()
    generate_long_names()
    generate_fk_fkey(schema)
    generate_annotations_fkey(schema)
    generate_acl_bindings_fkey(schema)
    generate_mandatory(schema)

sys.exit(0)



"""
map_table = {'string1': 'text1'}
test_string = 'string1 string11'

a = 'string1'
print(test_string.replace(a, map_table[a]))

map_table = {'"string1"': '"text1"'}
test_string = '"string1" "string11"'

a = '"string1"'
print(test_string.replace(a, map_table[a]))
python3 /home/serban/dependencies.py 99 PDB /home/serban/dump true
python3 /home/serban/dependencies.py 99 PDB /home/serban/dump false
"""


