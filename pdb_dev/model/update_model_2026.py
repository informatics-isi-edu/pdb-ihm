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
    """Populate User_mmCIF_File related columns of existing entries
    """
    logger.info("migrate_user_mmcif_files - begins")
    
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

    
def migrate_accession_issue_time(model):
    """Populate Accession_Issue_Time of existing entries
    """
    logger.info("migrate_accession_issue_time - begins")
    
    catalog = model.catalog
    attributes=["Deposit_Date", "Accession_Issue_Time"]
    entries = get_ermrest_query(catalog, "PDB", "entry", constraints="Accession_Issue_Time::null::", attributes=attributes)
    
    updating = []
    for row in entries:
        if not row["Accession_Issue_Time"]:
            updating.append({
                "RID": row["RID"],
                "Accession_Issue_Time": row["Deposit_Date"]
            })
            
    logger.info("migrate_accession_issue_time: updating entries [%d]: %s" % (len(updating), json.dumps(updating[0:2], indent=4)))
    updated = update_table_rows(catalog, "PDB", "entry", payload=updating, model=model, column_names=["Accession_Issue_Time"])
    logger.info("migrate_accession_issue_time: updated entries [%d]: %s" % (len(updated), json.dumps(updated[0:2], indent=4)))
    

def update_PDB_entry(model):
    """Update model and migrate data to keep track of user submitted mmcif files
    Target deployment date: 11/15/2026
    """
    logger.info("update_PDB_entry - begins")
    
    sname = "PDB"
    tname = "entry"
    table = model.schemas[sname].tables[tname]
    
    # == User_mmCIF_File columns
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
            logger.info("+ Create column: %s:%s - created" % (tname, cname))
        else:
            logger.info("Create column: %s:%s already exists" % (tname, cname))

    # == accession_issue_date: drop
    cname = "Accession_Issue_Date"
    if cname in table.columns.elements:
        table.columns[cname].drop()
        logger.info("+ Drop column: %s:%s - dropped" % (tname, cname))        
        
    # == accession_issue_time
    cname = "Accession_Issue_Time"
    if cname not in table.columns.elements:
        table.create_column(
            Column.define(
                cname,
                builtin_types.timestamptz,
                nullok=True,
                comment="Accession code issue time",
            ),
        )
        logger.info("+ Create column: %s:%s - created" % (tname, cname))
    else:
        logger.info("Create column: %s:%s already exists" % (tname, cname))
    

def update_PDB_Entry_Generated_File(model):
    """Drop obsolete columns according to issue:
    https://github.com/informatics-isi-edu/pdb-ihm/issues/281
    """
    logger.info("update_PDB_Entry_Generated_File - begins")    
    sname = "PDB"
    tname = "Entry_Generated_File"
    table = model.schemas[sname].tables[tname]
    
    for cname in ["mmCIF_Schema_Version"]:
        if cname in table.columns.elements:
            table.columns[cname].drop()
            logger.info("+ drop column: %s:%s - dropped" % (tname, cname))
        else:
            logger.info("drop column: %s:%s doesn't exist" % (tname, cname))

def update_PDB_ihm_multi_state_scheme_connectivity(model):
    """begin_state_id and end_state_id share the same RID, which is incorrect.
    Need seprate RID for begin and end.
    """
    sname = "PDB"
    tname = "ihm_multi_state_scheme_connectivity"
    schema = model.schemas[sname]
    table = schema.tables[tname]

    logger.info("update_PDB_ihm_multi_state_scheme_connectivity - begins")
    
    # == rename State_RID to Begin_State_RID
    cname = "State_RID"
    if cname in table.columns.elements:
        table.columns[cname].alter(name="Begin_State_RID")
        logger.info("+ rename column: %s:%s - renamed" % (tname, cname))
    else:
        logger.info("rename column: %s:%s doesn't exist" % (tname, cname))        
        
    # == create End_State_RID        
    cname = "End_State_RID"
    if cname not in table.columns.elements:
        table.create_column(
            Column.define(
                cname,
                builtin_types.text,
                nullok=True,
            ),
        )
        logger.info("+ Create column: %s:%s - created" % (tname, cname))
    else:
        logger.info("Create column: %s:%s already exists" % (tname, cname))        

    # == drop and recrate begin_state fkey
    ct_name = "ihm_multi_state_scheme_connectivity_modeling_1_combo1_fkey"
    if (schema, ct_name) in table.foreign_keys.elements:
        table.foreign_keys[(schema, ct_name)].drop()
        logger.info("+ drop fkey: %s:%s - dropped" % (tname, ct_name))
    else:
        logger.info("drop fkey: %s:%s doesn't exist" % (tname, ct_name))

    ct_name = "ihm_multi_state_scheme_connectivity_begin_state_combo1_fkey"
    if (schema, ct_name) not in table.foreign_keys.elements:
        table.create_fkey(
            ForeignKey.define(
                ["Begin_State_RID", "structure_id", "begin_state_id"],
                "PDB", "ihm_multi_state_modeling", ["RID", "structure_id", "state_id"],
                constraint_names=[[schema.name, ct_name]],
                on_update="CASCADE"
            )
        )
        logger.info("+ create fkey: %s:%s - created" % (tname, ct_name))
    else:
        logger.info("create fkey: %s:%s already exists" % (tname, ct_name))

    # == drop and recreate end_state fkey
    ct_name = "ihm_multi_state_scheme_connectivity_modeling_2_combo2_fkey"
    if (schema, ct_name) in table.foreign_keys.elements:
        table.foreign_keys[(schema, ct_name)].drop()
        logger.info("+ drop fkey: %s:%s - dropped" % (tname, ct_name))
    else:
        logger.info("drop fkey: %s:%s doesn't exist" % (tname, ct_name))        
        
    ct_name = "ihm_multi_state_scheme_connectivity_end_state_combo2_fkey"
    if (schema, ct_name) not in table.foreign_keys.elements:
        table.create_fkey(
            ForeignKey.define(
                ["End_State_RID", "end_state_id"],
                "PDB", "ihm_multi_state_modeling", ["RID", "state_id"],
                constraint_names=[[schema.name, ct_name]],
                on_update="CASCADE"
            )
        )
        logger.info("+ create fkey: %s:%s - created" % (tname, ct_name))
    else:
        logger.info("create fkey: %s:%s already exists" % (tname, ct_name))        


def update_PDB_chem_comp_atom(model):
    """Drop chem_comp_atom table if exist"""
    
    logger.info("update_PDB_checm_comp_atom - begins")
    sname = "PDB"
    tname = "chem_comp_atom"
    schema = model.schemas[sname]
    
    if tname in schema.tables.keys():
        schema.tables[tname].drop()
        logger.info("+ drop table: %s - dropped" % (tname))
    else:
        logger.info("drop table: %s doesn't exist" % (tname))

# ============================================================
def update_model_2026(model):

    logger.info("=== update_model_2026: begins ===")

    update_PDB_entry(model)
    migrate_user_mmcif_files(model)
    migrate_accession_issue_time(model)
    update_PDB_Entry_Generated_File(model)
    update_PDB_ihm_multi_state_scheme_connectivity(model)
    update_PDB_chem_comp_atom(model)
    
    logger.info("=== update_model_2026: ends ===")

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
    
