#!/bin/bash                                                                                                                                                       

# --------
# Script to archive on the dev instance the staging catalog
# Run the script as ubuntu user
# -------   

cd /home/pdbihm
sudo -u pdbihm python3 -m pdb_dev.archive.client --config /home/pdbihm/pdb/config/staging/pdb_archive.json

