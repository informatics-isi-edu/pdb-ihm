#!/usr/bin/python3

from requests import HTTPError
from deriva.core import DerivaServer, ErmrestCatalog, get_credential
from deriva.core.ermrest_model import Table, Column, Key, builtin_types
import argparse
import sys
import json
from functools import cmp_to_key

categories = ['Entry and structure',
              'Citation, authors and software',
              'Chemical Components',
              'Molecular entities, instances and segments',
              'Model representation',
              'Structure assembly',
              'Input data',
              'Starting Models',
              'Experimental Restraints',
              'Probe labeling information',
              'Chemical Crosslinks',
              '2DEM',
              '3DEM',
              'SAS',
              'EPR',
              'Hydroxyl radical foot printing',
              'Predicted contacts',
              'Generic distance restraints',
              'Geometric objects',
              'Modeling protocol',
              'Output data',
              'Model list',
              'Multi-state modeling and ordered ensembles',
              'Localization densities',
              'Audit conform',
              'PDBX related'
              ]

tables_categories = {
    'Entry and structure': ['entry',
                            'struct'
                            ],
    'Citation, authors and software': ['audit_author',
                                       'citation',
                                       'citation_author',
                                       'software'
                                       ],
    'Chemical Components': ['chem_comp',
                            'chem_comp_atom'],
    'Molecular entities, instances and segments': ['entity',
                                                   'entity_name_com',
                                                   'entity_name_sys',
                                                   'entity_src_gen',
                                                   'entity_poly',
                                                   'pdbx_entity_nonpoly',
                                                   'entity_poly_seq',
                                                   'atom_type',
                                                   'struct_asym',
                                                   'ihm_entity_poly_segment'
                                                   ],
    'Model representation': ['ihm_model_representation',
                             'ihm_model_representation_details'
                             ],
    'Structure assembly': ['ihm_struct_assembly',
                           'ihm_struct_assembly_details',
                           'ihm_struct_assembly_class',
                           'ihm_struct_assembly_class_link'
                           ],
    'Input data': ['ihm_dataset_list',
                   'ihm_dataset_group',
                   'ihm_dataset_group_link',
                   'ihm_dataset_related_db_reference',
                   'ihm_external_reference_info',
                   'ihm_external_files',
                   'ihm_dataset_external_reference',
                   'ihm_related_datasets'
                   ],
    'Starting Models': ['ihm_starting_model_details',
                        'ihm_starting_comparative_models',
                        'ihm_starting_computational_models',
                        'ihm_starting_model_seq_dif'
                        ],
    'Experimental Restraints': [],
    'Probe labeling information': ['ihm_chemical_component_descriptor',
                                   'ihm_probe_list',
                                   'ihm_poly_probe_position',
                                   'ihm_poly_probe_conjugate',
                                   'ihm_ligand_probe'
                                   ],
    'Chemical Crosslinks': ['ihm_cross_link_list',
                            'ihm_cross_link_restraint',
                            'ihm_cross_link_result',
                            'ihm_cross_link_result_parameters'
                            ],
    '2DEM': ['ihm_2dem_class_average_restraint',
             'ihm_2dem_class_average_fitting'
             ],
    '3DEM': ['ihm_3dem_restraint'],
    'SAS': ['ihm_sas_restraint'],
    'EPR': ['ihm_epr_restraint'],
    'Hydroxyl radical foot printing': ['ihm_hydroxyl_radical_fp_restraint'],
    'Predicted contacts': ['ihm_predicted_contact_restraint'],
    'Generic distance restraints': ['ihm_feature_list',
                                    'ihm_poly_atom_feature',
                                    'ihm_poly_residue_feature',
                                    'ihm_non_poly_feature',
                                    'ihm_interface_residue_feature',
                                    'ihm_pseudo_site_feature',
                                    'ihm_derived_distance_restraint'
                                    ],
    'Geometric objects': ['ihm_geometric_object_list',
                          'ihm_geometric_object_center',
                          'ihm_geometric_object_transformation',
                          'ihm_geometric_object_sphere',
                          'ihm_geometric_object_torus',
                          'ihm_geometric_object_half_torus',
                          'ihm_geometric_object_axis',
                          'ihm_geometric_object_plane',
                          'ihm_geometric_object_distance_restraint'
                          ],
    'Modeling protocol': ['ihm_modeling_protocol',
                          'ihm_modeling_protocol_details',
                          'ihm_modeling_post_process'
                          ],
    'Output data': [],
    'Model list': ['ihm_model_list',
                   'ihm_model_group',
                   'ihm_model_group_link',
                   'ihm_model_representative',
                   'ihm_residues_not_modeled'
                   ],
    'Multi-state modeling and ordered ensembles': ['ihm_multi_state_modeling',
                                                   'ihm_multi_state_model_group_link',
                                                   'ihm_ensemble_info',
                                                   'ihm_ordered_ensemble'
                                                   ],
    'Localization densities': ['ihm_localization_density_files'
                               ],
    'Audit conform': ['audit_conform'
                      ],
    'PDBX related': ['pdbx_entity_poly_na_type',
                     'pdbx_entry_details',
                     'pdbx_inhibitor_info',
                     'pdbx_ion_info',
                     'pdbx_protein_info'
                     ]
}

