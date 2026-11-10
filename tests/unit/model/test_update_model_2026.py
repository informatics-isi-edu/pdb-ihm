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
    # accession code issued; the Accession_Code row's RMT is inside [deposit + 1 day, release - 1 day]
    {"RID": "1-A", "Accession_Code": "9ABC", "Deposit_Date": "2025-01-02", "Release_Date": "2025-03-05",
     "ac_rmt": "2025-01-10T18:30:00-08:00", "Accession_Issue_Time": None},
    # still in deposition: no accession code yet
    {"RID": "1-B", "Accession_Code": None, "Deposit_Date": "2025-03-04", "Release_Date": None,
     "ac_rmt": None, "Accession_Issue_Time": None},
    # already has an issue time (set earlier or by the trigger): not queried, not changed
    {"RID": "1-C", "Accession_Code": "9DEF", "Deposit_Date": "2025-02-01", "Release_Date": None,
     "ac_rmt": "2025-02-05T08:00:00+00:00", "Accession_Issue_Time": "2025-02-05T08:00:00+00:00"},
]


def fake_query(rows):
    """get_ermrest_query stand-in: honours the null filters used here ('&' and '/' both mean AND; the join and
    $M parts are ignored) and returns the requested attributes under their alias (e.g. 'ac_rmt:=AC:RMT')."""
    def query(catalog, sname, tname, constraints=None, attributes=None, **kwargs):
        out = rows
        for c in re.split(r"[&/]", constraints or ""):
            if c == "Accession_Issue_Time::null::":
                out = [r for r in out if r["Accession_Issue_Time"] is None]
            elif c == "!Accession_Code::null::":
                out = [r for r in out if r["Accession_Code"] is not None]
            elif c == "Accession_Code::null::":
                out = [r for r in out if r["Accession_Code"] is None]
        keep = ["RID"] + [a.split(":=")[0] for a in attributes or []]
        return [{k: r[k] for k in keep if k in r} for r in out]
    return query


@pytest.fixture
def ermrest(monkeypatch):
    update = mock.MagicMock(side_effect=lambda *a, **k: k["payload"])
    monkeypatch.setattr(um, "get_ermrest_query", mock.MagicMock(side_effect=fake_query(ENTRIES)))
    monkeypatch.setattr(um, "update_table_rows", update)
    return SimpleNamespace(query=um.get_ermrest_query, update=update)


def issue_time_for(monkeypatch, **row):
    """Run migrate_accession_issue_time on one entry; return the Accession_Issue_Time it writes (None if unchanged)."""
    row = {"RID": "1-X", "Accession_Code": "9XYZ", "Release_Date": None, "Accession_Issue_Time": None, **row}
    update = mock.MagicMock(side_effect=lambda *a, **k: k["payload"])
    monkeypatch.setattr(um, "get_ermrest_query", mock.MagicMock(side_effect=fake_query([row])))
    monkeypatch.setattr(um, "update_table_rows", update)
    um.migrate_accession_issue_time(entry_model([])[0])
    payload = update.call_args.kwargs["payload"]
    return payload[0]["Accession_Issue_Time"] if payload else None


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


def test_migrate_accession_issue_time_query(ermrest):
    """Entries with an accession code, joined to their Accession_Code row to read its RMT."""
    model, _ = entry_model([])
    um.migrate_accession_issue_time(model)
    kwargs = ermrest.query.call_args.kwargs
    assert "Accession_Issue_Time::null::" in kwargs["constraints"]
    assert "!Accession_Code::null::" in kwargs["constraints"]
    assert "AC:=(Accession_Code)=(PDB:Accession_Code:Accession_Code)" in kwargs["constraints"]
    assert "ac_rmt:=AC:RMT" in kwargs["attributes"]
    assert ermrest.update.call_args.kwargs["column_names"] == ["Accession_Issue_Time"]


def test_migrate_accession_issue_time_fills_only_empty_values(ermrest):
    model, _ = entry_model([])
    um.migrate_accession_issue_time(model)
    payload = ermrest.update.call_args.kwargs["payload"]
    assert [r["RID"] for r in payload] == ["1-A"]          # 1-B has no accession code, 1-C already has a value
    assert payload[0]["Accession_Issue_Time"] == "2025-01-10T18:30:00-08:00"


