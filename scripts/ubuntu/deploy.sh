#!/bin/bash

ROOT_DIR=$PWD

apt update -y
apt install -y wget git

# Download prebuilt singularity package for Ubuntu 20.04
wget https://salilab.org/~arthur/ihmv/packages/singularity_3.8.4-2_amd64.deb

# Install singularity
apt install -yf ./singularity_3.8.4-2_amd64.deb

# Remove deb
rm ./singularity_3.8.4-2_amd64.deb

# Create singularity work directory
mkdir -p /mnt/vdb1/pdbihm
cd /mnt/vdb1/pdbihm
mkdir -p input output cache

# Download precompiled singularity image
wget https://salilab.org/~arthur/ihmv/prebuilt_containers/ihmv_20231222.sif

# Clone code
git clone --branch dev_2.0 https://github.com/salilab/IHMValidation.git

# Test installation
singularity exec --pid --bind IHMValidation/:/opt/IHMValidation,input:/ihmv/input,output:/ihmv/output,cache:/ihmv/cache ihmv_20231222.sif /opt/IHMValidation/ihm_validation/ihm_validator.py --output-root /ihmv/output --cache-root /ihmv/cache --force -h

# Create users
useradd -m pdbihm
useradd -m isrddev

# Clone the isrddev repositories
cd /home/isrddev
git clone https://github.com/informatics-isi-edu/deriva-py.git
git clone https://github.com/informatics-isi-edu/protein-database.git
chown -R isrddev:isrddev /home/isrddev

# Install py-rcsb_db
cd /home/pdbihm
mkdir -p .secrets pdb/config/www pdb/make-mmCIF pdb/sdb pdb/log/www pdb/cpp-dict-pack/build/bin backup_logs/www temp 
cd /home/pdbihm/pdb
wget https://salilab.org/~arthur/ihmv/packages/py-rcsb_db_v0.86.tar.gz
tar -xzf py-rcsb_db_v0.86.tar.gz
rm -f py-rcsb_db_v0.86.tar.gz

# Install make-mmcif.py
cd /home/pdbihm/pdb/make-mmCIF
# wget https://github.com/ihmwg/python-ihm/blob/main/util/make-mmcif.py
wget https://raw.githubusercontent.com/ihmwg/python-ihm/main/util/make-mmcif.py

# From the protein-database repository
# wget https://raw.githubusercontent.com/informatics-isi-edu/protein-database/master/scripts/make-mmCIF/make-mmcif.py

# Install CifCheck
cp /home/isrddev/protein-database/scripts/validator/CifCheck /home/pdbihm/pdb/cpp-dict-pack/build/bin/

# Install the mmcif_ihm_v1.22.sdb dictionary
cp /home/isrddev/protein-database/scripts/pdb_processing/config/mmcif_ihm_v1.22.sdb /home/pdbihm/pdb/sdb/

# Install secrets
cp XXX/credentials.json /home/pdbihm/.secrets/
cp XXX/mail.json /home/pdbihm/.secrets/

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
cp /home/isrddev/protein-database/scripts/pdb_processing/config/pdb_conf.json ./

# Install SELinux packages
apt -y install policycoreutils

# Install pip3
apt -y install python3-pip

# Install Python packages
pip3 install --upgrade bdbag[boto,globus]
pip3 install --upgrade biopython
pip3 install --upgrade ihm
pip3 install --upgrade mmcif
pip3 install --upgrade rcsb.utils.io
pip3 install --upgrade rcsb.utils.io
pip3 install --upgrade rcsb.utils.chemref
pip3 install --upgrade rcsb.utils.ec
pip3 install --upgrade rcsb.utils.seq
pip3 install --upgrade rcsb.utils.struct
pip3 install --upgrade rcsb.utils.taxonomy
pip3 install --upgrade rcsb.utils.multiproc

# Copy the isrd software library
cp /home/isrddev/protein-database/scripts/ubuntu/isrd-software-lib.sh /usr/local/sbin/

# Create the scratch directory
mkdir -p /var/scratch/www

# Install the g++ library
add-apt-repository -y ppa:ubuntu-toolchain-r/test
apt install -y g++-11

# Adjust ownership
chown -R pdbihm:pdbihm /home/pdbihm
chown -R pdbihm:pdbihm /var/scratch
chown -R pdbihm:root /mnt/vdb1/pdbihm

# Install and start the backend service
cp /home/isrddev/protein-database/scripts/ubuntu/pdb_www_processing_worker.service /etc/systemd/system/
chmod u-w /etc/systemd/system/pdb_www_processing_worker.service
systemctl daemon-reload
systemctl enable pdb_www_processing_worker
systemctl start pdb_www_processing_worker

