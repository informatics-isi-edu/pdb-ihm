import json
from deriva.core import ErmrestCatalog, AttrDict, get_credential, DEFAULT_CREDENTIAL_FILE, tag, urlquote, DerivaServer, get_credential, BaseCLI
from deriva.core.ermrest_model import builtin_types, Schema, Table, Column, Key, ForeignKey
from deriva.core import urlquote, urlunquote
import requests.exceptions
from ...utils.shared import DCCTX, PDBDEV_CLI
from deriva.utils.extras.model import print_catalog_model_extras, print_schema_model_extras, print_table_model_extras, get_schemas, get_tables, get_columns, check_model_acl_types, tag2name, clear_all_schema_annotations

export_annotation_tags = [tag["export"], tag["export_2019"], tag["export_fragment_definitions"]]

# -- =================================================================================
# -- asset related annotations
# -- =================================================================================


def update_PDB_entry(model):
    schema = model.schemas["PDB"]
    table = schema.tables["entry"]    

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
				"table": "PDB:entry"
			    },
			    "destination": {
				"name": "entry",
				"type": "csv"
			    }
			},
			{
			    "source": {
				"api": "Entry_Generated_File",
				"table": "PDB:entry"
			    },
			    "destination": {
				"name": "entry",
				"type": "csv"
			    }
			},
			{
			    "source": {
				"api": "attribute",
				"table": "PDB:entry",                              
                                "path": "id,url:=Image_File_URL,length:=Image_File_Bytes,filename:=Image_File_Name,md5:=Image_File_MD5"
			    },
			    "destination": {
				"name": "Images",
				"type": "download",
                                #"params:" {
                                #    "output_path": "Related_Files",
                                #    "output_filename": "{File_Name}"
                                #}
			    }
			},
			{
			    "source": {
				"api": "attribute",
				"path": "PDB:Entry_Generated_File/url:=File_URL"
			    },
			    "destination": {
				"name": "Entry_Generated_Files",
				"type": "download"
			    }
			}
		    ],
		}]
        },
    })


# -- ==========================================================================    
def print_export_annotations(model):
    for schema in model.schemas.values():
        print("def update_%s(model):" % (schema.name))
        for table in schema.tables.values():
            for key, annotation in table.annotations.items():
                if key not in export_annotation_tags: continue
                print('    model.schemas["%s"].tables["%s"].%s.update(' % (schema.name, table.name, tag2name[key]))
                print('%s' % (json.dumps(annotation, indent=4)))
                print(')\n')
        print()

# -- ---------------------------------------------------------------------------------


# -- =================================================================================    
def update_export_annotations(model):
    update_PDB_entry(model)
    # -- list of specific tables

    
# -- =================================================================================    
def main(server_name, catalog_id, credentials, args):
    server = DerivaServer('https', server_name, credentials)
    catalog = server.connect_ermrest(catalog_id)
    catalog.dcctx['cid'] = DCCTX["annotation"]
    model = catalog.getCatalogModel()
    
    if args.pre_print:
        print_export_annotations(model)
    clear_all_schema_annotations(model, export_annotation_tags)
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
