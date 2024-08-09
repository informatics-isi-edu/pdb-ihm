#!/bin/bash

mkdir -p "/home/pdbihm/config"
target_dir=/home/pdbihm/config

usage="Usage: $0"

host=`uname -n`

# lookup config_dir for complicated hostname
case "$host" in
    docker-pdbdev-validation-o3558551)
	config_dir=workflow-dev
	;;
    ubuntu-ihm-o999742)
	config_dir=workflow-prod
	;;
    *)
	config_dir="$host"
	;;
esac


if [ $# -ne 0 ]
then
    echo "ERROR: no arguments supported"
    echo $usage
    exit 1
fi

filenames=(
    archive_processing/pdb_archive_config.json
)

mkdir -p "${target_dir}/archive_processing/"
mkdir -p "${target_dir}/pdb_processing/"

chmod u=rwx,og=rx \
      "${target_dir}" \
      "${target_dir}/archive_processing" \
      "${target_dir}/pdb_processing" 

for f in "${filenames[@]}"
do
    if [ -f "${config_dir}/${f}" ]
    then
	cp "${config_dir}/${f}" "${target_dir}/${f}"
    elif [ -f "default/${f}" ]
    then
	cp "default/${f}" "${target_dir}/${f}"
    fi
    if [ -f "${target_dir}/${f}" ]
    then
	chmod u=rw,og=r "${target_dir}/${f}"
    fi
done

