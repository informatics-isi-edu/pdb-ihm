import sys
import json
from deriva.core import ErmrestCatalog, AttrDict, get_credential, DEFAULT_CREDENTIAL_FILE, tag, urlquote, DerivaServer, get_credential, BaseCLI
from deriva.core.ermrest_model import builtin_types, Schema, Table, Column, Key, ForeignKey, DomainType, ArrayType
import utils

def update_PDB_ihm_ensemble_info(model):
    # Add the PDB.ihm_ensemble_info.model_group_superimposed_flag
    utils.create_column_if_not_exist(model, 'PDB', 'ihm_ensemble_info',
                                     Column.define(
                                        'model_group_superimposed_flag',
                                        builtin_types.text,
                                        comment='Flag to identify if the models in a group or cluster are structurally aligned',
                                        nullok=True
                                    ))

    # Create the foreign keys
    utils.create_foreign_key_if_not_exists(model, 'PDB', 'ihm_ensemble_info', 'ihm_ensemble_info_model_group_superimposed_flag_fkey',
                                            ForeignKey.define(['model_group_superimposed_flag'], 'Vocab', 'ihm_ensemble_info_model_group_superimposed_flag', ['Name'],
                                              constraint_names=[ ['Vocab', 'ihm_ensemble_info_model_group_superimposed_flag_fkey'] ],
                                              on_update='CASCADE',
                                              on_delete='NO ACTION')
                                           )

# ============================================================
def main(server_name, catalog_id, credentials):
    server = DerivaServer('https', server_name, credentials)
    catalog = server.connect_ermrest(catalog_id)
    catalog.dcctx['cid'] = 'oneoff/model'
    model = catalog.getCatalogModel()

    """
    Update existing model
    """
    update_PDB_ihm_ensemble_info(model)

# ===================================================    

if __name__ == '__main__':
    args = BaseCLI('ad-hoc table creation tool', None, 1).parse_cli()
    credentials = get_credential(args.host, args.credential_file)
#    if args.catalog is None:
#        catalog_id = 99

    main(args.host, 1, credentials)
    
