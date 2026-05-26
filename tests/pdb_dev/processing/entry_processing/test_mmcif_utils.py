import unittest
import os
import json
from argparse import Namespace
from test_entry_processor import TestProcessor
from deriva.utils.extras.data import insert_if_not_exist, update_table_rows, delete_table_rows, get_ermrest_query
from pdb_dev.processing.entry_processing.mmcif_utils import PkTables, check_entry_tables_fkeys, print_table_fkeys


pk_tables: dict = None

class TestmmCIFUtils(TestProcessor):
    pk_tables = None
    catalog = None
    model = None
    
    def setUp(self):
        """
        This method is called before each test function (methods starting with 'test_') 
        is run.
        """
        global pk_tables
        
        super().setUp()
        if not pk_tables:
            self.pk_tables = PkTables(catalog=self.catalog)
            print("---------- initialize PkTables ----------")

    def tearDown(self):
        """ Tear down after test
        """
        pass

        
    def test_PkTable(self):
        """
        Notes: among the tables in 9A9V, only 2 tables have combo2 fkeys (ihm_model_representation_details and ihm_struct_assembly_details).
        
        """
        print("- test_prepare_model")
        entry_id = "D_4-K8M2"        
        #check_entry_tables_fkeys(self.catalog)

        # tables in .json file
        if False:
            for tname in ['atom_type', 'chem_comp', 'entity', 'ihm_modeling_protocol', 'ihm_model_group', 'ihm_model_representation', 'ihm_struct_assembly', 'struct', 'entity_poly', 'ihm_model_list', 'struct_asym', 'entity_poly_seq', 'ihm_model_group_link', 'ihm_entity_poly_segment', 'ihm_struct_assembly_details', 'ihm_model_representation_details']:
                print_table_fkeys(self.model.schemas["PDB"].tables[tname])

        table = self.model.schemas["PDB"].tables["ihm_model_representation_details"]
        print_table_fkeys(table)
        self.pk_tables.prepare_model(table)

        #parent_tables = { fkey.pk_table for fkey in table.foreign_keys }
        #print("parent_tables: %s" % ([table.name for table in parent_tables]))
        self.pk_tables.ermrest_data = self.pk_tables.get_ermrest_data(self.catalog, [table], entry_id)
        print("ermrest_data: %s" % (json.dumps(self.pk_tables.ermrest_data, indent=4)))
        
        self.pk_tables.prepare_data(table)
        #self.pk_tables.print_structures()

        pdb_data = None
        with open("/scratch/pdb/entry_processing/9A9V.json", "r") as f:
            pdb_data = json.load(f)[0]
        print("- before %s: %s" % (table.name, json.dumps(pdb_data[table.name], indent=4)) )

        self.pk_tables.update_payload_with_rids(table, pdb_data[table.name])
        print("- after %s: %s" % (table.name, json.dumps(pdb_data[table.name], indent=4)) )


    def test_PkTable_2(self):
        print("- test_PkTable with fake values from 9A9V")

        # both combo1 and 2 exist
        entry_id = "D_4-K8M2"
        table = self.model.schemas["PDB"].tables["ihm_relaxation_time"]
        print_table_fkeys(table)
        self.pk_tables.prepare_model(table)
        self.pk_tables.ermrest_data.update(self.pk_tables.get_ermrest_data(self.catalog, [table], entry_id))
        print("ermrest_data: %s" % (json.dumps(self.pk_tables.ermrest_data, indent=4)))
        
        self.pk_tables.prepare_data(table)
        self.pk_tables.print_structures()
        
        pdb_data = None
        with open("/scratch/pdb/entry_processing/9A9V.json", "r") as f:
            pdb_data = json.load(f)[0]
            
        # fake data in table with both combo1 and 2
        pdb_data["ihm_relaxation_time"] = [
            {"id": 99, "value": 99, "unit":"seconds", "external_file_id":1, "dataset_group_id":1, "details": "test PkTable", "structure_id": "D_4-K8M2" }
        ]
        print("- before %s: %s" % (table.name, json.dumps(pdb_data[table.name], indent=4)) )

        self.pk_tables.update_payload_with_rids(table, pdb_data[table.name])
        print("- after %s: %s" % (table.name, json.dumps(pdb_data[table.name], indent=4)) )
        
        self.assertAlmostEqual(pdb_data[table.name][0]["External_File_RID"], "4-K964")
        self.assertAlmostEqual(pdb_data[table.name][0]["Dataset_Group_RID"], "4-K94T")

        
if __name__ == '__main__':
    cli = PDBDEV_CLI("test_entry_processor", None, 1)
    # note: no way to make use of params. Need ENV variables
    args = cli.parse_cli()

    unittest.main()
    
