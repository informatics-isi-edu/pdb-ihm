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
def define_tdoc_ihm_ordered_model():
    table_name='ihm_ordered_model'
    comment='Details of model groups related by time or other order; model groups are represented as nodes with directed edges between them indicating the ordering; mmCIF category: ihm_ordered_model'

    column_defs = [
        Column.define(
            'process_id',
            builtin_types.int8,
            comment='Identifier for the ordered process',                        
            nullok=False
        ),
        Column.define(
            'process_description',
            builtin_types.text,
            comment='Description of the ordered process',
            nullok=True
        ),
        Column.define(
            'edge_id',
            builtin_types.int8,
            comment='Identifier for the edge in a directed graph',   
            nullok=False
        ),
        Column.define(
            'edge_description',
            builtin_types.text,
            comment='Description of the edge in a directed graph',
            nullok=True
        ),
        Column.define(
            'step_id',
            builtin_types.int8,
            comment='Identifier for a step in the ordered process',   
            nullok=False
        ),
        Column.define(
            'step_description',
            builtin_types.text,
            comment='Description of the step in the ordered process',
            nullok=True
        ),
        Column.define(
            'ordered_by',
            builtin_types.text,
            comment='Parameter based on which the ordering is carried out, e.g., time steps, steps in an assembly process, steps in a metabolic pathway, steps in an interaction pathway',
            nullok=False
        ),
        Column.define(
            'model_group_id_begin',
            builtin_types.int8,
            comment='Model group id corresponding to the node at the origin of the directed edge',
            nullok=False
        ),
        Column.define(
            'model_group_id_end',
            builtin_types.int8,
            comment='Model group id corresponding to the node at the end of the directed edge',
            nullok=False
        ),
        Column.define(
            "structure_id",
            builtin_types.text,
            comment='Structure identifier',
            nullok=False
        ),
        Column.define(
            "Model_Group_RID",
            builtin_types.text,
            comment='Identifier to the model group RID',
            nullok=False
        )
    ]
    key_defs = [
        Key.define(["structure_id", "edge_id", "process_id"], constraint_names=[["PDB", "ihm_ordered_model_primary_key"]] ),
        Key.define(["RID"], constraint_names=[["PDB", "ihm_ordered_model_RID_key"]] )
    ]

    fkey_defs = [
        ForeignKey.define(["structure_id"], "PDB", "entry", ["id"],
                          constraint_names=[["PDB", "ihm_ordered_model_structure_id_fkey"]],
                          on_update="CASCADE",
                          on_delete="NO ACTION"
        ),
        ForeignKey.define(["Model_Group_RID", "structure_id", "model_group_id_begin"], "PDB", "ihm_model_group", ["RID", "structure_id", "id"],
                          constraint_names=[["PDB", "ihm_ordered_model_ihm_model_group_1_combo1_fkey"]],
                          on_update="CASCADE",
                          on_delete="NO ACTION"
        ),
        ForeignKey.define(["Model_Group_RID", "structure_id", "model_group_id_end"], "PDB", "ihm_model_group", ["RID", "structure_id", "id"],
                          constraint_names=[["PDB", "ihm_ordered_model_ihm_model_group_2_combo1_fkey"]],
                          on_update="CASCADE",
                          on_delete="NO ACTION"
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

# --------------------------------------------------------------
def table_comments(model):

    model.table("PDB", "ihm_ordered_ensemble").comment = "Details of model groups related by time or other order; model groups are represented as nodes with directed edges between them indicating the ordering; mmCIF category: ihm_ordered_ensemble (to be deprecated and superseded by ihm_ordered_model)"

# ============================================================
def main(server_name, catalog_id, credentials):
    server = DerivaServer('https', server_name, credentials)
    catalog = server.connect_ermrest(catalog_id)
    catalog.dcctx['cid'] = 'oneoff/model'
    model = catalog.getCatalogModel()

    """
    Update table comments
    """
    table_comments(model)

    """
    Create keys for existing tables
    """
    utils.create_key_if_not_exists(model, 'PDB', 'ihm_model_group', ['RID', 'structure_id', 'id'], 'ihm_model_group_combo1_key')

    """
    Create table
    """
    utils.create_table_if_not_exist(model, 'PDB',  define_tdoc_ihm_ordered_model())

# ===================================================    

if __name__ == '__main__':
    args = BaseCLI('ad-hoc table creation tool', None, 1).parse_cli()
    credentials = get_credential(args.host, args.credential_file)

    main(args.host, 1, credentials)
    
