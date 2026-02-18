import unittest
import os
import json
from argparse import Namespace
from deriva.utils.extras.data import insert_if_not_exist, update_table_rows, delete_table_rows, get_ermrest_query
from pdb_dev.processing.entry_processing.entry_processor import EntryProcessor
from pdb_dev.processing.entry_processing.mmcif_utils import PkTables, get_mmcif_rid_optional_fkeys, get_mmcif_rid_mandatory_fkeys
from pdb_dev.processing.entry_processing.pdb_process_entry import load

entry_processor = None
entry_row = None
entry_related_file_row = None

HERE = os.path.abspath(os.path.dirname(__file__))
TOPDIR = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))

rid2json = {
    '4-K8M2': '/scratch/pdb/entry_processing/test_data/9A9V_output.json', # ref    
    '4-X83E': '/scratch/pdb/entry_processing/test_data/9A9V_output.json', # test
    '4-ETK0': '/scratch/pdb/entry_processing/test_data/9A8W_output.json', # ref
}

    
class TestProcessor(unittest.TestCase):
    catalog = None
    processor = None
    config_file = os.getenv("PDB_CONFIG", "local_pdb_conf.json")
    host = os.getenv("PDB_SERVER", "data-dev.pdb-ihm.org")
    catalog_id = os.getenv("CATALOG", "99")
    entry_ciff_filepath = os.getenv("CIF_FILE", "pdb_test_entry.cif")
    entry_rid = os.getenv("RID", "4-K8M2")    # 9A9V (500K)
    #entry_rid = os.getenv("RID", "4-ETK0")    # 9A8W (1MB)
    entry_row = None
    verbose = bool(os.getenv("VERBOSE", False))

    def setUp(self):
        """
        This method is called before each test function (methods starting with 'test_') 
        is run.
        """
        global entry_processor, entry_row
        
        if not entry_processor:
            args = Namespace(host=self.host, catalog_id=self.catalog_id, action="entry", rid=self.entry_rid, verbose=self.verbose, notify=False)
            config = load(self.config_file, args)
            # setup a test entry if not exist            
            entry_processor = EntryProcessor(**config)
            print("---------- initialize EntryProcessor ----------")
            print("args: %s" % (args))
            print("**__file__: %s, HERE: %s, TOPDIR: %s" % (__file__, HERE, TOPDIR))

        if not entry_row:
            entry_row = get_ermrest_query(entry_processor.catalog, "PDB", "entry", constraints=f'RID={self.entry_rid}')[0]
            
        self.processor = entry_processor
        self.catalog = self.processor.catalog
        self.model = self.catalog.getCatalogModel()
        self.entry_row = entry_row
        
        
        # You can also set up other resources here

    def tearDown(self):
        """ Tear down after test
        """
        pass
    
