"""The per-area annotation scripts (pdb_dev/config/annotation/*.py, ihmv/*.py): main() and the __main__ block.

Most tests run each script against a mocked catalog model. The --pre-print/--post-print checks there only look for
errors raised by the scripts themselves (e.g. NameError); json.dumps is stubbed because the mocked annotations
aren't JSON. The print helpers are also tested against a real (offline) deriva Model.
"""
import copy
import importlib
import runpy
import types
from unittest import mock

import pytest
from deriva.core import ermrest_model as em, tag

PKG = "pdb_dev.config.annotation"
SCRIPTS = [f"{PKG}.{name}" for name in
           ["PDB", "PDB_base", "PDB_ihm", "Vocab", "asset", "bulk_upload", "catalog_annotations", "citation", "export",
            "public", "ihmv.IHMV", "ihmv.Vocab", "ihmv.asset", "ihmv.bulk_upload", "ihmv.catalog_annotations",
            "ihmv.export", "ihmv.public"]]

# main() never calls model.apply() in these scripts: `#model.apply()` (PDB_base, PDB_ihm) or a `return` before the
# post-print/apply block (public, ihmv/public). Documented here; change the list if that is not intended.
NEVER_APPLY = {f"{PKG}.PDB_base", f"{PKG}.PDB_ihm", f"{PKG}.public", f"{PKG}.ihmv.public"}



def run(module_name, monkeypatch, **flags):
    module = importlib.import_module(module_name)
    server = mock.MagicMock()
    monkeypatch.setattr(module, "DerivaServer", mock.MagicMock(return_value=server))
    monkeypatch.setattr("json.dumps", lambda *a, **k: "{}")
    monkeypatch.setattr("builtins.print", lambda *a, **k: None)
    args = types.SimpleNamespace(**{"pre_print": False, "post_print": False, "dry_run": False, **flags})
    module.main("data-dev.pdb-ihm.org", "99", {"cookie": "x"}, args)
    return module, server


@pytest.mark.parametrize("module_name", SCRIPTS)
def test_main_connects_and_applies(module_name, monkeypatch):
    module, server = run(module_name, monkeypatch)
    module.DerivaServer.assert_called_once_with("https", "data-dev.pdb-ihm.org", {"cookie": "x"})
    server.connect_ermrest.assert_called_once_with("99")
    model = server.connect_ermrest.return_value.getCatalogModel.return_value
    assert model.apply.call_count == (0 if module_name in NEVER_APPLY else 1)


@pytest.mark.parametrize("module_name", SCRIPTS)
def test_main_dry_run_does_not_apply(module_name, monkeypatch):
    _, server = run(module_name, monkeypatch, dry_run=True)
    server.connect_ermrest.return_value.getCatalogModel.return_value.apply.assert_not_called()


@pytest.mark.parametrize("module_name", SCRIPTS)
def test_main_pre_print(module_name, monkeypatch):
    run(module_name, monkeypatch, pre_print=True, dry_run=True)


@pytest.mark.parametrize("module_name", SCRIPTS)
def test_main_post_print(module_name, monkeypatch):
    """Regression: asset, citation and ihmv/asset called print_schema_annotations(model, schema_name) (both undefined);
    ihmv/asset --pre-print called print_asset_annotations, which wasn't defined there."""
    run(module_name, monkeypatch, post_print=True, dry_run=True)


@pytest.mark.filterwarnings("ignore:.*found in sys.modules:RuntimeWarning")    # re-running an imported module
@pytest.mark.parametrize("module_name", SCRIPTS)
def test_running_script_passes_cli_args_to_main(module_name, monkeypatch):
    """Regression (master 50d6003): bulk_upload's main() read a global `args`, and --debug used init_logging/logging
    without importing them. Runs each file as __main__ with --debug --dry-run."""
    import deriva.core
    server = mock.MagicMock()
    monkeypatch.setattr(deriva.core, "DerivaServer", mock.MagicMock(return_value=server))
    monkeypatch.setattr(deriva.core, "get_credential", mock.MagicMock(return_value={}))
    monkeypatch.setattr("sys.argv", ["prog", "--host", "example.org", "--catalog-id", "42", "--debug", "--dry-run"])
    monkeypatch.setattr("json.dumps", lambda *a, **k: "{}")
    runpy.run_module(module_name, run_name="__main__")
    deriva.core.get_credential.assert_called_once_with("example.org", None)
    server.connect_ermrest.assert_called_once_with("42")
    server.connect_ermrest.return_value.getCatalogModel.return_value.apply.assert_not_called()


