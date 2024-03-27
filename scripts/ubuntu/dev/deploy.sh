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
git clone https://github.com/ihmwg/python-ihm.git
chown -R isrddev:isrddev /home/isrddev

# Install py-rcsb_db
cd /home/pdbihm
mkdir -p .secrets pdb/config/dev pdb/config/staging pdb/make-mmCIF pdb/sdb pdb/log/dev pdb/log/staging pdb/cpp-dict-pack/build/bin backup_logs/dev backup_logs/staging temp 
cd /home/pdbihm/pdb
wget https://salilab.org/~arthur/ihmv/packages/py-rcsb_db_v0.86.tar.gz
tar -xzf py-rcsb_db_v0.86.tar.gz
rm -f py-rcsb_db_v0.86.tar.gz

# Install make-mmcif.py
cp /home/isrddev/python-ihm/util/make-mmcif.py /home/pdbihm/pdb/make-mmCIF/

# Install the mmcif_ihm_v1.22.sdb dictionary
cp /home/isrddev/protein-database/scripts/pdb_processing/config/mmcif_ihm_v1.22.sdb /home/pdbihm/pdb/sdb/

# Install secrets
# Replace XXX with the location of those files and uncomment the lines
# cp XXX/credentials.json /home/pdbihm/.secrets/
# cp XXX/mail.json /home/pdbihm/.secrets/

# Install configuration files
cd /home/pdbihm/pdb/config/dev
cp /home/isrddev/protein-database/scripts/pdb_processing/config/catalog_99_display_entry.json ./
cp /home/isrddev/protein-database/scripts/pdb_processing/config/mmCIF_defaults.json ./
cp /home/isrddev/protein-database/scripts/pdb_processing/config/vocab_ucode.json ./
cp /home/isrddev/protein-database/scripts/pdb_processing/config/tables_groups.json ./
cp /home/isrddev/protein-database/scripts/pdb_processing/config/optional_fk.json ./
cp /home/isrddev/protein-database/scripts/pdb_processing/config/ermrest_table_defs.json ./
cp /home/isrddev/protein-database/scripts/pdb_processing/config/mmcif_tables_input2output.json ./
cp /home/isrddev/protein-database/scripts/pdb_processing/config/order_by.json ./
cp /home/isrddev/protein-database/scripts/pdb_processing/config/combo1_columns.json ./
cp /home/isrddev/protein-database/scripts/pdb_processing/config/exported_vocab.map ./
cp /home/isrddev/protein-database/scripts/pdb_processing/config/pdb_conf_dev.json ./pdb_conf.json

cd /home/pdbihm/pdb/config/staging
cp /home/isrddev/protein-database/scripts/pdb_processing/config/catalog_50_display_entry.json ./
cp /home/isrddev/protein-database/scripts/pdb_processing/config/mmCIF_defaults.json ./
cp /home/isrddev/protein-database/scripts/pdb_processing/config/vocab_ucode.json ./
cp /home/isrddev/protein-database/scripts/pdb_processing/config/tables_groups.json ./
cp /home/isrddev/protein-database/scripts/pdb_processing/config/optional_fk.json ./
cp /home/isrddev/protein-database/scripts/pdb_processing/config/ermrest_table_defs.json ./
cp /home/isrddev/protein-database/scripts/pdb_processing/config/mmcif_tables_input2output.json ./
cp /home/isrddev/protein-database/scripts/pdb_processing/config/order_by.json ./
cp /home/isrddev/protein-database/scripts/pdb_processing/config/combo1_columns.json ./
cp /home/isrddev/protein-database/scripts/pdb_processing/config/exported_vocab.map ./
cp /home/isrddev/protein-database/scripts/pdb_processing/config/pdb_conf_staging.json ./pdb_conf.json

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
cp /home/isrddev/protein-database/scripts/ubuntu/dev/pdb-software-lib.sh /usr/local/sbin/
cp /home/isrddev/protein-database/scripts/ubuntu/dev/cleanup-tmp /etc/cron.daily/
cp /home/isrddev/protein-database/scripts/ubuntu/dev/dev-checkout.sh /root/

# Create the scratch directory
mkdir -p /var/scratch/dev
mkdir -p /var/scratch/staging

# Install the g++ library
add-apt-repository -y ppa:ubuntu-toolchain-r/test
apt install -y g++-11

# Build CifCheck
apt install -y cmake flex bison
cd /home/pdbihm/pdb
git clone  --recurse-submodules  https://github.com/rcsb/cpp-dict-pack.git
cd cpp-dict-pack
mkdir build
cd build
cmake .. -DMINIMAL_DICTS=ON
make


# Adjust ownership
chown -R pdbihm:pdbihm /home/pdbihm
chown -R pdbihm:pdbihm /var/scratch
chown -R pdbihm:root /mnt/vdb1/pdbihm

# Apply the tags
/root/dev-checkout.sh

# Install pdb_dev
cd /home/isrddev/protein-database
pip3 install --upgrade .

# Install and start the backend service
cp /home/isrddev/protein-database/scripts/ubuntu/dev/pdb_dev_processing_worker.service /etc/systemd/system/
cp /home/isrddev/protein-database/scripts/ubuntu/dev/pdb_staging_processing_worker.service /etc/systemd/system/
chmod u-w /etc/systemd/system/pdb_dev_processing_worker.service
chmod u-w /etc/systemd/system/pdb_staging_processing_worker.service
systemctl daemon-reload
systemctl enable pdb_dev_processing_worker
systemctl enable pdb_staging_processing_worker
systemctl start pdb_dev_processing_worker
systemctl start pdb_staging_processing_worker

