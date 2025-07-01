#!/usr/bin/python

import sys
import json
import requests.exceptions
from deriva.core import ErmrestCatalog, AttrDict, get_credential, DEFAULT_CREDENTIAL_FILE, tag, urlquote, DerivaServer, get_credential, BaseCLI
from deriva.core.ermrest_model import builtin_types, Schema, Table, Column, Key, ForeignKey
from deriva.core import urlquote, urlunquote
from deriva.core import HatracStore
from deriva.utils.extras.hatrac_acl import set_hatrac_namespaces_acl, create_hatrac_namespaces_if_not_exist, set_hatrac_read_per_user, set_hatrac_write_per_user
from deriva.utils.extras.model import ermrest_groups, set_ermrest_groups
from ...utils import DCCTX, PDBDEV_CLI, cfg
from .ermrest_acl import GROUPS, initialize_policies
import re

# remove all members from namespaces. Read/update doesn't work on namespace.
hatrac_reset_acls = {
    "owner": [],
    "create": [],
    "subtree-owner": [],
    "subtree-create": [],
    "subtree-update": [],
    "subtree-read": [],
}
hatrac_curators_read = {}
hatrac_curators_write_submitters_read = {}
hatrac_curators_write_submitters_write = {}
hatrac_curators_write = {}

def initialize_hatrac_policies():
    global hatrac_curators_read, hatrac_curators_write, hatrac_curators_write_submitters_read, hatrac_curators_write_submitters_write
    
    # general policy: submitters can create, curators can read, only owners can update existing namespaces.
    hatrac_curators_read = {
        "owner": GROUPS["owners"],    
        "subtree-owner": GROUPS["owners"],
        "subtree-create": [],
        "subtree-update": [],
        "subtree-read": GROUPS["entry-updaters"] + GROUPS["entry-readers"],
    }

    # no need to set subtree-read for curators. In herit from root.
    hatrac_curators_write = {
        "owner": [],
        "subtree-owner": [],    
        "create": GROUPS["entry-updaters"],
        "subtree-create": GROUPS["entry-updaters"],
        "subtree-update": GROUPS["entry-updaters"],
        "subtree-read":  [],
    }

    # policy: submitters cannot create, curators can read/write, only owners can update existing namespaces.
    # curator_read inherits from parent namespace
    hatrac_curators_write_submitters_read = {
        "owner": [],
        "subtree-owner": [],
        "create": GROUPS["entry-updaters"],
        "subtree-create": GROUPS["entry-updaters"],
        "subtree-update": GROUPS["entry-updaters"],
        "subtree-read": GROUPS["pdb-submitters"],
    }
    
    # policy: curators and submitters can create/update. The read access will be given to appropriate submitter in the shell script. 
    # no need to set subtree-read for curators. In herit from root.
    hatrac_curators_write_submitters_write = {
        "owner": [],
        "subtree-owner": [],    
        "create": GROUPS["entry-updaters"] + GROUPS["pdb-submitters"],
        "subtree-create": GROUPS["entry-updaters"] + GROUPS["pdb-submitters"],
        "subtree-update": GROUPS["entry-updaters"] + GROUPS["pdb-submitters"],
        "subtree-read": [],
    }
    


# ==============================================================================
# functions for managing acls
#
# -- ---------------------------------------------------------------------
# set read acl for individual submitters based on RID.
# This function is needed to address old namespace strategy
# NOTE: DO NOT SET OWNER. LET SQL SCRIPT DEAL WITH IT
def set_hatrac_read_per_rid(store, catalog):
    model = catalog.getCatalogModel()
    table = model.schemas["PDB"].tables["entry"]
    global count
    count = 0
    resp = catalog.get("/attribute/PDB:entry/RCB,RID,RCT")
    rows = resp.json()

    print("======= set_hatrac_read_per_rid =======")
    
    for row in rows:
        year = row["RCT"].split("-")[0]
        namespace = "/hatrac/pdb/entry/%s/D_%s" % (year, row["RID"])
        acl = {
            "subtree-read": [row["RCB"]]
        }
        set_hatrac_namespace_acl(store, acl, namespace)

