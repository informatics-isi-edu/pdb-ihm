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

    utils.set_nullok_column_if_exists(model, 'Vocab', 'File_Type', 'Table_Name', False)
    utils.set_nullok_column_if_exists(model, 'PDB', 'ihm_entity_poly_segment', 'Entity_Poly_Seq_RID_Begin', False)
    utils.set_nullok_column_if_exists(model, 'PDB', 'ihm_entity_poly_segment', 'Entity_Poly_Seq_RID_End', False)
    utils.create_foreign_key_if_not_exists(model, 'PDB', 'ihm_entity_poly_segment', 'ihm_entity_poly_segment_mm_poly_res_label_begin_fkey', 
                                            ForeignKey.define(['Entity_Poly_Seq_RID_Begin', 'structure_id', 'comp_id_begin', 'entity_id', 'seq_id_begin'], 'PDB', 'entity_poly_seq', ['RID', 'structure_id', 'mon_id', 'entity_id', 'num'],
                                                                                            constraint_names=[ ['PDB', 'ihm_entity_poly_segment_mm_poly_res_label_begin_fkey'] ],
                                                                                            on_update='CASCADE',
                                                                                            on_delete='SET NULL')
                                                )
    utils.create_foreign_key_if_not_exists(model, 'PDB', 'ihm_entity_poly_segment', 'ihm_entity_poly_segment_mm_poly_res_label_end_fkey', 
                                            ForeignKey.define(['Entity_Poly_Seq_RID_End', 'seq_id_end', 'structure_id', 'comp_id_end', 'entity_id'], 'PDB', 'entity_poly_seq', ['RID', 'num', 'structure_id', 'mon_id', 'entity_id'],
                                                                                            constraint_names=[ ['PDB', 'ihm_entity_poly_segment_mm_poly_res_label_end_fkey'] ],
                                                                                            on_update='CASCADE',
                                                                                            on_delete='SET NULL')
                                                )

# ===================================================    

if __name__ == '__main__':
    args = BaseCLI('ad-hoc table creation tool', None, 1).parse_cli()
    credentials = get_credential(args.host, args.credential_file)
#    if args.catalog is None:
#        catalog_id = 99

    main(args.host, 50, credentials)
    
