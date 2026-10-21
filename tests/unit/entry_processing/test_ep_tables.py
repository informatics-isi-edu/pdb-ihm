"""Table ordering and loading: sortTablesFromFile, updateRecordsBasic, rollbackInsertedRows, loadTablesFromJSON,
loadTableFromCSV, clear_cif_tables, clear_entry. The deriva model is replaced with small fakes."""
import json
from unittest import mock

import pytest

from ep_helpers import ep, FakeTable, FakeFKey, fake_model

RANKED = {0: ["entry", "chem_comp"], 1: ["entity"], 2: ["entity_poly", "struct_asym"], 3: ["entity_poly_seq"]}


def write_json(tmp_path, tables):
    path = tmp_path / "pdb.json"
    path.write_text(json.dumps([tables]))
    return str(path)


@pytest.fixture
def proc(make_processor, monkeypatch):
    p = make_processor()
    monkeypatch.setattr(p, "get_topo_ranked_tables", lambda catalog, tname_only=False: RANKED)
    monkeypatch.setattr(p, "get_topo_sorted_tables",
                        lambda catalog, tname_only=False, reverse=False:
                        [t for tier in RANKED.values() for t in tier][::-1 if reverse else 1])
    return p


# ---------------------------------------------------------------------------
# sortTablesFromFile
# ---------------------------------------------------------------------------
def test_sort_tables_from_file_orders_by_fk_rank(proc, tmp_path):
    fpath = write_json(tmp_path, {"entity_poly_seq": [], "entity": [], "chem_comp": [], "entity_poly": []})
    assert proc.sortTablesFromFile(fpath) == ["chem_comp", "entity", "entity_poly", "entity_poly_seq"]


def test_sort_tables_from_file_keeps_file_order_within_tier(proc, tmp_path):
    fpath = write_json(tmp_path, {"struct_asym": [], "entity_poly": []})
    assert proc.sortTablesFromFile(fpath) == ["struct_asym", "entity_poly"]


def test_sort_tables_from_file_drops_excluded(proc, tmp_path):
    fpath = write_json(tmp_path, {"entry": {}, "database_2": [], "pdbx_database_status": {}, "entity": []})
    assert proc.sortTablesFromFile(fpath) == ["entity"]


def test_sort_tables_from_file_unknown_table(proc, tmp_path):
    fpath = write_json(tmp_path, {"entity": [], "brand_new_category": []})
    with pytest.raises(RuntimeError, match="brand_new_category from mmCIF is not present"):
        proc.sortTablesFromFile(fpath)


# ---------------------------------------------------------------------------
# updateRecordsBasic
# ---------------------------------------------------------------------------
def entity_table():
    entry = FakeTable("entry", ["id", "RID"])
    entity = FakeTable("entity", ["id", "structure_id", "type", "src_method", "details"])
    FakeFKey(entity, entry, [("structure_id", "id")])
    return entity


def test_update_records_basic(proc):
    proc.mmCIF_defaults = {"entity": ["details"]}
    proc.vocab_ucode = {"entity": ["type", "src_method"]}
    rows = [{"id": "1", "structure_id": "9ABC", "type": "polymer", "src_method": "man"},
            {"id": "2", "type": "non-polymer", "details": "kept"}]
    out = proc.updateRecordsBasic(entity_table(), rows, "D_1-ABCD")
    assert out is rows
    assert rows[0] == {"id": "1", "structure_id": "D_1-ABCD", "type": "POLYMER", "src_method": "MAN", "details": "."}
    # structure_id is only replaced, never added
    assert rows[1] == {"id": "2", "type": "NON-POLYMER", "details": "kept"}


@pytest.mark.xfail(strict=True, reason="a null value in a vocab (ucode) column raises AttributeError on .upper()")
def test_update_records_basic_null_ucode_value(proc):
    proc.vocab_ucode = {"entity": ["type"]}
    rows = [{"id": "1", "type": None}]
    proc.updateRecordsBasic(entity_table(), rows, "D_1-ABCD")
    assert rows[0]["type"] is None


