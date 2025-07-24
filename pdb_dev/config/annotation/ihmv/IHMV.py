from deriva.core import ErmrestCatalog, AttrDict, get_credential, DEFAULT_CREDENTIAL_FILE, tag, urlquote, DerivaServer, get_credential, BaseCLI
from deriva.core.ermrest_model import builtin_types, Schema, Table, Column, Key, ForeignKey
from deriva.core import urlquote, urlunquote
import requests.exceptions
from ....utils.shared import DCCTX, PDBDEV_CLI
from deriva.utils.extras.model import print_schema_model_extras, print_table_model_extras, print_schema_annotations, per_schema_annotation_tags, clear_schema_annotations

# -- =================================================================================
# -- schema level annotation

def update_IHMV(model):
    schema = model.schemas["IHMV"]

    # ----------------------------
    """ # use catalog default
    schema.display.update({
        "name_style": {
            "title_case": False,
            "underline_space": True
        }
    })
    """

# -- =================================================================================        
# -- individual table updates
    
# -- =================================================================================    
def update_IHMV_annotations(model):
    update_IHMV(model)
    
    # -- list of specific tables

# -- =================================================================================    
def main(server_name, catalog_id, credentials, args):
    server = DerivaServer('https', server_name, credentials)
    catalog = server.connect_ermrest(catalog_id)
    catalog.dcctx['cid'] = DCCTX["annotation"]
    model = catalog.getCatalogModel()

    if args.pre_print:
        print_schema_annotations(model, "IHMV")
        
    clear_schema_annotations(model, "IHMV", per_schema_annotation_tags)
    update_Vocab_annotations(model)
    
    if args.post_print:
        print_schema_annotations(model, "IHMV")
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
