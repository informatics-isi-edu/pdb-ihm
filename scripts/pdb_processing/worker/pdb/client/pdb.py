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
Load configuration for the Pyramidal Tiles Generator.
Check for images that need tiles.
Generate the tiles directory.
Generate the thumbnail and the HTML zoomify file.
Generate the dzi directory.
Generate the dzi file structure
Update the ermrest tables.
"""

import os
import logging
import json
import sys
import traceback

from rbk_pyramidal_tiles_lib.client import PyramidalClient
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
        logger.error('Launch the script "env URL=https://foo.org/ermrest/catalog/N rbk_pyramidal_tiles.py --config config-file".')
        return None
        
    logger.info('URL: %s' % url)
    
    cookie = cfg.get('cookie', None)
    if not cookie:
        logger.error('RBK cookie must be provided.')
        return None

    data_scratch = cfg.get('data_scratch', None)
    if not data_scratch:
        logger.error('data_scratch directory must be provided.')
        return None

    metadata = cfg.get('metadata', [])

    dzi = cfg.get('dzi', None)
    if not dzi or not os.path.isdir(dzi):
        logger.error('DZI directory must be given and exist.')
        return None

    thumbnails = cfg.get('thumbnails', None)
    if not thumbnails or not os.path.isdir(thumbnails):
        logger.error('Thumbnails directory must be given and exist.')
        return None

    czi2dzi = cfg.get('czi2dzi', None)
    if not czi2dzi or not os.path.isfile(czi2dzi):
        logger.error('Convert czi to dzi application must be given and exist.')
        return None

    viewer = cfg.get('viewer', None)
    if not viewer:
        logger.error('The viewer application must be given.')
        return None

    czirules = cfg.get('czirules', None)
    if not czirules or not os.path.isfile(czirules):
        logger.error('CZI rules file must be given and exist.')
        return None

    showinf = cfg.get('showinf', None)
    if not showinf:
        logger.error('Extract metadata application must be given.')
        return None

    mail_server = cfg.get('mail_server', None)
    mail_sender = cfg.get('mail_sender', None)
    mail_receiver = cfg.get('mail_receiver', None)

    # Establish Ermrest client connection
    try:
        client = PyramidalClient(baseuri=url, \
                               cookie=cookie, \
                               data_scratch=data_scratch, \
                               metadata=metadata, \
                               dzi=dzi, \
                               thumbnails=thumbnails, \
                               czi2dzi=czi2dzi, \
                               viewer=viewer, \
                               czirules=czirules, \
                               showinf=showinf, \
                               mail_server=mail_server, \
                               mail_sender=mail_sender, \
                               mail_receiver=mail_receiver,
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
            client.start()
        except:
            sys.exit(1)
except:
    et, ev, tb = sys.exc_info()
    sys.stderr.write('got exception "%s"' % str(ev))
    sys.stderr.write('%s' % ''.join(traceback.format_exception(et, ev, tb)))
    sys.stderr.write('\nusage: env URL=https://foo.org/ermrest/catalog/N rbk_pyramidal_tiles.py --config config-file\n\n')
    sys.exit(1)

