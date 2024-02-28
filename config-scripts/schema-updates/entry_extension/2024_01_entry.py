import sys
import json
from deriva.core import ErmrestCatalog, AttrDict, get_credential, DEFAULT_CREDENTIAL_FILE, tag, urlquote, DerivaServer, get_credential, BaseCLI
from deriva.core.ermrest_model import builtin_types, Schema, Table, Column, Key, ForeignKey, DomainType, ArrayType
import utils

# ========================================================

def update_PDB_entry(model):
    
    # Add the PDB.entry.Method_Details column    
    utils.create_column_if_not_exist(model, 'PDB', 'entry', 
                                     Column.define(
                                        'Method_Details',
                                        builtin_types.text,
                                        comment='PDB-Dev is a repository for integrative structures determined by combining information from different types experimental and computational methods. Please provide specific details regarding types of experimental data, starting structural models, and computational methods used in the modeling process.',
                                        nullok=False,
                                        default="Integrative modeling"
                                    ))

# ============================================================
def main(server_name, catalog_id, credentials):
    server = DerivaServer('https', server_name, credentials)
    catalog = server.connect_ermrest(catalog_id)
    catalog.dcctx['cid'] = 'oneoff/model'
    model = catalog.getCatalogModel()

    """
    Update existing PDB table
    """
    if True:
        update_PDB_entry(model)    
        utils.set_default_column_if_exists(model, 'PDB', 'entry', 'Method_Details', None) 

# ===================================================    

if __name__ == '__main__':
    args = BaseCLI('ad-hoc table creation tool', None, 1).parse_cli()
    credentials = get_credential(args.host, args.credential_file)

    main(args.host, 1, credentials)
    
