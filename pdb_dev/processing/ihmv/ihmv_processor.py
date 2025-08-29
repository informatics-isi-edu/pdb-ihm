#!/usr/bin/python

import json
import subprocess
import os
from subprocess import TimeoutExpired
from pathlib import Path
import shutil
import typing
import re

from deriva.core import PollingErmrestCatalog, DerivaServer, HatracStore, urlquote, get_credential
from deriva.core.datapath import DataPathException

from deriva.utils.extras.data import insert_if_not_exist, update_table_rows, delete_table_rows, get_ermrest_query
from deriva.utils.extras.hatrac import HatracFile
#from ...utils.shared import PDBDEV_CLI, DCCTX, cfg
from pdb_dev.utils.shared import PDBDEV_CLI, DCCTX, cfg
from pdb_dev.processing.processor import PipelineProcessor, ProcessingError, ErmrestError, ErmrestUpdateError, FileError


class IHMVProcessor(PipelineProcessor):
    """Network client for standalone PDB Validation Report
    """
    scratch_dir = "/mnt/vdb1/ihmv_processing/scratch"
    log_dir = "/home/pdbihm/log/ihmv"
    structure_rid = None
    singularity_sif = None
    ihmvalidation_dir = None
    timeout = 30
    hatrac_root = '/hatrac'
    pdbihm_config_file = '/home/pdbihm/config/entry_processing/pdb_conf.json'
    pdbihm_config = None

    def __init__(self, catalog=None, store=None, hostname=None, catalog_id=None, credential_file=None,
                 scratch_dir=None, cfg=None, logger=None, log_level="info", log_file="/home/pdbihm/log/ihmv/process_ihmv.log", verbose=None,
                 email_config="/home/pdbihm/.secrets/email.json", structure_rid=None,
                 pdbihm_config_file: typing.Optional[str]=None,
                 singularity_sif: typing.Optional[str]=None,
                 ihmvalidation_dir: typing.Optional[str]=None,
                 timeout: typing.Optional[int]=None,
                 ):
        super().__init__(hostname=hostname, catalog_id=catalog_id, credentials = credential_file, cfg=cfg)
        if scratch_dir: self.scratch_dir = scratch_dir
        if structure_rid: self.structure_rid = structure_rid
        self.log_file = log_file.replace(".log", "_dev.log") if cfg and cfg.is_dev else log_file        
        if cfg: self.hatrac_root = cfg.hatrac_root
        
        # get structure row
        rows = get_ermrest_query(self.catalog, "IHMV", "Structure_mmCIF", constraints=f"RID={structure_rid}")
        if len(rows) != 1:
            raise Exception("ERROR: RID %s doesn't exist" % (structure_rid))
        self.structure_row = rows[0]

        # -- get config properties from pdb_ihm config
        if pdbihm_config_file:
            self.pdbihm_config_file = pdbihm_config_file
        elif cfg.is_dev:
            self.pdbihm_config_file = '/home/pdbihm/dev/config/entry_processing/pdb_conf.json'
        
        try:
            with open(self.pdbihm_config_file, 'r') as file:
                self.pdbihm_config = json.load(file)
        except FileNotFoundError:
            print(f"Error: The file '{file_path}' was not found.")
            raise Exception("Config ERROR: pdb_ihm config file doesn't exist: %s" % (self.pdbihm_config_file))
        except json.JSONDecodeError:
            print(f"Error: Could not decode JSON from '{file_path}'. Check if the file contains valid JSON.")
            raise Exception("Config ERROR: pdb_ihm config file is not a json file: %s" % (self.pdbihm_config_file))

        # -- unless overwrite, use values from pdbihm_config_file
        self.timeout = timeout if timeout else (self.pdbihm_config["timeout"] if "timeout" in self.pdbihm_config.keys() else self.timeout)
        self.singularity_sif = singularity_sif if singularity_sif else (self.pdbihm_config["singularity_sif"] if "singularity_sif" in self.pdbihm_config.keys() else self.singularity_sif)
        self.ihmvalidation_dir = ihmvalidation_dir if ihmvalidation_dir else (self.pdbihm_config["validation_dir"] if "validation_dir" in self.pdbihm_config.keys() else self.ihmvalidation_dir)

        print("pdbihm_confif_file: %s " % (self.pdbihm_config_file))
        print("timeout: %s, singularity_sif: %s, ihmvalidation_dir: %s " % (self.timeout, self.singularity_sif, self.ihmvalidation_dir))
        print("cfg.host: %s, cfg.catalog_id: %s, is_dev:%s, hatrac_root: %s, log_file: %s " % (self.cfg.host, self.cfg.catalog_id, self.cfg.is_dev, self.hatrac_root, self.log_file))

        #raise Exception("Die here")
    
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
                upload_url = f"{self.hatrac_root}/ihmv/generated/uid/{uid}/structure/rid/{self.structure_rid}/validation_report/{hf_file_name}"
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
            # Remove old directory
            shutil.rmtree(data_dir, ignore_errors=True)
            # Create directory structure
            Path(data_dir).mkdir(parents=True, exist_ok=True)
            for dir_ in ['input', 'output', 'cache']:
                Path(data_dir, dir_).mkdir(parents=True, exist_ok=True)

            # Download cif file
            cif_hf = self.download_mmcif_file(Path(data_dir, 'input'))

            # -- process: process cif and generate ihmv files. Make sure that file names follow naming conventions with appropriate prefix/suffix
            filename = Path(cif_hf.file_path).name

            # Note: the parameter before : is the local directory in the base vm, the parameter after : is the container path
            # To test this manually, cd to the validation directory (e.g. /mnt/vdb1/validation

            # Pass system ihm package
            bind_paths_ = []
            ihm_dir = '/usr/local/lib/python3.8/dist-packages/ihm/'
            if Path(ihm_dir).exists():
                bind_paths_.append(f'{ihm_dir}:/opt/conda/lib/python3.10/site-packages/ihm/')
            # Pass IHMValidation directory
            bind_paths_.append(f'{self.ihmvalidation_dir}:/opt/IHMValidation')
            # Pass input, output, and cache directories
            for dir_ in ['input', 'output', 'cache']:
                bind_paths_.append(f'{Path(data_dir, dir_)}:{Path("/ihmv", dir_)}')
            bind_paths = ','.join(bind_paths_)

            # prepare call to the IHMValidation pipeline
            args = ['singularity',
                    'exec', '--pid',
                    '--bind', bind_paths,
                    self.singularity_sif,
                    '/opt/IHMValidation/ihm_validation/ihm_validator.py',
                    '-f', f'/ihmv/input/{filename}',
                    '--force',
                    '--output-root', '/ihmv/output',
                    '--cache-root', '/ihmv/cache'
                    ]
            # self.logger.debug(f'Running "{" ".join(args)}" from the {self.validation_dir} directory')
            p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            # Set non-zero return code by-default
            returncode = 127
            try:
                stdoutdata, stderrdata = p.communicate(timeout=self.timeout*60)
                returncode = p.returncode
                if returncode != 0:
                    error_msg = (f'ERROR.\nstdoutdata: {stdoutdata}\nstderrdata: {stderrdata}\n')
                    structure_payload = [{
                        "RID": self.structure_rid,
                        "Processing_Status": "Error",
                        "Processing_Details": error_msg,
                    }]
                    update_table_rows(self.catalog, "IHMV", "Structure_mmCIF", payload=structure_payload, column_names=["Processing_Status", "Processing_Details"])
            except TimeoutExpired:
                et, ev, tb = sys.exc_info()
                error_msg = 'ERROR.\nTimeout exception\n' + '%s' % ''.join(traceback.format_exception(et, ev, tb))
                structure_payload = [{
                    "RID": self.structure_rid,
                    "Processing_Status": "Error",
                    "Processing_Details": error_msg,
                }]
                update_table_rows(self.catalog, "IHMV", "Structure_mmCIF", payload=structure_payload, column_names=["Processing_Status", "Processing_Details"])
                p.kill()

            if returncode == 0:
                # -- upload files to hatrac
                # output location
                pdf_loc = Path(data_dir, 'output', Path(filename).stem)
                ihmv_hfs = self.upload_file_groups(pdf_loc, [".pdf"])

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
                        "File_Type": "Validation: Summary PDF" if hf.file_name.endswith("summary_validation.pdf") else "Validation: Full PDF"
                    })
                # check whether files already exist
                existing_files = get_ermrest_query(self.catalog, "IHMV", "Generated_File", constraints=f"Structure_mmCIF={self.structure_rid}")
                if len(existing_files) != 0:
                    # simply delete all old files
                    values_ = [x['RID'] for x in existing_files]
                    delete_table_rows(self.catalog, "IHMV", "Generated_File", key='RID', values=values_)

                insert_if_not_exist(self.catalog, "IHMV", "Generated_File", ihmv_payload)

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
                "Processing_Details": str(e),
            }]
            update_table_rows(self.catalog, "IHMV", "Structure_mmCIF", payload=structure_payload, column_names=["Processing_Status", "Processing_Details"])
        finally:
            # cleaup directory
            shutil.rmtree(data_dir, ignore_errors=True)

