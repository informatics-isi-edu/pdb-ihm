import json
import logging
from datetime import datetime
from types import SimpleNamespace
from unittest import mock

import pytest
import pytz

import pdb_dev.processing.processor as P
from pdb_dev.processing.processor import PipelineProcessor, ProcessingError

LA = pytz.timezone("America/Los_Angeles")


def make_processor(**kwargs):
    """Build a PipelineProcessor against a mocked catalog/store (no network)."""
    catalog = mock.MagicMock()
    catalog.dcctx = {}
    params = dict(catalog=catalog, store=mock.MagicMock(), hostname="example.org", catalog_id="99",
                  email_config_file=None)
    params.update(kwargs)
    return PipelineProcessor(**params)


def frozen_now(naive_local):
    """Patch processor.dt so dt.now(tz) returns the given Pacific wall-clock time."""
    class FakeDT(datetime):
        @classmethod
        def now(cls, tz=None):
            aware = LA.localize(naive_local)
            return aware.astimezone(tz) if tz else aware
    return mock.patch.object(P, "dt", FakeDT)


# ---------------------------------------------------------------------------
# construction
# ---------------------------------------------------------------------------
def test_init_with_mocked_catalog():
    p = make_processor(verbose=True, process_id="p7")
    assert p.catalog.dcctx["cid"] == "pipeline/pdb"
    assert p.verbose is True and p.process_id == "p7"


def test_init_without_credentials_raises_clear_error():
    """Regression: the error path referenced an undefined name and raised NameError instead."""
    with mock.patch.object(P, "get_credential", return_value=None):
        with pytest.raises(Exception, match="credential_file: /no/such/file"):
            PipelineProcessor(hostname="example.org", catalog_id="99", credential_file="/no/such/file",
                              email_config_file=None)


def test_init_cutoff_and_release_overrides():
    """Regression: release_time_utc kwarg was stored in a different attribute and silently ignored."""
    p = make_processor(cutoff_time_pacific="Friday 10:00", release_time_utc="Thursday 00:00")
    assert p.cutoff_time_pacific == "Friday 10:00"
    assert p.release_time_utc == "Thursday 00:00"


# ---------------------------------------------------------------------------
# archive / release datetime
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("now, expected", [
    (datetime(2025, 6, 2, 9, 0), "2025-06-05 21:00:00-07:00"),    # Monday -> same week Thursday
    (datetime(2025, 6, 5, 20, 59), "2025-06-05 21:00:00-07:00"),  # Thursday before cutoff
    (datetime(2025, 6, 5, 21, 0), "2025-06-05 21:00:00-07:00"),   # exactly at cutoff
    (datetime(2025, 6, 5, 21, 1), "2025-06-12 21:00:00-07:00"),   # Thursday after cutoff -> next week
    (datetime(2025, 6, 6, 8, 0), "2025-06-12 21:00:00-07:00"),    # Friday -> next week
])
def test_get_archive_datetime(now, expected):
    p = make_processor()
    with frozen_now(now):
        assert p.get_archive_datetime() == expected


def test_get_archive_datetime_across_dst_end():
    """Regression: on Sat 2025-11-01 (PDT) the next cutoff, Thu 2025-11-06, is in PST (-08:00).
    pytz arithmetic kept -07:00, which moved the real cutoff one hour early."""
    p = make_processor()
    with frozen_now(datetime(2025, 11, 1, 10, 0)):
        assert p.get_archive_datetime() == "2025-11-06 21:00:00-08:00"
        assert str(p.get_archive_datetime(utz=True)) == "2025-11-07 05:00:00+00:00"


def test_get_archive_datetime_across_dst_start():
    p = make_processor()
    with frozen_now(datetime(2025, 3, 7, 10, 0)):   # Friday PST; next Thursday is PDT
        assert p.get_archive_datetime() == "2025-03-13 21:00:00-07:00"


def test_get_archive_datetime_custom_cutoff():
    p = make_processor(cutoff_time_pacific="Monday 12:30")
    with frozen_now(datetime(2025, 6, 4, 9, 0)):   # Wednesday
        result = p.get_archive_datetime(isoformat=False)
    assert (result.weekday(), result.hour, result.minute) == (0, 12, 30)
    assert result.date().isoformat() == "2025-06-09"


def test_get_release_datetime_is_following_wednesday(capsys):
    p = make_processor()
    with frozen_now(datetime(2025, 6, 2, 9, 0)):
        release = p.get_release_datetime_utc(isoformat=False)
    assert release.strftime("%Y-%m-%d") == "2025-06-11"
    assert release.weekday() == 2 and release.hour == 0


