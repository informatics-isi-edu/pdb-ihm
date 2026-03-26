import unittest
import os
import json
from argparse import Namespace
from deriva.utils.extras.data import insert_if_not_exist, update_table_rows, delete_table_rows, get_ermrest_query
from pdb_dev.processing.ihmv_processing.ihmv_processor import IHMVProcessor
from pdb_dev.processing.entry_processing.pdb_process_entry import load
from pdb_dev.utils.shared import PDBDEV_CLI, cfg

ihmv_processor = None
structure_row = None

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
    catalog_id = os.getenv("CATALOG", "199")
    entry_ciff_filepath = os.getenv("CIF_FILE", "pdb_test_entry.cif")
    structure_rid = os.getenv("RID", "2J8") 
    structure_row = None
    verbose = bool(os.getenv("VERBOSE", False))

    def setUp(self):
        """
        This method is called before each test function (methods starting with 'test_') 
        is run.
        """
        global ihmv_processor, structure_row

        cli = PDBDEV_CLI("test_ihmv_processor", None, 1)
        args = Namespace(host=self.host, catalog_id=self.catalog_id)
        # address cfg        
        cfg.apply_hostname(args.host, args.catalog_id)
        cfg.args = args
        
        if not ihmv_processor:
            # setup a test entry if not exist
            #singularity_sif=args.singularity_sif,
            
            ihmv_processor = IHMVProcessor(
                hostname=self.host, catalog_id=self.catalog_id, cfg=cfg, structure_rid=self.structure_rid, pdbihm_config_file=self.config_file,
                verbose=True, 
            )
            print("---------- initialize IHMVProcessor ----------")
            print("args: %s" % (args))
            print("**__file__: %s, HERE: %s, TOPDIR: %s" % (__file__, HERE, TOPDIR))

        if not structure_row:
            structure_row = get_ermrest_query(ihmv_processor.catalog, "IHMV", "Structure_mmCIF", constraints=f'RID={self.structure_rid}')[0]
            
        self.processor = ihmv_processor
        self.catalog = self.processor.catalog
        self.model = self.catalog.getCatalogModel()
        self.structure_row = structure_row
        
        
        # You can also set up other resources here

    def tearDown(self):
        """ Tear down after test
        """
        pass
    
class TestIHMVProcessor(TestProcessor):
    """ hongsuda user
    id             | 10402
    pid            | 9927
    ancestors      | {1,7785,9923,9926,9927}
    name           | /dev/ihmv/generated/uid/a57909ea-d274-11e5-9c2f-83467f6b5c29
    subtype        | 0
    is_deleted     | f
    owner          | 
    create         | 
    update         | 
    read           | {https://auth.globus.org/a57909ea-d274-11e5-9c2f-83467f6b5c29}
    subtree-owner  | 
    subtree-create | 
    subtree-update | 
    subtree-read   | {https://auth.globus.org/a57909ea-d274-11e5-9c2f-83467f6b5c29}
    
    update name set name='/dev/ihmv/generated/uid/hongsuda' where id = 10402;
    select * from name where id = 10402;
    select * from name where name = '/dev/ihmv/generated/uid/a57909ea-d274-11e5-9c2f-83467f6b5c29';
    select * from name where name ~ '/dev/ihmv/generated/uid/[^\/]*$';
    """

    def test_create_hatrac_uid_namespace(self):
        """Test to ensure hatrac namespaces are created based on structure RCB
        """
        print("- test_create_hatrac_uid_namespace")
        print(json.dumps(self.structure_row, indent=4))
        user_id="https://auth.globus.org/a57909ea-d274-11e5-9c2f-83467f6b5c29"
        namespace_prefix="%s/ihmv/generated/uid" % (cfg.hatrac_root)
        namespace="%s/%s" % (namespace_prefix, self.structure_row["RCB"].rsplit("/")[1])
        self.processor.create_hatrac_uid_namespace(namespace_prefix, self.structure_row["RCB"])
        print(json.dumps(self.processor.store.retrieve_namespace(namespace), indent=4))

        
"""
python -m unittest test_ihmv_processor.py
python -m unittest test_ihmv_processor.TestIHMVProcessor
python -m unittest test_ihmv_processor.TestIHMVProcessor.test_create_hatrac_uid_namespace

"""
if __name__ == '__main__':
    cli = PDBDEV_CLI("test_ihmv_processor", None, 1)
    # note: no way to make use of params. Need ENV variables
    cli.parser.add_argument('--config', metavar='<config-file>',
                            action='store', type=str, help='The JSON configuration file. Default is PDB_CONFIG env variable.',
                            default=os.getenv("PDB_CONFIG", "~/config/entry_processing/pdb_conf.json"), required=False)
    args = cli.parse_cli()

    unittest.main()
    
    
