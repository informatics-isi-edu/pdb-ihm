import sys
import json
from deriva.core import ErmrestCatalog, AttrDict, get_credential, DEFAULT_CREDENTIAL_FILE, tag, urlquote, DerivaServer, get_credential, BaseCLI
from deriva.core.ermrest_model import builtin_types, Schema, Table, Column, Key, ForeignKey, DomainType, ArrayType
import utils
import re
from utils import ApplicationClient

# ========================================================

# ============================================================

def main(server_name, catalog_id, credentials):
    server = DerivaServer('https', server_name, credentials)
    catalog = server.connect_ermrest(catalog_id)
    catalog.dcctx['cid'] = 'oneoff/model'
    model = catalog.getCatalogModel()

    """
    Drop existing FK
    """
    utils.drop_fkey_if_exist(model, 'PDB', 'ihm_ordered_model', 'ihm_ordered_model_ihm_model_group_1_combo1_fkey')
    utils.drop_fkey_if_exist(model, 'PDB', 'ihm_ordered_model', 'ihm_ordered_model_ihm_model_group_2_combo1_fkey')
    
    """
    Rename column
    """
    utils.rename_column_if_exists(model, 'PDB', 'ihm_ordered_model', 'Model_Group_RID', 'Model_Group_Begin_RID')
    
    """
    Create column
    """
    utils.create_column_if_not_exist(model, 'PDB', 'ihm_ordered_model', 
                                     Column.define(
                                        'Model_Group_End_RID',
                                        builtin_types.text,
                                        comment='Foreign Key to the ihm_model_group.id.',
                                        nullok=True
                                    ))

    """
    Update the Model_Group_End_RID values
    """
    url = '/attribute/A:=PDB:ihm_ordered_model/A:RID,A:Model_Group_Begin_RID'
    resp = catalog.get(url)
    resp.raise_for_status()
    rows = resp.json()
    
    """
    Update the Model_Group_End_RID values
    """
    updated_rows = []
    for row in rows:
        updated_rows.append({'RID': row['RID'], 'Model_Group_End_RID': row['Model_Group_Begin_RID']})

    url = '/attributegroup/PDB:ihm_ordered_model/RID;Model_Group_End_RID'
    resp = catalog.put(
        url,
        json=updated_rows
    )
    resp.raise_for_status()
    
    """
    Set the constraint Entry_RCB NOT NULL
    """
    utils.set_nullok_column_if_exists(model, 'PDB', 'ihm_ordered_model', 'Model_Group_End_RID', False)

    """
    Create FK
    """
    utils.create_foreign_key_if_not_exists(model, 'PDB', 'ihm_ordered_model', 'ihm_ordered_model_ihm_model_group_begin_combo1_fkey', 
                                            ForeignKey.define(['Model_Group_Begin_RID', 'structure_id', 'model_group_id_begin'], 'PDB', 'ihm_model_group', ['RID', 'structure_id', 'id'],
                                                                                            constraint_names=[ ['PDB', 'ihm_ordered_model_ihm_model_group_begin_combo1_fkey'] ],
                                                                                            on_update='CASCADE',
                                                                                            on_delete='NO ACTION'))

    utils.create_foreign_key_if_not_exists(model, 'PDB', 'ihm_ordered_model', 'ihm_ordered_model_ihm_model_group_end_combo1_fkey', 
                                            ForeignKey.define(['Model_Group_End_RID', 'structure_id', 'model_group_id_end'], 'PDB', 'ihm_model_group', ['RID', 'structure_id', 'id'],
                                                                                            constraint_names=[ ['PDB', 'ihm_ordered_model_ihm_model_group_end_combo1_fkey'] ],
                                                                                            on_update='CASCADE',
                                                                                            on_delete='NO ACTION'))

# ===================================================    

if __name__ == '__main__':
    args = ApplicationClient('ad-hoc table creation tool', None, 1).parse_cli()
    credentials = get_credential(args.host, args.credential_file)
    main(args.host, args.catalog_id, credentials)

