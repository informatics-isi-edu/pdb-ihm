#!/usr/bin/python

import sys
import json
from deriva.core import ErmrestCatalog, AttrDict, get_credential, DEFAULT_CREDENTIAL_FILE, tag, urlquote, DerivaServer, get_credential, BaseCLI
from deriva.core.ermrest_model import builtin_types, Schema, Table, Column, Key, ForeignKey

#
# The purpose is to refactor the keys and forieng keys of the PDB table to conform to the naming convention.
#

# print all keys that [RID, structure_id] is a subset of
# key.name returns [schema_obj, constraint_name]
def print_rid_structure_id_keys(model):
    for table in model.schemas["PDB"].tables.values():
        for key in table.keys:
            #if set([ c.name for c in key.unique_columns ]).issubset({'RID', 'structure_id'}) == True:
            if {'RID', 'structure_id'}.issubset(set([ c.name for c in key.unique_columns ])) == True:                                   
                print("%s %s: %s" % (table.name, key.constraint_name, set([ c.name for c in key.unique_columns ])))


# rename these incorrect key constraint
def print_keys_with_rid(model):
    # all composite keys contains [RID, structure_id] 
    for table in model.schemas["PDB"].tables.values():
        for key in table.keys:
            key_length = len(key.columns)
            if (key_length >= 2) and ({'RID'}.issubset(set([ c.name for c in key.unique_columns ])) == True):
                if ({'structure_id'}.issubset(set([ c.name for c in key.unique_columns ])) == True):
                    key_name = "_".join([table.name, 'combo1_key'])
                    if key.constraint_name == key_name:
                        print("++    [%d] %s %s : %s" % (key_length, table.name, key.constraint_name, set([ c.name for c in key.unique_columns ])))
                    else:
                        # need correction
                        print("++ ** [%d] %s %s => %s : %s" % (key_length, table.name, key.constraint_name, key_name, set([ c.name for c in key.unique_columns ])))

    # all composite keys contains RID but not structure_id
    for table in model.schemas["PDB"].tables.values():
        for key in table.keys:
            key_length = len(key.columns)
            if (key_length >= 2) and ({'RID'}.issubset(set([ c.name for c in key.unique_columns ])) == True):
                if ({'structure_id'}.issubset(set([ c.name for c in key.unique_columns ])) == False):
                    key_name = "_".join([table.name, 'combo2_key'])
                    if key.constraint_name == key_name:
                        print("--    [%d] %s %s : %s" % (key_length, table.name, key.constraint_name, set([ c.name for c in key.unique_columns ])))
                    else:
                        # need correction
                        print("-- ** [%d] %s %s => %s : %s" % (key_length, table.name, key.constraint_name, key_name, set([ c.name for c in key.unique_columns ])))


