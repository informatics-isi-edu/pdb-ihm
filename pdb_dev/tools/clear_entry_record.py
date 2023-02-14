#!/usr/bin/python

"""
usage: python3 clear_entry_record.py --credential-file <file> --host <host> --catalog_id CATALOG_ID --rid RID [--action {DRY,DELETE}]

options:
  --credential-file <file>    Path to a credential file.
  --host <host>               Fully qualified host name.
  --catalog_id CATALOG_ID     The catalog number.
  --rid RID                   The RID of the record.
  --action {DRY,DELETE}       The action to be performed: DRY or DELETE. The default is DRY.
  
Examples:

    1. Execute a DRY action: just print the URL's to be deleted
    
        python3 clear_entry_record.py --host data.pdb-dev.org --credential-file ~/.deriva/credential.json --catalog_id 1 --rid 1-W4CY 

    2. Execute a DELETE action: print the URL's to be deleted and then delete the records
    
        python3 clear_entry_record.py --host data.pdb-dev.org --credential-file ~/.deriva/credential.json --catalog_id 1 --rid 1-W4CY --action DELETE

"""

import sys
import json
from deriva.core import ErmrestCatalog, AttrDict, get_credential, DEFAULT_CREDENTIAL_FILE, tag, urlquote, DerivaServer, get_credential, BaseCLI
from deriva.core.ermrest_model import builtin_types, Schema, Table, Column, Key, ForeignKey, DomainType, ArrayType
import traceback
from .. import utils


class ApplicationClient (BaseCLI):
    def __init__(self, description, epilog, version=None, hostname_required=False, config_file_required=False):
        if version == None:
            super(ApplicationClient, self).__init__(description, epilog, hostname_required, config_file_required)
        else:
            super(ApplicationClient, self).__init__(description, epilog, version, hostname_required, config_file_required)
        self.parser.add_argument('--catalog_id', action='store', type=int, required=True, help='The catalog number.')
        self.parser.add_argument('--rid', action='store', type=str, required=True, help='The RID of the record.')
        self.parser.add_argument('--action', action='store', type=str, choices=['DRY', 'DELETE'], default='DRY', help='The action to be performed: DRY or DELETE.')


def main(server_name, catalog_id, credentials, rid, dry):
    try:
        print('server_name={}, catalog_id={}, rid={}, dry={}, '.format(server_name, catalog_id, rid, dry))
        server = DerivaServer('https', server_name, credentials)
        catalog = server.connect_ermrest(catalog_id)
        catalog.dcctx['cid'] = utils.DCCTX['tools']['clear_entry']
        url = '/entity/PDB:entry/RID={}'.format(rid)
        resp = catalog.get(url)
        resp.raise_for_status()
        if len(resp.json()) == 1:
            id = resp.json()[0]['id']

        """
        Get the references of the "entry" table 
        """
        references = []
        delete_tables = []
        cols = []
        model_root = catalog.getCatalogModel()
        schema = model_root.schemas['PDB']
        table = schema.tables['entry']
        for referenced_by in table.referenced_by:
            pk_table_name = referenced_by.table.name
            for foreign_column in referenced_by.foreign_key_columns:
                col = foreign_column.name
                references.append({pk_table_name: col})
                if col not in cols:
                    cols.append(col)
        
        print('References columns of the PDB:entry table:\n{}"'.format(json.dumps(cols, indent=4))) 
        
        """
        Get the referenced that need to be deleted
        """
        for reference in references:
            for k,v in reference.items():
                if v in ['Entry_RID', 'entry_id']:
                    val = rid
                else:
                    val = id
                if k == 'struct':
                    val = id
                url = '/entity/PDB:{}/{}={}'.format(k, v, val)
                resp = catalog.get(url)
                resp.raise_for_status()
                if len(resp.json()) > 0:
                    delete_tables.append(url)
        
        print('Entries to delete:\n{}"'.format(json.dumps(delete_tables, indent=4))) 
        
        if dry==True:
            return 
        
        """
        Delete the records referenced by the entry table
        """
        for url in delete_tables:
            resp = catalog.get(url)
            resp.raise_for_status()
            if len(resp.json()) > 0:
                resp = catalog.delete(
                    url
                )
                resp.raise_for_status()
                print('SUCCEEDED deleted the rows for the URL "%s".' % (url)) 
    except:
        et, ev, tb = sys.exc_info()
        print('got unexpected exception "%s"' % str(ev))
        print('%s' % ''.join(traceback.format_exception(et, ev, tb)))


if __name__ == '__main__':
    cli = utils.PDBDEV_CLI('Clear PDB.entry record tool', None, 1, hostname_required=True, catalog_id_required=True, rid_required=True)
    cli.parser.add_argument('--action', action='store', type=str, choices=['DRY', 'DELETE'], default='DRY', help='The action to be performed: DRY or DELETE.')
    args = cli.parse_cli()
    print("env is %s" % (utils.env,))        
    credentials = get_credential(args.host, args.credential_file)
    main(args.host, args.catalog_id, credentials, args.rid, args.action=='DRY')