def test_get_previous_archive_datetime_without_db():
    p = make_processor()
    assert p.get_previous_archive_datetime("2025-06-05 21:00:00-07:00", check_db_previous_archive=False) \
        == "2025-05-29 21:00:00-07:00"


def test_get_previous_archive_datetime_from_db():
    p = make_processor()
    rows = [{"previous_submission_time": "2025-05-22T21:00:00-07:00"}]
    with mock.patch.object(P, "get_ermrest_query", return_value=rows) as q:
        assert p.get_previous_archive_datetime("2025-06-05 21:00:00-07:00") == "2025-05-22 21:00:00-07:00"
    assert q.call_args.args[1:3] == ("PDB", "PDB_Archive")


def test_get_previous_archive_datetime_db_empty_falls_back():
    p = make_processor()
    with mock.patch.object(P, "get_ermrest_query", return_value=[{"previous_submission_time": None}]):
        assert p.get_previous_archive_datetime("2025-06-05 21:00:00-07:00") == "2025-05-29 21:00:00-07:00"


# ---------------------------------------------------------------------------
# small helpers
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("message, limit, tail, expected", [
    (None, 5, False, None),
    ("", 5, False, ""),
    ("abc", 5, False, "abc"),
    ("abcdefgh", 3, False, "fgh"),
    ("abcdefgh", 3, True, "abc"),
])
def test_truncate_message(message, limit, tail, expected):
    assert PipelineProcessor.truncate_message(message, limit=limit, truncate_tail=tail) == expected


def test_truncate_message_default_limit():
    msg = "x" * (PipelineProcessor.processing_details_limit + 10)
    assert len(PipelineProcessor.truncate_message(msg)) == PipelineProcessor.processing_details_limit


def test_json_dump_and_read_roundtrip(tmp_path):
    path = tmp_path / "c.json"
    PipelineProcessor.dump_json_to_file(str(path), {"a": [1, 2]})
    assert PipelineProcessor.read_json_config_file(str(path)) == {"a": [1, 2]}


def test_read_json_config_file_errors(tmp_path):
    with pytest.raises(Exception, match="doesn't exist"):
        PipelineProcessor.read_json_config_file(str(tmp_path / "missing.json"))
    bad = tmp_path / "bad.json"
    bad.write_text("{not json")
    with pytest.raises(Exception, match="not a json file"):
        PipelineProcessor.read_json_config_file(str(bad))


def test_rcb2user_uuid():
    p = make_processor()
    assert p.RCB2user_uuid("https://auth.globus.org/abc-123") == "abc-123"
    with pytest.raises(Exception):
        p.RCB2user_uuid(None)


def test_clean_directory(tmp_path):
    (tmp_path / "f.txt").write_text("x")
    (tmp_path / "sub").mkdir()
    (tmp_path / "sub" / "g.txt").write_text("y")
    p = make_processor(logger=logging.getLogger("test"))
    p.clean_directory(str(tmp_path))
    assert list(tmp_path.iterdir()) == []


def test_clean_directory_preserve(tmp_path):
    (tmp_path / "f.txt").write_text("x")
    p = make_processor(preserve=True)
    p.clean_directory(str(tmp_path), remove_dir=True)
    assert (tmp_path / "f.txt").exists()


def test_create_hatrac_uid_namespace_creates_and_sets_acl():
    p = make_processor()
    p.store.is_valid_namespace.return_value = False
    with mock.patch.object(P, "set_hatrac_namespace_acl") as set_acl:
        p.create_hatrac_uid_namespace("/hatrac/ihmv/generated/uid", "https://auth.globus.org/u-1")
    p.store.create_namespace.assert_called_once_with("/hatrac/ihmv/generated/uid/u-1", parents=True)
    assert set_acl.call_args.args[1] == {"subtree-read": ["https://auth.globus.org/u-1"]}


def test_create_hatrac_uid_namespace_existing_is_noop():
    p = make_processor()
    p.store.is_valid_namespace.return_value = True
    p.create_hatrac_uid_namespace("/hatrac/ns", "https://auth.globus.org/u-1")
    p.store.create_namespace.assert_not_called()


# ---------------------------------------------------------------------------
# logging / mail
# ---------------------------------------------------------------------------
def test_log_exception_includes_details_outside_except_block():
    """Regression: with a logger and no active exception, et.__name__ raised AttributeError."""
    logger = mock.MagicMock()
    p = make_processor(logger=logger)
    msg = p.log_exception(ProcessingError("boom", details="more info"))
    assert "boom" in msg and "more info" in msg
    assert "ProcessingError" in logger.error.call_args_list[0].args[0]


