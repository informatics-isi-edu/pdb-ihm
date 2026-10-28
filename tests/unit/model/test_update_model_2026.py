"""pdb_dev.model.update_model_2026: entry column changes and data migrations (catalog mocked)."""
import re
import sys
from types import SimpleNamespace
from unittest import mock

import pytest

um = pytest.importorskip("pdb_dev.model.update_model_2026")


class FakeColumn:
    def __init__(self, name):
        self.name = name
        self.drop = mock.MagicMock()


class FakeColumns:
    def __init__(self, names):
        self.elements = {n: FakeColumn(n) for n in names}

    def __getitem__(self, name):
        return self.elements[name]


def entry_model(column_names):
    table = SimpleNamespace(columns=FakeColumns(column_names), create_column=mock.MagicMock())
    return SimpleNamespace(schemas={"PDB": SimpleNamespace(tables={"entry": table})}, catalog=mock.MagicMock()), table


ENTRIES = [
    # issued an accession code (HOLD/REL), no issue time yet
    {"RID": "1-A", "Accession_Code": "9ABC", "Deposit_Date": "2025-01-02", "Accession_Issue_Time": None},
    # still in deposition: no accession code yet
    {"RID": "1-B", "Accession_Code": None, "Deposit_Date": "2025-03-04", "Accession_Issue_Time": None},
    # already has an issue time
    {"RID": "1-C", "Accession_Code": "9DEF", "Deposit_Date": "2025-05-06", "Accession_Issue_Time": "2025-05-20T10:00:00+00:00"},
]


def fake_query(rows):
    """get_ermrest_query stand-in that honours the simple filters used here ('&' and '/' both mean AND)."""
    def query(catalog, sname, tname, constraints=None, attributes=None, **kwargs):
        out = rows
        for c in re.split(r"[&/]", constraints or ""):
            if c == "Accession_Issue_Time::null::":
                out = [r for r in out if r["Accession_Issue_Time"] is None]
            elif c == "!Accession_Code::null::":
                out = [r for r in out if r["Accession_Code"] is not None]
            elif c == "Accession_Code::null::":
                out = [r for r in out if r["Accession_Code"] is None]
        keep = ["RID"] + list(attributes or [])
        return [{k: r[k] for k in keep if k in r} for r in out]
    return query


@pytest.fixture
def ermrest(monkeypatch):
    update = mock.MagicMock(side_effect=lambda *a, **k: k["payload"])
    monkeypatch.setattr(um, "get_ermrest_query", mock.MagicMock(side_effect=fake_query(ENTRIES)))
    monkeypatch.setattr(um, "update_table_rows", update)
    return SimpleNamespace(query=um.get_ermrest_query, update=update)


# ---------------------------------------------------------------------------
# update_PDB_entry: column changes
# ---------------------------------------------------------------------------
def test_update_pdb_entry_creates_new_columns_and_drops_issue_date():
    model, table = entry_model(["RID", "Accession_Issue_Date"])
    um.update_PDB_entry(model)
    created = {c.args[0]["name"]: c.args[0] for c in table.create_column.call_args_list}
    assert set(created) == {"User_mmCIF_File_URL", "User_mmCIF_File_Name", "Accession_Issue_Time"}
    assert created["Accession_Issue_Time"]["type"]["typename"] == "timestamptz"
    assert created["Accession_Issue_Time"]["nullok"] is True
    table.columns["Accession_Issue_Date"].drop.assert_called_once()


def test_update_pdb_entry_is_idempotent():
    model, table = entry_model(["RID", "User_mmCIF_File_URL", "User_mmCIF_File_Name", "Accession_Issue_Time"])
    um.update_PDB_entry(model)
    table.create_column.assert_not_called()


