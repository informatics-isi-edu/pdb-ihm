"""Workflow steps: process_mmCIF (DEPO), process_Entry_Related_File, export_mmCIF (SUBMIT), generateConformDictionary.

Each step is checked for (a) what it writes back to the processing row, (b) the notification subject,
and (c) cleanup of the per-RID scratch directory.
"""
import os
from unittest import mock

import pytest

from ep_helpers import ep


def last_payload(ermrest):
    return ermrest.update.call_args.kwargs["payload"][0]


@pytest.fixture
def fake_hatrac(monkeypatch):
    """Replace HatracFile in entry_processor with a fake whose download writes a small file."""
    class FakeHatracFile:
        instances = []
        md5_hex = "md5-downloaded"

        def __init__(self, store):
            self.file_path = None
            FakeHatracFile.instances.append(self)

        def download_file(self, url, data_dir, filename, verbose=False, hashes=None):
            self.file_path = os.path.join(data_dir, filename)
            with open(self.file_path, "w") as f:
                f.write("data_x\n")
    monkeypatch.setattr(ep, "HatracFile", FakeHatracFile)
    return FakeHatracFile


# ---------------------------------------------------------------------------
# process_mmCIF
# ---------------------------------------------------------------------------
def test_process_mmcif_same_md5_short_circuits(make_processor, ermrest, fake_hatrac):
    p = make_processor(row={"Last_mmCIF_File_MD5": "md5-new"})
    with mock.patch.object(p, "sendMail") as send:
        p.process_mmCIF()
    assert fake_hatrac.instances == []                      # nothing downloaded
    assert last_payload(ermrest)["Workflow_Status"] == "RECORD READY"
    assert "Same mmCIF file content" in send.call_args.args[1]


def test_process_mmcif_empty_file_is_error(make_processor, ermrest, fake_hatrac):
    p = make_processor(row={"mmCIF_File_Bytes": 0})
    with mock.patch.object(p, "sendMail") as send:
        p.process_mmCIF()
    payload = last_payload(ermrest)
    assert payload["Workflow_Status"] == "ERROR"
    assert payload["Process_Status"] == ep.Process_Status_Terms["ERROR_PROCESSING_UPLOADED_mmCIF_FILE"]
    assert "Empty submitted cif file (submitted.cif)" in payload["Record_Status_Detail"]
    assert send.call_args.args[0] == \
        "1-ABCD DEPO: Error: processing uploaded mmCIF file (depositor@example.org)"


def test_process_mmcif_success(make_processor, ermrest, fake_hatrac, tmp_path):
    p = make_processor()
    with mock.patch.object(p, "getMakeMmcifFile") as make, mock.patch.object(p, "mmcif2json") as to_json, \
         mock.patch.object(p, "loadTablesFromJSON") as load, mock.patch.object(p, "sendMail") as send:
        p.process_mmCIF()

    work = str(tmp_path / "scratch" / "1-ABCD")
    make.assert_called_once_with(f"{work}/1-ABCD_input.cif", f"{work}/1-ABCD_output.cif")
    to_json.assert_called_once_with(f"{work}/1-ABCD_output.cif", f"{work}/1-ABCD_output.json", data_mode="DEPO")
    load.assert_called_once_with(f"{work}/1-ABCD_output.json")
    payload = last_payload(ermrest)
    assert payload["Workflow_Status"] == "RECORD READY"
    assert payload["Process_Status"] == "Success"
    assert payload["Last_mmCIF_File_MD5"] == "md5-downloaded"
    assert "mmCIF_File_MD5" not in payload                 # already set on the row
    assert send.call_args.args[0] == "1-ABCD RECORD READY: Success (depositor@example.org)"
    assert not os.path.exists(work)                         # scratch cleaned up


def test_process_mmcif_fills_missing_md5(make_processor, ermrest, fake_hatrac):
    p = make_processor(row={"mmCIF_File_MD5": None, "Last_mmCIF_File_MD5": "old"})
    with mock.patch.object(p, "getMakeMmcifFile"), mock.patch.object(p, "mmcif2json"), \
         mock.patch.object(p, "loadTablesFromJSON"), mock.patch.object(p, "sendMail"):
        p.process_mmCIF()
    assert last_payload(ermrest)["mmCIF_File_MD5"] == "md5-downloaded"


