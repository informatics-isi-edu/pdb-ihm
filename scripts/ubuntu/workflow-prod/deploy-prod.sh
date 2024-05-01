#!/bin/bash

# scp the credentials.json and mail.json files into the directory from where you are running the deploy-prod.sh script

BASEDIR=$(pwd)

apt update -y

# Install if necessary wget and git
apt install -y wget git

# Create isrddev user
useradd -m isrddev

# Clone protein-database repository
cd /home/isrddev
git clone https://github.com/informatics-isi-edu/protein-database.git

# Install common packages
/home/isrddev/protein-database/scripts/ubuntu/workflow-common/deploy-common.sh

# Create singularity work directory
mkdir -p /mnt/vdb1/pdbihm
cd /mnt/vdb1/pdbihm
mkdir -p input output cache

# Download precompiled singularity image
wget https://salilab.org/~arthur/ihmv/prebuilt_containers/ihmv_20231222.sif

# Clone code
git clone --branch dev_2.0 https://github.com/salilab/IHMValidation.git

# Test installation
# singularity exec --pid --bind IHMValidation/:/opt/IHMValidation,input:/ihmv/input,output:/ihmv/output,cache:/ihmv/cache ihmv_20231222.sif /opt/IHMValidation/ihm_validation/ihm_validator.py --output-root /ihmv/output --cache-root /ihmv/cache --force -h

# Create users
useradd -m pdbihm

# Clone the isrddev repositories
cd /home/isrddev
git clone https://github.com/informatics-isi-edu/deriva-py.git
git clone https://github.com/ihmwg/python-ihm.git
chown -R isrddev:isrddev /home/isrddev

# Make production specific directories
cd /home/pdbihm
mkdir -p pdb/config/www pdb/log/www backup_logs/www 

# Install secrets
cp $BASEDIR/credentials.json /home/pdbihm/.secrets/
cp $BASEDIR/mail.json /home/pdbihm/.secrets/

# Install configuration files
cd /home/pdbihm/pdb/config/www
cp /home/isrddev/protein-database/scripts/pdb_processing/config/catalog_1_display_entry.json ./
cp /home/isrddev/protein-database/scripts/pdb_processing/config/mmCIF_defaults.json ./
cp /home/isrddev/protein-database/scripts/pdb_processing/config/vocab_ucode.json ./
cp /home/isrddev/protein-database/scripts/pdb_processing/config/tables_groups.json ./
cp /home/isrddev/protein-database/scripts/pdb_processing/config/optional_fk.json ./
cp /home/isrddev/protein-database/scripts/pdb_processing/config/ermrest_table_defs.json ./
cp /home/isrddev/protein-database/scripts/pdb_processing/config/mmcif_tables_input2output.json ./
cp /home/isrddev/protein-database/scripts/pdb_processing/config/order_by.json ./
cp /home/isrddev/protein-database/scripts/pdb_processing/config/combo1_columns.json ./
cp /home/isrddev/protein-database/scripts/pdb_processing/config/exported_vocab.map ./
cp /home/isrddev/protein-database/scripts/pdb_processing/config/pdb_conf_www.json ./pdb_conf.json

# Copy the production scripts
cp /home/isrddev/protein-database/scripts/ubuntu/workflow-prod/www-update.sh /root/
cp /home/isrddev/protein-database/scripts/ubuntu/workflow-prod/ihm_validation_checkout.sh /root/
cp /home/isrddev/protein-database/scripts/ubuntu/workflow-prod/www-checkout.sh /root/

# Create the scratch directory
mkdir -p /var/scratch/www

# Adjust ownership
chown -R pdbihm:pdbihm /home/pdbihm
chown -R pdbihm:pdbihm /var/scratch
chown -R pdbihm:root /mnt/vdb1/pdbihm

# Apply the tags
/root/ihm_validation_checkout.sh
/root/www-checkout.sh

# Install and start the backend service
cp /home/isrddev/protein-database/scripts/ubuntu/workflow-prod/pdb_www_processing_worker.service /etc/systemd/system/
chmod u-w /etc/systemd/system/pdb_www_processing_worker.service
systemctl daemon-reload
systemctl enable pdb_www_processing_worker
systemctl start pdb_www_processing_worker

