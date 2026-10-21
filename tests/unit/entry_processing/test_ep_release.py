"""Accession codes, database_2 records, and the HOLD / REL release steps (set_accession_code, addReleaseRecords)."""
from unittest import mock

import pytest

from ep_helpers import ep

ACCESSION_ROW = {
    "RID": "AC-1", "Accession_Code": "9ABC", "PDB_Accession_Code": "9ABC", "PDBDEV_Accession_Code": "PDBDEV_00000099",
    "PDB_Extended_Code": "PDB_00009ABC", "PDB_Code": "9ABC", "Entry": "1-ABCD", "Accession_Serial": 10,
}


# ---------------------------------------------------------------------------
# accession-code helpers
# ---------------------------------------------------------------------------
def test_get_primary_accession_code(make_processor):
    p = make_processor()
    assert p.get_primary_accession_code("PDB", ACCESSION_ROW) == "9ABC"
    assert p.get_primary_accession_code("PDBDEV", ACCESSION_ROW) == "PDBDEV_00000099"


@pytest.mark.parametrize("value, expected", [
    ("PDB_00009ABC", "pdb_00009abc"),
    ("9ABC", "9abc"),
    ("TEST-PDB_00009ABC", "TEST-pdb_00009abc"),   # TEST- prefix keeps its case
])
def test_get_lower_accession_code(make_processor, value, expected):
    assert make_processor().get_lower_accession_code(value) == expected


def test_get_database_2_string_pdb(make_processor):
    assert make_processor().get_database_2_string("PDB", ACCESSION_ROW) == \
        "PDB 9ABC pdb_00009abc 10.2210/pdb9abc/pdb"


def test_get_database_2_string_pdbdev(make_processor):
    assert make_processor().get_database_2_string("PDBDEV", ACCESSION_ROW) == \
        "PDB-Dev PDBDEV_00000099 PDBDEV_00000099 ?"


def test_get_database_2_string_pdbdev_missing_and_none_mode(make_processor):
    p = make_processor()
    assert p.get_database_2_string("PDBDEV", dict(ACCESSION_ROW, PDBDEV_Accession_Code=None)) is None
    assert p.get_database_2_string("None", ACCESSION_ROW) == "#"


def test_database_2_accession_code_appends_rows(make_processor):
    p = make_processor()
    assert p.database_2_accession_code("HDR\n", "PDB a b c", None) == "HDR\nPDB a b c\n#\n"
    assert p.database_2_accession_code("HDR\n", "P", "Q") == "HDR\nP\nQ\n#\n"


# ---------------------------------------------------------------------------
# getAccessionCode / assignAccessionCode
# ---------------------------------------------------------------------------
def test_get_accession_code_returns_existing(make_processor, ermrest):
    p = make_processor()
    ermrest.query.return_value = [ACCESSION_ROW]
    assert p.getAccessionCode("1-ABCD") == "9ABC"
    ermrest.update.assert_not_called()


def test_get_accession_code_assigns_next_free_code(make_processor, ermrest):
    p = make_processor()
    free = dict(ACCESSION_ROW, Entry=None, Accession_Code="9XYZ")
    ermrest.query.side_effect = [[], [free]]       # no code assigned yet -> next free one
    assert p.getAccessionCode("1-ABCD") == "9XYZ"
    second_query = ermrest.query.call_args_list[1]
    assert second_query.kwargs["constraints"] == "Entry::null::"
    assert second_query.kwargs["sort"] == ["Accession_Serial"] and second_query.kwargs["limit"] == 1
    assert ermrest.update.call_args.kwargs["payload"][0]["Entry"] == "1-ABCD"
    assert ermrest.update.call_args.kwargs["column_names"] == ["Entry"]


def test_assign_accession_code_none_available(make_processor, ermrest):
    p = make_processor()
    ermrest.query.return_value = []
    with pytest.raises(ep.ErmrestError, match="No PDB accession code is available"):
        p.assignAccessionCode("1-ABCD")


@pytest.mark.xfail(strict=True, reason="if an entry already has >1 accession codes, getAccessionCode silently "
                                       "assigns yet another one instead of raising")
def test_get_accession_code_multiple_assigned_raises(make_processor, ermrest):
    p = make_processor()
    ermrest.query.side_effect = [[ACCESSION_ROW, dict(ACCESSION_ROW, RID="AC-2")], [dict(ACCESSION_ROW, Entry=None)]]
    with pytest.raises(Exception):
        p.getAccessionCode("1-ABCD")


