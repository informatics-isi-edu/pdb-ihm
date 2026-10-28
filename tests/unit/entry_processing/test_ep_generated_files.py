"""Cleanup of stale Entry_Generated_File rows (EntryProcessor.delete_stale_generated_files) in every step that
uses it, plus the addReleaseRecords accession-code error messages."""
import os
from unittest import mock

import pytest

from ep_helpers import ep

ACCESSION_ROW = {"RID": "AC-1", "Accession_Code": "9ABC", "PDB_Accession_Code": "9ABC",
                 "PDBDEV_Accession_Code": "PDBDEV_00000099", "PDB_Extended_Code": "PDB_00009ABC", "PDB_Code": "9ABC",
                 "Entry": "1-ABCD"}

OK_ROW = {"RID": "1-ABCD", "Workflow_Status": "RECORD READY", "Process_Status": "Success", "Record_Status_Detail": None}
OK = ("Success", "1-ABCD RECORD READY: Success (depositor@example.org)", "changed to RECORD READY", OK_ROW)


def call(p, state=OK):
    process_status, subject, message, row = state
    return p.delete_stale_generated_files(process_status, subject, message, dict(row))


def last_payload(ermrest):
    return ermrest.update.call_args.kwargs["payload"][0]


# ---------------------------------------------------------------------------
# the delete query
# ---------------------------------------------------------------------------
def test_keeps_files_generated_in_this_step(make_processor, ermrest):
    p = make_processor()
    p.workflow_status = "DEPO"
    p.generated_file_rows = [{"File_MD5": "aaa"}, {"File_MD5": "bbb"}]
    call(p)
    args, kwargs = ermrest.delete.call_args
    assert args[1:3] == ("PDB", "Entry_Generated_File")
    assert kwargs["constraints"] == "Structure_Id=D_1-ABCD/!File_MD5=any(aaa,bbb)"


def test_no_files_generated_deletes_all_of_the_entrys_files(make_processor, ermrest):
    p = make_processor()
    p.workflow_status = "DEPO"
    call(p)
    assert ermrest.delete.call_args.kwargs["constraints"] == "Structure_Id=D_1-ABCD"


def test_values_are_url_quoted(make_processor, ermrest):
    p = make_processor()
    p.workflow_status = "DEPO"
    p.entry_id = "D_1 ABCD"
    p.generated_file_rows = [{"File_MD5": "a,b"}]
    call(p)
    assert ermrest.delete.call_args.kwargs["constraints"] == "Structure_Id=D_1%20ABCD/!File_MD5=any(a%2Cb)"


# ---------------------------------------------------------------------------
# return values
# ---------------------------------------------------------------------------
def test_success_returns_state_unchanged(make_processor, ermrest):
    p = make_processor()
    p.workflow_status = "DEPO"
    assert call(p) == OK


@pytest.mark.parametrize("workflow_status, error_status", [
    ("DEPO", "Error: processing uploaded mmCIF file"),
    ("SUBMIT", "Error: generating mmCIF file"),
    ("SUBMISSION COMPLETE", "Error: generating system files"),
    ("RELEASE READY", "Error: releasing entry"),
])
def test_delete_failure_marks_entry_as_error(make_processor, ermrest, workflow_status, error_status):
    p = make_processor()
    p.workflow_status = workflow_status
    ermrest.delete.side_effect = RuntimeError("503 Service Unavailable")
    process_status, subject, message, row = call(p)
    assert process_status == error_status
    assert subject == f"1-ABCD {workflow_status}: {error_status} (depositor@example.org)"
    assert "503 Service Unavailable" in message and "Error occured in delete_stale_generated_files." in message
    assert row == {"RID": "1-ABCD", "Workflow_Status": "ERROR", "Process_Status": error_status,
                   "Record_Status_Detail": "Error occured while deleting stale files."}