def test_process_mmcif_subprocess_failure(make_processor, ermrest, fake_hatrac):
    p = make_processor()
    with mock.patch.object(p, "getMakeMmcifFile",
                           side_effect=ep.SubProcessError("make_mmcif failed", details="traceback...")), \
         mock.patch.object(p, "loadTablesFromJSON") as load, mock.patch.object(p, "sendMail"):
        p.process_mmCIF()
    load.assert_not_called()
    payload = last_payload(ermrest)
    assert payload["Workflow_Status"] == "ERROR"
    assert "make_mmcif failed" in payload["Record_Status_Detail"]
    assert "Last_mmCIF_File_MD5" not in payload            # so the same file is retried next time


def test_process_mmcif_truncates_long_error(make_processor, ermrest, fake_hatrac):
    p = make_processor()
    with mock.patch.object(p, "getMakeMmcifFile", side_effect=ep.ProcessingError("x" * 10000)), \
         mock.patch.object(p, "sendMail"):
        p.process_mmCIF()
    assert len(last_payload(ermrest)["Record_Status_Detail"]) <= p.processing_details_limit


def test_process_mmcif_cleans_stale_generated_files(make_processor, ermrest, fake_hatrac):
    p = make_processor()
    p.generated_file_rows = [{"File_MD5": "a"}, {"File_MD5": "b"}]
    with mock.patch.object(p, "getMakeMmcifFile"), mock.patch.object(p, "mmcif2json"), \
         mock.patch.object(p, "loadTablesFromJSON"), mock.patch.object(p, "sendMail"):
        p.process_mmCIF()
    args, kwargs = ermrest.delete.call_args
    assert args[1:3] == ("PDB", "Entry_Generated_File")
    assert kwargs["constraints"] == "Structure_Id=D_1-ABCD/!File_MD5=any(a,b)"


# ---------------------------------------------------------------------------
# process_Entry_Related_File
# ---------------------------------------------------------------------------
@pytest.fixture
def related(make_processor):
    p = make_processor(action="Entry_Related_File")
    p.workflow_status = "DEPO"
    p.hatrac_file = mock.MagicMock(file_path="/tmp/whatever.csv")
    return p


@pytest.mark.parametrize("file_format, delimiter", [("CSV", ","), ("TSV", "\t")])
def test_entry_related_file_success(related, ermrest, file_format, delimiter):
    related.processing_row["File_Format"] = file_format
    with mock.patch.object(related, "loadTableFromCSV") as load, mock.patch.object(related, "sendMail") as send:
        related.process_Entry_Related_File()
    load.assert_called_once_with("/tmp/whatever.csv", delimiter, "ihm_cross_link_list", "D_1-ABCD", "1-FILE",
                                 "depositor@example.org")
    args, kwargs = ermrest.update.call_args
    assert args[2] == "Entry_Related_File"
    assert kwargs["payload"][0] == {"RID": "1-FILE", "Restraint_Workflow_Status": "RECORD READY",
                                    "Restraint_Process_Status": "Success", "Record_Status_Detail": None}
    assert send.call_args.args[0].startswith("1-FILE RECORD READY: ")


def test_entry_related_file_success_subject_matches_other_steps(related):
    """Regression: the success subject used the dict key 'SUCCESS' instead of the term 'Success'."""
    with mock.patch.object(related, "loadTableFromCSV"), mock.patch.object(related, "sendMail") as send:
        related.process_Entry_Related_File()
    assert send.call_args.args[0] == "1-FILE RECORD READY: Success (depositor@example.org)"


def test_entry_related_file_failure_rolls_back_rows(related, ermrest):
    with mock.patch.object(related, "loadTableFromCSV", side_effect=ep.FileError("HEADER ERROR: bad column")), \
         mock.patch.object(related, "sendMail") as send:
        related.process_Entry_Related_File()
    ermrest.delete.assert_called_once()
    assert ermrest.delete.call_args.args[2] == "ihm_cross_link_list"
    assert ermrest.delete.call_args.kwargs["constraints"] == "structure_id=D_1-ABCD&Entry_Related_File=1-FILE"
    payload = ermrest.update.call_args.kwargs["payload"][0]
    assert payload["Restraint_Workflow_Status"] == "ERROR"
    assert payload["Restraint_Process_Status"] == ep.Process_Status_Terms["ERROR_PROCESSING_UPLOADED_RESTRAINT_FILES"]
    assert "HEADER ERROR: bad column" in payload["Record_Status_Detail"]
    assert send.call_args.args[0].startswith("1-FILE DEPO: Error: processing uploaded restraint files")


