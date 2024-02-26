from deriva.core import DerivaServer, get_credential, BaseCLI
from deriva.core.ermrest_model import Table, Column, Key, ForeignKey, builtin_types

#def table_comments(model):
    #table = model.table("PDB", "software")
    #table.comment = "List of software used in the modeling"
    #table.column_definitions["Species_Tested_In"].comment = None

    #model.table("PDB", "struct").comment = "Details about the structural models submitted; mmCIF category: struct"

def column_comments(model):

    model.table("PDB", "entry").column_definitions["Image_File_URL"].comment = "Uploaded image file. Image provided will be used for displaying the entry on the PDB-Dev website"
    model.table("PDB", "entry").column_definitions["mmCIF_File_URL"].comment = "Uploaded mmCIF file. Use MAXIT or python-ihm to convert PDB to mmCIF. Using other tools may not provide compliant files"
    model.table("PDB", "ihm_starting_model_details").column_definitions["mmCIF_File_URL"].comment = "Uploaded starting model mmCIF file. The chain identifiers and residue numbers in the mmCIF file should match the data provided in this table. PDB file format can be converted to mmCIF using the MAXIT software."

# ===================================================
# -- this function will be called from the update_schemas.py file

def set_comments(model):
    #table_comments(model)
    column_comments(model)


# ===================================================    
def main(server_name, catalog_id, credentials):
    server = DerivaServer('https', server_name, credentials)
    catalog = server.connect_ermrest(catalog_id)
    catalog.dcctx['cid'] = "oneoff/model"
    model = catalog.getCatalogModel()

    set_comments(model)

    # let's the library deals with applying the difference
    model.apply()

# ===================================================    

if __name__ == '__main__':
    args = BaseCLI("ad-hoc table creation tool", None, 1).parse_cli()
    credentials = get_credential(args.host, args.credential_file)
#    if args.catalog is None:
#        catalog_id = 99

    main(args.host, 99, credentials)
