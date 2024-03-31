#!/bin/sh

/home/isrddev/protein-database/scripts/ubuntu/workflow-common/config-common_update.sh

cp /home/isrddev/protein-database/scripts/pdb_processing/config/mmcif_tables_input2output.json /home/pdbihm/pdb/config/dev/
cp /home/isrddev/protein-database/scripts/pdb_processing/config/mmcif_tables_input2output.json /home/pdbihm/pdb/config/staging/