def test_log_exception_inside_except_block_has_traceback():
    p = make_processor(logger=mock.MagicMock())
    try:
        raise ValueError("bad value")
    except ValueError as e:
        msg = p.log_exception(e, body_prefix="PREFIX")
    assert "PREFIX" in msg and "Traceback" in msg and "bad value" in msg


def test_log_exception_notify_calls_sendmail():
    p = make_processor(logger=mock.MagicMock())
    with mock.patch.object(p, "sendMail") as send:
        p.log_exception(ValueError("x"), notify=True)
    assert send.call_args.args[0] == "Processing error"


def test_sendmail_muted_does_not_connect():
    p = make_processor(mute=True, email_config={"server": "s"})
    with mock.patch.object(P.smtplib, "SMTP_SSL") as smtp:
        p.sendMail("subj", "body")
    smtp.assert_not_called()


def test_sendmail_sends_with_prefix():
    cfg = {"server": "smtp", "port": 465, "sender": "from@x", "receivers": "a@x,b@x", "curators": "",
           "user": "u", "password": "pw", "footer": "--"}
    p = make_processor(email_config=cfg, logger=mock.MagicMock(), hostname="data-dev.pdb-ihm.org")
    with mock.patch.object(P.smtplib, "SMTP_SSL") as smtp:
        p.sendMail("hello", "body")
    server = smtp.return_value
    sender, receivers, raw = server.sendmail.call_args.args
    assert receivers == ["a@x", "b@x"]
    assert "Subject: DEV:99 PDB-IHM hello" in raw


# ---------------------------------------------------------------------------
# topological table sort (fake model, no catalog)
# ---------------------------------------------------------------------------
class FakeTable:
    def __init__(self, name, schema="PDB"):
        self.name = name
        self.schema = SimpleNamespace(name=schema)
        self.foreign_keys = []

    def sqlite3_table_name(self):
        return f"{self.schema.name}:{self.name}"

    def __repr__(self):
        return self.name


def _fk(table, pk_table):
    table.foreign_keys.append(SimpleNamespace(table=table, pk_table=pk_table))


def fake_catalog():
    entry, entity, poly, seq, chem = (FakeTable(n) for n in ["entry", "entity", "entity_poly", "entity_poly_seq", "chem_comp"])
    acc = FakeTable("Accession_Code")
    vocab = FakeTable("Workflow_Status", schema="Vocab")
    _fk(entity, entry); _fk(poly, entity); _fk(seq, poly); _fk(seq, chem); _fk(chem, entry)
    _fk(acc, entry)            # ignored by design
    _fk(entry, acc)            # entry -> Accession_Code creates a cycle unless the reverse is ignored
    _fk(entry, vocab)          # Vocab references ignored
    pdb = SimpleNamespace(tables={t.name: t for t in [entry, entity, poly, seq, chem, acc]})
    model = SimpleNamespace(schemas={"PDB": pdb})
    catalog = mock.MagicMock()
    catalog.getCatalogModel.return_value = model
    return catalog


def test_get_topo_sorted_tables_respects_fkeys():
    order = PipelineProcessor.get_topo_sorted_tables(fake_catalog(), tname_only=True)
    idx = {name: i for i, name in enumerate(order)}
    assert idx["Accession_Code"] < idx["entry"] < idx["entity"] < idx["entity_poly"] < idx["entity_poly_seq"]
    assert idx["chem_comp"] < idx["entity_poly_seq"]


def test_get_topo_sorted_tables_reverse():
    forward = PipelineProcessor.get_topo_sorted_tables(fake_catalog(), tname_only=True)
    backward = list(PipelineProcessor.get_topo_sorted_tables(fake_catalog(), tname_only=True, reverse=True))
    assert backward == list(reversed(forward))


def test_utils_data_topo_sort_matches_processor():
    from pdb_dev.utils import data
    assert data.get_topo_sorted_tables(fake_catalog(), tname_only=True) == \
        PipelineProcessor.get_topo_sorted_tables(fake_catalog(), tname_only=True)


def test_topo_ranked_tables_ranks_are_contiguous():
    ranked = PipelineProcessor.get_topo_ranked_tables(fake_catalog(), tname_only=True)
    assert list(ranked) == list(range(len(ranked)))
    assert sorted(t for tier in ranked.values() for t in tier) == \
        sorted(["entry", "entity", "entity_poly", "entity_poly_seq", "chem_comp", "Accession_Code"])


