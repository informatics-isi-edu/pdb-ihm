import sys
import json
from deriva.core import ErmrestCatalog, AttrDict, get_credential, DEFAULT_CREDENTIAL_FILE, tag, urlquote, DerivaServer, get_credential, BaseCLI
from deriva.core.ermrest_model import builtin_types, Schema, Table, Column, Key, ForeignKey, DomainType, ArrayType
from pdb_dev.utils.shared import PDBDEV_CLI, DCCTX


# ============================================================
def main(server_name, catalog_id, credentials):
    server = DerivaServer('https', server_name, credentials)
    catalog = server.connect_ermrest(catalog_id)
    catalog.dcctx['cid'] = DCCTX["model"]
    model = catalog.getCatalogModel()

    """
    model.schemas["PDB"].tables["PDB_Archive"].create_column(
        Column.define(
            'Unreleased_Entries',
            builtin_types.int4,
            nullok=True,
            comment="Number of unreleased entries (HOLD status) listed in the Unreleaed_Entries manifest."
        ),
    )
    model.schemas["PDB"].tables["PDB_Archive"].create_column(    
        Column.define(
            'Unreleased_Entries_Unzip_MD5',
            builtin_types.text,
            nullok=True,
            comment="MD5 of uncompressed Unreleased_Entries.json"
        )
    )
    """
    
    model.schemas["PDB"].tables["PDB_Archive"].columns["Current_File_Holdings_URL"].alter(default=None)
    model.schemas["PDB"].tables["PDB_Archive"].columns["Current_File_Holdings_MD5"].alter(default=None)
    model.schemas["PDB"].tables["PDB_Archive"].columns["Released_Structures_LMD_URL"].alter(default=None)
    model.schemas["PDB"].tables["PDB_Archive"].columns["Released_Structures_LMD_MD5"].alter(default=None)
    model.schemas["PDB"].tables["PDB_Archive"].columns["Unreleased_Entries_URL"].alter(default=None)
    model.schemas["PDB"].tables["PDB_Archive"].columns["Unreleased_Entries_MD5"].alter(default=None)
    
# ===================================================    

if __name__ == '__main__':
    args = PDBDEV_CLI('ad-hoc table creation tool', None, 1).parse_cli()
    credentials = get_credential(args.host, args.credential_file)

    main(args.host, args.catalog_id, credentials)




    
