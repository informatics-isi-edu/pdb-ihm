import sys
import json
from deriva.core import ErmrestCatalog, AttrDict, get_credential, DEFAULT_CREDENTIAL_FILE, tag, urlquote, DerivaServer, get_credential, BaseCLI
from deriva.core.ermrest_model import builtin_types, Schema, Table, Column, Key, ForeignKey, tag, AttrDict
from deriva.core import urlquote, urlunquote
import requests.exceptions
from ....utils.shared import DCCTX, PDBDEV_CLI, cfg
from deriva.utils.extras.model import get_schemas, get_tables, get_columns, print_catalog_model_extras, print_presence_tag_annotations, clear_catalog_annotations, tag2name
#from . import bulk_upload
from ...acl.ermrest_acl import GROUPS, initialize_policies

catalog_wide_annotation_tags = [tag["generated"], tag["immutable"], tag["non_deletable"], tag["required"]]
catalog_specific_annotation_tags = [tag["chaise_config"], tag["bulk_upload"], tag["column_defaults"], tag["display"]]

# -- =================================================================================
# -- chaise config.. Assuming that navbar is set through chaise-config
# chaise-config params: https://github.com/informatics-isi-edu/chaise/blob/master/docs/user-docs/chaise-config.md#internalhosts
def get_chaise_config(catalog_id):
    config = {
        "defaultCatalog": catalog_id,
        "resolverImplicitCatalog": catalog_id,        
        "customCSS": '/assets/css/chaise.css',
        "allowErrorDismissal": True,
        "confirmDelete": True,
	"deleteRecord": True,
	"editRecord": True,
        "maxRecordsetRowHeight": 235,
        #"footerMarkdown": "[* Privacy policy](/privacy-policy){target='_blank'}",
        "exportServicePath": "/deriva/export",
        "SystemColumnsDisplayCompact": ["RID", "RCB", "RCT"],
        "SystemColumnsDisplayDetailed": ["RID", "RCB", "RCT", "RMT"],
        "SystemColumnsDisplayEntry": [],
        "dataBrowser": "/ihmv/",
        "navbarBrand": "/ihmv/",
        "headTitle": "IHMV",
        "navbarBrandText": "IHMV",
	"signUpURL": "https://app.globus.org/groups/99da042e-64a6-11ea-ad5f-0ef992ed7ca1/about",
        #"disableExternalLinkModal": True, # check this?
	#"internaleHosts": ["github.com"],
        "templating": {
            "engine": "handlebars",
            "site_var": {
                "acl_groups": {
                    "entry_submitters": ["https://auth.globus.org/99da042e-64a6-11ea-ad5f-0ef992ed7ca1"],
                    "entry_updaters": ["https://auth.globus.org/eef3e02a-3c40-11e9-9276-0edc9bdd56a6", "https://auth.globus.org/0b98092c-3c41-11e9-a8c8-0ee7d80087ee", "https://auth.globus.org/3938e0d0-ed35-11e5-8641-22000ab4b42b"], # pdb-curators, pdb-admins, isrd-systems
                }  
            },
        }
    }
    
    config.update(get_navbar_menu(catalog_id))        

    if cfg.is_dev == True:
        config["navbarBrandText"] = "%s (Dev)" % (config["navbarBrandText"])
    elif cfg.is_staging == True:
        config["navbarBrandText"] = "%s (Test)" % (config["navbarBrandText"])

    #print("%s\n" % (json.dumps(config, indent=2)))    
    return config

