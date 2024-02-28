#/bin/bash
#####################################################################################
# Schema updates 2024 release version 1
#####################################################################################
cd validation_files
python3 2023_01_Entry_mmCIF_File.py --host dev-aws.pdb-dev.org
cd ../comments
python3 2024_01_comment.py --host dev-aws.pdb-dev.org 
cd ../entry_extension
python3 2024_01_entry.py --host dev-aws.pdb-dev.org 
cd ..
