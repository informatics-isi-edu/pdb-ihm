"""Shared fixtures for the annotation-script tests.

catalog_annotations imports pdb_dev.config.acl.ermrest_acl, which moved to the pdb-ihm-ops repo (commit 94947dc),
so a stub is installed when it is not importable here.
"""
import collections
import importlib
import sys
import types
from unittest import mock

import pytest


@pytest.fixture(scope="module", autouse=True)
def acl_stub():
    """Provide pdb_dev.config.acl.ermrest_acl if the real one (pdb-ihm-ops) isn't installed."""
    try:
        importlib.import_module("pdb_dev.config.acl.ermrest_acl")
        yield
        return
    except ModuleNotFoundError:
        pass
    pkg = types.ModuleType("pdb_dev.config.acl")
    pkg.__path__ = []
    mod = types.ModuleType("pdb_dev.config.acl.ermrest_acl")
    mod.GROUPS = collections.defaultdict(list)
    mod.initialize_policies = lambda *a, **k: None
    with mock.patch.dict(sys.modules, {"pdb_dev.config.acl": pkg, "pdb_dev.config.acl.ermrest_acl": mod}):
        yield
