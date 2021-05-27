import sys
import json
from deriva.core import ErmrestCatalog, AttrDict, get_credential, DEFAULT_CREDENTIAL_FILE, tag, urlquote, DerivaServer, get_credential, BaseCLI
from deriva.core.ermrest_model import builtin_types, Schema, Table, Column, Key, ForeignKey, DomainType, ArrayType
import utils

"""
This script will be run after:
    - 2021_11_update_vocab.py
    - 2021_04_ihm_data_transformation.py
    - 2021_01_ihm_data_transformation.py
    - 2021_02_ihm_data_transformation.py
"""

# ========================================================
# -- create a table that is not a Vocab structure
def define_tdoc_ihm_ensemble_sub_sample():
    table_name='ihm_ensemble_sub_sample'
    comment='Details of the sub samples within the ensembles; mmCIF category: ihm_ensemble_sub_sample'

    column_defs = [
        Column.define(
            'id',
            builtin_types.int8,
            comment='A unique id for the ensemble sub sample',
            nullok=False
        ),
        Column.define(
            'sample_name',
            builtin_types.text,
            comment='A name for the ensemble sub sample',
            nullok=True
        ),
        Column.define(
            'ensemble_id',
            builtin_types.int8,
            comment='The ensemble identifier corresponding to the sub sample',
            nullok=False
        ),
        Column.define(
            'num_models',
            builtin_types.int8,
            comment='The number of models in the ensemble sub sample',
            nullok=False
        ),
        Column.define(
            'num_models_deposited',
            builtin_types.int8,
            comment='The number of models in the sub sample that are deposited',
            nullok=True
        ),
        Column.define(
            'model_group_id',
            builtin_types.int8,
            comment='The model group identifier corresponding to the sub sample',
            nullok=True
        ),
        Column.define(
            'file_id',
            builtin_types.int8,
            comment='A reference to the external file containing the structural models in the sub sample',
            nullok=True
        ),
        Column.define(
            'structure_id',
            builtin_types.text,
            comment='Structure identifier',
            nullok=False
        ),
        Column.define(
            'Ensemble_RID',
            builtin_types.text,
            comment='Identifier to the ensemble RID',
            nullok=False
        ),
        Column.define(
            'Model_Group_RID',
            builtin_types.text,
            comment='Identifier to the model group RID',
            nullok=True
        ),
        Column.define(
            'File_RID',
            builtin_types.text,
            comment='Identifier to the external file RID',
            nullok=True
        )
    ]
    #BV: This is a leaf table; so no combo1/combo2 keys required
    key_defs = [
        Key.define(['structure_id', 'id'], constraint_names=[['PDB', 'ihm_ensemble_sub_sample_primary_key']] ),
        Key.define(['RID'], constraint_names=[['PDB', 'ihm_ensemble_sub_sample_RID_key']] ),
    ]

    # @brinda: add fk pseudo-definition
    fkey_defs = [
        ForeignKey.define(['structure_id'], 'PDB', 'entry', ['id'],
                          constraint_names=[['PDB', 'ihm_ensemble_sub_sample_structure_id_fkey']],
                          on_update='CASCADE',
                          on_delete='NO ACTION'
        ),
        ForeignKey.define(['Ensemble_RID', 'structure_id', 'ensemble_id'], 'PDB', 'ihm_ensemble_info', ['RID', 'structure_id', 'ensemble_id'],
                          constraint_names=[['PDB', 'ihm_ensemble_sub_sample_ihm_ensemble_info_combo1_fkey']],
                          on_update='CASCADE',
                          on_delete='NO ACTION'
        ),
        ForeignKey.define(['Model_Group_RID', 'model_group_id'], 'PDB', 'ihm_model_group', ['RID', 'id'],
                          constraint_names=[['PDB', 'ihm_ensemble_sub_sample_ihm_model_group_combo2_fkey']],
                          on_update='CASCADE',
                          on_delete='NO ACTION'
        ),
        ForeignKey.define(['File_RID', 'file_id'], 'PDB', 'ihm_external_files', ['RID', 'id'],
                          constraint_names=[['PDB', 'ihm_ensemble_sub_sample_ihm_external_files_combo2_fkey']],
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

    utils.create_table_if_not_exist(model, 'PDB',  define_tdoc_ihm_ensemble_sub_sample())
    utils.create_key_if_not_exists(model, 'PDB', 'ihm_ensemble_info', ['RID', 'structure_id', 'ensemble_id'], 'ihm_ensemble_info_combo1_key')
        

# ===================================================    

if __name__ == '__main__':
    args = BaseCLI('ad-hoc table creation tool', None, 1).parse_cli()
    credentials = get_credential(args.host, args.credential_file)
#    if args.catalog is None:
#        catalog_id = 99

    main(args.host, 99, credentials)
    