# ---------------------------------------------------------------------------
# migrations
# ---------------------------------------------------------------------------
def test_migrate_user_mmcif_files(monkeypatch):
    rows = [{"RID": "1-A", "mmCIF_File_URL": "/h/a", "mmCIF_File_Name": "a.cif", "User_mmCIF_File_URL": None,
             "User_mmCIF_File_Name": None},
            {"RID": "1-B", "mmCIF_File_URL": "/h/b", "mmCIF_File_Name": "b.cif", "User_mmCIF_File_URL": "/h/b",
             "User_mmCIF_File_Name": "b.cif"}]
    monkeypatch.setattr(um, "get_ermrest_query", mock.MagicMock(return_value=rows))
    update = mock.MagicMock(side_effect=lambda *a, **k: k["payload"])
    monkeypatch.setattr(um, "update_table_rows", update)
    model, _ = entry_model([])
    um.migrate_user_mmcif_files(model)
    payload = update.call_args.kwargs["payload"]
    assert [r["RID"] for r in payload] == ["1-A"]
    assert (payload[0]["User_mmCIF_File_URL"], payload[0]["User_mmCIF_File_Name"]) == ("/h/a", "a.cif")
    assert update.call_args.kwargs["column_names"] == ["User_mmCIF_File_URL", "User_mmCIF_File_Name"]


def test_migrate_accession_issue_time_uses_deposit_date(ermrest):
    model, _ = entry_model([])
    um.migrate_accession_issue_time(model)
    payload = ermrest.update.call_args.kwargs["payload"]
    assert {"RID": "1-A", "Accession_Issue_Time": "2025-01-02"} in payload
    assert all(r["RID"] != "1-C" for r in payload)                 # existing issue times are kept
    assert ermrest.update.call_args.kwargs["column_names"] == ["Accession_Issue_Time"]


def test_migrate_accession_issue_time_skips_entries_without_accession_code(ermrest):
    """Regression: entries without an accession code also got Accession_Issue_Time = Deposit_Date, and the trigger
    (which only fills a NULL value) then never set the real time when they were put on HOLD."""
    model, _ = entry_model([])
    um.migrate_accession_issue_time(model)
    payload = ermrest.update.call_args.kwargs["payload"]
    assert all(r["RID"] != "1-B" for r in payload)
    constraints = ermrest.query.call_args.kwargs["constraints"]
    assert "!Accession_Code::null::" in constraints and "Accession_Issue_Time::null::" in constraints


def test_update_model_2026_runs_steps_in_order(monkeypatch):
    calls = []
    for name in ["update_PDB_entry", "migrate_user_mmcif_files", "migrate_accession_issue_time",
                 "update_PDB_Entry_Generated_File", "update_PDB_ihm_multi_state_scheme_connectivity",
                 "update_PDB_chem_comp_atom"]:
        monkeypatch.setattr(um, name, mock.MagicMock(side_effect=lambda m, n=name: calls.append(n)))
    um.update_model_2026(object())
    # columns exist before data is migrated into them
    assert calls.index("update_PDB_entry") < calls.index("migrate_accession_issue_time")
    assert calls.index("update_PDB_entry") < calls.index("migrate_user_mmcif_files")


def test_main_runs_update(monkeypatch):
    """Regression: main() called cli.get_credential(...), which PDBDEV_CLI/BaseCLI doesn't have."""
    monkeypatch.setattr(sys, "argv", ["prog", "--host", "example.org", "--catalog-id", "99",
                                      "--credential-file", "/tmp/cred.json"])
    monkeypatch.setattr(um, "get_credential", mock.MagicMock(return_value={"cookie": "x"}))
    monkeypatch.setattr(um, "DerivaServer", mock.MagicMock())
    run = mock.MagicMock()
    monkeypatch.setattr(um, "update_model_2026", run)
    um.main()
    um.get_credential.assert_called_once_with("example.org", credential_file="/tmp/cred.json")
    um.DerivaServer.assert_called_once_with("https", "example.org", {"cookie": "x"})
    um.DerivaServer.return_value.connect_ermrest.assert_called_once_with("99")
    run.assert_called_once_with(um.DerivaServer.return_value.connect_ermrest.return_value.getCatalogModel.return_value)