def print_fkeys_with_rid(model, ncols, exclude_deriva=True):
    schema = model.schemas["PDB"]
    deriva_tables = {'Catalog_Group', 'ERMrest_Client', 'Entry_Related_File'}
    for table in schema.tables.values():
        for fkey in table.foreign_keys:
            fkey_length = len(fkey.columns)
            column_map_values = {c.name for c in fkey.column_map.values()}
            column_map_keys = {c.name for c in fkey.column_map.keys()}
            pk_table = fkey.pk_table
            
            # only look at fkeys to PDB schema (not Vocab)
            if fkey.pk_table.schema.name != 'PDB':
                continue
            
            # focus on a particular number of columns
            if (fkey_length != ncols):
                continue
            
            # combo1 or combo2 fkeys
            if ('RID' in column_map_values):
                # check for column_name corresponding to RID in the parent table
                for from_col, to_col in fkey.column_map.items():
                    if to_col.name == 'RID':
                        primary_cnames = column_map_keys - {from_col.name}
                        
                # -- combo1 
                if ('structure_id' in column_map_values):
                    # check whether primiary key still exists                    
                    if list(table.fkeys_by_columns(primary_cnames, raise_nomatch=False)):                    
                        print("-c1  p+  [%d] %s -> %s : %s : %s -> %s" % (fkey_length, table.name, fkey.pk_table.name, fkey.constraint_name, column_map_keys, column_map_values))
                        # TODO: for ncols=2, delete corresponding primary key from the model. Somehow some are deleted but some are still present. 
                    else:
                        print("-c1      [%d] %s -> %s : %s : %s -> %s" % (fkey_length, table.name, fkey.pk_table.name, fkey.constraint_name, column_map_keys, column_map_values))
                # -- combo2 case                
                else:
                    primary_cnames = primary_cnames | {'structure_id'}
                    # check whether primiary key still exists                                        
                    if list(table.fkeys_by_columns(primary_cnames, raise_nomatch=False)):
                        print("-c2  p+  [%d] %s -> %s : %s : %s -> %s --> p%s" % (fkey_length, table.name, fkey.pk_table.name, fkey.constraint_name, column_map_keys, column_map_values, primary_cnames))
                        # TODO: for ncols=2, delete corresponding primary key from the model. Somehow some are deleted but some are still present. 
                    else:
                        print("-c2      [%d] %s -> %s : %s : %s -> %s -- p%s" % (fkey_length, table.name, fkey.pk_table.name, fkey.constraint_name, column_map_keys, column_map_values, primary_cnames))
                    
            # primary key with structure_id or other kinds
            else :
                # -- normal composite key
                if ('structure_id' in column_map_values):
                    print("--p      [%d] %s -> %s : %s : %s -> %s" % (fkey_length, table.name, fkey.pk_table.name, fkey.constraint_name, column_map_keys, column_map_values))
                    # TODO: create a lookup table for long table names
                    # can't check for combo1/2 since the parent_table RID column is not known. Some tables have shorter name lookup
                    
                    # 1. determine whether it is combo1 or combo2:
                    # Except for structure_id, if a column in the key is not-null, then it is mandatory
                    mandatory = False
                    for col in fkey.column_map:
                        # exclude structure_id 
                        if col.name == 'structure_id':
                            continue
                        if col.nullok == False:
                            mandatory = True
                            break
                        
                    # 2. setup variables
                    if mandatory == True:
                        expected_fkey_column_names = column_map_keys|{parent_rid}
                        expected_fkey_parent_column_names = column_map_values|{'RID'}
                        flag = '1'
                    else:
                        expected_fkey_column_names = (column_map_keys|{parent_rid})-{'structure_id'}
                        expected_fkey_parent_column_names = (column_map_values|{'RID'})-{'structure_id'}
                        flag = '2'
                    expected_fkey_constraint_name = '_'.join([fkey.table.name, pk_table.name, 'combo'+flag, 'fkey'])
                    expected_parent_key_name = '_'.join([pk_table.name + 'combo'+flag, 'key'])
                    parent_rid = fkey.pk_table.name.capitalize() + '_RID'
                    
                    # 3. check parent column in the table
                    if parent_rid not in table.columns.elements:
                        # TODO: add column
                        print("    col: Add new column: %s.%s for fkey %s:%s" % (table.name, parent_rid, fkey.constraint_name, column_map_keys))
                                        

                    # 4. check whether expected key exist in the parent table
                    if fkey.pk_table.key_by_columns(expected_fkey_parent_column_names, raise_nomatch=False) is None:
                        print("    key: c%s %s %s:%s doesn't exist" % (flag, pk_table.name, expected_parent_key_name, expected_fkey_parent_column_names))
                                                        
                    # 5. create fkey if not exist                    
                    found = False
                    
                    # 5.1 check whether it already exist. If not, create
                    for fk in table.foreign_keys:
                        if found == True:
                            break
                        
                        # exclude fkey to other tables
                        if fk.pk_table != pk_table:
                            continue
                        
                        # look for fk with 'RID' in it.
                        fk_column_map_values = {c.name for c in fk.column_map.values()}
                        if 'RID' in fk_column_map_values:
                            if fk_column_map_values == expected_fkey_parent_column_names:
                                found = True
                                print("--p  c%s+ [%d] %s -> %s : %s : %s -> %s" % (flag, fkey_length, table.name, fkey.pk_table.name, fkey.constraint_name, column_map_keys, column_map_values))                                     
                            else:
                                print("ERROR: found 'RID' fkey but not combo%s in %s -> %s : %s : %s -> %s" % (flag, table.name, pk_table.name, fk.constraint_name, {c.name for c in fk.column_map.keys()}, {c.name for c in fk.column_map.values()}))
                                
                    # 5.2 if not found, create a combo1/comb2 fkey
                    if not found:
                        # TODO: create a new fkey
                        # print("--p  c%s [%d] %s -> %s : %s : %s -> %s" % (flag, fkey_length, table.name, fkey.pk_table.name, fkey.constraint_name, column_map_keys, column_map_values))
                        print("    *c%s  [%d] %s -> %s : %s : %s -> %s" % (flag, fkey_length, table.name, fkey.pk_table.name, expected_fkey_constraint_name, expected_fkey_column_names, expected_fkey_parent_column_names))
                        
                # -- single keys or composite keys without structure_id (which should be none)
                else:
                    if fkey.pk_table.name not in deriva_tables or exclude_deriva == False:
                        print("---       [%d] %s -> %s : %s : %s -> %s" % (fkey_length, table.name, fkey.pk_table.name, fkey.constraint_name, column_map_keys, column_map_values))


# fix inconsistant naming
# Entry_Related_File:
#  column name:
#    structure_id -> Structure_Id
#  change fkey name to be consistent with convention
#    "Entry_Related_File_entry_id_fkey" FOREIGN KEY (structure_id) REFERENCES "PDB".entry(id) ON UPDATE CASCADE ON DELETE CASCADE
#    "Entry_Related_File_process_status_fkey" FOREIGN KEY ("Process_Status") REFERENCES "Vocab".process_status("Name") ON UPDATE CASCADE ON DELETE SET NULL
#    "Entry_Related_File_workflow_status_fkey" FOREIGN KEY ("Workflow_Status") REFERENCES "Vocab".workflow_status("Name") ON UPDATE CASCADE


def main(server_name, catalog_id, credentials):
    server = DerivaServer('https', server_name, credentials)
    catalog = server.connect_ermrest(catalog_id)
    catalog.dcctx['cid'] = "oneoff/model"
    model = catalog.getCatalogModel()

    print_fkeys_with_rid(model, 2)
 
        

if __name__ == '__main__':
    args = BaseCLI("ad-hoc table creation tool", None, 1).parse_cli()
    credentials = get_credential(args.host, args.credential_file)
    main(args.host, 99, credentials)