# -- ----------------------------------------------------------------------    
def get_navbar_menu(catalog_id):
    navbar = {
        "navbarMenu": {
            "newTab": False,
            "children": [
	        {
	            "name": "Structure",
	            "url": "/chaise/recordset/#"+catalog_id+"/IHMV:Structure_mmCIF"
	        },
	        {
	            "name": "Validation Reports",
	            "url": "/chaise/recordset/#"+catalog_id+"/IHMV:Generated_File"
	        },
            #    {
            #        "name": "Vocabulary",
            #        "acls": { "show": GROUPS["owners"] + GROUPS["entry-updaters"], "enable": GROUPS["owners"] + GROUPS["entry-updaters"] },
            #        "children": [
            #            {
            #                "name": "To be added",
            #                "url": "/chaise/recordset/#"+catalog_id+"/Vocab:entity_poly_seq_hetero"
            #            },
            #        ]
            #    },
                {
                    "name": "Documentation",
                    "children": [
                        { "name": "Validation System", "url": "https://docs.google.com/document/d/1SEFMWU4SDkOSg3Hk1ebFxy8BrPt7v-MlogS3gFDb6K8" },
                        { "name": "Validation Reports", "url": "https://pdb-ihm.org/validation_help.html" },
                    ],
                }
            ],
        }
    }

    return navbar

# -- ----------------------------------------------------------------------
# TODO: check this annotation. I (HT) am not aware of this annotations. 
def update_catalog_config(model):
    pass

# -- ===============================================================================================
# -- catalog level annotation

def update_catalog_display(model):
    model.display.update({
        "name_style" : {
            "title_case" : True,
            "underline_space" : True
        },
        "show_foreign_key_link" : {
	    "compact" : False,
	    "detailed" : True
	},
        "show_key_link" : {
	    "compact" : False,
	    "detailed" : True
	},        
    })

# -- ----------------------------------------------------------------------    
def update_catalog_column_defaults(model):
    # column-defaults
    #["tag:isrd.isi.edu,2023:column-defaults"]
    model.column_defaults.update({
        "by_type": {
            "boolean": {
                tag["column_display"]: {
                    "*": {
                        "pre_format": {
                            "format": "%t",
                            "bool_true_value": "Yes",
                            "bool_false_value": "No"
                        }
                    }
                },
            },
        },
        # NOTE: non_deletable doesn't apply to column level
        "by_name": {
            "RID": {
                "tag:misd.isi.edu,2015:display" : {
                    "comment": "Record ID",
                },
                #"tag:isrd.isi.edu,2016:generated": True,
                #"tag:isrd.isi.edu,2016:immutable": True,
                #"tag:isrd.isi.edu,2016:non-deletable": True, # NOT COLUMN LEVEL
            },
            "RCB": {
                "tag:misd.isi.edu,2015:display": {
                    "name": "RCB",
                    "comment": "Created by",
                },
            },
            "RMB": {
                "tag:misd.isi.edu,2015:display": {
                    "name": "RMB",
                    "comment": "Modified by"                    
                },
            },            
            "RCT": {
                "tag:misd.isi.edu,2015:display": {
                    "name": "Creation Time",
                },
                "tag:isrd.isi.edu,2016:column-display": {
                    "*" : {
		        "pre_format" : {
                            "format" : "YYYY-MM-DD HH:mm"
		        }
                    }
	        },
            },
            "RMT": {
                "tag:misd.isi.edu,2015:display": {
                    "name": "Last Modified Time",
                },
                "tag:isrd.isi.edu,2016:column-display": {
                    "*" : {
		        "pre_format" : {
                            "format" : "YYYY-MM-DD HH:mm"
		        }
                    }
	        },
            },
            "Processing_Detail": {
                "tag:isrd.isi.edu,2016:generated": True,
                "tag:isrd.isi.edu,2016:immutable": True,
                #"tag:misd.isi.edu,2015:display" : {
                #    "comment": "Record status detail is listed"
                #},
            },
            "File_Bytes": {
                "tag:misd.isi.edu,2015:display" : {
                    "name": "File Size"                    
                },
            },
        },
    })
            
    
