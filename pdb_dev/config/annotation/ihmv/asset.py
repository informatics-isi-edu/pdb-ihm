import json
from deriva.core import ErmrestCatalog, AttrDict, get_credential, DEFAULT_CREDENTIAL_FILE, tag, urlquote, DerivaServer, get_credential, BaseCLI
from deriva.core.ermrest_model import builtin_types, Schema, Table, Column, Key, ForeignKey
from deriva.core import urlquote, urlunquote
import requests.exceptions
from ....utils.shared import DCCTX, PDBDEV_CLI, cfg
#from pdb_dev.utils.shared import DCCTX, PDBDEV_CLI, cfg
from deriva.utils.extras.model import print_catalog_model_extras, print_schema_model_extras, print_table_model_extras, get_schemas, get_tables, get_columns, check_model_acl_types, tag2name, clear_all_schema_annotations

# -- =================================================================================
# -- asset related annotations
# -- =================================================================================

# --------------------------------------------------------------------------------------    
def update_IHMV(model):
    schema = model.schemas["IHMV"]
    
    # ----------------------------
    schema.tables["Structure_mmCIF"].columns["File_URL"].asset.update({
        "md5": "File_MD5",
        "url_pattern": "%s/ihmv/submitted/uid/{{#if _RCB}}{{#regexFindFirst _RCB \"[^/]+$\"}}{{this}}{{/regexFindFirst}}{{else}}{{#regexFindFirst $session.client.id \"[^/]+$\"}}{{this}}{{/regexFindFirst}}{{/if}}/structure/mmCIF/{{{File_MD5}}}{{{_File_URL.filename_ext}}}" % (cfg.hatrac_root),
        "filename_column": "File_Name",
        "byte_count_column": "File_Bytes"
    })
    
    # ----------------------------
    schema.tables["Generated_File"].columns["File_URL"].asset.update({
        "md5": "File_MD5",
        "url_pattern": "%s/pdb/generated/uid/{{#if _Entry_RCB}}{{#regexFindFirst _Entry_RCB \"[^/]+$\"}}{{this}}{{/regexFindFirst}}{{else}}{{#regexFindFirst $session.client.id \"[^/]+$\"}}{{this}}{{/regexFindFirst}}{{/if}}/structure/rid/{{{Structure_mmCIF}}}/validation_report/{{{File_Name}}}" % (cfg.hatrac_root),
        "filename_column": "File_Name",
        "byte_count_column": "File_Bytes"
    })


# -- =================================================================================    
def update_asset_annotations(model):
    
    update_IHMV(model)

# -- ---------------------------------------------
def clear_asset_annotations(model):
    clear_all_schema_annotations(model, [tag["asset"]])
    
# -- =================================================================================    
def main(server_name, catalog_id, credentials, args):
    server = DerivaServer('https', server_name, credentials)
    catalog = server.connect_ermrest(catalog_id)
    catalog.dcctx['cid'] = DCCTX["annotation"]
    model = catalog.getCatalogModel()

    if args.pre_print:
        print_asset_annotations(model)
        #print_schema_annotations(model, schema_name)
    
    clear_asset_annotations(model)
    update_asset_annotations(model)
    
    if args.post_print:
        print_schema_annotations(model, schema_name)
    if not args.dry_run:
        model.apply()
        pass


# -- =================================================================================

if __name__ == '__main__':
    cli = PDBDEV_CLI("PDB-IHM", None, 1)
    cli.parser.add_argument('--schema', metavar='<schema>', help="print catalog acl script without applying", default=False)
    cli.parser.add_argument('--table', metavar='<table>', help="print catalog acl script without applying", default=False)
    args = cli.parse_cli()
    credentials = get_credential(args.host, args.credential_file)
    print(credentials)

    if args.debug:
        init_logging(level=logging.DEBUG)
    
    main(args.host, args.catalog_id, credentials, args)
