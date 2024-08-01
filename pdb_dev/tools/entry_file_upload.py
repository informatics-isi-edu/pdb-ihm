#!/usr/bin/python3

import argparse
import json
import sys
import os
from deriva.core import ErmrestCatalog, HatracStore, AttrDict, get_credential, DEFAULT_CREDENTIAL_FILE, tag, urlquote, DerivaServer, get_credential, BaseCLI
from deriva.core.ermrest_model import builtin_types, Schema, Table, Column, Key, ForeignKey, tag, AttrDict
from deriva.core import urlquote, urlunquote
from deriva.core.utils.hash_utils import compute_hashes

from pdb_dev.utils.shared import PDBDEV_CLI, DCCTX
from atlas_d2k.utils.data import get_entities, insert_if_not_exist, update_table_rows, delete_table_rows

'''
    mmcif/<entry_id>.cif
    validation_reports/<entry_id>/<entry_id>_full_validation.pdf
    validation_reports/<entry_id>/<entry_id>_summary_validation.pdf
    validation_reports/<entry_id>/<entry_id>_html.tar.gz
    json/<entry_id>.json
'''
#os.chdir(dir)

upload_path = "/tmp/pdb/remediation_upload"

def get_file_type(file_name, entry_code):
    if file_name == "%s.cif" % (entry_code):
        file_type = "mmCIF"
    elif file_name == "%s.json" % (entry_code):
        file_type = "JSON: mmCIF content"
    elif file_name == "%s_full_validation.pdf" % (entry_code):
        file_type = "Validation: Full PDF"
    elif file_name == "%s_summary_validation.pdf" % (entry_code):
        file_type = "Validation: Summary PDF"                    
    elif file_name == "%s_html.tar.gz" % (entry_code):
        file_type = "Validation: HTML tar.gz"                                        
    else:
        file_type = "UNKNOWN"
        raise "ERROR: %s is non supported file name" % (file_name)
    return file_type
    
def get_file_type_dir_name(file_type): 
    file_type_dir_names = {
        "mmCIF" : "final_mmCIF",
        "JSON: mmCIF content": "final_mmCIF",
        "Validation: Full PDF": "validation_report",
        "Validation: Summary PDF": "validation_report",
        "Validation: HTML tar.gz": "validation_report",
    }
    if file_type not in file_type_dir_names.keys():
        raise "ERROR: non supported file type"
    else:
        return file_type_dir_names[file_type]

