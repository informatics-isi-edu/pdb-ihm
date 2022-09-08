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

renamed_values = {
    "New": Process_Status_Terms['NEW'],
    "ERROR": Process_Status_Terms['ERROR_PROCESSING_UPLOADED_mmCIF_FILE'],
    "success": Process_Status_Terms['SUCCESS'],
    "Renew": Process_Status_Terms['RESUME'],
    "in progress": Process_Status_Terms['IN_PROGRESS_UPLOADING_mmCIF_FILE']
    }

updated_values =[
    {'Name': Process_Status_Terms['NEW'], 'Description': 'A new record was just created.'},
    {'Name': Process_Status_Terms['REPROCESS'], 'Description': 'The status was reset to rerun the backend process.'},
    {'Name': Process_Status_Terms['IN_PROGRESS_UPLOADING_mmCIF_FILE'], 'Description': 'The curator has triggered the entry DEPO process.'},
    {'Name': Process_Status_Terms['IN_PROGRESS_GENERATING_mmCIF_FILE'], 'Description': 'The curator has triggered the entry SUBMIT process.'},
    {'Name': Process_Status_Terms['IN_PROGRESS_GENERATING_ACCESSION_CODE'], 'Description': 'The curator has triggered the SUBMISSION COMPLETE process.'},
    {'Name': Process_Status_Terms['IN_PROGRESS_RELEASING_ENTRY'], 'Description': 'The curator has triggered the RELEASE READY process.'},
    {'Name': Process_Status_Terms['SUCCESS'], 'Description': 'The backend process was successfully.'},
    {'Name': Process_Status_Terms['RESUME'], 'Description': 'The backend process was resumed.'},
    {'Name': Process_Status_Terms['ERROR_PROCESSING_UPLOADED_mmCIF_FILE'], 'Description': 'An error occurred while uploading the mmCIF file.'},
    {'Name': Process_Status_Terms['ERROR_GENERATING_mmCIF_FILE'], 'Description': 'An error occurred while generating the mmCIF file.'},
    {'Name': Process_Status_Terms['ERROR_GENERATING_ACCESSION_CODE'], 'Description': 'An error occurred while generating the accession code.'},
    {'Name': Process_Status_Terms['ERROR_RELEASING_ENTRY'], 'Description': 'An error occurred while releasing the entry.'},
    {'Name': Process_Status_Terms['IN_PROGRESS_PROCESSING_UPLOADED_RESTRAINT_FILES'], 'Description': 'The curator has triggered the Entry_Related_File DEPO process.'},
    {'Name': Process_Status_Terms['ERROR_PROCESSING_UPLOADED_RESTRAINT_FILES'], 'Description': 'An error occurred while uploading the restraint file.'}
]

vocab_names = list(Process_Status_Terms.values())

def main(server_name, catalog_id, credentials):
    server = DerivaServer('https', server_name, credentials)
    catalog = server.connect_ermrest(catalog_id)
    catalog.dcctx['cid'] = "oneoff/model"
    model = catalog.getCatalogModel()
    
    """
    Get the new values already exist
    """
    url = '/attribute/Vocab:Process_Status/Name'
    resp = catalog.get(
        url
    )
    resp.raise_for_status()
    rows = resp.json()
    renaming_rows = []
    for row in rows:
        if row['Name'] in renamed_values.keys():
            renaming_rows.append({'original': row['Name'], 'replacement': renamed_values[row['Name']]})
    if len(renaming_rows) > 0:
        """
        Rename the values
        """
        url = '/attributegroup/Vocab:Process_Status/original:=Name;replacement:=Name'
        resp = catalog.put(
            url,
            json=renaming_rows
        )
        resp.raise_for_status()
        #print(url)
        print('Renamed values :\n{}'.format(json.dumps(renaming_rows, indent=4)))

    """
    Add new values
    """
    url = '/attribute/Vocab:Process_Status/Name'
    resp = catalog.get(
        url
    )
    resp.raise_for_status()
    rows = resp.json()
    
    existing_names = []
    for row in rows:
        if row['Name'] in renamed_values.keys():
            existing_names.append(renamed_values[row['Name']])
        else:
            existing_names.append(row['Name'])
        
    inserted_rows = []
    for val in vocab_names:
        if val not in existing_names:
            inserted_rows.append({'Name': val, 'Description': val})
    """
    New values
    """
    utils.add_rows_to_vocab_table(catalog, 'Process_Status', inserted_rows)
    print('New values :\n{}'.format(json.dumps(inserted_rows, indent=4)))

    """
    Update the description values
    """
    url = '/attributegroup/Vocab:Process_Status/Name;Description'
    resp = catalog.put(
        url,
        json=updated_values
    )
    resp.raise_for_status()
    #print(url)
    print('Updated description :\n{}'.format(json.dumps(updated_values, indent=4)))

if __name__ == '__main__':
    args = ApplicationClient('ad-hoc table creation tool', None, 1).parse_cli()
    credentials = get_credential(args.host, args.credential_file)
    main(args.host, args.catalog_id, credentials)
    
