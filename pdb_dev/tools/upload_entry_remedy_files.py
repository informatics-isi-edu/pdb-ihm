#!/usr/bin/python3

import argparse
import json
import sys
import os
from deriva.core import ErmrestCatalog, HatracStore, AttrDict, get_credential, DEFAULT_CREDENTIAL_FILE, tag, urlquote, DerivaServer, get_credential, BaseCLI
from deriva.core.ermrest_model import builtin_types, Schema, Table, Column, Key, ForeignKey, tag, AttrDict
from deriva.core import urlquote, urlunquote, DEFAULT_SESSION_CONFIG
from deriva.core.utils.hash_utils import compute_hashes

from ..utils.shared import PDBDEV_CLI, DCCTX, cfg
#from pdb_dev.utils.shared import PDBDEV_CLI, DCCTX, cfg
from deriva.utils.extras.data import get_ermrest_query, insert_if_not_exist, update_table_rows, delete_table_rows
from deriva.utils.extras.hatrac import HatracFile


'''
    -- destination remedy files per entries???
    mmcif/<entry_id>.cif
    validation_reports/<entry_id>/<entry_id>_full_validation.pdf
    validation_reports/<entry_id>/<entry_id>_summary_validation.pdf
    validation_reports/<entry_id>/<entry_id>_html.tar.gz
    json/<entry_id>.json


    select * from "PDB"."Entry_Generated_File" WHERE "Structure_Id" in ('PDBDEV_00000001', 'PDBDEV_00000002', 'D_3-7BTT', 'D_3-7B7T');

    -- get existing conform dicts
    select cd."RID" as crid, e."Accession_Code", f."Structure_Id", f."File_Type", d."Name", d."Version", d."RID" as drid, cd."RMT"
    from "PDB"."Conform_Dictionary" cd
      JOIN "PDB"."Entry_Generated_File" f ON (cd."Exported_mmCIF_RID" = f."RID")
      JOIN "PDB".entry e ON (f."Structure_Id" = e.id)
      JOIN "PDB"."Accession_Code" ac ON (e."Accession_Code" = ac."Accession_Code")
      JOIN "PDB"."Data_Dictionary" d ON (cd."Data_Dictionary_RID" = d."RID")
    -- WHERE "RMT" > '20240801'
    WHERE "Accession_Code" in ('9A83', '9A86', '8ZZ1');
    
    -- check conform dicts
    SELECT e."Accession_Code", count(f."RID"), array_agg(f."File_Name"||':'||d."Version")
    from "PDB"."Conform_Dictionary" cd
      JOIN "PDB"."Entry_Generated_File" f ON (cd."Exported_mmCIF_RID" = f."RID")
      JOIN "PDB".entry e ON (f."Structure_Id" = e.id)
      JOIN "PDB"."Accession_Code" ac ON (e."Accession_Code" = ac."Accession_Code")
      JOIN "PDB"."Data_Dictionary" d ON (cd."Data_Dictionary_RID" = d."RID")
    -- WHERE f."RMT" > '20250312'
    GROUP BY e."Accession_Code"
    HAVING count(f."RID") != 2
    
    -- check generated files associated with entries
    SELECT e."Accession_Code", count(f."RID"), array_agg(concat(f."File_Name", ':', f."File_Bytes", ':', f."File_MD5", ' '))
    from "PDB"."Entry_Generated_File" f 
      JOIN "PDB".entry e ON (f."Structure_Id" = e.id)
      JOIN "PDB"."Accession_Code" ac ON (e."Accession_Code" = ac."Accession_Code")
    WHERE f."RMT" > '20250312'
    GROUP BY e."Accession_Code"

'''

#os.chdir(dir)
upload_path = "/tmp/pdb/remediation_upload"
ihm_version = "1.27"    # "1.26"
pdbx_version = "5.399"  # "5.395"
flr_version = "0.02"    # not track previously
delete_other_dicts = False
verbose = False

# --------------------------------------------------------------------------
def insert_new_data_dicts(catalog):
    payload = [
        { "Name": "mmcif_ihm_ext.dic", "Category":"IHMCIF dictionary", "Version": "1.27", "Location": "https://raw.githubusercontent.com/ihmwg/IHMCIF/master/archive/mmcif_ihm_ext-v1.27.dic"},
        { "Name": "mmcif_pdbx.dic", "Category":"PDBx/mmCIF", "Version": "5.399", "Location": "https://raw.githubusercontent.com/wwpdb-dictionaries/mmcif_pdbx/master/archive/mmcif_pdbx_v50-v5.399.dic"},        
        { "Name": "mmcif_ihm_flr_ext.dic", "Category": "FLRCIF dictionary", "Version": "0.02", "Location": "https://raw.githubusercontent.com/ihmwg/flrCIF/master/archive/mmcif_ihm_flr_ext-v0.02.dic"},        
    ]
    insert_if_not_exist(catalog, "PDB", "Data_Dictionary", payload)
    
