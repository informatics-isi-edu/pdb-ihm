"""ArchiveProcessor helpers: archive date, path/hash helpers, gzip, holdings ordering, Hatrac upload.

ArchiveProcessor.__init__ always connects to the server (it does not accept an injected catalog/store), so
these tests build the object with __new__ and set only the attributes each method uses.
"""
import gzip
import logging
from datetime import datetime
from types import SimpleNamespace
from unittest import mock

import pytest
import pytz

ap = pytest.importorskip("pdb_dev.processing.archive.archive_processor")

LA = pytz.timezone("America/Los_Angeles")


@pytest.fixture
def proc(tmp_path):
    p = ap.ArchiveProcessor.__new__(ap.ArchiveProcessor)
    p.logger = logging.getLogger("test_archive_processor")
    p.verbose = False
    p.cutoff_time_pacific = "Thursday 21:00"
    p.released_entry_dir = "released"
    p.catalog = mock.MagicMock()
    p.store = mock.MagicMock()
    p.host, p.catalog_id = "example.org", "99"
    return p


def frozen_now(naive_local):
    class FakeDT(datetime):
        @classmethod
        def now(cls, tz=None):
            aware = LA.localize(naive_local)
            return aware.astimezone(tz) if tz else aware
    return mock.patch.object(ap, "dt", FakeDT)


# ---------------------------------------------------------------------------
# getArchiveDate / getPreviousArchiveDate / getTimeUTC
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("now, expected", [
    (datetime(2025, 6, 2, 9, 0), "2025-06-05 21:00:00-07:00"),    # Monday -> this Thursday
    (datetime(2025, 6, 5, 21, 0), "2025-06-05 21:00:00-07:00"),   # exactly at cutoff
    (datetime(2025, 6, 5, 21, 1), "2025-06-12 21:00:00-07:00"),   # after cutoff -> next week
    (datetime(2025, 6, 7, 8, 0), "2025-06-12 21:00:00-07:00"),    # Saturday -> next week
])
def test_get_archive_date(proc, now, expected):
    with frozen_now(now):
        assert proc.getArchiveDate() == expected


def test_get_archive_date_matches_pipeline_processor_outside_dst_change(proc):
    """ArchiveProcessor has its own copy of the cutoff logic; keep it consistent with PipelineProcessor."""
    import pdb_dev.processing.processor as base
    with frozen_now(datetime(2025, 6, 3, 12, 0)):
        with mock.patch.object(base, "dt", ap.dt):           # same frozen clock for both implementations
            assert proc.getArchiveDate() == ap.PipelineProcessor.get_archive_datetime(proc)


@pytest.mark.xfail(strict=True, reason="known, intentionally deferred: getArchiveDate keeps the UTC offset of 'now' "
                                       "(pytz), so in a DST-change week the archive time is one hour off. See the TODO "
                                       "in ArchiveProcessor.__init__ to switch to self.get_archive_datetime().")
def test_get_archive_date_across_dst_end(proc):
    with frozen_now(datetime(2025, 11, 1, 10, 0)):                  # PDT now; next Thursday is PST
        assert proc.getArchiveDate() == "2025-11-06 21:00:00-08:00"


def test_get_previous_archive_date_from_db(proc):
    proc.catalog.get.return_value.json.return_value = [{"previous_submission_time": "2025-05-29T21:00:00-07:00"}]
    assert proc.getPreviousArchiveDate("2025-06-05 21:00:00-07:00") == "2025-05-29 21:00:00-07:00"
    assert "Submission_Time::lt::" in proc.catalog.get.call_args.args[0]


def test_get_previous_archive_date_defaults_to_one_week(proc):
    proc.catalog.get.return_value.json.return_value = [{"previous_submission_time": None}]
    assert proc.getPreviousArchiveDate("2025-06-05 21:00:00-07:00") == "2025-05-29 21:00:00-07:00"


def test_get_time_utc(proc):
    assert proc.getTimeUTC("2025-06-05 21:00:00-07:00") == "2025-06-06T04:00:00+00:00"


# ---------------------------------------------------------------------------
# path / hash helpers
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("code, h", [("9ABC", "ab"), ("8zz1", "zz")])
def test_get_hash(proc, code, h):
    assert proc.get_hash(code) == h


@pytest.mark.parametrize("code", ["pdb_00009abc", "ABC", ""])
def test_get_hash_rejects_non_pdb_codes(proc, code):
    with pytest.raises(Exception, match="Expect legnth of 4"):
        proc.get_hash(code)


def test_get_file_archive_sub_directory2(proc):
    assert proc.getFileArchiveSubDirectory2("9ABC", "structures") == "released/ab/9abc/structures"


@pytest.mark.parametrize("filename, expected", [
    ("local/file.cif", "local/file.cif"),
    ("/hatrac/pdb/generated/uid/u/entry/id/D_1/9ABC.cif:VERSION", "/hatrac/pdb/generated/uid/u/entry/9abc.cif.gz"),
])
def test_get_submitted_zip_file(proc, filename, expected):
    assert proc.getSubmittedZipFile(filename) == expected


