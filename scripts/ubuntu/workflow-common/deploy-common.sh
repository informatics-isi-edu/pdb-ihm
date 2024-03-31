#!/bin/bash

# Download prebuilt singularity package for Ubuntu 20.04
wget https://salilab.org/~arthur/ihmv/packages/singularity_3.8.4-2_amd64.deb

# Install singularity
apt install -yf ./singularity_3.8.4-2_amd64.deb

# Remove deb
rm ./singularity_3.8.4-2_amd64.deb

# Create pdbihm user
useradd -m pdbihm

# Clone the isrddev repositories
cd /home/isrddev
git clone https://github.com/informatics-isi-edu/deriva-py.git
git clone https://github.com/ihmwg/python-ihm.git
chown -R isrddev:isrddev /home/isrddev

# Install py-rcsb_db
cd /home/pdbihm
mkdir -p .secrets pdb/make-mmCIF pdb/sdb temp 
cd /home/pdbihm/pdb
wget https://salilab.org/~arthur/ihmv/packages/py-rcsb_db_v0.86.tar.gz
tar -xzf py-rcsb_db_v0.86.tar.gz
rm -f py-rcsb_db_v0.86.tar.gz

# Install make-mmcif.py
cp /home/isrddev/python-ihm/util/make-mmcif.py /home/pdbihm/pdb/make-mmCIF/

# Install the mmcif_ihm_v1.22.sdb dictionary
cp /home/isrddev/protein-database/scripts/pdb_processing/config/mmcif_ihm_v1.22.sdb /home/pdbihm/pdb/sdb/

# Install SELinux packages
apt -y install policycoreutils

# Install pip3
apt -y install python3-pip

# Install Python packages
pip3 install --upgrade bdbag[boto,globus]
pip3 install --upgrade biopython
pip3 install --upgrade ihm==1.0
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
cp /home/isrddev/protein-database/scripts/ubuntu/lib/pdb-software-lib.sh /usr/local/sbin/
cp /home/isrddev/protein-database/scripts/cron.daily/cleanup-tmp /etc/cron.daily/

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

# Install pdb_dev
cd /home/isrddev/protein-database
pip3 install --upgrade .