def test_entry_related_file_cleanup_failure_still_updates_status(related, ermrest):
    ermrest.delete.side_effect = RuntimeError("delete failed")
    with mock.patch.object(related, "loadTableFromCSV", side_effect=ep.FileError("bad")), \
         mock.patch.object(related, "sendMail"):
        with pytest.raises(ep.ErmrestError, match="cleanup restraint table ihm_cross_link_list failed"):
            related.process_Entry_Related_File()
    assert ermrest.update.call_args.kwargs["payload"][0]["Restraint_Workflow_Status"] == "ERROR"


# ---------------------------------------------------------------------------
# export_mmCIF
# ---------------------------------------------------------------------------
@pytest.fixture
def exporter(make_processor, fake_hatrac):
    p = make_processor(row={"Workflow_Status": "SUBMIT"})
    p.workflow_status = "SUBMIT"
    for name in ["getMakeMmcifFile", "exportErmrestData", "exportCIFContent", "validateExportmmCIF",
                 "generateConformDictionary", "sendMail"]:
        setattr(p, name, mock.MagicMock())
    return p


def test_export_mmcif_submit_success(exporter, ermrest, tmp_path):
    result = exporter.export_mmCIF()
    assert result is None                                    # SUBMIT does not hand the file back
    export_fpath = str(tmp_path / "scratch" / "1-ABCD" / "D_1-ABCD.cif")
    exporter.validateExportmmCIF.assert_called_once_with(export_fpath, update_cif=True)
    exporter.generateConformDictionary.assert_called_once_with("D_1-ABCD", "1-ABCD")
    assert last_payload(ermrest) == {"RID": "1-ABCD", "Workflow_Status": "mmCIF CREATED", "Process_Status": "Success",
                                     "Record_Status_Detail": None}


def test_export_mmcif_writes_header(exporter, tmp_path):
    dest = tmp_path / "copy.cif"
    exporter.export_mmCIF(dest_fpath=str(dest))
    assert dest.read_text().startswith("data_D_1-ABCD\n\n#\n_entry.id  D_1-ABCD\n#\n")


def test_export_mmcif_submit_failure_sets_error(exporter, ermrest):
    exporter.validateExportmmCIF.side_effect = ep.ProcessingError("CifCheck error files found")
    exporter.export_mmCIF()
    payload = last_payload(ermrest)
    assert payload["Workflow_Status"] == "ERROR"
    assert payload["Process_Status"] == ep.Process_Status_Terms["ERROR_GENERATING_mmCIF_FILE"]
    assert "CifCheck error files found" in payload["Record_Status_Detail"]
    exporter.generateConformDictionary.assert_not_called()


@pytest.mark.parametrize("status", ["SUBMISSION COMPLETE", "RELEASE READY"])
def test_export_mmcif_intermediate_step_returns_path_and_skips_validation(exporter, ermrest, tmp_path, status):
    exporter.workflow_status = status
    dest = tmp_path / "dest.cif"
    assert exporter.export_mmCIF(dest_fpath=str(dest)).endswith("/D_1-ABCD.cif")
    assert dest.exists()
    exporter.validateExportmmCIF.assert_not_called()
    ermrest.update.assert_not_called()                       # status is the caller's job


def test_export_mmcif_intermediate_step_failure_raises(exporter):
    exporter.workflow_status = "SUBMISSION COMPLETE"
    exporter.exportErmrestData.side_effect = RuntimeError("ermrest down")
    with pytest.raises(ep.ProcessingError, match="unable to export mmCIF file") as exc:
        exporter.export_mmCIF()
    assert "ermrest down" in exc.value.details        # the original error is passed on to the caller


