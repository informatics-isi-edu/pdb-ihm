#!/usr/bin/python

import json
import subprocess
import os
from subprocess import TimeoutExpired

from deriva.core import PollingErmrestCatalog, DerivaServer, HatracStore, urlquote, get_credential
from deriva.core.datapath import DataPathException

from deriva.utils.extras.data import insert_if_not_exist, update_table_rows, delete_table_rows, get_ermrest_query
from deriva.utils.extras.hatrac import HatracFile
#from ...utils.shared import PDBDEV_CLI, DCCTX
from pdb_dev.utils.shared import PDBDEV_CLI, DCCTX
from pdb_dev.processing.processor import PipelineProcessor, ProcessingError, ErmrestError, ErmrestUpdateError, FileError


class IHMVProcessor(PipelineProcessor):
    """Network client for standalone PDB Validation Report
    """
    scratch_dir = "/mnt/vdb1/ihmv_processing/scratch"
    log_dir = "/home/pdbihm/log/ihmv"
    structure_rid = None

    def __init__(self, catalog=None, store=None, hostname=None, catalog_id=None, credential_file=None,
                 scratch_dir=None, cfg=None, logger=None, log_level="info", log_file="/home/pdbihm/log/ihmv/processor.log", verbose=None,
                 email_config="/home/pdbihm/.secrets/email.json", structure_rid=None
                 ):
        super().__init__(hostname=hostname, catalog_id=catalog_id, credentials = credential_file, cfg=cfg)
        if scratch_dir: self.scratch_dir = scratch_dir
        if structure_rid: self.structure_rid = structure_rid

        # get structure row
        rows = get_ermrest_query(self.catalog, "IHMV", "Structure_mmCIF", constraints=f"RID={structure_rid}")
        if len(rows) != 1:
            raise Exception("ERROR: RID %s doesn't exist" % (structure_rid))
        self.structure_row = rows[0]

    # -------------------------------------------------                
    def download_mmcif_file(self, data_dir):
        # -- download files
        hatrac_url = self.structure_row["File_URL"]
        filename = self.structure_row["File_Name"]
        print("data_dir: %s, hatrac_url: %s, filename: %s" % (data_dir, hatrac_url, filename))
        hf = HatracFile(self.store)
        hf.download_file(hatrac_url, data_dir, filename, verbose=True)
        file_path = hf.file_path
        return hf

    # -------------------------------------------------        
    def upload_file_groups(self, data_dir, filter_groups):
        """
        Upload files in the directory to hatrac that match regex criteria specified in filter_groups.
        If filter_groups are not set, allow all files to match.
        Note: To upload an individual file, specify the data_dir and put its exact filename in the filter list. 
        Return a array of HatracFile corresponding to uploaded files.
        """
        
        if not filter_groups:
            filter_groups = [".*"]
            
        print("data_dir: %s, groups: %s" % (data_dir, filter_groups))
        #os.chdir(data_dir)        
        hfs = []
        for filter in filter_groups: 
            for file in os.scandir(data_dir):
                if not re.search(filter, file.name): continue
                if not file.is_file(): continue
                uid = self.structure_row["RCB"].rsplit("/", 1)[1]
                # TODO: rename files if needed. Suggest prepend with structure_mmcif RID
                hf = HatracFile(self.store)                
                hf_file_name = f"{self.structure_rid}_{file.name}"
                hf_file_name = hf.sanitize_filename(hf_file_name)                
                upload_url = f"{self.cfg.hatrac_root}/ihmv/generated/uid/{uid}/structure/rid/{self.structure_rid}/validation_report/{hf_file_name}"
                hf.upload_file(file.path, upload_url, hf_file_name, verbose=True)
                hfs.append(hf)
        return hfs

    # -------------------------------------------------
    """
    TODO: address the File_Type when store to ermrest
    """
    def run(self):

        try:
            # -- download file. Do help(HatracFile) for obj properties
            data_dir = f"{self.scratch_dir}/{self.structure_rid}"
            os.system(f'mkdir -p {data_dir}')
            cif_hf = self.download_mmcif_file(data_dir)
            
            # -- process: process cif and generate ihmv files. Make sure that file names follow naming conventions with appropriate prefix/suffix
            # TODO: @Authur fill in the processing that generate outputs
            
            # -- upload files to hatrac
            ihmv_hfs = self.upload_file_groups(data_dir, ["*.pdf"])
            
            # -- update ermrest
            # TODO: fix file_type logic
            ihmv_payload = []
            for hf in ihmv_hfs:
                ihmv_payload.append({
                    "Structure_mmCIF": self.structure_rid,
                    "File_Name": hf.file_name,
                    "File_URL": hf.hatrac_url,
                    "File_MD5": hf.md5_hex,
                    "File_Bytes": hf.file_bytes,
                    "File_Type": "Validation: Summary PDF" if hf.file_name.endswith("summary.pdf") else "Validation: Full PDF"
                })
            # check whether files already exist
            existing_files = get_ermrest_query(self.catalog, "IHMV", "Generated_File", constraints=f"Structure_mmCIF={self.structure_rid}")
            if len(existing_files) == 0:
                #insert_if_not_exist(self.catalog, "IHMV", "Generated_File", ihmv_payload)
                pass
            else:
                # do an update instead
                #update_table_rows(self.catalog, "IHMV", "Generated_File", payload=structure_payload, column_names=["File_URL", "File_Name", "File_Bytes", "File_MD5"])                
                pass
            
            structure_payload = [{
                "RID": self.structure_rid,
                "Processing_Status": "Success",
                "Processing_Details": None
            }]
            update_table_rows(self.catalog, "IHMV", "Structure_mmCIF", payload=structure_payload, column_names=["Processing_Status", "Processing_Details"])
        except Exception as e:
            print("Exception: %s" % (e))
            structure_payload = [{
                "RID": self.structure_rid,
                "Processing_Status": "Error",
                "Processing_Details": "Add details here from exception",
            }]
            update_table_rows(self.catalog, "IHMV", "Structure_mmCIF", payload=structure_payload, column_names=["Processing_Status", "Processing_Details"])
        finally:
            # cleaup directory
            pass
            
def main(server_name, catalog_id, credentials, args):
    server = DerivaServer('https', server_name, credentials)
    store = HatracStore('https', server_name, credentials)
    catalog = server.connect_ermrest(catalog_id)
    model = catalog.getCatalogModel()

    processor = IHMVProcessor(
        catalog=catalog, store=store, hostname=server_name, catalog_id=catalog_id,
        scratch_dir=args.scratch_dir,
        structure_rid=args.rid, 
    ).run()

    
    
if __name__ == '__main__':
    cli = PDBDEV_CLI("ihmv", None, 1)
    cli.parser.add_argument('--scratch-dir', metavar='<scratch_dir>', help="scratch directory path")
    args = cli.parse_cli()
    credentials = get_credential(args.host, args.credential_file)
    print("args = %s" % (args))
    main(args.host, args.catalog_id, credentials, args)

