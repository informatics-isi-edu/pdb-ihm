import unittest
import os
import json
from argparse import Namespace
from deriva.utils.extras.data import insert_if_not_exist, update_table_rows, delete_table_rows, get_ermrest_query
from pdb_dev.processing.processor import PipelineProcessor
from pdb_dev.utils.shared import PDBDEV_CLI, cfg

base_processor = None

HERE = os.path.abspath(os.path.dirname(__file__))
TOPDIR = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))

    
class TestProcessor(unittest.TestCase):
    catalog = None
    processor = None
    host = os.getenv("PDB_SERVER", "data-dev.pdb-ihm.org")
    catalog_id = os.getenv("CATALOG", "99")
    config_file = os.getenv("PDB_CONFIG", "local_pdb_conf.json")
    entry_ciff_filepath = os.getenv("CIF_FILE", "pdb_test_entry.cif")
    verbose = bool(os.getenv("VERBOSE", False))

    def setUp(self):
        """
        This method is called before each test function (methods starting with 'test_') 
        is run.
        """
        global base_processor

        cli = PDBDEV_CLI("test_processor", None, 1)
        args = Namespace(host=self.host, catalog_id=self.catalog_id)
        # address cfg        
        cfg.apply_hostname(args.host, args.catalog_id)
        cfg.args = args
        
        if not base_processor:
            # setup a test entry if not exist
            #singularity_sif=args.singularity_sif,
            params = {
                "hostname": self.host,
                "catalog_id": self.catalog_id,
                "cfg": cfg,
                "verbose": True
            }
            base_processor = PipelineProcessor(**params)
            print("---------- initialize PipelineProcessor ----------")
            print("args: %s" % (args))
            print("**__file__: %s, HERE: %s, TOPDIR: %s" % (__file__, HERE, TOPDIR))

        self.processor = base_processor
        self.catalog = self.processor.catalog
        self.model = self.catalog.getCatalogModel()
        
        
        # You can also set up other resources here

    def tearDown(self):
        """ Tear down after test
        """
        pass


class TestPipelineProcessor(TestProcessor):    

    """
    HT's user id
      - user_id="https://auth.globus.org/a57909ea-d274-11e5-9c2f-83467f6b5c29"
    
    Aurhtur's created user
    update name set name='/dev/ihmv/generated/uid/arthur_test' where id = 10423;
    update name set read=ARRAY['https://auth.globus.org/4adb2f2a-993c-40f2-9d3f-0a12d17f9084'] where id=10591;

    update name set "subtree-read"=ARRAY['https://auth.globus.org/4adb2f2a-993c-40f2-9d3f-0a12d17f9084'] where id=10593;
    
    """
    def test_create_hatrac_uid_namespace(self):
        """Test to ensure hatrac namespaces are created according to user_id
        """
        print("- test_create_hatrac_uid_namespace from user_id")
        
        user_id="https://auth.globus.org/4adb2f2a-993c-40f2-9d3f-0a12d17f9084"
        namespace_prefix="%s/ihmv/generated/uid" % (cfg.hatrac_root)
        namespace="%s/%s" % (namespace_prefix, user_id.rsplit("/")[1])
        self.processor.create_hatrac_uid_namespace(namespace_prefix, user_id)
        print(json.dumps(self.processor.store.retrieve_namespace(namespace), indent=4))
        
"""
python -m unittest test_processor.py
python -m unittest test_processor.TestProcessor
python -m unittest test_processor.TestProcessor.test_create_hatrac_uid_namespace

"""
if __name__ == '__main__':
    cli = PDBDEV_CLI("test_ihmv_processor", None, 1)
    # note: no way to make use of params. Need ENV variables
    cli.parser.add_argument('--config', metavar='<config-file>',
                            action='store', type=str, help='The JSON configuration file. Default is PDB_CONFIG env variable.',
                            default=os.getenv("PDB_CONFIG", "~/config/entry_processing/pdb_conf.json"), required=False)
    args = cli.parse_cli()

    unittest.main()
    
    
