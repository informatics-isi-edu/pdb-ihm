#!/bin/sh

cp /home/isrddev/protein-database/scripts/pdb_processing/config/mmcif_tables_input2output.json /home/pdbihm/pdb/config/dev/
cp /home/isrddev/protein-database/scripts/pdb_processing/config/mmcif_tables_input2output.json /home/pdbihm/pdb/config/staging/
cp /home/isrddev/protein-database/scripts/validator/CifCheck /home/pdbihm/pdb/cpp-dict-pack/build/bin/
cp /home/isrddev/protein-database/scripts/make-json/py-rcsb_db/rcsb/db/tests-validate/testSchemaDataPrepValidate-ihm.py /home/pdbihm/pdb/py-rcsb_db/rcsb/db/tests-validate/
