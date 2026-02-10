#!/usr/bin/python
import json
from deriva.core import ErmrestCatalog, HatracStore, AttrDict, get_credential, DEFAULT_CREDENTIAL_FILE, tag, urlquote, DerivaServer, BaseCLI
from deriva.core.ermrest_model import builtin_types, Schema, Table, Column, Key, ForeignKey, tag, AttrDict
from deriva.utils.extras.data import insert_if_not_exist, update_table_rows, delete_table_rows, get_ermrest_query

#from pdb_dev.utils.shared import PDBDEV_CLI, DCCTX, cfg
from ...utils.shared import PDBDEV_CLI, DCCTX, cfg
from ..processor import ProcessingError, ErmrestError, ErmrestUpdateError, FileError


def is_mmcif_rid_mandatory_fkey(fkey):
    """Check whether the given fkey is a mandatory fkey.
    Assuming that structure_id is always required.
    if the referenced (parent) row RID and structure_id are part of fkey, then it is mandatory (e.g. combo1).

    Args:
        fkey (obj): ERMrest fkey object

    Return:
        bool : A boolean indicates whether the fkey is optiona.
    
    """
    to_cnames = [ col.name for col in fkey.column_map.values()]    
    if set(["RID", "structure_id"]).issubset(set(to_cnames)) or set(["RID", "entry_id"]).issubset(set(to_cnames)):
        return True
    else:
        return False

def is_mmcif_rid_optional_fkey(fkey):
    """Check whether the given fkey is an optional fkey.
    Assuming that structure_id is always required.
    if the referenced (parent) row RID is in fkey but not structure_id, then it is optional fkey (e.g. combo2).

    Args:
        fkey (obj): ERMrest fkey object

    Return:
        bool : A boolean indicates whether the fkey is optiona.
    """
    to_cnames = [ col.name for col in fkey.column_map.values()]
    if len(to_cnames) > 1 and "RID" in to_cnames and "structure_id" not in to_cnames and "entry_id" not in to_cnames:
        return True
    else:
        return False

def get_mmcif_rid_mandatory_fkeys(table):
    """Get mandatory (i.e. combo1) fkeys

    Args:
        table (obj): ERMrest table

    Returns:
        list: a list of optional fkeys
    """
    
    fkeys = []
    for fkey in table.foreign_keys:
        if is_mmcif_rid_mandatory_fkey(fkey):
            fkeys.append(fkey)
    return fkeys

def get_mmcif_rid_optional_fkeys(table):
    """
    combo2 equivalence

    Args:
        table (obj): ERMrest table

    Returns:
        list: a list of optional fkeys
    """
    fkeys = []
    for fkey in table.foreign_keys:
        if is_mmcif_rid_optional_fkey(fkey):
            fkeys.append(fkey)
    return fkeys


def print_table_fkeys(table):
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
        print_table_fkeys(table)

def check_entry_tables_fkeys(catalog, ignore_restraints=True):
    model = catalog.getCatalogModel()
    restraint_types = get_ermrest_query(catalog, "Vocab", "File_Type", constraints=None)
    restraint_tnames = [ row["Table_Name"] for row in restraint_types ]
    print("restraint_types: %s" % (len(restraint_tnames)))
    for tname, table in model.schemas["PDB"].tables.items():
        if ignore_restraints and tname in restraint_tnames: continue
        print_table_fkeys(table)        

def check_shared_fkey_columns(catalog, sname="PDB", skip_rid=True):
    model = catalog.getCatalogModel()
    cname2fkey_counts = {}
    cname2fkeys = {}
    for tname, table in model.schemas[sname].tables.items():
        cname2fkey_counts[tname] = {}
        cname2fkeys[tname] = {}
        for fkey in table.foreign_keys:
            pk_table = fkey.pk_table
            from_cnames = [ col.name for col in fkey.column_map.keys()]            
            to_cnames = [ col.name for col in fkey.column_map.values()]
            if skip_rid and "RID" in to_cnames: continue # only look for natural fkey
            if pk_table.schema.name == "Vocab": continue
            for cname in from_cnames:
                if cname in ["RMB", "RCB", "Owner"]: continue                
                cname2count = cname2fkey_counts[tname].setdefault(cname, 0)
                cname2fkey_counts[tname][cname] = cname2count+1
                cname2fkeys[tname].setdefault(cname, []).append(fkey)

    for tname, shared_cnames in cname2fkey_counts.items():
        print("\ntname: %s" % (tname))
        for k,v in shared_cnames.items():
            if v > 1 and k not in ["structure_id", "entry_id"]:
                cname_fkeys = [ fkey.constraint_name for fkey in cname2fkeys[tname][k] ]
                print("    !! %s : %d --> %s" % (k,v, cname_fkeys))
            else:
                print("    %s : %d" % (k,v))
        

