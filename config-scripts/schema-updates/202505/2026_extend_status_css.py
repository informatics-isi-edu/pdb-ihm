import json
from deriva.core import ErmrestCatalog, AttrDict, get_credential, DEFAULT_CREDENTIAL_FILE, tag, urlquote, DerivaServer, get_credential, BaseCLI
from deriva.core.ermrest_model import builtin_types, Schema, Table, Column, Key, ForeignKey
from deriva.core import urlquote, urlunquote
from deriva.utils.extras.data import update_table_rows
from pdb_dev.utils.shared import DCCTX, PDBDEV_CLI, cfg


# -- =================================================================================
def update_Vocab_Workflow_Status(catalog):
    """ Update Vocab.Workflow_Status to
      - Create a flag called Entry_Related_File_Status in this vocab table to indicate which Workflow Status can be used
      - Submitter_Select whether to allow submitter to select those values
      - Submitter_Update_Entry Allow the submitters to update the rows
    """
    
    model = catalog.getCatalogModel()    
    schema = model.schemas["Vocab"]
    table = schema.tables["Workflow_Status"]


    if not "Restraint_Submitter_Select" in table.columns.elements:
        table.create_column(
            Column.define(
                "Restraint_Submitter_Select",
                builtin_types.boolean,
                nullok=True,
                comment="A flag indiciating whether to allow Submitters to select during a Related_File (e.g. restraint) editing",                
            )
        )
    
    '''
    select '{ "Name": "'||"Name"||'", "Restraint_Status": None, "PDB_Submitter_Select": None, "Restraint_Submitter_Select": None, },' FROM "Vocab"."Workflow_Status";
    '''
    payload = [
        { "Name": "DRAFT",             "Restraint_Status": True, "Entry_Submitter_Select": True, "Restraint_Submitter_Select": True, },
        { "Name": "DEPO",              "Restraint_Status": True, "Entry_Submitter_Select": True, "Restraint_Submitter_Select": True, },
        { "Name": "RECORD READY",      "Restraint_Status": True, "Entry_Submitter_Select": None, "Restraint_Submitter_Select": None, },
        { "Name": "SUBMIT",            "Restraint_Status": None, "Entry_Submitter_Select": True, "Restraint_Submitter_Select": None, },
        { "Name": "mmCIF CREATED",     "Restraint_Status": None, "Entry_Submitter_Select": None, "Restraint_Submitter_Select": None, },
        { "Name": "SUBMISSION COMPLETE", "Restraint_Status": None, "Entry_Submitter_Select": None, "Restraint_Submitter_Select": None, },
        { "Name": "HOLD",              "Restraint_Status": None, "Entry_Submitter_Select": None, "Restraint_Submitter_Select": None, },
        { "Name": "RELEASE READY",     "Restraint_Status": None, "Entry_Submitter_Select": None, "Restraint_Submitter_Select": None, },
        { "Name": "REL",               "Restraint_Status": None, "Entry_Submitter_Select": None, "Restraint_Submitter_Select": None, },
        { "Name": "ERROR",             "Restraint_Status": True, "Entry_Submitter_Select": None, "Restraint_Submitter_Select": None, },
        { "Name": "ABANDONED",         "Restraint_Status": None, "Entry_Submitter_Select": None, "Restraint_Submitter_Select": None, },
    ]
    print(json.dumps(payload, indent=4))
    
    update_table_rows(catalog, "Vocab", "Workflow_Status", keys=["Name"], column_names=["Restraint_Status", "Entry_Submitter_Select", "Restraint_Submitter_Select"], payload=payload)
        
