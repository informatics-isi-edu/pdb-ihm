import sys
import json
from deriva.core import ErmrestCatalog, AttrDict, get_credential, DEFAULT_CREDENTIAL_FILE, tag, urlquote, DerivaServer, get_credential, BaseCLI
from deriva.core.ermrest_model import builtin_types, Schema, Table, Column, Key, ForeignKey, DomainType, ArrayType
import utils


# ========================================================
# -- create a table that is not a Vocab structure
def define_tdoc_struct_ref():
    table_name='struct_ref'
    comment='Table that provides reference information regarding the macromolecules in the integrative model available from external repositories such as UNIPROT and GENBANK; mmCIF category: struct_ref'

    column_defs = [
        Column.define(
            "id",
            builtin_types.text,
            comment='An identifier for the reference',
            nullok=False
        ),
        Column.define(
            "entity_id",
            builtin_types.text,
            comment='An identifier to the molecular entity in the ENTITY table',
            nullok=False
        ),
        Column.define(
            "db_name",
            builtin_types.text,
            comment='The name of the database containing reference information about this entity',
            nullok=False
        ),
        Column.define(
            "db_code",
            builtin_types.text,
            comment='The code for this entity in the named database',
            nullok=False
        ),
        Column.define(
            "pdbx_db_accession",
            builtin_types.text,
            comment='Accession code assigned by the reference database',
            nullok=True
        ),
        Column.define(
            "pdbx_db_isoform",
            builtin_types.text,
            comment='Database code assigned by the reference database for a sequence isoform',
            nullok=True
        ),
        Column.define(
            "pdbx_align_begin",
            builtin_types.text,
            comment='Beginning index in the chemical sequence from the reference database',
            nullok=True
        ),
        Column.define(
            "pdbx_align_end",
            builtin_types.text,
            comment='Ending index in the chemical sequence from the reference database',
            nullok=True
        ),
        Column.define(
            "pdbx_seq_one_letter_code",
            builtin_types.text,
            comment='Database chemical sequence expressed as string of one-letter amino acid or nucleotide codes',
            nullok=True
        ),
        Column.define(
            "details",
            builtin_types.text,
            comment='Additional details about the reference',
            nullok=True
        ),
        Column.define(
            "structure_id",
            builtin_types.text,
            comment='Structure identifier',
            nullok=False
        ),
        # HT: to use for Chaise
        Column.define(
            "Entity_RID",
            builtin_types.text,
            comment='Identifier to the entity RID',
            nullok=False
        )
    ]
    key_defs = [
        Key.define(["structure_id", "id"], constraint_names=[["PDB", "struct_ref_primary_key"]] ),
        Key.define(["RID"], constraint_names=[["PDB", "struct_ref_RID_key"]] ),
        Key.define(["RID", "structure_id", "id"], constraint_names=[["PDB", "struct_ref_combo1_key"]] )
    ]

    # @brinda: add fk pseudo-definition
    fkey_defs = [
        # HT: it own fk to Entry table
        ForeignKey.define(["structure_id"], "PDB", "entry", ["id"],
                          constraint_names=[["PDB", "struct_ref_structure_id_fkey"]],
                          on_update="CASCADE",
                          on_delete="NO ACTION"
        ),
        # HT: In annotation, apply domain_filter to filter the RID list by constraining structure_id        
        ForeignKey.define(["Entity_RID", "structure_id", "entity_id"], "PDB", "entity", ["RID", "structure_id", "id"],
                          constraint_names=[["PDB", "struct_ref_entity_combo1_fkey"]],
                          on_update="CASCADE",
                          on_delete="NO ACTION"
        ),
        ForeignKey.define(["db_name"], "Vocab", "struct_ref_db_name", ["Name"],
                          constraint_names=[ ["Vocab", "struct_ref_db_name_fkey"] ],
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

# ==========================================================================
def define_tdoc_struct_ref_seq():
    table_name='struct_ref_seq'
    comment='Table that provides a mechanism for indicating and annotating the regions of alignment between the macromolecular sequence of an entity in the integrative model and the sequence in the reference database; mmCIF category: struct_ref_seq'

    column_defs = [
        Column.define(
            "align_id",
            builtin_types.text,
            comment='A unique identifier for a record in the table',
            nullok=False
        ),
        Column.define(
            "ref_id",
            builtin_types.text,
            comment='A pointer to the reference in the struct_ref table',
            nullok=False
        ),
        Column.define(
            "db_align_beg",
            builtin_types.int8,
            comment='The sequence position in the referenced database entry at which the alignment begins',
            nullok=False
        ),
        Column.define(
            "db_align_end",
            builtin_types.int8,
            comment='The sequence position in the referenced database entry at which the alignment ends',
            nullok=False
        ),
        Column.define(
            "seq_align_beg",
            builtin_types.int8,
            comment='The position in the macromolecular entity sequence at which the alignment begins',
            nullok=False
        ),
        Column.define(
            "seq_align_end",
            builtin_types.int8,
            comment='The position in the macromolecular entity sequence at which the alignment ends',
            nullok=False
        ),
        Column.define(
            "details",
            builtin_types.text,
            comment='Additional details about the alignment',
            nullok=True
        ),
        Column.define(
            "structure_id",
            builtin_types.text,
            comment='Structure identifier',
            nullok=False
        ),
        # HT: to use for Chaise
        Column.define(
            "Ref_RID",
            builtin_types.text,
            comment='Identifier to the reference RID',
            nullok=False
        )
    ]
    key_defs = [
        Key.define(["structure_id", "align_id"], constraint_names=[["PDB", "struct_ref_seq_primary_key"]] ),
        Key.define(["RID"], constraint_names=[["PDB", "struct_ref_seq_RID_key"]] ),
        Key.define(["RID", "structure_id", "align_id"], constraint_names=[["PDB", "struct_ref_seq_combo1_key"]] )
    ]

    # @brinda: add fk pseudo-definition
    fkey_defs = [
        # HT: it own fk to Entry table
        ForeignKey.define(["structure_id"], "PDB", "entry", ["id"],
                          constraint_names=[["PDB", "struct_ref_seq_structure_id_fkey"]],
                          on_update="CASCADE",
                          on_delete="NO ACTION"
        ),
        # HT: In annotation, apply domain_filter to filter the RID list by constraining structure_id        
        ForeignKey.define(["Ref_RID", "structure_id", "ref_id"], "PDB", "struct_ref", ["RID", "structure_id", "id"],
                          constraint_names=[["PDB", "struct_ref_seq_struct_ref_combo1_fkey"]],
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

# ==========================================================================
def define_tdoc_struct_ref_seq_dif():
    table_name='struct_ref_seq_dif'
    comment='Table that provides a mechanism for indicating and annotating point differences in the alignment of the macromolecular sequence with the reference sequence; mmCIF category: struct_ref_seq_dif'

    column_defs = [
        Column.define(
            "pdbx_ordinal",
            builtin_types.int8,
            comment='A unique identifier for a record in the table',
            nullok=False
        ),
        Column.define(
            "align_id",
            builtin_types.text,
            comment='A pointer to the alignment in the struct_ref_seq table',
            nullok=False
        ),
        Column.define(
            "seq_num",
            builtin_types.int8,
            comment='The position in the macromolecular sequence with the point difference',
            nullok=True
        ),
        Column.define(
            "mon_id",
            builtin_types.text,
            comment='The monomer type in the macromolecular sequence with the point difference',
            nullok=True
        ),
        Column.define(
            "db_mon_id",
            builtin_types.text,
            comment='The monomer type in the reference database sequence with the point difference',
            nullok=True
        ),
        Column.define(
            "details",
            builtin_types.text,
            comment='Additional details about the special aspects of the point difference',
            nullok=True
        ),
        Column.define(
            "structure_id",
            builtin_types.text,
            comment='Structure identifier',
            nullok=False
        ),
        # HT: to use for Chaise
        Column.define(
            "Align_RID",
            builtin_types.text,
            comment='Identifier to the alignment RID',
            nullok=False
        )
    ]
    key_defs = [
        Key.define(["structure_id", "pdbx_ordinal"], constraint_names=[["PDB", "struct_ref_seq_dif_primary_key"]] ),
        Key.define(["RID"], constraint_names=[["PDB", "struct_ref_seq_dif_RID_key"]] )
    ]

    # @brinda: add fk pseudo-definition
    fkey_defs = [
        # HT: it own fk to Entry table
        ForeignKey.define(["structure_id"], "PDB", "entry", ["id"],
                          constraint_names=[["PDB", "struct_ref_seq_dif_structure_id_fkey"]],
                          on_update="CASCADE",
                          on_delete="NO ACTION"
        ),
        # HT: In annotation, apply domain_filter to filter the RID list by constraining structure_id        
        ForeignKey.define(["Align_RID", "structure_id", "align_id"], "PDB", "struct_ref_seq", ["RID", "structure_id", "align_id"],
                          constraint_names=[["PDB", "struct_ref_seq_dif_struct_ref_seq_combo1_fkey"]],
                          on_update="CASCADE",
                          on_delete="NO ACTION"
        ),
        ForeignKey.define(["details"], "Vocab", "struct_ref_seq_dif_details", ["Name"],
                          constraint_names=[ ["Vocab", "struct_ref_seq_dif_details_fkey"] ],
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

# ==========================================================================

def update_PDB_entity(model):
    table = model.schemas['PDB'].tables['entity']

    table.create_key(
        Key.define(["RID", "structure_id", "id"], constraint_names=[["PDB", "entity_combo1_key"]] )
    )

# ---------------
# update vocab table
def add_rows_to_Vocab_struct_ref_seq_dif_details(catalog):

    rows =[
        {'Name': 'acetylation', 'Description': 'acetylation'},
        {'Name': 'amidation', 'Description': 'amidation'},
        {'Name': 'chromophore', 'Description': 'chromophore'},
        {'Name': 'cloning artifact', 'Description': 'cloning artifact'},
        {'Name': 'conflict', 'Description': 'conflict'},
        {'Name': 'deletion', 'Description': 'deletion'},
        {'Name': 'engineered mutation', 'Description': 'engineered mutation'},
        {'Name': 'expression tag', 'Description': 'expression tag'},
        {'Name': 'initiating methionine', 'Description': 'initiating methionine'},
        {'Name': 'insertion', 'Description': 'insertion'},
        {'Name': 'linker', 'Description': 'linker'},
        {'Name': 'microheterogeneity', 'Description': 'microheterogeneity'},
        {'Name': 'microheterogeneity/modified residue', 'Description': 'microheterogeneity/modified residue'},
        {'Name': 'modified residue', 'Description': 'modified residue'},
        {'Name': 'variant', 'Description': 'variant'},
    ]
    
    pb = catalog.getPathBuilder()
    schema = pb.Vocab
    struct_ref_seq_dif_details = schema.struct_ref_seq_dif_details
    struct_ref_seq_dif_details.insert(rows, defaults=['ID', 'URI'])

# -----------------------------------
def add_rows_to_Vocab_struct_ref_db_name(catalog):

    rows =[
        {'Name': 'UNP', 'Description': 'UNIPROT'},
        {'Name': 'GB', 'Description': 'GENBANK'}
    ]

    pb = catalog.getPathBuilder()
    schema = pb.Vocab
    struct_ref_db_name = schema.struct_ref_db_name
    struct_ref_db_name.insert(rows, defaults=['ID', 'URI'])


# ============================================================
def main(server_name, catalog_id, credentials):
    server = DerivaServer('https', server_name, credentials)
    catalog = server.connect_ermrest(catalog_id)
    catalog.dcctx['cid'] = "oneoff/model"
    model = catalog.getCatalogModel()
    
    #-- clean up
    if False:
        drop_table(catalog, 'PDB', 'struct_ref')
        drop_table(catalog, 'PDB', 'struct_ref_seq')
        drop_table(catalog, 'PDB', 'struct_ref_seq_dif') 
    
    # new changes
    if True:
        model = catalog.getCatalogModel()    
    
        utils.create_table_if_not_exist(model, "Vocab",  utils.define_Vocab_table('struct_ref_db_name', 'The name of the database containing reference information'))
        utils.create_table_if_not_exist(model, "Vocab",  utils.define_Vocab_table('struct_ref_seq_dif_details', 'Details about the special aspects of point differences in the alignment of the macromolecular sequence in the integrative model and the sequence in the reference database'))
        add_rows_to_Vocab_struct_ref_db_name(catalog)
        add_rows_to_Vocab_struct_ref_seq_dif_details(catalog)
        update_PDB_entity(model)
        utils.create_table_if_not_exist(model, "PDB",  define_tdoc_struct_ref())
        utils.create_table_if_not_exist(model, "PDB",  define_tdoc_struct_ref_seq())
        utils.create_table_if_not_exist(model, "PDB",  define_tdoc_struct_ref_seq_dif())
        
    # vocab
    #if False:
    #    add_rows_to_Vocab_ihm_derived_angle_restraint_group_conditionality(catalog)
    #    add_rows_to_Vocab_ihm_derived_angle_restraint_restraint_type(catalog)
    

# ===================================================    

if __name__ == '__main__':
    args = BaseCLI("ad-hoc table creation tool", None, 1).parse_cli()
    credentials = get_credential(args.host, args.credential_file)
#    if args.catalog is None:
#        catalog_id = 99

    main(args.host, 99, credentials)
    
