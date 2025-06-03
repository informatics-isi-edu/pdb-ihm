from deriva.core import DerivaServer, get_credential, BaseCLI
from deriva.core.ermrest_model import Table, Column, Key, ForeignKey, builtin_types
import sys
from model_archive.utils.shared import DCCTX, PDBDev_CLI

# -- import per-schema comments
import Vocab
import PDB


# =========================================================
def table_comments(model):
    schema = model.schemas["MA"]
    for sname, schema in model.schemas.items():
        for tname,table in schema.tables.items():
            if table.comment:
                print("%s:%s: %s" % (sname, tname, table.comment))

                
def print_comment_py(model):
    schema = model.schemas["MA"]
    for sname, schema in model.schemas.items():
        print("# ------------------------------------------------------------------------")
        print("def %s_comments(model):" % (sname))
        print('    schema = model.schemas["%s"]' % (sname))
        for tname,table in schema.tables.items():
            print("\n    #------------" % ())            
            if table.comment:
              print('    schema.tables["%s"].comment = ' % (tname) + '%r' % (table.comment))
            for column in table.columns:
                if column.comment:
                    print('    schema.tables["%s"].columns["%s"].comment = ' % (tname, column.name) + '%r' % (column.comment))
        print("\n\n")

def main(server_name, catalog_id, credentials):
    server = DerivaServer('https', server_name, credentials)
    catalog = server.connect_ermrest(catalog_id)
    catalog.dcctx['cid'] = "comment"
    model = catalog.getCatalogModel()

    Vocab.set_comments(model)
    PDB.set_comments(model)
    
    # let's the library deals with applying the difference
    model.apply()



if __name__ == '__main__':
    args = PDBDev_CLI("pdbdev", None, 1).parse_cli()
    credentials = get_credential(args.host, args.credential_file)

    main(args.host, catalog_id, credentials)
    
