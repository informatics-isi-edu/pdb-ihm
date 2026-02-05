from deriva.core import ErmrestCatalog, HatracStore, AttrDict, get_credential, DEFAULT_CREDENTIAL_FILE, tag, urlquote, DerivaServer, get_credential, BaseCLI
from deriva.core.ermrest_model import builtin_types, Schema, Table, Column, Key, ForeignKey, tag, AttrDict
from deriva.core import urlquote, urlunquote, DEFAULT_SESSION_CONFIG
from deriva.core.utils.hash_utils import compute_hashes

#from ..utils.shared import PDBDEV_CLI, DCCTX, cfg
from pdb_dev.utils.shared import PDBDEV_CLI, DCCTX, cfg
from deriva.utils.extras.data import get_ermrest_query, insert_if_not_exist, update_table_rows, delete_table_rows
from deriva.utils.extras.pdb_ma.mmcif_model import mmCIFErmrestModel, dump_json_to_file

# ----------------------------------------------------------------------
# TODO: fix names in mmcif_model.py
#
def compare_models(model, mmcif_ermrest_model):
    pdb_sdocs = mmcif_ermrest_model.ermrest_domain_schema

    pdb_schema = model.schemas["PDB"]
    pdb_tnames = set(pdb_schema.tables.keys())
    mmcif_tnames = set(pdb_sdocs["tables"].keys())
    
    intersection = mmcif_tnames & pdb_tnames
    mmcif_only = mmcif_tnames - pdb_tnames
    pdb_only = pdb_tnames - mmcif_tnames
    print()
    print("\nmmcif_tnames & ermrest_tnames [%d]: %s" % (len(intersection), sorted(intersection)))
    print("\nmmcif_tnames only [%d]: %s" % (len(mmcif_only), sorted(mmcif_only)))
    print("\nermrest_tnames only [%d]: %s" % (len(pdb_only), sorted(pdb_only)))

    
    for tname in sorted(intersection):
        pdb_table = pdb_schema.tables[tname]
        mmcif_table = pdb_sdocs["tables"][tname]
        attention = False
        
        # ==== column diff
        pdb_cnames = set(pdb_table.columns.elements)
        mmcif_cnames = { c["name"] for c in mmcif_table["column_definitions"] }
        
        intersection = mmcif_cnames & pdb_cnames
        mmcif_only = mmcif_cnames - pdb_cnames
        pdb_only = pdb_cnames - mmcif_cnames

        for cname in mmcif_only:
            if not cname.endswith("RID"): attention = True
        for cname in pdb_only:
            if cname not in ["Owner", "Entry_Related_File"]: attention = True
            
        print("\n===== tname: %s  %s" % (tname, "C-ATTENTION" if attention else ""))
        print("- c: intersection: tname:%s [%d]: %s" % (tname, len(intersection), sorted(intersection)))
        print("- c: mmcif only: tname:%s [%d]: %s" % (tname, len(mmcif_only), sorted(mmcif_only)))
        print("- c: ermrest only: tname:%s [%d]: %s" % (tname, len(pdb_only), sorted(pdb_only)))

        # ==== fkey diff
        pdb_fkey_cnames2fkeys = {}
        mmcif_fkey_cnames2fkeys = {}
        
        pdb_fkeys_cnames = set()
        for fkey in pdb_table.foreign_keys:
            from_cnames = [c.name for c in fkey.column_map.keys()]
            to_cnames = [c.name for c in fkey.column_map.values()]
            pk_table = fkey.pk_table
            ct_name = fkey.constraint_name
            #print("== fk-pdb: pdb: from_cnames: %s, to_cnames: %s " % (from_cnames, to_cnames))
            pdb_fkeys_cnames.add(tuple(sorted(from_cnames)))
            pdb_fkey_cnames2fkeys[tuple(sorted(from_cnames))] = (ct_name, from_cnames, pk_table.name, to_cnames)

        mmcif_fkeys_cnames = set()
        for fkey in pdb_sdocs["tables"][tname]["foreign_keys"]:
            from_cnames = [ c["column_name"] for c in fkey["foreign_key_columns"]]
            to_cnames = [ c["column_name"] for c in fkey["referenced_columns"]]
            pk_tname = fkey["referenced_columns"][0]["table_name"]
            ct_name = fkey["names"][0]
            
            #print("== fk-mmcif: pdb: from_cnames: %s, to_cnames: %s " % (from_cnames, to_cnames))            
            mmcif_fkeys_cnames.add(tuple(sorted(from_cnames)))
            mmcif_fkey_cnames2fkeys[tuple(sorted(from_cnames))] = (ct_name, from_cnames, pk_tname, to_cnames)
            
        intersection = mmcif_fkeys_cnames & pdb_fkeys_cnames
        mmcif_only = mmcif_fkeys_cnames - pdb_fkeys_cnames
        pdb_only = pdb_fkeys_cnames - mmcif_fkeys_cnames
        print()
        print("- fk: intersection: tname:%s [%d]: %s" % (tname, len(intersection), sorted(intersection)))
        print("- fk: mmcif only: tname:%s [%d]: %s" % (tname, len(mmcif_only), sorted(mmcif_only)))
        print("- fk: ermrest only: tname:%s [%d]: %s" % (tname, len(pdb_only), sorted(pdb_only)))

        # to remove: natural and combo2
        pdb_to_remove=set()
        for fkey_cnames in pdb_only:
            (ct_name, from_cnames, pk_tname, to_cnames) = pdb_fkey_cnames2fkeys[fkey_cnames]
            if "structure_id" in fkey_cnames or ("RID" in to_cnames and "structure_id" not in from_cnames and len(fkey_cnames) > 1):
                pdb_to_remove.add(fkey_cnames)
        print("-> fk-rm: ermrest only: tname:%s [%d]: " % (tname, len(pdb_to_remove)))
        for fkey_cnames in sorted(pdb_to_remove):
            print("     - rm: %s" % (list(pdb_fkey_cnames2fkeys[fkey_cnames])))

        # to add
        pdb_to_add=set()
        for fkey_cnames in mmcif_only:
            (ct_name, from_cnames, pk_tname, to_cnames) = mmcif_fkey_cnames2fkeys[fkey_cnames]
            pdb_to_add.add(fkey_cnames)
        #print("-> fk-add: mmcif only: tname:%s [%d]: %s" % (tname, len(pdb_to_add), [ mmcif_fkey_cnames2fkeys[fkey_cnames] for fkey_cnames in sorted(pdb_to_add) ] ))
        print("-> fk-add: mmcif only: tname:%s [%d]: " % (tname, len(pdb_to_add)))
        for fkey_cnames in sorted(pdb_to_add):
            print("     - add: %s" % (list(mmcif_fkey_cnames2fkeys[fkey_cnames])))

        # ==== key diff
        pdb_kcnames2ctname = {}
        pdb_keys_cnames = set()
        for key in pdb_table.keys:
            from_cnames = [c.name for c in key.columns ] 
            ct_name = [ key.name[0].name, key.name[1] ]
            pdb_keys_cnames.add(tuple(sorted(from_cnames)))
            pdb_kcnames2ctname[tuple(sorted(from_cnames))] = ct_name
            
        mmcif_kcnames2ctname = {}
        mmcif_keys_cnames = set()
        for key in pdb_sdocs["tables"][tname]["keys"]:
            from_cnames = key["unique_columns"]
            ct_name = key["names"][0]
            mmcif_keys_cnames.add(tuple(sorted(from_cnames)))
            mmcif_kcnames2ctname[tuple(sorted(from_cnames))] = ct_name
            
        intersection = mmcif_keys_cnames & pdb_keys_cnames
        mmcif_only = mmcif_keys_cnames - pdb_keys_cnames
        pdb_only = pdb_keys_cnames - mmcif_keys_cnames
        print()
        print("- k: intersection: tname:%s [%d]: %s" % (tname, len(intersection), sorted(intersection)))
        print("- k: mmcif only: tname:%s [%d]: %s" % (tname, len(mmcif_only), sorted(mmcif_only)))
        print("- k: ermrest only: tname:%s [%d]: %s" % (tname, len(pdb_only), sorted(pdb_only)))

        # to remove: natural and combo2
        pdb_to_remove=set()
        for key_cnames in pdb_only:
            if "RID" in key_cnames and "structure_id" not in key_cnames and len(key_cnames) > 1:
                pdb_to_remove.add(key_cnames)
        print("-> k-rm: ermrest only: tname:%s [%d]: %s " % (tname, len(pdb_to_remove), [ ( kcnames, pdb_kcnames2ctname[kcnames] ) for kcnames in sorted(pdb_to_remove) ]))

        # to add
        pdb_to_add=mmcif_only
        print("-> k-add: mmcif only: tname:%s [%d]: %s " % (tname, len(pdb_to_add), [ ( kcnames, mmcif_kcnames2ctname[kcnames] ) for kcnames in sorted(pdb_to_add) ]))
        
