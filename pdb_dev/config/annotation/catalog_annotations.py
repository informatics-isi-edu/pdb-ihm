import sys
import json
from deriva.core import ErmrestCatalog, AttrDict, get_credential, DEFAULT_CREDENTIAL_FILE, tag, urlquote, DerivaServer, get_credential, BaseCLI
from deriva.core.ermrest_model import builtin_types, Schema, Table, Column, Key, ForeignKey, tag, AttrDict
from deriva.core import urlquote, urlunquote
import requests.exceptions
from ...utils.shared import DCCTX, PDBDEV_CLI, cfg
from deriva.utils.extras.model import get_schemas, get_tables, get_columns, print_catalog_model_extras, print_presence_tag_annotations
#from . import bulk_upload
#from ..acl.ermrest_acl import schemas_not_in_model, tables_not_in_model, columns_not_in_model, set_elements_not_in_model

catalog_wide_annotation_tags = [tag["generated"], tag["immutable"], tag["non_deletable"], tag["required"]]

# -- =================================================================================
# -- chaise config.. Assuming that navbar is set through chaise-config
def get_chaise_config(catalog_id):
    config = {
        "defaultCatalog": catalog_id,
        "customCSS": '/assets/css/chaise.css',
        "allowErrorDismissal": True,
        "confirmDelete": True,
        "maxRecordsetRowHeight": 235,
        #"footerMarkdown": "[* Privacy policy](/privacy-policy){target='_blank'}",
        "resolverImplicitCatalog": 2,
        "exportServicePath": "/deriva/export",
        "templating": {"engine": "handlebars"},
        "SystemColumnsDisplayCompact": ["RID"],
        "SystemColumnsDisplayDetailed": ["RID", "RCT", "RMT"],
        "SystemColumnsDisplayEntry": [],
        #"internalHosts": ["dev.gudmap.org", "dev.rebuildingakidney.org", "staging.gudmap.org", "staging.rebuildingakidney.org", "www.gudmap.org", "www.rebuildingakidney.org", "deriva-imaging.isi.edu", "isrd.wufoo.com", "dev.atlas-d2k.org", "www.atlas-d2k.org"],
        "headTitle": "PDB-Dev",
        "navbarBrand": "/",
        "navbarBrandText": "PDB-Dev",
    }

    if cfg.is_dev == True:
        config["navbarBrandText"] = "%s (Dev)" % (config["navbarBrandText"])
    elif cfg.is_staging == True:
        config["navbarBrandText"] = "%s (Test)" % (config["navbarBrandText"])
        
    print("%s\n" % (json.dumps(config, indent=2)))    
    return config

# -- ===============================================================================================
# -- catalog level annotation

