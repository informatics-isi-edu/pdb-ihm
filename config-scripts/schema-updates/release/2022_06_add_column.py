import sys
import json
from deriva.core import ErmrestCatalog, AttrDict, get_credential, DEFAULT_CREDENTIAL_FILE, tag, urlquote, DerivaServer, get_credential, BaseCLI
from deriva.core.ermrest_model import builtin_types, Schema, Table, Column, Key, ForeignKey, DomainType, ArrayType
import utils
import re
from utils import ApplicationClient

updated_values =[
    {'Name': 'DRAFT', 'Restraint_Status': 'True'},
    {'Name': 'DEPO', 'Restraint_Status': 'True'},
    {'Name': 'RECORD READY', 'Restraint_Status': 'True'},
    {'Name': 'ERROR', 'Restraint_Status': 'True'}
]

def main(server_name, catalog_id, credentials):
    server = DerivaServer('https', server_name, credentials)
    catalog = server.connect_ermrest(catalog_id)
    catalog.dcctx['cid'] = 'oneoff/model'
    model = catalog.getCatalogModel()
    
    """
    Drop column if exists
    """
    utils.drop_column_if_exist(model, 'Vocab', 'Workflow_Status', 'Restraint_Status')

    """
    Create column Restraint
    """
    model = catalog.getCatalogModel()
    utils.create_column_if_not_exist(model, 'Vocab', 'Workflow_Status', 
                                     Column.define(
                                        'Restraint_Status',
                                        builtin_types.text,
                                        comment='If set to True, the status is applicable to "Uploaded Restraint Files"',
                                        nullok=True
                                    ))
    
    """
    Update the Restraint values
    """
    url = '/attributegroup/Vocab:Workflow_Status/Name;Restraint_Status'
    resp = catalog.put(
        url,
        json=updated_values
    )
    resp.raise_for_status()

if __name__ == '__main__':
    args = ApplicationClient('ad-hoc table creation tool', None, 1).parse_cli()
    credentials = get_credential(args.host, args.credential_file)
    main(args.host, args.catalog_id, credentials)
    