# --------------------------------------------------------------------------
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

# --------------------------------------------------------------------------
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

# =================================================================================
'''
# TODO: Make this more modular. Allow adaptation to dictionary model and versions.
#
# Note: The current script hard code dictionaries and their versions. The existing
# conform dicts that are not from this list is deleted.

# Supported dics used in the script: 
# - mmcif_ihm_ext.dic (v 1.26)
# - mmcif_pdbx.dic (v 5.395)
'''
def main(catalog, store):
    global upload_path
    global ihm_version
    global pdbx_version
    hatrac_file = HatracFile(store)
    print("current cwd: %s" % (os.getcwd()))
    print("upload dir: %s" % (upload_path))

    # == query data from ermrest to be used for processing
    # -- get accession code to entry information
    code2entries = {}
    id2entries = {}
    # TODO: check whether accession_code is already in entry table
    #rows = catalog.get("/attribute/M:=PDB:entry/A:=PDB:Accession_Code/$M/RID,id,RCB,A:Accession_Code,Workflow_Status,Manual_Processing,Process_Status?limit=1000").json()
    rows = get_ermrest_query(catalog, "PDB", "entry", attributes=["id","RCB","Accession_Code","Workflow_Status","Manual_Processing","Process_Status"])
    for row in rows:
        row["uid"] = row["RCB"].replace("https://auth.globus.org/", "")
        code2entries[row["Accession_Code"]] = row
        id2entries[row["id"]] = row
    #print(json.dumps(rows, indent=4))
    #print(json.dumps(code2rcb, indent=4))

    # -- get existing system generated files
    existing_file2rows = {}
    #rows = catalog.get("/entity/M:=PDB:entry/F:=PDB:Entry_Generated_File?limit=5000").json()
    rows = get_ermrest_query(catalog, "PDB", "entry", constraints="F:=PDB:Entry_Generated_File")
    for row in rows:
        existing_file2rows[(row["Structure_Id"], row["File_Type"])] = row
        
    # -- lookup Data_Dictionary
    mmcif_ihm_rid = None
    mmcif_pdbx_rid = None
    mmcif_flr_rid = None    
    #rows = catalog.get("/entity/M:=PDB:Data_Dictionary").json()
    rows = get_ermrest_query(catalog, "PDB", "Data_Dictionary")
    for row in rows:
        if row["Name"] == "mmcif_ihm_ext.dic" and row["Version"] == ihm_version: 
            mmcif_ihm_rid = row["RID"]
        elif row["Name"] == "mmcif_pdbx.dic" and row["Version"] == pdbx_version: 
            mmcif_pdbx_rid = row["RID"]
        elif row["Name"] == "mmcif_ihm_flr_ext.dic" and row["Version"] == flr_version: 
            mmcif_flr_rid = row["RID"]
    if verbose: print("mmcif_ihm_rid: %s, mmcif_pdbx_rid: %s mmcif_flr_rid:%s " % (mmcif_ihm_rid, mmcif_pdbx_rid, mmcif_flr_rid))
    if not mmcif_ihm_rid or not mmcif_pdbx_rid or not mmcif_flr_rid:
        raise Exception("ERROR: mmcif_ihm_ext.dic version %s or mmcif_pdbx.dic version %s or mmcif_ihm_flr_ext.dic version %s does not exist" % (ihm_version, pdbx_version, flr_version))

    # == read directory
    insert_files = []
    update_files = []
    dir_entry_codes = []
    dir_entry_ids = []
    dir_mmcif_entry_ids = []  # track entries with mmCIF file for conform_dictionary
    for entry_code in os.listdir(upload_path):
        # look for entry metadata
        entry_path = "%s/%s" % (upload_path, entry_code)
        if verbose: print("entry = %s, structure_id:%s" % (entry_code, code2entries[entry_code]["id"]))
        if entry_code not in code2entries.keys():
            print("ERROR: entry_code %s is not in the entry table" % (entry_code))
            continue
        structure_id = code2entries[entry_code]["id"]
        dir_entry_codes.append(entry_code)        
        dir_entry_ids.append(structure_id)
        if os.path.isfile(entry_path): continue
        # iternate ver file in the directory
        for file_name in os.listdir(entry_path):
            if not file_name.startswith(entry_code): continue
            file_path = "%s/%s" % (entry_path, file_name)
            hatrac_entry_path = "%s/pdb/generated/uid/%s/entry/id/%s" % (cfg.hatrac_root, code2entries[entry_code]["uid"], structure_id)
            print("  file_name: %s, file_path: %s" % (file_name, file_path))
            if not os.path.isfile(file_path): continue
            file_type = get_file_type(file_name, entry_code)
            if file_type == "mmCIF": dir_mmcif_entry_ids.append(structure_id)
            upload_file_url = "%s/%s/%s" % (hatrac_entry_path, get_file_type_dir_name(file_type), file_name)
            hatrac_file.upload_file(file_path, upload_file_url, file_name, verbose=False)
            row = {
                "File_URL" : hatrac_file.hatrac_url,
                "File_Name" : hatrac_file.file_name,
                "File_MD5" : hatrac_file.md5_hex,
                "File_Bytes" : hatrac_file.file_bytes,
                "Structure_Id" : structure_id,
                "mmCIF_Schema_Version": ihm_version if file_type == "mmCIF" else  None, # legacy? 
                "File_Type" : file_type,
                "Entry_RCB" : code2entries[entry_code]["RCB"]
            }
            if verbose: print("  file entry ==> %s" % (json.dumps(row, indent=4)))
            if (structure_id, file_type) not in existing_file2rows.keys():
                insert_files.append(row)                
            else:
                row["RID"] = existing_file2rows[(structure_id, file_type)]["RID"]
                # check for changes before update
                if hatrac_file.hatrac_url != existing_file2rows[(structure_id, file_type)]["File_URL"]:
                    update_files.append(row)
            #print(json.dumps(row, indent=4))

    inserted_files = []
    updated_files = []
    if verbose: print("\ninsert_files(%d): %s" % (len(insert_files), json.dumps(insert_files, indent=4)))
    if verbose: print("\nupdate_files(%d): %s" % (len(update_files), json.dumps(update_files, indent=4)))
    inserted_files = insert_if_not_exist(catalog, "PDB", "Entry_Generated_File", insert_files)
    updated_files = update_table_rows(catalog, "PDB", "Entry_Generated_File", keys=["RID"], payload=update_files)
    # update existing_file2rows with newly inserted files
    for row in inserted_files:
        existing_file2rows[(row["Structure_Id"], row["File_Type"])] = row

    # == update Conform_Dictionary. Can only do the update after Entry_Generated_File are updated
    # -- existing conform_dicts
    existing_conform_dicts = {}
    #rows = catalog.get("/attribute/M:=PDB:Conform_Dictionary/F:=(Exported_mmCIF_RID)=(PDB:Entry_Generated_File:RID)/$M/D:=(M:Data_Dictionary_RID)=(PDB:Data_Dictionary:RID)/$M/CRID:=RID,Exported_mmCIF_RID,Data_Dictionary_RID,F:Structure_Id,Dict_Name:=D:Name,D:Category,D:Version?limit=5000").json()
    constraints="F:=(M:Exported_mmCIF_RID)=(PDB:Entry_Generated_File:RID)/$M/D:=(M:Data_Dictionary_RID)=(PDB:Data_Dictionary:RID)/$M"
    rows = get_ermrest_query(catalog, "PDB", "Conform_Dictionary", constraints=constraints, attributes=["CRID:=RID","Exported_mmCIF_RID","Data_Dictionary_RID","F:Structure_Id","Dict_Name:=D:Name","D:Category","D:Version"])
    #print("\nconform_dicts_length:%d, dir_entry_ids: %s" % (len(rows), dir_entry_ids))
    for row in rows:
        if row["Structure_Id"] not in dir_entry_ids: continue
        existing_conform_dicts[(row["Structure_Id"], row["Dict_Name"])] = row

    '''
    print("\nexisting_conform_dicts(%d): " % (len(existing_conform_dicts.keys())) )
    for row in existing_conform_dicts.values():
        print("  (%s, %s) => %s, %s: (%s - %s)" % (row["Structure_Id"], row["Dict_Name"], row["Version"], row["CRID"], row["Exported_mmCIF_RID"], row["Data_Dictionary_RID"]))
    '''

    # -- Iterate over mmcif files in upload directory, create insert and update list of Conform_Dictionary based on Name and Version.
    insert_conform_dicts=[]
    update_conform_dicts=[]
    conform_dict_delete_rid=[]
    file_type = "mmCIF"            
    for structure_id in dir_mmcif_entry_ids:
        if not "RID" in existing_file2rows[(structure_id, file_type)].keys():
            raise Exception("ERROR: file RID doesn't exist: %s" % (row))
        file_rid = existing_file2rows[(structure_id, file_type)]["RID"]
        entry_code = id2entries[structure_id]["Accession_Code"]
        # -- ihm dict
        if (structure_id, "mmcif_ihm_ext.dic") not in existing_conform_dicts.keys():
            #print("(%s, %s) doesn't exist. Will insert" % (structure_id, "mmcif_ihm_ext.dic"))
            insert_conform_dicts.append({"Exported_mmCIF_RID": file_rid, "Data_Dictionary_RID": mmcif_ihm_rid, "_info": "%s - ihm %s" % (entry_code, ihm_version) })
        elif existing_conform_dicts[(structure_id, "mmcif_ihm_ext.dic")]["Version"] != ihm_version:
            crid = existing_conform_dicts[(structure_id, "mmcif_ihm_ext.dic")]["CRID"]
            update_conform_dicts.append({"Exported_mmCIF_RID": file_rid, "Data_Dictionary_RID": mmcif_ihm_rid, "RID": crid, "_info": "%s - ihm %s" % (entry_code, ihm_version) })
        # -- flr dict
        if (structure_id, "mmcif_ihm_flr_ext.dic") not in existing_conform_dicts.keys():
            #print("(%s, %s) doesn't exist. Will insert" % (structure_id, "mmcif_ihm_flr_ext.dic"))
            insert_conform_dicts.append({"Exported_mmCIF_RID": file_rid, "Data_Dictionary_RID": mmcif_flr_rid, "_info": "%s - flr %s" % (entry_code, flr_version) })
        elif existing_conform_dicts[(structure_id, "mmcif_ihm_flr_ext.dic")]["Version"] != flr_version:
            crid = existing_conform_dicts[(structure_id, "mmcif_ihm_flr_ext.dic")]["CRID"]
            update_conform_dicts.append({"Exported_mmCIF_RID": file_rid, "Data_Dictionary_RID": mmcif_flr_rid, "RID": crid, "_info": "%s - flr %s" % (entry_code, flr_version) })
        # -- pdbx dict
        if (structure_id, "mmcif_pdbx.dic") not in existing_conform_dicts.keys():
            #print("(%s, %s) doesn't exist. Will insert" % (structure_id, "mmcif_pdbx.dic"))            
            insert_conform_dicts.append({"Exported_mmCIF_RID": file_rid, "Data_Dictionary_RID": mmcif_pdbx_rid, "_info": "%s - pdbx %s" % (entry_code, pdbx_version) }),
        elif existing_conform_dicts[(structure_id, "mmcif_pdbx.dic")]["Version"] != pdbx_version:
            crid = existing_conform_dicts[(structure_id, "mmcif_pdbx.dic")]["CRID"]
            update_conform_dicts.append({"Exported_mmCIF_RID": file_rid, "Data_Dictionary_RID": mmcif_pdbx_rid, "RID": crid , "_info": "%s - pdbx %s" % (entry_code, pdbx_version) })
            
    #print("\ninsert_conform_dicts(%d): %s" % (len(insert_conform_dicts), json.dumps(insert_conform_dicts, indent=4)))
    #print("\nupdate_conform_dicts(%d): %s" % (len(update_conform_dicts), json.dumps(update_conform_dicts, indent=4)))
    inserted_conform_dicts = insert_if_not_exist(catalog, "PDB", "Conform_Dictionary", insert_conform_dicts)
    updated_conform_dicts = update_table_rows(catalog, "PDB", "Conform_Dictionary", keys=["RID"], payload=update_conform_dicts)
    if verbose: print("\nconform_dicts_inserted(%d/%d): %s" % (len(inserted_conform_dicts), len(insert_conform_dicts), json.dumps(inserted_conform_dicts, indent=4)))
    if verbose: print("\nconform_dicts_updated(%d/%d): %s" % (len(updated_conform_dicts), len(update_conform_dicts), json.dumps(updated_conform_dicts, indent=4)))    

    # -- If flag, delete dicts of uploaded_mmcif files that are not of these two types
    if delete_other_dicts:
        delete_conform_dict_rids=[]
        for (structure_id, dict_name), row in existing_conform_dicts.items():
            #print(" d: %s %s %s " % (structure_id, dict_name, row))
            if structure_id not in dir_mmcif_entry_ids: continue
            if dict_name in ["mmcif_ihm_ext.dic", "mmcif_pdbx.dic", "mmcif_ihm_flr_ext.dic"]: continue
            delete_conform_dict_rids.append(row["CRID"])
        print("\ndelete_conform_dict_rids(%d): %s" % (len(delete_conform_dict_rids), json.dumps(delete_conform_dict_rids, indent=4)))
        if delete_conform_dict_rids:
            constraints = "/RID=ANY(%s)" % (','.join(delete_conform_dict_rids))
            deleted = delete_table_rows(catalog, "PDB", "Conform_Dictionary", constraints=constraints)
            #print("deleted with constraint: %s" % (constraints))
    
    # == update entry table
    '''
    set Workflow_Status = REL, Manual_Processing = True, Process_Status = Success
    Note: Can't set id since it timeouts
    '''
    update_entries = []
    for id in dir_entry_ids: 
        entry_row = id2entries[id]
        structure_id = "D_%s" % (entry_row["RID"])
        if entry_row["Workflow_Status"] != "REL" or entry_row["Manual_Processing"] is False or entry_row["Process_Status"] != "Success":
            update_entries.append({"RID": entry_row["RID"], "Workflow_Status": "REL", "Manual_Processing": True, "Process_Status": "Success", "id": structure_id })
    print("\nupdate_entries (%d/%d): %s" % (len(update_entries), len(dir_entry_ids), json.dumps(update_entries, indent=4)))
    update_table_rows(catalog, "PDB", "entry", keys=["RID"], column_names=["Workflow_Status", "Manual_Processing", "Process_Status"], payload=update_entries)

