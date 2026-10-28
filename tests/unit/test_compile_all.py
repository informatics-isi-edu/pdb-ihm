"""Every module in pdb_dev must at least parse. Catches syntax errors in code that no other unit test imports
(a syntax error in entry_processor.py reached master once). deprecated/ and explore/ are skipped."""
import pathlib

import pytest

PKG = pathlib.Path(__file__).resolve().parents[2] / "pdb_dev"
SKIP_DIRS = {"deprecated", "explore", "__pycache__"}
MODULES = sorted(p for p in PKG.rglob("*.py") if not SKIP_DIRS.intersection(p.relative_to(PKG).parts))


@pytest.mark.parametrize("path", MODULES, ids=lambda p: str(p.relative_to(PKG)))
def test_module_compiles(path):
    compile(path.read_text(encoding="utf-8"), str(path), "exec")
