import sys
import json
from deriva.core import get_credential, DerivaServer, BaseCLI
from deriva.core.ermrest_model import Key, Column, builtin_types
import utils

ihm_cross_link_list_linker_type_rows = [
        {'Name': 'PDH', 'Description': 'PDH'},
        {'Name': 'DMTMM', 'Description': 'DMTMM'}
    ]

ihm_dataset_list_data_type_rows = [
    {'Name': 'Crosslinking-MS data', 'Description': 'Crosslinking-MS data'}
    ]

ihm_dataset_group_application_rows = [
    {'Name': 'modeling', 'Description': 'modeling'}
    ]

ihm_dataset_related_db_reference_db_name_rows = [
    {'Name': 'ProteomeXchange', 'Description': 'ProteomeXchange'}
    ]

struct_pdbx_structure_determination_methodology_rows = [
        {'Name': 'computational', 'Description': 'computational'},
        {'Name': 'experimental', 'Description': 'experimental'},
        {'Name': 'integrative', 'Description': 'integrative'}
    ]

ihm_relaxation_time_unit_rows = [
        {'Name': 'seconds', 'Description': 'seconds'},
        {'Name': 'milliseconds', 'Description': 'milliseconds'},
        {'Name': 'microseconds', 'Description': 'microseconds'}
    ]

ihm_equilibrium_constant_determination_method_rows = [
        {'Name': 'from population', 'Description': 'from population'},
        {'Name': 'from kinetic rates', 'Description': 'from kinetic rates'},
        {'Name': 'other', 'Description': 'other'}
    ]

def main(server_name, catalog_id, credentials):
    server = DerivaServer('https', server_name, credentials)
    catalog = server.connect_ermrest(catalog_id)
    catalog.dcctx['cid'] = "oneoff/model"
    model = catalog.getCatalogModel()
    
    """
    Create new Vocab tables
    """
    utils.create_table_if_not_exist(model, 'Vocab', utils.define_Vocab_table('struct_pdbx_structure_determination_methodology', 'Structure determination methodology'))
    utils.create_table_if_not_exist(model, 'Vocab', utils.define_Vocab_table('ihm_relaxation_time_unit', 'Relaxation time unit'))
    utils.create_table_if_not_exist(model, 'Vocab', utils.define_Vocab_table('ihm_equilibrium_constant_determination_method', 'Method used to determine the equilibrium constant'))

    """
    Load data into new and existing vocabulary tables
    """
    utils.add_rows_to_vocab_table(catalog, 'ihm_cross_link_list_linker_type', ihm_cross_link_list_linker_type_rows)
    utils.add_rows_to_vocab_table(catalog, 'ihm_dataset_list_data_type', ihm_dataset_list_data_type_rows)
    utils.add_rows_to_vocab_table(catalog, 'ihm_dataset_group_application', ihm_dataset_group_application_rows)
    utils.add_rows_to_vocab_table(catalog, 'ihm_dataset_related_db_reference_db_name', ihm_dataset_related_db_reference_db_name_rows)
    utils.add_rows_to_vocab_table(catalog, 'struct_pdbx_structure_determination_methodology', struct_pdbx_structure_determination_methodology_rows)
    utils.add_rows_to_vocab_table(catalog, 'ihm_relaxation_time_unit', ihm_relaxation_time_unit_rows)
    utils.add_rows_to_vocab_table(catalog, 'ihm_equilibrium_constant_determination_method', ihm_equilibrium_constant_determination_method_rows)

if __name__ == '__main__':
    args = BaseCLI("ad-hoc table creation tool", None, 1).parse_cli()
    credentials = get_credential(args.host, args.credential_file)

    main(args.host, 99, credentials)
    
