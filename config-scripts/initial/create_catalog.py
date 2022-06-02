#!/usr/bin/python3

from requests import HTTPError
from deriva.core import DerivaServer, ErmrestCatalog, get_credential
from deriva.core.ermrest_model import Table, Column, Key, builtin_types
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('hostname')
args = parser.parse_args()

hostname = args.hostname

credential = get_credential(hostname)
server = DerivaServer('https', hostname, credential)
catalog = server.create_ermrest_catalog()

print("Catalog ID: {}".format(catalog._catalog_id))