# -- =================================================================================
# support for code to be deprecated in the future
#

def get_legacy_combo1_columns(catalog):
    """
    Create data structure of combo1 cnames expected by EntryProcessor.
    This is to replace what's generated by pdb_dev.config.apps.get_columns_end_with_rid.py.
    Example:
    {
        "ihm_relaxation_time_multi_state_scheme": {
            "Scheme_RID": {
                "ihm_multi_state_scheme": {
                    "scheme_id": "id"
                }
            },
            "Relaxation_Time_RID": {
                "ihm_relaxation_time": {
                    "relaxation_time_id": "id"
                }
            }
        },
    }
    """
    model = catalog.getCatalogModel()
    
    combo1_columns = {}
    for tname in sorted(model.schemas["PDB"].tables.keys()):
        table = model.schemas["PDB"].tables[tname]
        combo1_fkeys = get_mmcif_rid_mandatory_fkeys(table)
        if not combo1_fkeys: continue
        table_dict = combo1_columns.setdefault(tname, {})
        
        for fkey in combo1_fkeys:
            from_cnames = [ col.name for col in fkey.column_map.keys() ]        
            to_cnames = [ col.name for col in fkey.column_map.values() ]
            rid_index = to_cnames.index("RID")
            fkey_dict = table_dict.setdefault(from_cnames[rid_index], {})
            col_dict = fkey_dict.setdefault(fkey.pk_table.name, {})
            for i in range(0,len(from_cnames)):
                from_cname = from_cnames[i]
                to_cname = to_cnames[i]
                if to_cname == "RID" or from_cname == "structure_id": continue
                col_dict.update( {from_cname : to_cname} )
                
    #print("Legacy_combo1_cnames[%d]: ==> %s" % (len(combo1_columns.keys()), json.dumps(combo1_columns, indent=4)))

    if False:
        with open("/tmp/combo1_columns.json", "r") as f:
            combo1 = json.load(f)
        print("combo1 [%s]: %s" % (len(combo1.keys()), sorted(combo1.keys())))
    
    return combo1_columns

# ------------------------------------------------------------------
def get_legacy_optional_fks(catalog):
    """
    Create data structure of combo2 cnames expected by EntryProcessor.
    This is to replace what's generated by pdb_dev.config.apps.get_columns_end_with_rid.py.
    """
    model = catalog.getCatalogModel()
    optional_fks = {}
    for tname in sorted(model.schemas["PDB"].tables.keys()):
        table = model.schemas["PDB"].tables[tname]
        if tname[0].isupper(): continue   # not ihm tables
        combo2_fkeys = get_mmcif_rid_optional_fkeys(table)
        if not combo2_fkeys: continue
        fkey_rows = optional_fks.setdefault(tname, [])
            
        for fkey in combo2_fkeys:
            from_cnames = [ col.name for col in fkey.column_map.keys() ]        
            to_cnames = [ col.name for col in fkey.column_map.values() ]
            rid_index = to_cnames.index("RID")
            other_from_cnames = []
            other_to_cnames = []
            for i in range(0,len(from_cnames)):
                from_cname = from_cnames[i]
                to_cname = to_cnames[i]
                if to_cname == "RID" or from_cname == "structure_id": continue
                other_from_cnames.append(from_cname)
                other_to_cnames.append(to_cname)
            assert(len(other_from_cnames) == 1)
            
            fkey_dict = {
                "fk_columns" : from_cnames, 
                "ref_columns" : to_cnames,
                "ref_table" : fkey.pk_table.name,
                "fk_name": fkey.constraint_name,
                "ref_RID_column_name": "RID",                
                "ref_other_column_name": other_to_cnames[0],
                "fk_RID_column_name": from_cnames[rid_index],
                "fk_other_column_name": other_from_cnames[0],
                "url_structure_pattern": "/attribute/PDB:{}/{}={}&structure_id={}/RID?limit=1",
                "url_pattern": "/attribute/PDB:{}/{}={}/RID?limit=1"
            }
            fkey_rows.append(fkey_dict)
                
    #print("\nLegacy_optional_fks[%d]: ==> %s" % (len(optional_fks.keys()), json.dumps(optional_fks, indent=4)))

    if False:
        with open("/tmp/optional_fk.json", "r") as f:
            combo2 = json.load(f)
        print("combo2 [%s]: %s" % (len(combo2.keys()), sorted(combo2.keys())))
        print("combo2 [%s]: %s" % (len(combo2.keys()), json.dumps( { k: combo2[k] for k in sorted(combo2.keys()) }, indent=4) ))

    return optional_fks
    

