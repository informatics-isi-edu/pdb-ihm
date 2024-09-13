from deriva.core import ErmrestCatalog, AttrDict, get_credential, DEFAULT_CREDENTIAL_FILE, tag, urlquote, DerivaServer, get_credential, BaseCLI
from deriva.core.ermrest_model import builtin_types, Schema, Table, Column, Key, ForeignKey
from deriva.core import urlquote, urlunquote
import requests.exceptions
from ...utils.shared import DCCTX, PDBDEV_CLI
from ...utils.model import print_catalog_model_extras, print_schema_model_extras, print_table_model_extras, get_schemas, get_tables, get_columns, check_model_acl_types

# -- =================================================================================
# -- asset related annotations
# -- =================================================================================


def update_PDB_entry(model):
    schema = model.schemas["PDB"]
    table = schema.tables["entry"]    

    # ----------------------------
    '''
    model.schemas["PDB"].tables["entry"].columns["File_URL"].asset.update({
        "md5": "Original_Schematic_MD5",
        "url_pattern": "/hatrac/resources/schematics/original/{{$moment.year}}/{{{Original_Schematic_MD5}}}{{#if _Original_Schematic_URL.filename_ext}}{{{_Original_Schematic_URL.filename_ext}}}{{/if}}",
        "filename_column": "Original_Schematic_Name",
        "byte_count_column": "Original_Schematic_Bytes"
    })
    '''
    

# -- ==========================================================================
def print_asset_annotations(model):
    for schema in model.schemas.values():
        print("def update_%s(model):" % (schema.name))
        for table in schema.tables.values():
            for cname in table.columns.elements:
                column = table.columns[cname]
                if column.asset:
                    print('    # ----------------------------')
                    print('    model.schemas["%s"].tables["%s"].columns[%s].asset.update(' % (schema.name, table.name, column.name))
                    print('%s' % (json.dumps([column.asset], indent=4)))
                    print(')\n')
        print()
    
# -- ---------------------------------------------------------------------------------
def update_PDB_System_Generated_File(model):
    schema = model.schemas["pDB"]
    table = schema.tables["System_Generated_File"]


# -- =================================================================================    
def update_asset_annotations(model):
    update_PDB_entry(model)
    # -- list of specific tables

    
# -- =================================================================================    
def main(server_name, catalog_id, credentials, args):
    server = DerivaServer('https', server_name, credentials)
    catalog = server.connect_ermrest(catalog_id)
    catalog.dcctx['cid'] = DCCTX["annotation"]
    model = catalog.getCatalogModel()

    if args.pre_print:
        print_schema_annotations(model, schema_name)
    #clear_schema_annotations(model, schema_name, per_schema_annotation_tags)
    update_asset_annotations(model)
    if args.post_print:
        print_schema_annotations(model, schema_name)
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