# Update entry table
# Workflow_Status = REL
# Manual_Processing = True
#
# Conform_Dictionary: mmCIF,
# https://data.pdb-dev.org/chaise/recordset/#1/PDB:Conform_Dictionary@sort(RID)
#
#mmcif_ihm_ext.dic (v 1.26)
# mmcif_pdbx.dic (v 5.395)
def main(catalog, store):
    global upload_path
    print("current cwd: %s" % (os.getcwd()))
    print("upload dir: %s" % (upload_path))

    # -- get accession code to entry information
    code2entries = {}
    id2entries = {}
    rows = catalog.get("/attribute/M:=PDB:entry/A:=PDB:Accession_Code/$M/RID,id,RCB,A:PDB_Accession_Code,Workflow_Status,Manual_Processing?limit=1000").json()
    #print(json.dumps(rows, indent=4))
    for row in rows:
        row["uid"] = row["RCB"].replace("https://auth.globus.org/", "")
        code2entries[row["PDB_Accession_Code"]] = row
        id2entries[row["id"]] = row
    #print(json.dumps(code2rcb, indent=4))

    # -- get existing system generated files
    existing_file2rows = {}
    rows = catalog.get("/entity/M:=PDB:entry/F:=PDB:Entry_Generated_File?limit=5000").json()
    for row in rows:
        existing_file2rows[(row["Structure_Id"], row["File_Type"])] = row
        
    # -- lookup data dictionary
    mmcif_ihm_rid = None
    mmcif_pdbx_rid = None
    rows = catalog.get("/entity/M:=PDB:Data_Dictionary").json()
    for row in rows:
        if row["Name"] == "mmcif_ihm_ext.dic" and row["Version"] == "1.26":
            mmcif_ihm_rid = row["RID"]
        elif row["Name"] == "mmcif_pdbx.dic" and row["Version"] == "5.395":
            mmcif_pdbx_rid = row["RID"]
    print("mmcif_ihm_rid: %s, mmcif_pdbx_rid: %s" % (mmcif_ihm_rid, mmcif_pdbx_rid))

    # == read directory
    insert_files = []
    update_files = []
    dir_entry_codes = []
    dir_entry_ids = []
    for entry_code in os.listdir(upload_path):
        # look for entry metadata
        entry_path = "%s/%s" % (upload_path, entry_code)
        print("entry = %s, structure_id:%s" % (entry_code, code2entries[entry_code]["id"]))
        if entry_code not in code2entries.keys():
            print("ERROR: entry_code %s is not in the entry table" % (entry_code))
            continue
        structure_id = code2entries[entry_code]["id"]
        dir_entry_codes.append(entry_code)        
        dir_entry_ids.append(structure_id)
        if os.path.isfile(entry_path): continue
        # iternate ver file in the directory
        for file_name in os.listdir(entry_path):
            file_path = "%s/%s" % (entry_path, file_name)
            hatrac_entry_path = "/hatrac/pdb/generated/uid/%s/entry/id/%s" % (code2entries[entry_code]["uid"], structure_id)
            print("  file_name: %s, file_path: %s" % (file_name, file_path))
            if not os.path.isfile(file_path): continue
            f = open(file_path, "rb")
            (md5_hex, md5_base64) = compute_hashes(f)["md5"]
            f.close()
            file_bytes = os.stat(file_path).st_size
            file_type = get_file_type(file_name, entry_code)
            upload_file_url = "%s/%s/%s" % (hatrac_entry_path, get_file_type_dir_name(file_type), file_name)
            hatrac_url = store.put_obj(upload_file_url, file_path, md5=md5_base64, content_disposition="filename*=UTF-8''%s" % (file_name))
            #print("    hashes: %s, %s, %d" % (md5_hex, md5_base64, file_bytes))
            #print("    file_type: %s" % (file_type))
            #print("    upload_file_url: %s, hatrac_url:%s " % (upload_file_url, hatrac_url))
            row = {
                "File_URL" : hatrac_url,
                "File_Name" : file_name,
                "File_MD5" : md5_hex,
                "File_Bytes" : file_bytes,
                "Structure_Id" : structure_id,
                "mmCIF_Schema_Version": "1.26" if file_type == "mmCIF" else  None,
                "File_Type" : file_type,
                "Entry_RCB" : code2entries[entry_code]["RCB"]
            }
            if (structure_id, file_type) not in existing_file2rows.keys():
                insert_files.append(row)                
            else:
                row["RID"] = existing_file2rows[(structure_id, file_type)]["RID"]
                # check for changes before update
                if hatrac_url != existing_file2rows[(structure_id, file_type)]["File_URL"]:
                    update_files.append(row)
            #print(json.dumps(row, indent=4))

    inserted_files = []
    updated_files = []
    print("\ninsert_files(%d): %s" % (len(insert_files), json.dumps(insert_files, indent=4)))
    print("\nupdate_files(%d): %s" % (len(update_files), json.dumps(update_files, indent=4)))
    inserted_files = insert_if_not_exist(catalog, "PDB", "Entry_Generated_File", insert_files)
    updated_files = update_table_rows(catalog, "PDB", "Entry_Generated_File", key="RID", payload=update_files)
    for row in inserted_files:
        existing_file2rows[(row["Structure_Id"], row["File_Type"])] = row

    # == update conform_dict. Can only do the update after Entry_Generated_File are updated
    '''
    select * from "PDB"."Entry_Generated_File" WHERE "Structure_Id" in ('PDBDEV_00000001', 'PDBDEV_00000002', 'D_3-7B7T');
    select cd."RID" as crid, f."Structure_Id", f."File_Type", d."Name", d."Version", d."RID" as drid from "PDB"."Conform_Dictionary" cd
      JOIN "PDB"."Entry_Generated_File" f ON (cd."Exported_mmCIF_RID" = f."RID")
      JOIN "PDB"."Data_Dictionary" d ON (cd."Data_Dictionary_RID" = d."RID")
    WHERE "Structure_Id" in ('PDBDEV_00000001', 'PDBDEV_00000002', 'D_3-7B7T');
    '''

    # -- existing conform_dicts
    existing_conform_dicts = {}
    rows = catalog.get("/attribute/M:=PDB:Conform_Dictionary/F:=(Exported_mmCIF_RID)=(PDB:Entry_Generated_File:RID)/Structure_Id=ANY(PDBDEV_00000001,PDBDEV_00000002,PDBDEV_00000003,PDBDEV_00000004,PDBDEV_00000380,D_3-7B7T)/D:=(M:Data_Dictionary_RID)=(PDB:Data_Dictionary:RID)/$M/CRID:=RID,Exported_mmCIF_RID,Data_Dictionary_RID,F:Structure_Id,Dict_Name:=D:Name,D:Category,D:Version?limit=10").json()
    for row in rows:
        existing_conform_dicts[(row["Structure_Id"], row["Dict_Name"])] = row
        #print("(%s, %s) => %s" % (row["Structure_Id"], row["Dict_Name"], row["Version"]))

    #print("existing_conform_dicts(%d): existing_conform_dicts.keys(): %s" % (len(existing_conform_dicts), existing_conform_dicts.keys()))

    insert_conform_dicts=[]
    update_conform_dicts=[]
    conform_dict_delete_rid=[]
    #for row in inserted_files + updated_files:
    for structure_id in dir_entry_ids:
        file_type = "mmCIF"
        if not "RID" in existing_file2rows[(structure_id, file_type)].keys():
            print("ERROR: RID doesn't exist: %s" % (row))
            continue
        file_rid = existing_file2rows[(structure_id, file_type)]["RID"]
        # -- ihm dict
        if (structure_id, "mmcif_ihm_ext.dic") not in existing_conform_dicts.keys():
            #print("(%s, %s) doesn't exist. Will insert" % (structure_id, "mmcif_ihm_ext.dic"))
            insert_conform_dicts.append({"Exported_mmCIF_RID": file_rid, "Data_Dictionary_RID": mmcif_ihm_rid })
        elif existing_conform_dicts[(structure_id, "mmcif_ihm_ext.dic")]["Version"] != "1.26":
            update_conform_dicts.append({"Exported_mmCIF_RID": file_rid, "Data_Dictionary_RID": mmcif_ihm_rid, "RID": existing_conform_dicts[(structure_id, "mmcif_ihm_ext.dic")]["CRID"] })
        # -- pdbx dict
        if (structure_id, "mmcif_pdbx.dic") not in existing_conform_dicts.keys():
            insert_conform_dicts.append({"Exported_mmCIF_RID": file_rid, "Data_Dictionary_RID": mmcif_pdbx_rid }),
        elif existing_conform_dicts[(structure_id, "mmcif_pdbx.dic")]["Version"] != "5.395":
            update_conform_dicts.append({"Exported_mmCIF_RID": file_rid, "Data_Dictionary_RID": mmcif_pdbx_rid, "RID": existing_conform_dicts[(structure_id, "mmcif_pdbx.dic")]["CRID"] })
            
    #print("\ninsert_conform_dicts(%d): %s" % (len(insert_conform_dicts), json.dumps(insert_conform_dicts, indent=4)))
    #print("\nupdate_conform_dicts(%d): %s" % (len(update_conform_dicts), json.dumps(update_conform_dicts, indent=4)))
    inserted_conform_dicts = insert_if_not_exist(catalog, "PDB", "Conform_Dictionary", insert_conform_dicts)
    updated_conform_dicts = update_table_rows(catalog, "PDB", "Conform_Dictionary", key="RID", payload=update_conform_dicts)
    print("\nconform_dicts_inserted(%d/%d): %s" % (len(inserted_conform_dicts), len(insert_conform_dicts), json.dumps(inserted_conform_dicts, indent=4)))
    print("\nconform_dicts_updated(%d/%d): %s" % (len(updated_conform_dicts), len(update_conform_dicts), json.dumps(updated_conform_dicts, indent=4)))    

    delete_conform_dict_rids=[]
    for (structure_id, dict_name), row in existing_conform_dicts.items():
        #print(" d: %s %s %s " % (structure_id, dict_name, row))
        if structure_id not in dir_entry_ids: continue
        if dict_name not in ["mmcif_ihm_ext.dic", "mmcif_pdbx.dic"]:
            delete_conform_dict_rids.append(row["CRID"])
    print("\ndelete_conform_dict_rids(%d): %s" % (len(delete_conform_dict_rids), json.dumps(delete_conform_dict_rids, indent=4)))
    if delete_conform_dict_rids:
        constraints = "/RID=ANY(%s)" % (','.join(delete_conform_dict_rids))
        deleted = delete_table_rows(catalog, "PDB", "Conform_Dictionary", constraints=constraints)
        #print("delete constraint: %s" % (constraints))
        print(deleted)
    
    # == update entry table
    '''
    Set entry.Process_Status == Success
    Update entry.id to D_+<entry.RID> if it is something else
    '''
    
    update_entries = []
    for id in dir_entry_ids: 
        entry_row = id2entries[id]
        if entry_row["Workflow_Status"] != "REL" or entry_row["Manual_Processing"] is False :
            update_entries.append({"id": entry_row["id"], "Workflow_Status": "REL", "Manual_Processing": True})
    print("\nupdate_entries (%d/%d): %s" % (len(update_entries), len(dir_entry_ids), json.dumps(update_entries, indent=4)))
    update_table_rows(catalog, "PDB", "entry", key="id", column_names=["Workflow_Status", "Manual_Processing"], payload=update_entries)

    
## Run the Script
if __name__ == "__main__":
    cli = PDBDEV_CLI("pdbdev", None, 1)
    cli.parser.add_argument('--upload-dir', help="directory containing entry generated files", default="/tmp/pdb/remediation_upload")
    
    args = cli.parse_cli()
    upload_dir = args.upload_dir
    credentials = get_credential(args.host, args.credential_file)
    catalog = ErmrestCatalog("https", args.host, args.catalog_id, credentials)
    catalog.dcctx['cid'] = DCCTX["cli/remedy"]
    store = HatracStore("https", args.host, credentials)
    main(catalog, store)

            
        
    

