#!/usr/bin/python

import sys
import json
from deriva.core import ErmrestCatalog, AttrDict, get_credential, DEFAULT_CREDENTIAL_FILE, tag, urlquote, DerivaServer, get_credential, BaseCLI
from deriva.core.ermrest_model import builtin_types, Schema, Table, Column, Key, ForeignKey

from pdb_dev.utils.shared import PDBDEV_CLI, DCCTX

""" From Brinda (02/05/2025)
Two column names are wrong in ermrest:
  - ihm_derived_dihedral_restraint: dihedral_threshold_mean_esd -> dihedral_threshold_esd
  - ihm_derived_angle_restraint: angle_threshold_mean_esd -> angle_threshold_esd  

"""
def update_incorrect_columns(model):
    table = model.schemas["PDB"].tables["ihm_derived_dihedral_restraint"]
    if "dihedral_threshold_mean_esd" in table.columns.elements:
        table.columns["dihedral_threshold_mean_esd"].alter(name="dihedral_threshold_esd")

    table = model.schemas["PDB"].tables["ihm_derived_angle_restraint"]
    if "angle_threshold_mean_esd" in table.columns.elements:
        table.columns["angle_threshold_mean_esd"].alter(name="angle_threshold_esd")

# -- =================================================================================        
    
def main(server_name, catalog_id, credentials):
    server = DerivaServer('https', server_name, credentials)
    catalog = server.connect_ermrest(catalog_id)
    catalog.dcctx['cid'] = DCCTX["model"]
    model = catalog.getCatalogModel()

    update_incorrect_columns(model)

    
# -- =================================================================================        
if __name__ == '__main__':
    args = PDBDEV_CLI("pdb_dev", None, 1).parse_cli()
    credentials = get_credential(args.host, args.credential_file)
    main(args.host, args.catalog_id, credentials)
