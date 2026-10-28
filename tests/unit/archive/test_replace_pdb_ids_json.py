import gzip
import json

import pytest

from pdb_dev.processing.archive import replace_pdb_ids_json as rj


@pytest.mark.parametrize("value, expected", [
    ("8ZZ1", True),
    ("8zz1", True),
    ("ABCD", False),
    ("1234", False),
    ("8ZZ", False),
    (1234, False),
    (None, False),
])
def test_is_pdb_id(value, expected):
    assert rj.is_pdb_id(value) is expected


def test_convert_pdb_id():
    assert rj.convert_pdb_id("8ZZ8") == "pdb_00008zz8"
    assert rj.convert_pdb_id("too-long") == "too-long"


def test_replace_pdb_id_in_path_all_cases():
    new = "pdb_00008zz1"
    assert rj.replace_pdb_id_in_path("/8zz1/8ZZ1.cif.gz", "8ZZ1", new) == f"/{new}/{new}.cif.gz"
    assert rj.replace_pdb_id_in_path("/8Zz1/x.gz", "8Zz1", new) == f"/{new}/x.gz"
    assert rj.replace_pdb_id_in_path(42, "8ZZ1", new) == 42


def test_process_value_only_touches_gz_paths():
    assert rj.process_value("8zz1 plain text", "8zz1", "pdb_00008zz1") == "8zz1 plain text"
    assert rj.process_value("a/8zz1.cif.gz", "8zz1", "pdb_00008zz1") == "a/pdb_00008zz1.cif.gz"


def test_process_value_without_context_uses_pattern():
    assert rj.process_value("files/8zz1/8zz1.cif.gz", None, None) == "files/pdb_00008zz1/pdb_00008zz1.cif.gz"
    # 4-digit tokens are not PDB IDs
    assert rj.process_value("files/2024/x.cif.gz", None, None) == "files/2024/x.cif.gz"


def test_process_value_with_context_handles_underscore_suffix():
    # with the key as context, plain substring replacement does convert it
    assert rj.process_value("8zz1_model.cif.gz", "8ZZ1", "pdb_00008zz1") == "pdb_00008zz1_model.cif.gz"


def test_process_json_data_leaves_non_pdb_keys_and_values():
    data = {"version": "1.0", "count": 3, "9ABCD": {"f": "9abcd.cif.gz"}}
    assert rj.process_json_data(data) == data


def test_process_value_recurses_into_lists_and_dicts():
    value = {"files": ["8zz1/a.cif.gz", {"p": "8zz1/b.json.gz"}], "n": 3}
    out = rj.process_value(value, "8zz1", "pdb_00008zz1")
    assert out == {"files": ["pdb_00008zz1/a.cif.gz", {"p": "pdb_00008zz1/b.json.gz"}], "n": 3}


def test_process_json_data_renames_pdb_id_keys():
    data = {
        "8ZZ1": {"mmcif": "8zz1/8zz1.cif.gz", "status": "REL"},
        "meta": {"note": "not a key"},
    }
    out = rj.process_json_data(data)
    assert set(out) == {"pdb_00008zz1", "meta"}
    assert out["pdb_00008zz1"] == {"mmcif": "pdb_00008zz1/pdb_00008zz1.cif.gz", "status": "REL"}
    assert out["meta"] == data["meta"]


def test_process_json_data_non_dict_passthrough():
    assert rj.process_json_data([1, 2]) == [1, 2]


def test_process_json_file_roundtrip(tmp_path):
    src = tmp_path / "in.json.gz"
    with gzip.open(src, "wt", encoding="utf-8") as f:
        json.dump({"9A9V": {"f": "9a9v/9a9v.cif.gz"}}, f)
    dst = tmp_path / "sub" / "out.json.gz"
    rj.process_json_file(str(src), str(dst))
    with gzip.open(dst, "rt", encoding="utf-8") as f:
        assert json.load(f) == {"pdb_00009a9v": {"f": "pdb_00009a9v/pdb_00009a9v.cif.gz"}}


def test_process_json_file_missing_input(tmp_path):
    with pytest.raises(Exception, match="does not exist"):
        rj.process_json_file(str(tmp_path / "nope.json.gz"), str(tmp_path / "out.json.gz"))