# ---------------------------------------------------------------------------
# release-date caveat (see "Flagged, not changed" in the project review doc)
# ---------------------------------------------------------------------------
def test_release_datetime_current_behavior_is_pacific_wednesday_midnight():
    """Documents current behavior, not necessarily the intended one: the docstring says Wednesday 00:00 UTC,
    but the value is Wednesday 00:00 in Pacific time. Only the date is used downstream, which is correct
    for the default Thursday cutoff. Update this test if the decision is to switch to true UTC."""
    p = make_processor()
    with frozen_now(datetime(2025, 6, 2, 9, 0)):
        release = p.get_release_datetime_utc(isoformat=False)
    assert release.isoformat() == "2025-06-11T00:00:00-07:00"


def test_release_datetime_custom_release_weekday():
    p = make_processor(release_time_utc="Friday 00:00")
    with frozen_now(datetime(2025, 6, 2, 9, 0)):                 # archive Thu 2025-06-05
        assert p.get_release_datetime_utc(isoformat=False).date().isoformat() == "2025-06-06"


def test_release_datetime_same_weekday_as_cutoff_moves_a_week():
    p = make_processor(release_time_utc="Thursday 00:00")
    with frozen_now(datetime(2025, 6, 2, 9, 0)):
        assert p.get_release_datetime_utc(isoformat=False).date().isoformat() == "2025-06-12"


# ---------------------------------------------------------------------------
# ERMrest / Hatrac helpers
# ---------------------------------------------------------------------------
def test_get_user_row_joins_rcb_to_client_table():
    p = make_processor()
    user = {"ID": "https://auth.globus.org/u-1", "Email": "a@b", "Full_Name": "A"}
    with mock.patch.object(P, "get_ermrest_query", return_value=[user]) as q:
        assert p.get_user_row("PDB", "entry", "1-ABC") == user
    args, kwargs = q.call_args
    assert args[1:3] == ("PDB", "entry")
    assert kwargs["constraints"] == "RID=1-ABC/B:=(M:RCB)=(public:ERMrest_Client:ID)"
    assert kwargs["attributes"] == ["B:ID", "B:Email", "B:Full_Name"]


def test_download_hatrac_file_returns_local_path(tmp_path):
    p = make_processor()
    with mock.patch.object(P, "HatracFile") as HF:
        HF.return_value.file_path = str(tmp_path / "x.cif")
        assert p.download_hatrac_file("/hatrac/a/x.cif", str(tmp_path), "x.cif") == str(tmp_path / "x.cif")
    HF.return_value.download_file.assert_called_once_with("/hatrac/a/x.cif", str(tmp_path), "x.cif", verbose=True)


@pytest.fixture
def upload_dir(tmp_path):
    for name in ["9ABC_full_validation.pdf", "9ABC_html.tar.gz", "notes.txt", "with space.pdf"]:
        (tmp_path / name).write_text("x")
    (tmp_path / "sub.pdf").mkdir()                        # directories are never uploaded
    return tmp_path


def _uploaded(HF):
    return sorted(c.args[2] for c in HF.return_value.upload_file.call_args_list)


def test_upload_file_groups_filters_and_sanitizes(upload_dir):
    p = make_processor()
    with mock.patch.object(P, "HatracFile") as HF:
        HF.return_value.sanitize_filename.side_effect = lambda n: n.replace(" ", "_")
        hfs = p.upload_file_groups(str(upload_dir), [r"\.pdf$"], "/hatrac/pdb/generated")
    assert _uploaded(HF) == ["9ABC_full_validation.pdf", "with_space.pdf"]
    assert len(hfs) == 2
    urls = sorted(c.args[1] for c in HF.return_value.upload_file.call_args_list)
    assert urls == ["/hatrac/pdb/generated/9ABC_full_validation.pdf", "/hatrac/pdb/generated/with_space.pdf"]


def test_upload_file_groups_default_uploads_all_files_with_prefix(upload_dir):
    p = make_processor()
    with mock.patch.object(P, "HatracFile") as HF:
        HF.return_value.sanitize_filename.side_effect = lambda n: n
        p.upload_file_groups(str(upload_dir), None, "/hatrac/ns", file_prefix="1-ABC")
    assert _uploaded(HF) == ["1-ABC_9ABC_full_validation.pdf", "1-ABC_9ABC_html.tar.gz", "1-ABC_notes.txt",
                             "1-ABC_with space.pdf"]


