from argparse import Namespace
from types import SimpleNamespace
from unittest import mock

import pytest

from pdb_dev.utils import data


class Col:
    """Hashable stand-in for an ermrest Column (column_map keys must be hashable)."""
    def __init__(self, name):
        self.name = name


def _table(name, fkeys):
    """fkeys: list of (pk_table_name, [(from_col, to_col), ...])"""
    t = SimpleNamespace(name=name, foreign_keys=[])
    for pk_name, cols in fkeys:
        column_map = {Col(f): Col(to) for f, to in cols}
        t.foreign_keys.append(SimpleNamespace(pk_table=SimpleNamespace(name=pk_name), column_map=column_map))
    return t


TABLES = [
    _table("ihm_model_list", [("entry", [("structure_id", "id")])]),
    _table("Entry_Related_File", [("entry", [("Entry", "RID")])]),
    _table("Accession_Code", [("entry", [("Entry", "RID")])]),       # excluded by default
    _table("chem_comp", [("Vocab_thing", [("type", "Name")])]),        # does not reference entry
    _table("entry", []),
]

ENTRIES = [
    {"RID": "1-A", "id": "D_1-A", "Last_mmCIF_File_MD5": "abc"},
    {"RID": "1-B", "id": "D_1-B", "Last_mmCIF_File_MD5": None},
]


@pytest.fixture
def patched():
    with mock.patch.object(data, "get_topo_sorted_tables", return_value=TABLES), \
         mock.patch.object(data, "get_ermrest_query", return_value=ENTRIES) as q, \
         mock.patch.object(data, "delete_table_rows") as d, \
         mock.patch.object(data, "update_table_rows", side_effect=lambda *a, **k: k["payload"]) as u:
        yield SimpleNamespace(query=q, delete=d, update=u)


def test_clear_entries_builds_constraints(patched):
    data.clear_entries("catalog", ["1-A", "1-B"])
    calls = {c.args[2]: c.kwargs["constraints"] for c in patched.delete.call_args_list}
    assert calls == {
        "ihm_model_list": "structure_id=any(D_1-A,D_1-B)",
        "Entry_Related_File": "Entry=any(1-A,1-B)",
    }
    # only entries that still have an md5 are reset
    assert patched.update.call_args.kwargs["payload"] == [{"RID": "1-A", "Last_mmCIF_File_MD5": None}]


def test_clear_entries_dry_run_does_not_update(patched):
    data.clear_entries("catalog", ["1-A", "1-B"], dry_run=True)
    assert all(c.kwargs["dry_run"] is True for c in patched.delete.call_args_list)
    patched.update.assert_not_called()


def test_clear_entries_empty_is_noop(patched):
    data.clear_entries("catalog", [])
    patched.query.assert_not_called()


def test_clear_entries_no_match_raises(patched):
    patched.query.return_value = []
    with pytest.raises(Exception, match="no match"):
        data.clear_entries("catalog", ["9-Z"])


def test_clear_entry_single(patched):
    patched.query.return_value = [ENTRIES[0]]
    data.clear_entry("catalog", "1-A")
    calls = {c.args[2]: c.kwargs["constraints"] for c in patched.delete.call_args_list}
    assert calls == {"ihm_model_list": "structure_id=D_1-A", "Entry_Related_File": "Entry=1-A"}
    patched.update.assert_called_once()


def test_main_clear_entries_uses_rid_and_rids():
    """Regression: main() called clear_entry(..., dry_run=...) which does not accept dry_run,
    and ignored --rids."""
    args = Namespace(host="h", credential_file=None, catalog_id="99", clear_entries=True,
                     rid="1-C", rids="1-A,1-B", dry_run=True)
    with mock.patch.object(data, "get_credential", return_value={}), \
         mock.patch.object(data, "ErmrestCatalog") as cat, \
         mock.patch.object(data, "clear_entries") as ce:
        cat.return_value.dcctx = {}
        data.main(args)
    assert ce.call_args.args[1] == ["1-A", "1-B", "1-C"]
    assert ce.call_args.kwargs == {"dry_run": True}


# ---------------------------------------------------------------------------
# EntryProcessor.fname2ftype (classmethod, no catalog needed)
# ---------------------------------------------------------------------------
ep = pytest.importorskip("pdb_dev.processing.entry_processing.entry_processor")


@pytest.mark.parametrize("fname, ftype", [
    ("9A9V_full_validation.pdf", "Validation: Full PDF"),
    ("9A9V_summary_validation.pdf", "Validation: Summary PDF"),
    ("9A9V_html.tar.gz", "Validation: HTML tar.gz"),
])
def test_fname2ftype(fname, ftype):
    assert ep.EntryProcessor.fname2ftype(fname) == ftype


def test_fname2ftype_unknown_raises_subprocess_error():
    """Regression: classmethod referenced `self` and raised NameError instead of SubProcessError."""
    with pytest.raises(ep.SubProcessError, match="unknown file type"):
        ep.EntryProcessor.fname2ftype("9A9V_other.txt")
