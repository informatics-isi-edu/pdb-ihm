#!/bin/bash                                                                                                                                                       

# --------
# Script to archive on the production instance 
# Run the script as ubuntu user
# -------   

cd /home/pdbihm
#sudo -u pdbihm python3 -m pdb_dev.archive.client --config /home/pdbihm/pdb/config/www/pdb_archive.json
sudo -u pdbihm python3 -m pdb_dev.processing.archive.client --config /home/pdbihm/pdb/config/www/pdb_archive.json --host data.pdb-dev.org --catalog-id 1

python3 -m pdb_dev.tools.send_email_notification --config /home/pdbihm/.secrets/mail.json -s "Archive Generation has Completed" -b ""
