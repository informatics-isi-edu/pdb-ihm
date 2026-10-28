"""Shared fixtures for offline EntryProcessor tests.

`make_processor(...)` builds a real EntryProcessor whose ERMrest/Hatrac access is replaced by mocks:

  * the catalog and Hatrac store are MagicMocks,
  * module-level ERMrest helpers used by entry_processor.py (get_ermrest_query, update_table_rows,
    delete_table_rows, insert_if_not_exist) are patched and exposed as `ermrest.query`, `ermrest.update`, ...,
  * the entry row returned while the processor initializes is ENTRY_ROW (override any column per test).

Nothing here touches the network, /scratch or external binaries (CifCheck, singularity, py-rcsb_db).
"""
import copy
import logging
from types import SimpleNamespace
from unittest import mock

import pytest

import pdb_dev.processing.processor as base_processor  # noqa: E402

from ep_helpers import ep, ENTRY_ROW, RELATED_FILE_ROW, USER_ROW  # noqa: E402


@pytest.fixture
def ermrest(monkeypatch):
    """Patch the ERMrest helper functions imported into entry_processor.py."""
    mocks = SimpleNamespace(
        query=mock.MagicMock(return_value=[]),
        update=mock.MagicMock(side_effect=lambda *a, **k: k.get("payload", [])),
        delete=mock.MagicMock(),
        insert=mock.MagicMock(side_effect=lambda *a, **k: k.get("payload", a[3] if len(a) > 3 else [])),
    )
    monkeypatch.setattr(ep, "get_ermrest_query", mocks.query)
    monkeypatch.setattr(ep, "update_table_rows", mocks.update)
    monkeypatch.setattr(ep, "delete_table_rows", mocks.delete)
    monkeypatch.setattr(ep, "insert_if_not_exist", mocks.insert)
    # PipelineProcessor.get_user_row uses the processor module's binding
    monkeypatch.setattr(base_processor, "get_ermrest_query", mock.MagicMock(return_value=[USER_ROW]))
    return mocks


@pytest.fixture
def make_processor(ermrest, tmp_path):
    """Factory: make_processor(action="entry", row=None, **kwargs) -> EntryProcessor."""
    def _make(action="entry", row=None, **kwargs):
        base = RELATED_FILE_ROW if action == "Entry_Related_File" else ENTRY_ROW
        processing_row = copy.deepcopy(base)
        processing_row.update(row or {})
        ermrest.query.return_value = [processing_row]

        catalog = mock.MagicMock()
        catalog.dcctx = {}
        store = mock.MagicMock()
        store.is_valid_namespace.return_value = True

        params = dict(
            action=action, rid=processing_row["RID"], catalog=catalog, store=store,
            hostname="data-dev.pdb-ihm.org", catalog_id="99", email_config_file=None,
            validation_dir=str(tmp_path / "validation"), scratch=str(tmp_path / "scratch"),
            logger=logging.getLogger("test_entry_processor"), mute=True, verbose=False,
            mmCIF_defaults={}, vocab_ucode={}, cif_tables=[], export_order_by={},
            export_ermrest_ignore_tnames=[],
        )
        params.update(kwargs)
        processor = ep.EntryProcessor(**params)
        # after construction, default subsequent queries to "no rows" unless a test says otherwise
        ermrest.query.return_value = []
        ermrest.query.reset_mock()
        return processor
    return _make


