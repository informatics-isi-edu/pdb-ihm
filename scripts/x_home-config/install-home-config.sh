#!/bin/bash

mkdir -p "/home/pdbihm/config"
target_dir=/home/pdbihm/config

usage="Usage: $0"

host=`uname -n`

# lookup config_dir for complicated hostname
case "$host" in
    docker-pdbdev-validation-o3558551)
	config_dir=workflow-dev.pdb-dev.org
	;;
    ubuntu-ihm-o999742)
	config_dir=workflow-prod.pdb-dev.org
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
    pdb_processing/pdb_conf.json
    pdb_processing/catalog_1_display_entry.json
    pdb_processing/catalog_50_display_entry.json
    pdb_processing/catalog_99_display_entry.json
    pdb_processing/combo1_columns.json
    pdb_processing/ermrest_table_defs.json
    pdb_processing/exported_vocab.pickle
    pdb_processing/json-full-db-ihm_dev_full-col-ihm_dev_full.json
    pdb_processing/mmCIF_defaults.json
    pdb_processing/mmcif_tables_input2output.json
    pdb_processing/optional_fk.json
    pdb_processing/order_by.json
    pdb_processing/tables_groups.json
    pdb_processing/vocab_ucode.json
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

chown -R pdbihm:pdbihm "${target_dir}"

