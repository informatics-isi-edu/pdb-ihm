"""ihmv_worker.main start-up (logger and credential check); no catalog or Hatrac access."""
import sys
from unittest import mock

import pytest

iw = pytest.importorskip("pdb_dev.processing.ihmv_worker")


@pytest.fixture
def started(monkeypatch, tmp_path):
    monkeypatch.setattr(sys, "argv", ["ihmv_worker", "--host", "data-dev.pdb-ihm.org", "--catalog-id", "199",
                                      "--log-file", str(tmp_path / "ihmv.log")])
    logger = mock.MagicMock()
    monkeypatch.setattr(iw, "init_logger", mock.MagicMock(return_value=logger))
    monkeypatch.setattr(iw, "DerivaServer", mock.MagicMock())
    monkeypatch.setattr(iw, "HatracStore", mock.MagicMock())
    return logger


def test_missing_credentials_is_reported_through_logger(started, monkeypatch):
    """Regression: the logger was created after the credential check, which raised NameError instead."""
    monkeypatch.setattr(iw, "get_credential", mock.MagicMock(return_value=None))
    assert iw.main() == 1
    assert "CREDENTIAL ERROR" in started.error.call_args.args[0]
    iw.DerivaServer.assert_not_called()


def test_logger_uses_log_file_argument(started, monkeypatch, tmp_path):
    monkeypatch.setattr(iw, "get_credential", mock.MagicMock(return_value=None))
    iw.main()
    assert iw.init_logger.call_args.kwargs == {"log_file": str(tmp_path / "ihmv.log"), "name": "ihmv"}
    assert "starts ihmv worker" in started.info.call_args_list[0].args[0]
