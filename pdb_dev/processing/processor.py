#!/usr/bin/python
# 
# Copyright 2020 University of Southern California
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#    http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import os
import subprocess
import json
from urllib.parse import urlparse
import sys
import traceback
import shutil
import hashlib
import smtplib
from email.mime.text import MIMEText
import socket
from socket import gaierror, EAI_AGAIN
from dateutil.parser import parse
from requests import HTTPError
from subprocess import TimeoutExpired
import csv
import filecmp
import mimetypes
import tempfile

import time
from datetime import datetime as dt, timedelta, timezone
import pytz

from deriva.core import PollingErmrestCatalog, HatracStore, urlquote, get_credential, DerivaServer
from deriva.utils.extras.data import insert_if_not_exist, update_table_rows, delete_table_rows, get_ermrest_query
from deriva.utils.extras.hatrac import HatracFile
from ..utils.shared import PDBDEV_CLI, DCCTX

pacific_timezone = "America/Los_Angeles"

# ===================================================================================
class ProcessingError(Exception):
    """ Exception when fail to perform processing
    """
    pass

class ErmrestError(ProcessingError):
    """ Exception when fail to perform transaction with Ermrest
    """
    pass
    
class ErmrestUpdateError(ErmrestError):
    """ Exception when fail to update to Ermrest
    """
    pass

class FileError(ProcessingError):
    """ Exception when fail to read or write files
    """
    pass


