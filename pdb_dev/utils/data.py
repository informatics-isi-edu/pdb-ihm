import sys
import json
import logging
from deriva.core import ErmrestCatalog, AttrDict, get_credential, DEFAULT_CREDENTIAL_FILE, tag, urlquote, DerivaServer, \
    get_credential, BaseCLI, topo_sorted, topo_ranked
from deriva.core.ermrest_model import builtin_types, Schema, Table, Column, Key, ForeignKey, DomainType, ArrayType

from deriva.utils.extras.data import get_ermrest_query, update_table_rows, delete_table_rows
from .shared import PDBDEV_CLI, DCCTX

logger = logging.getLogger(__name__)

"""
add rows to a table
"""
def add_rows_to_vocab_table(catalog, table_name, rows):
    pb = catalog.getPathBuilder()
    schema = pb.Vocab
    table = schema.__getattr__(table_name)
    table.insert(rows, defaults=['ID', 'URI'])
    print('Added rows to the vocabulary table {}'.format(table_name))


# -------------------------------------------------------------------

def get_topo_ranked_tables(catalog, tname_only=False):
    """Assign order to tables for insert operation based on fkeys e.g. tables with no fkeys should be inserted first.
    This function should be used to replace the needs of tables_groups.json.
    
    Returns:
        dict: a lookup dict from rank to list of tables associated with each rank in the topological sort of
    foreign key dependency.
        
    Notes: The current tables_groups.json keys are string, and the list contains PDB schema table names.
    """
    model = catalog.getCatalogModel()
    tables = {
        table
        for sname in ["PDB"]
        for table in model.schemas[sname].tables.values()
    }
        
    # dependency map { table: set(referenced_table... ), ... } (either a set of list is ok)
    table_depmap = {
        table: {
            # use a set to collapse references to same pk_table
            fkey.pk_table
            for fkey in table.foreign_keys
            if not (
                # ignore references like these...
                fkey.table.schema.name in {'Vocab'} or
                fkey.pk_table.schema.name in {'public', 'Vocab'}
                or (
                    fkey.pk_table.sqlite3_table_name() == 'PDB:entry'
                    and fkey.table.sqlite3_table_name() == 'PDB:Accession_Code'
                )
                #or fkey.table.sqlite3_table_name() == 'PDB:entry'
                #or fkey.constraint_name == 'entry_Workflow_Status_fkey'
            )
        }
        for table in tables
    }
        
    tname_depmap = {
        #table.sqlite3_table_name(): [ pktable.sqlite3_table_name() for pktable in pktables ] # produce PDB:entry
        table.name: [ pktable.name for pktable in pktables ]                # ignore schema prefix
        for table, pktables in table_depmap.items()
    }
        
    rank_list = topo_ranked(tname_depmap) if tname_only else topo_ranked(table_depmap)
    rank_dict = {i: rank_list[i] for i in range(len(rank_list))}
   
    return rank_dict


def get_topo_sorted_tables(catalog, tname_only=False, reverse=False, sort_tname=True):
    """
    Topologically sort table based on foreign key dependencies. Tables with minimial outbound dependencies are
    at the beginning of the list. 
    """
    topo_sorted_tables = []
    ranked_tables = get_topo_ranked_tables(catalog, tname_only=tname_only)
        
    for group_no, tset in ranked_tables.items():
        if sort_tname:
            tlist = sorted(tset, key=lambda t: t if tname_only else t.name)                
        else:
            tlist = list(tset)
        #print("- group: %d => %s" % (group_no, tlist if tname_only else [t.name for t in tlist] ))
        topo_sorted_tables.extend(tlist)

    if reverse:
        return reversed(topo_sorted_tables)            
    else:
        return topo_sorted_tables

    
def clear_entry(catalog, entry_rid, update_last_mmcif_md5=True,
                exclude_tnames=["Entry_Latest_Archive", "Accession_Code", "Curation_Log"]):
    """
    Clear all tables that reference entry row except those in exclude_tnames and set
    Last_mmCIF_File_MD5 to None, so the same file can be re-processed.
    
    Args:
        exclude_tnames (str): exclude table names from being cleared
    """
    rows = get_ermrest_query(catalog, "PDB", "entry", constraints=f"RID={entry_rid}")
    if not rows:
        raise Exception(f"entry RID {entry_rid} does not exist")
    else:
        entry_row = rows[0]
    entry_id = entry_row["id"]

    sorted_tables = get_topo_sorted_tables(catalog, reverse=True)
    for table in sorted_tables:
        tname = table.name
        if tname in (exclude_tnames + ["entry"]): continue
        for fkey in table.foreign_keys:
            if fkey.pk_table.name != "entry": continue
            from_cnames =  [ c.name for c in fkey.column_map.keys() ]
            to_cnames =  [ c.name for c in fkey.column_map.values() ]
            # == set constraints
            if "id" in to_cnames:
                index = to_cnames.index("id")
                constraints = f"{from_cnames[index]}={entry_id}"
            elif "RID" in to_cnames:
                index = to_cnames.index("RID")
                constraints = f"{from_cnames[index]}={entry_rid}"
            else:
                raise Exception("Unexpected event: id or rid is not part of reference to entry")
            # == delete 
            #print("clear_entry: tname: %s, constraints: %s" % (tname, constraints))
            delete_table_rows(catalog, "PDB", tname, constraints=constraints)
            break
                
    # == update entry so the process_mmcif can go ahead later
    if not update_last_mmcif_md5: return
    updating_row = {"RID": entry_rid, "Last_mmCIF_File_MD5":None }
    if entry_row["Last_mmCIF_File_MD5"] != updating_row["Last_mmCIF_File_MD5"]:
        updated = update_table_rows(catalog, "PDB", "entry", payload=[updating_row], keys=["RID"], column_names=["Last_mmCIF_File_MD5"])
        logger.info("entry %s: Last_mmCIF_File_MD5 is set to None")