# ===========================================================================================

def main(server_name, catalog_id, credentials, args):
    server = DerivaServer('https', server_name, credentials)
    store = HatracStore('https', server_name, credentials)
    catalog = server.connect_ermrest(catalog_id)
    model = catalog.getCatalogModel()

    processor = IHMVProcessor(
        catalog=catalog, store=store, hostname=server_name, catalog_id=catalog_id, cfg=cfg,
        scratch_dir=args.scratch_dir,
        structure_rid=args.rid,
        pdbihm_config_file=args.pdbihm_config_file,
        singularity_sif=args.singularity_sif,
        ihmvalidation_dir=args.ihmvalidation_dir,
        timeout=args.timeout
    ).run()

# ===========================================================================================
# usage:
#
# HT laptop
#> python ihmv_processor.py --pdbihm-config-file ~/git/pdb-ihm-ops/scripts/home-config/workflow-dev/dev/config/entry_processing/pdb_conf.json --catalog-id 199 --rid 2ET
#
# workflow-dev: as pdbihm user
#
#> python ihmv_processor.py --pdbihm-config-file /home/pdbihm/dev/config/entry_processing/pdb_conf.json --catalog-id 199 --rid 2ET
#

if __name__ == '__main__':
    cli = PDBDEV_CLI("ihmv", None, 1)
    cli.parser.add_argument('--scratch-dir', metavar='<scratch_dir>', help="scratch directory path")
    cli.parser.add_argument('--pdbihm-config-file', metavar='<pdbihm_config_file>', help="Path to PDB-IHM entry processing config file")    
    cli.parser.add_argument('--singularity-sif', metavar='<singularity_sif>', help="Path to a singularity image")
    cli.parser.add_argument('--ihmvalidation-dir', metavar='<ihmvalidation_dir>', help="Path to IHMValidation code")
    cli.parser.add_argument('--timeout', metavar='<timeout>', help="Timeout for the IHMValidation pipeline", type=int)
    args = cli.parse_cli()
    credentials = get_credential(args.host, args.credential_file)
    print("args = %s" % (args))
    main(args.host, args.catalog_id, credentials, args)

