import sys
import json
from deriva.core import get_credential, DerivaServer, BaseCLI
from deriva.core.ermrest_model import Key, Column, builtin_types
import utils

# add scripts for updating vocabs that has nothing to do with mmcif model changes.

workflow_status_rows =[
    {'Name': 'SUBMISSION COMPLETE', 'Description': 'The curator has checked and is happy with the submission.'},
    {'Name': 'RELEASE READY', 'Description': 'The curator has triggered the release process.'}
]

def main(server_name, catalog_id, credentials):
    server = DerivaServer('https', server_name, credentials)
    catalog = server.connect_ermrest(catalog_id)
    catalog.dcctx['cid'] = "oneoff/model"
    model = catalog.getCatalogModel()
    
    """
    Check if the new values already exist
    """
    url = '/entity/Vocab:workflow_status/Name=SUBMISSION%20COMPLETE;Name=RELEASE%20READY'
    resp = catalog.get(
        url
    )
    resp.raise_for_status()
    deleted_rows = resp.json()
    if len(deleted_rows) > 0:
        """
        Delete the new values
        """
        url = '/entity/Vocab:workflow_status/Name=SUBMISSION%20COMPLETE;Name=RELEASE%20READY'
        resp = catalog.delete(
            url
        )
        resp.raise_for_status()
        deleted_values = []
        
        for row in deleted_rows:
            deleted_values.append(row['Name'])
            
        print('Deleted values from the Vocab.workflow_status table: "{}"'.format(', '.join(deleted_values)))

    """
    Load data into the new vocabulary tables
    """
    utils.add_rows_to_vocab_table(catalog, 'workflow_status', workflow_status_rows)

if __name__ == '__main__':
    args = BaseCLI("ad-hoc table creation tool", None, 1).parse_cli()
    credentials = get_credential(args.host, args.credential_file)

    main(args.host, 1, credentials)
    
