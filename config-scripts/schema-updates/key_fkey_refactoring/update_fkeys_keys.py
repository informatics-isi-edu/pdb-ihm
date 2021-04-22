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
            fkey_parent_col_names = {c.name for c in fkey.column_map.values()}
            fkey_col_names = {c.name for c in fkey.column_map.keys()}
            pk_table = fkey.pk_table
            
            # only look at fkeys to PDB schema (not Vocab)
            if fkey.pk_table.schema.name != 'PDB':
                continue
            
            # focus on a particular number of columns
            if (fkey_length != ncols):
                continue
            
            # combo1 or combo2 fkeys
            if ('RID' in fkey_parent_col_names):
                # check for column_name corresponding to RID in the parent table
                for from_col, to_col in fkey.column_map.items():
                    if to_col.name == 'RID':
                        primary_col_names = fkey_col_names - {from_col.name}
                        
                # -- combo1 
                if ('structure_id' in fkey_parent_col_names):
                    # check whether primiary key still exists                    
                    if list(table.fkeys_by_columns(primary_col_names, raise_nomatch=False)):                    
                        print("-c1  p  [%d] %s -> %s : %s : %s -> %s" % (fkey_length, table.name, fkey.pk_table.name, fkey.constraint_name, fkey_col_names, fkey_parent_col_names))
                        # TODO: for ncols=2, delete corresponding primary key from the model. Somehow some are deleted but some are still present. 
                    else:
                        print("-c1      [%d] %s -> %s : %s : %s -> %s" % (fkey_length, table.name, fkey.pk_table.name, fkey.constraint_name, fkey_col_names, fkey_parent_col_names))
                # -- combo2 case                
                else:
                    primary_col_names = primary_col_names | {'structure_id'}
                    # check whether primiary key still exists                                        
                    if list(table.fkeys_by_columns(primary_col_names, raise_nomatch=False)):
                        print("-c2  p  [%d] %s -> %s : %s : %s -> %s --> p%s" % (fkey_length, table.name, fkey.pk_table.name, fkey.constraint_name, fkey_col_names, fkey_parent_col_names, primary_col_names))
                        # TODO: for ncols=2, delete corresponding primary key from the model. Somehow some are deleted but some are still present. 
                    else:
                        print("-c2      [%d] %s -> %s : %s : %s -> %s -- p%s" % (fkey_length, table.name, fkey.pk_table.name, fkey.constraint_name, fkey_col_names, fkey_parent_col_names, primary_col_names))
                    
            # primary key with structure_id or other kinds
            else :
                # -- normal composite key
                if ('structure_id' in fkey_parent_col_names):
                    # TODO: create a lookup table for long table names
                    # can't check for combo1/2 since the parent_table RID column is not known. Some tables have shorter name lookup
                    
                    # 1. determine whether it needs combo1 or combo2:
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
                    parent_rid = fkey.pk_table.name.capitalize() + '_RID'
                    if mandatory == True:
                        expected_fkey_column_names = fkey_col_names|{parent_rid}
                        expected_fkey_parent_column_names = fkey_parent_col_names|{'RID'}
                        flag = '1'
                    else:
                        expected_fkey_column_names = (fkey_col_names|{parent_rid})-{'structure_id'}
                        expected_fkey_parent_column_names = (fkey_parent_col_names|{'RID'})-{'structure_id'}
                        flag = '2'
                    expected_fkey_constraint_name = '_'.join([fkey.table.name, pk_table.name, 'combo'+flag, 'fkey'])
                    expected_parent_key_name = '_'.join([pk_table.name, 'combo'+flag, 'key'])

                    # 3. check whether the combo fkeys already exist.
                    found = False                    
                    for fk in table.foreign_keys:
                        if found == True:
                            break
                        
                        # exclude fkey to other tables
                        if fk.pk_table != pk_table:
                            continue
                        
                        # look for fk with 'RID' in it.
                        fk_parent_col_names = {c.name for c in fk.column_map.values()}
                        if 'RID' in fk_parent_col_names:
                            if fk_parent_col_names == expected_fkey_parent_column_names:
                                found = True
                                print("--p  c%s [%d] %s -> %s : %s : %s -> %s" % (flag, fkey_length, table.name, fkey.pk_table.name, fkey.constraint_name, fkey_col_names, fkey_parent_col_names))
                            else:
                                print("ERROR: found 'RID' fkey but not combo%s in %s -> %s : %s : %s -> %s" % (flag, table.name, pk_table.name, fk.constraint_name, {c.name for c in fk.column_map.keys()}, {c.name for c in fk.column_map.values()}))

                    if not found:
                        print("--p      [%d] %s -> %s : %s : %s -> %s" % (fkey_length, table.name, fkey.pk_table.name, fkey.constraint_name, fkey_col_names, fkey_parent_col_names))
                    
                    # 4. check whether there are multiple fkeys pointing to the same parent table.
                    dup_fkey_parent = False
                    for fk in table.foreign_keys:
                        if dup_fkey_parent == True:
                            break
                        # exclude fkey to other tables or its own
                        if fk.pk_table != pk_table or fkey == fk:
                            continue
                        fk_parent_col_names = {c.name for c in fk.column_map.values()}
                        if 'RID' not in fk_parent_col_names:
                            dup_fkey_parent = True
                            print("    *dup: %s -> %s : %s vs %s : %s->%s" % (table.name, pk_table.name, fk.constraint_name, fkey.constraint_name, {c.name for c in fk.column_map.keys()}, {c.name for c in fk.column_map.values()}))
                            # break
                        
                    # 5. if combo fkeys not found, create a combo1/comb2 fkey
                    # NOTE: Multiple fkeys pointing to the same parent table shuld probably be handled manually. Need lookup table.
                    if not found:
                        
                        # 5.1 check parent column in the table
                        if parent_rid not in table.columns.elements:
                            # TODO: add column
                            print("    +col: Add new column: %s.%s for fkey %s:%s" % (table.name, parent_rid, fkey.constraint_name, fkey_col_names))
                                        
                        # 5.2 check whether expected key exist in the parent table
                        if fkey.pk_table.key_by_columns(expected_fkey_parent_column_names, raise_nomatch=False) is None:
                            print("    *key: c%s create %s %s:%s" % (flag, pk_table.name, expected_parent_key_name, expected_fkey_parent_column_names))
                                                        
                        
                        # 5.3 create a new fkey
                        # print("--p  c%s [%d] %s -> %s : %s : %s -> %s" % (flag, fkey_length, table.name, fkey.pk_table.name, fkey.constraint_name, fkey_col_names, fkey_parent_col_names))
                        print("    +c%s  [%d] %s -> %s : %s : %s -> %s" % (flag, fkey_length, table.name, fkey.pk_table.name, expected_fkey_constraint_name, expected_fkey_column_names, expected_fkey_parent_column_names))
                        
                # -- single keys or composite keys without structure_id (which should be none)
                else:
                    if fkey.pk_table.name not in deriva_tables or exclude_deriva == False:
                        print("---       [%d] %s -> %s : %s : %s -> %s" % (fkey_length, table.name, fkey.pk_table.name, fkey.constraint_name, fkey_col_names, fkey_parent_col_names))


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
