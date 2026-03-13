# type: ignore
import json
from deriva.core import ErmrestCatalog, AttrDict, get_credential, DEFAULT_CREDENTIAL_FILE, tag, urlquote, DerivaServer, get_credential, BaseCLI
from deriva.core.ermrest_model import builtin_types, Schema, Table, Column, Key, ForeignKey
from deriva.core import urlquote, urlunquote
from deriva.utils.extras.data import update_table_rows
from pdb_dev.utils.shared import DCCTX, PDBDEV_CLI, cfg

CSS_CLASSES = {
    "DEFAULT": ".chaise-record-status-default",
    "DEFAULT_COMPACT": ".chaise-record-status-compact-default",
    "ERROR": ".chaise-record-status-warning",
    "ERROR_COMPACT": ".chaise-record-status-compact-warning",
    "SUCCESS": ".chaise-record-status-success",
    "SUCCESS_COMPACT": ".chaise-record-status-compact-success",
}

# -- =================================================================================
def update_Vocab_Workflow_Status(catalog):
    """ Update Vocab.Workflow_Status to
      - Create a flag called Entry_Related_File_Status in this vocab table to indicate which Workflow Status can be used
      - Submitter_Select whether to allow submitter to select those values
      - Submitter_Update_Entry Allow the submitters to update the rows
      - Add CSS_Class and CSS_Class_compact to show different colors
    """

    model = catalog.getCatalogModel()
    schema = model.schemas["Vocab"]
    table = schema.tables["Workflow_Status"]


    if "Restraint_Submitter_Select" not in table.columns.elements:
        table.create_column(
            Column.define(
                "Restraint_Submitter_Select",
                builtin_types.boolean,
                nullok=True,
                comment="A flag indiciating whether to allow Submitters to select during a Related_File (e.g. restraint) editing",
            )
        )

    if "CSS_Class" not in table.columns.elements:
        table.create_column(
            Column.define(
                "CSS_Class",
                builtin_types.text,
                nullok=False,
                comment="A column to store the CSS class for this Workflow Status, which can be used for coloring the status.",
                default=CSS_CLASSES["DEFAULT"],
            )
        )

    if "CSS_Class_Compact" not in table.columns.elements:
        table.create_column(
            Column.define(
                "CSS_Class_Compact",
                builtin_types.text,
                nullok=False,
                comment="A column to store the CSS class for this Workflow Status, which can be used for coloring the status in compact context.",
                default=CSS_CLASSES["DEFAULT_COMPACT"],
            )
        )

    payload = [
        { "Name": "DRAFT",               "Restraint_Status": True,   "Entry_Submitter_Select": True, "Restraint_Submitter_Select": True, "CSS_Class": CSS_CLASSES["DEFAULT"], "CSS_Class_Compact": CSS_CLASSES["DEFAULT_COMPACT"] },
        { "Name": "DEPO",                "Restraint_Status": True,   "Entry_Submitter_Select": True, "Restraint_Submitter_Select": True, "CSS_Class": CSS_CLASSES["DEFAULT"], "CSS_Class_Compact": CSS_CLASSES["DEFAULT_COMPACT"] },
        { "Name": "RECORD READY",        "Restraint_Status": True,   "Entry_Submitter_Select": None, "Restraint_Submitter_Select": None, "CSS_Class": CSS_CLASSES["SUCCESS"], "CSS_Class_Compact": CSS_CLASSES["SUCCESS_COMPACT"] },
        { "Name": "SUBMIT",              "Restraint_Status": None,   "Entry_Submitter_Select": True, "Restraint_Submitter_Select": None, "CSS_Class": CSS_CLASSES["DEFAULT"], "CSS_Class_Compact": CSS_CLASSES["DEFAULT_COMPACT"] },
        { "Name": "mmCIF CREATED",       "Restraint_Status": None,   "Entry_Submitter_Select": None, "Restraint_Submitter_Select": None, "CSS_Class": CSS_CLASSES["SUCCESS"], "CSS_Class_Compact": CSS_CLASSES["SUCCESS_COMPACT"] },
        { "Name": "SUBMISSION COMPLETE", "Restraint_Status": None,   "Entry_Submitter_Select": None, "Restraint_Submitter_Select": None, "CSS_Class": CSS_CLASSES["DEFAULT"], "CSS_Class_Compact": CSS_CLASSES["DEFAULT_COMPACT"] },
        { "Name": "HOLD",                "Restraint_Status": None,   "Entry_Submitter_Select": None, "Restraint_Submitter_Select": None, "CSS_Class": CSS_CLASSES["DEFAULT"], "CSS_Class_Compact": CSS_CLASSES["DEFAULT_COMPACT"] },
        { "Name": "RELEASE READY",       "Restraint_Status": None,   "Entry_Submitter_Select": None, "Restraint_Submitter_Select": None, "CSS_Class": CSS_CLASSES["DEFAULT"], "CSS_Class_Compact": CSS_CLASSES["DEFAULT_COMPACT"] },
        { "Name": "REL",                 "Restraint_Status": None,   "Entry_Submitter_Select": None, "Restraint_Submitter_Select": None, "CSS_Class": CSS_CLASSES["DEFAULT"], "CSS_Class_Compact": CSS_CLASSES["DEFAULT_COMPACT"] },
        { "Name": "ERROR",               "Restraint_Status": True,   "Entry_Submitter_Select": None, "Restraint_Submitter_Select": None, "CSS_Class": CSS_CLASSES["ERROR"],   "CSS_Class_Compact": CSS_CLASSES["ERROR_COMPACT"]   },
        { "Name": "ABANDONED",           "Restraint_Status": None,   "Entry_Submitter_Select": None, "Restraint_Submitter_Select": None, "CSS_Class": CSS_CLASSES["DEFAULT"], "CSS_Class_Compact": CSS_CLASSES["DEFAULT_COMPACT"] },
    ]
    print(json.dumps(payload, indent=4))

    update_table_rows(
        catalog,
        "Vocab",
        "Workflow_Status",
        keys=["Name"],
        column_names=["Restraint_Status", "Entry_Submitter_Select", "Restraint_Submitter_Select", "CSS_Class", "CSS_Class_Compact"],
        payload=payload
    )

