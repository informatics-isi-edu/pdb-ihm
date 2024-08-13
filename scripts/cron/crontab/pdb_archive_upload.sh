#!/bin/bash

rsync -av --password-file=/home/pdbihm/.secrets/pdb-archive/ihm__user --delete --port=8730  /mnt/vdb1/archive/pdb_ihm/ ihm__user@ihm-exch.rcsb.rutgers.edu::pdb_ihm
