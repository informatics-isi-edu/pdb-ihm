"""CIF serialization: getColumnValue, writeTableToCif, exportCIFContent.

Round-trip tests parse the written text with python-ihm's CifReader, so they check that the output is
valid CIF that decodes back to the original value, not just that it matches a string.
"""
import io

import ihm.format
import pytest

from ep_helpers import ep


class _Collector:
    """Minimal python-ihm category handler that records the raw values."""
    not_in_file = None
    omitted = None
    unknown = "?"
    _int_keys = _float_keys = _bool_keys = ()

    def __init__(self, keys):
        self._keys = list(keys)
        self.rows = []

    def __call__(self, *values):
        self.rows.append(dict(zip(self._keys, values)))

    def end_save_frame(self):
        pass


def parse(text, category, keys):
    handler = _Collector(keys)
    ihm.format.CifReader(io.StringIO(text), {f"_{category}": handler}).read_file()
    return handler.rows


@pytest.fixture
def proc(make_processor):
    return make_processor()


# ---------------------------------------------------------------------------
# getColumnValue: string-level expectations
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("ctype, value, expected", [
    ("text", None, "."),
    ("int4", None, "."),
    ("int4", 42, "42"),
    ("float4", 1.5, "1.5"),
    ("text", "plain", "plain"),
    ("text", "has space", '"has space"'),
    ("text", "_starts_with_underscore", '"_starts_with_underscore"'),
    ("text", 'say "hi"', "'say \"hi\"'"),
    ("text", "it's", '"it\'s"'),
    ("text", "smart “quotes”", "'smart “quotes”'"),
    ("text", "both ' and \"", "\n;both ' and \"\n;\n"),
    ("text", "line1\nline2", "\n;line1\nline2\n;\n"),
])
def test_get_column_value(proc, ctype, value, expected):
    assert proc.getColumnValue("t", "c", ctype, value) == expected


def test_get_column_value_rejects_tab(proc):
    with pytest.raises(ep.ProcessingError, match="tab character"):
        proc.getColumnValue("t", "c", "text", "a\tb")


@pytest.mark.parametrize("ctype", ["int8", "float8", "boolean", "date", "timestamptz"])
def test_get_column_value_rejects_unsupported_types(proc, ctype):
    with pytest.raises(ep.ProcessingError, match="unknown type"):
        proc.getColumnValue("t", "c", ctype, 1)


# ---------------------------------------------------------------------------
# getColumnValue: round-trip through a CIF parser
# ---------------------------------------------------------------------------
ROUNDTRIP_VALUES = [
    "plain", "has space", "_underscore", 'say "hi"', "it's", "both ' and \"", "multi\nline\ntext",
    "9A9V", "1.5", "x" * 300,
]


@pytest.mark.parametrize("value", ROUNDTRIP_VALUES)
def test_get_column_value_roundtrips_single_row(proc, value):
    buf = io.StringIO("data_test\n")
    proc.writeTableToCif("t", {"v": "text"}, [{"v": value}], buf)
    assert parse(buf.getvalue(), "t", ["v"]) == [{"v": value}]


@pytest.mark.parametrize("value", ROUNDTRIP_VALUES)
def test_get_column_value_roundtrips_in_loop(proc, value):
    buf = io.StringIO("data_test\n")
    proc.writeTableToCif("t", {"id": "int4", "v": "text"}, [{"id": 1, "v": value}, {"id": 2, "v": "x"}], buf)
    assert parse(buf.getvalue(), "t", ["id", "v"]) == [{"id": "1", "v": value}, {"id": "2", "v": "x"}]


@pytest.mark.parametrize("ctype", ["text", "int4", "float4"])
def test_get_column_value_empty_string_is_omitted(proc, ctype):
    """An empty string is treated the same as None: written as '.' (omitted)."""
    assert proc.getColumnValue("t", "a", ctype, "") == "."


def test_get_column_value_empty_string_keeps_loop_columns_aligned(proc):
    buf = io.StringIO("data_test\n")
    proc.writeTableToCif("t", {"a": "text", "b": "text"}, [{"a": "", "b": "x"}, {"a": "y", "b": "z"}], buf)
    assert parse(buf.getvalue(), "t", ["a", "b"]) == [{"a": None, "b": "x"}, {"a": "y", "b": "z"}]


@pytest.mark.parametrize("value", ["loop_", "data_x", "save_frame", "stop_", "global_", "LOOP_", "Data_x"])
def test_get_column_value_cif_keywords_are_quoted(proc, value):
    """CIF keywords (data_, save_, loop_, stop_, global_; case-insensitive) must be quoted to survive parsing."""
    assert proc.getColumnValue("t", "v", "text", value) == f'"{value}"'
    buf = io.StringIO("data_test\n")
    proc.writeTableToCif("t", {"id": "int4", "v": "text"}, [{"id": 1, "v": value}, {"id": 2, "v": "x"}], buf)
    assert parse(buf.getvalue(), "t", ["id", "v"])[0]["v"] == value


