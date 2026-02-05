import unittest
import os
import json
from argparse import Namespace
from pdb_dev.processing.entry_processing.entry_processor import EntryProcessor
from pdb_dev.processing.entry_processing.pdb_process_entry import load

entry_processor = None

HERE = os.path.abspath(os.path.dirname(__file__))
TOPDIR = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))

class TestEntryProcessor(unittest.TestCase):
    processor = None
    config_file = os.getenv("PDB_CONFIG", "local_pdb_conf.json")
    host = os.getenv("PDB_SERVER", "data-dev.pdb-ihm.org")
    catalog_id = os.getenv("CATALOG", "99")
    entry_ciff_filepath = os.getenv("CIF_FILE", "pdb_test_entry.cif")
    entry_rid = os.getenv("RID", "4-K8M2")    # 9A9V , 4-ETK0: 9A8W
    verbose = bool(os.getenv("VERBOSE", False))
    
    def setUp(self):
        """
        This method is called before each test function (methods starting with 'test_') 
        is run.
        """
        global entry_processor
        
        if not entry_processor:
            args = Namespace(host=self.host, catalog_id=self.catalog_id, action="entry", rid=self.entry_rid, verbose=self.verbose)
            config = load(self.config_file, args)
            # setup a test entry if not exist            
            entry_processor = EntryProcessor(**config)
            print("---------- initialize EntryProcessor ----------")
            print("args: %s" % (args))
            print("**__file__: %s, HERE: %s, TOPDIR: %s" % (__file__, HERE, TOPDIR))
            

        self.processor = entry_processor
        
        # You can also set up other resources here

    def tearDown(self):
        """ Tear down after test
        """
        pass


    def test_get_user_row(self):
        print("- test_get_user_row")        
        
        ref_user = {
            "RID": "4-K8KY",
            "ID": "https://auth.globus.org/3ebd2fe2-8897-4e04-855a-31c3841aabbd",
            "Email": "i20bioq@gmail.com",
            "Full_Name": "Jos\u00e9"
        }
        
        user = self.processor.get_user_row('PDB', "entry", self.entry_rid)
        #print("user: %s" % (json.dumps(user, indent=4)))
        self.assertAlmostEqual(user["ID"], ref_user["ID"])

    def test_getHatracFile(self):
        print("- test_getHatracFile")


    def test_storeFileInHatrac(self):
        print("- test_storeFileInHatrac")

        
    def test_get_order2tables(self):
        """Sort based on fkey constraints
        """
        print("- test_get_order2tables")        
        order2tables = self.processor.get_order2tables()
        table2orders = {}
        for order, tnames in order2tables.items():
            for tname in tnames:
                table2orders[tname] = order

        # check dependecy orders
        self.assertTrue(table2orders["ihm_cross_link_pseudo_site"] > table2orders["ihm_cross_link_restraint"])
        
        self.assertTrue(table2orders["ihm_cross_link_restraint"] > table2orders["ihm_cross_link_list"])
        self.assertTrue(table2orders["ihm_cross_link_restraint"] > table2orders["struct_asym"])
        self.assertTrue(table2orders["ihm_cross_link_restraint"] > table2orders["entity_poly_seq"])
        
        self.assertTrue(table2orders["ihm_cross_link_list"] > table2orders["entity_poly_seq"])
        self.assertTrue(table2orders["ihm_cross_link_list"] > table2orders["ihm_chemical_component_descriptor"])

        self.assertTrue(table2orders["entity_poly_seq"] > table2orders["entity_poly"])
        self.assertTrue(table2orders["entity_poly_seq"] > table2orders["chem_comp"])

        self.assertTrue(table2orders["entity_poly"] > table2orders["entity"])

        self.assertTrue(table2orders["entity"] > table2orders["entry"])

        self.assertTrue(table2orders["ihm_derived_angle_restraint"] > table2orders["ihm_feature_list"])
        self.assertTrue(table2orders["ihm_feature_list"] > table2orders["Entry_Related_File"])                


    def test_sortTable(self):
        print("- test_sortTable")
        sorted_tables = self.processor.sortTable("/scratch/pdb/entry_processing/9A9V.json")
                
        
    def test_loadTablesFromJSON(self):
        """This is when the json file is loaded to ermrest
        """
        print("- test_loadTablesFromJSON")
        
    
    def test_convert2json(self):
        """
        Generate cif file using make_mmcif and move it to rcsb/db/tests-validate/test-output/ihm-files/<RID>_output.cif
        Convert the generated cif file to json to rcsb/db/tests-validate/test-output/<RID>_output.json
        There should only be one .json created?
        Load json content into table:
        
        
        """
        print("- test_convert2json")
        
    def test_process_mmCIF(self):
        print("- test_process_mmCIF")


        
if __name__ == '__main__':
    cli = PDBDEV_CLI("test_entry_processor", None, 1)
    # note: no way to make use of params. Need ENV variables
    cli.parser.add_argument('--config', metavar='<config-file>',
                            action='store', type=str, help='The JSON configuration file. Default is PDB_CONFIG env variable.',
                            default=os.getenv("PDB_CONFIG", "~/config/entry_processing/pdb_conf.json"), required=False)
    args = cli.parse_cli()

    unittest.main()
    
