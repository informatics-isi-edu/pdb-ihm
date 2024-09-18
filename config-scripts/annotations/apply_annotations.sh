#!/bin/bash

# Apply annotations by running
# ./apply_annotations.sh <host> <catalog>
#

host=$1
catalog_id=$2

echo make

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

echo deriva-annotation-config --host ${host} --config-file ${prefix}_annotation_config.json ${catalog_id}
echo python3 -m pdb_dev.config.annotation.apply_all_annotations --host ${host} --catalog-id ${catalog_id}
