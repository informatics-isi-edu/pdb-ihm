from .shared import *
from .data import *
from .model import *

env = None
DEV = 'dev'
STAGING = 'staging'
WWW = 'www'

def set_env(host, catalog_id):
    global env

    if host == "data.pdb-dev.org":
        env = 'www'
    elif catalog_id == "50":
        env = 'staging'
    else:
        env = 'dev'
    #print("host = %s, catalog_id = %s ==> env = %s" % (host, catalog_id, env,))
    
# -- =================================================================================
# -- add catalog_id as an optional argument with default for SMITE
# -- set default host to be SMITE dev server
class PDBDEV_CLI(BaseCLI):
    def __init__(self, description, epilog, version=None, hostname_required=False, config_file_required=False, catalog_id_required=True, rid_required=False):
        if version:
            super().__init__(description, epilog, version, False, config_file_required)            
        else:
            super().__init__(description, epilog, False, config_file_required)
            
        self.remove_options(['--host', '--config-file'])
        self.parser.add_argument('--host', metavar='<host>', help="Fully qualified hostname (default=dev.pdb-dev.org)", default="dev.pdb-dev.org", required=catalog_id_required)
        self.parser.add_argument('--catalog-id', metavar='<id>', help="Deriva catalog ID (default=99)", default=1, required=catalog_id_required)
        self.parser.add_argument('--rid', type=str, metavar='<RID>', action='store', help='The RID of the record.', required=rid_required, )
        #self.parser.set_defaults(host='dev.pdb-dev.org')
        

    def parse_cli(self):
        global env
        args = super().parse_cli()

        set_env(args.host, args.catalog_id)
        
        return args
    
# -- =================================================================================        