def clear_entries(catalog, entry_rids, update_last_mmcif_md5=True, dry_run=False,
                  exclude_tnames=["Entry_Latest_Archive", "Accession_Code", "Curation_Log"]):
    """
    Clear all tables that reference entry row except those in exclude_tnames and set
    Last_mmCIF_File_MD5 to None, so the same file can be re-processed.
    
    Args:
        exclude_tnames (str): exclude table names from being cleared
    """
    
    if not entry_rids: return
    
    logger.info("clear_entries: begins with RIDs [%d]: %s" % (len(entry_rids), entry_rids))
    
    rows = get_ermrest_query(catalog, "PDB", "entry", constraints=f'RID=any({",".join(entry_rids)})')
    if len(rows) == 0:
        raise Exception(f"Error: no match found for {entry_rids}")
    rid2rows = { row["RID"]: row for row in rows }
    entry_ids = [ row["id"] for row in rows ] 

    sorted_tables = get_topo_sorted_tables(catalog, reverse=True)
    for table in sorted_tables:
        tname = table.name
        if tname in (exclude_tnames + ["entry"]): continue
        for fkey in table.foreign_keys:
            if fkey.pk_table.name != "entry": continue
            from_cnames =  [ c.name for c in fkey.column_map.keys() ]
            to_cnames =  [ c.name for c in fkey.column_map.values() ]
            # == set constraints
            if "id" in to_cnames:
                index = to_cnames.index("id")
                constraints = f'{from_cnames[index]}=any({",".join(entry_ids)})'
            elif "RID" in to_cnames:
                index = to_cnames.index("RID")
                constraints = f'{from_cnames[index]}=any({",".join(entry_rids)})'
            else:
                raise Exception("Unexpected event: id or rid is not part of reference to entry")
            # == delete 
            #print("clear_entry: tname: %s, constraints: %s" % (tname, constraints))
            delete_table_rows(catalog, "PDB", tname, constraints=constraints, dry_run=dry_run)
            break
                
    # == update entry so the process_mmcif can go ahead later
    if not update_last_mmcif_md5: return
    updating = []
    for row in rows: 
        if row["Last_mmCIF_File_MD5"] != None:
            updating.append({"RID": row["RID"], "Last_mmCIF_File_MD5":None })
    if updating:
        if dry_run:
            print("clear_entries: DRY_RUN updating Last_mmCIF_File_MD5 to None for RIDs [%d]: %s" % (len(updating), [ r["RID"] for r in updating] ))
            return
        updated = update_table_rows(catalog, "PDB", "entry", payload=updating, keys=["RID"], column_names=["Last_mmCIF_File_MD5"])
        logger.info("clear_entries: Last_mmCIF_File_MD5 was updated to None for RIDs [%d]: %s" % (len(updated), [ r["RID"] for r in updated] ))
        

def main(args):
    credentials = get_credential(args.host, args.credential_file)
    print("credentials: %s" % (credentials))
    catalog = ErmrestCatalog("https", args.host, args.catalog_id, credentials)
    catalog.dcctx['cid'] = DCCTX["cli"]
    #store = HatracStore("https", args.host, credentials)
    
    if args.clear_entries:
        rids = set()
        if args.rids: rids = set(args.rids.split(","))
        if args.rid: rids.add(args.rid)
        clear_entry(catalog, args.rid, dry_run=args.dry_run)

# running the script:
# >python -m pdb_dev.utils.data --host data-dev.pdb-ihm.org --catalog-id 99 --rid <RID> --clear-entry
#
if __name__ == "__main__":
    cli = PDBDEV_CLI("pdb", None, 1)
    cli.parser.add_argument('--clear-entries', action='store_true', help='clear entry related tables', default=False, required=False)
    #cli.parser.add_argument('--dry-run', action='store_true', help='dry run', default=False, required=False)    
    cli.parser.add_argument('--rids', metavar='<rids>',  action='store', type=str, help='rids to be cleared', required=False)
    args = cli.parse_cli()
    main(args)
