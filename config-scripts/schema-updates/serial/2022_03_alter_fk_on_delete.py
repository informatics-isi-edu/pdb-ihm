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

    utils.alter_on_delete_fkey_if_exist(model, 'PDB', 'ihm_starting_computational_models', 'ihm_starting_computational_models_script_file_id_fk', 'CASCADE')
    utils.alter_on_delete_fkey_if_exist(model, 'PDB', 'ihm_starting_computational_models', 'ihm_starting_computational_models_software_id_fk', 'CASCADE')
    utils.alter_on_delete_fkey_if_exist(model, 'PDB', 'ihm_starting_computational_models', 'ihm_starting_computational_models_starting_model_id_fkey', 'CASCADE')

    
# ===================================================    

if __name__ == '__main__':
    args = ApplicationClient('ad-hoc table creation tool', None, 1).parse_cli()
    credentials = get_credential(args.host, args.credential_file)
#    if args.catalog is None:
#        catalog_id = 99

    main(args.host, args.catalog_id, credentials)
    
