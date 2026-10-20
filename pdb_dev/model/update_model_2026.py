#!/usr/bin/python

import sys
import json
import logging

from deriva.core import ErmrestCatalog, AttrDict, get_credential, DEFAULT_CREDENTIAL_FILE, tag, urlquote, DerivaServer, get_credential
from deriva.core.ermrest_model import builtin_types, Schema, Table, Column, Key, ForeignKey, DomainType, ArrayType

from deriva.utils.extras.data import get_ermrest_query, update_table_rows
from pdb_dev.utils.shared import PDBDEV_CLI, DCCTX

logger = logging.getLogger(__name__)


# ======================================================================

cname2comments = {
    "User_mmCIF_File_URL": "Latest user submitted file URL",
    "User_mmCIF_File_Name": "Latest user submitted file name",
}

def migrate_user_mmcif_files(model):
    catalog = model.catalog
    attributes=["mmCIF_File_URL", "mmCIF_File_Name", "User_mmCIF_File_URL", "User_mmCIF_File_Name"]    
    entries = get_ermrest_query(catalog, "PDB", "entry", attributes=attributes)
    
    updating = []
    for row in entries:
        if row["User_mmCIF_File_URL"] != row["mmCIF_File_URL"]:
            updating_row = row.copy()
            updating_row.update({
                "User_mmCIF_File_URL": row["mmCIF_File_URL"],
                "User_mmCIF_File_Name": row["mmCIF_File_Name"]
            })
            updating.append(updating_row)

    logger.info("migrate_user_mmcif_files: updating entries [%d]: %s" % (len(updating), json.dumps(updating[0:2], indent=4)))
    updated = update_table_rows(catalog, "PDB", "entry", payload=updating, model=model, column_names=list(cname2comments.keys()))
    logger.info("migrate_user_mmcif_files: updated entries [%d]: %s" % (len(updated), json.dumps(updated[0:2], indent=4)))


def update_entry_user_mmcif_file(model):
    """Update model and migrate data to keep track of user submitted mmcif files
    Target deployment date: 11/15/2026
    """
    sname = "PDB"
    tname = "entry"

    table = model.schemas[sname].tables[tname]
    for cname in cname2comments.keys():
        if cname not in table.columns.elements:
            table.create_column(
                Column.define(
                    cname,
                    builtin_types.text,
                    nullok=True,
                    comment=cname2comments[cname],
                ),
            )
            logger.info("Create column: %s:%s - created" % (tname, cname))
        else:
            logger.info("Create column: %s:%s already exists" % (tname, cname))

    migrate_user_mmcif_files(model)

def update_Entry_Generated_File(model):
    """Drop obsolete columns according to issue:
    https://github.com/informatics-isi-edu/pdb-ihm/issues/281
    """
    sname = "PDB"
    tname = "Entry_Generated_File"
    table = model.schemas[sname].tables[tname]
    
    for cname in ["mmCIF_Schema_Version"]:
        if cname in table.columns.elements:
            table.columns[cname].drop()
            logger.info("drop column: %s:%s - dropped" % (tname, cname))
        else:
            logger.info("drop column: %s:%s doesn't exist" % (tname, cname))
    
# ============================================================
def update_model_2026(model):
    logger.info("== update_model_2026: begins ==")
    
    update_entry_user_mmcif_file(model)
    update_Entry_Generated_File(model)
    
    logger.info("== update_model_2026: ends ==")

# ===================================================    

def main():
    """Update model main
    """
    cli = PDBDEV_CLI('ad-hoc table creation tool', None, 1).parse_cli()
    args = cli.parse_cli()        
    credentials = cli.get_credential(args.host, credential_file=args.credential_file)

    server = DerivaServer('https', args.host, credentials)
    catalog = server.connect_ermrest(args.catalog_id)
    catalog.dcctx['cid'] = DCCTX["model"]
    model = catalog.getCatalogModel()
    
    update_model_2026(model)    
    

if __name__ == '__main__':
    sys.exit(main())
    