# ----------------------------------------------------------------------
def compare_tables(model, mmcif_ermrest_model):
    
    pdb_sdocs = mmcif_ermrest_model.ermrest_domain_schema
    mmcif_tnames = set(pdb_sdocs["tables"].keys())
    print("\nmmcif_tnames[%d]: %s" % (len(mmcif_tnames),  sorted(mmcif_tnames)))

    pdb_schema = model.schemas["PDB"]
    pdb_tnames = set(pdb_schema.tables.keys())
    print("\nermrest_tnames[%d]: %s" % (len(pdb_tnames), sorted(pdb_tnames)))

    intersection = mmcif_tnames & pdb_tnames
    mmcif_only = mmcif_tnames - pdb_tnames
    pdb_only = pdb_tnames - mmcif_tnames
    
    print("\nmmcif_tnames & ermrest_tnames [%d]: %s" % (len(intersection), sorted(intersection)))
    print("\nmmcif_tnames only [%d]: %s" % (len(mmcif_only), sorted(mmcif_only)))
    print("\nermrest_tnames only [%d]: %s" % (len(pdb_only), sorted(pdb_only)))
    

# ==================================================================

def main(args):
    credentials = get_credential(args.host, args.credential_file)    
    catalog = ErmrestCatalog("https", args.host, args.catalog_id, credentials)
    catalog.dcctx['cid'] = "model"
    store = HatracStore("https", args.host, credentials)
    model = catalog.getCatalogModel()

    mmcif_ermrest_model = mmCIFErmrestModel(args.model_docs, "PDB", "Vocab")
    pdb_sdocs = mmcif_ermrest_model.ermrest_domain_schema
    vocab_sdocs = mmcif_ermrest_model.ermrest_vocab_schema
    dump_json_to_file("/tmp/pdb_schema.json", pdb_sdocs)

    compare_models(model, mmcif_ermrest_model)
    #compare_tables(model, mmcif_ermrest_model)
                                        

'''
# Comparing the table listed in mmcif json schema docs with w hat's in deriva catalog
#
python -m pdb_dev.tools.compare_mmcif_schema  --host data-dev.pdb-ihm.org --catalog-id 99 --model-docs config-scripts/model-changes/initial/ma-min-db-schema.json

'''
if __name__ == "__main__":
    cli = PDBDEV_CLI("pdbdev", None, 1)    
    cli.parser.add_argument('--model-docs', help="json schema docs representing mmCIF dict", default="/tmp/json-full-db-ihm_dev_full-col-ihm_dev_full.json")
    args = cli.parse_cli()
    
    main(args)

