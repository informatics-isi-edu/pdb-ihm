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

from pdb_workflow_processing_lib.client import PDBClient
from deriva.core import init_logging

FORMAT = '%(asctime)s: %(levelname)s <%(module)s>: %(message)s'
logger = logging.getLogger(__name__)

# Loglevel dictionary
__LOGLEVEL = {'error': logging.ERROR,
              'warning': logging.WARNING,
              'info': logging.INFO,
              'debug': logging.DEBUG}

def load(config_filename):
    """
    Read the configuration file.
    """
    
    # Load configuration file, or create configuration based on arguments
    cfg = {}
    if os.path.exists(config_filename):
        f = open(config_filename, 'r')
        try:
            cfg = json.load(f)
            loglevel = cfg.get('loglevel', None)
            logfile = cfg.get('log', None)
            if loglevel and logfile:
                init_logging(level=__LOGLEVEL.get(loglevel), log_format=FORMAT, file_path=logfile)
            else:
                logging.getLogger().addHandler(logging.NullHandler())
            logger.debug("config: %s" % cfg)
        except ValueError as e:
            logger.error('Malformed configuration file: %s' % e)
            return None
        else:
            f.close()
    else:
        sys.stderr.write('Configuration file: "%s" does not exist.\n' % config_filename)
        return None
    
    # Ermrest settings
    url = os.getenv('URL', None)
    if url == None:
        logger.error('URL must be supplied through the "URL" environment variable.')
        logger.error('Launch the script "env URL=https://foo.org/ermrest/catalog/N pdb_workflow_processing.py --config config-file".')
        return None
        
    logger.info('URL: %s' % url)
    
    credentials_file = cfg.get('credentials', None)
    if not credentials_file or not os.path.isfile(credentials_file):
        logger.error('credentials file must be provided and exist.')
        return None
    credentials = json.load(open(credentials_file))
    
    make_mmCIF = cfg.get('make_mmCIF', None)
    if not make_mmCIF or not os.path.isdir(make_mmCIF):
        logger.error('make_mmCIF directory must be provided and exist.')
        return None
    
    py_rcsb_db = cfg.get('py_rcsb_db', None)
    if not py_rcsb_db or not os.path.isdir(py_rcsb_db):
        logger.error('py_rcsb_db directory must be provided and exist.')
        return None
    
    scratch = cfg.get('scratch', None)
    if not scratch or not os.path.isdir(scratch):
        logger.error('scratch directory must be provided and exist.')
        return None
    
    python_bin = cfg.get('python3', None)
    if not python_bin or not os.path.isfile(python_bin):
        logger.error('python3 executable must be provided and exist.')
        return None

    tables_groups = cfg.get('tables_groups', None)
    if not tables_groups or not os.path.isfile(tables_groups):
        logger.error('tables_groups file must be provided and exist.')
        return None

    optional_fk_file = cfg.get('optional_fk_file', None)
    if not optional_fk_file or not os.path.isfile(optional_fk_file):
        logger.error('optional_fk_file file must be provided and exist.')
        return None

    CifCheck = cfg.get('CifCheck', None)
    if not CifCheck or not os.path.isfile(CifCheck):
        logger.error('CifCheck file must be provided and exist.')
        return None

    dictSdb = cfg.get('dictSdb', None)
    if not dictSdb or not os.path.isfile(dictSdb):
        logger.error('dictSdb file must be provided and exist.')
        return None

    entry = cfg.get('entry', None)
    if not entry or not os.path.isfile(entry):
        logger.error('entry file must be provided and exist.')
        return None

    export_tables_file = cfg.get('export_tables', None)
    if not export_tables_file or not os.path.isfile(export_tables_file):
        logger.error('export_tables file must be provided and exist.')
        return None
    export_tables = json.load(open(export_tables_file))
    
    cif_tables_file = cfg.get('cif_tables', None)
    if not cif_tables_file or not os.path.isfile(cif_tables_file):
        logger.error('cif_tables file must be provided and exist.')
        return None
    cif_tables = json.load(open(cif_tables_file))
    
    export_order_by_file = cfg.get('export_order_by', None)
    if not export_order_by_file or not os.path.isfile(export_order_by_file):
        logger.error('export_order_by file must be provided and exist.')
        return None
    export_order_by = json.load(open(export_order_by_file))
    
    combo1_columns_file = cfg.get('combo1_columns', None)
    if not combo1_columns_file or not os.path.isfile(combo1_columns_file):
        logger.error('combo1_columns file must be provided and exist.')
        return None
    combo1_columns = json.load(open(combo1_columns_file))
    
    mmCIF_defaults = cfg.get('mmCIF_defaults', None)
    if not mmCIF_defaults or not os.path.isfile(mmCIF_defaults):
        logger.error('mmCIF_defaults file must be provided and exist.')
        return None
    mmCIF_defaults = json.load(open(mmCIF_defaults))
    
    vocab_ucode = cfg.get('vocab_ucode', None)
    if not vocab_ucode or not os.path.isfile(vocab_ucode):
        logger.error('vocab_ucode file must be provided and exist.')
        return None
    vocab_ucode = json.load(open(vocab_ucode))
    
    mmCIF_Schema_Version = cfg.get('mmCIF_Schema_Version', '1.0')
    hatrac_namespace = cfg.get('hatrac_namespace', None)
    if hatrac_namespace == None:
        hatrac_namespace = 'hatrac/pdb'
    else:
        hatrac_namespace = 'hatrac/{}/pdb'.format(hatrac_namespace)
    
    email_file = cfg.get('mail', None)
    if not email_file or not os.path.isfile(email_file):
        logger.error('email file must be provided and exist.')
        return None
    
    with open(email_file, 'r') as f:
        email = json.load(f)

    # Establish Ermrest client connection
    try:
        client = PDBClient(baseuri=url, \
                               credentials=credentials, \
                               mmCIF_Schema_Version=mmCIF_Schema_Version, \
                               make_mmCIF=make_mmCIF, \
                               mmCIF_defaults=mmCIF_defaults, \
                               vocab_ucode=vocab_ucode, \
                               scratch=scratch, \
                               py_rcsb_db=py_rcsb_db, \
                               python_bin=python_bin, \
                               tables_groups=tables_groups, \
                               optional_fk_file=optional_fk_file, \
                               export_tables=export_tables, \
                               cif_tables=cif_tables, \
                               export_order_by=export_order_by, \
                               combo1_columns=combo1_columns, \
                               dictSdb=dictSdb, \
                               CifCheck=CifCheck, \
                               hatrac_namespace=hatrac_namespace, \
                               entry=entry, \
                               email=email, \
                               logger=logger)
    except:
        et, ev, tb = sys.exc_info()
        logger.error('got INIT exception "%s"' % str(ev))
        logger.error('%s' % ''.join(traceback.format_exception(et, ev, tb)))
        return None
    
    return client

try:
    if len(sys.argv) < 3:
        raise
    config_filename = sys.argv[2]
    client = load(config_filename)
    if client:
        try:
            print ('The client will be started')
            client.start()
        except:
            sys.exit(1)
except:
    et, ev, tb = sys.exc_info()
    sys.stderr.write('got exception "%s"' % str(ev))
    sys.stderr.write('%s' % ''.join(traceback.format_exception(et, ev, tb)))
    sys.stderr.write('\nusage: env URL=https://foo.org/ermrest/catalog/N pdb_workflow_processing.py --config config-file\n\n')
    sys.exit(1)

