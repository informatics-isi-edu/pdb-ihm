"""Wrappers around external tools: make_mmcif, py-rcsb_db (mmcif2json), CifCheck (validateExportmmCIF),
IHMValidation (generate_ihmv_reports), plus fname2ftype and generate_PDB_JSON. subprocess.Popen is mocked;
tests check the command line, return-code handling and the ERMrest bookkeeping around each tool."""
import os
import subprocess
from types import SimpleNamespace
from unittest import mock

import pytest

from ep_helpers import ep


def fake_popen(returncode=0, stdout=b"out", stderr=b"err", on_run=None, timeout_exc=False):
    """Return a Popen replacement. `on_run(args)` can create files the tool would produce."""
    calls = []

    def _popen(args, stdout=None, stderr=None):
        calls.append(args)
        if on_run:
            on_run(args)
        proc = mock.MagicMock(returncode=returncode)
        if timeout_exc:
            proc.communicate.side_effect = subprocess.TimeoutExpired(args, 1)
        else:
            proc.communicate.return_value = (stdout_data, stderr_data)
        return proc
    stdout_data, stderr_data = stdout, stderr
    _popen.calls = calls
    return _popen


def hatrac_file(path):
    name = os.path.basename(path)
    return SimpleNamespace(hatrac_url=f"/hatrac/x/{name}", file_name=name, md5_hex=f"md5-{name}", file_bytes=10)


@pytest.fixture
def proc(make_processor, monkeypatch):
    p = make_processor(python_bin="/usr/bin/python3", CifCheck="/bin/CifCheck", dictSdb="/dict.sdb",
                       py_rcsb_db="/opt/rcsb", timeout=2)
    # upload_file_groups -> one fake HatracFile per matching file actually present on disk
    def upload(data_dir, filters, namespace_prefix=None, file_prefix=None):
        names = sorted(f for f in os.listdir(data_dir) if any(flt in f for flt in filters))
        return [hatrac_file(os.path.join(data_dir, n)) for n in names]
    monkeypatch.setattr(p, "upload_file_groups", mock.MagicMock(side_effect=upload))
    return p


# ---------------------------------------------------------------------------
# getMakeMmcifFile
# ---------------------------------------------------------------------------
def test_get_make_mmcif_file_command(proc, tmp_path, monkeypatch):
    out = tmp_path / "out.cif"
    out.write_text("stale")
    popen = fake_popen()
    monkeypatch.setattr(ep.subprocess, "Popen", popen)
    assert proc.getMakeMmcifFile(str(tmp_path / "in.cif"), str(out)) == str(out)
    assert popen.calls == [["/usr/bin/python3", "-m", "ihm.util.make_mmcif", "--histidines",
                            str(tmp_path / "in.cif"), str(out)]]
    assert not out.exists()          # stale output removed before running


def test_get_make_mmcif_file_failure(proc, tmp_path, monkeypatch):
    monkeypatch.setattr(ep.subprocess, "Popen", fake_popen(returncode=1, stderr=b"bad cif"))
    with pytest.raises(ep.SubProcessError, match="(?s)make_mmcif failed for entry rid = \"1-ABCD\".*bad cif"):
        proc.getMakeMmcifFile(str(tmp_path / "in.cif"), str(tmp_path / "out.cif"))


def test_get_make_mmcif_file_real_tool(proc, tmp_path):
    """Runs the real python-ihm make_mmcif on a minimal file (no mocks) to catch CLI changes upstream."""
    import sys
    src = tmp_path / "in.cif"
    src.write_text("data_model\n_entry.id model\n_struct.entry_id model\n_struct.title 'x'\n")
    proc.python_bin = sys.executable
    out = proc.getMakeMmcifFile(str(src), str(tmp_path / "out.cif"))
    assert "_entry.id" in open(out).read()


# ---------------------------------------------------------------------------
# mmcif2json
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("mode, config, cache", [
    ("DEPO", "exdb-config-example-ihm-DEPO.yml", "CACHE-DEPO"),
    ("HOLD-REL", "exdb-config-example-ihm-HOLD-REL.yml", "CACHE-HOLD-REL"),
])
def test_mmcif2json_command(proc, monkeypatch, mode, config, cache):
    popen = fake_popen()
    monkeypatch.setattr(ep.subprocess, "Popen", popen)
    assert proc.mmcif2json("/w/in.cif", "/w/out.json", data_mode=mode) == "/w/out.json"
    assert popen.calls == [[
        "env", "PYTHONPATH=/opt/rcsb", "/usr/bin/python3", "/opt/rcsb/rcsb/db/tests-validate/SchemaDataPrepValidateIhm.py",
        "-c", f"/opt/rcsb/rcsb/db/config/{config}", "-i", "/w/in.cif", "-o", "/w/out.json", "-cc", f"/opt/rcsb/{cache}"]]


