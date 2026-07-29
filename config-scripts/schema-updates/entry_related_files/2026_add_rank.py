import sys
import json

from deriva.core import ErmrestCatalog, AttrDict, get_credential, DEFAULT_CREDENTIAL_FILE, tag, urlquote, DerivaServer, get_credential, BaseCLI
from deriva.core.ermrest_model import builtin_types, Schema, Table, Column, Key, ForeignKey, DomainType, ArrayType

from deriva.utils.extras.data import get_ermrest_query, update_table_rows
from pdb_dev.utils.shared import PDBDEV_CLI, DCCTX

def update_file_type(model):
    catalog = model.catalog
    sname = "Vocab"
    tname = "File_Type"
    table = model.schemas[sname].tables[tname]
    if "Rank" not in table.columns.elements:
        print(f"- update_file_type: create column {tname}.Rank")
        table.create_column(
            Column.define(
                'Rank',
                builtin_types.text,
                nullok=True,
            ),
        )

    
        """ to add in payload after editing
        """
        
    payload = [
        { "Name": "Chemical Crosslinks from Experiments", "Rank":"01" },
        { "Name": "Chemical Crosslinking Restraints Applied in the Modeling", "Rank":"02" },
     ]
    
    if False: payload.extend([
        { "Name": "Chemical Crosslink Restraint Results", "Rank":"03" },
        { "Name": "Chemical Crosslink Restraint Result Parameters", "Rank":"04" },
        { "Name": "Predicted Contact Restraints", "Rank":"05" },
        { "Name": "Hydroxyl Radical Footprinting Restraints", "Rank":"06" },
        { "Name": "Molecular Features used in Generic Restraints", "Rank":"07" },
        { "Name": "Molecular Features Comprising of Pseudo Sites", "Rank":"08" },
        { "Name": "Molecular Features Comprising of Polymeric Atoms", "Rank":"09" },
        { "Name": "Molecular Features Comprising of Polymeric Residues", "Rank":"10" },
        { "Name": "Molecular Features Comprising of Non-polymeric Entities", "Rank":"11" },
        { "Name": "Molecular Features Comprising of Polymeric Residues at Interfaces", "Rank":"12" },
        { "Name": "Generic Distance Restraints Between Molecular Features", "Rank":"13" },
        { "Name": "Probes Attached to Residues in Polymeric Entities", "Rank":"14" },
        { "Name": "Distance Restraints between Geometric Objects and Molecular Features", "Rank":"15" },
        { "Name": "Residue Positions in Polymeric Entities where Probes are Attached", "Rank":"16" },
        { "Name": "Non-polymeric Entities used as Probes", "Rank":"17" },
        { "Name": "Chemical Crosslinks with Pseudo Sites", "Rank":"18" },
        { "Name": "HD Exchange Restraints", "Rank":"19" },
        { "Name": "Pseudo Site Coordinates", "Rank":"20" },
        { "Name": "Angle Restraints Between Molecular Features", "Rank":"21" },
        { "Name": "Dihedral Restraints Between Molecular Features", "Rank":"22" },
    ])
    
    rows = get_ermrest_query(catalog, sname, tname)
    name2rows = { row["Name"]: row for row in rows }
    updating = []
    for row in payload:
        ref = name2rows[row["Name"]]
        if ref["Rank"] != row["Rank"]:
            updating.append(row)
    updated = update_table_rows(catalog, sname, tname, payload=payload, keys=["Name"], column_names=["Rank"])
    print("- update_file_type: updated [%d]: %s" % (len(updated), json.dumps(updated[0:2], indent=4)))

def fix_fkey_constraints(model):
    sname = "PDB"
    schema = model.schemas[sname]
    
    tname = "ihm_cross_link_restraint"
    table = schema.tables[tname]
    
    fkey_ctname = "ihm_cross_link_restraint_group_id_fkey"
    if (schema, fkey_ctname) in table.foreign_keys.elements:
        fkey = table.foreign_keys[(schema, fkey_ctname)]
        if fkey.on_delete not in ["NO ACTION"]:
            print(f"Altering fkey: {fkey_ctname}")
            fkey.alter(on_delete="NO ACTION")

# ============================================================
def main(server_name, catalog_id, credentials):
    server = DerivaServer('https', server_name, credentials)
    catalog = server.connect_ermrest(catalog_id)
    catalog.dcctx['cid'] = DCCTX["model"]
    model = catalog.getCatalogModel()

    fix_fkey_constraints(model)
    
    #update_file_type(model)

        
# ===================================================    

if __name__ == '__main__':
    args = PDBDEV_CLI('ad-hoc table creation tool', None, 1).parse_cli()
    credentials = get_credential(args.host, args.credential_file)

    main(args.host, args.catalog_id, credentials)