def test_export_mmcif_intermediate_failure_reaches_entry_status(make_processor, ermrest, fake_hatrac):
    """addReleaseRecords (REL) records the export error passed up through ProcessingError.details."""
    p = make_processor(row={"Accession_Code": "9ABC", "Release_Date": "2025-01-08"})
    p.workflow_status = "RELEASE READY"
    p.sendMail = mock.MagicMock()
    p.getMakeMmcifFile = mock.MagicMock(side_effect=RuntimeError("make_mmcif crashed"))
    accession = {"Accession_Code": "9ABC", "PDB_Accession_Code": "9ABC", "PDBDEV_Accession_Code": None,
                 "PDB_Extended_Code": "PDB_00009ABC", "PDB_Code": "9ABC"}
    ermrest.query.side_effect = lambda *a, **k: [accession] if a[2] == "Accession_Code" else []
    p.addReleaseRecords()
    payload = ermrest.update.call_args.kwargs["payload"][0]
    assert payload["Process_Status"] == ep.Process_Status_Terms["ERROR_RELEASING_ENTRY"]
    assert "make_mmcif crashed" in payload["Record_Status_Detail"]


def test_export_mmcif_unknown_workflow_status(exporter):
    exporter.workflow_status = "DEPO"
    with pytest.raises(ep.ProcessingError, match="unknown workflow status: DEPO"):
        exporter.export_mmCIF()


def test_export_mmcif_early_failure_with_dest(exporter, fake_hatrac, tmp_path):
    """Regression: if the download failed and dest_fpath was given, the finally block read export_fpath before
    assignment (UnboundLocalError) and hid the real error."""
    exporter.workflow_status = "SUBMISSION COMPLETE"
    with mock.patch.object(fake_hatrac, "download_file", side_effect=RuntimeError("hatrac 404")):
        with pytest.raises(ep.ProcessingError, match="unable to export mmCIF file"):
            exporter.export_mmCIF(dest_fpath=str(tmp_path / "dest.cif"))
    assert not (tmp_path / "dest.cif").exists()


def test_export_mmcif_submit_early_failure_records_real_error(exporter, fake_hatrac, ermrest):
    with mock.patch.object(fake_hatrac, "download_file", side_effect=RuntimeError("hatrac 404")):
        exporter.export_mmCIF()
    payload = last_payload(ermrest)
    assert payload["Workflow_Status"] == "ERROR"
    assert "hatrac 404" in payload["Record_Status_Detail"]


# ---------------------------------------------------------------------------
# generateConformDictionary
# ---------------------------------------------------------------------------
def test_generate_conform_dictionary_syncs_with_supported(make_processor, ermrest):
    p = make_processor()

    def query(catalog, sname, tname, **kwargs):
        return {
            "Entry_Generated_File": [{"RID": "GF-1"}],
            "Conform_Dictionary": [
                {"RID": "CD-keep", "Category": "mmcif", "Data_Dictionary_RID": "DD-mmcif-5"},
                {"RID": "CD-old", "Category": "ihm", "Data_Dictionary_RID": "DD-ihm-1.0"},
                {"RID": "CD-gone", "Category": "flr", "Data_Dictionary_RID": "DD-flr"},
            ],
            "Supported_Dictionary": [
                {"Data_Dictionary_Category": "mmcif", "Data_Dictionary_RID": "DD-mmcif-5"},
                {"Data_Dictionary_Category": "ihm", "Data_Dictionary_RID": "DD-ihm-1.2"},
                {"Data_Dictionary_Category": "ma", "Data_Dictionary_RID": "DD-ma"},
            ],
        }[tname]
    ermrest.query.side_effect = query
    ermrest.update.side_effect = lambda *a, **k: k["payload"]

    p.generateConformDictionary("D_1-ABCD", "1-ABCD")

    assert ermrest.insert.call_args.kwargs["payload"] == [{"Exported_mmCIF_RID": "GF-1", "Data_Dictionary_RID": "DD-ma"}]
    assert ermrest.delete.call_args.kwargs["constraints"] == "RID=any(CD-gone)"
    assert ermrest.update.call_args.kwargs["payload"] == [
        {"RID": "CD-old", "Exported_mmCIF_RID": "GF-1", "Data_Dictionary_RID": "DD-ihm-1.2"}]


def test_generate_conform_dictionary_no_export(make_processor, ermrest):
    p = make_processor()
    ermrest.query.return_value = []
    with pytest.raises(ep.ProcessingError, match="no export mmCIF file found"):
        p.generateConformDictionary("D_1-ABCD", "1-ABCD")