@pytest.mark.parametrize("deposit, release, ac_rmt, expected", [
    # Accession_Code RMT inside [deposit + 1 day, release - 1 day]: use it
    ("2025-01-02", "2025-03-05", "2025-01-10T18:30:00-08:00", "2025-01-10T18:30:00-08:00"),
    ("2025-04-01", None, "2025-04-02T00:00:00+00:00", "2025-04-02T00:00:00+00:00"),      # exactly deposit + 1 day
    ("2025-06-01", "2025-06-11", "2025-06-10T00:00:00+00:00", "2025-06-10T00:00:00+00:00"),  # exactly release - 1 day
    ("2025-06-01", None, "2029-12-30T00:00:00+00:00", "2029-12-30T00:00:00+00:00"),      # no release date: up to 2030
    # otherwise: deposit date + 1 day (UTC midnight)
    ("2025-05-06", None, "2025-05-06T12:00:00+00:00", "2025-05-07T00:00:00+00:00"),      # RMT before deposit + 1 day
    ("2025-06-01", "2025-06-11", "2025-06-10T12:00:00+00:00", "2025-06-02T00:00:00+00:00"),  # RMT after release - 1 day
    ("2025-06-01", None, "2030-01-01T00:00:00+00:00", "2025-06-02T00:00:00+00:00"),      # no release date, RMT >= 2030
])
def test_migrate_accession_issue_time_rules(monkeypatch, deposit, release, ac_rmt, expected):
    assert issue_time_for(monkeypatch, Deposit_Date=deposit, Release_Date=release, ac_rmt=ac_rmt) == expected


@pytest.mark.parametrize("code", ["8ZZ1", "8ZZ2", "8ZZ3"])
def test_migrate_accession_issue_time_8zz_entries_use_deposit_date(monkeypatch, code):
    """Hard-coded in the migration: when the RMT is outside the window, 8ZZ1-8ZZ3 get the deposit date itself."""
    assert issue_time_for(monkeypatch, Accession_Code=code, Deposit_Date="2024-01-01", Release_Date="2024-05-01",
                          ac_rmt="2025-07-01T00:00:00+00:00") == "2024-01-01T00:00:00+00:00"


def test_migrate_accession_issue_time_8zz_entries_use_rmt_inside_window(monkeypatch):
    assert issue_time_for(monkeypatch, Accession_Code="8ZZ1", Deposit_Date="2024-01-01", Release_Date="2024-05-01",
                          ac_rmt="2024-02-01T00:00:00+00:00") == "2024-02-01T00:00:00+00:00"


@pytest.mark.parametrize("existing", ["2025-05-10T09:00:01.250+00:00", "2025-01-01T00:00:00+00:00"])
def test_migrate_accession_issue_time_keeps_existing_values(monkeypatch, existing):
    """Regression (e7173fe): existing values, e.g. set by the trigger, were replaced by the computed time.
    The migration now only fills entries whose Accession_Issue_Time is null."""
    assert issue_time_for(monkeypatch, Deposit_Date="2025-05-06", ac_rmt="2025-05-10T09:00:00+00:00",
                          Accession_Issue_Time=existing) is None


def test_migrate_accession_issue_time_second_run_changes_nothing(monkeypatch):
    rows = [dict(r) for r in ENTRIES]
    update = mock.MagicMock(side_effect=lambda *a, **k: k["payload"])
    monkeypatch.setattr(um, "get_ermrest_query", mock.MagicMock(side_effect=fake_query(rows)))
    monkeypatch.setattr(um, "update_table_rows", update)
    model, _ = entry_model([])
    um.migrate_accession_issue_time(model)
    for written in update.call_args.kwargs["payload"]:                     # apply the first run's update
        next(r for r in rows if r["RID"] == written["RID"])["Accession_Issue_Time"] = written["Accession_Issue_Time"]
    um.migrate_accession_issue_time(model)
    assert update.call_args.kwargs["payload"] == []


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
