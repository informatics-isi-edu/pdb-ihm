#!/bin/bash                                                                                                                                                       

# --------
# Script to archive on the dev instance 
# Run the script as ubuntu user
# -------   

cd /home/pdbihm
sudo -u pdbihm python3 -m pdb_dev.processing.archive.client --config /home/pdbihm/config/archive_processing/pdb_archive_config.json --catalog-id 99
