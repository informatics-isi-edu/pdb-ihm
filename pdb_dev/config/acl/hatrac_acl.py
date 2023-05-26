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

# general policy: submitters can create, curators can read, only owners can update existing namespaces.
hatrac_curators_read = {
    "owner": GROUPS["owners"],    
    "subtree-owner": GROUPS["owners"],
    "subtree-create": [],
    "subtree-update": [],
    "subtree-read": GROUPS["entry-updaters"],
}

# policy: submitters cannot create, curators can read/write, only owners can update existing namespaces.
hatrac_curators_write_submitters_read = {
    "owner": [],
    "subtree-owner": [],
    "create": GROUPS["entry-updaters"],
    "subtree-create": GROUPS["entry-updaters"],
    "subtree-update": GROUPS["entry-updaters"],
    "subtree-read": GROUPS["entry-updaters"] + GROUPS["pdb-submitters"],
}

hatrac_curators_write_submitters_write = {
    "owner": [],
    "subtree-owner": [],    
    "create": GROUPS["entry-updaters"] + GROUPS["pdb-submitters"],
    "subtree-create": GROUPS["entry-updaters"] + GROUPS["pdb-submitters"],
    "subtree-update": GROUPS["entry-updaters"] + GROUPS["pdb-submitters"],
    "subtree-read": GROUPS["entry-updaters"] + GROUPS["pdb-submitters"],
}

# policy: entry_owner is the owner of <RID> based folder, curators can read, only owners can update existing namespaces.
hatrac_curators_write = {
    "owner": [],
    "subtree-owner": [],    
    "create": GROUPS["entry-updaters"],
    "subtree-create": GROUPS["entry-updaters"],
    "subtree-update": GROUPS["entry-updaters"],
    "subtree-read":  GROUPS["entry-updaters"],
}

hatrac_reset_acls = {
    "owner": [],
    "subtree-owner": [],
    "subtree-create": [],
    "subtree-update": [],
    "subtree-read": [],
}

count=0
# =====================================================================
# hatrac
# =====================================================================
def adjust_hatrac_namespace(namespace):
    if cfg.is_dev:
        if namespace == "/hatrac/":        
            namespace = "/hatrac/dev" 
        elif not namespace.startswith('/hatrac/dev'):
            namespace = namespace.replace("/hatrac", "/hatrac/dev", 1)
            
    return namespace
    
# -- ---------------------------------------------------------------------
def set_hatrac_namespace_acl(store, acl, namespace):
    global count

    namespace = adjust_hatrac_namespace(namespace)
            
    # TODO: create namespace if doesn't exist
    
    try :
        if not store.is_valid_namespace(namespace):
            print("%s is not a valid namespace" % (namespace))
            return
    except Exception as e:
        print("EXCEPTION %s: %s " % (namespace, e))
        return
        
    for access, roles in acl.items():
        if cfg.is_dev and GROUPS["pdb-curators"][0] in roles:
            print("    - namespace: %s seting access %s = %s" % (namespace, access, roles+GROUPS["isrd-testers"]))            
            store.set_acl(namespace, access, roles+GROUPS["isrd-testers"])
        else:
            print("    - namespace: %s seting access %s = %s" % (namespace, access, roles))
            store.set_acl(namespace, access, roles)
            
    count = count+1
    if False:
        try :
            print("-- set rcb_access %s: %s" % (namespace, json.dumps(store.get_acl(namespace), indent=2) ))
        except Exception as e:
            pass
        
# -- ---------------------------------------------------------------------
def set_hatrac_namespaces_acl(store, acl, namespaces):
    for namespace in namespaces:
        set_hatrac_namespace_acl(store, acl, namespace)
        

# -- ---------------------------------------------------------------------
'''
SELECT e.id, f."RID", m."RID" FROM "PDB".entry e LEFT join "PDB"."Entry_Related_File" f ON (e.id = f.structure_id)
LEFT JOIN "PDB"."Entry_mmCIF_File" m ON (e.id = m."Structure_Id")
'''
def set_hatrac_rcb_read_per_rid(store, catalog):
    model = catalog.getCatalogModel()
    table = model.schemas["PDB"].tables["entry"]
    global count
    count = 0
    resp = catalog.get("/attribute/PDB:entry/RCB,RID,RCT")
    rows = resp.json()
    #print("---------------- number of rows: %d --------------" % (len(rows)))
    
    for row in rows:
        year = row["RCT"].split("-")[0]
        namespace = "/hatrac/pdb/entry/%s/D_%s" % (year, row["RID"])
        acl = {
            "subtree-read": [row["RCB"]]
        }
        set_hatrac_namespace_acl(store, acl, namespace)

