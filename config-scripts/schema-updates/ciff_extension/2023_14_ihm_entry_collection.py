import sys
import json
from deriva.core import ErmrestCatalog, AttrDict, get_credential, DEFAULT_CREDENTIAL_FILE, tag, urlquote, DerivaServer, get_credential, BaseCLI
from deriva.core.ermrest_model import builtin_types, Schema, Table, Column, Key, ForeignKey, DomainType, ArrayType
import utils

"""
This script will be run after:
    - 
"""

# ========================================================
# -- create a table that is not a Vocab structure
# -- define ihm_entry_collection table
def define_tdoc_ihm_entry_collection():
    table_name='ihm_entry_collection'
    comment='Define collection of IHM entries that belong to a single deposition or group; mmCIF category: ihm_entry_collection'

    column_defs = [
        Column.define(
            'id',
            builtin_types.text,
            comment='A unique identifier for the entry collection assigned by the archive',                        
            nullok=False
        ),
        Column.define(
            'name',
            builtin_types.text,
            comment='Name for the entry collection',
            nullok=True
        ),
        Column.define(
            'details',
            builtin_types.text,
            comment='Details about the entry collection',
            nullok=True
        )
    ]
    #BV: This is a parent table with simple keys
    key_defs = [
        Key.define(['id'], constraint_names=[['PDB', 'ihm_entry_collection_id_key']] )
    ]

    #BV: No outgoing fkeys 
    fkey_defs = []
    
    table_def = Table.define(
        table_name,
        column_defs,
        key_defs=key_defs,
        fkey_defs=fkey_defs,
        comment=comment,
        provide_system=True
    )
    
    return table_def

# --------------------------------------------------------------

def define_tdoc_ihm_entry_collection_mapping():
    table_name='ihm_entry_collection_mapping'
    comment='Category that identifies entries that belong to a collection; mmCIF category: ihm_entry_collection_mapping'

    column_defs = [
        Column.define(
            'collection_id',
            builtin_types.text,
            comment='Identifier for the entry collection',
            nullok=False
        ),
        Column.define(
            'entry_id',
            builtin_types.text,
            comment='Identifier for the entry',
            nullok=False
        )
    ]

    #BV: This is a leaf table; so no combo1/combo2 key required
    key_defs = [
        Key.define(['entry_id', 'collection_id'], constraint_names=[['PDB', 'ihm_entry_collection_mapping_primary_key']] )
    ]

    #BV: Outgoing fkeys are entry_id and collection_id, which are simple fkeys
    fkey_defs = [
        ForeignKey.define(['entry_id'], 'PDB', 'entry', ['id'],
                          constraint_names=[['PDB', 'ihm_entry_collection_mapping_entry_id_fkey']],
                          on_update='CASCADE',
                          on_delete='NO ACTION'
        ),
        ForeignKey.define(['collection_id'], 'PDB', 'ihm_entry_collection', ['id'],
                          constraint_names=[['PDB', 'ihm_entry_collection_mapping_collection_id_fkey']],
                          on_update='CASCADE',
                          on_delete='NO ACTION'
        )
    ]

    table_def = Table.define(
        table_name,
        column_defs,
        key_defs=key_defs,
        fkey_defs=fkey_defs,
        comment=comment,
        provide_system=True
    )

    return table_def

# ============================================================
def main(server_name, catalog_id, credentials):
    server = DerivaServer('https', server_name, credentials)
    catalog = server.connect_ermrest(catalog_id)
    catalog.dcctx['cid'] = 'oneoff/model'
    model = catalog.getCatalogModel()

    """
    Create table
    """
    utils.create_table_if_not_exist(model, 'PDB',  define_tdoc_ihm_entry_collection())
    utils.create_table_if_not_exist(model, 'PDB',  define_tdoc_ihm_entry_collection_mapping())

# ===================================================    

if __name__ == '__main__':
    args = BaseCLI('ad-hoc table creation tool', None, 1).parse_cli()
    credentials = get_credential(args.host, args.credential_file)

    main(args.host, 99, credentials)
    