# ===================================================================================
class PipelineProcessor(object):
    """
    PipelineProcessor base class that set common variables and shared functions
    """
    python_bin = "/usr/bin/python3"    
    cutoff_time_pacific = "Thursday 20:00"    
    release_time_utc = "Wednesday 00:00"      # In UTC, so we don't have to address day light saving time.
    timeout = 30                              # minutes
    email_config_file = "/home/pdbihm/.secrets/mail.json"  # NOT USE CURRENTLY
    email_config = None
    email_subject_prefix = "PDB-IHM"
    log_dir = "/home/pdbihm/log"
    verbose = False
    notify = True
    logger = None
    
    def __init__(self, **kwargs):
        # -- ermrest and hatrac
        self.cfg = kwargs.get("cfg", None)
        self.catalog = kwargs.get("catalog", None)
        self.host = kwargs.get("hostname")
        self.credential_file = kwargs.get("credential_file", None)
        self.catalog_id = kwargs.get("catalog_id", None)
        credentials = kwargs.get("credentials", None)
        if not self.catalog:
            if not credentials: credentials = get_credential(self.host, self.credential_file)
            if not credentials:
                raise Exception("ERROR: a proper credential or credential file is required. Provided credential_file: %s" % (credential_file))
            server = DerivaServer('https', self.host, credentials)
            self.catalog = server.connect_ermrest(self.catalog_id)            
        self.catalog.dcctx['cid'] = 'pipeline/pdb'
        self.store = kwargs.get("store", None)
        if not self.store:
            self.store = HatracStore('https', self.host, credentials)
        self.hatrac_file = HatracFile(self.store)
        
        # -- local host
        self.local_hostname = socket.gethostname() # processing host

        # -- email: TODO: handle email config file here instead of pdb_process_entry
        #if kwargs.get("email", None): self.email_config = kwargs.get("email")
        
        # -- archive/release time
        if kwargs.get('cutoff_time_pacific', None): self.cutoff_time_pacific = kwargs.get('cutoff_time_pacific') 
        if kwargs.get('release_time_utc', None): self.release_time_pacific = kwargs.get('release_time_utc')

    @classmethod
    def same_table_rows(table, base_rows, compare_rows, key="structure_id"):
        """
        Check whether content are all the same before deleting.
        TODO: look up existing content based on keys
        """
        return False
        tname = table.name
        if base_rows is None and compare_rows is None: return True
        if len(base_rows) == 0 and len(compare_rows) == 0: return True
        id2compare_rows = { row["structure_id"]: row for row in compare_rows }
        print("%s base_rows[%d]: %s" % (tname, len(existing_rows), base_rows))
        print("id2compare_rows: %s " % (json.dumps(id2compare_rows, indent=4)))
        
        different = False
        for row in base_rows:
            print("current base row: %s " % (json.dumps(row, indent=4)))
            if row["structure_id"] not in id2compare_rows.keys():
                different = True
                break
            compare_row = id2compare_rows[row["structure_id"]]
            for cname in table.columns.elements:
                    if cname in ["RID", "RCB", "RCT", "RMB", "RMT", "Owner"]: continue
                    if row[cname] != compare_row[cname]:
                        print("Different contents: base => %s\n  compare => %s" % (json.dumps(row, indent=4), json.dumps(compare_row, indent=4)))
                        different = True
                        break
        print("same_table_rows: %s = %s" % (tname, different))
        return different
        
    # -------------------------------------------------------------------        
    def get_archive_datetime(self, utz=False, isoformat=True):
        """
        Archive datetime is the upcoming Thursday 8 PM PT (or the value specified in the cutoff_time_pacific config parameter)
        """
        cutoff_time = time.strptime(self.cutoff_time_pacific, "%A %H:%M")
        now = dt.now(pytz.timezone("America/Los_Angeles"))
        now_to_cutoff_weekday = (cutoff_time.tm_wday - now.weekday()) % 7
        archive_datetime = now + timedelta(days=now_to_cutoff_weekday)
        #print("get_archive_datetime: weekday_diff = %s" % (now_to_cutoff_weekday))
        if now_to_cutoff_weekday == 0 and (now.hour > cutoff_time.tm_hour or (now.hour == cutoff_time.tm_hour and now.minute > cutoff_time.tm_min)):
            archive_datetime += timedelta(days=7)
        archive_datetime = archive_datetime.replace(hour=cutoff_time.tm_hour,minute=cutoff_time.tm_min,second=0,microsecond=0)
        #print("archive pacific time: %s" % (str(archive_datetime)))
        if utz: 
            archive_datetime = archive_datetime.astimezone(timezone.utc)
        print("archive returned time (utc=%s): %s " % (str(utz), str(archive_datetime)))
        if isoformat:
            return str(archive_datetime)
        else: 
            return archive_datetime
        
    # -------------------------------------------------------------------
    def get_release_datetime_utc(self, isoformat=True):
        """
        Release Date logic:
          - If the REL is set before the archive deadline reference time (Thursday 11 PM PT), the release date is next Wednesday 0 UTC.
          - If REL is set after the archive deadline, the release date is the Wednesday after the next 0 UTC.
        Caveat: Cutoff datetime and archive datetime are in Pacific time and release date is always Wednesday 0:00 UTC.
          Because of the time zone difference, any cutoff time between Tuesday 16:00 PT and Wednesday 00:00 PT will result in a wrong release date
          (release date before cutoff datetime). Do not set cutoff datetime between Tuesday 16:00 PT and Wednesday 00:00 PT.
        """
        archive_datetime = dt.fromisoformat(self.get_archive_datetime(isoformat=True))
        release_time = time.strptime(self.release_time_utc, "%A %H:%M")
        diff_weekday = (release_time.tm_wday - archive_datetime.weekday()) % 7
        if diff_weekday == 0:
            release_datetime = archive_datetime + timedelta(days=7)
        else: 
            release_datetime = archive_datetime + timedelta(days=diff_weekday)
        release_datetime = release_datetime.replace(hour=release_time.tm_hour,minute=release_time.tm_min,second=0,microsecond=0)
        print("release time (utc): %s (diff = %d, %s)" % (str(release_datetime), diff_weekday, release_time.tm_hour))
        if isoformat:
            return str(release_datetime)
        else: 
            return release_datetime

    # ------------------------------------------------------------------------
    # the caller sometimes need the error message to be included in ermrest.
    # HT TODO: return the error message for now
    def log_exception(self, e, notify=False, subject=None, receivers=None):
        """
        log exception, send email notificatioin if specified
        """
        error_message = str(e)
        et, ev, tb = sys.exc_info()
        tb_message = error_message + '\n' + ''.join(traceback.format_exception(et, ev, tb))
        if self.logger:
            self.logger.error('-- Got exception "%s: %s"' % (et.__name__, str(ev)))
            self.logger.error('%s' % (tb_message))
        if notify: self.sendMail(subject, tb_message, receivers)
        if self.verbose: print(tb_message)
        return tb_message

    # -------------------------------------------------------------------
    """
    Send Linux email notification
    """
    def sendLinuxMail(self, subject, text, receivers):
        if receivers == None:
            receivers = self.email_config['receivers']
        temp_name = '/tmp/{}.txt'.format(next(tempfile._get_candidate_names()))
        fw = open(temp_name, 'w')
        fw.write('{}\n\n{}'.format(text, self.email_config['footer']))
        fw.close()
        fr = open(temp_name, 'r')
        args = ['/usr/bin/mail', '-r', self.email_config['sender'], '-s', 'DEV {}'.format(subject), receivers]
        p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=fr)
        stdoutdata, stderrdata = p.communicate()
        returncode = p.returncode
        
        if returncode != 0:
            self.logger.debug('Can not send Linux email for file {}.\nstdoutdata: {}\nstderrdata: {}\n'.format(temp_name, stdoutdata, stderrdata)) 
        else:
            self.logger.debug('Sent Linux email for file {}.\n'.format(temp_name)) 
        
        fr.close()
        os.remove(temp_name)

    # -------------------------------------------------------------------        
    """
    Send email notification
    HT TODO: make this not deployment specific
    """
    def sendMail(self, subject, text, receivers=None):
        if not self.notify:
            if self.verbose: print("Send mail: subject: %s, text:%s" % (subject, text))
            return
        if self.email_config and self.email_config['server'] and self.email_config['sender'] and (self.email_config['receivers'] or self.email_config['curators']):
            subject = '%s %s' % (self.email_subject_prefix, subject)
            if self.host in ['dev.pdb-dev.org', 'data-dev.pdb-ihm.org']:
                subject = f'DEV:{self.catalog_id} {subject}'
            text = f'Backend hostname: {self.local_hostname}, catalog: {self.catalog_id}\n\n{text}'
            if not receivers: receivers = self.email_config['receivers']
            retry = 0
            ready = False
            while not ready:
                try:
                    msg = MIMEText('%s\n\n%s' % (text, self.email_config['footer']), 'plain')
                    msg['Subject'] = subject
                    msg['From'] = self.email_config['sender']
                    msg['To'] = receivers
                    s = smtplib.SMTP_SSL(self.email_config['server'], self.email_config['port'])
                    s.login(self.email_config['user'], self.email_config['password'])
                    s.sendmail(self.email_config['sender'], receivers.split(','), msg.as_string())
                    s.quit()
                    self.logger.debug(f'Sent email notification to {receivers}.')
                    ready = True
                except socket.gaierror as e:
                    if e.errno == socket.EAI_AGAIN:
                        time.sleep(100)
                        retry = retry + 1
                        ready = retry > 10
                    else:
                        ready = True
                    if ready:
                        et, ev, tb = sys.exc_info()
                        self.logger.error('got exception "%s"' % str(ev))
                        self.logger.error('%s' % ''.join(traceback.format_exception(et, ev, tb)))
                except:
                    et, ev, tb = sys.exc_info()
                    self.logger.error('got exception "%s"' % str(ev))
                    self.logger.error('%s' % ''.join(traceback.format_exception(et, ev, tb)))
                    ready = True

# -- =================================================================================
def main(server_name, catalog_id, credentials, args):
    server = DerivaServer('https', server_name, credentials)
    store = HatracStore('https', server_name, credentials)
    catalog = server.connect_ermrest(catalog_id)
    model = catalog.getCatalogModel()

    cutoff_time = args.cutoff_time if args.cutoff_time else None
    processor = PipelineProcessor(
        hostname=args.host, credential_file=args.credential_file, catalog_id=args.catalog_id, cutoff_time_pacific=cutoff_time
    )
    #processor.get_archive_datetime(utz=True)
    release_date = processor.get_release_datetime_utc(isoformat=False).strftime("%Y-%m-%d")
    print("release_date: %s" % (release_date))

 # -- =================================================================================
if __name__ == '__main__':
    cli = PDBDEV_CLI("pdb-ihm", None, 1)
    cli.parser.add_argument('--cutoff-time', metavar='<cutoff_time>', help="cutoff_time in PT", required=False)
    args = cli.parse_cli()
    credentials = get_credential(args.host, args.credential_file)
    
    main(args.host, args.catalog_id, credentials, args)
