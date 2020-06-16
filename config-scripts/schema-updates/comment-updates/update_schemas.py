from deriva.core import DerivaServer, get_credential, BaseCLI
from deriva.core.ermrest_model import Table, Column, Key, ForeignKey, builtin_types
import sys

# -- import per-schema comments
import vocab
import pdb


def main(server_name, catalog_id, credentials):
    server = DerivaServer('https', server_name, credentials)
    catalog = server.connect_ermrest(catalog_id)
    catalog.dcctx['cid'] = "oneoff/model"
    model = catalog.getCatalogModel()

    vocab.set_comments(model)
    pdb.set_comments(model)
    
    # let's the library deals with applying the difference
    model.apply()



if __name__ == '__main__':
    args = BaseCLI("ad-hoc table creation tool", None, 1).parse_cli()
    credentials = get_credential(args.host, args.credential_file)
    if args.catalog is None:
        catalog_id = 99

    main(args.host, catalog_id, credentials)
    