# ---------------------------------------------------------------------------
# rollbackInsertedRows / clear_cif_tables / clear_entry
# ---------------------------------------------------------------------------
def model_with(*specs):
    return fake_model(*[FakeTable(name, cnames) for name, cnames in specs])


def test_rollback_deletes_in_reverse_dependency_order(proc, ermrest):
    proc.model = model_with(("entity", ["structure_id"]), ("entity_poly_seq", ["structure_id"]),
                            ("chem_comp", ["structure_id"]))
    proc.rollbackInsertedRows({"entity": [1], "entity_poly_seq": [1], "chem_comp": [1]}, "D_1-ABCD")
    deleted = [c.args[2] for c in ermrest.delete.call_args_list]
    assert deleted == ["entity_poly_seq", "entity", "chem_comp"]
    assert all(c.kwargs["constraints"] == "structure_id=D_1-ABCD" for c in ermrest.delete.call_args_list)


def test_rollback_uses_entry_id_column_when_no_structure_id(proc, ermrest):
    proc.model = model_with(("entity", ["entry_id"]))
    proc.rollbackInsertedRows({"entity": []}, "D_1-ABCD")
    assert ermrest.delete.call_args.kwargs["constraints"] == "entry_id=D_1-ABCD"


def test_rollback_failure_raises_ermrest_error(proc, ermrest):
    proc.model = model_with(("entity", ["structure_id"]))
    ermrest.delete.side_effect = RuntimeError("409 conflict")
    with pytest.raises(ep.ErmrestError, match="rolling back table entity"):
        proc.rollbackInsertedRows({"entity": []}, "D_1-ABCD")


def test_clear_cif_tables_from_json(proc, ermrest, tmp_path):
    proc.model = model_with(("entity", ["structure_id"]), ("entity_poly", ["entry_id"]), ("chem_comp", ["id"]))
    proc.processing_row["Last_mmCIF_File_MD5"] = "md5-old"
    fpath = write_json(tmp_path, {"entity": [], "entity_poly": [], "chem_comp": []})
    proc.clear_cif_tables(json_fpath=fpath)
    calls = [(c.args[2], c.kwargs["constraints"]) for c in ermrest.delete.call_args_list]
    assert calls == [("entity_poly", "entry_id=D_1-ABCD"), ("entity", "structure_id=D_1-ABCD")]  # chem_comp skipped
    assert ermrest.update.call_args.kwargs["payload"] == [{"RID": "1-ABCD", "Last_mmCIF_File_MD5": None}]


def test_clear_entry_deletes_rows_referencing_entry(proc, ermrest, monkeypatch):
    entry = FakeTable("entry", ["id", "RID"])
    by_id = FakeTable("entity", ["structure_id"]); FakeFKey(by_id, entry, [("structure_id", "id")])
    by_rid = FakeTable("Entry_Related_File", ["Entry"]); FakeFKey(by_rid, entry, [("Entry", "RID")])
    kept = FakeTable("Accession_Code", ["Entry"]); FakeFKey(kept, entry, [("Entry", "RID")])
    monkeypatch.setattr(proc, "get_topo_sorted_tables", lambda catalog, reverse=False: [by_id, by_rid, kept, entry])
    proc.processing_row["Last_mmCIF_File_MD5"] = "md5-old"
    proc.clear_entry()
    calls = [(c.args[2], c.kwargs["constraints"]) for c in ermrest.delete.call_args_list]
    assert calls == [("entity", "structure_id=D_1-ABCD"), ("Entry_Related_File", "Entry=1-ABCD")]


