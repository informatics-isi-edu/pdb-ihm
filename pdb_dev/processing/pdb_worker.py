#!/usr/bin/python

import os
import json
import subprocess
import sys
import traceback
import logging
import logging.handlers
import random
import time
from argparse import Namespace

from deriva.core import PollingErmrestCatalog, ErmrestCatalog, HatracStore, DerivaServer, get_credential, init_logging, urlquote, DEFAULT_SESSION_CONFIG

from deriva.utils.extras.data import insert_if_not_exist, get_ermrest_query, delete_table_rows
from deriva.utils.extras.model import create_vocabulary_tdoc, create_vocab_tdoc, create_table_if_not_exist, create_schema_if_not_exist
from deriva.utils.extras.job_dispatcher import JobDispatcher, JobStream, init_logger

from pdb_dev.utils.shared import PDBDEV_CLI, DCCTX, cfg
from pdb_dev.processing.processor import PipelineProcessor, ProcessingError, ErmrestError, ErmrestUpdateError, FileError
from pdb_dev.processing.entry_processing.pdb_process_entry import process_entry

# enable retry for all requests
session_config = DEFAULT_SESSION_CONFIG.copy()
session_config['allow_retry_on_all_methods'] = True

# Reference: git/synspy/synspy/worker.py

process_status_terms = {
    'NEW': 'New (trigger backend process)',
    'REPROCESS': 'Reprocess (trigger backend process after Error)',
    'IN_PROGRESS_UPLOADING_mmCIF_FILE': 'In progress: processing uploaded mmCIF file',
    'IN_PROGRESS_GENERATING_mmCIF_FILE': 'In progress: generating mmCIF file',
    'IN_PROGRESS_GENERATING_SYSTEM_FILES': 'In progress: generating system files',
    'IN_PROGRESS_RELEASING_ENTRY': 'In progress: releasing entry',
    'SUCCESS': 'Success',
    'RESUME': 'Resume (trigger backend process)',
    'ERROR_PROCESSING_UPLOADED_mmCIF_FILE': 'Error: processing uploaded mmCIF file',
    'ERROR_GENERATING_mmCIF_FILE': 'Error: generating mmCIF file',
    'ERROR_GENERATING_SYSTEM_FILES': 'Error: generating system files',
    'ERROR_RELEASING_ENTRY': 'Error: releasing entry',
    'IN_PROGRESS_PROCESSING_UPLOADED_RESTRAINT_FILES': 'In progress: processing uploaded restraint files',
    'ERROR_PROCESSING_UPLOADED_RESTRAINT_FILES': 'Error: processing uploaded restraint files'
}

restraint_depo_status = "RESTRAINT DEPO"

workflow_status2actions = {
    "DEPO": "entry",
    "SUBMIT": "export",
    "SUBMISSION COMPLETE": "accession_code",
    "RELEASE READY": "release_mmCIF",
    "RESTRAINT DEPO": "Entry_Related_File",    
}

workflow_status2suffixes = {
    "DEPO": "UPLOADING_mmCIF_FILE",
    "SUBMIT": "GENERATING_mmCIF_FILE",
    "SUBMISSION COMPLETE": "GENERATING_SYSTEM_FILES",
    "RELEASE READY": "RELEASING_ENTRY",
    "RESTRAINT DEPO": "PROCESSING_UPLOADED_RESTRAINT_FILES",
}

poll_seconds = int(os.getenv('POLL_SECONDS', '300'))
config_file = os.getenv("PDB_CONFIG", '/home/pdbihm/config/entry_processing/pdb_conf.json')
process_id = os.getenv('PROCESS_ID', 'p0')
loglevel = os.getenv('LOGLEVEL', 'info')        
log_file = os.getenv("PDB_LOG", f"/home/pdbihm/pdb/log/entry_processing/pdb_entry_worker_{process_id}.log")
mute = bool(os.getenv("MUTE", False))

def get_process_status(workflow_status, status_mode="in-progress"):
    if status_mode in ["in-progress", "In-progress"]:
        prefix = "IN_PROGRESS"
    elif status_mode in ["error", "Error"]:
        prefix = "ERROR"
    else:
        raise Exception(f"ERROR: unknown process_status_mode: {status_mode}")
    
    key = f"{prefix}_{workflow_status2suffixes[workflow_status]}"
    process_status = process_status_terms[key]
    
    return process_status    
    

