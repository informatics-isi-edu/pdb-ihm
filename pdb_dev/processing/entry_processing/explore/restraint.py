#!/usr/bin/python3

import json
import sys
import os
import csv
import traceback
from deriva.core import ErmrestCatalog, HatracStore, AttrDict, get_credential, DEFAULT_CREDENTIAL_FILE, tag, urlquote, DerivaServer, BaseCLI
from deriva.core.ermrest_model import builtin_types, Schema, Table, Column, Key, ForeignKey, tag, AttrDict
from deriva.core import urlquote, urlunquote, DEFAULT_SESSION_CONFIG
from deriva.core.utils.hash_utils import compute_hashes

from pdb_dev.utils.shared import PDBDEV_CLI, DCCTX
from deriva.utils.extras.data import insert_if_not_exist, update_table_rows, delete_table_rows, get_ermrest_query

class ErmrestError(Exception):
    """ Exception when fail to perform transaction with Ermrest
    """
    
class ErmrestUpdateError(ErmrestError):
    """ Exception when fail to update to Ermrest
    """
    pass
    
# No array or jsonb column
# col.type.typename == col.type.__dict__["typename"]
# col.type.is_array == col.type.__dict__["is_array"]
def check_restraint_tables_column_types(catalog):
    model = catalog.getCatalogModel()
    file_types = get_ermrest_query(catalog, "Vocab", "File_Type", constraints=None)
    for row in file_types:
        table_name = row["Table_Name"]
        print("\ntable_name: %s --> " % (table_name))
        for col in model.schemas["PDB"].tables[table_name].columns:
            if col.type.is_array:
                print("  ! %s : %s - %s " % (col.name, col.type.typename, col.type.is_array))                
                continue
            if col.type.typename in ["json", "jsonb"]:
                print("  ! %s : %s - %s " % (col.name, col.type.typename, col.type.is_array))                                
                continue
            print("  - %s : %s - %s " % (col.name, col.type.typename, col.type.is_array))                                

# ======================================================================
def is_mmcif_mandatory_fkey(fkey):
    to_cnames = [ col.name for col in fkey.column_map.values()]    
    if set(["RID", "structure_id"]).issubset(set(to_cnames)) or set(["RID", "entry_id"]).issubset(set(to_cnames)):
        return True
    else:
        return False

def is_mmcif_optional_fkey(fkey):
    to_cnames = [ col.name for col in fkey.column_map.values()]
    if len(to_cnames) > 1 and "RID" in to_cnames and "structure_id" not in to_cnames and "entry_id" not in to_cnames:
        return True
    else:
        return False

def get_mandatory_fkeys(table):
    fkeys = []
    for fkey in table.foreign_keys():
        if is_mmcif_mandatory_fkey(fkey):
            fkeys.append(fkey)
    return fkeys

def get_mmcif_optional_fkeys(table):
    fkeys = []
    for fkey in table.foreign_keys:
        if is_mmcif_optional_fkey(fkey):
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
        if is_mmcif_mandatory_fkey(fkey):
            print("  1 combo1: %s -> %s : %s" % (from_cnames, pk_table.name, to_cnames))
        elif is_mmcif_optional_fkey(fkey):
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

# ======================================================================
def print_pk_tables_dict(pk_table_dict, data_dict=False):
    for pk_tname in pk_table_dict.keys():
        print("   - tname : %s" % pk_tname)
        for constraint_name in pk_table_dict[pk_tname].keys():
            print("      name : %s" % constraint_name)
            if not data_dict:
                print("         %s" % (pk_table_dict[pk_tname][constraint_name]))
                continue
            for k,v in pk_table_dict[pk_tname][constraint_name].items():
                print("        k: %s -> %s" % (k, json.dumps(v, indent=2)))
                
# ------------------------------------------------------------------
def handle_error(e, re_raise=False, subject=None):
    et, ev, tb = sys.exc_info()
    print('-- Got exception "%s: %s"' % (et.__name__, str(ev)))
    message = ''.join(traceback.format_exception(et, ev, tb))
    print('%s' % message)
    subject = '%s:%s : %s (%s)' % ("1234", 'DEPO', 'ERROR_PROCESSING_UPLOADED_mmCIF_FILE', 'x@gmail.org')
    #self.sendMail(subject, message)
    if re_raise: raise

