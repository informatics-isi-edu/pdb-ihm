import sys
import json
from deriva.core import ErmrestCatalog, AttrDict, get_credential, DEFAULT_CREDENTIAL_FILE, tag, urlquote, DerivaServer, get_credential, BaseCLI
from deriva.core.ermrest_model import builtin_types, Schema, Table, Column, Key, ForeignKey, DomainType, ArrayType
import utils

# ========================================================

# ============================================================

def main(server_name, catalog_id, credentials):
    server = DerivaServer('https', server_name, credentials)
    catalog = server.connect_ermrest(catalog_id)
    catalog.dcctx['cid'] = 'oneoff/model'
    model = catalog.getCatalogModel()

    utils.alter_on_update_fkey_if_exist(model, 'PDB', 'Entry_Related_File', 'Entry_Related_File_File_Type_fkey', 'CASCADE')
    utils.create_column_if_not_exist(model, 'PDB', 'ihm_entity_poly_segment',
                                     Column.define(
                                        'Entity_Poly_Seq_RID_Begin',
                                        builtin_types.text,
                                        nullok=True
                                    ))
    utils.create_column_if_not_exist(model, 'PDB', 'ihm_entity_poly_segment',
                                     Column.define(
                                        'Entity_Poly_Seq_RID_End',
                                        builtin_types.text,
                                        nullok=True
                                    ))
    utils.create_key_if_not_exists(model, 'PDB', 'struct', ['entry_id'], 'struct_primary_key')
    utils.create_key_if_not_exists(model, 'PDB', 'entity_poly_seq', ['num', 'RID', 'entity_id', 'mon_id'], 'entity_poly_seq_combo2_key')
    utils.create_key_if_not_exists(model, 'PDB', 'entity_poly_seq', ['mon_id', 'num', 'structure_id', 'entity_id', 'RID'], 'entity_poly_seq_combo1_key')
    utils.drop_fkey_if_exist(model, 'PDB', 'ihm_entity_poly_segment', 'ihm_entity_poly_segment_mm_poly_res_label_begin_fkey')
    utils.drop_fkey_if_exist(model, 'PDB', 'ihm_entity_poly_segment', 'ihm_entity_poly_segment_mm_poly_res_label_end_fkey')
    

# ===================================================    

if __name__ == '__main__':
    args = BaseCLI('ad-hoc table creation tool', None, 1).parse_cli()
    credentials = get_credential(args.host, args.credential_file)
#    if args.catalog is None:
#        catalog_id = 99

    main(args.host, 50, credentials)
    
