"""Offline unit tests for pdb_dev.

These tests do not need a DERIVA server, credentials, or /scratch test data. Network-facing objects
(ERMrest catalog, Hatrac store) are replaced with mocks.

Run from the repository root:
    python -m pytest tests/unit

The tests under tests/pdb_dev/ are integration tests that require a live catalog and are not run here.
"""
import os
import socket
import sys

import pytest

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)


@pytest.fixture(autouse=True)
def _no_network(monkeypatch):
    """Fail fast if a unit test accidentally opens a network connection (instead of hanging on retries)."""
    def guard(*args, **kwargs):
        raise RuntimeError("Network access attempted in an offline unit test")
    monkeypatch.setattr(socket.socket, "connect", guard)
    monkeypatch.setattr(socket, "create_connection", guard)
