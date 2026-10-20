#!/usr/bin/python

import sys
import json

from deriva.core import ErmrestCatalog, AttrDict, get_credential, DEFAULT_CREDENTIAL_FILE, tag, urlquote, DerivaServer, get_credential
from deriva.core.ermrest_model import builtin_types, Schema, Table, Column, Key, ForeignKey, DomainType, ArrayType

from deriva.utils.extras.data import get_ermrest_query, update_table_rows
from ..utils.shared import PDBDEV_CLI, DCCTX
from .update_model_2026 import update_model_2026

# ============================================================


# ============================================================
def update_model(args, credentials):
    """Update model"""
    
    server = DerivaServer('https', args.host, credentials)
    catalog = server.connect_ermrest(args.catalog_id)
    catalog.dcctx['cid'] = DCCTX["model"]
    model = catalog.getCatalogModel()
    
    update_model_2026(model)

    
def main():
    """Update model main
    """
    cli = PDBDEV_CLI('pdb', None, 1)
    args = cli.parse_cli()        
    credentials = get_credential(args.host, credential_file=args.credential_file)

    update_model(args, credentials)

    
if __name__ == '__main__':
    sys.exit(main())
    
