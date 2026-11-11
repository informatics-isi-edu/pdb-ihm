"""pdb_dev.processing.pdb_worker main(): start-up and session logging (catalog, store and dispatcher mocked)."""
import sys
from unittest import mock

import pytest

pw = pytest.importorskip("pdb_dev.processing.pdb_worker")


SESSION = {"client": {"id": "https://auth.example.org/abc-123", "display_name": "worker@example.org"},
           "attributes": [{"id": "g1", "display_name": "pdb-curators"}], "since": "s", "expires": "e"}


@pytest.fixture
def worker_main(monkeypatch):
    def run(*extra_args):
        monkeypatch.setattr(sys, "argv", ["pdb_worker", "--host", "data-dev.pdb-ihm.org", "--catalog-id", "99",
                                          *extra_args])
        logger = mock.MagicMock()
        monkeypatch.setattr(pw, "get_credential", mock.MagicMock(return_value={"cookie": "x"}))
        server = mock.MagicMock()
        server.connect_ermrest.return_value.get_authn_session.return_value.json.return_value = SESSION
        monkeypatch.setattr(pw, "DerivaServer", mock.MagicMock(return_value=server))
        monkeypatch.setattr(pw, "HatracStore", mock.MagicMock())
        monkeypatch.setattr(pw, "init_logger", mock.MagicMock(return_value=logger))
        monkeypatch.setattr(pw, "JobDispatcher", mock.MagicMock())
        monkeypatch.setattr(pw, "EntryJobStream", mock.MagicMock())
        monkeypatch.setattr(pw, "RestraintJobStream", mock.MagicMock())
        assert pw.main() == 0
        pw.JobDispatcher.return_value.blocking_poll.assert_called_once()
        return logger
    return run


def test_main_logs_session_summary(worker_main, capsys):
    logger = worker_main()
    pw.init_logger.assert_called_once_with(log_level="info", log_file=mock.ANY, name="pdb_worker")
    assert any("* pdb_worker session: client: ('https://auth.example.org/abc-123'" in c.args[0]
               for c in logger.info.call_args_list)
    assert "- ** pdb_worker session: client:" in capsys.readouterr().out


@pytest.mark.parametrize("verbose", [False, True])
def test_main_debug_logs_full_session(worker_main, capsys, verbose):
    logger = worker_main("--debug", *(["--verbose"] if verbose else []))
    pw.init_logger.assert_called_once_with(log_level="debug", log_file=mock.ANY, name="pdb_worker")
    assert '"display_name": "pdb-curators"' in logger.debug.call_args.args[0]
    assert ("- **pdb_worker session:" in capsys.readouterr().out) is verbose
