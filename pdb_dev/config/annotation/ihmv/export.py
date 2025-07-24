import json
from deriva.core import ErmrestCatalog, AttrDict, get_credential, DEFAULT_CREDENTIAL_FILE, tag, urlquote, DerivaServer, get_credential, BaseCLI
from deriva.core.ermrest_model import builtin_types, Schema, Table, Column, Key, ForeignKey
from deriva.core import urlquote, urlunquote
import requests.exceptions
from ....utils.shared import DCCTX, PDBDEV_CLI
from deriva.utils.extras.model import print_catalog_model_extras, print_schema_model_extras, print_table_model_extras, get_schemas, get_tables, get_columns, check_model_acl_types, tag2name, clear_all_schema_annotations

export_annotation_tags = [tag["export"], tag["export_2019"], tag["export_fragment_definitions"]]

# -- =================================================================================
# -- asset related annotations
# chaise docs: https://github.com/informatics-isi-edu/ermrestjs/blob/master/docs/user-docs/export.md
# export docs: 
# -- =================================================================================

"""
Note: For the entry csv, setting path to none break chaise, while setting path to empty string break ermrest syntax
"""
def update_IHMV_Structure_mmCIF(model):
    schema = model.schemas["IHMV"]
    table = schema.tables["Structure_mmCIF"]    

    table.export_2019.update({
	"compact" : {
	    "templates" : [
		{
		    "displayname":"BDBag",
		    "type":"BAG",
		    "outputs": [
			{
			    "source": {
				"api": "entity",
			    },
			    "destination": {
				"name": "Structure_mmCIF",
				"type": "csv"
			    }
			},
			{
			    "source": {
				"api": "entity",
				"path": "IHMV:Generated_File",
			    },
			    "destination": {
				"name": "Generated_File",
				"type": "csv"
			    }
			},
			{
			    "source": {
				"api": "attribute",
				"path": "IHMV:Generated_File/url:=File_URL"
			    },
			    "destination": {
				"name": "Generated_Files",
				"type": "download"
			    }
			}
		    ],
		}]
        },
    })


# -- ==========================================================================    

# -- =================================================================================    
def update_export_annotations(model):
    
    update_IHMV_Structure_mmCIF(model)
    # -- list of specific tables

# -------------------------------------------
def clear_export_annotations(model):
    clear_all_schema_annotations(model, export_annotation_tags)    
    
# -- =================================================================================    
def main(server_name, catalog_id, credentials, args):
    server = DerivaServer('https', server_name, credentials)
    catalog = server.connect_ermrest(catalog_id)
    catalog.dcctx['cid'] = DCCTX["annotation"]
    model = catalog.getCatalogModel()
    
    if args.pre_print:
        print_export_annotations(model)
    clear_export_annotations(model)
    update_export_annotations(model)
    if args.post_print:
        print_export_annotations(model)
    if not args.dry_run:
        model.apply()
        pass


# -- =================================================================================

if __name__ == '__main__':
    cli = PDBDEV_CLI("PDB_Dev", None, 1)
    cli.parser.add_argument('--schema', metavar='<schema>', help="print catalog acl script without applying", default=False)
    cli.parser.add_argument('--table', metavar='<table>', help="print catalog acl script without applying", default=False)
    args = cli.parse_cli()
    credentials = get_credential(args.host, args.credential_file)
    print("host name: %s, credential: %s" % (args.host, credentials))

    if args.debug:
        init_logging(level=logging.DEBUG)
    
    main(args.host, args.catalog_id, credentials, args)
