#!/bin/bash                                                                                                                                                       

# --------
# Script to archive on the production instance 
# Run the script as ubuntu user
# -------   

cd /home/pdbihm
sudo -u pdbihm python3 -m pdb_dev.archive.client --config /home/pdbihm/pdb/config/www/pdb_archive.json

