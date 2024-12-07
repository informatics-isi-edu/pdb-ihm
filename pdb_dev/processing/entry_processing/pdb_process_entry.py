#!/usr/bin/python

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
"""
Load configuration for the PDB processing.
Update the ermrest tables.
"""

import os
import logging
import json
import sys
import traceback
import logging.handlers
from urllib.parse import urlparse

from deriva.core import init_logging, get_credential
from ...utils.shared import PDBDEV_CLI, cfg
from .entry_processor import EntryProcessor
#from pdb_dev.processing.curation.entry_processor import EntryProcessor


FORMAT = '%(asctime)s: %(levelname)s <%(module)s>: %(message)s'
logger = logging.getLogger(__name__)

# Loglevel dictionary
__LOGLEVEL = {'error': logging.ERROR,
              'warning': logging.WARNING,
              'info': logging.INFO,
              'debug': logging.DEBUG}

class ConfigError(Exception):
    """ Exception when fail to load config
    """
    pass

def load(config_filename, args):
    """
    Read the configuration file.
    """
    
    # Load configuration file, or create configuration based on arguments
    conf = {}
    if os.path.exists(config_filename):
        f = open(config_filename, 'r')
        try:
            conf = json.load(f)
            loglevel = conf.get('loglevel', None)
            #logfile = conf.get('log', None)            
            log_dir = conf.get('log_dir')
            logfile = "%s/curation_%s.log" % (log_dir, cfg.catalog_name)
            if loglevel and logfile:
                handler=logging.handlers.TimedRotatingFileHandler(logfile,when='D',backupCount=7)
                logger.addHandler(handler)
                init_logging(level=__LOGLEVEL.get(loglevel), log_format=FORMAT, file_path=logfile)
            else:
                logging.getLogger().addHandler(logging.NullHandler())
            logger.debug("config: %s" % conf)
        except ValueError as e:
            raise ConfigError('Malformed configuration file: %s' % e)
        else:
            f.close()
    else:
        raise ConfigError('Configuration file: "%s" does not exist.\n' % config_filename)

    config = {}
    config['logger'] = logger
    config['logfile'] = logfile    
    config['cfg'] = cfg
    
    # Ermrest settings -- get from command line args if exist, then look for environment variables (for backward compatibility)
    if args.host and args.catalog_id:
        hostname = args.host
        catalog_id = args.catalog_id
        logger.info(f'hostname: {hostname}, catalog_id: {catalog_id}')
    else:
        url = os.getenv('URL', None)
        if not url:
            raise ConfigError(f'Require host and catalog number. Either provide "host" and "catalog-id" CLI parameters or proper "URL" env variable. URL:{URL}')            
        elements = urlparse(url)
        scheme = elements[0]
        hostname = elements[1].split(":")[0]
        port = elements[1].split(":")[1] if ":" in elements[1] else None
        path = elements[2]
        catalog_id = int(path.split('/')[-1]) if path else None
        logger.info('URL: %s' % url)        
        
    if not hostname or not catalog_id:
        raise ConfigError(f'Require host and catalog number. Either provide "host" and "catalog-id" CLI parameters or proper "URL" env variable. args.host:{args.host}, args.catalog-id:{args.catalog_id}, URL:{URL}')

    config["rid"] = args.rid if args.rid else os.getenv('RID', os.getenv('rid', None))
    if not config["rid"]:
        raise ConfigError(f'Require rid. Either provide "rid" as CLI parameters or "RID" env variable.')

    config["action"] = args.action if args.action else os.getenv('action', None)
    if not config["action"]:
        raise ConfigError(f'Require action. Either provide "action" as CLI parameters or env variable.')
    
    config['hostname'] = hostname
    config['catalog_id'] = catalog_id
    config['verbose'] = args.verbose
    #config['rollback'] = args.rollback
    #config['dry_run'] = args.dry_run    
    
    credentials_file = conf.get('credentials', None)
    credentials = get_credential(hostname, credentials_file)
    if not credentials:
        raise ConfigError('Credential is NULL. Provide a proper credential file or set up credential under the user account properly. Provided credential file:%s' % (credentials_file))
    #print("get_recential: %s" % (credentials))
    config['credentials'] = credentials
    config['timeout'] = conf.get('timeout', 30)


    primary_accession_code_mode = conf.get('primary_accession_code_mode', 'PDB')    
    if primary_accession_code_mode not in ['PDBDEV', 'PDB']:
        raise ConfigError(f'Invalid value for the primary_accession_code_mode: {config['primary_accession_code_mode']}.')
    config['primary_accession_code_mode'] = primary_accession_code_mode

    alternative_accession_code_mode = conf.get('alternative_accession_code_mode', 'PDBDEV')
    if alternative_accession_code_mode not in ['PDBDEV', 'PDB', 'None']:
        raise ConfigError(f'Invalid value for the alternative_accession_code_mode: {config['alternative_accession_code_mode']}.')        
    config['alternative_accession_code_mode'] = alternative_accession_code_mode
    
    if config['primary_accession_code_mode'] == config['alternative_accession_code_mode']:
        raise ConfigError(f'primary_accession_code_mode "{config['primary_accession_code_mode']}" must be different from alternative_accession_code_mode "{config['alternative_accession_code_mode']}".')        

    make_mmCIF = conf.get('make_mmCIF', None)
    if not make_mmCIF or not os.path.isdir(make_mmCIF):
        raise ConfigError('make_mmCIF directory must be provided and exist.')
    config['make_mmCIF'] = make_mmCIF
    
    py_rcsb_db = conf.get('py_rcsb_db', None)
    if not py_rcsb_db or not os.path.isdir(py_rcsb_db):
        raise ConfigError('py_rcsb_db directory must be provided and exist.')
    config['py_rcsb_db'] = py_rcsb_db
    
    scratch = conf.get('scratch', None)
    if not scratch or not os.path.isdir(scratch):
        raise ConfigError('scratch directory must be provided and exist.')
    config['scratch'] = scratch
    
    validation_dir = conf.get('validation_dir', None)
    if not validation_dir or not os.path.isdir(validation_dir):
        raise ConfigError('validation_dir directory must be provided and exist.')
    config['validation_dir'] = validation_dir
    
    python_bin = conf.get('python3', None)
    if not python_bin or not os.path.isfile(python_bin):
        raise ConfigError('python3 executable must be provided and exist.')
    config['python_bin'] = python_bin
    
    tables_groups = conf.get('tables_groups', None)
    if not tables_groups or not os.path.isfile(tables_groups):
        raise ConfigError('tables_groups file must be provided and exist.')
    config['tables_groups'] = tables_groups
    
    optional_fk_file = conf.get('optional_fk_file', None)
    if not optional_fk_file or not os.path.isfile(optional_fk_file):
        raise ConfigError('optional_fk_file file must be provided and exist.')
    config['optional_fk_file'] = optional_fk_file

    CifCheck = conf.get('CifCheck', None)
    if not CifCheck or not os.path.isfile(CifCheck):
        raise ConfigError('CifCheck file must be provided and exist.')
    config['CifCheck'] = CifCheck
    
    dictSdb = conf.get('dictSdb', None)
    if not dictSdb or not os.path.isfile(dictSdb):
        raise ConfigError('dictSdb file must be provided and exist.')
    config['dictSdb'] = dictSdb
    
    entry = conf.get('entry', None)
    if not entry or not os.path.isfile(entry):
        raise ConfigError('entry file must be provided and exist.')
    config['entry'] = entry
    
    export_tables_file = conf.get('export_tables', None)
    if not export_tables_file or not os.path.isfile(export_tables_file):
        raise ConfigError('export_tables file must be provided and exist.')
    export_tables = json.load(open(export_tables_file))
    config['export_tables'] = export_tables
    
    cif_tables_file = conf.get('cif_tables', None)
    if not cif_tables_file or not os.path.isfile(cif_tables_file):
        raise ConfigError('cif_tables file must be provided and exist.')
    cif_tables = json.load(open(cif_tables_file))
    config['cif_tables'] = cif_tables
    
    export_order_by_file = conf.get('export_order_by', None)
    if not export_order_by_file or not os.path.isfile(export_order_by_file):
        raise ConfigError('export_order_by file must be provided and exist.')
    export_order_by = json.load(open(export_order_by_file))
    config['export_order_by'] = export_order_by
    
    combo1_columns_file = conf.get('combo1_columns', None)
    if not combo1_columns_file or not os.path.isfile(combo1_columns_file):
        raise ConfigError('combo1_columns file must be provided and exist.')
    combo1_columns = json.load(open(combo1_columns_file))
    config['combo1_columns'] = combo1_columns
    
    mmCIF_defaults = conf.get('mmCIF_defaults', None)
    if not mmCIF_defaults or not os.path.isfile(mmCIF_defaults):
        raise ConfigError('mmCIF_defaults file must be provided and exist.')
    mmCIF_defaults = json.load(open(mmCIF_defaults))
    config['mmCIF_defaults'] = mmCIF_defaults
    
    vocab_ucode = conf.get('vocab_ucode', None)
    if not vocab_ucode or not os.path.isfile(vocab_ucode):
        raise ConfigError('vocab_ucode file must be provided and exist.')
    vocab_ucode = json.load(open(vocab_ucode))
    config['vocab_ucode'] = vocab_ucode
    
    config['mmCIF_Schema_Version'] = conf.get('mmCIF_Schema_Version', '1.0')
    hatrac_namespace = conf.get('hatrac_namespace', None)
    if hatrac_namespace == None:
        hatrac_namespace = 'hatrac/pdb'
    else:
        hatrac_namespace = 'hatrac/{}/pdb'.format(hatrac_namespace)
    config['hatrac_namespace'] = hatrac_namespace
    
    config['reportValidation'] = conf.get('reportValidation', 'Yes')
    email_file = conf.get('mail', None)
    if not email_file or not os.path.isfile(email_file):
        raise ConfigError('email file must be provided and exist.')
    
    with open(email_file, 'r') as f:
        email = json.load(f)
    config['email'] = email

    # print config object
    '''
    for k, v in config.items():
        if k in ['logger', 'cfg']:
            print("%s : %s" % (k, v))
        else:
            print("%s : %s" % (k, json.dumps(v, indent=4)))
    '''
    
    return config

