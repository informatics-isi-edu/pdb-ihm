import sys
import json
from deriva.core import ErmrestCatalog, AttrDict, get_credential, DEFAULT_CREDENTIAL_FILE, tag, urlquote, DerivaServer, BaseCLI
from deriva.core.ermrest_model import builtin_types, Schema, Table, Column, Key, ForeignKey, DomainType, ArrayType
import utils

# ========================================================

def update_PDB_entity_src_gen(model):
    utils.create_column_if_not_exist(model, 'PDB', 'entity_src_gen',
                                     Column.define(
                                        'host_org_common_name',
                                        builtin_types.text,
                                        comment='The common name of the organism that served as host for the production of the entity',
                                        nullok=True
                                    ))
    utils.create_column_if_not_exist(model, 'PDB', 'entity_src_gen',
                                     Column.define(
                                        'pdbx_gene_src_ncbi_taxonomy_id',
                                        builtin_types.text,
                                        comment='NCBI Taxonomy identifier for the gene source organism',
                                        nullok=True
                                    ))
    utils.create_column_if_not_exist(model, 'PDB', 'entity_src_gen',
                                     Column.define(
                                        'pdbx_host_org_ncbi_taxonomy_id',
                                        builtin_types.text,
                                        comment='NCBI Taxonomy identifier for the expression system organism',
                                        nullok=True
                                    ))
    utils.create_column_if_not_exist(model, 'PDB', 'entity_src_gen',
                                     Column.define(
                                        'pdbx_host_org_scientific_name',
                                        builtin_types.text,
                                        comment='The scientific name of the organism that served as host for the production of the entity',
                                        nullok=True
                                    ))
    utils.create_column_if_not_exist(model, 'PDB', 'entity_src_gen',
                                     Column.define(
                                        'pdbx_host_org_strain',
                                        builtin_types.text,
                                        comment='The strain of the organism in which the entity was expressed',
                                        nullok=True
                                    ))

def main(server_name, catalog_id, credentials):
    server = DerivaServer('https', server_name, credentials)
    catalog = server.connect_ermrest(catalog_id)
    catalog.dcctx['cid'] = "oneoff/model"
    model = catalog.getCatalogModel()

    if True:
        """
        Rename column in existing table
        """
        utils.rename_column_if_exists(model, 'PDB', 'ihm_ensemble_sub_sample', 'sample_name', 'name')

        """
        Update existing tables
        """
        update_PDB_entity_src_gen(model)

if __name__ == '__main__':
    args = BaseCLI("ad-hoc table creation tool", None, 1).parse_cli()
    credentials = get_credential(args.host, args.credential_file)

    main(args.host, 99, credentials)
    