# ---------------------------------------------------------------------------
# print helpers against a real (offline) deriva Model
# ---------------------------------------------------------------------------
ASSET = {"url_pattern": "/hatrac/x/{{{MD5}}}", "filename_column": "File_Name"}
CITATION = {"journal_pattern": "PDB-IHM", "year_pattern": "{{{Year}}}"}


def real_model():
    def col(name, ann=None):
        return {"name": name, "type": {"typename": "text"}, "nullok": True, "annotations": ann or {},
                "comment": None, "default": None}

    def table(sname, tname, cols, ann=None):
        return {"schema_name": sname, "table_name": tname, "kind": "table", "comment": None,
                "annotations": ann or {}, "column_definitions": cols, "keys": [], "foreign_keys": []}
    doc = {"annotations": {}, "schemas": {"PDB": {"schema_name": "PDB", "annotations": {}, "comment": None, "tables": {
        "entry": table("PDB", "entry", [col("File_URL", {tag["asset"]: ASSET}), col("Title")],
                       {tag["citation"]: CITATION}),
        "plain": table("PDB", "plain", [col("Name")]),
    }}}}
    return em.Model(mock.MagicMock(), copy.deepcopy(doc))


def annotations_of(model):
    out = {}
    for s in model.schemas.values():
        for t in s.tables.values():
            out[(s.name, t.name)] = dict(t.annotations)
            for c in t.columns:
                out[(s.name, t.name, c.name)] = dict(c.annotations)
    return out


@pytest.mark.parametrize("module_name, printer, expected", [
    (f"{PKG}.asset", "print_asset_annotations",
     'model.schemas["PDB"].tables["entry"].columns["File_URL"].asset.update('),
    (f"{PKG}.ihmv.asset", "print_asset_annotations",
     'model.schemas["PDB"].tables["entry"].columns["File_URL"].asset.update('),
    (f"{PKG}.citation", "print_citation_annotations", 'model.schemas["PDB"].tables["entry"].citation.update('),
])
def test_print_helpers_with_real_model(module_name, printer, expected, capsys):
    """Regression: the helpers read column.asset / column.citation. Column has no .citation (AttributeError), and the
    .asset property adds an empty {} asset annotation to every column, which main() then saved with model.apply()."""
    model = real_model()
    before = annotations_of(model)
    getattr(importlib.import_module(module_name), printer)(model)
    out = capsys.readouterr().out
    assert expected in out
    assert "/hatrac/x/" in out if "asset" in printer else "PDB-IHM" in out
    assert annotations_of(model) == before              # printing changes nothing


@pytest.mark.parametrize("module_name", [f"{PKG}.asset", f"{PKG}.ihmv.asset", f"{PKG}.citation"])
def test_main_pre_and_post_print_save_no_extra_annotations(module_name, monkeypatch):
    module = importlib.import_module(module_name)
    model = real_model()
    model.apply = mock.MagicMock()
    server = mock.MagicMock()
    server.connect_ermrest.return_value.getCatalogModel.return_value = model
    monkeypatch.setattr(module, "DerivaServer", mock.MagicMock(return_value=server))
    update = next(n for n in ["update_asset_annotations", "update_citation_annotations"] if hasattr(module, n))
    monkeypatch.setattr(module, update, lambda m: None)         # the real updates need the full PDB model
    monkeypatch.setattr(module, "clear_all_schema_annotations", lambda *a, **k: None)
    monkeypatch.setattr("builtins.print", lambda *a, **k: None)
    before = annotations_of(model)
    module.main("h", "99", {}, types.SimpleNamespace(pre_print=True, post_print=True, dry_run=False))
    model.apply.assert_called_once()
    assert annotations_of(model) == before


@pytest.mark.xfail(strict=True, reason="deriva-extras clear_table_annotations: the column and foreign-key loops are "
                                       "nested inside `for tt in t_tags`, so they only run when the table itself "
                                       "has at least one annotation")
def test_clear_all_schema_annotations_clears_columns_of_tables_without_annotations():
    from deriva.utils.extras.model import clear_all_schema_annotations
    model = real_model()
    model.schemas["PDB"].tables["plain"].columns["Name"].annotations[tag["asset"]] = dict(ASSET)
    clear_all_schema_annotations(model, [tag["asset"]])
    assert tag["asset"] not in model.schemas["PDB"].tables["plain"].columns["Name"].annotations
    assert tag["asset"] not in model.schemas["PDB"].tables["entry"].columns["File_URL"].annotations
