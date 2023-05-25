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
hatrac_acl = {
    "owner": GROUPS["owners"],    
    "subtree-owner": GROUPS["owners"],
    "subtree-create": GROUPS["entry-updaters"],
    "subtree-update": [],
    "subtree-read": GROUPS["entry-updaters"],
}

# policy: submitters cannot create, curators can read/write, only owners can update existing namespaces.
hatrac_curators_own_submitters_read = {
    "owner": GROUPS["entry-updaters"],
    "subtree-owner": GROUPS["entry-updaters"],
    "subtree-create": [],
    "subtree-update": [],
    "subtree-read": GROUPS["pdb-submitters"],
}

hatrac_curator_own_submitters_create = {
    "owner": GROUPS["entry-updaters"],
    "subtree-owner": GROUPS["entry-updaters"],
    "subtree-create": GROUPS["pdb-submitters"],
    "subtree-update": [],
    "subtree-read": [],
}

# policy: entry_owner is the owner of <RID> based folder, curators can read, only owners can update existing namespaces.
hatrac_curators_own = {
    "owner": GROUPS["entry-updaters"],
    "subtree-owner": GROUPS["entry-updaters"],
    "subtree-create": [],
    "subtree-update": [],
    "subtree-read": [],
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
# -- ---------------------------------------------------------------------
def set_hatrac_namespace_acl(store, acl, namespace):
    global count

    if cfg.is_dev:
        if namespace == "/hatrac/":        
            namespace = "/hatrac/dev" 
        else:
            namespace = namespace.replace("/hatrac", "/hatrac/dev", 1)
            
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
def set_hatrac_rcb_access(store, catalog):
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

# -- ---------------------------------------------------------------------
# In case the namespaces (non-objects) are owned by submitters
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
    
                      
    
# -- ---------------------------------------------------------------------
# update subtrees ACLs of the root namespace
def set_hatrac_acl(store, catalog):

    set_hatrac_namespaces_acl(store, hatrac_acl, ["/hatrac/"])
    set_hatrac_namespaces_acl(store, hatrac_curators_own_submitters_read, ["/hatrac/pdb/templates"])
    set_hatrac_namespaces_acl(store, hatrac_curators_own, ["/hatrac/pdb/entry"])    
    set_hatrac_namespaces_acl(store, hatrac_curators_own_submitters_create, ["/hatrac/pdb/entry/submitted"])
    set_hatrac_namespaces_acl(store, hatrac_reset_acls, ["/hatrac/pdb/entry_files", "/hatrac/pdb/entry_mmCIF", "/hatrac/pdb/mmCIF", "/hatrac/pdb/image"])

    set_hatrac_rcb_access(store, catalog)
    #reset_namespaces_owners(store)
    
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
