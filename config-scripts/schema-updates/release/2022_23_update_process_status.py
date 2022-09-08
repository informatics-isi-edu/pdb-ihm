import sys
import json
from deriva.core import get_credential, DerivaServer, BaseCLI
from deriva.core.ermrest_model import Key, Column, builtin_types
import utils
from utils import ApplicationClient


Process_Status_Terms = {
    'NEW': 'New (trigger backend process)',
    'REPROCESS': 'Reprocess (trigger backend process after Error)',
    'IN_PROGRESS_UPLOADING_mmCIF_FILE': 'In progress: processing uploaded mmCIF file',
    'IN_PROGRESS_GENERATING_mmCIF_FILE': 'In progress: generating mmCIF file',
    'IN_PROGRESS_GENERATING_ACCESSION_CODE': 'In progress: generating accession code',
    'IN_PROGRESS_RELEASING_ENTRY': 'In progress: releasing entry',
    'SUCCESS': 'Success',
    'RESUME': 'Resume (trigger backend process)',
    'ERROR_PROCESSING_UPLOADED_mmCIF_FILE': 'Error: processing uploaded mmCIF file',
    'ERROR_GENERATING_mmCIF_FILE': 'Error: generating mmCIF file',
    'ERROR_GENERATING_ACCESSION_CODE': 'Error: generating accession code',
    'ERROR_RELEASING_ENTRY': 'Error: releasing entry',
    'IN_PROGRESS_PROCESSING_UPLOADED_RESTRAINT_FILES': 'In progress: processing uploaded restraint files',
    'ERROR_PROCESSING_UPLOADED_RESTRAINT_FILES': 'Error: processing uploaded restraint files'
    }

updated_values =[
    {'Name': Process_Status_Terms['NEW'], 'Description': 'New record created', 'Rank': 1},
    {'Name': Process_Status_Terms['REPROCESS'], 'Description': 'Status reset to rerun the last backend process (after fixing error)', 'Rank': 2},
    {'Name': Process_Status_Terms['IN_PROGRESS_UPLOADING_mmCIF_FILE'], 'Description': 'Uploaded mmCIF file is processing after user triggers DEPO', 'Rank': 5},
    {'Name': Process_Status_Terms['IN_PROGRESS_GENERATING_mmCIF_FILE'], 'Description': 'Generating mmCIF file in progress after user triggers SUBMIT', 'Rank': 6},
    {'Name': Process_Status_Terms['IN_PROGRESS_GENERATING_ACCESSION_CODE'], 'Description': 'Generating accession code in progress after curator triggers SUBMISSION COMPLETE', 'Rank': 7},
    {'Name': Process_Status_Terms['IN_PROGRESS_RELEASING_ENTRY'], 'Description': 'Pre-release process in progress after curator triggers RELEASE READY', 'Rank': 8},
    {'Name': Process_Status_Terms['SUCCESS'], 'Description': 'Last backend process successful', 'Rank': 3},
    {'Name': Process_Status_Terms['RESUME'], 'Description': 'Workflow resumed (triggered after SUBMIT, SUBMISSION COMPLETE, RELEASE READY)', 'Rank': 4},
    {'Name': Process_Status_Terms['ERROR_PROCESSING_UPLOADED_mmCIF_FILE'], 'Description': 'Error processing uploaded mmCIF file after user triggers DEPO', 'Rank': 9},
    {'Name': Process_Status_Terms['ERROR_GENERATING_mmCIF_FILE'], 'Description': 'Error generating mmCIF file after user triggers SUBMIT', 'Rank': 10},
    {'Name': Process_Status_Terms['ERROR_GENERATING_ACCESSION_CODE'], 'Description': 'Error generating accession code after curator triggers SUBMISSION COMPLETE', 'Rank': 11},
    {'Name': Process_Status_Terms['ERROR_RELEASING_ENTRY'], 'Description': 'Error releasing entry after curator triggers RELEASE READY', 'Rank': 12},
    {'Name': Process_Status_Terms['IN_PROGRESS_PROCESSING_UPLOADED_RESTRAINT_FILES'], 'Description': 'Uploaded restraint file is processing after user triggers DEPO', 'Rank': 13},
    {'Name': Process_Status_Terms['ERROR_PROCESSING_UPLOADED_RESTRAINT_FILES'], 'Description': 'Error processing uploaded restraint file after user triggers DEPO', 'Rank': 14}
]

def main(server_name, catalog_id, credentials):
    server = DerivaServer('https', server_name, credentials)
    catalog = server.connect_ermrest(catalog_id)
    catalog.dcctx['cid'] = "oneoff/model"
    model = catalog.getCatalogModel()
    
    """
    Drop column if exists
    """
    utils.drop_column_if_exist(model, 'Vocab', 'Process_Status', 'Rank')

    """
    Create column Rank
    """
    model = catalog.getCatalogModel()
    utils.create_column_if_not_exist(model, 'Vocab', 'Process_Status', 
                                     Column.define(
                                        'Rank',
                                        builtin_types.int2,
                                        comment='Order the display of the vocabulary terms.',
                                        nullok=False,
                                        default=0
                                    ))
    
    model = catalog.getCatalogModel()
    
    """
    Update the description and Rank values
    """
    url = '/attributegroup/Vocab:Process_Status/Name;Description,Rank'
    resp = catalog.put(
        url,
        json=updated_values
    )
    resp.raise_for_status()
    print('Updated description :\n{}'.format(json.dumps(updated_values, indent=4)))

if __name__ == '__main__':
    args = ApplicationClient('ad-hoc table creation tool', None, 1).parse_cli()
    credentials = get_credential(args.host, args.credential_file)
    main(args.host, args.catalog_id, credentials)
    
