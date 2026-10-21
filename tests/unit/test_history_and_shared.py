from datetime import datetime, timezone, timedelta

import pytest

from pdb_dev.utils import history
from pdb_dev.utils.shared import Config

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
# shared.Config
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("host, catalog_id, name, flag, hatrac_root", [
    ("data.pdb-ihm.org", "1", "prod", "is_prod", "/hatrac"),
    ("data-dev.pdb-ihm.org", "50", "staging", "is_staging", "/hatrac"),
    ("data-dev.pdb-ihm.org", 150, "staging", "is_staging", "/hatrac"),
    ("dev.pdb-dev.org", "50", "staging", "is_staging", "/hatrac"),
    ("data-dev.pdb-ihm.org", "99", "dev", "is_dev", "/hatrac/dev"),
    ("localhost", "1", "dev", "is_dev", "/hatrac/dev"),
])
def test_config_apply_hostname(host, catalog_id, name, flag, hatrac_root):
    cfg = Config()
    cfg.apply_hostname(host, catalog_id)
    assert cfg.catalog_name == name
    assert getattr(cfg, flag) is True
    assert cfg.hatrac_root == hatrac_root
    assert sum([cfg.is_prod, cfg.is_staging, cfg.is_dev]) == 1


def test_config_reapply_resets_flags():
    """Regression: cfg is a module singleton; re-applying a different host left stale flags/hatrac_root."""
    cfg = Config()
    cfg.apply_hostname("data-dev.pdb-ihm.org", "99")
    cfg.apply_hostname("data.pdb-ihm.org", "1")
    assert cfg.is_prod and not cfg.is_dev
    assert cfg.hatrac_root == "/hatrac"
