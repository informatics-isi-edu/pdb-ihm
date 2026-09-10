#!/usr/bin/python3
# 
# Copyright 2017 University of Southern California
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#    http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import sys
import json
from pathlib import Path

from deriva.core import PollingErmrestCatalog, HatracStore, urlquote, get_credential, DerivaServer
from deriva.utils.extras.data import get_key2rows, get_ermrest_query, insert_if_not_exist, update_table_rows, delete_table_rows
from deriva.utils.extras.hatrac import HatracFile
#from ...utils.shared import PDBDEV_CLI, cfg
from pdb_dev.utils.shared import PDBDEV_CLI, cfg
from pdb_dev.processing.processor import PipelineProcessor, ProcessingError, ErmrestError, ErmrestUpdateError, FileError, SubProcessError


def get_latest_pdb_archive(catalog):
    """Get latest pdb_archive row from Ermrest
    """
    constraints = "$M@sort(Submission_Time::desc::)"
    rows = get_ermrest_query(catalog, "PDB", "PDB_Archive", constraints=constraints, limit=1, sort=None)
    print("latest_pdb_archive: %s" % (json.dumps(rows[0], indent=4)))
    return rows[0]


def get_latest_archive_files(catalog, store, download_dir):
    """Download files corresponding to enries associated with the latest PDB archive
    """
    model = catalog.getCatalogModel()
    file_types = ["Validation: HTML tar.gz"] # change the list to reflect what to download
    if not download_dir: return
    
    # == get latest pdb archive
    archive_row = get_latest_pdb_archive(catalog)
    archive_rid = archive_row["RID"]

    # == get latest archive entries. 
    constraints=f"PDB:Entry_Latest_Archive/Archive={archive_rid}/$M"
    entries = get_ermrest_query(catalog, "PDB", "entry", constraints=constraints)
    print("latest_archive_entries [%d]: %s" % (len(entries), json.dumps(entries[0:1], indent=4)))
    
    # == get latest archive entries' generated files with specific file type
    ftype_str = ",".join( [urlquote(t) for t in file_types] )
    constraints=f"Archive={archive_rid}/entry/F:=Entry_Generated_File/File_Type=any({ftype_str})/$F"
    files = get_ermrest_query(catalog, "PDB", "Entry_Latest_Archive", constraints=constraints)
    print("latest_archive_files [%d]: %s" % (len(files), json.dumps(files[0:2], indent=4)))

    # == download files from hatrac
    Path(download_dir).mkdir(parents=True, exist_ok=True)
    hf = HatracFile(store)
    for file in files:  
        # Note: set hashes to None if we do not want to validate file checksum later
        hf.download_file(file["File_URL"], download_dir, file_name=file["File_Name"], hashes=["md5"])
        assert file["File_MD5"] == hf.md5_hex
        print("hf: file_url: %s, file_path: %s, md5: %s" % (hf.hatrac_url, hf.file_path, hf.md5_hex))


# -- =================================================================================
def main():
    cli = PDBDEV_CLI("pdb-ihm", None, 1)
    cli.parser.add_argument('--dir-name', metavar='dir_name', help="Download dir name", default="/tmp/pdb_download", required=False)
    args = cli.parse_cli()
    server_name = args.host
    
    credentials = get_credential(server_name, args.credential_file)
    server = DerivaServer('https', server_name, credentials)
    store = HatracStore('https', server_name, credentials)
    catalog = server.connect_ermrest(args.catalog_id)

    get_latest_archive_files(catalog, store, args.dir_name)
    return 0
    

 # -- =================================================================================
if __name__ == '__main__':
    
    sys.exit(main())

    
