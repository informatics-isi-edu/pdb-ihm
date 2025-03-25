#!/usr/bin/python3

import argparse
import json
import sys
import os
from deriva.core import ErmrestCatalog, HatracStore, AttrDict, get_credential, DEFAULT_CREDENTIAL_FILE, tag, urlquote, DerivaServer, get_credential, BaseCLI
from deriva.core.ermrest_model import builtin_types, Schema, Table, Column, Key, ForeignKey, tag, AttrDict
from deriva.core import urlquote, urlunquote, DEFAULT_SESSION_CONFIG
from deriva.core.utils.hash_utils import compute_hashes

from ..utils.shared import PDBDEV_CLI, DCCTX, cfg
#from pdb_dev.utils.shared import PDBDEV_CLI, DCCTX, cfg
from deriva.utils.extras.data import get_ermrest_query, insert_if_not_exist, update_table_rows, delete_table_rows
from deriva.utils.extras.hatrac import HatracFile

collection_id = None
author_file = None
verbose = False


def get_collection_entries(catalog, collection_id):
    constraints="C:=(id)=(PDB:ihm_entry_collection_mapping:entry_id)/C:collection_id=%s/$M" % (collection_id)
    attributes = ["id", "Accession_Code"] # columns from entry tables
    rows = get_ermrest_query(catalog, "PDB", "entry", constraints=constraints, attributes=attributes)
    if len(rows) == 0:
        raise Exception("Collection id: %s doesn't exist" % (collection_rid))
    if verbose: print("rows[%d][0:4]: %s" % (len(rows), json.dumps(rows[:5], indent=4)))
    structure_id2entries = { row["id"] : row for row in rows }
    return structure_id2entries


def get_citations(catalog, collection_id):
    constraints="C:=(structure_id)=(PDB:ihm_entry_collection_mapping:entry_id)/C:collection_id=%s/$M" % (collection_id)
    attributes = ["structure_id", "id", "title", "pdbx_database_id_DOI"] # columns from citation
    rows = get_ermrest_query(catalog, "PDB", "citation", constraints=constraints, attributes=attributes)
    if len(rows) == 0:
        raise Exception("citation associated with Collection id: %s doesn't exist" % (collection_rid))
    if verbose: print("rows[%d][0:4]: %s" % (len(rows), json.dumps(rows[:5], indent=4)))
    structure_id2citations = {}
    for row in rows:
        structure_id2citations.setdefault(row["structure_id"], []).append(row) 
    return structure_id2citations


def clear_citation_authors(catalog, citation_authors):
    """
    Deleting rows from the citation_authors of entries associated with a collection_id
    TODO: TEST THIS TO MAKE SURE IT DELETES THE RIGHT ROWS
    TODO: Add function to check whether delete is needed. Later.
    """
    constraints="C:=(structure_id)=(PDB:ihm_entry_collection_mapping:entry_id)/C:collection_id=%s/$M" % (collection_id)
    rows = get_ermrest_query(catalog, "PDB", "citation_author", constraints=constraints, attributes=["structure_id", "citation_id", "name", "ordinal"])
    # TODO: uncomment to delete
    #deleted = delete_table_rows(catalog, "PDB", "citation_author", constraints=constraints)
    
# TODO: complete this function
def get_author_list(author_file):
    """
    Returns a list of authors with information to be used for updating citation_authors.
    Assuming the author structure:   { "name": "name1", "ordinal": 1 }
    """
    rows = [
        { "name": "name1", "ordinal": 1},
        { "name": "name2", "ordinal": 2},
    ]
    return rows

def prepare_citation_author_payload(catalog, structure_id2entries, structure_id2citations, authors):
    """
    """
    citation_id = None
    payload = []
    for structure_id in structure_id2entries.keys():
        for citation in structure_id2citations[structure_id]:
            for author in authors:
                payload.append({
                    "structure_id": citation["structure_id"],
                    "citation_id": citation["id"],
                    "name": author["name"],
                    "ordinal": author["ordinal"],
                })
    if verbose: print("inserting citation_author [%d]: %s" % (len(payload), json.dumps(payload[0:5], indent=4)))
    return payload
    
    
def main(catalog, store, args):
    global collection_id, author_file, verbose
    collection_id = args.collection_id
    author_file = args.author_file
    verbose = args.verbose
    delete_first = args.delete_first
    
    structure_id2entries = get_collection_entries(catalog, collection_id)
    structure_id2citations = get_citations(catalog, collection_id)
    authors = get_author_list(author_file)
    citation_authors = prepare_citation_author_payload(catalog, structure_id2entries, structure_id2citations, authors)    
    if delete_first:
        print("WARNING: Will clear citation first")
        clear_citation_authors(catalog, citation_authors) 
    # TODO: uncomment inserted
    #inserted = insert_if_not_exist(catalog, "PDB", "citation_author", citation_authors)
    #if verbose: print("inserted citation_author [%d]: %s" % (len(inserted), json.dumps(inserted[0:5], indent=4)))
    

"""
To run
python -m pdb_dev.tools.update_citation_authors --host data-dev.pdb-ihm.org --catalog-id 99 --collection-id xxx --author-file /tmp/author.json 
TODO: change the default author-file location
"""

if __name__ == "__main__":
    cli = PDBDEV_CLI("pdbdev", None, 1)
    cli.parser.add_argument('--author-file', help="directory containing entry generated files", default="/tmp/author.json")
    cli.parser.add_argument('--collection-id', help="ihm_entry_collection id ", default="PDBDEV_G_1000003")    
    cli.parser.add_argument('--verbose', action="store_true", help="flag whether to print progress/status")
    cli.parser.add_argument('--delete-first', action="store_true", help="flag whether to delete existing citation_authors first")
    
    args = cli.parse_cli()
    credentials = get_credential(args.host, args.credential_file)
    print("credentials: %s" % (credentials))
    catalog = ErmrestCatalog("https", args.host, args.catalog_id, credentials)
    catalog.dcctx['cid'] = DCCTX["cli"]
    store = HatracStore("https", args.host, credentials)

    main(catalog, store, args)
