import json
from deriva.core import ErmrestCatalog, AttrDict, get_credential, DEFAULT_CREDENTIAL_FILE, tag, urlquote, DerivaServer, get_credential, BaseCLI
from deriva.core.ermrest_model import builtin_types, Schema, Table, Column, Key, ForeignKey
from deriva.core import urlquote, urlunquote
import requests.exceptions
#from ...utils.shared import DCCTX, PDBDEV_CLI
from pdb_dev.utils.shared import DCCTX, PDBDEV_CLI, cfg
from deriva.utils.extras.model import print_catalog_model_extras, print_schema_model_extras, print_table_model_extras, get_schemas, get_tables, get_columns, check_model_acl_types, tag2name, clear_all_schema_annotations

# -- =================================================================================
# -- citation related annotations
# -- =================================================================================

# --------------------------------------------------------------------------------------    
def update_PDB(model):
    schema = model.schemas["PDB"]
    pass
                                                                                        
# -- ==========================================================================
def print_citation_annotations(model):
    for schema in model.schemas.values():
        print("def update_%s(model):" % (schema.name))
        for table in schema.tables.values():
            for cname in table.columns.elements:
                column = table.columns[cname]
                if column.citation:
                    print('    # ----------------------------')
                    print('    model.schemas["%s"].tables["%s"].columns["%s"].asset.update(' % (schema.name, table.name, column.name))
                    print('%s' % (json.dumps(column.asset, indent=4)))
                    print(')\n')
        print()
    

# -- =================================================================================    
def update_citation_annotations(model):
    
    update_PDB(model)

# -- ---------------------------------------------
def clear_citation_annotations(model):
    clear_all_schema_annotations(model, [tag["citation"]])
    
# -- =================================================================================    
def main(server_name, catalog_id, credentials, args):
    server = DerivaServer('https', server_name, credentials)
    catalog = server.connect_ermrest(catalog_id)
    catalog.dcctx['cid'] = DCCTX["annotation"]
    model = catalog.getCatalogModel()

    if args.pre_print:
        print_citation_annotations(model)
        #print_schema_annotations(model, schema_name)
    
    clear_citation_annotations(model)
    update_citation_annotations(model)
    
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
