#!/bin/bash

target_dir=/var/www/html

usage="Usage: $0"

host=`uname -n`

if [ $# -ne 0 ]
then
    echo "ERROR: no arguments supported"
    echo $usage
    exit 1
fi

filenames=(
    robots.txt
    sitemap.xml
    gtm-id.js
    chaise/config/chaise-config.js
    chaise/config/viewer-config.js
    deriva-webapps/config/boolean-search-config.js
    deriva-webapps/config/heatmap-config.js
    deriva-webapps/config/plot-config.js
    deriva-webapps/config/treeview-config.js
    deriva-webapps/config/matrix-config.js
    deriva-webapps/config/vitessce-config.js
)

mkdir -p "${target_dir}/chaise/config"
mkdir -p "${target_dir}/deriva-webapps/config"

chmod u=rwx,og=rx \
      "${target_dir}/chaise" \
      "${target_dir}/chaise/config" \
      "${target_dir}/deriva-webapps" \
      "${target_dir}/deriva-webapps/config"

for f in "${filenames[@]}"
do
    if [ -f "${host}/${f}" ]
    then
	cp "${host}/${f}" "${target_dir}/${f}"
    elif [ -f "default/${f}" ]
    then
	cp "default/${f}" "${target_dir}/${f}"
    fi
    if [ -f "${target_dir}/${f}" ]
    then
	chmod u=rw,og=r "${target_dir}/${f}"
    fi
done

