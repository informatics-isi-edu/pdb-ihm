#!/bin/bash                                                                                                                                                       

# --------
# Script to archive on the dev instance 
# Run the script as ubuntu user
# -------   

cd /home/pdbihm
#sudo -u pdbihm python3 -m pdb_dev.archive.client --config /home/pdbihm/pdb/config/dev/pdb_archive.json
sudo -u pdbihm python3 -m pdb_dev.processing.archive.client --config /home/pdbihm/pdb/config/dev/pdb_archive.json --catalog-id 99