# ---------------------------------------------------------------------------
# addReleaseRecords
# ---------------------------------------------------------------------------
EXPORTED_CIF = """data_D_1-ABCD

#
_entry.id  D_1-ABCD
#
_struct.entry_id\tD_1-ABCD
_struct.title\t"A title"
#
loop_
_audit_conform.dict_name
_audit_conform.dict_version
mmcif_pdbx.dic 5.0
ihm-extension.dic 1.0
#
_ihm_model_list.model_id\t1
#
"""


@pytest.fixture
def release(make_processor, ermrest, monkeypatch):
    """A processor ready for addReleaseRecords with every external step mocked.
    `captured["final"]` holds the content of the final cif when validateExportmmCIF is called."""
    p = make_processor(row={"Accession_Code": "9ABC", "Workflow_Status": "SUBMISSION COMPLETE"})
    captured = {}

    def fake_export(dest_fpath):
        with open(dest_fpath, "w") as f:
            f.write(EXPORTED_CIF)
        return dest_fpath

    def fake_validate(fpath, update_cif=True):
        with open(fpath) as f:
            captured["final"] = f.read()
        captured["final_fpath"] = fpath

    def query(catalog, sname, tname, **kwargs):
        if tname == "Accession_Code":
            return [ACCESSION_ROW]
        return []          # no collections
    ermrest.query.side_effect = query

    for name, impl in [("export_mmCIF", fake_export), ("validateExportmmCIF", fake_validate),
                       ("generateConformDictionary", None), ("generate_ihmv_reports", None),
                       ("generate_PDB_JSON", None), ("sendMail", None)]:
        monkeypatch.setattr(p, name, mock.MagicMock(side_effect=impl))
    p.alternative_accession_code_mode = "None"
    return p, captured


def test_add_release_records_hold(release, ermrest):
    p, captured = release
    p.workflow_status = "SUBMISSION COMPLETE"
    p.addReleaseRecords()

    final = captured["final"]
    assert captured["final_fpath"].endswith("/9ABC.cif")
    assert final.startswith("data_9ABC\n")
    assert "_entry.id  9ABC\n" in final
    assert "_struct.entry_id\t9ABC\n" in final
    assert "_struct.title\t\"A title\"\n" in final                      # other _struct lines untouched
    # release block is inserted right after the _audit_conform loop
    after_conform = final.split("ihm-extension.dic 1.0\n#\n", 1)[1]
    assert after_conform.startswith("_pdbx_database_status.status_code                     HOLD\n")
    assert "_pdbx_database_status.entry_id                        9ABC" in after_conform
    assert "_pdbx_database_status.recvd_initial_deposition_date   2025-01-02" in after_conform
    assert "PDB 9ABC pdb_00009abc 10.2210/pdb9abc/pdb\n#\n#\n" in after_conform
    assert "_pdbx_audit_revision_history" not in final                  # HOLD has no revision history

    p.generate_ihmv_reports.assert_called_once_with(captured["final_fpath"])
    p.generate_PDB_JSON.assert_called_once()
    assert p.generate_PDB_JSON.call_args.args[1].endswith("/9ABC.json")
    ermrest.update.assert_not_called()          # HOLD status is written by set_accession_code, not here


def test_add_release_records_rel_sets_release_date(release, ermrest):
    p, captured = release
    p.workflow_status = "RELEASE READY"
    with mock.patch.object(p, "get_release_datetime_utc") as rel:
        rel.return_value.strftime.return_value = "2025-01-08"
        p.addReleaseRecords()

    assert "_pdbx_database_status.status_code                     REL" in captured["final"]
    assert "1 'Structure model' 1 0 2025-01-08" in captured["final"]
    payload = ermrest.update.call_args.kwargs["payload"][0]
    assert payload["Workflow_Status"] == "REL"
    assert payload["Process_Status"] == "Success"
    assert payload["Release_Date"] == "2025-01-08"
    p.sendMail.assert_called_once()
    assert p.sendMail.call_args.args[0] == "1-ABCD REL: Success (depositor@example.org)"


def test_add_release_records_rel_keeps_existing_release_date(release, ermrest):
    p, captured = release
    p.processing_row["Release_Date"] = "2024-12-31"
    p.workflow_status = "RELEASE READY"
    p.addReleaseRecords()
    assert "1 'Structure model' 1 0 2024-12-31" in captured["final"]
    assert "Release_Date" not in ermrest.update.call_args.kwargs["payload"][0]