# =================================================================================
class EntryJobStream (JobStream):
    mute = False
    def __init__(
            self,
            get_claimable_url,
            put_claim_url,
            put_update_baseurl,
            config_file=None,
            poll_seconds=None,
            process_id="p0",
            logger = None,
    ):
        super().__init__(get_claimable_url, put_claim_url, put_update_baseurl)
        if config_file: self.config_file = config_file
        if poll_seconds: self.poll_seconds = poll_seconds
        self.process_id = process_id
        self.logger = logger if logger else init_logger("info", "/home/pdbihm/log/entry_processing/pdbs_worker.log")
        self.mute = cfg.args.mute

        #print("- cfg.args: %s" % (cfg.args))
        print("- -- EntryJobStream init: config_file: %s, poll_seconds: %s, mute: %s " % (self.config_file, self.poll_seconds, self.mute))
        self.logger.info(f"EntryJobStream: claimable url: {self.get_claimable_url}")
        
    def run_row_job(self, dispatcher, row):
        assert row['RID']
        deriva_host = dispatcher.deriva_host
        catalog_id = dispatcher.catalog_id
        action = workflow_status2actions[row["Workflow_Status"]]
        
        self.logger.info('EntryJobStream: Running job: host=%s catalog-id=%s RID="%s" action=%s' % (deriva_host, catalog_id, row['RID'], action))
        args = Namespace(host=deriva_host, catalog_id=catalog_id, action=action, rid=row["RID"], config=self.config_file, process_id=self.process_id, mute=self.mute)
        process_entry(args, existing_logger=self.logger)

        """ # old approach
        args = ['env', f'ACTION={action}', f'PDB_SERVER={deriva_host}', f'CATALOG={catalog_id}', f'RID={row["RID"]}', 'pdb_process_entry', '--config', dispatcher.config_file, '--process-id', process_id ]
        p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdoutdata, stderrdata = p.communicate()
        returncode = p.returncode
        if returncode != 0:
            logger.error('Could not execute the script for the PDB Workflow Processing.\nstdoutdata: %s\nstderrdata: %s\n' % (stdoutdata, stderrdata)) 
            raise WorkerRuntimeError('Could not execute the script for the PDB Workflow Processing.\nstdoutdata: %s\nstderrdata: %s\n' % (stdoutdata, stderrdata))
        """
                
    def claim_input_data(self, row):
        process_status = get_process_status(row["Workflow_Status"], status_mode="in-progress")
        return {'RID': row['RID'], 'Process_Status': process_status, 'Record_Status_Detail': None}

    def failure_input_data(self, row, e):
        process_status = get_process_status(row["Workflow_Status"], status_mode="error")        
        return  {'RID': row['RID'], 'Process_Status': process_status, 'Record_Status_Detail': str(e)}    
        
# --------------------------------------------------------------------------------
class RestraintJobStream (JobStream):
    mute = False
    def __init__(
            self,
            get_claimable_url,
            put_claim_url,
            put_update_baseurl,
            config_file=None, poll_seconds=None, process_id="p0", logger = None,
    ):

        super().__init__(get_claimable_url, put_claim_url, put_update_baseurl)
        if config_file: self.config_file = config_file
        if poll_seconds: self.poll_seconds = poll_seconds
        self.process_id = process_id
        self.logger = logger if logger else init_logger("info", "/home/pdbihm/log/entry_processing/pdbs_worker.log")
        self.mute = cfg.args.mute        
        
        print("- -- RestraintJobStream init: config_file: %s, poll_seconds: %s, mute: %s " % (self.config_file, self.poll_seconds, self.mute))
        self.logger.info(f"{self.logger.name} RestraintJobStream: claimable url: {self.get_claimable_url}")
        
    def run_row_job(self, dispatcher, row):
        assert row['RID']
        deriva_host = dispatcher.deriva_host
        catalog_id = dispatcher.catalog_id
        action = workflow_status2actions[restraint_depo_status]

        self.logger.info('RestraintJobStream: Running job: host=%s catalog-id=%s RID="%s" action=%s' % (deriva_host, catalog_id, row['RID'], action))
        args = Namespace(host=deriva_host, catalog_id=catalog_id, action=action, rid=row["RID"], config=self.config_file, process_id=self.process_id, mute=self.mute)
        process_entry(args, existing_logger=self.logger)

    def claim_input_data(self, row):
        process_status = get_process_status(restraint_depo_status, status_mode="in-progress")
        return {'RID': row['RID'], 'Restraint_Process_Status': process_status, 'Record_Status_Detail': None}

    def failure_input_data(self, row, e):
        process_status = get_process_status(restraint_depo_status, status_mode="error")        
        return  {'RID': row['RID'], 'Restraint_Process_Status': process_status, 'Record_Status_Detail': str(e)}    
        