# --------------------------------------------------------------------
# set read acl for individual submitters based on URL in the entry.
# This function is needed to address old namespace strategy.
# NOTE: DO NOT SET OWNER. LET SQL SCRIPT DEAL WITH IT
def set_hatrac_read_legacy_submitted_files(store, catalog):
    model = catalog.getCatalogModel()
    table = model.schemas["PDB"].tables["entry"]
    resp = catalog.get("/attribute/PDB:entry/RCB,RID,RCT,Image_File_URL,mmCIF_File_URL")
    rows = resp.json()
    pattern = "/hatrac(/dev)*/pdb/(entry_files|entry_mmCIF|mmCIF|image|entry/submitted)/.*"

    print("======= set_hatrac_read_legacy_submitted_files =======")
    for row in rows:
        acl = {
            "read": [row["RCB"]],
            "subtree-read": [row["RCB"]]
        }
        if row["Image_File_URL"] and re.search(pattern, row["Image_File_URL"]) :
            image_object = row["Image_File_URL"].split(":")[0]
            #print("image object: %s" % (image_object))
            set_hatrac_namespace_acl(store, acl, image_object)
            
        if row["mmCIF_File_URL"] and re.search(pattern, row["mmCIF_File_URL"]) :
            mmcif_object = row["mmCIF_File_URL"].split(":")[0]
            #print("mmCIF object: %s" % (mmcif_object))            
            set_hatrac_namespace_acl(store, acl, mmcif_object)

# =====================================================================
# functions to manage namespaces
#

# =====================================================================
# update subtrees ACLs of the root namespace
def set_hatrac_acl(store, catalog):
    initialize_policies(catalog)
    initialize_hatrac_policies()    

    # creating legacy namespaces on dev for proper acls. 
    if cfg.is_dev:
        create_hatrac_namespaces_if_not_exist(store, ["/hatrac/pdb/entry/submitted", "/hatrac/pdb/user"], cfg.hatrac_root)  

    # -- new policy
    create_hatrac_namespaces_if_not_exist(store, ["/hatrac/pdb/templates", "/hatrac/pdb/submitted/uid", "/hatrac/pdb/generated/uid", "/hatrac/pdb/public/images", "/hatrac/pdb/internal"], cfg.hatrac_root)
    set_hatrac_namespaces_acl(store, hatrac_curators_read, ["/hatrac"], cfg.hatrac_root)
    # remove unnecessary policies    
    set_hatrac_namespaces_acl(store, hatrac_reset_acls, ["/hatrac/pdb", "/hatrac/pdb/submitted", "/hatrac/pdb/generated"], cfg.hatrac_root)
    set_hatrac_namespaces_acl(store, hatrac_curators_write_submitters_read, ["/hatrac/pdb/templates", "/hatrac/pdb/public"], cfg.hatrac_root)
    set_hatrac_namespaces_acl(store, hatrac_curators_write_submitters_write, ["/hatrac/pdb/submitted/uid", "/hatrac/pdb/user"], cfg.hatrac_root)
    set_hatrac_namespaces_acl(store, hatrac_curators_write, ["/hatrac/pdb/generated/uid", "/hatrac/pdb/internal"], cfg.hatrac_root)

    # -- no need to set this up here as it covers in hourly job
    # set_hatrac_read_per_user(store, ["/hatrac/pdb/generated/uid"], cfg.hatrac_root)
    # set_hatrac_write_per_user(store, ["/hatrac/pdb/submitted/uid", "/hatrac/pdb/user"]) 
        
    # legacy tree on all envs. Only turns this to True if needs to rerun the acl for legacy trees.
    if False:
        set_hatrac_namespaces_acl(store, hatrac_curators_write, ["/hatrac/pdb/entry"], cfg.hatrac_root)    
        set_hatrac_namespaces_acl(store, hatrac_curators_write_submitters_write, ["/hatrac/pdb/entry/submitted"], cfg.hatrac_root)
        set_hatrac_namespaces_acl(store, hatrac_reset_acls, ["/hatrac/pdb/entry_files", "/hatrac/pdb/entry_mmCIF", "/hatrac/pdb/mmCIF", "/hatrac/pdb/image"], cfg.hatrac_root)
        set_hatrac_read_per_rid(store, catalog)
        set_hatrac_read_legacy_submitted_files(store, catalog)

    
# =====================================================================

def main(server_name, catalog_id, credentials):
    server = DerivaServer("https", server_name, credentials)
    catalog = server.connect_ermrest(catalog_id)
    catalog.dcctx["cid"] = DCCTX["acl"]
    store = HatracStore("https", server_name, credentials)

    set_hatrac_acl(store, catalog)

    
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
