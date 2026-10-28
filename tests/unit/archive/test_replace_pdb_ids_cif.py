import gzip
import io
import os

import pytest

from pdb_dev.processing.archive import replace_pdb_ids_cif as cif


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("pdb_id, expected", [
    ("8ZZ1", "pdb_00008zz1"),
    ("9a9v", "pdb_00009a9v"),
    ("1ABC", "pdb_00001abc"),
])
def test_convert_pdb_id(pdb_id, expected):
    assert cif.convert_pdb_id(pdb_id) == expected


@pytest.mark.parametrize("value", [None, "", "ABC", "ABCDE", "pdb_00008zz1"])
def test_convert_pdb_id_leaves_non_4_char_values(value):
    assert cif.convert_pdb_id(value) == value


@pytest.mark.parametrize("value, expected", [
    ("8ZZ1", True),
    (" 8ZZ1 ", True),
    ('"8ZZ1"', True),
    ("'8ZZ1'", True),
    ("1234", False),   # no letter
    ("ABCD", False),   # does not start with a digit
    ("8Z-1", False),   # not alphanumeric
    ("8ZZ", False),
    ("", False),
    (None, False),
])
def test_is_pdb_id(value, expected):
    assert cif.is_pdb_id(value) is expected


@pytest.mark.parametrize("value, expected", [
    ("ABCD", True),
    ("1234", True),
    ("8ZZ1", True),
    ("8Z-1", False),
    ("8ZZ12", False),
    (None, False),
])
def test_is_pdb_id_simple(value, expected):
    assert cif.is_pdb_id_simple(value) is expected


@pytest.mark.parametrize("line, expected", [
    ("_entry.id 9A9V\n", "_entry.id"),
    ("_citation.entry_id\n", "_citation.entry_id"),
    ("data_9A9V\n", "data_ block"),
    ("1 'x' 9A9V\n", ""),
])
def test_extract_field_name(line, expected):
    assert cif.extract_field_name(line) == expected


def test_find_pdb_ids_in_line_ignores_field_name_only_lines():
    assert cif.find_pdb_ids_in_line("_citation.entry_id\n", 1) == []


def test_find_pdb_ids_in_line_reports_offset_in_value_part():
    line = "_entry.id 9A9V\n"
    found = cif.find_pdb_ids_in_line(line, 1)
    assert len(found) == 1
    start, end, pdb_id, context = found[0]
    assert pdb_id == "9A9V"
    assert line[start:end] == "9A9V"
    assert context == "_entry.id"


def test_find_pdb_ids_in_line_data_row():
    found = cif.find_pdb_ids_in_line("1 'A title' 9A9V 7ABC\n", 1)
    assert [f[2] for f in found] == ["9A9V", "7ABC"]


# ---------------------------------------------------------------------------
# process_cif_file
# ---------------------------------------------------------------------------
SAMPLE_CIF = """data_9A9V
#
_entry.id 9A9V
#
_struct.entry_id   9A9V
_struct.title 'test'
#
loop_
_database_2.database_id
_database_2.database_code
PDB 9A9V
#
loop_
_citation.id
_citation.title
_citation.entry_id
1 'A title with spaces' 9A9V
2 "Another title" '9A9V'
#
_pdbx_database_status.entry_id 9A9V
"""


def _run(tmp_path, text, out_name="out.cif"):
    src = tmp_path / "in.cif"
    src.write_text(text)
    dst = tmp_path / out_name
    cif.process_cif_file(str(src), str(dst))
    return dst.read_text().splitlines()


def test_process_cif_replaces_single_value_fields(tmp_path):
    out = _run(tmp_path, SAMPLE_CIF)
    assert out[0] == "data_pdb_00009a9v"
    assert "_entry.id pdb_00009a9v" in out
    assert "_struct.entry_id   pdb_00009a9v" in out          # whitespace preserved
    assert "_pdbx_database_status.entry_id pdb_00009a9v" in out


def test_process_cif_does_not_touch_database_2_loop(tmp_path):
    out = _run(tmp_path, SAMPLE_CIF)
    assert "PDB 9A9V" in out


def test_process_cif_replaces_entry_id_column_in_loops(tmp_path):
    """Regression: bare loop headers like '_citation.entry_id' used to be swallowed by the single-value
    branch (\\s+ matched the newline), so loop entry_id columns were never converted."""
    out = _run(tmp_path, SAMPLE_CIF)
    assert "_citation.entry_id" in out
    assert "1 'A title with spaces' pdb_00009a9v" in out
    assert "2 \"Another title\" 'pdb_00009a9v'" in out       # original quoting preserved


def test_process_cif_entry_id_loop_header_keeps_column_index(tmp_path):
    text = """data_1ABC
loop_
_ihm_entry_collection_mapping.collection_id
_ihm_entry_collection_mapping.entry_id
C1 1ABC
C2 1ABC
#
"""
    out = _run(tmp_path, text)
    assert out[-3:-1] == ["C1 pdb_00001abc", "C2 pdb_00001abc"]


def test_process_cif_leaves_unrelated_content_unchanged(tmp_path):
    out = _run(tmp_path, SAMPLE_CIF)
    assert "_struct.title 'test'" in out
    assert out.count("#") == SAMPLE_CIF.splitlines().count("#")