# ------------------------------------------------------------------            
def loadTableFromCSV(catalog, fpath, delimiter, tname, entry_id, related_file_rid):
    model = catalog.getCatalogModel()
    table = model.schemas["PDB"].tables[tname]
    structure_id = entry_id
    entry_id = entry_id.replace("D_", "")
    
    """
    Empty the tname table of those with structure_id
    """
    constraints="structure_id=%s" % (structure_id)
    #rows = get_ermrest_query(catalog, "PDB", tname, constraints=constraints)

    #delete_table_rows(catalog, "PDB", tname, constraints=constraints)
    #self.logger.debug('Deleted rows from PDB:%s with constraints=%s' % (tname, constraints))

    # read csv file
    csvfile = open(fpath, 'r')
    reader = csv.DictReader(csvfile, delimiter=delimiter)
    headers = reader.fieldnames
    # check missing headers or unrecognized headers
    bad_headers = []
    for header in headers:
        if header not in table.columns.elements:
            print("header: %s is not a column" % (header))
            bad_headers.append(header)
    if bad_headers:
        print("ERROR: columns %s not found" % (bad_headers))        
        #raise Exception("ERROR: columns %s not found" % (bad_headers))

    """
    Create initial payload based on the file. "" is treated as NULL.
    Note: ermrest deals with text of int/float. No need to convert.
    """
    payload = []
    for row in reader:
        for k,v in row.items():
            #print("k: %s, type: %s, name: %s" % (k, table.columns[k].type, table.columns[k].type.__dict__["typename"]))
            if k not in table.columns.elements: continue
            type = table.columns[k].type.__dict__["typename"]
            if v == "":
                row[k] = None
            """ No need to convert
            elif type.startswith("int"):
                print("key: %s is an int" % (k))
                row[k] = int(v)
            elif type.startswith("float"):
                print("key: %s is an float" % (k))
                row[k] = float(v)
            """
            if "Structure_RID" in table.columns.elements:
                row["Structure_RID"] = entry_rid
        payload.append(row)
    csvfile.close()
    print(json.dumps(payload[0:2], indent=4))
    
    """
    Read content from needed parent tables, so RID can be obtained in bulk.
    pk_tables_raw: dict of corresponding payload based on table name
    """
    # - Prepare raw data from parent tables
    print_restraint_table_fkeys(table)    
    optional_fkeys = get_mmcif_optional_fkeys(table)
    #  - query parent tables once
    pk_tables_raw = {}  # raw data based on tname
    for fkey in optional_fkeys:
        pk_tname = fkey.pk_table.name
        if pk_tname in pk_tables_raw.keys(): continue
        pk_tables_raw[pk_tname] = get_ermrest_query(catalog, "PDB", pk_tname, "structure_id=%s" % (structure_id))
        
    # - create lookup tables based on keys used in fkey definition. The keys are sorted to get canonical key. 
    pk_tables_constraint2keys={}
    pk_tables_key2constraints={}
    pk_tables_to_cname2from_cnames={}
    # key value to row based on tname and key_cnames e.g. { tname : { ["group_id", "feature_id"] : { [1, 2] : row } } }    
    pk_tables_key2rows = {}     
    for fkey in optional_fkeys:
        pk_tname = fkey.pk_table.name
        from_cnames = [ col.name for col in fkey.column_map.keys() ]        
        to_cnames = [ col.name for col in fkey.column_map.values() ]
        to_cname2from_cnames = { to_col.name : from_col.name for from_col, to_col in fkey.column_map.items() }
        print("fkey: name:%s %s -> %s : %s" % (fkey.constraint_name, from_cnames, pk_tname, to_cnames))
        rid_index = to_cnames.index("RID")
        to_cnames.remove("RID")
        key_cnames = tuple(sorted(to_cnames))
        pk_tables_to_cname2from_cnames[pk_tname] = pk_tables_to_cname2from_cnames.get(pk_tname, {})
        pk_tables_to_cname2from_cnames[pk_tname][fkey.constraint_name] = to_cname2from_cnames
        pk_tables_constraint2keys[pk_tname] = pk_tables_constraint2keys.get(pk_tname, {})
        pk_tables_constraint2keys[pk_tname][fkey.constraint_name] = key_cnames        
        pk_tables_key2constraints[pk_tname] = pk_tables_key2constraints.get(pk_tname, {})
        pk_tables_key2constraints[pk_tname][key_cnames] = pk_tables_key2constraints[pk_tname].get(key_cnames, [])
        pk_tables_key2constraints[pk_tname][key_cnames].append(fkey.constraint_name)
        # - initialize 
        pk_tables_key2rows[pk_tname] = pk_tables_key2rows.get(pk_tname, {}) 
        if key_cnames in pk_tables_key2rows[pk_tname].keys(): continue # pk_table_dict already generated
        # -- create a dict based on cannonical key
        pk_table_dict = {}
        for row in pk_tables_raw[pk_tname]:
            k = tuple([ str(row[cname]) for cname in key_cnames ])  # convert to text
            pk_table_dict[k] = row
        pk_tables_key2rows[pk_tname][key_cnames] = pk_table_dict

    print("pk_tables_constraint2keys: %s ==>" % (pk_tables_constraint2keys))
    print_pk_tables_dict(pk_tables_constraint2keys, data_dict=False)
    
    print("pk_tables_key2constraints: ==> %s" % (pk_tables_key2constraints))
    print_pk_tables_dict(pk_tables_key2constraints, data_dict=False)
    
    #print("pk_tables_to_cname2from_cnames: %s" % (pk_tables_to_cname2from_cnames))
    print("pk_tables_to_cname2from_cnames: ==>")
    print_pk_tables_dict(pk_tables_to_cname2from_cnames, data_dict=True)
    
    #print("pk_tables_key2rows: %s" % (pk_tables_key2rows))
    print("pk_tables_key2rows: ==> ")
    print_pk_tables_dict(pk_tables_key2rows, data_dict=True)
        
    # - for each fkey, fill in corresponding RID column
    for fkey in optional_fkeys:
        pk_tname = fkey.pk_table.name
        rid_cname = pk_tables_to_cname2from_cnames[pk_tname][fkey.constraint_name]["RID"]
        key_cnames = pk_tables_constraint2keys[pk_tname][fkey.constraint_name]
        to_cname2from_cnames = pk_tables_to_cname2from_cnames[pk_tname][fkey.constraint_name]        
        key_from_cnames = [ to_cname2from_cnames[cname] for cname in key_cnames ]
        print("fkey: %s : %s -> %s : %s" % (fkey.constraint_name, key_from_cnames, pk_tname, key_cnames))
        for row in payload:
            pk_table_rows = pk_tables_key2rows[pk_tname][key_cnames]
            #print("pk_table_rows: %s" % (pk_table_rows))
            key = tuple([ row[cname] for cname in key_from_cnames ])
            print("key : %s <- %s" % (key, key_from_cnames))
            if None in key: continue
            row[rid_cname] = pk_table_rows[key]["RID"]
            
    print(json.dumps(payload[0:2], indent=4))

    # throw exception if insert fails
    try:
        insert_if_not_exist(catalog, "PDB", tname, payload)
    except:
        raise ErmrestUpdateError("ERROR")
        
