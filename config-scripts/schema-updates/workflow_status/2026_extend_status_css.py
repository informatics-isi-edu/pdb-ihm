
from deriva.core import get_credential, DerivaServer
from deriva.core.ermrest_model import builtin_types, Column
from deriva.utils.extras.data import update_table_rows
from pdb_dev.utils.shared import DCCTX, PDBDEV_CLI

CSS_CLASSES = {
    "DEFAULT": ".chaise-record-status-default",
    "DEFAULT_COMPACT": ".chaise-record-status-compact-default",
    "ERROR": ".chaise-record-status-danger",
    "ERROR_COMPACT": ".chaise-record-status-compact-danger",
    "SUCCESS": ".chaise-record-status-success",
    "SUCCESS_COMPACT": ".chaise-record-status-compact-success",
}

# -- =================================================================================
def update_Vocab_Workflow_Status(catalog):
    """ Update Vocab.Workflow_Status to
      - Add CSS_Class and CSS_Class_compact to show different colors
    """

    model = catalog.getCatalogModel()
    schema = model.schemas["Vocab"]
    table = schema.tables["Workflow_Status"]

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
        { "Name": "DRAFT",               "CSS_Class": CSS_CLASSES["DEFAULT"], "CSS_Class_Compact": CSS_CLASSES["DEFAULT_COMPACT"] },
        { "Name": "DEPO",                "CSS_Class": CSS_CLASSES["DEFAULT"], "CSS_Class_Compact": CSS_CLASSES["DEFAULT_COMPACT"] },
        { "Name": "RECORD READY",        "CSS_Class": CSS_CLASSES["SUCCESS"], "CSS_Class_Compact": CSS_CLASSES["SUCCESS_COMPACT"] },
        { "Name": "SUBMIT",              "CSS_Class": CSS_CLASSES["DEFAULT"], "CSS_Class_Compact": CSS_CLASSES["DEFAULT_COMPACT"] },
        { "Name": "mmCIF CREATED",       "CSS_Class": CSS_CLASSES["SUCCESS"], "CSS_Class_Compact": CSS_CLASSES["SUCCESS_COMPACT"] },
        { "Name": "SUBMISSION COMPLETE", "CSS_Class": CSS_CLASSES["DEFAULT"], "CSS_Class_Compact": CSS_CLASSES["DEFAULT_COMPACT"] },
        { "Name": "HOLD",                "CSS_Class": CSS_CLASSES["DEFAULT"], "CSS_Class_Compact": CSS_CLASSES["DEFAULT_COMPACT"] },
        { "Name": "RELEASE READY",       "CSS_Class": CSS_CLASSES["DEFAULT"], "CSS_Class_Compact": CSS_CLASSES["DEFAULT_COMPACT"] },
        { "Name": "REL",                 "CSS_Class": CSS_CLASSES["DEFAULT"], "CSS_Class_Compact": CSS_CLASSES["DEFAULT_COMPACT"] },
        { "Name": "ERROR",               "CSS_Class": CSS_CLASSES["ERROR"],   "CSS_Class_Compact": CSS_CLASSES["ERROR_COMPACT"]   },
        { "Name": "ABANDONED",           "CSS_Class": CSS_CLASSES["DEFAULT"], "CSS_Class_Compact": CSS_CLASSES["DEFAULT_COMPACT"] },
    ]

    update_table_rows(
        catalog,
        "Vocab",
        "Workflow_Status",
        keys=["Name"],
        column_names=["CSS_Class", "CSS_Class_Compact"],
        payload=payload
    )

# -------------------------------------------------------------------------
def update_Vocab_Process_Status(catalog):
    """ Update Vocab.Workflow_Status to
      - Add CSS_Class and CSS_Class_compact that are used by row-name to show different colors
    """
    model = catalog.getCatalogModel()
    schema = model.schemas["Vocab"]
    table = schema.tables["Process_Status"]

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
        { "Name": "New (trigger backend process)",                    "CSS_Class": CSS_CLASSES["DEFAULT"], "CSS_Class_Compact": CSS_CLASSES["DEFAULT_COMPACT"] },
        { "Name": "Reprocess (trigger backend process after Error)",  "CSS_Class": CSS_CLASSES["DEFAULT"], "CSS_Class_Compact": CSS_CLASSES["DEFAULT_COMPACT"] },
        { "Name": "In progress: processing uploaded mmCIF file",      "CSS_Class": CSS_CLASSES["DEFAULT"], "CSS_Class_Compact": CSS_CLASSES["DEFAULT_COMPACT"] },
        { "Name": "In progress: generating mmCIF file",               "CSS_Class": CSS_CLASSES["DEFAULT"], "CSS_Class_Compact": CSS_CLASSES["DEFAULT_COMPACT"] },
        { "Name": "In progress: releasing entry",                     "CSS_Class": CSS_CLASSES["DEFAULT"], "CSS_Class_Compact": CSS_CLASSES["DEFAULT_COMPACT"] },
        { "Name": "Success",                                          "CSS_Class": CSS_CLASSES["SUCCESS"], "CSS_Class_Compact": CSS_CLASSES["SUCCESS_COMPACT"] },
        { "Name": "Resume (trigger backend process)",                 "CSS_Class": CSS_CLASSES["DEFAULT"], "CSS_Class_Compact": CSS_CLASSES["DEFAULT_COMPACT"] },
        { "Name": "Error: processing uploaded mmCIF file",            "CSS_Class": CSS_CLASSES["ERROR"],   "CSS_Class_Compact": CSS_CLASSES["ERROR_COMPACT"]   },
        { "Name": "Error: generating mmCIF file",                     "CSS_Class": CSS_CLASSES["ERROR"],   "CSS_Class_Compact": CSS_CLASSES["ERROR_COMPACT"]   },
        { "Name": "Error: releasing entry",                           "CSS_Class": CSS_CLASSES["ERROR"],   "CSS_Class_Compact": CSS_CLASSES["ERROR_COMPACT"]   },
        { "Name": "In progress: processing uploaded restraint files", "CSS_Class": CSS_CLASSES["DEFAULT"], "CSS_Class_Compact": CSS_CLASSES["DEFAULT_COMPACT"] },
        { "Name": "Error: processing uploaded restraint files",       "CSS_Class": CSS_CLASSES["ERROR"],   "CSS_Class_Compact": CSS_CLASSES["ERROR_COMPACT"]   },
        { "Name": "In progress: generating system files",             "CSS_Class": CSS_CLASSES["DEFAULT"], "CSS_Class_Compact": CSS_CLASSES["DEFAULT_COMPACT"] },
        { "Name": "Error: generating system files",                   "CSS_Class": CSS_CLASSES["ERROR"],   "CSS_Class_Compact": CSS_CLASSES["ERROR_COMPACT"]   },
    ]
    
    update_table_rows(
        catalog,
        "Vocab",
        "Process_Status",
        keys=["Name"],
        column_names=["CSS_Class", "CSS_Class_Compact"],
        payload=payload,
    )


# -- =================================================================================

def main(server_name, catalog_id, credentials):
    server = DerivaServer("https", server_name, credentials)
    catalog = server.connect_ermrest(catalog_id)
    catalog.dcctx["cid"] = DCCTX["model"]

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

