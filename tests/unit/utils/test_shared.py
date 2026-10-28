"""pdb_dev.utils.shared: Config environment detection and the PDBDEV_CLI argument defaults."""
import pytest

from pdb_dev.utils import shared
from pdb_dev.utils.shared import Config


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


def test_config_staging_requires_staging_catalog():
    cfg = Config()
    cfg.apply_hostname("validate-dev.pdb-ihm.org", "50")
    assert cfg.is_staging
    cfg.apply_hostname("validate-dev.pdb-ihm.org", "51")
    assert cfg.is_dev and cfg.hatrac_root == "/hatrac/dev"


# ---------------------------------------------------------------------------
# PDBDEV_CLI
# ---------------------------------------------------------------------------
@pytest.fixture
def fresh_cfg(monkeypatch):
    """parse_cli() writes into the module-level cfg singleton; isolate it per test."""
    cfg = Config()
    monkeypatch.setattr(shared, "cfg", cfg)
    return cfg


def parse(monkeypatch, argv, **env):
    for k in ["PDB_SERVER", "CATALOG", "PDB_CREDENTIALS", "RID", "rid"]:
        monkeypatch.delenv(k, raising=False)
    for k, v in env.items():
        monkeypatch.setenv(k, v)
    monkeypatch.setattr("sys.argv", ["prog"] + argv)
    return shared.PDBDEV_CLI("test", None, 1).parse_cli()


def test_cli_defaults(monkeypatch, fresh_cfg):
    args = parse(monkeypatch, [])
    assert (args.host, args.catalog_id, args.credential_file, args.rid) == ("data-dev.pdb-ihm.org", "99", None, None)
    assert (args.dry_run, args.pre_print, args.post_print) == (False, False, False)
    assert fresh_cfg.is_dev and fresh_cfg.args is args


def test_cli_defaults_from_environment(monkeypatch, fresh_cfg):
    args = parse(monkeypatch, [], PDB_SERVER="data.pdb-ihm.org", CATALOG="1", PDB_CREDENTIALS="/c.json", rid="1-X")
    assert (args.host, args.catalog_id, args.credential_file, args.rid) == ("data.pdb-ihm.org", "1", "/c.json", "1-X")
    assert fresh_cfg.is_prod


def test_cli_arguments_override_environment(monkeypatch, fresh_cfg):
    args = parse(monkeypatch, ["--host", "data-dev.pdb-ihm.org", "--catalog-id", "50", "--rid", "2-Y", "--dry-run"],
                 PDB_SERVER="data.pdb-ihm.org", CATALOG="1")
    assert (args.host, args.catalog_id, args.rid, args.dry_run) == ("data-dev.pdb-ihm.org", "50", "2-Y", True)
    assert fresh_cfg.is_staging


def test_cli_required_rid(monkeypatch, fresh_cfg):
    monkeypatch.setattr("sys.argv", ["prog"])
    for k in ["RID", "rid"]:
        monkeypatch.delenv(k, raising=False)
    with pytest.raises(SystemExit):
        shared.PDBDEV_CLI("test", None, 1, rid_required=True).parse_cli()


def test_dcctx_values_are_short_strings():
    flat = [v for v in shared.DCCTX.values() if isinstance(v, str)] + list(shared.DCCTX["pipelines"].values())
    assert all(isinstance(v, str) and v for v in flat)
