#!/usr/bin/python3

import sys
import json
from deriva.core import ErmrestCatalog, AttrDict, get_credential, DEFAULT_CREDENTIAL_FILE, tag, urlquote, DerivaServer, get_credential, BaseCLI
from deriva.core.ermrest_model import builtin_types, Schema, Table, Column, Key, ForeignKey, DomainType, ArrayType
import utils
from utils import ApplicationClient

def setTableAnnotation(schema_name, table_name, table_annotations):
    table = model_root.schemas[schema_name].tables[table_name]
    table.annotations.update(table_annotations)       
    model_root.apply()
    print ('Successfully updated the visible columns annotation for the entry table.')
    
def rename_matrix_columns(table_annotations):
    ret = json.dumps(table_annotations)
    ret = ret.replace('rot_matrix_1_1', 'rot_matrix[1][1]')\
        .replace('rot_matrix_1_2', 'rot_matrix[1][2]')\
        .replace('rot_matrix_1_3', 'rot_matrix[1][3]')\
        .replace('rot_matrix_2_1', 'rot_matrix[2][1]')\
        .replace('rot_matrix_2_2', 'rot_matrix[2][2]')\
        .replace('rot_matrix_2_3', 'rot_matrix[2][3]')\
        .replace('rot_matrix_3_1', 'rot_matrix[3][1]')\
        .replace('rot_matrix_3_2', 'rot_matrix[3][2]')\
        .replace('rot_matrix_3_3', 'rot_matrix[3][3]')\
        .replace('tr_vector_1', 'tr_vector[1]')\
        .replace('tr_vector_2', 'tr_vector[2]')\
        .replace('tr_vector_3', 'tr_vector[3]')
    ret = json.loads(ret)
    return ret

def main(server_name, catalog_id, credentials):
    server = DerivaServer('https', server_name, credentials)
    catalog = server.connect_ermrest(catalog_id)
    catalog.dcctx['cid'] = 'oneoff/model'
    model = catalog.getCatalogModel()
    schema_name = 'PDB'
    
    table_name = 'ihm_2dem_class_average_fitting'
    table = model.schemas[schema_name].tables[table_name]
    table_annotations = table.annotations
    ret = rename_matrix_columns(table_annotations)
    table.annotations.update(ret)       
    model.apply()
    print ('Successfully updated the visible columns annotation for the ihm_2dem_class_average_fitting table.')
    #print(json.dumps(table_annotations, indent=4))
    #print(json.dumps(ret, indent=4))
    
    
    table_name = 'ihm_geometric_object_transformation'
    table = model.schemas[schema_name].tables[table_name]
    table_annotations = table.annotations
    ret = rename_matrix_columns(table_annotations)
    table.annotations.update(ret)       
    model.apply()
    print ('Successfully updated the visible columns annotation for the ihm_geometric_object_transformation table.')
    #print(json.dumps(table_annotations, indent=4))
    #print(json.dumps(ret, indent=4))
    
    print('Successfully updated the annotations of the matrix tables')
    
if __name__ == '__main__':
    args = ApplicationClient('ad-hoc table creation tool', None, 1).parse_cli()
    credentials = get_credential(args.host, args.credential_file)
    main(args.host, args.catalog_id, credentials)