# =================================================================================
"""
# involved envs
env PDB_CREDENTIALS="/home/pdbihm/.secrets/credentials_proper.json" PDB_SERVER="data-dev.pdb-ihm.org" CATALOG="50" PDB_CONFIG="/home/pdbihm/config/entry_processing/pdb_conf.json" PROCESSOR_ID=p0 PDB_LOG="/home/pdbihm/log/entry_processing/pdbs_worker_p0.log"

# HT local dir:
# > PDB_CREDENTIALS=/home/hongsuda/.secrets/credentials_proper.json PDB_SERVER=data-dev.pdb-ihm.org CATALOG=99 PDB_CONFIG=/home/hongsuda/config/entry_processing/local_pdb_conf.json PROCESSOR_ID=p0 PDB_LOG=/tmp/log/entry_processing/pdbs_worker.log python pdbihm_worker.py
#
# workflow server:
# switch user to pdb-ihm
# > sudo su - pdbihm
# env PDB_CREDENTIALS="/home/pdbihm/.secrets/credentials_proper.json" PDB_SERVER="data-dev.pdb-ihm.org" CATALOG="99" PDB_CONFIG="/home/pdbihm/config/entry_processing/pdb_conf.json" PROCESSOR_ID=p0 PDB_LOG="/home/pdbihm/log/entry_processing/pdbs_worker_p0.log" python pdbihm_worker.py

#
"""
def main():
    """
    Entry Processing worker
    """
    logger = logging.getLogger("pdb_worker")
    
    cli = PDBDEV_CLI("ihm", None, 1)
    cli.parser.add_argument('--log-file', metavar='<log_file>', help="Log file", default=log_file)    
    cli.parser.add_argument('--config-file', metavar='<config_file>', help="Path to PDB-IHM entry processing config file", default=config_file)
    cli.parser.add_argument('--poll-seconds', metavar='<poll_seconds>', help="Worker sleep time (seconds) before polling", default=poll_seconds)
    cli.parser.add_argument('--process-id', metavar='<process_id>', help="Worker process id", default=process_id)    
    cli.parser.add_argument('--verbose', action='store_true', help='Whether to print status to stdout', default=False, required=False)
    cli.parser.add_argument('--mute', action='store_true', help='Whether to notify', default=mute, required=False)
    cli.parser.add_argument('--workshop', action='store_true', help='Whether it is for PDB workshop', default=False, required=False)        
    args = cli.parse_cli()
    print("- main: args = %s" % (args))    

    credentials = get_credential(args.host, args.credential_file)
    server = DerivaServer('https', args.host, credentials)
    store = HatracStore('https', args.host, credentials)
    catalog = server.connect_ermrest(args.catalog_id)
    model = catalog.getCatalogModel()

    logger = init_logger(log_file=args.log_file, name="pdb_worker")
    #logger = init_logger(log_file=args.log_file, name=__name__)    
    
    logger.info("======== starts entry_processing worker with args: %s" % (args))

    dispatcher = JobDispatcher(args.host, args.catalog_id, args.credential_file, logger=logger)

    process_statuses = [ urlquote(process_status_terms[term]) for term in ["NEW", "RESUME", "REPROCESS"] ]
    process_status_string = ",".join(process_statuses)
    workflow_statuses = [ urlquote(term) for term in workflow_status2actions.keys() if term != restraint_depo_status ]
    if args.workshop: workflow_statuses = [ urlquote(term) for term in ['DEPO'] ] # limited support during workshop
    workflow_status_string = ",".join(workflow_statuses)
    print("- * workflow_statuses = %s" % (workflow_statuses))
    
    job_streams = [
        EntryJobStream(
            '/attribute/M:=PDB:entry/Manual_Processing=False/Process_Status=any(%s)/Workflow_Status=any(%s)/$M/RID,LMT,id,Workflow_Status,Process_Status,mmCIF_File_Name@sort(LMT)?limit=1' % (process_status_string, workflow_status_string),
            '/attributegroup/PDB:entry/RID;Process_Status,Record_Status_Detail',
            '/attributegroup/PDB:entry/RID',
            config_file=args.config_file,            
            poll_seconds = args.poll_seconds,
            process_id=args.process_id,
            logger=logger
        ),
        
        RestraintJobStream(
            # -- default sort
            #'/entity/M:=PDB:Entry_Related_File/Restraint_Process_Status=any(%s)/Restraint_Workflow_Status=DEPO/PDB:entry/Manual_Processing=False/Process_Status=%s/$M/F:=Vocab:File_Type/$M?limit=1' % (process_status_string, urlquote(process_status_terms['SUCCESS'])),        
            # -- sort by Rank
            '/attribute/M:=PDB:Entry_Related_File/Restraint_Process_Status=any(%s)/Restraint_Workflow_Status=DEPO/PDB:entry/Manual_Processing=False/Process_Status=%s/$M/F:=Vocab:File_Type/$M/RID,LMT,structure_id,File_Type,File_Name,F:Rank@sort(Rank,LMT)?limit=1' % (process_status_string, urlquote(process_status_terms['SUCCESS'])),            
            '/attributegroup/PDB:Entry_Related_File/RID;Restraint_Process_Status,Record_Status_Detail',
            '/attributegroup/PDB:Entry_Related_File/RID',
            config_file=args.config_file,            
            poll_seconds = args.poll_seconds,
            process_id=args.process_id,            
            logger=logger,
        ),
    ]
    dispatcher.blocking_poll(job_streams)

    return 0

# =================================================================================
if __name__ == '__main__':

    sys.exit(main())
