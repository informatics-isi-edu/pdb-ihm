"""Work-unit status mapping in pdb_entry_processing_worker.

The worker module configures logging and builds a PollingErmrestCatalog at import time from environment
variables, so the module is imported with harmless placeholder values (no connection is opened).
"""
import importlib
import sys

import pytest


@pytest.fixture(scope="module")
def worker(tmp_path_factory):
    mp = pytest.MonkeyPatch()
    mp.setenv("PDB_LOG", str(tmp_path_factory.mktemp("log") / "worker.log"))
    mp.setenv("PDB_SERVER", "example.invalid")
    mp.setenv("CATALOG", "1")
    sys.modules.pop("pdb_dev.processing.entry_processing.pdb_entry_processing_worker", None)
    try:
        yield importlib.import_module("pdb_dev.processing.entry_processing.pdb_entry_processing_worker")
    finally:
        mp.undo()


@pytest.fixture(scope="module")
def ep():
    return importlib.import_module("pdb_dev.processing.entry_processing.entry_processor")


ROW = {"RID": "1-ABCD"}


def test_worker_status_terms_match_entry_processor(worker, ep):
    """The worker keeps its own copy of the status vocabulary; it must stay identical to entry_processor's."""
    assert worker.Process_Status_Terms == ep.Process_Status_Terms


def test_every_work_unit_claims_in_progress_and_fails_with_error_status(worker):
    terms = set(worker.Process_Status_Terms.values())
    assert len(worker._work_units) == 5
    for unit in worker._work_units:
        claim = unit.claim_input_data(ROW)
        failure = unit.failure_input_data(ROW, RuntimeError("boom"))
        assert claim["RID"] == failure["RID"] == "1-ABCD"
        (claim_col, claim_status), = [(k, v) for k, v in claim.items() if k != "RID"]
        (fail_col, fail_status), = [(k, v) for k, v in failure.items() if k != "RID"]
        assert claim_col == fail_col                       # same status column is claimed and failed
        assert claim_status in terms and claim_status.startswith("In progress:")
        assert fail_status in terms and fail_status.startswith("Error:")


def test_release_unit_failure_status(worker, ep):
    """Regression: the release unit's failure handler used an unquoted name and raised NameError, so a failed
    release never set the error status."""
    statuses = {unit.claim_input_data(ROW)["Process_Status"]: unit.failure_input_data(ROW, None)
                for unit in worker._work_units if "Process_Status" in unit.claim_input_data(ROW)}
    release = statuses[ep.Process_Status_Terms["IN_PROGRESS_RELEASING_ENTRY"]]
    assert release == {"RID": "1-ABCD", "Process_Status": ep.Process_Status_Terms["ERROR_RELEASING_ENTRY"]}


@pytest.mark.parametrize("in_progress, error", [
    ("IN_PROGRESS_UPLOADING_mmCIF_FILE", "ERROR_PROCESSING_UPLOADED_mmCIF_FILE"),
    ("IN_PROGRESS_GENERATING_mmCIF_FILE", "ERROR_GENERATING_mmCIF_FILE"),
    ("IN_PROGRESS_GENERATING_SYSTEM_FILES", "ERROR_GENERATING_SYSTEM_FILES"),
    ("IN_PROGRESS_RELEASING_ENTRY", "ERROR_RELEASING_ENTRY"),
    ("IN_PROGRESS_PROCESSING_UPLOADED_RESTRAINT_FILES", "ERROR_PROCESSING_UPLOADED_RESTRAINT_FILES"),
])
def test_each_step_has_matching_claim_and_failure(worker, in_progress, error):
    terms = worker.Process_Status_Terms
    pairs = {next(v for k, v in u.claim_input_data(ROW).items() if k != "RID"):
             next(v for k, v in u.failure_input_data(ROW, None).items() if k != "RID")
             for u in worker._work_units}
    assert pairs[terms[in_progress]] == terms[error]
