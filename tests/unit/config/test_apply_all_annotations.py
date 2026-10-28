"""Entry points pdb_set_annotations / ihmv_set_annotations (apply_all_annotations.main).

The catalog connection is mocked; the acl stub lives in conftest.py.
"""
import importlib
from unittest import mock

import pytest

ENTRY_POINTS = ["pdb_dev.config.annotation.apply_all_annotations",
                "pdb_dev.config.annotation.ihmv.apply_all_annotations"]


class StopAfterPrePrint(Exception):
    pass


def run_main(module_name, monkeypatch, argv):
    module = importlib.import_module(module_name)
    monkeypatch.setattr("sys.argv", ["prog"] + argv)
    monkeypatch.setattr(module, "get_credential", mock.MagicMock(return_value={}))
    server = mock.MagicMock()
    monkeypatch.setattr(module, "DerivaServer", mock.MagicMock(return_value=server))
    model = server.connect_ermrest.return_value.getCatalogModel.return_value
    model.clear.side_effect = StopAfterPrePrint     # stop before the (large) annotation updates
    printers = {}
    for name in ["print_catalog_model_extras", "print_schema_model_extras", "print_table_model_extras"]:
        printers[name] = mock.MagicMock()
        monkeypatch.setattr(module, name, printers[name])
    return module, model, printers


@pytest.mark.parametrize("module_name", ENTRY_POINTS)
def test_main_connects_with_cli_arguments(module_name, monkeypatch):
    module, model, _ = run_main(module_name, monkeypatch, ["--host", "data-dev.pdb-ihm.org", "--catalog-id", "99"])
    with pytest.raises(StopAfterPrePrint):
        module.main()
    module.DerivaServer.assert_called_once_with("https", "data-dev.pdb-ihm.org", {})
    module.DerivaServer.return_value.connect_ermrest.assert_called_once_with("99")
    model.clear.assert_called_once_with(clear_comment=False, clear_annotations=True, clear_acls=False,
                                        clear_acl_bindings=False)


@pytest.mark.parametrize("module_name", ENTRY_POINTS)
def test_main_pre_print_whole_catalog(module_name, monkeypatch):
    """Regression: --schema/--table were only defined in the old __main__ block, so --pre-print raised AttributeError."""
    module, model, printers = run_main(module_name, monkeypatch, ["--pre-print"])
    module.main()
    printers["print_catalog_model_extras"].assert_called_once()
    model.clear.assert_not_called()                 # pre-print only prints


@pytest.mark.parametrize("module_name", ENTRY_POINTS)
@pytest.mark.parametrize("argv, printer, expected_args", [
    (["--schema", "PDB"], "print_schema_model_extras", ("PDB",)),
    (["--schema", "PDB", "--table", "entry"], "print_table_model_extras", ("PDB", "entry")),
])
def test_main_pre_print_schema_or_table(module_name, monkeypatch, argv, printer, expected_args):
    module, model, printers = run_main(module_name, monkeypatch, ["--pre-print"] + argv)
    module.main()
    assert printers[printer].call_args.args[1:] == expected_args
    model.clear.assert_not_called()


def test_setup_console_scripts_point_to_main():
    import ast
    import pathlib
    setup_py = pathlib.Path(__file__).resolve().parents[3] / "setup.py"
    text = setup_py.read_text()
    for name, target in [("pdb_set_annotations", "pdb_dev.config.annotation.apply_all_annotations:main"),
                         ("ihmv_set_annotations", "pdb_dev.config.annotation.ihmv.apply_all_annotations:main")]:
        assert f"'{name} = {target}'" in text
        module_name, func = target.split(":")
        assert callable(getattr(importlib.import_module(module_name), func))
    ast.parse(text)