def test_mmcif2json_unknown_mode(proc):
    with pytest.raises(ep.ProcessingError, match="unknown pyrcsb_db data_mode: REL"):
        proc.mmcif2json("/w/in.cif", "/w/out.json", data_mode="REL")


def test_mmcif2json_failure_names_input_file(proc, monkeypatch):
    """Regression: the error message referenced an undefined variable (NameError)."""
    monkeypatch.setattr(ep.subprocess, "Popen", fake_popen(returncode=2))
    with pytest.raises(ep.SubProcessError, match='file "/w/in.cif"'):
        proc.mmcif2json("/w/in.cif", "/w/out.json")


# ---------------------------------------------------------------------------
# validateExportmmCIF (CifCheck)
# ---------------------------------------------------------------------------
def test_validate_export_clean_file(proc, ermrest, tmp_path, monkeypatch):
    cif = tmp_path / "D_1-ABCD.cif"
    cif.write_text("data_x\n")
    popen = fake_popen()
    monkeypatch.setattr(ep.subprocess, "Popen", popen)
    cwd = os.getcwd()
    proc.validateExportmmCIF(str(cif))

    assert popen.calls == [["/bin/CifCheck", "-f", str(cif), "-dictSdb", "/dict.sdb"]]
    assert os.getcwd() == cwd                                     # chdir restored
    assert ermrest.delete.call_args.args[2] == "Entry_Error_File"  # old errors cleared
    row = ermrest.insert.call_args.kwargs["payload"][0]
    assert (row["File_Type"], row["Structure_Id"], row["File_Name"]) == ("mmCIF", "D_1-ABCD", "D_1-ABCD.cif")
    assert proc.upload_file_groups.call_args.kwargs["namespace_prefix"].endswith("/final_mmCIF")
    assert proc.generated_file_rows == [row]


def test_validate_export_update_cif_false_skips_upload(proc, ermrest, tmp_path, monkeypatch):
    cif = tmp_path / "D_1-ABCD.cif"
    cif.write_text("data_x\n")
    monkeypatch.setattr(ep.subprocess, "Popen", fake_popen())
    proc.validateExportmmCIF(str(cif), update_cif=False)
    ermrest.insert.assert_not_called()
    assert proc.generated_file_rows == []


def test_validate_export_existing_generated_file_is_updated(proc, ermrest, tmp_path, monkeypatch):
    cif = tmp_path / "D_1-ABCD.cif"
    cif.write_text("data_x\n")
    monkeypatch.setattr(ep.subprocess, "Popen", fake_popen())
    ermrest.insert.side_effect = lambda *a, **k: []                 # already exists
    ermrest.query.return_value = [{"RID": "GF-1", "File_MD5": "old", "File_Name": "D_1-ABCD.cif"}]
    proc.validateExportmmCIF(str(cif))
    payload = ermrest.update.call_args.kwargs["payload"][0]
    assert payload["RID"] == "GF-1" and payload["File_MD5"] == "md5-D_1-ABCD.cif"


def test_validate_export_with_cifcheck_errors(proc, ermrest, tmp_path, monkeypatch):
    cif = tmp_path / "D_1-ABCD.cif"
    cif.write_text("data_x\n")
    (tmp_path / "D_1-ABCD.cif-parser.log").write_text("stale from last run")     # must be removed first

    def cifcheck(args):
        (tmp_path / "D_1-ABCD.cif-diag.log").write_text("ERROR: bad item")
    monkeypatch.setattr(ep.subprocess, "Popen", fake_popen(on_run=cifcheck))

    with pytest.raises(ep.ProcessingError, match="CifCheck error files found"):
        proc.validateExportmmCIF(str(cif))

    types = [r["File_Type"] for r in ermrest.insert.call_args.kwargs["payload"]]
    assert types == ["Log: CifCheck diagnostic error file", "mmCIF"]   # stale parser log not reported
    assert (tmp_path / "D_1-ABCD.cif-error.cif").exists() and not cif.exists()
    deleted = [c.args[2] for c in ermrest.delete.call_args_list]
    assert deleted == ["Entry_Generated_File"]
    assert proc.generated_file_rows == []


def test_validate_export_nonzero_return(proc, tmp_path, monkeypatch):
    cif = tmp_path / "D_1-ABCD.cif"
    cif.write_text("data_x\n")
    monkeypatch.setattr(ep.subprocess, "Popen", fake_popen(returncode=1))
    cwd = os.getcwd()
    with pytest.raises(ep.SubProcessError):
        proc.validateExportmmCIF(str(cif))
    assert os.getcwd() == cwd


