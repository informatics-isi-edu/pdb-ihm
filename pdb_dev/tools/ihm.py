#!/usr/bin/python3

import sys
import json
from pathlib import Path

from deriva.core import PollingErmrestCatalog, HatracStore, urlquote, get_credential, DerivaServer
from deriva.utils.extras.data import get_key2rows, get_ermrest_query, insert_if_not_exist, update_table_rows, delete_table_rows
from deriva.utils.extras.hatrac import HatracFile
from pdb_dev.utils.shared import PDBDEV_CLI, cfg
from pdb_dev.utils.data import clear_entries
from pdb_dev.processing.processor import PipelineProcessor, ProcessingError, ErmrestError, ErmrestUpdateError, FileError, SubProcessError

def get_entries(catalog, rids, succint=False):
    attributes = None 
    if succint: attributes=["Accession_Code", "Workflow_Status", "Process_Status", "Record_Status_Detail"]
    entries = get_ermrest_query(catalog, "PDB", "entry", constraints="RID=any(%s)" % ",".join(rids), attributes=attributes)
    print("entries [%d]: %s" % (len(entries), json.dumps(entries, indent=4)))
    return entries

# -- =================================================================================

def main():
    cli = PDBDEV_CLI("ihm", None, 1)
    cli.parser.add_argument('--clear-entries', action='store_true', help='clear entry related tables', default=False, required=False)
    cli.parser.add_argument('--check-entries', action='store_true', help='get entries information ', default=False, required=False)
    cli.parser.add_argument('--succint', action='store_true', help='succint entry info', default=False, required=False)        
    cli.parser.add_argument('--rids', metavar='<rids>',  action='store', type=str, help='rids to be cleared', required=False)
    # dry-run is supported through default args
    args = cli.parse_cli()
    
    server_name = args.host 
    credentials = get_credential(server_name, args.credential_file)
    server = DerivaServer('https', server_name, credentials)
    store = HatracStore('https', server_name, credentials)
    catalog = server.connect_ermrest(args.catalog_id)

    rids = set()
    if args.rids: rids = set(args.rids.split(","))
    if args.rid: rids.add(args.rid)
    
    if args.clear_entries:
        clear_entries(catalog, rids, dry_run=args.dry_run)
    elif args.check_entries:
        get_entries(catalog, rids, args.succint)
    
    return 0
    

# -- =================================================================================
# running the script:
# >python -m pdb_dev.tools.ihm --host data-dev.pdb-ihm.org --catalog-id 99 --rid <RID> --clear-entry
#

if __name__ == '__main__':
    
    sys.exit(main())