pdb_tables = []
visible_fk_tables = []
visible_foreign_keys = {}
tablesVisibleForeignKey = []

def getPosition(table):
    try:
        index = visible_fk_tables.index(table)
        return index
    except:
        return -1
    
def compare_tables(x, y):
    px = getPosition(x)
    py = getPosition(y)
    if px < py:
        return -1
    elif px > py:
        return 1
    else:
        return 0
    
def setReferences(schema_name, table_name):
    global visible_foreign_keys
    table = model_root.schemas[schema_name].tables[table_name]
    
    foreign_keys = table.foreign_keys
    for foreign_key in foreign_keys:
        foreign_key_columns = foreign_key.foreign_key_columns
        referenced_columns = foreign_key.referenced_columns
        i = 0
        fks = []
        refs = []
        for foreign_key_column in foreign_key_columns:
            column_name = foreign_key_column['column_name']
            names = foreign_key.names[0]
            if column_name not in ['Owner', 'RCB', 'RMB']:
                reference = referenced_columns[i]
                ref_schema = reference['schema_name']
                if ref_schema == schema_name:
                    ref_table = reference['table_name']
                    ref_column = reference['column_name']
                    fks.append((schema_name, table_name, column_name))
                    refs.append((ref_schema, ref_table, ref_column))
            i = i+1
        if len(fks) > 0:
            constraint_schema, constraint_name = names
            tables_ref = []
            for ref in refs:
                schema_ref,table_ref,column_ref = ref
                if table_ref not in tables_ref:
                    tables_ref.append(table_ref)
                if table_ref not in visible_foreign_keys.keys():
                    visible_foreign_keys[table_ref] = {}
                if table_name not in visible_foreign_keys[table_ref]:
                    visible_foreign_keys[table_ref][table_name] = []
            for table_ref in tables_ref:
                visible_foreign_keys[table_ref][table_name].append({'constraint_schema': constraint_schema,
                                                                    'constraint_name': constraint_name,
                                                                    'foreign_key_columns': fks,
                                                                    'referenced_columns': refs
                                                                    })

def setVisibleForeignKey(schema_name, table_name):
    table_visible_foreign_keys = {'schema': schema_name,
                                  'table': table_name,
                                  'uri': 'tag:isrd.isi.edu,2016:visible-foreign-keys',
                                  'value': {'detailed': [],
                                            'filter': 'detailed'
                                            }
                                  }
    refs = table_visible_foreign_keys['value']['detailed']
    for tname in visible_fk_tables:
        if tname in visible_foreign_keys[table_name].keys():
            for ref in visible_foreign_keys[table_name][tname]:
                refs.append([ref['constraint_schema'], ref['constraint_name']])
    return table_visible_foreign_keys
    
parser = argparse.ArgumentParser()
parser.add_argument('hostname')
parser.add_argument('catalog_number')
parser.add_argument('schema_name')
parser.add_argument('output_dir')
args = parser.parse_args()


hostname = args.hostname
catalog_number = args.catalog_number
schema_name = args.schema_name
output_dir = args.output_dir

credential = get_credential(hostname)
server = DerivaServer('https', hostname, credential)
catalog = ErmrestCatalog('https', hostname, catalog_number, credential)

model_root = catalog.getCatalogModel()

tables = model_root.schemas[schema_name].tables
for table in tables.keys():
    pdb_tables.append(table)

pdb_tables.sort()

for category in categories:
    for table in tables_categories[category]:
        if table not in pdb_tables:
            print ('Category "{}", table "{}" does not exist.'.format(category, table))

for category in categories:
    for table in tables_categories[category]:
        if table in visible_fk_tables:
            print ('Duplicate table in categories: {}'.format(table))
        else:
            visible_fk_tables.append(table)


print ('Schema {} has {} tables.'.format(schema_name, len(pdb_tables)))
print ('Categories has {} tables.'.format(len(visible_fk_tables)))

for table in pdb_tables:
    setReferences(schema_name, table)

fp = open('{}/references.json'.format(output_dir), 'w')
json.dump(visible_foreign_keys, fp, indent=4)
fp.close()

for table_name in tables:
    if table_name in visible_foreign_keys.keys():
        tablesVisibleForeignKey.append(setVisibleForeignKey(schema_name, table_name))
    
fp = open('{}/tablesVisibleForeignKey.json'.format(output_dir), 'w')
json.dump(tablesVisibleForeignKey, fp, indent=4)
fp.close()
    