# --------------------------------------------------------------------
# set hatrac read access based on user folders
def set_hatrac_read_per_user(store, parent_namespaces=[]):
    for parent in parent_namespaces:
        parent = adjust_hatrac_namespace(parent)
        try:
            uid_namespaces = store.retrieve_namespace(parent)
            print(" - UID: %s" % (uid_namespaces))
            for uid_namespace in uid_namespaces:
                uid = uid_namespace.replace(parent+"/", "")
                user_id = "https://auth.globus.org/%s" % (uid)
                acl = {
                    "create": [user_id],
                    "subtree-create": [user_id],
                    "subtree-update": [user_id],            
                    "subtree-read": [user_id]
                }
                set_hatrac_namespace_acl(store, acl, uid_namespace)
        except Exception as e:
            print("NO node to set READ per user at: %s, %s" % (parent, e))
    
# --------------------------------------------------------------------
# set hatrac read access based on user folders
def set_hatrac_write_per_user(store, parent_namespaces=[]):
    for parent in parent_namespaces:
        parent = adjust_hatrac_namespace(parent)
        try:
            uid_namespaces = store.retrieve_namespace(parent)
            print(" - UID: %s" % (uid_namespaces))
            for uid_namespace in uid_namespaces:
                uid = uid_namespace.replace(parent+"/", "")
                user_id = "https://auth.globus.org/%s" % (uid)
                acl = {
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
# THE HATRAC APIS ARE NOT WORKING AS INTENDED. DO NOT CALL THIS FOR NOW.
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
# -- ---------------------------------------------------------------------
def create_hatrac_namespace(store, namespace):
    namespace = adjust_hatrac_namespace(namespace)

    try :
        if store.is_valid_namespace(namespace):
            return
        else:
            print("CREATE NAMESPACE: %s " % (namespace))
            store.create_namespace(namespace, parents=True)
    except Exception as e:
        print("EXCEPTION NAMESPACE DOES NOT EXIST: %s: %s " % (namespace, e))
        print("CREATE NAMESPACE: %s " % (namespace))
        store.create_namespace(namespace, parents=True)        
        
# -- ---------------------------------------------------------------------
def create_hatrac_namespaces(store, namespaces=[]):
    for namespace in namespaces:
        create_hatrac_namespace(store, namespace)

# =====================================================================
# update subtrees ACLs of the root namespace
def set_hatrac_acl(store, catalog):

    # legacy tree
    if True:
        set_hatrac_namespaces_acl(store, hatrac_curators_read, ["/hatrac/"])
        set_hatrac_namespaces_acl(store, hatrac_curators_write_submitters_read, ["/hatrac/pdb/templates"])
        set_hatrac_namespaces_acl(store, hatrac_curators_write_submitters_read, ["/hatrac/pdb/entry"])    
        set_hatrac_namespaces_acl(store, hatrac_curators_write_submitters_write, ["/hatrac/pdb/entry/submitted"])
        set_hatrac_namespaces_acl(store, hatrac_reset_acls, ["/hatrac/pdb/entry_files", "/hatrac/pdb/entry_mmCIF", "/hatrac/pdb/mmCIF", "/hatrac/pdb/image"])
        set_hatrac_rcb_read_per_rid(store, catalog)

    # -- new policy
    create_hatrac_namespaces(store, ["/hatrac/pdb/user", "/hatrac/pdb/submitted/uid", "/hatrac/pdb/generated/uid"])
    set_hatrac_namespaces_acl(store, hatrac_curators_write, ["/hatrac/pdb/submitted/uid", "/hatrac/pdb/generated/uid", "/hatrac/pdb/user"])
    set_hatrac_write_per_user(store, ["/hatrac/pdb/submitted/uid", "/hatrac/pdb/user"])
    set_hatrac_read_per_user(store, ["/hatrac/pdb/generated/uid"])
    
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
