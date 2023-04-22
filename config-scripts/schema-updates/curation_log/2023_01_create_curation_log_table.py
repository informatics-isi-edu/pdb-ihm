import sys                
import json               
from deriva.core import ErmrestCatalog, AttrDict, get_credential, DEFAULT_CREDENTIAL_FILE, tag, urlquote, DerivaServer, get_credential, BaseCLI
from deriva.core.ermrest_model import builtin_types, Schema, Table, Column, Key, ForeignKey, DomainType, ArrayType
import utils

def define_tdoc_Curation_Log():
    table_name='Curation_Log'
    comment='Log information regarding curation steps and communication with depositor'

    column_defs = [
         Column.define(
            'Entry',
            builtin_types.text,
            nullok=False,
            comment='Entry Identifier'
        ),
       Column.define(
            'Log_Date',
            builtin_types.date,
            nullok=False,
            comment='Date of creation of the log'
        ),
        Column.define(
            "Details",
            builtin_types.markdown,
            comment='Details of the log',                        
            nullok=False
        ),
        Column.define(
            "Submitter_Allow",
            builtin_types.boolean,
            comment='Flag to indicate if submitter can see the log. Default is False.',                                       
            nullok=True,
            default=False
        )
    ]
    
    fkey_defs = [
        ForeignKey.define(["Entry"], "PDB", "entry", ["id"],
                          constraint_names=[ ["PDB", "Curation_Log_Entry_fkey"] ],
                          on_update="CASCADE",
                          on_delete="CASCADE"
        ),
        ForeignKey.define(["RCB"], "public", "ERMrest_Client", ["ID"],
                          constraint_names=[["PDB", '{}_RCB_fkey'.format(table_name)]],
                          on_update="NO ACTION",
                          on_delete="NO ACTION"   
        ),
        ForeignKey.define(["RMB"], "public", "ERMrest_Client", ["ID"],
                          constraint_names=[["PDB", '{}_RMB_fkey'.format(table_name)]],
                          on_update="NO ACTION",
                          on_delete="NO ACTION"   
        )
    ]
    table_def = Table.define(
        table_name,
        column_defs,
        fkey_defs=fkey_defs,
        comment=comment,
        provide_system=True
    )
    return table_def

def update_PDB_entry(model):
    # Add the PDB.entry.Submitter_Flag and PDB.entry.Submitter_Flag_date columns  
    utils.create_column_if_not_exist(model, 'PDB', 'entry',
                                     Column.define(
                                        'Submitter_Flag',
                                        builtin_types.boolean,
                                        comment='This flag is set to "true" when the entry is waiting for input from user.', 
                                        nullok=True
                                    ))

    utils.create_column_if_not_exist(model, 'PDB', 'entry',
                                     Column.define(
                                        'Submitter_Flag_Date',
                                        builtin_types.date,
                                        comment='Date last communicated with the submitter. Waiting for response from submitter.',
                                        nullok=True
                                    ))

# ============================================================
def main(server_name, catalog_id, credentials):
    server = DerivaServer('https', server_name, credentials)
    catalog = server.connect_ermrest(catalog_id)
    catalog.dcctx['cid'] = 'oneoff/model'
    model = catalog.getCatalogModel()

    """
    Create table
    """
    utils.create_table_if_not_exist(model, 'PDB',  define_tdoc_Curation_Log())

    """
    Update table
    """
    update_PDB_entry(model)

# ===================================================    

if __name__ == '__main__':
    args = BaseCLI('ad-hoc table creation tool', None, 1).parse_cli()
    credentials = get_credential(args.host, args.credential_file)

    main(args.host, 99, credentials)

