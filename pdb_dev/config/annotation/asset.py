import json
from deriva.core import ErmrestCatalog, AttrDict, get_credential, DEFAULT_CREDENTIAL_FILE, tag, urlquote, DerivaServer, get_credential, BaseCLI
from deriva.core.ermrest_model import builtin_types, Schema, Table, Column, Key, ForeignKey
from deriva.core import urlquote, urlunquote
import requests.exceptions
#from ...utils.shared import DCCTX, PDBDEV_CLI
from pdb_dev.utils.shared import DCCTX, PDBDEV_CLI, cfg
from deriva.utils.extras.model import print_catalog_model_extras, print_schema_model_extras, print_table_model_extras, get_schemas, get_tables, get_columns, check_model_acl_types, tag2name, clear_all_schema_annotations

# -- =================================================================================
# -- asset related annotations
# -- =================================================================================

def x_update_WWW(model):
    # ----------------------------
    model.schemas["WWW"].tables["Page_Asset"].columns["URL"].asset.update(
        [
            {
                "md5": "MD5",
                "url_pattern": "%s/WWW/Page_Asset/{{{MD5}}}.{{#encode}}{{{Filename}}}{{/encode}}",
                "filename_column": "Filename",
                "byte_count_column": "Length"
            }
        ]
    )

# --------------------------------------------------------------------------------------    
def update_PDB_entry_related(model):
    schema = model.schemas["PDB"]

    # ----------------------------
    model.schemas["PDB"].tables["entry"].columns["Image_File_URL"].asset.update({
        "md5": "Image_File_MD5",
        "url_pattern": "%s/pdb/submitted/uid/{{#if _RCB}}{{#regexFindFirst _RCB \"[^/]+$\"}}{{this}}{{/regexFindFirst}}{{else}}{{#regexFindFirst $session.client.id \"[^/]+$\"}}{{this}}{{/regexFindFirst}}{{/if}}/entry/image/{{{Image_File_MD5}}}{{{_Image_File_URL.filename_ext}}}" % (cfg.hatrac_root),
        "filename_column": "Image_File_Name",
        "template_engine": "handlebars",
        "byte_count_column": "Image_File_Bytes"
    })
    
    # ----------------------------
    model.schemas["PDB"].tables["entry"].columns["mmCIF_File_URL"].asset.update({
        "md5": "mmCIF_File_MD5",
        "url_pattern": "%s/pdb/submitted/uid/{{#if _RCB}}{{#regexFindFirst _RCB \"[^/]+$\"}}{{this}}{{/regexFindFirst}}{{else}}{{#regexFindFirst $session.client.id \"[^/]+$\"}}{{this}}{{/regexFindFirst}}{{/if}}/entry/mmCIF/{{{mmCIF_File_MD5}}}{{{_mmCIF_File_URL.filename_ext}}}" % (cfg.hatrac_root),
        "filename_column": "mmCIF_File_Name",
        "template_engine": "handlebars",
        "byte_count_column": "mmCIF_File_Bytes",
        "filename_ext_filter": [
            ".cif",
            ".CIF"
        ]
    })

    # ----------------------------
    model.schemas["PDB"].tables["Entry_Generated_File"].columns["File_URL"].asset.update({
        "md5": "File_MD5",
        "url_pattern": "%s/pdb/generated/uid/{{#if _Entry_RCB}}{{#regexFindFirst _Entry_RCB \"[^/]+$\"}}{{this}}{{/regexFindFirst}}{{else}}{{#regexFindFirst $session.client.id \"[^/]+$\"}}{{this}}{{/regexFindFirst}}{{/if}}/entry/id/{{{Structure_Id}}}/final_mmCIF/{{{File_Name}}}" % (cfg.hatrac_root),
        "filename_column": "File_Name",
        "template_engine": "handlebars",
        "byte_count_column": "File_Bytes"
    })

    # ----------------------------
    model.schemas["PDB"].tables["Entry_Related_File"].columns["File_URL"].asset.update({
        "md5": "File_MD5",
        "url_pattern": "%s/pdb/submitted/uid/{{#if _RCB}}{{#regexFindFirst _RCB \"[^/]+$\"}}{{this}}{{/regexFindFirst}}{{else}}{{#regexFindFirst $session.client.id \"[^/]+$\"}}{{this}}{{/regexFindFirst}}{{/if}}/entry/id/{{{structure_id}}}/related_file/{{{File_MD5}}}{{{_File_URL.filename_ext}}}" % (cfg.hatrac_root),
        "filename_column": "File_Name",
        "template_engine": "handlebars",
        "byte_count_column": "File_Bytes"
    })

    # ----------------------------
    model.schemas["PDB"].tables["Entry_Related_File_Templates"].columns["File_URL"].asset.update({
        "md5": "File_MD5",
        "url_pattern": "%s/pdb/templates/{{{File_Name}}}" % (cfg.hatrac_root),
        "filename_column": "File_Name",
        "byte_count_column": "File_Bytes"
    })

    # ----------------------------
    model.schemas["PDB"].tables["Entry_Error_File"].columns["File_URL"].asset.update({
    "md5": "File_MD5",
        "url_pattern": "%s/pdb/generated/uid/{{#if _RCB}}{{#regexFindFirst _RCB \"[^/]+$\"}}{{this}}{{/regexFindFirst}}{{else}}{{#regexFindFirst $session.client.id \"[^/]+$\"}}{{this}}{{/regexFindFirst}}{{/if}}/entry/rid/{{{Entry_RID}}}/validation_error/{{{File_Name}}}" % (cfg.hatrac_root),
        "filename_column": "File_Name",
        "template_engine": "handlebars",
        "byte_count_column": "File_Bytes"
    })
    

