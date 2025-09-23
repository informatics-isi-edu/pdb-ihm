#!/usr/bin/python

import sys
import json
import requests.exceptions

from deriva.core import ErmrestCatalog, AttrDict, get_credential, DEFAULT_CREDENTIAL_FILE, tag, urlquote, DerivaServer, get_credential, BaseCLI, urlquote, urlunquote
from deriva.core.ermrest_model import builtin_types, Schema, Table, Column, Key, ForeignKey
from deriva.core import HatracStore
from pdb_dev.utils.shared import DCCTX, PDBDEV_CLI, cfg


def delete_catalog(catalog):
    """
    To delete a catalog, 1) delete catalog (this script),
    2) turn off httpd service, 3) as ermrest, purge from the registry with deriva-client ermrest-registry-purge command 
    """
    catalog.delete_ermrest_catalog(really=True)
    return


"""
Note: if needed to turn catalog 1 to another alias, we will need to clone the catalog, then drop the catalog from database
      before creating an alias of "1"
"""

def main(server_name, catalog_id, credentials):
    server = DerivaServer('https', server_name, credentials)
    store = HatracStore('https', server_name, credentials)
    
    # create a catalog if doesn't exist. Let ermrest assign catalog 1 to use as a default
    if cfg.is_prod:
        catalog = server.connect_ermrest(catalog_id)
        if not catalog.exists():
            print("creating prod catalog with id: %s" % (catalog_id))            
            server.create_ermrest_catalog(name="IHMV production catalog", id=catalog_id)
    elif cfg.is_staging:
        catalog = server.connect_ermrest(catalog_id)
        if not catalog.exists():
            print("creating staging catalog with id: %s" % (catalog_id))
            server.create_ermrest_catalog(name="IHMV staging catalog", id=catalog_id)
    else:
        # create a catalog if doesn't exist
        catalog = server.connect_ermrest(catalog_id)
        if not catalog.exists():
            print("creating dev catalog with id: %s" % (catalog_id))            
            server.create_ermrest_catalog(name="IHMV development catalog", id=catalog_id)
            #server.create_ermrest_alias(id="ihmv-dev", alias_target=catalog_id, name="IHMV development catalog alias")

    
    

# -- =================================================================================

if __name__ == '__main__':
    args = PDBDEV_CLI(DCCTX["model"], None, 1).parse_cli()
    credentials = get_credential(args.host, args.credential_file)
    main(args.host, args.catalog_id, credentials)
