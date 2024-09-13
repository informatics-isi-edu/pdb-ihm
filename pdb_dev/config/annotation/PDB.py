from deriva.core import ErmrestCatalog, AttrDict, get_credential, DEFAULT_CREDENTIAL_FILE, tag, urlquote, DerivaServer, get_credential, BaseCLI
from deriva.core.ermrest_model import builtin_types, Schema, Table, Column, Key, ForeignKey
from deriva.core import urlquote, urlunquote
import requests.exceptions
from ...utils.shared import DCCTX, PDBDEV_CLI
from deriva.utils.extras.model import print_catalog_model_extras, print_schema_model_extras, print_table_model_extras, get_schemas, get_tables, get_columns, check_model_acl_types

# -- =================================================================================
# -- schema level annotation
# TODO: In progress. Still need to be tested
def update_PDB(model):
    schema = model.schemas["PDB"]
    print("update_PDB")

    for tname, table in schema.tables.items():
        for fkey in table.foreign_keys:
            from_cols = {c.name for c in fkey.column_map.keys()}
            to_cols = {c.name for c in fkey.column_map.values()}
            if len(from_cols) > 1 and "structure_id" in from_cols:
                fkey.foreign_key.update({
                    "domain_filter_pattern": "%s/structure_id={{{structure_id}}}"
                })
        
    # -- make sure all fkeys containing structure_id are updated with domain_filter_pattern
    '''
    schema.tables["Experiment"].foreign_keys[(schema,"Experiment_Growth_Protocol_Reference_fkey")].foreign_key.update({
        "from_name": "Experiment Growth Protocol",
        "domain_filter_pattern": "Category=any({{#encode 'Growth protocol'}}{{/encode}},{{#encode 'Overall sequencing'}}{{/encode}})"        
    })
    '''

    
# -- ---------------------------------------------------------------------------------
def update_PDB_entry(model):
    schema = model.schemas["PDB"]
    table = schema.tables["entry"]


# -- =================================================================================    
def update_PDB_annotations(model):
    update_PDB(model)
    # -- list of specific tables

    
# -- =================================================================================    
def main(server_name, catalog_id, credentials, args):
    server = DerivaServer('https', server_name, credentials)
    catalog = server.connect_ermrest(catalog_id)
    catalog.dcctx['cid'] = DCCTX["annotation"]
    model = catalog.getCatalogModel()
    '''
    if args.pre_print:
        print_schema_annotations(model, schema_name)
    '''
    #clear_schema_annotations(model, schema_name, per_schema_annotation_tags)
    update_PDB_annotations(model)

    '''
    if args.post_print:
        print_schema_annotations(model, schema_name)
    '''
    if not args.dry_run:
        #model.apply()
        pass


# -- =================================================================================

if __name__ == '__main__':
    cli = AtlasD2KCLI("ATLAS-D2K", None, 1)
    cli.parser.add_argument('--schema', metavar='<schema>', help="print catalog acl script without applying", default=False)
    cli.parser.add_argument('--table', metavar='<table>', help="print catalog acl script without applying", default=False)
    args = cli.parse_cli()
    credentials = get_credential(args.host, args.credential_file)
    print(credentials)

    if args.debug:
        init_logging(level=logging.DEBUG)
    
    main(args.host, args.catalog_id, credentials, args)