# ---------------------------------------------------------------------------
# loadTablesFromJSON
# ---------------------------------------------------------------------------
@pytest.fixture
def loader(proc, monkeypatch):
    proc.model = fake_model(FakeTable("chem_comp", ["id"]), FakeTable("entity", ["id", "structure_id"]),
                            FakeTable("ihm_entry_collection", ["id"]))
    pk = mock.MagicMock()
    monkeypatch.setattr(ep, "PkTables", mock.MagicMock(return_value=pk))
    monkeypatch.setattr(proc, "get_topo_ranked_tables",
                        lambda catalog, tname_only=False: {0: ["entry", "chem_comp", "ihm_entry_collection"], 1: ["entity"]})
    pb_tables = {}
    def table(name):
        t = pb_tables.setdefault(name, mock.MagicMock())
        t.insert.return_value.fetch.side_effect = lambda: [{"RID": f"{name}-1"}]
        return t
    proc.catalog.getPathBuilder.return_value.schemas = {"PDB": mock.MagicMock(tables=mock.MagicMock(
        __getitem__=lambda self, name: table(name)))}
    return proc, pk, pb_tables


def test_load_tables_from_json_inserts_in_order(loader, tmp_path):
    proc, pk, pb_tables = loader
    fpath = write_json(tmp_path, {"entity": [{"id": "1"}], "chem_comp": {"id": "ALA"},
                                  "ihm_entry_collection": [{"id": "C"}]})
    proc.loadTablesFromJSON(fpath)
    assert list(proc.tname2inserted) == ["chem_comp", "entity"]              # ignored table skipped
    pb_tables["chem_comp"].insert.assert_called_once_with([{"id": "ALA"}])   # single dict -> list
    entity_rows = pb_tables["entity"].insert.call_args.args[0]
    assert entity_rows == [{"id": "1"}]
    assert [c.args[0].name for c in pk.update_payload_with_rids.call_args_list] == ["chem_comp", "entity"]


def test_load_tables_from_json_dry_run(loader, tmp_path):
    proc, _, pb_tables = loader
    fpath = write_json(tmp_path, {"entity": [{"id": "1"}]})
    proc.loadTablesFromJSON(fpath, ermrest_insert=False)
    assert proc.tname2inserting == {"entity": [{"id": "1"}]}
    assert pb_tables == {}


def test_load_tables_from_json_failure_rolls_back(loader, tmp_path):
    proc, pk, _ = loader
    pk.update_payload_with_rids.side_effect = [None, KeyError("missing parent row")]
    fpath = write_json(tmp_path, {"chem_comp": [{"id": "ALA"}], "entity": [{"id": "1"}]})
    with mock.patch.object(proc, "rollbackInsertedRows") as rollback:
        with pytest.raises(ep.ProcessingError, match="Failed to insert rows in entity"):
            proc.loadTablesFromJSON(fpath)
    rollback.assert_called_once_with({"chem_comp": [{"RID": "chem_comp-1"}]}, "D_1-ABCD")


# ---------------------------------------------------------------------------
# loadTableFromCSV
# ---------------------------------------------------------------------------
@pytest.fixture
def csv_env(proc, ermrest, monkeypatch, tmp_path):
    """ihm_cross_link_list with a mandatory combo fkey to entity_poly_seq (entity_id, seq_id) -> RID."""
    seq = FakeTable("entity_poly_seq", ["RID", "entity_id", "num", "structure_id"])
    xl = FakeTable("ihm_cross_link_list",
                   ["id", "group_id", "entity_id", "seq_id", "Entity_Poly_Seq_RID", "details",
                    "structure_id", "Entry_Related_File"],
                   not_null=["entity_id", "seq_id"])
    fkey = FakeFKey(xl, seq, [("entity_id", "entity_id"), ("seq_id", "num"), ("Entity_Poly_Seq_RID", "RID")])
    proc.model = fake_model(xl, seq)
    monkeypatch.setattr(ep, "get_mmcif_rid_mandatory_fkeys", lambda table: [fkey])
    monkeypatch.setattr(ep, "get_mmcif_rid_optional_fkeys", lambda table: [])

    def query(catalog, sname, tname, constraints=None, **kwargs):
        if tname == "entry":
            return [{"RID": "1-ABCD", "id": "D_1-ABCD"}]
        if tname == "entity_poly_seq":
            return [{"RID": "SEQ-1", "entity_id": "1", "num": 10}, {"RID": "SEQ-2", "entity_id": "1", "num": 11}]
        return []
    ermrest.query.side_effect = query
    ermrest.insert.side_effect = lambda catalog, sname, tname, payload: payload

    def write(text, name="xl.csv"):
        path = tmp_path / name
        path.write_text(text)
        return str(path)
    return proc, write