def test_process_cif_gzip_roundtrip(tmp_path):
    src = tmp_path / "in.cif.gz"
    with gzip.open(src, "wt", encoding="utf-8") as f:
        f.write(SAMPLE_CIF)
    dst = tmp_path / "nested" / "out.cif.gz"
    cif.process_cif_file(str(src), str(dst))
    with gzip.open(dst, "rt", encoding="utf-8") as f:
        assert f.readline().strip() == "data_pdb_00009a9v"


def test_process_cif_output_in_current_directory(tmp_path, monkeypatch):
    """Regression: a bare output filename used to fail with os.makedirs('')."""
    src = tmp_path / "in.cif"
    src.write_text(SAMPLE_CIF)
    monkeypatch.chdir(tmp_path)
    cif.process_cif_file(str(src), "out.cif")
    assert (tmp_path / "out.cif").exists()


def test_process_cif_missing_input_raises(tmp_path):
    with pytest.raises(Exception, match="does not exist"):
        cif.process_cif_file(str(tmp_path / "missing.cif"), str(tmp_path / "out.cif"))


def test_process_cif_unknown_extension_raises(tmp_path):
    src = tmp_path / "in.txt"
    src.write_text(SAMPLE_CIF)
    with pytest.raises(Exception, match="unknown file extension"):
        cif.process_cif_file(str(src), str(tmp_path / "out.cif"))


def test_process_cif_latin1_input(tmp_path):
    src = tmp_path / "in.cif"
    src.write_bytes("data_9A9V\n_struct.title 'Caf\xe9'\n".encode("latin-1"))
    dst = tmp_path / "out.cif"
    cif.process_cif_file(str(src), str(dst))
    assert dst.read_text(encoding="utf-8").startswith("data_pdb_00009a9v")


# ---------------------------------------------------------------------------
# create_pdb_comparison
# ---------------------------------------------------------------------------
def test_create_pdb_comparison_reports_changes(tmp_path):
    src = tmp_path / "in.cif"
    src.write_text(SAMPLE_CIF)
    dst = tmp_path / "out.cif"
    cif.process_cif_file(str(src), str(dst))

    buf = io.StringIO()
    cif.create_pdb_comparison(str(src), str(dst), buf)
    report = buf.getvalue()
    assert "PDB ID Comparison Report" in report
    assert "CHANGED ENTRIES:" in report
    assert "UNCHANGED ENTRIES:" in report       # the _database_2 row stays
    assert "PDB 9A9V" in report


def test_process_cif_tab_separated_loop_keeps_tabs(tmp_path):
    text = "data_9A9V\nloop_\n_citation.id\n_citation.entry_id\n1\t9A9V\n#\n"
    out = _run(tmp_path, text)
    assert "1\tpdb_00009a9v" in out


def test_process_cif_multiple_entry_id_loops(tmp_path):
    text = ("data_9A9V\nloop_\n_citation.id\n_citation.entry_id\n1 9A9V\n#\n"
            "loop_\n_software.ordinal\n_software.name\n1 IMP\n#\n"
            "loop_\n_audit_author.entry_id\n_audit_author.name\n9A9V 'Doe, J.'\n#\n")
    out = _run(tmp_path, text)
    assert "1 pdb_00009a9v" in out
    assert "1 IMP" in out                                  # loop without entry_id untouched
    assert "pdb_00009a9v 'Doe, J.'" in out


def test_process_cif_ignores_non_pdb_values_in_entry_id_column(tmp_path):
    text = "data_9A9V\nloop_\n_citation.id\n_citation.entry_id\n1 D_1-ABCD\n2 .\n#\n"
    out = _run(tmp_path, text)
    assert "1 D_1-ABCD" in out and "2 ." in out


def test_process_cif_data_block_with_non_pdb_name_unchanged(tmp_path):
    out = _run(tmp_path, "data_D_1-ABCD\n_entry.id D_1-ABCD\n")
    assert out == ["data_D_1-ABCD", "_entry.id D_1-ABCD"]


def test_process_cif_is_idempotent(tmp_path):
    first = _run(tmp_path, SAMPLE_CIF, "first.cif")
    second = _run(tmp_path, "\n".join(first) + "\n", "second.cif")
    assert second == first


def test_create_pdb_comparison_skips_atom_site_rows(tmp_path):
    src = tmp_path / "in.cif"
    src.write_text("data_9A9V\n_entry.id 9A9V\n#\nloop_\n_atom_site.group_PDB\n_atom_site.label_comp_id\n"
                   "ATOM 1ABC\nHETATM 2DEF\n#\n")
    dst = tmp_path / "out.cif"
    cif.process_cif_file(str(src), str(dst))
    buf = io.StringIO()
    cif.create_pdb_comparison(str(src), str(dst), buf)
    report = buf.getvalue()
    assert "1ABC" not in report and "2DEF" not in report
    assert "_entry.id" in report


def test_create_pdb_comparison_no_ids(tmp_path):
    src = tmp_path / "in.cif"
    src.write_text("data_test\n_struct.title 'nothing here'\n")
    buf = io.StringIO()
    cif.create_pdb_comparison(str(src), str(src), buf)
    assert "No PDB IDs found" in buf.getvalue()