def test_delete_failure_keeps_previous_error_detail(make_processor, ermrest):
    p = make_processor()
    p.workflow_status = "DEPO"
    ermrest.delete.side_effect = RuntimeError("503")
    failed = ("Error: processing uploaded mmCIF file", "subj", "msg",
              {"RID": "1-ABCD", "Workflow_Status": "ERROR", "Process_Status": "Error: processing uploaded mmCIF file",
               "Record_Status_Detail": "make_mmcif failed"})
    row = call(p, failed)[3]
    assert row["Record_Status_Detail"] == "Error occured while deleting stale files. Previous error: make_mmcif failed"


def test_error_mapping_covers_every_step_that_cleans_up():
    assert set(ep.Workflow2Status_Error) == {"DEPO", "SUBMIT", "SUBMISSION COMPLETE", "RELEASE READY"}
    assert all(v in ep.Process_Status_Terms.values() and v.startswith("Error:") for v in ep.Workflow2Status_Error.values())


# ---------------------------------------------------------------------------
# each step that cleans up: a failed delete is recorded, not lost
# ---------------------------------------------------------------------------
@pytest.fixture
def fake_hatrac(monkeypatch):
    class FakeHatracFile:
        md5_hex = "md5-downloaded"

        def __init__(self, store):
            self.file_path = None

        def download_file(self, url, data_dir, filename, verbose=False, hashes=None):
            self.file_path = os.path.join(data_dir, filename)
            open(self.file_path, "w").write("data_x\n")
    monkeypatch.setattr(ep, "HatracFile", FakeHatracFile)


def test_process_mmcif_delete_failure(make_processor, ermrest, fake_hatrac):
    p = make_processor()
    p.workflow_status = "DEPO"
    ermrest.delete.side_effect = RuntimeError("503")
    with mock.patch.object(p, "getMakeMmcifFile"), mock.patch.object(p, "mmcif2json"), \
         mock.patch.object(p, "loadTablesFromJSON"), mock.patch.object(p, "sendMail") as send:
        p.process_mmCIF()
    payload = last_payload(ermrest)
    assert (payload["Workflow_Status"], payload["Process_Status"]) == ("ERROR", "Error: processing uploaded mmCIF file")
    assert "Last_mmCIF_File_MD5" not in payload       # so the file is processed again next time
    assert send.call_args.args[0] == "1-ABCD DEPO: Error: processing uploaded mmCIF file (depositor@example.org)"


def test_start_entry_delete_failure(make_processor, ermrest, fake_hatrac):
    """The production path: start() sets workflow_status before process_mmCIF runs the cleanup."""
    p = make_processor()
    ermrest.delete.side_effect = RuntimeError("503")
    with mock.patch.object(p, "getMakeMmcifFile"), mock.patch.object(p, "mmcif2json"), \
         mock.patch.object(p, "loadTablesFromJSON"), mock.patch.object(p, "sendMail"):
        p.start()
    payload = last_payload(ermrest)
    assert (payload["Workflow_Status"], payload["Process_Status"]) == ("ERROR", "Error: processing uploaded mmCIF file")


def test_process_mmcif_failure_and_delete_failure_keeps_both(make_processor, ermrest, fake_hatrac):
    p = make_processor()
    p.workflow_status = "DEPO"
    ermrest.delete.side_effect = RuntimeError("503")
    with mock.patch.object(p, "getMakeMmcifFile", side_effect=ep.SubProcessError("make_mmcif failed")), \
         mock.patch.object(p, "sendMail"):
        p.process_mmCIF()
    detail = last_payload(ermrest)["Record_Status_Detail"]
    assert detail.startswith("Error occured while deleting stale files. Previous error: ")
    assert "make_mmcif failed" in detail


def test_export_mmcif_submit_delete_failure(make_processor, ermrest, fake_hatrac):
    p = make_processor()
    p.workflow_status = "SUBMIT"
    ermrest.delete.side_effect = RuntimeError("503")
    for name in ["getMakeMmcifFile", "exportErmrestData", "exportCIFContent", "validateExportmmCIF",
                 "generateConformDictionary", "sendMail"]:
        setattr(p, name, mock.MagicMock())
    p.export_mmCIF()
    payload = last_payload(ermrest)
    assert (payload["Workflow_Status"], payload["Process_Status"]) == ("ERROR", "Error: generating mmCIF file")


