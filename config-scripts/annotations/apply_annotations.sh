#!/bin/bash

# Apply annotations by running
# ./apply_annotations.sh <host> <catalog>
#

host=$1
catalog_id=$2

if [ ${catalog_id} -eq 99 ]
then
	prefix="dev"
elif [ ${catalog_id} -eq 50 ]
then
	prefix="staging"
elif [ ${catalog_id} -eq 1 ]
then
	prefix="production"
fi

make all
make clean
deriva-annotation-config --host ${host} --config-file ${prefix}_annotation_config.json ${catalog_id}
python3 -m pdb_dev.config.annotation.apply_all_annotations --host ${host} --catalog-id ${catalog_id}
