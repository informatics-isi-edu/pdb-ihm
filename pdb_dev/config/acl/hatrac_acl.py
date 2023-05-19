#!/usr/bin/python

import sys
import json
from deriva.core import ErmrestCatalog, AttrDict, get_credential, DEFAULT_CREDENTIAL_FILE, tag, urlquote, DerivaServer, get_credential, BaseCLI
from deriva.core.ermrest_model import builtin_types, Schema, Table, Column, Key, ForeignKey
from deriva.core import urlquote, urlunquote
from deriva.core import HatracStore
import requests.exceptions
from ...utils import DCCTX, PDBDEV_CLI, cfg
from .ermrest_acl import GROUPS

hatrac_acl = {
    "owner": GROUPS["owners"],    
    "subtree-owner": GROUPS["owners"],
    "subtree-create": GROUPS["entry-creators"],
    "subtree-update": GROUPS["entry-creators"],
    "subtree-read": GROUPS["entry-creators"],
}

hatrac_submitters_cannot_write = {
    "owner": GROUPS["owners"],    
    "subtree-owner": GROUPS["owners"],
    "subtree-create": GROUPS["entry-updaters"],
    "subtree-update": GROUPS["entry-updaters"],
    "subtree-read": GROUPS["entry-creators"],
}

hatrac_acl_dev = {
    "owner": GROUPS["owners"],    
    "subtree-owner": GROUPS["owners"],
    "subtree-create": GROUPS["entry-creators"] + GROUPS["isrd-testers"],
    "subtree-update": GROUPS["entry-creators"] + GROUPS["isrd-testers"],
    "subtree-read": GROUPS["entry-creators"] + GROUPS["isrd-testers"],
}

hatrac_submitters_cannot_write_dev = {
    "owner": GROUPS["owners"],    
    "subtree-owner": GROUPS["owners"],
    "subtree-create": GROUPS["entry-updaters"] + GROUPS["isrd-testers"],
    "subtree-update": GROUPS["entry-updaters"] + GROUPS["isrd-testers"],
    "subtree-read": GROUPS["entry-creators"] + GROUPS["isrd-testers"],
}


# =====================================================================
# hatrac
# -- ---------------------------------------------------------------------
# update subtrees ACLs of the root namespace
def set_hatrac_acl(store):

    if cfg.is_prod or cfg.is_staging:
        for namespace in ["/hatrac/"]:        
            for access, roles in hatrac_acl.items():
                store.set_acl(namespace, access, roles)
            print("-- set prod acl %s: %s" % (namespace, store.get_acl(namespace)))
        # templates: remove pdb-submitters from writing to templates folder
        for namespace in ["/hatrac/pdb/templates"]:
            for access, roles in hatrac_submitters_cannot_write.items():
                store.set_acl(namespace, access, roles)            
            print("-- set prod acl submitters cannot create %s: %s" % (namespace, store.get_acl(namespace)))
    else:
        for namespace in ["/hatrac/dev"]:        
            for access, roles in hatrac_acl_dev.items():
                store.set_acl(namespace, access, roles)
            print("-- set dev acl %s: %s" % (namespace, store.get_acl(namespace)))                
        # templates: remove pdb-submitters from writing to templates folder
        for namespace in []:
            for access, roles in hatrac_submitters_cannot_write.items():
                store.set_acl(namespace, access, roles)            
            print("-- set dev acl submitters cannot create %s: %s" % (namespace, store.get_acl(namespace)))

    # clean up    
    if cfg.is_staging:            
        for namespace in ["/hatrac/pdb", "/hatrac/pdb/mmCIF", "/hatrac/pdb/image", "/hatrac/pdb/entry_files", "/hatrac/pdb/entry_mmCIF"]:
            for access, roles in hatrac_acl.items():
                if access == "owner":
                    store.set_acl(namespace, "owner", GROUPS["owners"])                    
                else:
                    store.del_acl(namespace, access, None)
    
# =====================================================================

def main(server_name, catalog_id, credentials):
    server = DerivaServer("https", server_name, credentials)
    catalog = server.connect_ermrest(catalog_id)
    catalog.dcctx["cid"] = DCCTX["acl"]
    store = HatracStore("https", server_name, credentials)

    set_hatrac_acl(store)

    
# -- =================================================================================
# Install the Python package:
#    From the protein-database directory, run: 
#        pip3 install --upgrade --no-deps .
#
# Running the script:
#    python3 -m pdb_dev.config.acl.hatrac_acl --host dev.pdb-dev.org --catalog-id 99 
#
if __name__ == "__main__":
    args = PDBDEV_CLI(DCCTX["acl"], None, 1).parse_cli()
    credentials = get_credential(args.host, args.credential_file)
    print("credential: %s" % (credentials))
    main(args.host, args.catalog_id, credentials)
