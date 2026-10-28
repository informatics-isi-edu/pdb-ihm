"""EntryProcessor construction, processing-row initialization, and start() dispatch."""
from unittest import mock

import pytest

from ep_helpers import ep, USER_ID, USER_ROW


# ---------------------------------------------------------------------------
# __init__ / initialize_processing_row
# ---------------------------------------------------------------------------
def test_init_entry_action(make_processor, tmp_path):
    p = make_processor()
    assert p.processing_tname == "entry"
    assert (p.entry_id, p.entry_rid) == ("D_1-ABCD", "1-ABCD")
    assert p.user_email == USER_ROW["Email"]
    assert p.user_uuid == USER_ID.rsplit("/", 1)[1]
    assert p.hatrac_generated_prefix == f"/hatrac/pdb/generated/uid/{p.user_uuid}/entry/id/D_1-ABCD"
    assert p.generated_file_rows == []
    assert p.catalog.dcctx["cid"] == "pipeline/pdb"


def test_init_entry_related_file_action(make_processor):
    p = make_processor(action="Entry_Related_File")
    assert p.processing_tname == "Entry_Related_File"
    assert (p.entry_id, p.entry_rid) == ("D_1-ABCD", "1-ABCD")


def test_init_uses_injected_store(make_processor):
    """Regression: EntryProcessor did not forward `store` to the base class, so it always opened a new
    HatracStore connection (and could not be tested offline)."""
    p = make_processor()
    p.store.is_valid_namespace.assert_called()       # the mock store was used for the namespace check


def test_init_creates_user_namespace_when_missing(make_processor):
    store = mock.MagicMock()
    store.is_valid_namespace.return_value = False
    with mock.patch("pdb_dev.processing.processor.set_hatrac_namespace_acl") as acl:
        p = make_processor(store=store)
    namespace = f"/hatrac/pdb/generated/uid/{p.user_uuid}"
    store.create_namespace.assert_called_once_with(namespace, parents=True)
    assert acl.call_args.args[1] == {"subtree-read": [USER_ID]}


def test_init_existing_user_namespace_is_reused(make_processor):
    p = make_processor()
    assert p.store.is_valid_namespace.call_args.args[0] == f"/hatrac/pdb/generated/uid/{p.user_uuid}"
    p.store.create_namespace.assert_not_called()


def test_init_missing_rid_raises(ermrest, make_processor):
    p = make_processor()   # build once so we have a processor to re-initialize
    ermrest.query.return_value = []
    with pytest.raises(Exception, match="does not exist in table entry"):
        p.initialize_processing_row("9-NOPE")


def test_init_validation_dir_suffix(make_processor, tmp_path):
    assert make_processor(validation_dir="/opt/val").validation_dir == "/opt/val/IHMValidation"
    assert make_processor(validation_dir="/opt/IHMValidation").validation_dir == "/opt/IHMValidation"


def test_init_overrides(make_processor):
    p = make_processor(python_bin="/py", py_rcsb_db="/rcsb", CifCheck="/cc", timeout=5,
                       primary_accession_code_mode="PDBDEV", alternative_accession_code_mode="None",
                       singularity_sif="x.sif")
    assert (p.python_bin, p.py_rcsb_db, p.CifCheck, p.timeout) == ("/py", "/rcsb", "/cc", 5)
    assert (p.primary_accession_code_mode, p.alternative_accession_code_mode) == ("PDBDEV", "None")
    assert p.singularity_sif == "x.sif"


def test_status_tables_are_consistent():
    # every next workflow status the processor writes must be a known transition
    assert ep.Next_Workflow_Status == {
        "DEPO": "RECORD READY", "SUBMIT": "mmCIF CREATED", "SUBMISSION COMPLETE": "HOLD",
        "RELEASE READY": "REL", "REL": "REL",
    }
    # each error status has a matching in-progress status family
    assert all(v.startswith(("Error:", "In progress:")) or k in {"NEW", "REPROCESS", "SUCCESS", "RESUME"}
               for k, v in ep.Process_Status_Terms.items())


# ---------------------------------------------------------------------------
# start() dispatch
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("action, method, workflow_status", [
    ("entry", "process_mmCIF", "DEPO"),
    ("Entry_Related_File", "process_Entry_Related_File", "DEPO"),
    ("export", "export_mmCIF", "SUBMIT"),
    ("accession_code", "set_accession_code", "SUBMISSION COMPLETE"),
    ("release_mmCIF", "addReleaseRecords", "RELEASE READY"),
])
def test_start_dispatches_action(make_processor, action, method, workflow_status):
    p = make_processor(action="Entry_Related_File" if action == "Entry_Related_File" else "entry")
    p.action = action
    with mock.patch.object(p, method) as m:
        p.start()
    m.assert_called_once_with()
    assert p.workflow_status == workflow_status


def test_start_unknown_action_notifies_and_raises(make_processor):
    p = make_processor()
    p.action = "bogus"
    with mock.patch.object(p, "sendMail") as send:
        with pytest.raises(ep.ProcessingError, match="unknown action bogus"):
            p.start()
    subject = send.call_args.args[0]
    assert subject.startswith("1-ABCD Unexpected Exception") and "depositor@example.org" in subject


def test_start_reraises_step_exception(make_processor):
    p = make_processor()
    with mock.patch.object(p, "process_mmCIF", side_effect=ValueError("boom")), \
         mock.patch.object(p, "sendMail") as send:
        with pytest.raises(ValueError, match="boom"):
            p.start()
    assert "boom" in send.call_args.args[1]


# ---------------------------------------------------------------------------
# update_processing_row
# ---------------------------------------------------------------------------
def test_update_processing_row_skips_unchanged(make_processor, ermrest):
    p = make_processor()
    row = {"RID": "1-ABCD", "Workflow_Status": "DEPO", "Record_Status_Detail": None}
    assert p.update_processing_row(row) == []
    ermrest.update.assert_not_called()


def test_update_processing_row_updates_changed_columns(make_processor, ermrest):
    p = make_processor()
    row = {"RID": "1-ABCD", "Workflow_Status": "RECORD READY", "Process_Status": "Success", "RMT": "x"}
    p.update_processing_row(row)
    args, kwargs = ermrest.update.call_args
    assert args[1:3] == ("PDB", "entry")
    assert kwargs["payload"] == [row]
    assert kwargs["column_names"] == ["Workflow_Status", "Process_Status"]   # system columns excluded


def test_update_processing_row_explicit_table_and_columns(make_processor, ermrest):
    p = make_processor()
    p.update_processing_row({"RID": "1-ABCD", "Last_mmCIF_File_MD5": "abc", "Other": 1},
                            tname="entry", cnames=["Last_mmCIF_File_MD5"])
    assert ermrest.update.call_args.kwargs["column_names"] == ["Last_mmCIF_File_MD5"]
