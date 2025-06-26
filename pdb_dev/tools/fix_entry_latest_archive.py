#!/usr/bin/python3
import json
from deriva.core import ErmrestCatalog, HatracStore, AttrDict, get_credential, DEFAULT_CREDENTIAL_FILE, tag, urlquote, DerivaServer, get_credential, BaseCLI
from deriva.utils.extras.data import get_ermrest_query
from deriva.utils.extras.history import iso_to_snap
from pdb_dev.utils.shared import PDBDEV_CLI, DCCTX, cfg

# get historical data
snap_time="2025-06-18"
snap_id='33F-MSDD-KE00' # 2025-06-18
collection_rid = '2-YE32'
collection_id = 'PDBDEV_G_1000003'
rct="2024-09-13T02:01:52.643616+00:00"

def get_snap_entry_latest_archive(server, catalog_id, snap_time, collection_id):
    """
    Get Entry_Latest_Archive rows of an old snapshot
    """
    snap_id = iso_to_snap(snap_time)
    constraints = f'E:=(Entry)=(PDB:entry:RID)/CM:=(id)=(PDB:ihm_entry_collection_mapping:entry_id)/collection_id={collection_id}/$M'
    url = f'/ermrest/catalog/{catalog_id}@{snap_id}/entity/M:=PDB:Entry_Latest_Archive/{constraints}'
    print("url: %s" % (url))
    rows = server.get(url).json()
    print("Snap_time: %s, snap_id: %s" % (snap_time, snap_id))
    print("latest_archive[%d]: %s" % (len(rows), json.dumps(rows[0:5], indent=4)))
    return rows

def restore_latest_archive(catalog, latest_archive_rows):
    """
    Recreate Entry_Latest_Archive rows based on the data from the previous snapshot
    """
    payload = []
    for row in latest_archive_rows:
        insert_row = {}
        for k,v in row.items():
            if k in ["RID", "RMT", "RCB", "RMB"]: continue
            insert_row[k] = v
        payload.append(insert_row)
    print("\npayload[%d]: %s" % (len(payload), json.dumps(payload[0:5], indent=4)))

    inserted = catalog.post(
        "/entity/PDB:Entry_Latest_Archive?onconflict=skip&nondefaults=RCT",
        json=payload
    ).json()
    print("number of rows inserted: %d" % (len(inserted)))

    
def main(server, catalog_id, args):
    catalog = server.connect_ermrest(args.catalog_id)
    print("credentials: %s" % (credentials))    
    #catalog = ErmrestCatalog("https", args.host, catalog_snap, credentials)
    catalog.dcctx['cid'] = DCCTX["cli/remedy"]
    
    latest_archive_rows = get_snap_entry_latest_archive(server, catalog_id, snap_time, collection_id)
    restore_latest_archive(catalog, latest_archive_rows)

"""
python fix_entry_latest_archive.py --snap-time 2025-06-18 --collection-id PDBDEV_G_1000003

This script create the Entry_Latest_Archive rows of entries associated with a collection based on an old snapshot.
Note: The incorrect Entry_Latest_Archive rows should be deleted before running the script. 

TODO: Add input parameters to incorporate:
  - snpashot time that we want to restore the entry_latest_archive
  - collection_id
"""
if __name__ == "__main__":
    cli = PDBDEV_CLI("pdbdev", None, 1)
    cli.parser.add_argument('--snap-time', metavar='<snap_time>', help="snapshot time in ISO format e.g. '2025-06-18'", default=snap_time)
    cli.parser.add_argument('--collection-id', metavar='<collection_id>', help="collection id", default=collection_id)
    
    args = cli.parse_cli()
    credentials = get_credential(args.host, args.credential_file)    
    server = DerivaServer("https", args.host, credentials)    

    main(server, args.catalog_id, args)