def test_load_table_from_csv(csv_env, ermrest):
    proc, write = csv_env
    fpath = write("id,group_id,entity_id,seq_id,details\n1,1,1,10,\n2,1,1,11,note\n")
    proc.loadTableFromCSV(fpath, ",", "ihm_cross_link_list", "D_1-ABCD", "1-FILE", "user@x")

    assert ermrest.delete.call_args.kwargs["constraints"] == "structure_id=D_1-ABCD&Entry_Related_File=1-FILE"
    rows = ermrest.insert.call_args.args[3]
    assert rows[0] == {"id": "1", "group_id": "1", "entity_id": "1", "seq_id": "10", "details": None,
                       "structure_id": "D_1-ABCD", "Entry_Related_File": "1-FILE", "Entity_Poly_Seq_RID": "SEQ-1"}
    assert rows[1]["Entity_Poly_Seq_RID"] == "SEQ-2" and rows[1]["details"] == "note"


def test_load_table_from_csv_tsv(csv_env, ermrest):
    proc, write = csv_env
    fpath = write("id\tgroup_id\tentity_id\tseq_id\n1\t1\t1\t10\n", "xl.tsv")
    proc.loadTableFromCSV(fpath, "\t", "ihm_cross_link_list", "D_1-ABCD", "1-FILE", "user@x")
    assert ermrest.insert.call_args.args[3][0]["Entity_Poly_Seq_RID"] == "SEQ-1"


def test_load_table_from_csv_bad_header(csv_env, ermrest):
    proc, write = csv_env
    fpath = write("id,not_a_column\n1,x\n")
    with pytest.raises(ep.FileError, match=r"undefined columns: \['not_a_column'\]"):
        proc.loadTableFromCSV(fpath, ",", "ihm_cross_link_list", "D_1-ABCD", "1-FILE", "user@x")
    ermrest.insert.assert_not_called()


def test_load_table_from_csv_unknown_reference(csv_env):
    proc, write = csv_env
    fpath = write("id,entity_id,seq_id\n1,1,99\n")
    with pytest.raises(Exception, match=r"entity_poly_seq.*\('1', '99'\)"):
        proc.loadTableFromCSV(fpath, ",", "ihm_cross_link_list", "D_1-ABCD", "1-FILE", "user@x")


def test_load_table_from_csv_missing_mandatory_fkey_column(csv_env):
    proc, write = csv_env
    fpath = write("id,entity_id\n1,1\n")
    with pytest.raises(Exception, match="misses mandatory column seq_id"):
        proc.loadTableFromCSV(fpath, ",", "ihm_cross_link_list", "D_1-ABCD", "1-FILE", "user@x")


def test_load_table_from_csv_unreadable_file_reports_path(csv_env, tmp_path):
    """Regression: the error message used '%s ()' with two arguments, so a TypeError replaced the FileError."""
    proc, _ = csv_env
    missing = str(tmp_path / "missing.csv")
    with pytest.raises(ep.FileError, match="unable to read file .*missing.csv"):
        proc.loadTableFromCSV(missing, ",", "ihm_cross_link_list", "D_1-ABCD", "1-FILE", "user@x")


def test_load_table_from_csv_insert_failure(csv_env, ermrest):
    proc, write = csv_env
    ermrest.insert.side_effect = RuntimeError("400 bad request")
    fpath = write("id,entity_id,seq_id\n1,1,10\n")
    with pytest.raises(ep.ErmrestUpdateError, match="400 bad request"):
        proc.loadTableFromCSV(fpath, ",", "ihm_cross_link_list", "D_1-ABCD", "1-FILE", "user@x")
