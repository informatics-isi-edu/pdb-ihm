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
    "tools" : {
        "clear_entry": "tool/clr_ent",
    },
}