def test_order_dict_sorts_keys_and_lists_recursively(proc):
    data = {"b": [3, 1, 2], "a": {"z": 1, "y": ["b", "a"]}, "c": "x"}
    out = proc.order_dict(data)
    assert list(out) == ["a", "b", "c"]
    assert list(out["a"]) == ["y", "z"]
    assert out["b"] == [1, 2, 3] and out["a"]["y"] == ["a", "b"]


def test_order_dict_list_of_dicts_is_unsupported(proc):
    """Documents current behavior: lists are sorted directly, so a list of dicts raises TypeError."""
    with pytest.raises(TypeError):
        proc.order_dict({"entries": [{"id": 2}, {"id": 1}]})


def test_generate_gzip_roundtrip(proc, tmp_path):
    src = tmp_path / "holdings.json"
    src.write_text('{"9ABC": {}}')
    out = proc.generateGzip(str(src), output_dir=str(tmp_path / "out"))
    assert out == str(tmp_path / "out" / "holdings.json.gz")
    assert gzip.open(out, "rt").read() == '{"9ABC": {}}'
    assert not src.exists()


def test_generate_gzip_keeps_input(proc, tmp_path):
    src = tmp_path / "holdings.json"
    src.write_text("{}")
    assert proc.generateGzip(str(src), delete_input=False) == str(tmp_path / "holdings.json.gz")
    assert src.exists()


# ---------------------------------------------------------------------------
# getHatracFile / storeFileInHatrac
# ---------------------------------------------------------------------------
def test_get_hatrac_file(proc, tmp_path):
    proc.store.get_obj.side_effect = lambda url, destfilename: open(destfilename, "w").write("x")
    assert proc.getHatracFile("/hatrac/a", str(tmp_path), "f.json") == str(tmp_path / "f.json")


def test_get_hatrac_file_error(proc, tmp_path):
    proc.store.get_obj.side_effect = RuntimeError("404")
    with pytest.raises(ap.FileError) as exc:
        proc.getHatracFile("/hatrac/a", str(tmp_path), "f.json")
    assert "/hatrac/a" in exc.value.details


@pytest.fixture
def holdings(tmp_path):
    path = tmp_path / "current_file_holdings.json.gz"
    with gzip.open(path, "wt") as f:
        f.write('{"9abc": {}}')
    return path


def _existing_object(content_location, source=None):
    """get_obj fake: Hatrac already has an object (copy of `source`, or different bytes if None)."""
    def get_obj(url, destfilename):
        data = source.read_bytes() if source else b"different"
        with open(destfilename, "wb") as f:
            f.write(data)
        return SimpleNamespace(headers={"Content-Location": content_location})
    return get_obj


def _missing_object(url, destfilename):
    open(destfilename, "wb").close()        # HatracStore.get_obj creates the file before the request fails
    raise RuntimeError("404 Not Found")


def test_store_file_new_object_is_uploaded(proc, holdings):
    proc.store.get_obj.side_effect = _missing_object
    proc.store.put_loc.return_value = "/hatrac/ns/current_file_holdings.json.gz:V1"
    url, name, size, md5 = proc.storeFileInHatrac("/hatrac/ns", str(holdings))
    assert (url, name, size) == ("/hatrac/ns/current_file_holdings.json.gz:V1", holdings.name, holdings.stat().st_size)
    assert len(md5) == 32
    assert proc.store.put_loc.call_args.args[0] == "/hatrac/ns/current_file_holdings.json.gz"
    assert not (holdings.parent / (holdings.name + ".hatrac")).exists()       # temp download cleaned up


def test_store_file_unchanged_object_is_not_reuploaded(proc, holdings):
    proc.store.get_obj.side_effect = _existing_object("/hatrac/ns/x:V0", source=holdings)
    url, *_ = proc.storeFileInHatrac("/hatrac/ns", str(holdings))
    assert url == "/hatrac/ns/x:V0"
    proc.store.put_loc.assert_not_called()


def test_store_file_changed_object_is_reuploaded(proc, holdings):
    proc.store.get_obj.side_effect = _existing_object("/hatrac/ns/x:V0")
    proc.store.put_loc.return_value = "/hatrac/ns/x:V1"
    assert proc.storeFileInHatrac("/hatrac/ns", str(holdings))[0] == "/hatrac/ns/x:V1"


def test_store_file_not_modified_keeps_old_version(proc, holdings):
    proc.store.get_obj.side_effect = _existing_object("/hatrac/ns/x:V0")
    proc.store.put_loc.side_effect = ap.NotModified("same content")
    assert proc.storeFileInHatrac("/hatrac/ns", str(holdings))[0] == "/hatrac/ns/x:V0"


def test_store_file_upload_error(proc, holdings):
    proc.store.get_obj.side_effect = _missing_object
    proc.store.put_loc.side_effect = RuntimeError("403 Forbidden")
    with pytest.raises(ap.FileError) as exc:
        proc.storeFileInHatrac("/hatrac/ns", str(holdings))
    assert "/hatrac/ns/current_file_holdings.json.gz" in exc.value.details