def test_set_accession_code_delete_failure(make_processor, ermrest):
    p = make_processor()
    p.workflow_status = "SUBMISSION COMPLETE"
    ermrest.delete.side_effect = RuntimeError("503")
    with mock.patch.object(p, "getAccessionCode", return_value="9ABC"), mock.patch.object(p, "addReleaseRecords"), \
         mock.patch.object(p, "sendMail") as send:
        p.set_accession_code()
    payload = last_payload(ermrest)
    assert (payload["Workflow_Status"], payload["Process_Status"]) == ("ERROR", "Error: generating system files")
    assert "Accession_Code" not in payload
    assert send.call_args.args[0].startswith("1-ABCD SUBMISSION COMPLETE: Error: generating system files")


def test_set_accession_code_failure_deletes_all_generated_files(make_processor, ermrest):
    """Documents current policy: if HOLD generation fails before any file is regenerated, the files from the
    SUBMIT step are deleted too. Change this test if the policy changes."""
    p = make_processor()
    p.workflow_status = "SUBMISSION COMPLETE"
    with mock.patch.object(p, "getAccessionCode", return_value="9ABC"), \
         mock.patch.object(p, "addReleaseRecords", side_effect=ep.ProcessingError("failed early")), \
         mock.patch.object(p, "sendMail"):
        p.set_accession_code()
    assert ermrest.delete.call_args.kwargs["constraints"] == "Structure_Id=D_1-ABCD"


# ---------------------------------------------------------------------------
# addReleaseRecords (REL): accession-code checks and stale-file cleanup
# ---------------------------------------------------------------------------
@pytest.fixture
def releasing(make_processor, ermrest):
    p = make_processor(row={"Accession_Code": "9ABC", "Release_Date": "2025-01-08"})
    p.workflow_status = "RELEASE READY"
    p.export_mmCIF = mock.MagicMock()
    p.sendMail = mock.MagicMock()
    return p


def test_release_delete_failure(releasing, ermrest):
    ermrest.query.side_effect = lambda *a, **k: [dict(ACCESSION_ROW, Accession_Code="8ZZZ")] \
        if a[2] == "Accession_Code" else []
    ermrest.delete.side_effect = RuntimeError("503")
    releasing.addReleaseRecords()
    payload = last_payload(ermrest)
    assert (payload["Workflow_Status"], payload["Process_Status"]) == ("ERROR", "Error: releasing entry")
    assert "Previous error:" in payload["Record_Status_Detail"]


def test_release_accession_code_mismatch_message(releasing, ermrest):
    """Regression: the message used an undefined name (accesion_code_row), so a NameError was recorded instead."""
    ermrest.query.side_effect = lambda *a, **k: [dict(ACCESSION_ROW, Accession_Code="8ZZZ")] \
        if a[2] == "Accession_Code" else []
    releasing.addReleaseRecords()
    detail = last_payload(ermrest)["Record_Status_Detail"]
    assert "primary_accession_code 9ABC different from Accession_Code column: 8ZZZ" in detail
    assert "NameError" not in detail
    releasing.export_mmCIF.assert_not_called()


@pytest.mark.parametrize("rows", [[], [ACCESSION_ROW, dict(ACCESSION_ROW, RID="AC-2")]])
def test_release_invalid_number_of_accession_codes_message(releasing, ermrest, rows):
    """Regression: '...' %s (...) raised NameError for 's' instead of reporting the count."""
    ermrest.query.side_effect = lambda *a, **k: rows if a[2] == "Accession_Code" else []
    releasing.addReleaseRecords()
    detail = last_payload(ermrest)["Record_Status_Detail"]
    assert f"entry 1-ABCD: Invalid number of accession codes assigned: {len(rows)}" in detail
    assert "NameError" not in detail