# =================================================================================
'''
Sset up to run the script:
 1. setup remedy file structures

 - <upload_dir>
   - <accession_code>
     - <accession_code><suffix>  -- <suffix follows file nameing conventions based on different file types>
 examples:
  remediation_upload/9A2H/9A2H_full_validation.pdf
  remediation_upload/9A2H/9A2H_html.tar.gz
  remediation_upload/9A2H/9A2H.cif
  remediation_upload/9A2H/9A2H_summary_validation.pdf
  remediation_upload/9A2H/9A2H.json

2. get the directory to be where we will run the script from. This can be your own laptop.
   If want to run on the server, setup appropriate ownership

# as root on the server:
> cd /scratch
> tar -xvf /home/hongsuda/remediation_upload.tar.gz
> chown -R  hongsuda:hongsuda remediation_upload

3. Run the Script
> python -m pdb_dev.tools.upload_entry_remedy_files --host data.pdb-dev.org --catalog-id 1 --upload-path /scratch/remediation_upload > log

Note: For mmcif files, the script will update the files and conform dict with the provided ihm-version (mmcif_ihm_ext.dic) and pdbx-version (mmcif_pdbx.dic).
If the files are associated with other dicts apart from mmcif_ihm_ext.dic and mmcif_pdbx.dict, if flagged, the conform_dict entries of those types will be deleted. 

'''
if __name__ == "__main__":
    cli = PDBDEV_CLI("pdbdev", None, 1)
    cli.parser.add_argument('--upload-path', help="directory containing entry generated files", default="/tmp/pdb/remedy")
    cli.parser.add_argument('--ihm-version', help="mmcif_ihm_ext.dic version (default: 1.27)", default="1.27")
    cli.parser.add_argument('--pdbx-version', help="mmcif_pdbx.dict version (default: 5.399)", default="5.399")
    cli.parser.add_argument('--flr-version', help="mmcif_ihm_flr_ext.dic version (default: 0.02)", default="0.02")    
    cli.parser.add_argument('--delete-dicts', action="store_true", help="flag whether to delete other dicts that are not ihm/pdbx/flr", default=False)
    cli.parser.add_argument('--verbose', action="store_true", help="flag whether to print progress/status", default=False)
    
    args = cli.parse_cli()
    upload_path = args.upload_path
    ihm_version = args.ihm_version
    pdbx_version = args.pdbx_version
    delete_other_dicts = args.delete_dicts
    verbose = args.verbose
    
    credentials = get_credential(args.host, args.credential_file)
    print("credentials: %s" % (credentials))
    catalog = ErmrestCatalog("https", args.host, args.catalog_id, credentials)
    catalog.dcctx['cid'] = DCCTX["cli/remedy"]
    store = HatracStore("https", args.host, credentials)

    main(catalog, store)

            
        
    

