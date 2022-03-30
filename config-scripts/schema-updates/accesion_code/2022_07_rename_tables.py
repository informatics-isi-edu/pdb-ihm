import sys
import json
from deriva.core import ErmrestCatalog, AttrDict, get_credential, DEFAULT_CREDENTIAL_FILE, tag, urlquote, DerivaServer, get_credential, BaseCLI
from deriva.core.ermrest_model import builtin_types, Schema, Table, Column, Key, ForeignKey, DomainType, ArrayType
import utils
import re

# ============================================================
def main(server_name, catalog_id, credentials):
    server = DerivaServer('https', server_name, credentials)
    catalog = server.connect_ermrest(catalog_id)
    catalog.dcctx['cid'] = 'oneoff/model'
    model = catalog.getCatalogModel()
    
    """
    Drop FK if exists
    """
    utils.drop_fkey_if_exist(model, 'PDB', 'entry', 'entry_process_status_fkey')
    utils.drop_fkey_if_exist(model, 'PDB', 'Entry_Related_File', 'Entry_Related_File_process_status_fkey')

    utils.drop_fkey_if_exist(model, 'PDB', 'entry', 'entry_workflow_status_fkey')
    utils.drop_fkey_if_exist(model, 'PDB', 'Entry_Related_File', 'Entry_Related_File_workflow_status_fkey')

    """
    Rename table if exists
    """
    utils.rename_table_if_exists(model, 'Vocab', 'process_status', 'Process_Status')
    utils.rename_table_if_exists(model, 'Vocab', 'workflow_status', 'Workflow_Status')

    model = catalog.getCatalogModel()

    """
    Create the FK
    """
    utils.create_foreign_key_if_not_exists(model, 'PDB', 'entry', 'entry_Process_Status_fkey',
                                            ForeignKey.define(['Process_Status'], 'Vocab', 'Process_Status', ['Name'],
                                              constraint_names=[ ['PDB', 'entry_Process_Status_fkey'] ],
                                              on_update='CASCADE',
                                              on_delete='SET NULL')
                                           )

    utils.create_foreign_key_if_not_exists(model, 'PDB', 'entry', 'entry_Workflow_Status_fkey',
                                            ForeignKey.define(['Workflow_Status'], 'Vocab', 'Workflow_Status', ['Name'],
                                              constraint_names=[ ['PDB', 'entry_Workflow_Status_fkey'] ],
                                              on_update='CASCADE',
                                              on_delete='SET NULL')
                                           )

    utils.create_foreign_key_if_not_exists(model, 'PDB', 'Entry_Related_File', 'Entry_Related_File_Process_Status_fkey',
                                            ForeignKey.define(['Process_Status'], 'Vocab', 'Process_Status', ['Name'],
                                              constraint_names=[ ['PDB', 'Entry_Related_File_Process_Status_fkey'] ],
                                              on_update='CASCADE',
                                              on_delete='SET NULL')
                                           )

    utils.create_foreign_key_if_not_exists(model, 'PDB', 'Entry_Related_File', 'Entry_Related_File_Workflow_Status_fkey',
                                            ForeignKey.define(['Workflow_Status'], 'Vocab', 'Workflow_Status', ['Name'],
                                              constraint_names=[ ['PDB', 'Entry_Related_File_Workflow_Status_fkey'] ],
                                              on_update='CASCADE',
                                              on_delete='SET NULL')
                                           )
    
# ===================================================    

if __name__ == '__main__':
    args = BaseCLI('ad-hoc table creation tool', None, 1).parse_cli()
    credentials = get_credential(args.host, args.credential_file)
    main(args.host, 1, credentials)
    
