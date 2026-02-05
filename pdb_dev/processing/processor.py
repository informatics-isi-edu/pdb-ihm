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
import mimetypes
import tempfile
from collections import deque

import time
from datetime import datetime as dt, timedelta, timezone
import pytz

from deriva.core import PollingErmrestCatalog, HatracStore, urlquote, get_credential, DerivaServer
from deriva.utils.extras.model import topo_sort_ranked
from deriva.utils.extras.data import insert_if_not_exist, update_table_rows, delete_table_rows, get_ermrest_query
from deriva.utils.extras.hatrac import HatracFile
from deriva.utils.extras.hatrac_acl import set_hatrac_namespace_acl, adjust_hatrac_namespace
from ..utils.shared import PDBDEV_CLI, DCCTX

pacific_timezone = "America/Los_Angeles"

# ===================================================================================
class ProcessingError(Exception):
    """
    Exception when fail to perform processing    
    """
    def __init__(self, message, details=None):
        super().__init__(message)  # Call the base Exception's __init__
        self.details = details

    ''' # no need to custom str
    def __str__(self):
        """
        Custom string representation for the exception.
        """
        base_message = super().__str__()
        return f"{base_message} (Details: {self.details})"
    '''
    

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

class SubProcessError(ProcessingError):
    """ Sub-process failure
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

        if kwargs.get("email", None): self.email_config = kwargs.get("email")
        if kwargs.get("logger", None): self.logger = kwargs.get("logger")
        if kwargs.get("verbose", None): self.verbose = kwargs.get("verbose")
        if kwargs.get("notify", None): self.notify = kwargs.get("notify")                
        
        # -- archive/release time
        if kwargs.get('cutoff_time_pacific', None): self.cutoff_time_pacific = kwargs.get('cutoff_time_pacific') 
        if kwargs.get('release_time_utc', None): self.release_time_pacific = kwargs.get('release_time_utc')

    
    @classmethod
    def same_table_rows(table, base_rows, compare_rows, key="structure_id"):
        """Check whether content are all the same before deleting.
        
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

    
    @classmethod    
    def dump_json_to_file(file_path, json_object):
        """Dump a json object to a file

        Args:
            file_path (str): file path to dump the json object to
            json_object (obj): json compatible object

        """
        #print("dump_json_to_file: file_path %s" % (file_path))
        fw = open(file_path, 'w')
        json.dump(json_object, fw, indent=4)
        fw.write(f'\n')
        fw.close()

    @classmethod
    def read_json_config_file(config_file):
        """Load json file
        Args:
            config_file (str): config file path
        
        Returns:
            dict: json file content
        """
        config = None
        try:
            with open(config_file, 'r') as file:
                config = json.load(file)
        except FileNotFoundError:
            print(f"Error: The file '{email_config_file}' was not found.")
            raise Exception("Config ERROR: config file doesn't exist: %s" % (config_file))
        except json.JSONDecodeError:
            print(f"Error: Could not decode JSON from '{config_file}'. Check if the file contains valid JSON.")
            raise Exception("Config ERROR: config file is not a json file: %s" % (config_file))
        return config


    # -------------------------------------------------
    def create_hatrac_uid_namespace(self, namespace_prefix, user_id):
        """Create hatrac namespace for user_id so the user can be granted subtree-read access.
        This function checks first whether the namespace exist. If it doesn't, create a namespace and assign subtree-read.
        
        Notes: UUID of the user_id is extracted and used as part of the namespace

        Args:
            namespace_prefix (str): the namespace prefix to append user uuid after        
            user_id (str): globus user id (returned from RCB)

        """
        uuid = user_id.rsplit("/", 1)[1]
        namespace = f"{namespace_prefix}/{uuid}"
        namespace = adjust_hatrac_namespace(namespace, hatrac_root=self.hatrac_root)
        
        if not self.store.is_valid_namespace(namespace):
            self.store.create_namespace(namespace, parents=True)
            acl = { "subtree-read": [ user_id ] }
            set_hatrac_namespace_acl(self.store, acl, namespace, hatrac_root=self.hatrac_root)
        else:
            if self.verbose: print("- create_hatrac_uid_namespace: namespace %s already exists" % (namespace))
            pass

        
    
    def download_hatrac_file(self, hatrac_url, data_dir, filename):
        """Download files

        Args:
            hatrac_url (str): Hatrac URL to download
            data_dir (str): local directory to store the download file
            filename (str): file name to download as

        Returns:
            str : Loal file path that the hatrac file was downloaded to
        
        """
        if self.verbose: print("hatrac_url: %s, data_dir: %s, filename: %s" % (hatrac_url, data_dir, filename))
        
        hf = HatracFile(self.store)
        hf.download_file(hatrac_url, data_dir, filename, verbose=True)
        file_path = hf.file_path

        return file_path
    
    # -------------------------------------------------
    def upload_file_groups(self, data_dir, filter_groups, namespace_prefix):
        """Upload files in the directory to hatrac that match regex criteria specified in filter_groups.
        If filter_groups are not set, allow all files to match.
        Note: To upload an individual file, specify the data_dir and put its exact filename in the filter list.

        Args:
            data_dir (str): local directory to upload the data from
            filter_groups (list): a list of filters to apply to files before uploading to hatrac
        
        Returns:
           list: a array of HatracFile corresponding to uploaded files.
        """

        if not filter_groups: filter_groups = [".*"]
        namespace_prefix = adjust_hatrac_namespace(namespace_prefix, hatrac_root=self.hatrac_root)

        if self.verbose: print("data_dir: %s, groups: %s, hatrac_prefix: %s" % (data_dir, filter_groups, namespace_prefix))
        #os.chdir(data_dir)
        
        hfs = []
        for filter in filter_groups:
            for file in os.scandir(data_dir):
                if not re.search(filter, file.name): continue
                if not file.is_file(): continue
                # TODO: rename files if needed. Suggest prepend with structure_mmcif RID
                hf = HatracFile(self.store)
                hf_file_name = f"{self.structure_rid}_{file.name}"
                hf_file_name = hf.sanitize_filename(hf_file_name)
                upload_url = f"{namespace_prefix}/{hf_file_name}"
                hf.upload_file(file.path, upload_url, hf_file_name, verbose=True)
                hfs.append(hf)
        return hfs

    # -------------------------------------------------------------------

    def get_order2tables(self):
        """Assign order to tables for insert operation based on fkeys e.g. tables with no fkeys should be inserted first.
        This function should be used to replace the needs of tables_groups.json.

        Returns:
            dict: a lookup dict from rank to list of tables associated with each rank in the topological sort of
        foreign key dependency.
        
        Notes: The current tables_groups.json keys are string, and the list contains PDB schema table names.
        TODOs: Either change the keys to be string or address the type in the processing code.
        
        """
        model = self.catalog.getCatalogModel()
        tables = {
            table
            for sname in ["PDB"]
            for table in model.schemas[sname].tables.values()
        }
        
        # dependency map { table: [ referenced_table... ], ... }
        table_depmap = {
            table: {
                # use a set to collapse references to same pk_table
                fkey.pk_table
                for fkey in table.foreign_keys
                if not (
                    # ignore references like these...
                    fkey.table.schema.name in {'Vocab'} or
                    fkey.pk_table.schema.name in {'public', 'Vocab'}
                    or (
                        fkey.pk_table.sqlite3_table_name() == 'PDB:entry'
                        and fkey.table.sqlite3_table_name() == 'PDB:Accession_Code'
                    )
                    #or fkey.table.sqlite3_table_name() == 'PDB:entry'
                    #or fkey.constraint_name == 'entry_Workflow_Status_fkey'
                )
            }
            for table in tables
        }

        tname_depmap = {
            #table.sqlite3_table_name(): [ pktable.sqlite3_table_name() for pktable in pktables ] # produce PDB:entry
            table.name: [ pktable.name for pktable in pktables ]                # ignore schema prefix
            for table, pktables in table_depmap.items()
        }
        order2tables = topo_sort_ranked(tname_depmap)

        if self.verbose:
            print("order2tables: ")
            for order, tnames in order2tables.items():
                print("  %d [%d]: %s" % ( order, len(tnames), json.dumps(sorted(tnames), indent=4)))
         
        return order2tables
            
    # -------------------------------------------------------------------            
    def get_user_row(self, schema_name, table_name, rid):
        """get ERMrest user row

        Args:
            schema_name (str): schema name
            table_name (str): table name
            rid (str): entry RID in the specified table name we want to retrieve row RCB from

        Returns:
            dict: user object describing user properties (e.g. ID, Email, Full_Name)
        """
        
        constraints=f"RID={rid}/B:=(M:RCB)=(public:ERMrest_Client:ID)"
        user_row = get_ermrest_query(self.catalog, schema_name, table_name, constraints=constraints, attributes=["B:ID", "B:Email","B:Full_Name"])[0]
        return user_row

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
    # Note: In this function: e = ev
    # HT TODO: return the error message for now
    def log_exception(self, e, notify=False, subject=None, body_prefix=None, receivers=None):
        """
        log exception, send email notificatioin if specified
        """
        error_message = ""
        if e:
            details = f'{e.details}' if isinstance(e, ProcessingError) else ''
            error_message = f'{str(e)}. {details}\n'
        et, ev, tb = sys.exc_info()
        tb_message = error_message + (body_prefix if body_prefix else "") +  ''.join(traceback.format_exception(et, ev, tb))
        if self.logger:
            self.logger.error('-- Got exception "%s: %s"' % (et.__name__, str(ev)))
            self.logger.error('%s' % (tb_message))
        if notify:
            if not subject: subject = "Processing error"
            self.sendMail(subject, tb_message, receivers)
        if self.verbose: print("tb_message: %s" % (tb_message))

        return tb_message

    # -------------------------------------------------------------------
    def sendLinuxMail(self, subject, text, receivers):
        """
        Send Linux email notification
        """
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
    def sendMail(self, subject, text, receivers=None):
        """
        Send email notification
        HT TODO: make this not deployment specific
        """
        
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
                        self.logger.error('-- sendMail retry failed with exception "%s"' % str(ev))
                        self.logger.error('%s' % ''.join(traceback.format_exception(et, ev, tb)))
                except:
                    et, ev, tb = sys.exc_info()
                    self.logger.error('-- got sendMail exception "%s"' % str(ev))
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
