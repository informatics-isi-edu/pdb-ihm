#!/usr/bin/python

import sys
import json
import logging

from deriva.core import ErmrestCatalog, AttrDict, get_credential, DEFAULT_CREDENTIAL_FILE, tag, urlquote, DerivaServer, get_credential
from deriva.core.ermrest_model import builtin_types, Schema, Table, Column, Key, ForeignKey, DomainType, ArrayType

from deriva.utils.extras.data import get_ermrest_query, update_table_rows
from ...utils.shared import PDBDEV_CLI, DCCTX

logger = logging.getLogger(__name__)

# ============================================================
"""
SELECT s."RCB", MIN(c."Full_Name") AS "Name", s."File_Name", COUNT(s."RID"), array_agg(s."RID"), array_agg(s."Title") 
FROM "IHMV"."Structure_mmCIF" s JOIN public."ERMrest_Client" c ON (s."RCB" = c."ID")
GROUP BY s."RCB", s."File_Name"
HAVING COUNT(s."RID") > 1
;
"""
def migrate_Structure_mmCIF_File_Name(model):
    sname = "IHMV"
    tname = "Structure_mmCIF"
    catalog = model.catalog

    structures = get_ermrest_query(catalog, sname, tname)
    rid2rows = { row["RID"]: row for row in structures }
    
    key2rows = {}
    duplicates = []
    for row in structures:
        key = (row["RCB"], row["File_Name"])
        if key in key2rows.keys():
            duplicates.append(row["RID"])
        else:
            key2rows[key] = row

    logger.info("Duplicate filenames [%d]: %s" % (len(duplicates), [ (rid2rows[rid]["RID"], rid2rows[rid]["RCB"], rid2rows[rid]["File_Name"]) for rid in duplicates]))
    
    updating = []
    for rid in duplicates:
        row = rid2rows[rid]
        updating.append({
            "RID": row["RID"],
            "File_Name": row["File_Name"].replace(".cif", f'_{row["RID"]}.cif'),
        })
        
    logger.info("migrate_Structure_mmCIF_File_Name: updating Structure_mmCIF [%d]: %s" % (len(updating), json.dumps(updating[0:10], indent=4)))
    updated = update_table_rows(catalog, sname, tname, payload=updating, model=model, column_names=["File_Name"])
    logger.info("migrate_Structure_mmCIF_File_Name: updated Structure_mmCIF [%d]: %s" % (len(updated), json.dumps(updated[0:10], indent=4)))
        

def update_Structure_mmCIF(model):
    sname = "IHMV"
    tname = "Structure_mmCIF"
    schema = model.schemas[sname]
    table = schema.tables[tname]

    # == update key constraint
    constraint_name = "Structure_mmCIF_RCB_File_Name_key"
    if (schema, constraint_name) in table.keys.elements:
        logger.info("ihmv create key: %s:%s key already exists" % (tname, constraint_name))
    else:
        table.create_key(
            Key.define(["RCB", "File_Name"], constraint_names=[[sname, constraint_name]] )
        )
        logger.info("ihmv create key: %s:%s - created" % (tname, constraint_name))

        
def update_ihmv_2026(model):
    """Update ihmv model
    """
    migrate_Structure_mmCIF_File_Name(model)
    update_Structure_mmCIF(model)

    
    
# ============================================================
def update_model(args, credentials):
    """Update IHMV model"""
    
    server = DerivaServer('https', args.host, credentials)
    catalog = server.connect_ermrest(args.catalog_id)
    catalog.dcctx['cid'] = DCCTX["model"]
    model = catalog.getCatalogModel()
    
    update_ihmv_2026(model)

    
def main():
    """Update IHMV model main
    """
    cli = PDBDEV_CLI('ihmv', None, 1)
    args = cli.parse_cli()        
    credentials = get_credential(args.host, credential_file=args.credential_file)

    update_model(args, credentials)

    
if __name__ == '__main__':
    sys.exit(main())
    
