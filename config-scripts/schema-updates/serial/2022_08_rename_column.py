import sys
import json
from deriva.core import ErmrestCatalog, AttrDict, get_credential, DEFAULT_CREDENTIAL_FILE, tag, urlquote, DerivaServer, get_credential, BaseCLI
from deriva.core.ermrest_model import builtin_types, Schema, Table, Column, Key, ForeignKey, DomainType, ArrayType
import utils
from utils import ApplicationClient

# ========================================================

# ============================================================


def main(server_name, catalog_id, credentials):
    server = DerivaServer('https', server_name, credentials)
    catalog = server.connect_ermrest(catalog_id)
    catalog.dcctx['cid'] = 'oneoff/model'
    model = catalog.getCatalogModel()

    utils.rename_column_if_exists(model, 'PDB', 'ihm_2dem_class_average_fitting', 'rot_matrix_1_1', 'rot_matrix[1][1]')
    utils.rename_column_if_exists(model, 'PDB', 'ihm_2dem_class_average_fitting', 'rot_matrix_1_2', 'rot_matrix[1][2]')
    utils.rename_column_if_exists(model, 'PDB', 'ihm_2dem_class_average_fitting', 'rot_matrix_1_3', 'rot_matrix[1][3]')
    utils.rename_column_if_exists(model, 'PDB', 'ihm_2dem_class_average_fitting', 'rot_matrix_2_1', 'rot_matrix[2][1]')
    utils.rename_column_if_exists(model, 'PDB', 'ihm_2dem_class_average_fitting', 'rot_matrix_2_2', 'rot_matrix[2][2]')
    utils.rename_column_if_exists(model, 'PDB', 'ihm_2dem_class_average_fitting', 'rot_matrix_2_3', 'rot_matrix[2][3]')
    utils.rename_column_if_exists(model, 'PDB', 'ihm_2dem_class_average_fitting', 'rot_matrix_3_1', 'rot_matrix[3][1]')
    utils.rename_column_if_exists(model, 'PDB', 'ihm_2dem_class_average_fitting', 'rot_matrix_3_2', 'rot_matrix[3][2]')
    utils.rename_column_if_exists(model, 'PDB', 'ihm_2dem_class_average_fitting', 'rot_matrix_3_3', 'rot_matrix[3][3]')
    
    utils.rename_column_if_exists(model, 'PDB', 'ihm_2dem_class_average_fitting', 'tr_vector_1', 'tr_vector[1]')
    utils.rename_column_if_exists(model, 'PDB', 'ihm_2dem_class_average_fitting', 'tr_vector_2', 'tr_vector[2]')
    utils.rename_column_if_exists(model, 'PDB', 'ihm_2dem_class_average_fitting', 'tr_vector_3', 'tr_vector[3]')

    utils.rename_column_if_exists(model, 'PDB', 'ihm_geometric_object_transformation', 'rot_matrix_1_1', 'rot_matrix[1][1]')
    utils.rename_column_if_exists(model, 'PDB', 'ihm_geometric_object_transformation', 'rot_matrix_1_2', 'rot_matrix[1][2]')
    utils.rename_column_if_exists(model, 'PDB', 'ihm_geometric_object_transformation', 'rot_matrix_1_3', 'rot_matrix[1][3]')
    utils.rename_column_if_exists(model, 'PDB', 'ihm_geometric_object_transformation', 'rot_matrix_2_1', 'rot_matrix[2][1]')
    utils.rename_column_if_exists(model, 'PDB', 'ihm_geometric_object_transformation', 'rot_matrix_2_2', 'rot_matrix[2][2]')
    utils.rename_column_if_exists(model, 'PDB', 'ihm_geometric_object_transformation', 'rot_matrix_2_3', 'rot_matrix[2][3]')
    utils.rename_column_if_exists(model, 'PDB', 'ihm_geometric_object_transformation', 'rot_matrix_3_1', 'rot_matrix[3][1]')
    utils.rename_column_if_exists(model, 'PDB', 'ihm_geometric_object_transformation', 'rot_matrix_3_2', 'rot_matrix[3][2]')
    utils.rename_column_if_exists(model, 'PDB', 'ihm_geometric_object_transformation', 'rot_matrix_3_3', 'rot_matrix[3][3]')
    
    utils.rename_column_if_exists(model, 'PDB', 'ihm_geometric_object_transformation', 'tr_vector_1', 'tr_vector[1]')
    utils.rename_column_if_exists(model, 'PDB', 'ihm_geometric_object_transformation', 'tr_vector_2', 'tr_vector[2]')
    utils.rename_column_if_exists(model, 'PDB', 'ihm_geometric_object_transformation', 'tr_vector_3', 'tr_vector[3]')

# ===================================================    

if __name__ == '__main__':
    args = ApplicationClient('ad-hoc table creation tool', None, 1).parse_cli()
    credentials = get_credential(args.host, args.credential_file)
    main(args.host, args.catalog_id, credentials)