@pytest.mark.parametrize("value", ["datax", "loops", "my_data_"])
def test_get_column_value_keyword_lookalikes_stay_unquoted(proc, value):
    assert proc.getColumnValue("t", "v", "text", value) == value


# ---------------------------------------------------------------------------
# writeTableToCif layout
# ---------------------------------------------------------------------------
def test_write_table_to_cif_empty_writes_nothing(proc):
    buf = io.StringIO()
    proc.writeTableToCif("t", {"a": "text"}, [], buf)
    assert buf.getvalue() == ""


def test_write_table_to_cif_single_row_is_key_value(proc):
    buf = io.StringIO()
    proc.writeTableToCif("struct", {"entry_id": "text", "title": "text"},
                         [{"entry_id": "D_1", "title": "A title", "ignored": 1}], buf)
    assert buf.getvalue() == '_struct.entry_id\tD_1\n_struct.title\t"A title"\n#\n'


def test_write_table_to_cif_multiple_rows_is_loop_in_column_order(proc):
    buf = io.StringIO()
    proc.writeTableToCif("t", {"b": "int4", "a": "text"}, [{"a": "x", "b": 1}, {"a": None, "b": 2}], buf)
    assert buf.getvalue() == "loop_\n_t.b\n_t.a\n1\tx\n2\t.\n#\n"


def test_write_table_to_cif_missing_column_raises(proc):
    with pytest.raises(KeyError):
        proc.writeTableToCif("t", {"a": "text"}, [{"b": 1}], io.StringIO())


# ---------------------------------------------------------------------------
# exportCIFContent: copy selected categories from the make_mmcif output
# ---------------------------------------------------------------------------
SUBMITTED = """data_test
#
_entry.id test
#
_struct.title 'from file'
#
loop_
_ihm_model_list.model_id
_ihm_model_list.model_name
1 'model one'
2 'model two'
#
loop_
_ihm_2dem_class_average_fitting.id
_ihm_2dem_class_average_fitting.rot_matrix_1_1
_ihm_2dem_class_average_fitting.rot_matrix_2_3
1 0.5 0.25
#
_flr_experiment.id 1
#
loop_
_ihm_entry_collection.id
_ihm_entry_collection.name
C1 'collection'
#
_not_exported.x 1
#
"""


def run_export(proc, tmp_path, cif_tables, deriva_tables):
    src = tmp_path / "out.cif"
    src.write_text(SUBMITTED)
    proc.cif_tables = cif_tables
    buf = io.StringIO()
    proc.exportCIFContent(buf, str(src), deriva_tables)
    return buf.getvalue()


def test_export_cif_content_copies_only_requested_tables(proc, tmp_path):
    out = run_export(proc, tmp_path, ["ihm_model_list"], ["entry"])
    assert out == ("loop_\n_ihm_model_list.model_id\n_ihm_model_list.model_name\n"
                   "1 'model one'\n2 'model two'\n#\n")


def test_export_cif_content_skips_tables_already_exported_from_ermrest(proc, tmp_path):
    out = run_export(proc, tmp_path, ["ihm_model_list", "struct"], ["entry", "struct"])
    assert "_struct.title" not in out
    assert "_ihm_model_list.model_id" in out


def test_export_cif_content_rewrites_matrix_columns(proc, tmp_path):
    out = run_export(proc, tmp_path, ["ihm_2dem_class_average_fitting"], [])
    assert "_ihm_2dem_class_average_fitting.rot_matrix[1][1]" in out
    assert "_ihm_2dem_class_average_fitting.rot_matrix[2][3]" in out
    assert "rot_matrix_1_1" not in out


def test_export_cif_content_never_copies_flr_or_collection_tables(proc, tmp_path):
    out = run_export(proc, tmp_path, ["ihm_entry_collection", "flr_experiment"], [])
    assert "_flr_" not in out and "ihm_entry_collection" not in out


def test_export_cif_content_output_is_parseable(proc, tmp_path):
    out = run_export(proc, tmp_path, ["ihm_model_list"], [])
    rows = parse("data_x\n" + out, "ihm_model_list", ["model_id", "model_name"])
    assert rows == [{"model_id": "1", "model_name": "model one"}, {"model_id": "2", "model_name": "model two"}]


def test_export_cif_content_malformed_loop_raises(proc, tmp_path):
    src = tmp_path / "bad.cif"
    src.write_text("data_x\nloop_\nnot-a-header\n")
    with pytest.raises(ep.FileError):
        proc.exportCIFContent(io.StringIO(), str(src), [])
