import sys
import json
from deriva.core import get_credential, DerivaServer, BaseCLI
from deriva.core.ermrest_model import Key, Column, builtin_types
import utils

# add scripts for updating vocabs that has nothing to do with mmcif model changes.

ihm_cross_link_list_linker_type_rows = [
        {'Name': 'CDI', 'Description': 'CDI'},
        {'Name': 'L-Photo-Leucine', 'Description': 'L-Photo-Leucine'},
        {'Name': 'KArGO', 'Description': 'KArGO'}
    ]

ihm_dataset_list_data_type_rows = [
    {'Name': 'Ensemble FRET data', 'Description': 'Ensemble FRET data'}
    ]

ihm_dataset_related_db_reference_db_name_rows = [
    {'Name': 'jPOSTrepo', 'Description': 'jPOSTrepo'},
    {'Name': 'iProX', 'Description': 'iProX'}
    ]

ihm_ensemble_info_ensemble_clustering_method_rows = [
    {'Name': 'Density based threshold-clustering', 'Description': 'Density based threshold-clustering'}
    ]

def main(server_name, catalog_id, credentials):
    server = DerivaServer('https', server_name, credentials)
    catalog = server.connect_ermrest(catalog_id)
    catalog.dcctx['cid'] = "oneoff/model"
    model = catalog.getCatalogModel()
    
    """
    Load data into existing vocabulary tables
    """
    utils.add_rows_to_vocab_table(catalog, 'ihm_cross_link_list_linker_type', ihm_cross_link_list_linker_type_rows)
    utils.add_rows_to_vocab_table(catalog, 'ihm_dataset_list_data_type', ihm_dataset_list_data_type_rows)
    utils.add_rows_to_vocab_table(catalog, 'ihm_dataset_related_db_reference_db_name', ihm_dataset_related_db_reference_db_name_rows)
    utils.add_rows_to_vocab_table(catalog, 'ihm_ensemble_info_ensemble_clustering_method', ihm_ensemble_info_ensemble_clustering_method_rows)

if __name__ == '__main__':
    args = BaseCLI("ad-hoc table creation tool", None, 1).parse_cli()
    credentials = get_credential(args.host, args.credential_file)

    main(args.host, 99, credentials)
    
