#!/usr/bin/python

import sys
import json
from deriva.core import ErmrestCatalog, AttrDict, get_credential, DEFAULT_CREDENTIAL_FILE, tag, urlquote, DerivaServer, get_credential, BaseCLI
from deriva.core.ermrest_model import builtin_types, Schema, Table, Column, Key, ForeignKey
from deriva.core import urlquote, urlunquote
import requests.exceptions
from pdb_dev.utils.shared import DCCTX, PDBDEV_CLI, cfg
from deriva.utils.extras.model import print_catalog_model_extras, print_schema_model_extras, clear_catalog_annotations, print_table_model_extras, get_schemas, get_tables, get_columns, check_model_acl_types

"""
# == variable names available during upload
UploadMetadataReservedKeyNames = [
    "URI", "file_name", "file_ext", "file_size", "base_path", "base_name", "content-disposition", "md5", "sha256",
    "md5_base64", "sha256_base64", "schema", "table", "target_table", "_upload_year_", "_upload_month_", "_upload_day_",
    "_upload_time_", "_identity_id", "_identity_display_name", "_identity_full_name", "_identity_email"]
Note: All these are reserved word. Don't try to overwrite. Currently, file_ext can be overwritten, but base_name is
computed based on file_ext.

"""

def get_upload_config():
    """
    upload config for cif and image files.

    Note: 09/01/26: (RCB, File_Name) is not a key. Consider adding this to be consistent with IHM.
    Since (RCB, Title) is a key and base_name is used for Title, the tool will not allow model.cif
    with different MD5
    """
    
    config =  {
        "version_update_url": "https://github.com/informatics-isi-edu/deriva-client",
        "version_compatibility": [
            [
                ">=1.4.0",
                "<2.0.0"
            ]
        ],
        "asset_mappings": [
            {
                "column_map": {
                    "RID": "{RID}",                    
                    "Title": "{title}",
                    "File_MD5": "{md5}",
                    "File_URL": "{URI}",
                    "File_Bytes": "{file_size}",
                    "File_Name": "{file_name}",
                },
                "file_pattern": "(?i)^.*/deriva/(?P<globus_ID>[^/]*)/ihmv_structure/(?P<title>[^/]*)[.](?P<ext>cif)$",
                "target_table": [
                    "IHMV",
                    "Structure_mmCIF"
                ],
                "checksum_types": [
                    "sha256",
                    "md5"
                ],
                "hatrac_options": {
                    "versioned_urls": True
                },
                "hatrac_templates": {
                    "hatrac_uri": "/hatrac/ihmv/submitted/uid/{globus_ID}/structure/mmCIF/{md5}.cif",
                    "content-disposition": "filename*=UTF-8''{file_name}"
                },
                "record_query_template": "/entity/{target_table}/File_MD5={md5}&RCB=https%3A%2F%2Fauth.globus.org%2F{globus_ID}",
                "record_update_template": "/attributegroup/{target_table}/RID;Title,File_Name,File_URL,File_MD5,File_Bytes",
                "metadata_query_templates": [
                ],
                "create_record_before_upload": False,
                "require_record_update_template": True
            },
        ],
    }
    
    return(config)

# -- ==========================================================================
def print_bulk_upload_annotations(model):
    annotation = model.annotations[tag["bulk_upload"]]
    print("    config = ")
    print("%s" % (json.dumps(annotation, indent=4)))
    print()

# -- ==========================================================================    
def update_bulk_upload_annotations(model):

    model.bulk_upload.update(get_upload_config())
    
    
# -- ==========================================================================
def main(server_name, catalog_id, credentials):
    server = DerivaServer('https', server_name, credentials)
    catalog = server.connect_ermrest(catalog_id)
    catalog.dcctx['cid'] = DCCTX["annotation"]
    model = catalog.getCatalogModel()

    if args.pre_print:
        print_bulk_upload_annotations(model)
        
    # clear relevant annotations
    clear_catalog_annotations(model, [tag["bulk_upload"]])
    update_bulk_upload_annotations(model)
    
    if args.post_print:
        print_bulk_upload_annotations(model)
    
    if not args.dry_run:
        model.apply()
        pass

# -- =================================================================================

if __name__ == '__main__':
    cli = PDBDEV_CLI("MA", None, 1)
    args = cli.parse_cli()
    credentials = get_credential(args.host, args.credential_file)

    main(args.host, args.catalog_id, credentials)