# ======================================================================

def main(catalog, store):
    #check_restraint_tables_column_types(catalog)
    #check_restraint_tables_fkeys(catalog)
    #loadTableFromCSV(catalog, "Generic-Distance-Restraints-Between-Molecular-Features.tsv", "\t", "ihm_derived_distance_restraint", "D_3-6NBJ", "3-6NXA")
    #loadTableFromCSV(catalog, "Molecular-Features-Comprising-of-Polymeric-Residues-at-Interfaces.csv", ",", "ihm_interface_residue_feature", "D_1-SD46", "1-SDXT")    
    constraints = "RID=%s/B:=(M:RCB)=(public:ERMrest_Client:ID)/$M/T:=(M:File_Type)=(Vocab:File_Type:Name)" % ('1-SDXT')
    rows = get_ermrest_query(catalog, "PDB", "Entry_Related_File", constraints, attributes=['M:*','B:Email', 'B:Full_Name', 'T:Table_Name'])
    #rows = get_ermrest_query(catalog, "PDB", "Entry_Related_File", constraints=f'RID=1-SDXT/Vocab:File_Type', attributes=['Table_Name'])
    print(json.dumps(rows, indent=4))

    """
    try:
        raise Exception("Fail to update table xxx")
    except Exception as e:
        handle_error(e, re_raise=False)
    """
        
if __name__ == "__main__":
    cli = PDBDEV_CLI("pdbdev", None, 1)
    cli.parser.add_argument('--upload-path', help="directory containing entry generated files", default="/tmp/pdb/remediation_upload")
    
    args = cli.parse_cli()
    upload_path = args.upload_path
    credentials = get_credential(args.host, args.credential_file)
    catalog = ErmrestCatalog("https", args.host, args.catalog_id, credentials)
    catalog.dcctx['cid'] = DCCTX["cli/remedy"]
    store = HatracStore("https", args.host, credentials)
    main(catalog, store)


