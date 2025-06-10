from deriva.core import ErmrestCatalog, HatracStore, AttrDict, get_credential, DEFAULT_CREDENTIAL_FILE, tag, urlquote, DerivaServer, get_credential, BaseCLI
from deriva.core.ermrest_model import builtin_types, Schema, Table, Column, Key, ForeignKey, tag, AttrDict
from deriva.core import urlquote, urlunquote, DEFAULT_SESSION_CONFIG
from deriva.core.utils.hash_utils import compute_hashes

from ..utils.shared import PDBDEV_CLI, DCCTX, cfg
#from pdb_dev.utils.shared import PDBDEV_CLI, DCCTX, cfg
from deriva.utils.extras.data import get_ermrest_query, insert_if_not_exist, update_table_rows, delete_table_rows
from deriva.utils.extras.pdb_ma.mmcif_model import mmCIFErmrestModel, dump_json_to_file


def main(args):
    credentials = get_credential(args.host, args.credential_file)    
    catalog = ErmrestCatalog("https", args.host, args.catalog_id, credentials)
    catalog.dcctx['cid'] = "model"
    store = HatracStore("https", args.host, credentials)
    model = catalog.getCatalogModel()


    mmcif_ermrest_model = mmCIFErmrestModel(args.model_docs, "MA", "Vocab")
    pdb_sdocs = mmcif_ermrest_model.ermrest_domain_schema
    vocab_sdocs = mmcif_ermrest_model.ermrest_vocab_schema
    dump_json_to_file("/tmp/pdb_schema.json", pdb_sdocs)
    
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