class TestEntryProcessor(TestProcessor):
    def x_test_get_user_row(self):
        """Test get_user_row
        """
        print("- test_get_user_row")
        
        ref_users = {
            "4-K8M2": {
                "RID": "4-K8KY",
                "ID": "https://auth.globus.org/3ebd2fe2-8897-4e04-855a-31c3841aabbd",
                "Email": "i20bioq@gmail.com",
                "Full_Name": "Jos\u00e9"
            },
            "4-ETK0": {
                "RID": "1-RPZA",
                "ID": "https://auth.globus.org/5a627005-1b97-4251-9811-b5015953210b",
                "Email": "andrea.graziadei@tu-berlin.de",
                "Full_Name": "Andrea Graziadei"
            }  
        }
        user = self.processor.get_user_row('PDB', "entry", self.entry_rid)
        print("user: %s" % (json.dumps(user, indent=4)))
        self.assertAlmostEqual(user["ID"], ref_users[self.entry_rid]["ID"])

    def x_test_getHatracFile(self):
        print("- test_getHatracFile")


    def x_test_storeFileInHatrac(self):
        print("- test_storeFileInHatrac")

        
    def x_test_get_topo_sorted_tables(self):
        """Sort based on fkey constraints
        """
        print("- test_get_topo_sorted_tables")        
        sorted_tables = self.processor.get_topo_sorted_tables()
        table2orders = {}
        for tname in sorted_tables:
            table2orders[tname] = sorted_tables.index(tname)

        print("table2index:")
        for tname, index in table2orders.items():
            print("  %d : %s" % (index, tname))

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


    def x_test_sortTable(self):
        """Compare the previous implementation with the new one
        """
        print("- test_sortTable")
        expected_results = {
            "4-K8M2": ['atom_type', 'chem_comp', 'entity', 'ihm_modeling_protocol', 'ihm_model_group', 'ihm_model_representation', 'ihm_struct_assembly', 'struct', 'entity_poly', 'ihm_model_list', 'struct_asym', 'entity_poly_seq', 'ihm_model_group_link', 'ihm_entity_poly_segment', 'ihm_struct_assembly_details', 'ihm_model_representation_details'],
            "4-ETK0": ['atom_type', 'chem_comp', 'entity', 'ihm_modeling_protocol', 'ihm_model_group', 'ihm_model_representation', 'ihm_struct_assembly', 'struct', 'entity_poly', 'ihm_model_list', 'struct_asym', 'entity_poly_seq', 'ihm_model_group_link', 'ihm_entity_poly_segment', 'ihm_struct_assembly_details', 'ihm_model_representation_details']
        }

        sorted_tables = self.processor.x_sortTable(rid2json["4-K8M2"])
        sorted_tables_2 = self.processor.sortTablesFromFile(rid2json["4-K8M2"])

        self.assertAlmostEqual(len(sorted_tables), len(sorted_tables_2))
        self.assertAlmostEqual(sorted_tables, sorted_tables_2)
        
        print("sorted_tables: %s" % (sorted_tables))
        print("table2index: %d: %d" % (len(sorted_tables), len(sorted_tables_2)))
        for index in range(0, max([len(sorted_tables), len(sorted_tables_2)])):
            print("  %d : %s  --  %s" % (index, sorted_tables[index], sorted_tables_2[index]) )


    def print_data_dict(self, key2rows, heading="key2rows"):
        print("print_data_dict: %s " % (heading))
        for k, v in key2rows.items():
            print(" %s [%d] : %s\n" % (k, len(v), json.dumps(v[0:2], indent=4)))
        
    def x_test_loadTablesFromJSON(self):
        """Test to ensure that all the combo related RIDs are generated properly.
        The test is set up to compare the payload generated against the base entry database.
        It will not write to the actual ermrest database. This is because second insert
        will throw an error..
        """
        print("- test_loadTablesFromJSON")
        
        pdb_data = None
        with open(rid2json["4-K8M2"], "r") as f:
            pdb_data = json.load(f)[0]
        tname = "ihm_model_representation_details"
        print("- %s: %s" % (tname, json.dumps(pdb_data[tname], indent=4)) )
        
        # compare against the existing database
        base_entry = get_ermrest_query(self.catalog, "PDB", "entry", constraints="RID=4-K8M2")[0]

        if self.entry_row["RID"] == "4-K8M2": # "9A9V"
            base_entry = self.entry_row
            base_processor = self.processor
        else:
            args = Namespace(host=self.host, catalog_id=self.catalog_id, action="entry", rid="4-K8M2", verbose=self.verbose, notify=False)
            config = load(self.config_file, args)
            base_processor = EntryProcessor(**config)
            

        json_fpath = rid2json["4-K8M2"]
        base_user = base_processor.get_user_row('PDB', "entry", base_entry["RID"])
        
        base_inserted = {}
        base_data = {}
        base_pk_tables =  PkTables(ermrest_data=base_inserted)

        base_sorted_tnames = base_processor.sortTable(rid2json["4-K8M2"])
        base_model = base_processor.catalog.getCatalogModel()
        for tname in base_sorted_tnames:
            if tname not in base_model.schemas["PDB"].tables.keys() or tname in ['entry']: continue
            table = base_model.schemas["PDB"].tables[tname]
            base_pk_tables.prepare_model(table)
            if "structure_id" in table.columns.elements:
                base_data[tname] = get_ermrest_query(base_processor.catalog, "PDB", tname, constraints=f'structure_id={base_entry["id"]}')
            elif "entry_id" in table.columns.elements:
                base_data[tname] = get_ermrest_query(base_processor.catalog, "PDB", tname, constraints=f'entry_id={base_entry["id"]}')

        # check the values aginst itself
        base_processor.loadTablesFromJSON(json_fpath, processing_dir='/home/pdb/entry_processing/temp', ermrest_insert=False, ermrest_data=base_data)
        
        # check inserting data
        base_tname2inserting = base_processor.tname2inserting
        #self.print_data_dict(base_tname2inserting, "base_tname2inserting")
        for tname, rows in base_tname2inserting.items():
            if tname in ["entry"]: continue
            table = base_model.schemas["PDB"].tables[tname] 
            # -- same number of rows            
            self.assertAlmostEqual(len(rows), len(base_data[tname]))
            # -- check combo fkeys
            for i in range(0, len(rows)):
                inserting_row = rows[i]                
                data_row = base_data[tname][i]
                combo_fkeys = get_mmcif_rid_optional_fkeys(table) + get_mmcif_rid_mandatory_fkeys(table)                
                for fkey in combo_fkeys:
                    from_cnames = [ col.name for col in fkey.column_map.keys() ]
                    print("- tname: %s from_cnames: %s" % (tname, from_cnames))
                    for cname in from_cnames:
                        if cname not in inserting_row.keys():
                            print("  - %s missing cname: None v.s. %s" % (cname, data_row[cname]))                            
                            self.assertAlmostEqual(data_row[cname], None)
                        else:
                            print("  - %s v.s. %s" % (inserting_row[cname], data_row[cname]))
                            self.assertAlmostEqual(inserting_row[cname], data_row[cname])

        return
        for tname in base_sorted_tnames:
            if tname not in base_model.schemas["PDB"].tables.keys() or tname in ['entry']: continue
            table = base_model.schemas["PDB"].tables[tname]
            base_rid2rows = { row["RID"]: row for row in base_pk_tables.emrest_data[tname] }
            base_processor.tname2inserted[tname]
            print("base_rid2rows: %s" % (json.dumps(base_rid2rows, indent=4)))
            print("test_rid2rows: %s" % (json.dumps(base_rid2rows, indent=4)))            
            combo_fkeys = get_mmcif_rid_optional_fkeys(table) + get_mmcif_rid_mandatory_fkeys(table)
            if not combo_fkeys: continue
            for fkey in combo_fkeys:
                pk_tname = fkey.pk_table.name
                to_cname2from_cnames = self.fk_ctname_to_cname2from_cnames[pk_tname][fkey.constraint_name]
                key_cnames = self.fk_ctname2kcnames[pk_tname][fkey.constraint_name]
                key_from_cnames = [ to_cname2from_cnames[cname] for cname in key_cnames ]
                rid_cname = to_cname2from_cnames["RID"]
                for row in base_pk_tables.emrest_data[tname]:
                    self.assertAlmostEqual(row[rid_cname], test_rid2rows[row["RID"]][rid_cname])

        
    def x_test_rollbackInsertedRows(self):
        test_entry = get_ermrest_query(self.catalog, "PDB", "entry", constraints="RID=4-X83E")[0]        
        args = Namespace(host=self.host, catalog_id=self.catalog_id, action="entry", rid=test_entry["RID"], verbose=self.verbose, notify=False)
        config = load(self.config_file, args)
        test_processor = EntryProcessor(**config)
        
        test_sorted_tnames = test_processor.sortTable(rid2json["4-K8M2"])
        test_processor.tname2inserted = { tname: [] for tname in test_sorted_tnames }
        test_processor.rollbackInsertedRows(test_processor.tname2inserted, test_entry["id"])
        for tname in test_sorted_tnames:
            num_rows = len(get_ermrest_query(test_processor.catalog, "PDB", tname))
            self.assertAlmostEqual(num_rows, 0)

        
    def x_test_convert2json(self):
        """
        Making sure that all the files showed up in processing_dir folder
        
        Generate cif file using make_mmcif and move it to rcsb/db/tests-validate/test-output/ihm-files/<RID>_output.cif
        Convert the generated cif file to json to rcsb/db/tests-validate/test-output/<RID>_output.json
        There should only be one .json created?
        """
        
        print("- test_convert2json")
        test_entry = {"RID": "4-X83E"}
        args = Namespace(host=self.host, catalog_id=self.catalog_id, action="entry", rid=test_entry["RID"], verbose=self.verbose, notify=False)
        config = load(self.config_file, args)
        test_processor = EntryProcessor(**config)

        processing_dir = f'/scratch/pdb/entry_processing/scratch/{test_entry["RID"]}'
        
        test_processor.convert2json(rid2json["4-K8M2"], processing_dir)
        
        cif_fpath = f'{processing_dir}/{test_entry["RID"]}_output.cif'
        json_fpath = f'{processing_dir}/{test_entry["RID"]}_output.json'        
        self.assertTrue(os.path.exists(cif_fpath), f"Cif file (make-mmcif) not found: {cif_fpath}")
        self.assertTrue(os.path.exists(json_fpath), f"Json file (pyrcsb-db) not found: {json_fpath}")

    def get_ermrest_data(self, catalog, tname2rows, tnames, entry_rid):
        model = catalog.getCatalogModel()
        for tname in tnames:
            table = model.schemas["PDB"].tables[tname]
            constraints="%s=%s" % ("structure_id" if "structure_id" in table.columns.elements else "entry_id", entry_rid)
            tname2rows[table.name] = get_ermrest_query(catalog, "PDB", table.name, constraints=constraints)
        return tname2rows
    
    def test_process_mmCIF(self):
        """Test to ensure all related entries are generated properly
        """
        print("- test_process_mmCIF")
        
        test_rid = '4-X83E'
        test_entry = get_ermrest_query(self.catalog, "PDB", "entry", constraints=f"RID={test_rid}")[0]                
        args = Namespace(host=self.host, catalog_id=self.catalog_id, action="entry", rid=test_entry["RID"], verbose=self.verbose, notify=False)
        config = load(self.config_file, args)
        test_processor = EntryProcessor(**config)

        updating_row = {
            'RID': test_rid,
            #'Workflow_Status': 'DEPO',
            #'Processing_Status': 'IN_PROGRESS_UPLOADING_mmCIF_FILE': 'In progress: processing uploaded mmCIF file',
            'Last_mmCIF_File_MD5': None,
        }
        test_processor.update_processing_row(updating_row)
        test_processor.process_mmCIF()
        updated_test_entry = get_ermrest_query(test_processor.catalog, "PDB", "entry", constraints=f"RID={test_rid}")[0]
        #print(json.dumps(updated_test_entry, indent=4))
        
        # -- last_mmcif_file is set properly
        self.assertAlmostEqual(updated_test_entry["Last_mmCIF_File_MD5"], "77a0dfa50e902b913c04fedd3ba0893f")

        topo_sort_tnames = self.processor.sortTablesFromFile(rid2json["4-K8M2"])
        base_rid = "4-K8M2"
        base_entry = None

        if self.entry_row["RID"] == "4-K8M2": # "9A9V"
            base_entry = self.entry_row
            base_processor = self.processor
        else:
            args = Namespace(host=self.host, catalog_id=self.catalog_id, action="entry", rid="4-K8M2", verbose=self.verbose, notify=False)
            config = load(self.config_file, args)
            base_processor = EntryProcessor(**config)

        base_tname2rows = {}
        test_tname2rows = {}
        base_tname2rows = self.get_ermrest_data(base_processor.catalog, {}, topo_sort_tnames, base_rid)
        test_tname2rows = self.get_ermrest_data(test_processor.catalog, {}, topo_sort_tnames, test_rid)

        base_model = base_processor.catalog.getCatalogModel        
        for tname in topo_sort_tnames:
            if tname not in base_tname2rows.keys() or len(base_tname2rows[tname]) == 0: continue 
            self.assertAlmostEqual(len(base_tname2rows[tname]), len(test_tname2rows[tname]))
            base_row = base_tname2rows[i]
            test_row = test_tname2rows[i]
            for i in range(0, len(base_tname2rows)):
                for cname in base_row.keys():
                    self.assertAlmostEqual(base_row[cname], test_row[cname])

        
if __name__ == '__main__':
    cli = PDBDEV_CLI("test_entry_processor", None, 1)
    # note: no way to make use of params. Need ENV variables
    cli.parser.add_argument('--config', metavar='<config-file>',
                            action='store', type=str, help='The JSON configuration file. Default is PDB_CONFIG env variable.',
                            default=os.getenv("PDB_CONFIG", "~/config/entry_processing/pdb_conf.json"), required=False)
    args = cli.parse_cli()

    unittest.main()
    
    