# --------------------------------------------------------------------------------------
def update_PDB_ihm_related(model):
    
    # ----------------------------
    model.schemas["PDB"].tables["ihm_starting_model_details"].columns["mmCIF_File_URL"].asset.update({
        "md5": "mmCIF_File_MD5",
        "url_pattern": "%s/pdb/submitted/uid/{{#if _RCB}}{{#regexFindFirst _RCB \"[^/]+$\"}}{{this}}{{/regexFindFirst}}{{else}}{{#regexFindFirst $session.client.id \"[^/]+$\"}}{{this}}{{/regexFindFirst}}{{/if}}/entry/id/{{{structure_id}}}/starting_model/{{{mmCIF_File_MD5}}}{{{_mmCIF_File_URL.filename_ext}}}" % (cfg.hatrac_root),
        "filename_column": "mmCIF_File_Name",
        "template_engine": "handlebars",
        "byte_count_column": "mmCIF_File_Bytes"
    })
    
# --------------------------------------------------------------------------------------
# /hatrac/dev/pdb/generated/archive/pdb_ihm/holdings/2024/2024-11-28/
def update_PDB_PDB_Archive(model):
    # ----------------------------
    model.schemas["PDB"].tables["PDB_Archive"].columns["Current_File_Holdings_URL"].asset.update({
        "md5": "Current_File_Holdings_MD5",
        "url_pattern": "%s/pdb/generated/archive/pdb_ihm/holdings/{{$moment.year}}/{{formatDate $moment.ISOString 'YYYY-MM-DD'}}/{{{Current_File_Holdings_Name}}}" % (cfg.hatrac_root),
        "filename_column": "Current_File_Holdings_Name",
        "byte_count_column": "Current_File_Holdings_Bytes"
    })
    
    # ----------------------------
    model.schemas["PDB"].tables["PDB_Archive"].columns["Released_Structures_LMD_URL"].asset.update({
        "md5": "Released_Structures_LMD_MD5",
        "url_pattern": "%s/pdb/generated/archive/pdb_ihm/holdings/{{$moment.year}}/{{formatDate $moment.ISOString 'YYYY-MM-DD'}}/{{{Released_Structures_LMD_Name}}}" % (cfg.hatrac_root),        
        "filename_column": "Released_Structures_LMD_Name",
        "byte_count_column": "Released_Structures_LMD_Bytes"
    })

    # ----------------------------
    model.schemas["PDB"].tables["PDB_Archive"].columns["Unreleased_Entries_URL"].asset.update({
        "md5": "Unreleased_Entries_MD5",
        #"url_pattern": "%s/pdb/archive/holdings/{{$moment.year}}/{{{Unreleased_Entries_Name}}}" % (cfg.hatrac_root),
        "url_pattern": "%s/pdb/generated/archive/pdb_ihm/holdings/{{$moment.year}}/{{formatDate $moment.ISOString 'YYYY-MM-DD'}}/{{{Unreleased_Entries_Name}}}" % (cfg.hatrac_root),                
        "filename_column": "Unreleased_Entries_Name",
        "byte_count_column": "Unreleased_Entries_Bytes"
    })
    
# --------------------------------------------------------------------------------------
def update_PDB_IHM_New_Chem_Comp(model):
    
    model.schemas["PDB"].tables["IHM_New_Chem_Comp"].columns["CCD_CIF_File_URL"].asset.update({
        'md5': 'CCD_CIF_File_MD5',
        'url_pattern': "%s/pdb/internal/CCD/{{$moment.year}}/{{{CCD_CIF_File_Name}}}" % (cfg.hatrac_root),
        'filename_column': 'CCD_CIF_File_Name',
        'byte_count_column': 'CCD_CIF_File_Bytes'
    })
                                                                                        
# -- ==========================================================================
def print_asset_annotations(model):
    for schema in model.schemas.values():
        print("def update_%s(model):" % (schema.name))
        for table in schema.tables.values():
            for cname in table.columns.elements:
                column = table.columns[cname]
                if column.asset:
                    print('    # ----------------------------')
                    print('    model.schemas["%s"].tables["%s"].columns["%s"].asset.update(' % (schema.name, table.name, column.name))
                    print('%s' % (json.dumps(column.asset, indent=4)))
                    print(')\n')
        print()
    

# -- =================================================================================    
def update_asset_annotations(model):
    
    update_PDB_entry_related(model)
    update_PDB_ihm_related(model)
    update_PDB_PDB_Archive(model)
    update_PDB_IHM_New_Chem_Comp(model)
    

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
