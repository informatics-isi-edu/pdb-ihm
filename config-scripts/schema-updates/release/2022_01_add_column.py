import sys
import json
from deriva.core import ErmrestCatalog, AttrDict, get_credential, DEFAULT_CREDENTIAL_FILE, tag, urlquote, DerivaServer, get_credential, BaseCLI
from deriva.core.ermrest_model import builtin_types, Schema, Table, Column, Key, ForeignKey, DomainType, ArrayType
import utils
import re
from utils import ApplicationClient

# ============================================================
def main(server_name, catalog_id, credentials):
    server = DerivaServer('https', server_name, credentials)
    catalog = server.connect_ermrest(catalog_id)
    catalog.dcctx['cid'] = 'oneoff/model'
    model = catalog.getCatalogModel()
    
    """
    Drop column if exists
    """
    utils.drop_column_if_exist(model, 'PDB', 'entry', 'Release_Date')
    utils.drop_column_if_exist(model, 'PDB', 'entry', 'Notes')

    """
    Create column Release_Date
    """
    model = catalog.getCatalogModel()
    utils.create_column_if_not_exist(model, 'PDB', 'entry', 
                                     Column.define(
                                        'Release_Date',
                                        builtin_types.date,
                                        comment='The Release Date.',
                                        nullok=True
                                    ))
    
    """
    Create column Notes
    """
    model = catalog.getCatalogModel()
    utils.create_column_if_not_exist(model, 'PDB', 'entry', 
                                     Column.define(
                                        'Notes',
                                        builtin_types.markdown,
                                        comment='Notes for the Release.',
                                        nullok=True
                                    ))
    
# ===================================================    

if __name__ == '__main__':
    args = ApplicationClient('ad-hoc table creation tool', None, 1).parse_cli()
    credentials = get_credential(args.host, args.credential_file)
    main(args.host, args.catalog_id, credentials)
    
