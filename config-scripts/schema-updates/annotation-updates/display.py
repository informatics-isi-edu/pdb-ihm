from deriva.core import DerivaServer, get_credential, BaseCLI
from deriva.core.ermrest_model import Table, Column, Key, ForeignKey, builtin_types

def table_annotations(model):
    #table = model.table("PDB", "software")
    #table.comment = "List of software used in the modeling"
    #table.column_definitions["Species_Tested_In"].comment = None

    model.table("PDB", "Entry_mmCIF_File").annotations.update({"tag:misd.isi.edu,2015:display": {"name": "Entry mmCIF File"}})
    

def column_annotations(model):
    
    model.table("PDB", "Entry_mmCIF_File").column_definitions["mmCIF_Schema_Version"].annotations.update({"tag:misd.isi.edu,2015:display": {"name": "mmCIF Schema Version"}})

# ===================================================
# -- this function will be called from the update_schemas.py file

def set_annotations(model):
    table_annotations(model)
    column_annotations(model)


# ===================================================    
def main(server_name, catalog_id, credentials):
    server = DerivaServer('https', server_name, credentials)
    catalog = server.connect_ermrest(catalog_id)
    catalog.dcctx['cid'] = "oneoff/model"
    model = catalog.getCatalogModel()

    set_annotations(model)

    # let's the library deals with applying the difference
    model.apply()

# ===================================================    

if __name__ == '__main__':
    args = BaseCLI("ad-hoc table creation tool", None, 1).parse_cli()
    credentials = get_credential(args.host, args.credential_file)
#    if args.catalog is None:
#        catalog_id = 99

    main(args.host, 99, credentials)
    
    
