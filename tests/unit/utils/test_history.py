from datetime import datetime, timezone, timedelta
from types import SimpleNamespace

import pytest

from pdb_dev.utils import history

ALPHABET = '0123456789ABCDEFGHJKMNPQRSTVWXYZ'


def urlb32_decode(s):
    """Reference decoder for ERMrest's snapshot encoding (inverse of history.urlb32_encode)."""
    raw = 0
    for ch in s.replace('-', ''):
        raw = raw * 32 + ALPHABET.index(ch)
    return raw >> 1


# ---------------------------------------------------------------------------
# history
# ---------------------------------------------------------------------------
def test_urlb32_encode_zero():
    assert history.urlb32_encode(0) == '0'


@pytest.mark.parametrize("i", [1, 31, 32, 12345, 1_700_000_000_000_000, 2**63 - 1])
def test_urlb32_encode_roundtrip(i):
    assert urlb32_decode(history.urlb32_encode(i)) == i


def test_urlb32_encode_groups_with_dashes():
    encoded = history.urlb32_encode(1_700_000_000_000_000)
    assert all(len(group) == 4 for group in encoded.split('-')[1:])


@pytest.mark.parametrize("i", [2**63, -2**63 - 1])
def test_urlb32_encode_out_of_range(i):
    with pytest.raises(ValueError):
        history.urlb32_encode(i)


def test_urlb32_encode_is_monotonic():
    a = history.urlb32_encode(1_700_000_000_000_000)
    b = history.urlb32_encode(1_700_000_000_000_001)
    assert urlb32_decode(b) > urlb32_decode(a)


def test_datetime_epoch_us():
    dt = datetime(2024, 1, 1, 0, 0, 0, 123456, tzinfo=timezone.utc)
    assert history.datetime_epoch_us(dt) == 1704067200 * 1_000_000 + 123456


def test_iso_to_snap_matches_encode():
    iso = "2024-01-01T00:00:00.123456+00:00"
    assert history.iso_to_snap(iso) == history.urlb32_encode(1704067200 * 1_000_000 + 123456)


def test_iso_to_snap_timezone_independent():
    utc = "2024-06-01T12:00:00+00:00"
    pdt = "2024-06-01T05:00:00-07:00"
    assert history.iso_to_snap(utc) == history.iso_to_snap(pdt)


# ---------------------------------------------------------------------------
# get_record_history: walks back through snapshots using each version's RMT
# ---------------------------------------------------------------------------
class FakeServer:
    """Serves /ermrest/catalog/<cid> and /ermrest/catalog/<cid>@<snap>/entity/... from a version list."""

    def __init__(self, versions, latest_snap="LATEST"):
        self.versions = versions        # newest first: [{"RMT": ..., ...}, ...]
        self.latest_snap = latest_snap
        self.urls = []

    def get(self, url):
        self.urls.append(url)
        if "@" not in url:
            return SimpleNamespace(json=lambda: {"snaptime": self.latest_snap})
        snap = url.split("@", 1)[1].split("/", 1)[0]
        if snap == self.latest_snap:
            rows = self.versions[:1]
        else:
            # snapshot just before version i's birth time -> version i+1
            snaps = [history.urlb32_encode(history.datetime_epoch_us(datetime.fromisoformat(v["RMT"])) - 1)
                     for v in self.versions]
            i = snaps.index(snap)
            rows = self.versions[i + 1:i + 2]
        return SimpleNamespace(json=lambda rows=rows: rows)


VERSIONS = [
    {"RID": "2-TK8P", "RMT": "2024-03-01T10:00:00+00:00", "Workflow_Status": "REL"},
    {"RID": "2-TK8P", "RMT": "2024-02-01T10:00:00+00:00", "Workflow_Status": "HOLD"},
    {"RID": "2-TK8P", "RMT": "2024-01-01T10:00:00+00:00", "Workflow_Status": "DEPO"},
]


def test_get_record_history_walks_all_versions(capsys):
    server = FakeServer(VERSIONS)
    snap2rows = history.get_record_history(server, "1", "PDB", "entry", ["2-TK8P"])
    assert [r["Workflow_Status"] for r in snap2rows.values()] == ["REL", "HOLD", "DEPO"]
    assert list(snap2rows)[0] == "LATEST"
    assert server.urls[0] == "/ermrest/catalog/1"
    assert server.urls[1] == "/ermrest/catalog/1@LATEST/entity/PDB:entry/RID=2-TK8P"


def test_get_record_history_from_given_snapshot():
    server = FakeServer(VERSIONS)
    history.get_record_history(server, "1", "PDB", "entry", ["2-TK8P"], snap="LATEST")
    assert server.urls[0] == "/ermrest/catalog/1@LATEST/entity/PDB:entry/RID=2-TK8P"   # no catalog lookup


def test_get_record_history_quotes_keys():
    server = FakeServer(VERSIONS[:1])
    history.get_record_history(server, "1", "PDB", "entry", ["a b", "x"], kcols=["My Col", "RID"])
    assert server.urls[1].endswith("/entity/PDB:entry/My%20Col=a%20b,RID=x")


def test_get_record_history_rejects_non_unique_key():
    server = FakeServer(VERSIONS)
    server.get = lambda url: SimpleNamespace(json=lambda: {"snaptime": "S"} if "@" not in url else VERSIONS[:2])
    with pytest.raises(ValueError, match="more than one row"):
        history.get_record_history(server, "1", "PDB", "entry", ["2-TK8P"])
