import sys
import json
from deriva.core import get_credential, DerivaServer, BaseCLI
from deriva.core.ermrest_model import Key

# add scripts for updating vocabs that has nothing to do with mmcif model changes.


def main(server_name, catalog_id, credentials):
    server = DerivaServer('https', server_name, credentials)
    catalog = server.connect_ermrest(catalog_id)
    catalog.dcctx['cid'] = "oneoff/model"


if __name__ == '__main__':
    args = BaseCLI("ad-hoc table creation tool", None, 1).parse_cli()
    credentials = get_credential(args.host, args.credential_file)

    main(args.host, 99, credentials)
    
