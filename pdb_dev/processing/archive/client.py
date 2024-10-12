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
"""
Load configuration for the PDB archive.
"""

import os
import logging
import json
import sys
import traceback
import argparse

from worker2 import ArchiveClient
from deriva.core import init_logging, get_credential
#from ...utils.shared import PDBDEV_CLI, cfg
from pdb_dev.utils.shared import PDBDEV_CLI, cfg

FORMAT = '%(asctime)s: %(levelname)s <%(module)s>: %(message)s'
logger = logging.getLogger(__name__)

# Loglevel dictionary
__LOGLEVEL = {
    'critical': logging.FATAL,
    'fatal': logging.CRITICAL,
    'error': logging.ERROR,
    'warning': logging.WARNING,
    'info': logging.INFO,
    'debug': logging.DEBUG
}

catalog_id2name = {
    "1": "prod",
    "50": "staging",
    "99": "dev",
}

def load(config_filename):
    """
    Read the configuration file.
    """
    
    # Load configuration file, or create configuration based on arguments
    config = {}
    if os.path.exists(config_filename):
        try:
            with open(config_filename, 'r') as f:
                config = json.load(f)
            loglevel = config.get('loglevel', None)
            #logfile = config.get('log', None)            
            log_dir = config.get('log_dir', None)
            logfile = "%s/archive_%s.log" % (log_dir, catalog_id2name[cfg.catalog_id])
            config["logfile"] = logfile
            if loglevel and logfile:
                init_logging(level=__LOGLEVEL.get(loglevel), log_format=FORMAT, file_path=logfile)
            else:
                logging.getLogger().addHandler(logging.NullHandler())
            logger.debug("config: %s" % config)
            
            return config
        except ValueError as e:
            logger.error('Malformed configuration file: %s' % e)
            return None
    else:
        sys.stderr.write('ERROR: Configuration file: "%s" does not exist.\n' % config_filename)
        return None
    
'''
  fcfg: file configuration
'''
def get_configuration(fcfg, logger, args):
    """
    Return the client configuration.
    """
    
    config = {}

    config['hostname'] = cfg.host
    config['catalog_id'] = cfg.catalog_id
    config['hatrac_namespace'] = "/hatrac/pdb" if not cfg.is_dev else '/hatrac/dev/pdb'
    config['verbose'] = args.verbose

    credentials_file = fcfg.get('credentials', None)
    credentials = get_credential(cfg.host, credentials_file)
    if not credentials:
        print('Credential is NULL. Provide a proper credential file or set up credential under the user account properly. Provided credential file:%s' % (credentials_file))        
        logger.error('Credential is NULL. Provide a proper credential file or set up credential under the user account properly. Provided credential file:%s' % (credentials_file))
        return None
    #print("credentials = %s" % (credentials))        
    config['credentials'] = credentials

    archive_parent = fcfg.get('archive_parent', None)
    #archive_parent = "%s/%s" % (archive_parent, catalog_id2name[config['catalog_id']])    # use same location
    if not archive_parent or not os.path.isdir(archive_parent):
        logger.error('archive parent directory must be provided and exists.')
        return None

    config['archive_parent'] = archive_parent
    
    data_scratch = fcfg.get('data_scratch', None)
    #data_scratch = "%s/%s" % (data_scratch, catalog_id2name[config['catalog_id']])  # use same location
    if not data_scratch or not os.path.isdir(data_scratch):
        logger.error('The scratch directory must be provided and exist.')
        return None
    config['data_scratch'] = data_scratch


    holding_dir = fcfg.get('holding_dir', None)
    if not holding_dir:
        logger.error('The holding entry dir directory must be provided.')
        return None
    config['holding_dir'] = holding_dir
    
    cutoff_time_pacific = fcfg.get('cutoff_time_pacific', 'Thursday 20:00')
    config['cutoff_time_pacific'] = cutoff_time_pacific
    
    released_entry_dir = fcfg.get('released_entry_dir', None)
    if not released_entry_dir:
        logger.error('The released entry dir directory must be provided.')
        return None
    config['released_entry_dir'] = released_entry_dir

    holding_namespace = fcfg.get('holding_namespace', None)
    if holding_namespace == None:
        logger.error(f'The holding namespace must be provided.')
        return None
    config['holding_namespace'] = holding_namespace
    
    email_file = fcfg.get('mail', None)
    if not email_file or not os.path.isfile(email_file):
        logger.error('email file must be provided and exist.')
        return None
    
    with open(email_file, 'r') as f:
        email = json.load(f)
    config['email'] = email
    
    config['logger'] = logger

    return config

def main():
    cli = PDBDEV_CLI("pdbdev", None, 1)
    cli.parser.add_argument( '--config', action='store', type=str, help='The JSON configuration file.', required=True)
    cli.parser.add_argument( '--verbose', action='store_true', help='Print status to stdout', default=False, required=False)        
    args = cli.parse_cli()

    credentials = get_credential(args.host, args.credential_file)
    print("credentials = %s" % (credentials))

    try:
        config = load(args.config)
        if config != None:
            archive_worker_configuration = get_configuration(config, logger, args)
            #del archive_worker_configuration['logger']
            #print(json.dumps(archive_worker_configuration, indent=4))
            #return 1
            if archive_worker_configuration != None:
                archive_worker = ArchiveClient(archive_worker_configuration)
                returnStatus = archive_worker.processArchive()
                logger.debug('Return Status: {}'.format(returnStatus))
                return returnStatus
    except:
        et, ev, tb = sys.exc_info()
        sys.stderr.write('got exception "%s"' % str(ev))
        sys.stderr.write('%s' % ''.join(traceback.format_exception(et, ev, tb)))
        sys.stderr.write('\nusage: python3 -m pdb_dev.processing.archive.client --config /home/pdbihm/pdb/config/dev/pdb_archive.json --catalog-id 1\n\n')
        return 1

    
"""
# Install the Python package:
#    From the protein-database directory, run: 
#        pip3 install --upgrade .
#
# Running the script:
#    python3 -m pdb_dev.processing.archive.client --config /home/pdbihm/pdb/config/www/pdb_archive.json --catalog-id 1
#
"""

if __name__ == '__main__':
    sys.exit(main())

