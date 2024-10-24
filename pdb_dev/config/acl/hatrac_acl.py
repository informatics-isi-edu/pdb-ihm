#!/usr/bin/python

import sys
import json
from deriva.core import ErmrestCatalog, AttrDict, get_credential, DEFAULT_CREDENTIAL_FILE, tag, urlquote, DerivaServer, get_credential, BaseCLI
from deriva.core.ermrest_model import builtin_types, Schema, Table, Column, Key, ForeignKey
from deriva.core import urlquote, urlunquote
from deriva.core import HatracStore
import requests.exceptions
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
    global hatrac_curators_read, curator_write, hatrac_curators_write_submitters_read, hatrac_curators_write_submitters_write
    
    # general policy: submitters can create, curators can read, only owners can update existing namespaces.
    hatrac_curators_read = {
        "owner": GROUPS["owners"],    
        "subtree-owner": GROUPS["owners"],
        "subtree-create": [],
        "subtree-update": [],
        "subtree-read": GROUPS["entry-updaters"],
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
    

# ============================================================================
# helper functions
#
# add /dev prefix to namespace in the development environment. 
def adjust_hatrac_namespace(namespace):
    if cfg.is_dev:
        if namespace.startswith('/hatrac/dev'):
            return namespace
        elif namespace == "/hatrac/":
            namespace = "/hatrac/dev"
        else:
            namespace = namespace.replace("/hatrac", "/hatrac/dev", 1)
        
    return namespace

# ==============================================================================
# functions for managing acls
#
# -- ---------------------------------------------------------------------
# set one hatrac namespace acl
def set_hatrac_namespace_acl(store, acl, namespace):

    namespace = adjust_hatrac_namespace(namespace)
            
    try :
        if not store.is_valid_namespace(namespace):
            print("INFO: %s is not a valid namespace" % (namespace))
            return
    except Exception as e:
        #print("EXCEPTION %s: %s " % (namespace, e))
        return
        
    for access, roles in acl.items():
        print("    - namespace: %s seting access %s = %s" % (namespace, access, roles))
        store.set_acl(namespace, access, roles)
            
    if False:
        try :
            print("-- set rcb_access %s: %s" % (namespace, json.dumps(store.get_acl(namespace), indent=2) ))
        except Exception as e:
            pass
        
# -- ---------------------------------------------------------------------
# set acl for a list of namespaces
def set_hatrac_namespaces_acl(store, acl, namespaces):
    print("======= set_hatrac_namespaces: %s =======" % (namespaces))    
    for namespace in namespaces:
        set_hatrac_namespace_acl(store, acl, namespace)
        

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

# --------------------------------------------------------------------
# set hatrac read access based on user folders
# NOTE: DO NOT SET OWNER. LET SQL SCRIPT DEAL WITH IT
def set_hatrac_read_per_user(store, parent_namespaces=[]):
    print("======= set_hatrac_read_per_user: %s =======" % (parent_namespaces))        
    for parent in parent_namespaces:
        parent = adjust_hatrac_namespace(parent)
        try:
            uid_namespaces = store.retrieve_namespace(parent)
            print(" - UID: %s" % (uid_namespaces))
            for uid_namespace in uid_namespaces:
                uid = uid_namespace.replace(parent+"/", "")
                user_id = "https://auth.globus.org/%s" % (uid)
                acl = {
                    "subtree-read": [user_id]
                }
                set_hatrac_namespace_acl(store, acl, uid_namespace)
        except Exception as e:
            print("NO node to set READ per user at: %s, %s" % (parent, e))
    
# --------------------------------------------------------------------
# set hatrac read access based on user folders.
# Note: We no longer need to execute this in python script since it will be
# taken care of in the hourly cron job. 
def set_hatrac_write_per_user(store, parent_namespaces=[]):
    print("======= set_hatrac_write_per_user: %s =======" % (parent_namespaces))        
    for parent in parent_namespaces:
        parent = adjust_hatrac_namespace(parent)
        try:
            uid_namespaces = store.retrieve_namespace(parent)
            print(" - UID: %s" % (uid_namespaces))
            for uid_namespace in uid_namespaces:
                uid = uid_namespace.replace(parent+"/", "")
                user_id = "https://auth.globus.org/%s" % (uid)
                acl = {
                    "owner": [],
                    "subtree-owner": [],
                    "create": [user_id],
                    "subtree-create": [user_id],
                    "subtree-update": [user_id],            
                    "subtree-read": [user_id]
                }
                set_hatrac_namespace_acl(store, acl, uid_namespace)
        except Exception as e:
            print("NO node to set WRITE per user at: %s, %s" % (parent, e))

        
# -- ---------------------------------------------------------------------
# In case the namespaces (non-objects) are owned by submitters
# !!!
# NOTE: THE HATRAC APIS ARE NOT WORKING AS INTENDED. DO NOT CALL THIS FOR NOW.
# !!!
def reset_namespaces_owners(store):
    namespaces = []
    if cfg.is_dev:
        rootns = "/hatrac/dev"
    else:
        rootns = "/hatrac/"
        
    namespaces.extend(store.retrieve_namespace(rootns))

    while namespaces:
        ns = namespaces.pop(0)
        if store.is_valid_namespace(ns):
            print("+++++++++++++ ns: %s ++++++++++++" % (ns))
            roles = store.get_acl(ns, "owner")
            if roles:
                store.del_acl(ns, "owner", None)
            namespaces.extend(store.retrieve_namespace(ns))
            print("--- %s: reset owner: %s ---" % (ns, roles))
    

# =====================================================================
# functions to manage namespaces
#
# -- ---------------------------------------------------------------------
# create one hatrac namespace
def create_hatrac_namespace_if_not_exist(store, namespace):
    namespace = adjust_hatrac_namespace(namespace)

    try :
        if store.is_valid_namespace(namespace):
            return
        else:
            print("CREATE NAMESPACE: %s " % (namespace))
            store.create_namespace(namespace, parents=True)
    except Exception as e:
        print("NAMESPACE DOES NOT EXIST: %s: %s " % (namespace, e))
        print("CREATE NAMESPACE: %s " % (namespace))
        store.create_namespace(namespace, parents=True)        
        
# -- ---------------------------------------------------------------------
# create a set of hatrac namespaces
def create_hatrac_namespaces_if_not_exist(store, namespaces=[]):
    for namespace in namespaces:
        create_hatrac_namespace_if_not_exist(store, namespace)

# =====================================================================
# update subtrees ACLs of the root namespace
def set_hatrac_acl(store, catalog):

    # creating legacy namespaces on dev for proper acls. 
    if cfg.is_dev:
        create_hatrac_namespaces_if_not_exist(store, ["/hatrac/pdb/entry/submitted", "/hatrac/pdb/user"])  

    # -- new policy
    create_hatrac_namespaces_if_not_exist(store, ["/hatrac/pdb/templates", "/hatrac/pdb/submitted/uid", "/hatrac/pdb/generated/uid", "/hatrac/pdb/public/images"])
    set_hatrac_namespaces_acl(store, hatrac_curators_read, ["/hatrac/"])
    # remove unnecessary policies    
    set_hatrac_namespaces_acl(store, hatrac_reset_acls, ["/hatrac/pdb", "/hatrac/pdb/submitted", "/hatrac/pdb/generated"])
    set_hatrac_namespaces_acl(store, hatrac_curators_write_submitters_read, ["/hatrac/pdb/templates", "/hatrac/pdb/public"])
    set_hatrac_namespaces_acl(store, hatrac_curators_write_submitters_write, ["/hatrac/pdb/submitted/uid", "/hatrac/pdb/user"])
    set_hatrac_namespaces_acl(store, hatrac_curators_write, ["/hatrac/pdb/generated/uid"])
    set_hatrac_read_per_user(store, ["/hatrac/pdb/generated/uid"])

    # no need to set this up here as it covers in hourly job
    # set_hatrac_write_per_user(store, ["/hatrac/pdb/submitted/uid", "/hatrac/pdb/user"]) 
        
    # legacy tree on all envs. Only turns this to True if needs to rerun the acl for legacy trees.
    if False:
        set_hatrac_namespaces_acl(store, hatrac_curators_write, ["/hatrac/pdb/entry"])    
        set_hatrac_namespaces_acl(store, hatrac_curators_write_submitters_write, ["/hatrac/pdb/entry/submitted"])
        set_hatrac_namespaces_acl(store, hatrac_reset_acls, ["/hatrac/pdb/entry_files", "/hatrac/pdb/entry_mmCIF", "/hatrac/pdb/mmCIF", "/hatrac/pdb/image"])
        set_hatrac_read_per_rid(store, catalog)
        set_hatrac_read_legacy_submitted_files(store, catalog)

    
# =====================================================================

def main(server_name, catalog_id, credentials):
    initialize_policies()
    initialize_hatrac_policies()    
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