# -------------------------------------------------------------------------
def update_Vocab_Process_Status(catalog):
    """ Update Vocab.Workflow_Status to
      - Create a flag called Entry_Related_File_Status in this vocab table to indicate which Workflow Status can be used
      - Submitter_Select whether to allow submitter to select those values
      - Submitter_Update_Entry Allow the submitters to update the rows
    """
    model = catalog.getCatalogModel()    
    schema = model.schemas["Vocab"]
    table = schema.tables["Process_Status"]
    

    if not "Entry_Submitter_Select" in table.columns.elements:
        table.create_column(
            Column.define(
                "Entry_Submitter_Select",
                builtin_types.boolean,
                nullok=True,
                comment="A flag indiciating whether to allow Submitters to select during an entry editing",                
            )
        )
    if not "Restraint_Submitter_Select" in table.columns.elements:
        table.create_column(
            Column.define(
                "Restraint_Submitter_Select",
                builtin_types.boolean,
                nullok=True,
                comment="A flag indiciating whether to allow Submitters to select during a Related_File (e.g. restraint) editing",                
            )
        )

    '''
    select '{ "Name": "'||"Name"||'", "Restraint_Status": None, "Entry_Submitter_Select": None, "Restraint_Submitter_Select": None, },' FROM "Vocab"."Process_Status";
    '''
    payload = [
        { "Name": "New (trigger backend process)",                   "Restraint_Status": True, "Entry_Submitter_Select": True, "Restraint_Submitter_Select": True, },
        { "Name": "Reprocess (trigger backend process after Error)", "Restraint_Status": True, "Entry_Submitter_Select": None, "Restraint_Submitter_Select": None, },
        { "Name": "In progress: processing uploaded mmCIF file",     "Restraint_Status": None, "Entry_Submitter_Select": None, "Restraint_Submitter_Select": None, },
        { "Name": "In progress: generating mmCIF file",              "Restraint_Status": None, "Entry_Submitter_Select": None, "Restraint_Submitter_Select": None, },
        { "Name": "In progress: releasing entry",                    "Restraint_Status": None, "Entry_Submitter_Select": None, "Restraint_Submitter_Select": None, },
        { "Name": "Success",                                         "Restraint_Status": True, "Entry_Submitter_Select": None, "Restraint_Submitter_Select": None, },
        { "Name": "Resume (trigger backend process)",                "Restraint_Status": None, "Entry_Submitter_Select": None, "Restraint_Submitter_Select": None, },
        { "Name": "Error: processing uploaded mmCIF file",           "Restraint_Status": None, "Entry_Submitter_Select": None, "Restraint_Submitter_Select": None, },
        { "Name": "Error: generating mmCIF file",                    "Restraint_Status": None, "Entry_Submitter_Select": None, "Restraint_Submitter_Select": None, },
        { "Name": "Error: releasing entry",                          "Restraint_Status": None, "Entry_Submitter_Select": None, "Restraint_Submitter_Select": None, },
        { "Name": "In progress: processing uploaded restraint files", "Restraint_Status": True, "Entry_Submitter_Select": None, "Restraint_Submitter_Select": None, },
        { "Name": "Error: processing uploaded restraint files",      "Restraint_Status": True, "Entry_Submitter_Select": None, "Restraint_Submitter_Select": None, },
        { "Name": "In progress: generating system files",            "Restraint_Status": None, "Entry_Submitter_Select": None, "Restraint_Submitter_Select": None, },
        { "Name": "Error: generating system files",                  "Restraint_Status": None, "Entry_Submitter_Select": None, "Restraint_Submitter_Select": None, },
    ]
    update_table_rows(catalog, "Vocab", "Process_Status", keys=["Name"], column_names=["Restraint_Status", "Entry_Submitter_Select", "Restraint_Submitter_Select"], payload=payload)
        

# -- =================================================================================
        
def main(server_name, catalog_id, credentials):
    server = DerivaServer("https", server_name, credentials)
    catalog = server.connect_ermrest(catalog_id)
    catalog.dcctx["cid"] = DCCTX["acl"]
    #store = HatracStore("https", server_name, credentials)

    update_Vocab_Workflow_Status(catalog)
    update_Vocab_Process_Status(catalog)
    
# -- =================================================================================
# Running the script:
#    python3 2026_extend_status_css.py --host data-dev.pdb-ihm.org --catalog-id 99 
#
if __name__ == "__main__":
    args = PDBDEV_CLI(DCCTX["model"], None, 1).parse_cli()
    credentials = get_credential(args.host, args.credential_file)
    #print("credential: %s" % (credentials))
    main(args.host, args.catalog_id, credentials)

