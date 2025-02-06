#!/usr/bin/python
import json
from deriva.core import ErmrestCatalog, HatracStore, AttrDict, get_credential, DEFAULT_CREDENTIAL_FILE, tag, urlquote, DerivaServer, BaseCLI
from deriva.core.ermrest_model import builtin_types, Schema, Table, Column, Key, ForeignKey, tag, AttrDict
from deriva.utils.extras.data import insert_if_not_exist, update_table_rows, delete_table_rows, get_ermrest_query

#from pdb_dev.utils.shared import PDBDEV_CLI, DCCTX, cfg
from ...utils.shared import PDBDEV_CLI, DCCTX, cfg


def is_mmcif_rid_mandatory_fkey(fkey):
    to_cnames = [ col.name for col in fkey.column_map.values()]    
    if set(["RID", "structure_id"]).issubset(set(to_cnames)) or set(["RID", "entry_id"]).issubset(set(to_cnames)):
        return True
    else:
        return False

def is_mmcif_rid_optional_fkey(fkey):
    to_cnames = [ col.name for col in fkey.column_map.values()]
    if len(to_cnames) > 1 and "RID" in to_cnames and "structure_id" not in to_cnames and "entry_id" not in to_cnames:
        return True
    else:
        return False

def get_mmcif_rid_mandatory_fkeys(table):
    """
    combo1 equivalence
    """
    fkeys = []
    for fkey in table.foreign_keys:
        if is_mmcif_rid_mandatory_fkey(fkey):
            fkeys.append(fkey)
    return fkeys

def get_mmcif_rid_optional_fkeys(table):
    """
    combo2 equivalence
    """
    fkeys = []
    for fkey in table.foreign_keys:
        if is_mmcif_rid_optional_fkey(fkey):
            fkeys.append(fkey)
    return fkeys


def print_restraint_table_fkeys(table):
    print("\ntable_name: %s --> " % (table.name))    
    for fkey in table.foreign_keys:
        pk_table = fkey.pk_table
        from_cnames = [ col.name for col in fkey.column_map.keys()]            
        to_cnames = [ col.name for col in fkey.column_map.values()]
        if fkey.pk_table.schema.name not in ["PDB"]: continue
        if fkey.pk_table.name in ["Entry_Related_File"]: continue            
        if is_mmcif_rid_mandatory_fkey(fkey):
            print("  1 combo1: %s -> %s : %s" % (from_cnames, pk_table.name, to_cnames))
        elif is_mmcif_rid_optional_fkey(fkey):
            print("  2 combo2: %s -> %s : %s" % (from_cnames, pk_table.name, to_cnames))
        else:
            print("  - no combo: %s -> %s : %s" % (from_cnames, pk_table.name, to_cnames))
            
def check_restraint_tables_fkeys(catalog):
    model = catalog.getCatalogModel()
    file_types = get_ermrest_query(catalog, "Vocab", "File_Type", constraints=None)    
    for row in file_types:
        tname = row["Table_Name"]
        table = model.schemas["PDB"].tables[tname]
        print_restraint_table_fkeys(table)

# -- =================================================================================
def main(server_name, catalog_id, credentials, args):
    server = DerivaServer('https', server_name, credentials)
    store = HatracStore('https', server_name, credentials)
    catalog = server.connect_ermrest(catalog_id)
    catalog.dcctx['cid'] = 'pipeline/pdb'
    model = catalog.getCatalogModel()
    
    check_restraint_tables_fkeys(catalog)

 # -- =================================================================================
if __name__ == '__main__':
    args = PDBDEV_CLI("pdb-ihm", None, 1).parse_cli()
    credentials = get_credential(args.host, args.credential_file)
    main(args.host, args.catalog_id, credentials, args)