# ---------------------------------------------------------------------------
# generate_ihmv_reports (singularity / IHMValidation)
# ---------------------------------------------------------------------------
@pytest.fixture
def ihmv(proc, tmp_path):
    cif = tmp_path / "9ABC.cif"
    cif.write_text("data_9ABC\n")
    proc.workflow_status = "SUBMISSION COMPLETE"
    return proc, cif


def _write_reports(scratch):
    def run(args):
        out = os.path.join(scratch, "output", "9ABC")
        os.makedirs(out, exist_ok=True)
        for name in ["9ABC_full_validation.pdf", "9ABC_summary_validation.pdf", "9ABC_html.tar.gz", "ignored.log"]:
            open(os.path.join(out, name), "w").close()
    return run


def test_generate_ihmv_reports_success(ihmv, ermrest, monkeypatch, tmp_path):
    proc, cif = ihmv
    scratch = str(tmp_path / "scratch" / "1-ABCD")
    popen = fake_popen(on_run=_write_reports(scratch))
    monkeypatch.setattr(ep.subprocess, "Popen", popen)
    cwd = os.getcwd()
    proc.generate_ihmv_reports(str(cif))

    args = popen.calls[0]
    assert args[:3] == ["singularity", "exec", "--pid"]
    assert args[args.index("-f") + 1] == "/ihmv/input/9ABC.cif"
    assert args[args.index("--watermark") + 1] == "confidential"          # HOLD reports are watermarked
    assert os.path.exists(f"{scratch}/input/9ABC.cif")
    types = sorted(r["File_Type"] for r in ermrest.insert.call_args.args[3])
    assert types == ["Validation: Full PDF", "Validation: HTML tar.gz", "Validation: Summary PDF"]
    assert len(proc.generated_file_rows) == 3
    assert os.getcwd() == cwd


def test_generate_ihmv_reports_release_has_no_watermark(ihmv, monkeypatch, tmp_path):
    proc, cif = ihmv
    proc.workflow_status = "RELEASE READY"
    popen = fake_popen(on_run=_write_reports(str(tmp_path / "scratch" / "1-ABCD")))
    monkeypatch.setattr(ep.subprocess, "Popen", popen)
    proc.generate_ihmv_reports(str(cif))
    assert popen.calls[0][popen.calls[0].index("--watermark") + 1] == "none"


def test_generate_ihmv_reports_nonzero_return_keeps_details(ihmv, monkeypatch):
    proc, cif = ihmv
    monkeypatch.setattr(ep.subprocess, "Popen", fake_popen(returncode=1, stdout=b"x" * 10000, stderr=b"boom"))
    with pytest.raises(ep.SubProcessError, match="non-zero return code") as exc:
        proc.generate_ihmv_reports(str(cif))
    assert "boom" in exc.value.details
    assert len(exc.value.details) <= proc.processing_details_limit


def test_generate_ihmv_reports_missing_output_dir(ihmv, monkeypatch):
    proc, cif = ihmv
    monkeypatch.setattr(ep.subprocess, "Popen", fake_popen())
    with pytest.raises(ep.SubProcessError, match="output dir .* not found"):
        proc.generate_ihmv_reports(str(cif))


def test_generate_ihmv_reports_timeout(ihmv, monkeypatch):
    proc, cif = ihmv
    monkeypatch.setattr(ep.subprocess, "Popen", fake_popen(timeout_exc=True))
    with pytest.raises(ep.SubProcessError, match="TimeoutExpired"):
        proc.generate_ihmv_reports(str(cif))


# ---------------------------------------------------------------------------
# fname2ftype / generate_PDB_JSON
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("fname, ftype", [
    ("9ABC_full_validation.pdf", "Validation: Full PDF"),
    ("9ABC_summary_validation.pdf", "Validation: Summary PDF"),
    ("9ABC_html.tar.gz", "Validation: HTML tar.gz"),
])
def test_fname2ftype(fname, ftype):
    assert ep.EntryProcessor.fname2ftype(fname) == ftype


def test_fname2ftype_unknown():
    with pytest.raises(ep.SubProcessError, match="unknown file type"):
        ep.EntryProcessor.fname2ftype("9ABC.pdf")


def test_generate_pdb_json(proc, ermrest, tmp_path, monkeypatch):
    cif = tmp_path / "9ABC.cif"
    cif.write_text("data_9ABC\n")
    json_fpath = tmp_path / "9ABC.json"

    def to_json(cif_fpath, out, data_mode):
        assert data_mode == "HOLD-REL"
        open(out, "w").write("[]")
    monkeypatch.setattr(proc, "mmcif2json", mock.MagicMock(side_effect=to_json))
    assert proc.generate_PDB_JSON(str(cif), str(json_fpath)) == str(json_fpath)
    row = ermrest.insert.call_args.kwargs["payload"][0]
    assert (row["File_Type"], row["File_Name"]) == ("JSON: mmCIF content", "9ABC.json")
    assert proc.generated_file_rows == [row]