# -- =================================================================================
# TODO: to be tested
#@dataclass
class PkTables(object):
    """
    - A class containing book-keeping params of model and data related to parent tables of combo1/2 fkeys 
    (fkeys that refers to parent table RID instead of natural fkeys without RID involved).
    - The goal is to create a data dict (kcvals2rows) that allow us to search the data row based on
    key column values without the RID. The key columns contain structure_id for combo1, and other
    natural key for combo2. This will allow us to extract row RID when preparing data payload for inserts.
    Note that Structure_id is used to filter the rows when obtaining the raw data for this lookup table.
    
    - convention:
      - cnames : column name,
      - ctname: constraint name  
      - kcnames: key column names
      - fk_ctname: fkey constraint names (referring to the fkey constraint pointing to the pk_table

    - Note: The code was originally written for processing csv files where all column values are all text.
    Therefore, the key values are all converted to type string when creating a dict.
    The payload originated from Ermrest or json files will have a proper type in place (e.g. int instead of text),
    so when performing a lookup, a string conversion needs to be applied.
    
    - TODO: convert csv raw values to proper type, then remove str conversion from dict creation and payload update.
    
    """

    mandatory_fkeys: bool = True
    optional_fkeys: bool = True
    
    # - create lookup tables based on keys used in fkey definition. The keys are sorted to get canonical key.
    fk_ctname_to_cname2from_cnames: dict = {}   # to_cname2from_cname group by inbould fkey constraint names to the pk_table
    fk_ctname2kcnames: dict = {}                # fkey constraint name to key cnames (without RID column)
    kcnames2fk_ctnames: dict = {}               # key cnames to fk constraint names
    kcnames_kcvals2rows: dict = {}              # key column values to row grouped by key cnames
    raw_data: dict = {}                         # raw data of individual table
    
    catalog: object = None
    verbose: boolean = True

    def __init__(self, catalog=None, mandatory_fkeys=True, optional_fkeys=True, raw_data=None):
        if catalog: self.catalog = catalog
        
        self.mandatory_fkeys=mandatory_fkeys
        self.optional_fkeys=optional_fkeys
        if raw_data: self.raw_data = raw_data

    
    # TODO: split data from model book keeping? 
    def prepare_model(self, table):
        """
        Param table: table containing combo1/2 fkeys that needs to be managed
        """
        combo_fkeys=[]
        if self.mandatory_fkeys: combo_fkeys.extend(get_mmcif_rid_mandatory_fkeys(table))
        if self.optional_fkeys: combo_fkeys.extend(get_mmcif_rid_optional_fkeys(table))
        print("prepare_model: combo_fkeys: %s" % (combo_fkeys))
        
        for fkey in combo_fkeys:
            pk_tname = fkey.pk_table.name
            from_cnames = [ col.name for col in fkey.column_map.keys() ]        
            to_cnames = [ col.name for col in fkey.column_map.values() ]
            print(" %s -> %s (%s): %s -> %s" % (table.name, pk_tname, fkey.constraint_name, from_cnames, to_cnames))
            to_cname2from_cnames = { to_col.name : from_col.name for from_col, to_col in fkey.column_map.items() }
            if self.verbose: print("fkey: name:%s %s -> %s : %s" % (fkey.constraint_name, from_cnames, pk_tname, to_cnames))
            rid_index = to_cnames.index("RID")

            # -- create key_cnames without RID; sorted for cannonical list
            to_cnames.remove("RID")
            key_cnames = tuple(sorted(to_cnames)) 

            # -- to_cname2from_cname of different fkey constraint
            self.fk_ctname_to_cname2from_cnames[pk_tname] = self.fk_ctname_to_cname2from_cnames.get(pk_tname, {})
            self.fk_ctname_to_cname2from_cnames[pk_tname][fkey.constraint_name] = to_cname2from_cnames

            # -- fkey constraint name to key cnames
            self.fk_ctname2kcnames[pk_tname] = self.fk_ctname2kcnames.get(pk_tname, {})
            self.fk_ctname2kcnames[pk_tname][fkey.constraint_name] = key_cnames

            # -- key cnames to fkey constraint names
            self.kcnames2fk_ctnames[pk_tname] = self.kcnames2fk_ctnames.get(pk_tname, {})
            self.kcnames2fk_ctnames[pk_tname][key_cnames] = self.kcnames2fk_ctnames[pk_tname].get(key_cnames, [])
            self.kcnames2fk_ctnames[pk_tname][key_cnames].append(fkey.constraint_name)
            
    def set_raw_data(self, raw_data):
        self.raw_data = raw_data
    
    def prepare_data(self, table):
        """
        Update kcnames_kcvals2rows, assuming that raw data is already available.
        Param: table: table containing combo1/2 fkeys that needs to be managed
        """
        combo_fkeys=[]
        if self.mandatory_fkeys: combo_fkeys.extend(get_mmcif_rid_mandatory_fkeys(table))
        if self.optional_fkeys: combo_fkeys.extend(get_mmcif_rid_optional_fkeys(table))
        
        for fkey in combo_fkeys:
            pk_tname = fkey.pk_table.name
            key_cnames = self.fk_ctname2kcnames[pk_tname][fkey.constraint_name]

            # -- key column values to individual rows group by key_column_name
            self.kcnames_kcvals2rows[pk_tname] = self.kcnames_kcvals2rows.get(pk_tname, {})
            if key_cnames in self.kcnames_kcvals2rows[pk_tname].keys(): continue  # pk_table_dict already generated
            if pk_tname not in self.raw_data.keys():
                print("\nWARNING: %s: There is no parent rows %s to extract RID from" % (table.name, pk_tname))
            else:
                cvals2rows = {}    # - create a dict based on cannonical key
                for row in self.raw_data[pk_tname]:
                    k = tuple([ str(row[cname]) for cname in key_cnames ])  # convert to text
                    cvals2rows[k] = row
                self.kcnames_kcvals2rows[pk_tname][key_cnames] = cvals2rows

    
    # note: if the structure in print statement is a tuple, need to convert to string first
    @classmethod
    def print_pk_tables_dict(cls, pk_table_dict, data_dict=False, limit=50):
        """
        limit puts a cap on the number of data rows to print
        """
        for pk_tname in pk_table_dict.keys():
            print("   - tname : %s" % pk_tname)
            for constraint_name in pk_table_dict[pk_tname].keys():
                if not data_dict:
                    print("      key name : %s" % (str(constraint_name)))
                    print("         %s" % (str(pk_table_dict[pk_tname][constraint_name])))
                    #print("         %s" % (json.dumps(pk_table_dict[pk_tname][constraint_name])))
                    continue
                count=0
                print("      key name : %s [%d]" % (str(constraint_name), len(pk_table_dict[pk_tname][constraint_name].keys())))
                for k,v in pk_table_dict[pk_tname][constraint_name].items():
                    print("        k: %s -> %s" % (k, json.dumps(v, indent=2)))
                    count+=1
                    if count >= limit: break

            
    def print_structures(self):
        """
        print structures
        """
        print("\npk_tables_fk_ctname2kcnames: %s ==>" % (self.fk_ctname2kcnames))
        self.print_pk_tables_dict(self.fk_ctname2kcnames, data_dict=False)
        
        print("\npk_tables_kcnames2fk_ctnames: ==> %s" % (self.kcnames2fk_ctnames))
        self.print_pk_tables_dict(self.kcnames2fk_ctnames, data_dict=False)
        
        print("\npk_tables_to_cname2from_cnames: ==>")
        self.print_pk_tables_dict(self.fk_ctname_to_cname2from_cnames, data_dict=True)
        
        print("\npk_tables_key2rows: ==> ")
        self.print_pk_tables_dict(self.kcnames_kcvals2rows, data_dict=True, limit=5)
        print("------------")
        

    def update_payload_with_rids(self, table, payload):
        """Update payload with RID columns

        Args:
            table (obj): ERMrest table object containing combo1/2 fkeys that needs to be managed
            payload (list): A list of rows to have their RID columns updated
        """
        if not payload: return
        
        combo_fkeys = get_mmcif_rid_optional_fkeys(table) + get_mmcif_rid_mandatory_fkeys(table)
        
        # not all columns in the model are in payload. Extract this to address optional column
        headers = payload[0].keys()
        
        # -for each fkey, fill in corresponding RID column
        for fkey in combo_fkeys:
            pk_tname = fkey.pk_table.name
            to_cname2from_cnames = self.fk_ctname_to_cname2from_cnames[pk_tname][fkey.constraint_name]
            key_cnames = self.fk_ctname2kcnames[pk_tname][fkey.constraint_name]
            key_from_cnames = [ to_cname2from_cnames[cname] for cname in key_cnames ]
            rid_cname = to_cname2from_cnames["RID"]
            # skip filling in rid of this fkey if the columns are missing
            skip_fkey = False
            for cname in key_from_cnames:
                if cname in headers: continue
                if table.columns[cname].nullok:
                    if self.verbose: print("missing optional fkey column: %s. Won't fill in RID column" % (cname))
                    skip_fkey=True
                    break
                else:
                    raise Exception("INPUT ERROR: table %s misses mandatory column %s" % (table.name, cname))
            if skip_fkey: continue
            if self.verbose: print("filling fkey: %s : %s -> %s : %s" % (fkey.constraint_name, key_from_cnames, pk_tname, key_cnames))
            for row in payload:
                kcvals2rows = self.kcnames_kcvals2rows[pk_tname][key_cnames]
                #print("kcvals2rows: %s" % (kcvals2rows))
                key = tuple([ str(row[cname]) for cname in key_from_cnames ])  # convert to str
                #print("key : %s <- %s" % (key, key_from_cnames))
                # In case of optional fkey, the key column could have null value. In this case, don't fill in RID value
                if None in key: continue
                if key not in kcvals2rows.keys():
                    raise Exception("DATA ERROR: reference table: %s, do not contain columns: %s with reference values: %s" % (pk_tname, key_cnames, str(key)))
                else:
                    row[rid_cname] = kcvals2rows[key]["RID"]
        
        
    def get_raw_data(self, catalog, from_tables, entry_id):
        """Get raw data from from_tables (tables containing mandatory/optional fkeys to be filled in).
        The pk_tables are consolidated into a single list to avoid redundant calls
        
        """
        pk_tables = []
        for table in from_tables:
            combo_fkeys = get_mmcif_rid_optional_fkeys(table) + get_mmcif_rid_mandatory_fkeys(table)
            print("get_raw_data: %s combo_fkeys: %s" % (table.name, [fkey.pk_table.name for fkey in combo_fkeys]))            
            for fkey in combo_fkeys:
                pk_table = fkey.pk_table
                if pk_table not in pk_tables: pk_tables.append(pk_table)

        print("get_raw_data: pk_tables: %s" % ([table.name for table in pk_tables]))
        # get raw data based on entry_id
        raw_data = {}
        try:
            for pk_table in pk_tables:
                if "structure_id" in pk_table.columns.elements:
                    raw_data[pk_table.name] = get_ermrest_query(catalog, "PDB", pk_table.name, "structure_id=%s" % (entry_id))
                elif "entry_id" in pk_table.columns.elements:
                    raw_data[pk_table.name] = get_ermrest_query(catalog, "PDB", pk_table.tname, "entry_id=%s" % (entry_id))
                else:
                    print("WARNING: can't form a query for table %s " % (pk_table.name))
        except Exception as e:
            raise ErmrestError("Unable to read data from parent tables of %s (%s)" % (pk_table.name, e))

        return raw_data
    
    
# -- =================================================================================
def main(server_name, catalog_id, credentials, args):
    server = DerivaServer('https', server_name, credentials)
    store = HatracStore('https', server_name, credentials)
    catalog = server.connect_ermrest(catalog_id)
    catalog.dcctx['cid'] = 'pipeline/pdb'
    model = catalog.getCatalogModel()

    check_shared_fkey_columns(catalog, sname="MA", skip_rid=False)
    
    #check_entry_tables_fkeys(catalog, ignore_restraints=True)

    #get_legacy_combo1_columns(catalog)
    #get_legacy_optional_fks(catalog)
    
    #pktables = PkTables()
    #for table in model.schemas["PDB"].tables:
    #    pktables.update_model(table)
    #pktables.print_structures()
    
 # -- =================================================================================
if __name__ == '__main__':
    args = PDBDEV_CLI("pdb-ihm", None, 1).parse_cli()
    credentials = get_credential(args.host, args.credential_file)
    main(args.host, args.catalog_id, credentials, args)