def test_add_release_records_rel_failure_sets_error_status(release, ermrest):
    p, _ = release
    p.workflow_status = "RELEASE READY"
    p.processing_row["Release_Date"] = "2024-12-31"
    p.generate_ihmv_reports.side_effect = ep.SubProcessError("ihmv crashed", details="stderr...")
    p.addReleaseRecords()     # error is recorded, not raised, for the final step
    payload = ermrest.update.call_args.kwargs["payload"][0]
    assert payload["Workflow_Status"] == "ERROR"
    assert payload["Process_Status"] == ep.Process_Status_Terms["ERROR_RELEASING_ENTRY"]
    assert "ihmv crashed" in payload["Record_Status_Detail"]
    assert p.sendMail.call_args.args[0] == \
        "1-ABCD RELEASE READY: Error: releasing entry (depositor@example.org)"


def test_add_release_records_hold_failure_is_reraised(release, ermrest):
    p, _ = release
    p.workflow_status = "SUBMISSION COMPLETE"
    p.generate_ihmv_reports.side_effect = ep.SubProcessError("ihmv crashed", details="stderr...")
    with pytest.raises(ep.ProcessingError, match="FAILED while executing a subprocess") as exc:
        p.addReleaseRecords()
    assert exc.value.details == "stderr..."
    ermrest.update.assert_not_called()


def test_add_release_records_accession_mismatch(release, ermrest):
    p, _ = release
    ermrest.query.side_effect = lambda *a, **k: [dict(ACCESSION_ROW, Accession_Code="8ZZZ")]
    p.workflow_status = "SUBMISSION COMPLETE"
    with pytest.raises(ep.ProcessingError, match="FAILED"):
        p.addReleaseRecords()
    p.export_mmCIF.assert_not_called()


def test_add_release_records_cleans_processing_dir(release, tmp_path):
    p, _ = release
    p.workflow_status = "SUBMISSION COMPLETE"
    p.addReleaseRecords()
    assert not (tmp_path / "scratch" / "1-ABCD").exists()


# ---------------------------------------------------------------------------
# set_accession_code
# ---------------------------------------------------------------------------
def test_set_accession_code_success(make_processor, ermrest):
    p = make_processor(row={"Workflow_Status": "SUBMISSION COMPLETE"})
    p.workflow_status = "SUBMISSION COMPLETE"
    with mock.patch.object(p, "getAccessionCode", return_value="9ABC"), \
         mock.patch.object(p, "addReleaseRecords") as add, mock.patch.object(p, "sendMail"):
        p.set_accession_code()
    add.assert_called_once()
    assert p.processing_row["Accession_Code"] == "9ABC"     # made available to addReleaseRecords
    payload = ermrest.update.call_args.kwargs["payload"][0]
    assert payload == {"RID": "1-ABCD", "Workflow_Status": "HOLD", "Process_Status": "Success",
                       "Record_Status_Detail": None, "Accession_Code": "9ABC"}


def test_set_accession_code_reuses_existing(make_processor):
    p = make_processor(row={"Accession_Code": "9OLD"})
    p.workflow_status = "SUBMISSION COMPLETE"
    with mock.patch.object(p, "getAccessionCode") as get, mock.patch.object(p, "addReleaseRecords"), \
         mock.patch.object(p, "sendMail"):
        p.set_accession_code()
    get.assert_not_called()


def test_set_accession_code_failure(make_processor, ermrest):
    p = make_processor()
    p.workflow_status = "SUBMISSION COMPLETE"
    with mock.patch.object(p, "getAccessionCode", return_value="9ABC"), \
         mock.patch.object(p, "addReleaseRecords", side_effect=ep.ProcessingError("export broke")), \
         mock.patch.object(p, "sendMail") as send:
        p.set_accession_code()
    payload = ermrest.update.call_args.kwargs["payload"][0]
    assert payload["Workflow_Status"] == "ERROR"
    assert payload["Process_Status"] == ep.Process_Status_Terms["ERROR_GENERATING_SYSTEM_FILES"]
    assert "export broke" in payload["Record_Status_Detail"]
    assert "Accession_Code" not in payload
    assert send.call_args.args[0].startswith("1-ABCD SUBMISSION COMPLETE: Error: generating system files")
