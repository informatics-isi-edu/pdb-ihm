#!/usr/bin/python

import os
import json
import subprocess
import sys
import traceback
import logging
import logging.handlers

from deriva.core import PollingErmrestCatalog, init_logging, urlquote, get_credential
from deriva.core import ErmrestCatalog, AttrDict, get_credential, DEFAULT_CREDENTIAL_FILE, tag, urlquote, DerivaServer, get_credential, BaseCLI, HatracStore

from deriva.utils.extras.data import insert_if_not_exist, get_ermrest_query, delete_table_rows
from deriva.utils.extras.model import create_vocabulary_tdoc, create_vocab_tdoc, create_table_if_not_exist, create_schema_if_not_exist
from deriva.utils.extras.job_dispatcher import JobDispatcher, JobStream, init_logger

from pdb_dev.utils.shared import PDBDEV_CLI, DCCTX, cfg
from pdb_dev.processing.processor import PipelineProcessor, ProcessingError, ErmrestError, ErmrestUpdateError, FileError
from pdb_dev.processing.ihmv_processing.ihmv_processor import IHMVProcessor

# Reference: git/synspy/synspy/worker.py

#claim_input_data=lambda row: {'RID': row['RID'], 'Execution_Status': "In-progress", 'Status_Detail': None},
#failure_input_data=lambda row, e: {'RID': row['RID'], 'Execution_Status': "Error", 'Status_Detail': e}


# =================================================================================

# =================================================================================
class IHMVJobStream (JobStream):
    scratch_dir = "/mnt/vdb1/ihmv_processing"
    pdbihm_config_file = None
    timeout = None
    singularity_sif = None
    ihmvalidation_dir = None
    def __init__(
            self,
            get_claimable_url,
            put_claim_url,
            put_update_baseurl,
            logger = None, scratch_dir = None, pdbihm_config_file=None, timeout=None, singularity_sif = None, ihmvalidation_dir=None
    ):
        super().__init__(get_claimable_url, put_claim_url, put_update_baseurl)
        self.logger = logger if logger else init_logger("info", "/tmp/log/ihmv_processing/ihmv_worker.log")
        if scratch_dir: self.scratch_dir = scratch_dir
        if pdbihm_config_file: self.pdbihm_config_file = pdbihm_config_file
        if timeout: self.timeout = timeout
        if singularity_sif: self.singularity_sif = singularity_sif
        if ihmvalidation_dir: self.ihmvalidation_dir = ihmvalidation_dir
        print("IHMVJobStream init: scratch_dir: %s, pdbihm_config_file: %s, timeout: %s, singularity: %s, validation_dir: %s" % (self.scratch_dir, self.pdbihm_config_file, self.timeout, self.singularity_sif, self.ihmvalidation_dir))
        
    def run_row_job(self, dispatcher, row):
        assert row['RID']
        self.logger.info("\n\n********** Structure_mmCIF_run_row_job: begin task %s\n%s" % (row["RID"], json.dumps(row, indent=4)))
        
        scratch_dir = self.scratch_dir
        IHMVProcessor(
            catalog=dispatcher.catalog, store=dispatcher.store, cfg=cfg, scratch_dir=self.scratch_dir, logger=self.logger,            
            pdbihm_config_file=self.pdbihm_config_file,
            singularity_sif=self.singularity_sif,
            ihmvalidation_dir=self.ihmvalidation_dir,
            timeout=self.timeout,
            structure_rid=row["RID"],
        ).run()
        
    def claim_input_data(self, row):
        return {'RID': row['RID'], 'Processing_Status': "In Progress", 'Processing_Details': None}

    def failure_input_data(self, row, e):
        return  {'RID': row['RID'], 'Processing_Status': "Error", 'Processing_Details': str(e)}    
        
# --------------------------------------------------------------------------------

# =================================================================================
#
# HT local dir:
# > PDB_CREDENTIALS="/home/hongsuda/.secrets/credentials_proper.json" PDB_SERVER="data-dev.pdb-ihm.org" CATALOG=199 PDBIHM_CONFIG=/home/hongsuda/git/pdb-ihm-ops/scripts/home-config/workflow-dev/dev/config/entry_processing/pdb_conf.json SCRATCH_DIR=/tmp/ihmv_processing IHMV_LOG=/tmp/log/ihmv_processing/ihmv_worker.log  ihmv_worker
#
# workflow server:
# switch user to pdb-ihm
# > sudo su - pdbihm
# > "PDB_CREDENTIALS=/home/pdbihm/.secrets/credentials_proper.json" "PDB_SERVER=data-dev.pdb-ihm.org" "CATALOG=199" "PDBIHM_CONFIG=/home/pdbihm/dev/config/entry_processing/pdb_conf.json" "SCRATCH_DIR=/mnt/vbdb1/ihmv_processing" "IHMV_LOG=/home/pdbihm/log/ihmv_processing/ihmv_worker.log"  /usr/local/bin/ihmv_worker

def main():
    """
    IHMV Validation Processing worker
    """
    cli = PDBDEV_CLI("ihmv", None, 1)
    pdbihm_config_file = os.getenv("PDBIHM_CONFIG", None)
    scratch_dir = os.getenv("SCRATCH_DIR", None)
    log_file = os.getenv("LOG_FILE", "/tmp/log/ihmv_processing/ihmv_worker.log")
    
    cli.parser.add_argument('--scratch-dir', metavar='<scratch_dir>', help="scratch directory path", default=scratch_dir)
    cli.parser.add_argument('--log-file', metavar='<log_file>', help="Log file", default=log_file)    
    cli.parser.add_argument('--pdbihm-config-file', metavar='<pdbihm_config_file>', help="Path to PDB-IHM entry processing config file", default=pdbihm_config_file)
    cli.parser.add_argument('--singularity-sif', metavar='<singularity_sif>', help="Path to a singularity image")
    cli.parser.add_argument('--ihmvalidation-dir', metavar='<ihmvalidation_dir>', help="Path to IHMValidation code")
    cli.parser.add_argument('--timeout', metavar='<timeout>', help="Timeout for the IHMValidation pipeline", type=int)
    args = cli.parse_cli()
    print("args = %s" % (args))

    credentials = get_credential(args.host, args.credential_file)
    server = DerivaServer('https', args.host, credentials)
    store = HatracStore('https', args.host, credentials)
    catalog = server.connect_ermrest(args.catalog_id)
    model = catalog.getCatalogModel()

    logger = init_logger(log_file=args.log_file)
    
    logger.info("=========== starts ihmv worker with args: %s" % (args))

    dispatcher = JobDispatcher(args.host, args.catalog_id, args.credential_file, logger=logger)
    job_streams = [ IHMVJobStream(
        '/entity/M:=IHMV:Structure_mmCIF/Processing_Status=any(New,Reprocess)?limit=1',
        '/attributegroup/IHMV:Structure_mmCIF/RID;Processing_Status,Processing_Details',
        '/attributegroup/IHMV:Structure_mmCIF',        
        logger=logger,
        scratch_dir=args.scratch_dir,
        pdbihm_config_file=args.pdbihm_config_file,
        singularity_sif=args.singularity_sif,
        ihmvalidation_dir=args.ihmvalidation_dir,
        timeout=args.timeout,
    ) ]
    dispatcher.blocking_poll(job_streams)

    return 0

# =================================================================================
if __name__ == '__main__':

    sys.exit(main())
