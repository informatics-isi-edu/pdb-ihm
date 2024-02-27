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
git clone https://github.com/informatics-isi-edu/deriva-py.git /home/isrddev/deriva-py
git clone https://github.com/informatics-isi-edu/protein-database.git /home/isrddev/protein-database
chown -R isrddev:isrddev /home/isrddev

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

# Install the backend service
cp /home/isrddev/protein-database/scripts/ubuntu/pdb_www_processing_worker.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable pdb_www_processing_worker

# Adjust ownership
chown -R pdbihm:pdbihm /var/scratch
chown -R pdbihm:root /mnt/vdb1/pdbihm



