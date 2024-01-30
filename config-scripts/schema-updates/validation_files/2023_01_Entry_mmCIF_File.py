import sys
import json
from deriva.core import ErmrestCatalog, AttrDict, get_credential, DEFAULT_CREDENTIAL_FILE, tag, urlquote, DerivaServer, get_credential, BaseCLI
from deriva.core.ermrest_model import builtin_types, Schema, Table, Column, Key, ForeignKey, DomainType, ArrayType
import utils

# ========================================================

def update_PDB_Entry_Generated_File(model):
    
    # Add the PDB.Entry_Generated_File.File_Type column    
    utils.create_column_if_not_exist(model, 'PDB', 'Entry_Generated_File', 
                                     Column.define(
                                        'File_Type',
                                        builtin_types.text,
                                        comment='Type of file, e.g., mmCIF, Full Validation PDF, Summary Validation PDF',
                                        nullok=False,
                                        default="mmCIF"
                                    ))

    # Create the foreign key PDB.Entry_Generated_File.File_Type references Vocab.System_Generated_Entry_File_Type.Name
    utils.create_foreign_key_if_not_exists(model, 'PDB', 'Entry_Generated_File', 'Entry_Generated_File_System_Generated_File_Type_fkey', 
                                            ForeignKey.define(['File_Type'], 'Vocab', 'System_Generated_File_Type', ['Name'],
                                              constraint_names=[ ['Vocab', 'Entry_Generated_File_System_Generated_File_Type_fkey'] ],
                                              on_update='CASCADE',
                                              on_delete='NO ACTION')
                                           )

def add_rows_to_Vocab_Table_System_Generated_File_Type(catalog):
    #Add rows to Vocab.System_Generated_File_Type table
    rows =[
        {'Name': 'Validation: Full PDF', 'Description': 'System generated full validation report in PDF format'},
        {'Name': 'Validation: Summary PDF', 'Description': 'System generated summary validation report in PDF format'},
        {'Name': 'Validation: HTML tar.gz', 'Description': 'System generated full validation report in HTML format, provided as a tar-gzipped file'},
        {'Name': 'JSON: mmCIF content', 'Description': 'System generated JSON file with mmCIF content'}
    ]

    pb = catalog.getPathBuilder()
    schema = pb.Vocab
    System_Generated_File_Type = schema.System_Generated_File_Type
    System_Generated_File_Type.insert(rows, defaults=['ID', 'URI'])

def table_comments(model):
    # Update table comment for Entry_Generated_File
    model.table("PDB", "Entry_Generated_File").comment = "System generated files for the entry"

# ============================================================
def main(server_name, catalog_id, credentials):
    server = DerivaServer('https', server_name, credentials)
    catalog = server.connect_ermrest(catalog_id)
    catalog.dcctx['cid'] = 'oneoff/model'
    model = catalog.getCatalogModel()

    if False:
        utils.drop_table(catalog, 'Vocab', 'System_Generated_Entry_File_Type') #Only on dev
        utils.drop_column_if_exist(model, 'PDB', 'Entry_Generated_File', 'File_Type') #Only on dev
    if True:
        # Rename Validation_File_Type
        utils.rename_table_if_exists(model, 'Vocab', 'Validation_File_Type', 'System_Generated_File_Type')
        # Rename fkeys to System_Generated_File_Type
        utils.rename_fkey_if_exist(model, 'PDB', 'Entry_Error_File', 'Entry_Error_File_File_Type_fkey', 'Entry_Error_File_System_Generated_File_Type_fkey')
        # Rename fkeys from System_Generated_File_Type
        utils.rename_fkey_if_exist(model,'Vocab', 'System_Generated_File_Type', 'Validation_File_Type_RCB_fkey', 'System_Generated_File_Type_RCB_fkey')
        utils.rename_fkey_if_exist(model,'Vocab', 'System_Generated_File_Type', 'Validation_File_Type_RMB_fkey', 'System_Generated_File_Type_RMB_fkey')
        utils.rename_fkey_if_exist(model,'Vocab', 'System_Generated_File_Type', 'Validation_File_Type_Owner_fkey', 'System_Generated_File_Type_Owner_fkey')
        # Rename keys for System_Generated_File_Type
        utils.rename_key_if_exist(model, 'Vocab', 'System_Generated_File_Type', 'Validation_File_Type_ID_key', 'System_Generated_File_Type_ID_key')
        utils.rename_key_if_exist(model, 'Vocab', 'System_Generated_File_Type', 'Validation_File_Type_RID_key', 'System_Generated_File_Type_RID_key')
        utils.rename_key_if_exist(model, 'Vocab', 'System_Generated_File_Type', 'Validation_File_Type_URI_key', 'System_Generated_File_Type_URI_key')
        utils.rename_key_if_exist(model, 'Vocab', 'System_Generated_File_Type', 'Validation_File_Type_Name_key', 'System_Generated_File_Type_Name_key')
        # Rename Entry_mmCIF_File
        utils.rename_table_if_exists(model, 'PDB', 'Entry_mmCIF_File', 'Entry_Generated_File')
        # Rename fkeys to Entry_Generated_File
        utils.rename_fkey_if_exist(model, 'PDB', 'Conform_Dictionary', 'Conform_Dictionary_Entry_mmCIF_File_fkey', 'Conform_Dictionary_Entry_Generated_File_fkey')
        #Rename fkeys from Entry_Generated_File
        utils.rename_fkey_if_exist(model, 'PDB', 'Entry_Generated_File', 'Entry_mmCIF_File_Owner_fkey', 'Entry_Generated_File_Owner_fkey')
        utils.rename_fkey_if_exist(model, 'PDB', 'Entry_Generated_File', 'Entry_mmCIF_File_Structure_Id_fkey', 'Entry_Generated_File_Structure_Id_fkey')
        # Rename keys for Entry_Generated_File
        utils.rename_key_if_exist(model, 'PDB', 'Entry_Generated_File', 'Entry_mmCIF_File_RID_key', 'Entry_Generated_File_RID_key')
        utils.rename_key_if_exist(model, 'PDB', 'Entry_Generated_File', 'Entry_mmCIF_File_Structure_Id_mmCIF_Schema_Version_key', 'Entry_Generated_File_Structure_Id_mmCIF_Schema_Version_key')
        # Replace key ['Structure_Id', 'mmCIF_Schema_Version'] by ['Structure_Id', 'File_Type'] for Entry_Generated_File
        utils.drop_key_if_exist(model, 'PDB', 'Entry_Generated_File', 'Entry_Generated_File_Structure_Id_mmCIF_Schema_Version_key')
        utils.create_key_if_not_exists(model, 'PDB', 'Entry_Generated_File', ['Structure_Id', 'File_Type'], 'Entry_Generated_File_Structure_Id_File_Type_key')

    """
    Add rows to Vocab table
    """
    if True:
        add_rows_to_Vocab_Table_System_Generated_File_Type(catalog)
    
    """
    Update existing PDB table
    """
    if True:
        update_PDB_Entry_Generated_File(model)

    """
    Update existing PDB table comment
    """

    if True:
        table_comments(model)
        model.apply()
    
# ===================================================    

if __name__ == '__main__':
    args = BaseCLI('ad-hoc table creation tool', None, 1).parse_cli()
    credentials = get_credential(args.host, args.credential_file)

    main(args.host, 99, credentials)
    
