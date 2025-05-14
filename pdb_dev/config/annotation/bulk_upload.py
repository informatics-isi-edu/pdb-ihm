#!/usr/bin/python

import sys
import json
from deriva.core import ErmrestCatalog, AttrDict, get_credential, DEFAULT_CREDENTIAL_FILE, tag, urlquote, DerivaServer, get_credential, BaseCLI
from deriva.core.ermrest_model import builtin_types, Schema, Table, Column, Key, ForeignKey
from deriva.core import urlquote, urlunquote
import requests.exceptions
#from ...utils.shared import DCCTX, PDBDEV_CLI, cfg
from pdb_dev.utils.shared import DCCTX, PDBDEV_CLI, cfg
from deriva.utils.extras.model import print_catalog_model_extras, print_schema_model_extras, clear_catalog_annotations, print_table_model_extras, get_schemas, get_tables, get_columns, check_model_acl_types

"""
# Extra asset_mappings definitions that is in .cpp. 
    config = {
        "asset_mappings": [
            {
                "asset_type": "table",
                "ext_pattern": "^.*[.](?P<file_ext>json|csv)$",
                "file_pattern": "^((?!/assets/).)*/records/(?P<schema>WWW?)/(?P<table>Page)[.]",
                "target_table": [
                    "WWW",
                    "Page"
                ],
                "default_columns": [
                    "RID",
                    "RCB",
                    "RMB",
                    "RCT",
                    "RMT"
                ]
            },
            {
                "column_map": {
                    "MD5": "{md5}",
                    "URL": "{URI}",
                    "Page": "{table_rid}",
                    "Length": "{file_size}",
                    "Filename": "{file_name}"
                },
                "dir_pattern": "^.*/(?P<schema>WWW)/(?P<table>Page)/(?P<key_column>.*)/",
                "ext_pattern": "^.*[.](?P<file_ext>.*)$",
                "file_pattern": ".*",
                "target_table": [
                    "WWW",
                    "Page_Asset"
                ],
                "checksum_types": [
                    "md5"
                ],
                "hatrac_options": {
                    "versioned_uris": true
                },
                "hatrac_templates": {
                    "hatrac_uri": "/hatrac/{schema}/{table}/{md5}.{file_name}"
                },
                "record_query_template": "/entity/{schema}:{table}_Asset/{table}={table_rid}/MD5={md5}/URL={URI_urlencoded}",
                "metadata_query_templates": [
                    "/attribute/D:={schema}:{table}/RID={key_column}/table_rid:=D:RID"
                ]
            },

        ]
    }
"""

def get_upload_config():
    """
    upload config for cif and image files.
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
                    "Method_Details": "Integrative modeling",
                    "mmCIF_File_MD5": "{md5}",
                    "mmCIF_File_URL": "{URI}",
                    "Workflow_Status": "DEPO",
                    "mmCIF_File_Name": "{file_name}",
                    "mmCIF_File_Bytes": "{file_size}"
                },
                "file_pattern": "(?i)^.*/deriva/(?P<globus_ID>[^/]*)/entry/.*[.](?P<file_ext>cif)$",
                "target_table": [
                    "PDB",
                    "entry"
                ],
                "checksum_types": [
                    "sha256",
                    "md5"
                ],
                "hatrac_options": {
                    "versioned_urls": True
                },
                "hatrac_templates": {
                    "hatrac_uri": "/hatrac/pdb/submitted/uid/{globus_ID}/entry/mmcif/{file_name}",
                    "content-disposition": "filename*=UTF-8''{file_name}"
                },
                "record_query_template": "/entity/{target_table}/mmCIF_File_MD5={md5}&RCB=https%3A%2F%2Fauth.globus.org%2F{globus_ID}",
                "record_update_template": "/attributegroup/{target_table}/RID;mmCIF_File_MD5,mmCIF_File_URL,mmCIF_File_Name,mmCIF_File_Bytes",
                "metadata_query_templates": [],
                "create_record_before_upload": False,
                "require_record_update_template": True
            },
            {
                "column_map": {
                    "RID": "{entry_rid}",
                    "Image_File_MD5": "{md5}",
                    "Image_File_URL": "{URI}",
                    "Image_File_Name": "{file_name}",
                    "Image_File_Bytes": "{file_size}"
                },
                "dir_pattern": "(?i)^.*/deriva/(?P<globus_ID>[^/]*)/entry/(?P<base_name>[^/]*)[.](?P<file_ext>png|jpg|jpeg)",
                "target_table": [
                    "PDB",
                    "entry"
                ],
                "checksum_types": [
                    "sha256",
                    "md5"
                ],
                "hatrac_options": {
                    "versioned_urls": True
                },
                "hatrac_templates": {
                    "hatrac_uri": "/hatrac/pdb/submitted/uid/{globus_ID}/entry/image/{file_name}",
                    "content-disposition": "filename*=UTF-8''{file_name}"
                },
                "record_query_template": "/entity/{target_table}/RID={entry_rid}",
                "record_update_template": "/attributegroup/{target_table}/RID;Image_File_MD5,Image_File_URL,Image_File_Name,Image_File_Bytes",
                "metadata_query_templates": [
                    "/attribute/{target_table}/mmCIF_File_Name={base_name}.cif&RCB=https%3A%2F%2Fauth.globus.org%2F{globus_ID}/entry_rid:=RID"
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
        #model.apply()
        pass

# -- =================================================================================

if __name__ == '__main__':
    cli = PDBDEV_CLI("MA", None, 1)
    args = cli.parse_cli()
    credentials = get_credential(args.host, args.credential_file)

    main(args.host, args.catalog_id, credentials)
