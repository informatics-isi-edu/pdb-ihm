#!/usr/bin/python

import sys
import json
from deriva.core import ErmrestCatalog, AttrDict, get_credential, DEFAULT_CREDENTIAL_FILE, tag, urlquote, DerivaServer, get_credential, BaseCLI
from deriva.core.ermrest_model import builtin_types, Schema, Table, Column, Key, ForeignKey
from deriva.core import urlquote, urlunquote
import argparse

# define ddctx cid string
# 
DCCTX = {
    "model": "model/change",
    "acl" : "config/acl",
    "annotation" : "config/anno",
    "comment" : "config/comment",
    "pipelines" : {
        "pdbdev" :  "pipeline/pdbdev",
    },
    "pipeline": "pipeline",
    "pipeline/pdbdev": "pipeline/pdbdev",
    "cli": "cli",
    "cli/clear_entry" : "cli/clr_ent",
    "cli/history": "cli/history",
    "cli/remedy": "cli/remedy",
}

class Config():
    host = None
    catalog_id = None
    is_www = False
    is_prod = False
    is_staging = False
    is_dev = False
    
    def __init__(self):
        pass

    # set config variables from hostname and ctalog_id
    def apply_hostname(self, host, catalog_id):
        self.host = host
        self.catalog_id = catalog_id
        
        if host == "data.pdb-dev.org":
            self.is_www = True
            self.is_prod = True            
        elif host in ["dev.pdb-dev.org", "dev-aws.pdb-dev.org"] and catalog_id == "50":
            self.is_staging = True
        else:
            self.is_dev = True
            
    def print(self):
        print("host:%s, catalog_id:%s, is_www=%s, is_staging=%s, is_dev=%s" % (self.host, self.catalog_id, self.is_www, self.is_staging, self.is_dev))

cfg = Config()

# -- =================================================================================
# -- add catalog_id as an optional argument with default for SMITE
# -- set default host to be SMITE dev server
class PDBDEV_CLI(BaseCLI):
    def __init__(self, description, epilog, version=None, hostname_required=False, config_file_required=False, catalog_id_required=False, rid_required=False):
        if version:
            super().__init__(description, epilog, version, False, config_file_required)            
        else:
            super().__init__(description, epilog, False, config_file_required)
            
        self.remove_options(['--host', '--config-file'])
        self.parser.add_argument('--host', metavar='<host>', help="Fully qualified deriva hostname (default=dev-aws.pdb-dev.org)", default="dev-aws.pdb-dev.org", required=hostname_required)
        self.parser.add_argument('--catalog-id', metavar='<id>', help="Deriva catalog ID (default=99)", default="99", required=catalog_id_required)
        self.parser.add_argument('--rid', type=str, metavar='<RID>', action='store', help='The RID of the record.', required=rid_required, )
        #self.parser.set_defaults(host='dev.pdb-dev.org')
        

    def parse_cli(self):
        global env
        #args = super().parse_cli()        # parsing the arguments + initialize logging (stdout)
        args = self.parser.parse_args()    # parsing the arguments only

        cfg.apply_hostname(args.host, args.catalog_id)
        
        return args
    
# -- =================================================================================        

