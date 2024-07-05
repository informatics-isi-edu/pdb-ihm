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

from .worker import ArchiveClient
from deriva.core import init_logging

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

def load(config_filename):
    """
    Read the configuration file.
    """
    
    # Load configuration file, or create configuration based on arguments
    cfg = {}
    if os.path.exists(config_filename):
        try:
            with open(config_filename, 'r') as f:
                cfg = json.load(f)
            loglevel = cfg.get('loglevel', None)
            logfile = cfg.get('log', None)
            if loglevel and logfile:
                init_logging(level=__LOGLEVEL.get(loglevel), log_format=FORMAT, file_path=logfile)
            else:
                logging.getLogger().addHandler(logging.NullHandler())
            logger.debug("config: %s" % cfg)
            return cfg
        except ValueError as e:
            logger.error('Malformed configuration file: %s' % e)
            return None
    else:
        sys.stderr.write('Configuration file: "%s" does not exist.\n' % config_filename)
        return None
    
def get_configuration(cfg, logger):
    """
    Return the client configuration.
    """
    
    config = {}

    hostname = cfg.get('hostname', None)
    if hostname == None:
        logger.error('hostname must be supplied.')
        return None
        
    config['hostname'] = hostname

    catalog_id = cfg.get('catalog', None)
    if catalog_id == None:
        logger.error('catalog id must be supplied.')
        return None
        
    config['catalog_id'] = catalog_id

    credentials_file = cfg.get('credentials', None)
    if not credentials_file or not os.path.isfile(credentials_file):
        logger.error('credentials file must be provided and exist.')
        return None
    credentials = json.load(open(credentials_file))
    
    config['credentials'] = credentials

    hatrac_namespace = cfg.get('hatrac_namespace', None)
    if hatrac_namespace == None:
        hatrac_namespace = 'hatrac/pdb'
    else:
        hatrac_namespace = 'hatrac/{}/pdb'.format(hatrac_namespace)

    config['hatrac_namespace'] = hatrac_namespace

    holding_namespace = cfg.get('holding_namespace', None)
    if holding_namespace == None:
        logger.error(f'The holding namespace must be provided.')
        return None

    config['holding_namespace'] = holding_namespace

    primary_accession_code_mode = cfg.get('primary_accession_code_mode', 'PDBDEV')
    if primary_accession_code_mode not in ['PDBDEV', 'PDB']:
        logger.error(f'Invalid value for the primary_accession_code_mode: {primary_accession_code_mode}.')
        return None

    config['accession_code_mode'] = primary_accession_code_mode

    archive_parent = cfg.get('archive_parent', None)
    if not archive_parent or not os.path.isdir(archive_parent):
        logger.error('archive parent directory must be provided and exists.')
        return None

    config['archive_parent'] = archive_parent
    
    data_scratch = cfg.get('data_scratch', None)
    if not data_scratch or not os.path.isdir(data_scratch):
        logger.error('The scratch directory must be provided and exist.')
        return None
    
    config['data_scratch'] = data_scratch

    released_entry_dir = cfg.get('released_entry_dir', None)
    if not released_entry_dir:
        logger.error('The released entry dir directory must be provided.')
        return None
    
    config['released_entry_dir'] = released_entry_dir

    holding_dir = cfg.get('holding_dir', None)
    if not holding_dir:
        logger.error('The holding entry dir directory must be provided.')
        return None
    
    config['holding_dir'] = holding_dir

    email_file = cfg.get('mail', None)
    if not email_file or not os.path.isfile(email_file):
        logger.error('email file must be provided and exist.')
        return None
    
    with open(email_file, 'r') as f:
        email = json.load(f)

    config['email'] = email

    config['logger'] = logger
    
    return config

def main():
    parser = argparse.ArgumentParser(description='Tool to archive mmCIF files.')
    parser.add_argument( '--config', action='store', type=str, help='The JSON configuration file.', required=True)
    args = parser.parse_args()
    
    try:
        config = load(args.config)
        if config != None:
            archive_worker_configuration = get_configuration(config, logger)
            if archive_worker_configuration != None:
                try:
                    archive_worker = ArchiveClient(archive_worker_configuration)
                    returnStatus = archive_worker.processArchive()
                    logger.debug('Return Status: {}'.format(returnStatus))
                    return returnStatus
                except:
                    et, ev, tb = sys.exc_info()
                    sys.stderr.write('got exception "%s"' % str(ev))
                    sys.stderr.write('%s' % ''.join(traceback.format_exception(et, ev, tb)))
                    sys.stderr.write('\nusage: deriva-imaging-client --config <config-file> --rid <rid>\n\n')
                    return 1
    except:
        et, ev, tb = sys.exc_info()
        sys.stderr.write('got exception "%s"' % str(ev))
        sys.stderr.write('%s' % ''.join(traceback.format_exception(et, ev, tb)))
        sys.stderr.write('\nusage: deriva-imaging-client --config <config-file> --rid <rid>\n\n')
        return 1


"""
# Install the Python package:
#    From the protein-database directory, run: 
#        pip3 install --upgrade --no-deps .
#
# Running the script:
#    python3 -m pdb_dev.archive.client --config /home/pdbihm/pdb/config/www/pdb_archive.json 
#
"""

if __name__ == '__main__':
    sys.exit(main())

