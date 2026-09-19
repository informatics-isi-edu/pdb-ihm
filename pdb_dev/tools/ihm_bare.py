#!/usr/bin/python3

import json
import sys
import os

from deriva.core import ErmrestCatalog, HatracStore, urlquote, get_credential, DerivaServer, BaseCLI

ENV="dev"
default_host = "data-dev.pdb-ihm.org" if ENV=="dev" else "data.pdb-ihm.org"
default_catalog_id = "99" if ENV=="dev" else "1"

def get_user_uid(catalog, uid_only=True):
    r = catalog.get_authn_session()
    session = r.json()
    id = session["client"]["id"]
    uid = id.rsplit("/", 1)[1]
    
    #print(json.dumps(session, indent=4))
    print(f"id: {id}, uid: {uid}")
    
    return uid if uid_only else id


# -- =================================================================================

def main():
    cli = BaseCLI("ihm", None, 1)
    cli.remove_options(['--host']) # remove default params
    cli.parser.add_argument('--host', metavar='host', help="DERIVA host", default=default_host, required=False)
    cli.parser.add_argument('--catalog-id', metavar='catalog_id', help="catalog id", default=default_catalog_id, required=False)        
    args = cli.parse_cli()
    
    server_name = args.host 
    credentials = get_credential(server_name, args.credential_file)
    server = DerivaServer('https', server_name, credentials)
    store = HatracStore('https', server_name, credentials)
    catalog = server.connect_ermrest(args.catalog_id)

    get_user_uid(catalog)
    
    return 0
    

 # -- =================================================================================
if __name__ == '__main__':
    
    sys.exit(main())