# -------------------------------------------------------------------------
def update_Vocab_Process_Status(catalog):
    """ Update Vocab.Workflow_Status to
      - Create a flag called Entry_Related_File_Status in this vocab table to indicate which Workflow Status can be used
      - Submitter_Select whether to allow submitter to select those values
      - Submitter_Update_Entry Allow the submitters to update the rows
      - Add CSS_Class and CSS_Class_compact to show different colors
    """
    model = catalog.getCatalogModel()
    schema = model.schemas["Vocab"]
    table = schema.tables["Process_Status"]


    if "Entry_Submitter_Select" not in table.columns.elements:
        table.create_column(
            Column.define(
                "Entry_Submitter_Select",
                builtin_types.boolean,
                nullok=True,
                comment="A flag indiciating whether to allow Submitters to select during an entry editing",
            )
        )
    if "Restraint_Submitter_Select" not in table.columns.elements:
        table.create_column(
            Column.define(
                "Restraint_Submitter_Select",
                builtin_types.boolean,
                nullok=True,
                comment="A flag indiciating whether to allow Submitters to select during a Related_File (e.g. restraint) editing",
            )
        )

    if "CSS_Class" not in table.columns.elements:
        table.create_column(
            Column.define(
                "CSS_Class",
                builtin_types.text,
                nullok=False,
                comment="A column to store the CSS class for this Process Status, which can be used for coloring the status.",
                default=CSS_CLASSES["DEFAULT"],
            )
        )

    if "CSS_Class_Compact" not in table.columns.elements:
        table.create_column(
            Column.define(
                "CSS_Class_Compact",
                builtin_types.text,
                nullok=False,
                comment="A column to store the CSS class for this Process Status, which can be used for coloring the status in compact context.",
                default=CSS_CLASSES["DEFAULT_COMPACT"],
            )
        )

    payload = [
        { "Name": "New (trigger backend process)",                    "Restraint_Status": True, "Entry_Submitter_Select": True, "Restraint_Submitter_Select": True, "CSS_Class": CSS_CLASSES["DEFAULT"], "CSS_Class_Compact": CSS_CLASSES["DEFAULT_COMPACT"] },
        { "Name": "Reprocess (trigger backend process after Error)",  "Restraint_Status": True, "Entry_Submitter_Select": None, "Restraint_Submitter_Select": None, "CSS_Class": CSS_CLASSES["DEFAULT"], "CSS_Class_Compact": CSS_CLASSES["DEFAULT_COMPACT"] },
        { "Name": "In progress: processing uploaded mmCIF file",      "Restraint_Status": None, "Entry_Submitter_Select": None, "Restraint_Submitter_Select": None, "CSS_Class": CSS_CLASSES["DEFAULT"], "CSS_Class_Compact": CSS_CLASSES["DEFAULT_COMPACT"] },
        { "Name": "In progress: generating mmCIF file",               "Restraint_Status": None, "Entry_Submitter_Select": None, "Restraint_Submitter_Select": None, "CSS_Class": CSS_CLASSES["DEFAULT"], "CSS_Class_Compact": CSS_CLASSES["DEFAULT_COMPACT"] },
        { "Name": "In progress: releasing entry",                     "Restraint_Status": None, "Entry_Submitter_Select": None, "Restraint_Submitter_Select": None, "CSS_Class": CSS_CLASSES["DEFAULT"], "CSS_Class_Compact": CSS_CLASSES["DEFAULT_COMPACT"] },
        { "Name": "Success",                                          "Restraint_Status": True, "Entry_Submitter_Select": None, "Restraint_Submitter_Select": None, "CSS_Class": CSS_CLASSES["SUCCESS"], "CSS_Class_Compact": CSS_CLASSES["SUCCESS_COMPACT"] },
        { "Name": "Resume (trigger backend process)",                 "Restraint_Status": None, "Entry_Submitter_Select": None, "Restraint_Submitter_Select": None, "CSS_Class": CSS_CLASSES["DEFAULT"], "CSS_Class_Compact": CSS_CLASSES["DEFAULT_COMPACT"] },
        { "Name": "Error: processing uploaded mmCIF file",            "Restraint_Status": None, "Entry_Submitter_Select": None, "Restraint_Submitter_Select": None, "CSS_Class": CSS_CLASSES["ERROR"],   "CSS_Class_Compact": CSS_CLASSES["ERROR_COMPACT"]   },
        { "Name": "Error: generating mmCIF file",                     "Restraint_Status": None, "Entry_Submitter_Select": None, "Restraint_Submitter_Select": None, "CSS_Class": CSS_CLASSES["ERROR"],   "CSS_Class_Compact": CSS_CLASSES["ERROR_COMPACT"]   },
        { "Name": "Error: releasing entry",                           "Restraint_Status": None, "Entry_Submitter_Select": None, "Restraint_Submitter_Select": None, "CSS_Class": CSS_CLASSES["ERROR"],   "CSS_Class_Compact": CSS_CLASSES["ERROR_COMPACT"]   },
        { "Name": "In progress: processing uploaded restraint files", "Restraint_Status": True, "Entry_Submitter_Select": None, "Restraint_Submitter_Select": None, "CSS_Class": CSS_CLASSES["DEFAULT"], "CSS_Class_Compact": CSS_CLASSES["DEFAULT_COMPACT"] },
        { "Name": "Error: processing uploaded restraint files",       "Restraint_Status": True, "Entry_Submitter_Select": None, "Restraint_Submitter_Select": None, "CSS_Class": CSS_CLASSES["ERROR"],   "CSS_Class_Compact": CSS_CLASSES["ERROR_COMPACT"]   },
        { "Name": "In progress: generating system files",             "Restraint_Status": None, "Entry_Submitter_Select": None, "Restraint_Submitter_Select": None, "CSS_Class": CSS_CLASSES["DEFAULT"], "CSS_Class_Compact": CSS_CLASSES["DEFAULT_COMPACT"] },
        { "Name": "Error: generating system files",                   "Restraint_Status": None, "Entry_Submitter_Select": None, "Restraint_Submitter_Select": None, "CSS_Class": CSS_CLASSES["ERROR"],   "CSS_Class_Compact": CSS_CLASSES["ERROR_COMPACT"]   },
    ]
    
    update_table_rows(
        catalog,
        "Vocab",
        "Process_Status",
        keys=["Name"],
        column_names=["Restraint_Status", "Entry_Submitter_Select", "Restraint_Submitter_Select", "CSS_Class", "CSS_Class_Compact"],
        payload=payload,
    )


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