"""
To run this on command line
- switch user to pdb-ihm by
  > sudo su - pdb-ihm
- 2 ways to run the program:
  - 2.1 pass all parameters through the cli
    > pdb_process_entry --host data-dev.pdb-ihm.org --catalog-id 99 --config /home/pdbihm/pdb/config/pdb_conf.json --action entry --rid 3-4RHT
  - 2.2. pass some parameters through environment variables (deprecated)
    > URL="https://data-dev.pdb-ihm.org/ermrest/catalog/99" action="entry" RID="3-4RHT" pdb_process_entry --config /home/pdbihm/pdb/config/pdb_conf.json
- Note: ACTION : ["entry", "export", "accession_code", "release_mmCIF", "Entry_Related_File"]
"""
def main():
    '''
    Run the processing code for an individual entry.
    '''
    try:
        cli = PDBDEV_CLI("pdb_process_entry", None, 1)
        cli.remove_options(['--pre-print', '--post-print', '--dry-run'])
        cli.parser.add_argument('--config', metavar='<config-file>', action='store', type=str, help='The JSON configuration file.', required=True)
        #cli.parser.add_argument('--RID', metavar='<RID>', action='store', type=str, help='entry RID to be processed', required=False)
        cli.parser.add_argument('--action', metavar='<action>',  action='store', type=str, help='Workflow actions (entry, export, accession_code, release_mmCIF, Entry_Related_File)', default='entry', required=False)
        cli.parser.add_argument('--verbose', action='store_true', help='Print status to stdout', default=False, required=False)
        #cli.parser.add_argument('--rollback', action='store_true', help='Rollback ermrest update', default=False, required=False)
        
        args = cli.parse_cli()
        
        config_filename = args.config
        config = load(config_filename, args)
        entry_processor = EntryProcessor(**config)
        print ('The client will be started')
        entry_processor.start()
        return 0
    except ConfigError as e:
        sys.stderr.write(str(e))
        logger.error(str(e))
        return 1
    except:
        et, ev, tb = sys.exc_info()
        sys.stderr.write('got exception "%s"' % str(ev))
        sys.stderr.write('%s' % ''.join(traceback.format_exception(et, ev, tb)))
        sys.stderr.write('\nusage: URL=https://foo.org/ermrest/catalog/N pdb_process_workflow --config config-file\n\n')
        return 1


if __name__ == '__main__':
    sys.exit(main())
