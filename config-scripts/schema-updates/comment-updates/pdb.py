from deriva.core import DerivaServer, get_credential, BaseCLI
from deriva.core.ermrest_model import Table, Column, Key, ForeignKey, builtin_types

def software(model):
    table = model.table("PDB", "software")
    
    table.comment = "List of software used in the modeling"
    
    #table.columns["Species_Tested_In"].comment = None


# ===================================================
# -- this function will be called from the update_schemas.py file

def set_comments(model):
    software(model)


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
    if args.catalog is None:
        catalog_id = 99

    main(args.host, catalog_id, credentials)
    
    
