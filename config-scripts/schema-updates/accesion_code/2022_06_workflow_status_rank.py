import sys
import json
from deriva.core import ErmrestCatalog, AttrDict, get_credential, DEFAULT_CREDENTIAL_FILE, tag, urlquote, DerivaServer, get_credential, BaseCLI
from deriva.core.ermrest_model import builtin_types, Schema, Table, Column, Key, ForeignKey, DomainType, ArrayType
import utils
import re

rows = [
    {"Name": "DRAFT", "Rank": 1},
    {"Name": "DEPO", "Rank": 2},
    {"Name": "RECORD READY", "Rank": 3},
    {"Name": "SUBMIT", "Rank": 4},
    {"Name": "mmCIF CREATED", "Rank": 5},
    {"Name": "SUBMISSION COMPLETE", "Rank": 6},
    {"Name": "HOLD", "Rank": 7},
    {"Name": "RELEASE READY", "Rank": 8},
    {"Name": "REL", "Rank": 9},
    {"Name": "ERROR", "Rank": 10},
    {"Name": "PROC", "Rank": 11}
    ]

def main(server_name, catalog_id, credentials):
    server = DerivaServer('https', server_name, credentials)
    catalog = server.connect_ermrest(catalog_id)
    catalog.dcctx['cid'] = 'oneoff/model'
    model = catalog.getCatalogModel()
    
    """
    Create column Rank
    """
    model = catalog.getCatalogModel()
    utils.create_column_if_not_exist(model, 'Vocab', 'workflow_status', 
                                     Column.define(
                                        'Rank',
                                        builtin_types.int2,
                                        comment='Order the display of the vocabulary terms.',
                                        nullok=False,
                                        default=0
                                    ))
    
    model = catalog.getCatalogModel()
    url = '/attributegroup/Vocab:workflow_status/Name;Rank'
    resp = catalog.put(
        url,
        json=rows
    )
    resp.raise_for_status()
    print('Set the values for the "Rank" column of the "Vocab.workflow_status" table.')
    
# ===================================================    

if __name__ == '__main__':
    args = BaseCLI('ad-hoc table creation tool', None, 1).parse_cli()
    credentials = get_credential(args.host, args.credential_file)
    main(args.host, 1, credentials)
    
