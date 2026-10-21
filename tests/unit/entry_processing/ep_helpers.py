"""Constants and model fakes shared by the entry_processing unit tests (fixtures live in conftest.py)."""
from types import SimpleNamespace

import pytest

ep = pytest.importorskip("pdb_dev.processing.entry_processing.entry_processor")

USER_ID = "https://auth.globus.org/11111111-2222-3333-4444-555555555555"

ENTRY_ROW = {
    "RID": "1-ABCD",
    "id": "D_1-ABCD",
    "RCB": USER_ID,
    "RCT": "2025-01-02T03:04:05.000000+00:00",
    "mmCIF_File_Name": "submitted.cif",
    "mmCIF_File_URL": "/hatrac/pdb/submitted.cif",
    "mmCIF_File_Bytes": 1024,
    "mmCIF_File_MD5": "md5-new",
    "Last_mmCIF_File_MD5": None,
    "Workflow_Status": "DEPO",
    "Process_Status": "New (trigger backend process)",
    "Record_Status_Detail": None,
    "Accession_Code": None,
    "Deposit_Date": "2025-01-02",
    "Release_Date": None,
}

RELATED_FILE_ROW = {
    "RID": "1-FILE",
    "File_Name": "restraints.csv",
    "File_URL": "/hatrac/pdb/restraints.csv",
    "File_MD5": "md5-csv",
    "structure_id": "D_1-ABCD",
    "RCT": "2025-01-02T03:04:05.000000+00:00",
    "File_Format": "CSV",
    "Restraint_Process_Status": None,
    "Restraint_Workflow_Status": "DEPO",
    "Record_Status_Detail": None,
    "Table_Name": "ihm_cross_link_list",
    "entry_rid": "1-ABCD",
    "RCB": USER_ID,
}

USER_ROW = {"ID": USER_ID, "Email": "depositor@example.org", "Full_Name": "Test Depositor"}


# ---------------------------------------------------------------------------
# Small fakes for the deriva model objects that entry_processor walks
# ---------------------------------------------------------------------------
class FakeColumn:
    def __init__(self, name, nullok=True):
        self.name = name
        self.nullok = nullok


class FakeColumns:
    def __init__(self, columns):
        self._by_name = {c.name: c for c in columns}
        self.elements = self._by_name   # `cname in table.columns.elements`

    def __getitem__(self, name):
        return self._by_name[name]


class FakeTable:
    def __init__(self, name, cnames=(), not_null=()):
        self.name = name
        self.columns = FakeColumns([FakeColumn(c, nullok=c not in not_null) for c in cnames])
        self.foreign_keys = []


class FakeFKey:
    def __init__(self, table, pk_table, pairs, constraint_name=None):
        """pairs: [(from_cname, to_cname), ...]"""
        self.table = table
        self.pk_table = pk_table
        self.column_map = {FakeColumn(f): FakeColumn(t) for f, t in pairs}
        self.constraint_name = constraint_name or f"{table.name}_{pk_table.name}_fkey"
        table.foreign_keys.append(self)


def fake_model(*tables):
    pdb = SimpleNamespace(tables={t.name: t for t in tables})
    return SimpleNamespace(schemas={"PDB": pdb})