# -- ===============================================================================================
# presence tag annotations: generated, immutable, non-deletable, required
# 
# -- ----------------------------------------------------------------------
# identify generated schemas/tables/columns and mark them as generated, immutable, and non-deletables
def update_generated_elements(model):
        
    generated_tables = set()
    # consider tables: Accession_Code, Entry_Latest_Archive  --> TODO: Brinda to consider
    generated_tables.update(get_tables(model, schema_names=["IHMV"], table_names=[]))
    for table in generated_tables:
        table.annotations[tag["generated"]] = True
        #table.annotations[tag["immutable"]] = True  
        table.annotations[tag["non_deletable"]] = True        

    generated_columns = set()
    #generated_columns.update(get_columns(model, schema_pattern=".*", table_pattern=".*", column_pattern="Accession_Code"))
    #generated_columns.update(get_columns(model, schema_names=["PDB"], table_names=["entry"], column_names=["Accession_Code"]))
    for column in generated_columns:
        column.annotations[tag["generated"]] = True
        column.annotations[tag["immutable"]] = True
        # column.non_deletable = True # -- not at column level

# -- ----------------------------------------------------------------------
def update_required_annotations(model):
    #if not schemas_not_in_model: set_elements_not_in_model(model)    
    required = set()
    
    #required.update(get_columns(model, schema_names=["PDB"], table_names=["Data_Dictionary"], column_names=["Name", "Category", "Version", "Location"])) # already in model
    
    for column in required:
        if column in columns_not_in_model: continue
        column.annotations[tag["required"]] = True
    
    
# -- =================================================================================                    

# -- update annotations across multiple schemas
def update_catalog_wide_annotations(model):
    #if not schemas_not_in_model: set_elements_not_in_model(model)
    
    # -- catalog-wide annotations
    update_generated_elements(model)
    update_required_annotations(model)

# -- ---------------------------------------------------------------------------------
# catalog annotation
def update_catalog_annotations(model):
    initialize_policies(model.catalog)
    
    chaise_config = get_chaise_config(model.catalog.catalog_id)
    model.annotations[tag["chaise_config"]] = chaise_config
    #bulk_upload.update_bulk_upload_annotations(model)
    update_catalog_display(model)
    update_catalog_column_defaults(model)
    
# -- ---------------------------------------------------------------------------------
# catalog annotation
def clear_catalog_catalog_wide_annotations(model):
    model.annotations.clear()
    clear_catalog_annotations(model, catalog_specific_annotation_tags, recursive=False)                                    
    clear_catalog_annotations(model, catalog_wide_annotation_tags)

# -- =================================================================================

# -- =================================================================================
        
def main(server_name, catalog_id, credentials, args):
    server = DerivaServer('https', server_name, credentials)
    catalog = server.connect_ermrest(catalog_id)
    catalog.dcctx['cid'] = DCCTX["annotation"]        
    model = catalog.getCatalogModel()
    
    if args.pre_print:
        #print_isolated_tables(model)
        print("def catalog_annotations(model):");
        print("    model.annotations = %s" % (json.dumps(model.annotations, indent=4)))
        print_presence_tag_annotations(model, [tag["generated"], tag["immutable"], tag["non_deletable"]])
        print_presence_tag_annotations(model, [tag["required"]])

    clear_catalog_catalog_wide_annotations(model)
    update_catalog_annotations(model)
    update_catalog_wide_annotations(model)
    
    if args.post_print:
        print("def catalog_annotations(model):");
        print("    model.annotations = %s" % (json.dumps(model.annotations, indent=4)))
        print_presence_tag_annotations(model, [tag["generated"], tag["immutable"], tag["non_deletable"]])
        print_presence_tag_annotations(model, [tag["required"]])
        
    if not args.dry_run:
        model.apply()
        pass
    
# -- =================================================================================

if __name__ == '__main__':
    args = PDBDEV_CLI("PDB_Dev", None, 1).parse_cli()
    credentials = get_credential(args.host, args.credential_file)
    print(credentials)
    main(args.host, args.catalog_id, credentials, args)
