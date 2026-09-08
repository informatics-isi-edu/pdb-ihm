import json
from deriva.core import ErmrestCatalog, AttrDict, get_credential, DEFAULT_CREDENTIAL_FILE, tag, urlquote, DerivaServer, get_credential, BaseCLI
from deriva.core.ermrest_model import builtin_types, Schema, Table, Column, Key, ForeignKey
from deriva.core import urlquote, urlunquote
import requests.exceptions
from ....utils.shared import DCCTX, PDBDEV_CLI
from deriva.utils.extras.model import check_model_acl_types, tag2name, clear_all_schema_annotations

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
	"*" : {
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
    
    update_IHMV_Structure_mmCIF(model)


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
    args = cli.parse_cli()
    credentials = get_credential(args.host, args.credential_file)
    print("host name: %s, credential: %s" % (args.host, credentials))

    main(args.host, args.catalog_id, credentials, args)