def test_upload_file_groups_adjusts_namespace_for_dev_root(upload_dir):
    p = make_processor()
    p.hatrac_root = "/hatrac/dev"
    with mock.patch.object(P, "HatracFile") as HF:
        HF.return_value.sanitize_filename.side_effect = lambda n: n
        p.upload_file_groups(str(upload_dir), ["notes"], "/hatrac/pdb/generated")
    assert HF.return_value.upload_file.call_args.args[1] == "/hatrac/dev/pdb/generated/notes.txt"


def test_upload_file_groups_overlapping_filters_upload_twice(upload_dir):
    """Documents current behavior: a file matching two filters is uploaded (and returned) twice."""
    p = make_processor()
    with mock.patch.object(P, "HatracFile") as HF:
        HF.return_value.sanitize_filename.side_effect = lambda n: n
        hfs = p.upload_file_groups(str(upload_dir), ["9ABC", r"\.pdf$"], "/hatrac/ns")
    assert _uploaded(HF).count("9ABC_full_validation.pdf") == 2
    assert len(hfs) == 4


# ---------------------------------------------------------------------------
# mail edge cases
# ---------------------------------------------------------------------------
MAIL_CFG = {"server": "smtp", "port": 465, "sender": "from@x", "receivers": "a@x", "curators": "",
            "user": "u", "password": "pw", "footer": "--"}


def test_sendmail_retries_on_temporary_dns_failure():
    p = make_processor(email_config=MAIL_CFG, logger=mock.MagicMock())
    err = P.socket.gaierror(P.socket.EAI_AGAIN, "temporary failure")
    with mock.patch.object(P.smtplib, "SMTP_SSL", side_effect=[err, err, mock.MagicMock()]) as smtp, \
         mock.patch.object(P.time, "sleep") as sleep:
        p.sendMail("subj", "body")
    assert smtp.call_count == 3
    assert sleep.call_count == 2


def test_sendmail_gives_up_after_retries():
    logger = mock.MagicMock()
    p = make_processor(email_config=MAIL_CFG, logger=logger)
    err = P.socket.gaierror(P.socket.EAI_AGAIN, "temporary failure")
    with mock.patch.object(P.smtplib, "SMTP_SSL", side_effect=err) as smtp, mock.patch.object(P.time, "sleep"):
        p.sendMail("subj", "body")                       # must not raise
    assert smtp.call_count == 11
    assert "retry failed" in logger.error.call_args_list[0].args[0]


def test_sendmail_other_errors_are_logged_not_raised():
    logger = mock.MagicMock()
    p = make_processor(email_config=MAIL_CFG, logger=logger)
    with mock.patch.object(P.smtplib, "SMTP_SSL", side_effect=OSError("connection refused")):
        p.sendMail("subj", "body")
    assert "connection refused" in logger.error.call_args_list[0].args[0]


def test_sendmail_without_logger_still_sends():
    p = make_processor(email_config=MAIL_CFG)
    p.logger = None
    with mock.patch.object(P.smtplib, "SMTP_SSL") as smtp:
        p.sendMail("subj", "body")
    smtp.return_value.sendmail.assert_called_once()


@pytest.mark.parametrize("cfg", [None, dict(MAIL_CFG, server=None), dict(MAIL_CFG, receivers="", curators="")])
def test_sendmail_incomplete_config_is_noop(cfg):
    p = make_processor(email_config=cfg)
    p.email_config = cfg
    with mock.patch.object(P.smtplib, "SMTP_SSL") as smtp:
        p.sendMail("subj", "body")
    smtp.assert_not_called()


def test_send_linux_mail_command():
    p = make_processor(email_config=MAIL_CFG, logger=mock.MagicMock())
    with mock.patch.object(P.subprocess, "Popen") as popen:
        popen.return_value.communicate.return_value = (b"", b"")
        popen.return_value.returncode = 0
        p.sendLinuxMail("subj", "body", "a@x")
    assert popen.call_args.args[0] == ["/usr/bin/mail", "-r", "from@x", "-s", "DEV subj", "a@x"]


def test_send_linux_mail_removes_temp_file():
    p = make_processor(email_config=MAIL_CFG, logger=mock.MagicMock())
    created = []
    real_open = open

    def tracking_open(path, mode="r", *a, **k):
        if str(path).startswith("/tmp/") and str(path).endswith(".txt"):
            created.append(path)
        return real_open(path, mode, *a, **k)
    with mock.patch.object(P.subprocess, "Popen") as popen, mock.patch("builtins.open", tracking_open):
        popen.return_value.communicate.return_value = (b"", b"")
        popen.return_value.returncode = 1
        p.sendLinuxMail("subj", "body", None)            # None -> config receivers
    assert created and not P.os.path.exists(created[0])
    assert popen.call_args.args[0][-1] == "a@x"
