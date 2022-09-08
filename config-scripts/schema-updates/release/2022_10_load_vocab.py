import sys
import json
from deriva.core import get_credential, DerivaServer, BaseCLI
from deriva.core.ermrest_model import Key, Column, builtin_types
import utils
from utils import ApplicationClient

struct_ref_db_name_rows =[
    {'Name': 'PDB', 'Description': 'Protein Data Bank'},
    {'Name': 'PDB-Dev', 'Description': 'PDB-Dev'},
    {'Name': 'Other', 'Description': 'Other Database'}
]

def main(server_name, catalog_id, credentials):
    server = DerivaServer('https', server_name, credentials)
    catalog = server.connect_ermrest(catalog_id)
    catalog.dcctx['cid'] = "oneoff/model"
    model = catalog.getCatalogModel()
    
    """
    Check if the new values already exist
    """
    url = '/entity/Vocab:struct_ref_db_name/Name=PDB;Name=Other;Name=PDB-Dev'
    resp = catalog.get(
        url
    )
    resp.raise_for_status()
    deleted_rows = resp.json()
    if len(deleted_rows) > 0:
        """
        Delete the new values
        """
        url = '/entity/Vocab:struct_ref_db_name/Name=PDB;Name=Other;Name=PDB-Dev'
        resp = catalog.delete(
            url
        )
        resp.raise_for_status()
        deleted_values = []
        
        for row in deleted_rows:
            deleted_values.append(row['Name'])
            
        print('Deleted values from the Vocab.struct_ref_db_name table: "{}"'.format(', '.join(deleted_values)))

    """
    Load data into the new vocabulary tables
    """
    utils.add_rows_to_vocab_table(catalog, 'struct_ref_db_name', struct_ref_db_name_rows)

if __name__ == '__main__':
    args = ApplicationClient('ad-hoc table creation tool', None, 1).parse_cli()
    credentials = get_credential(args.host, args.credential_file)
    main(args.host, args.catalog_id, credentials)
    