def update_catalog_display(model):
    model.display.update({
        "name_style" : {
            "title_case" : False,
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
                "tag:isrd.isi.edu,2016:generated": True,
                "tag:isrd.isi.edu,2016:immutable": True,
                #"tag:isrd.isi.edu,2016:non-deletable": True, # NOT COLUMN LEVEL
            },
            "RCT": {
                "tag:misd.isi.edu,2015:display": {
                    "name": "Creation Time",
                },
                "tag:isrd.isi.edu,2016:generated": True,
                "tag:isrd.isi.edu,2016:immutable": True,
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
                "tag:isrd.isi.edu,2016:generated": True,
                "tag:isrd.isi.edu,2016:immutable": True,
                "tag:isrd.isi.edu,2016:column-display": {
                    "*" : {
		        "pre_format" : {
                            "format" : "YYYY-MM-DD HH:mm"
		        }
                    }
	        },
            },
            "Release_Date": {
                "tag:isrd.isi.edu,2016:generated": True,
                "tag:isrd.isi.edu,2016:immutable": True,
            },
            "Record_Status": {
                "tag:isrd.isi.edu,2016:generated": True,
                "tag:isrd.isi.edu,2016:immutable": True,
            },
            "Record_Status_Detail": {
                "tag:isrd.isi.edu,2016:generated": True,
                "tag:isrd.isi.edu,2016:immutable": True,
                "tag:misd.isi.edu,2015:display" : {
                    "comment": "If incomplete, the required detail is listed"
                },
                "tag:isrd.isi.edu,2016:column-display": {
                    "*" : {
                        # assuming that Record_Status_fkey is in source definition
                        "template_engine": "handlebars",
                        "markdown_pattern": "[{{{Record_Status}}}]({{{record_status_fkey.uri.detailed}}}){ {{{record_status_fkey.values.CSS_Class}}} }{{#if Record_Status_Detail}} : {{{Record_Status_Detail}}}{{/if}} "
                    }
	        },
            },
            "Accession_ID": {
                "tag:isrd.isi.edu,2016:generated": True,
                "tag:isrd.isi.edu,2016:immutable": True,
            },
            # in Common:Collection, Common:Instructional_Video
            "Persistent_ID": {
                "tag:isrd.isi.edu,2016:generated": True,
                "tag:isrd.isi.edu,2016:immutable": True,
                "tag:isrd.isi.edu,2016:column-display": {
                    "*" : {
                        "template_engine": "handlebars",    
                        "markdown_pattern": "[{{{Persistent_ID}}}]({{{Persistent_ID}}})"
                    }
	        },
            },
            "Processing_Status": {
                "tag:isrd.isi.edu,2016:generated": True,
                "tag:isrd.isi.edu,2016:immutable": True,
            },
            "Processing_Status_Detail": {
                "tag:isrd.isi.edu,2016:generated": True,
                "tag:isrd.isi.edu,2016:immutable": True,
            },
            "NCBI_Symbol": {
                "tag:misd.isi.edu,2015:display" : {
                    "name": "Gene Symbol"                    
                },
                "tag:isrd.isi.edu,2016:generated": True,
                "tag:isrd.isi.edu,2016:immutable": True,
            },
            "NCBI_GeneID": {
                "tag:misd.isi.edu,2015:display" : {
                    "name": "Gene ID"                    
                },
                "tag:isrd.isi.edu,2016:column-display": {
                    "*" : {
                        "pre_format": { "format": "%u" }
                    }
                },
            },
            "File_Bytes": {
                "tag:misd.isi.edu,2015:display" : {
                    "name": "File Size"                    
                },
            },
            "Principal_Investigator": {
                "tag:isrd.isi.edu,2018:required": True,
            }, 
            "Consortium": {
                "tag:isrd.isi.edu,2018:required": True,
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
    generated_tables.update(get_tables(model, schema_names=["PDB"], table_names=["Accession_Code", "PDB_Archive", "Entry_Latest_Archive"]))
    generated_tables.update(get_tables(model, schema_names=["_acl_admin"], table_names=["group_lists"]))
    for table in generated_tables:
        table.annotations[tag["generated"]] = True
        table.annotations[tag["immutable"]] = True
        table.annotations[tag["non_deletable"]] = True        

        
    generated_columns = set()
    #generated_columns.update(get_columns(model, schema_pattern=".*", table_pattern=".*", column_pattern="Accession_Code"))
    generated_columns.update(get_columns(model, schema_names=["PDB"], table_names=["entry"], column_names=["Accession_Code"]))
    for column in generated_columns:
        column.annotations[tag["generated"]] = True
        column.annotations[tag["immutable"]] = True
        # column.non_deletable = True # -- not at column level

# -- ----------------------------------------------------------------------
def update_required_annotations(model):
    if not schemas_not_in_model: set_elements_not_in_model(model)    
    required = set()
    #required.update(get_columns(model, schema_names=["PDB"], table_names=["Experiment_Settings"], column_names=["Strandedness", "Used_Spike_Ins", "Paired_End"]))
    
    for column in required:
        if column in columns_not_in_model: continue
        column.annotations[tag["required"]] = True
    
    
# =================================================================================================
def print_generated_elements(model):
    set_elements_not_in_model(model)
    generated_dict = {}
    for schema in model.schemas.values():
        if schema.generated: 
            generated_dict.setdefault((schema.name, None), set())
        for table in schema.tables.values():
            if table.generated:
                generated_dict.setdefault((schema.name, table.name), set())
                for column in table.columns:
                    #if column.name in ["RID", "RCT", "RMT", "RCB", "RMB", "Curation_Status", "Record_Status", "Record_Status_Detail"]: continue
                    if column.name in ["RID", "RCT", "RMT", "RCB", "RMB"]: continue                    
                    if column.generated:
                        generated_dict.setdefault((schema.name, table.name), set()).add(column.name)

    print("# ---- generated elements ----")
    for key, cnames in generated_dict.items():
        sname, tname = key
        print("generated %s:%s: %s" % (sname, tname, cnames))

    
# -- ----------------------------------------------------------------------
def print_required_annotations(model):
    set_elements_not_in_model(model)
    required_dict = {}
    for schema in model.schemas.values():
        for table in schema.tables.values():
            for column in table.columns:
                if column.name in ["Principal_Investigator", "Consortium"]: continue
                if column.required:
                    required_dict.setdefault((schema.name, table.name), set()).add(column.name)

    print("# ---- required elements ----")
    for key, cnames in required_dict.items():
        sname, tname = key
        print("required %s:%s: %s" % (sname, tname, cnames))
        

# -- ------------------------------------------------------------------------
def print_isolated_tables(model):
    referenced_tables = set()
    referring_tables = set()
    for schema in model.schemas.values():
        for table in schema.tables.values():
            if table.foreign_keys:
                referring_tables.add(table)
            for fkey in table.foreign_keys:
                referenced_tables.add(fkey.pk_table)

    print("# ----- print isolated/outbound-only/inbound-only tables ---- ")
    for schema in model.schemas.values():
        for table in schema.tables.values():
            if table not in referenced_tables and table not in referring_tables:
                print("-- isolated: %s:%s" % (table.schema.name, table.name))
            if table in referenced_tables - referring_tables:
                print("-> in_only: %s:%s" % (table.schema.name, table.name))
            if table in referring_tables - referenced_tables:
                print("<- out_only: %s:%s" % (table.schema.name, table.name))
            
# -- =================================================================================
# -- clear schema, table, columns with certain tags
def clear_catalog_wide_annotations(model):
    for schema in model.schemas.values():
        s_tags = list(schema.annotations.keys()).copy()
        for tag in s_tags:
            if tag in catalog_wide_annotation_tags: schema.annotations.pop(tag, None)
        for table in schema.tables.values():
            t_tags = list(table.annotations.keys()).copy()
            for tag in t_tags:
                if tag in catalog_wide_annotation_tags: table.annotations.pop(tag, None)
            for column in table.columns:
                c_tags = list(column.annotations.keys()).copy()
                for tag in c_tags:
                    if tag in catalog_wide_annotation_tags: column.annotations.pop(tag, None)


# -- ---------------------------------------------------------------------------------
# -- update annotations across multiple schemas
def update_catalog_wide_annotations(model):
    if not schemas_not_in_model: set_elements_not_in_model(model)
    
    # -- catalog-wide annotations
    update_generated_elements(model)
    update_required_annotations(model)

# -- =================================================================================
# catalog annotation
def update_catalog_annotations(model):

    chaise_config = get_chaise_config(model.catalog.catalog_id)
    model.annotations[tag["chaise_config"]] = chaise_config
    bulk_upload.update_bulk_upload_annotations(model)
    update_catalog_display(model)
    update_catalog_column_defaults(model)
    

# -- =================================================================================
def remove_catalog_generated(model):

    print(model.annotations.keys())
    if tag["generated"] in model.annotations.keys():  model.annotations.pop(tag["generated"])
    if tag["immutable"] in model.annotations.keys():  model.annotations.pop(tag["immutable"])
    if tag["non_deletable"] in model.annotations.keys(): model.annotations.pop(tag["non_deletable"])
    print(model.annotations.keys())
    model.apply()

# -- =================================================================================
        
def main(server_name, catalog_id, credentials, args):
    server = DerivaServer('https', server_name, credentials)
    catalog = server.connect_ermrest(catalog_id)
    catalog.dcctx['cid'] = DCCTX["annotation"]        
    model = catalog.getCatalogModel()

    '''
    # -- enable to explicitly remove catalog-evel generated annotations 
    if cfg.host == "www.atlas-d2k.org":
        remove_catalog_generated(model)
    '''
    
    if args.pre_print:
        print_isolated_tables(model)
        print("def catalog_annotations(model):");
        print("    model.annotations = %s" % (json.dumps(model.annotations, indent=4)))
        print_presence_tag_annotations(model, [tag["generated"], tag["immutable"], tag["non_deletable"]])
        print_presence_tag_annotations(model, [tag["required"]])
        
    #model.annotations.clear()
    #clear_catalog_wide_annotations(model)
    
    update_catalog_annotations(model)
    update_catalog_wide_annotations(model)
    
    if args.post_print:
        print("def catalog_annotations(model):");
        print("    model.annotations = %s" % (json.dumps(model.annotations, indent=4)))
        print_presence_tag_annotations(model, [tag["generated"], tag["immutable"], tag["non_deletable"]])
        print_presence_tag_annotations(model, [tag["required"]])
        
    if not args.dry_run:
        #model.apply()
        pass
    
# -- =================================================================================

if __name__ == '__main__':
    args = PDBDEVCLI("PDB_Dev", None, 1).parse_cli()
    credentials = get_credential(args.host, args.credential_file)
    print(credentials)
    main(args.host, args.catalog_id, credentials, args)
