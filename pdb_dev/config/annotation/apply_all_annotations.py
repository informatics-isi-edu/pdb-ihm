#!/usr/bin/python

import sys
import json
from deriva.core import ErmrestCatalog, AttrDict, get_credential, DEFAULT_CREDENTIAL_FILE, tag, urlquote, DerivaServer, get_credential, BaseCLI
from deriva.core.ermrest_model import builtin_types, Schema, Table, Column, Key, ForeignKey
from deriva.core import urlquote, urlunquote
import requests.exceptions
from ...utils.shared import DCCTX, PDBDEV_CLI
from deriva.utils.extras.model import print_catalog_model_extras, print_schema_model_extras, print_table_model_extras, per_schema_annotation_tags, clear_schema_annotations

from . import catalog_annotations
from . import export
from . import asset
from . import citation

'''
from . import google_dataset
from . import viz_3d_display
'''
from . import PDB
from . import Vocab
from . import public    
#from . import _acl_admin # NOT IN MODEL

# This script pull all the annotations in different scripts together and
# apply them simultaneously. The operation is idempotent. 
# -- ----------------------------------------------------------------------

# -- =================================================================================
        
def main(server_name, catalog_id, credentials, args):
    server = DerivaServer('https', server_name, credentials)
    catalog = server.connect_ermrest(catalog_id)
    catalog.dcctx['cid'] = DCCTX["annotation"]
    model = catalog.getCatalogModel()

    if args.pre_print:
        if args.schema and args.table:
            print_table_model_extras(model, args.schema, args.table, annotations=True, acls=False, acl_bindings=False, exclude_default_fkey=False)
        elif args.schema:
            print_schema_model_extras(model, args.schema, annotations=True, acls=False, acl_bindings=False, exclude_default_fkey=False)            
        else:
            print_catalog_model_extras(model, annotations=True, acls=False, acl_bindings=False, exclude_default_fkey=False)        
        return

    # -- clear annotations
    model.clear(clear_comment=False, clear_annotations=True, clear_acls=False, clear_acl_bindings=False)

    #catalog_annotations.clear_catalog_catalog_wide_annotations(model)
    #clear_schema_annotations(model, "Vocab", per_schema_annotation_tags)
    #clear_schema_annotations(model, "PDB", per_schema_annotation_tags)
    #clear_schema_annotations(model, "public", per_schema_annotation_tags)
    #export.clear_export_annotations(model)
    #asset.clear_asset_annotations(model)
    #citation.clear_citation_annotations(model)
    
    # -- catalog annotation (chaise_config, bulk_upload) and catalog-wide annotations
    catalog_annotations.update_catalog_annotations(model)
    catalog_annotations.update_catalog_wide_annotations(model)

    # -- per schema annotations
    Vocab.update_Vocab_annotations(model)
    PDB.update_PDB_annotations(model)
    public.update_public_annotations(model)
    
    # -- tag specifics annotations
    export.update_export_annotations(model)
    asset.update_asset_annotations(model)
    citation.update_citation_annotations(model)
    
    '''    
    viz_3d_display.update_viz_3d_display_annotations(model)
    # -- per schema annotations
    #public.update_public_annotations(model)
    #_acl_admin.update__acl_admin_annotations(model)    
    '''

    if args.post_print:
        if args.schema and args.table:
            print_table_model_extras(model, args.schema, args.table, annotations=True, acls=False, acl_bindings=False, exclude_default_fkey=False)
        elif args.schema:
            print_schema_model_extras(model, args.schema, annotations=True, acls=False, acl_bindings=False, exclude_default_fkey=False)            
        else:
            print_catalog_model_extras(model, annotations=True, acls=False, acl_bindings=False, exclude_default_fkey=False)        
        return
    if not args.dry_run:
        model.apply()
        print("Model changes have been applied")
        pass
    

# -- =================================================================================
'''
To run the annotation updates:
> python -m pdb_dev.config.annotation.apply_all_annotations --host dev-aws.pdb-dev.org --catalog-id 99

Note: This script doesn't clean up existing annotations in the database, and has to run after .cpp file.
'''

if __name__ == '__main__':
    cli = PDBDEV_CLI("PDB_Dev", None, "1.0")
    cli.parser.add_argument('--schema', metavar='<schema>', help="print catalog acl script without applying", default=False)
    cli.parser.add_argument('--table', metavar='<table>', help="print catalog acl script without applying", default=False)
    args = cli.parse_cli()
    credentials = get_credential(args.host, args.credential_file)
    print(credentials)

    if args.debug:
        init_logging(level=logging.DEBUG)
    
    main(args.host, args.catalog_id, credentials, args)
