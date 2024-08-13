#!/bin/bash

target_dir=/etc

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

# NOTE: Ubuntu doesn't work well with cron jobs that ends with .sh. 
#   cron.daily/pdb_www_backup.sh
filenames=(
    cron.hourly/manage_hatrac_acls.sh
    cron.daily/workflow-cleanup-tmp
    cron.daily/workflow-dev-update
    #   cron.daily/pdb_www_backup.sh
)

# change modes for parent dirs
#chmod u=rwx,og=rx "${target_dir}" 

for f in "${filenames[@]}"
do
    # get default_folders
    case "${f}" in
	cron.hourly/manage_hatrac_acls.sh )
	    default_dir=default
	    ;;
	cron.daily/workflow-dev-update )
	    default_dir=default-workflow
	    ;;
	cron.daily/workflow-cleanup-tmp )
	    default_dir=default-workflow
	    ;;
	cron.daily/pdb_www_backup.sh )
	    default_dir=default
	    ;;
	*)
	    default_dir="default"
	    ;;
    esac
    #echo "${f} - ${config_dir} ${default_dir}"

    # move files
    if [ -f "${config_dir}/${f}" ]
    then
	echo "cp ${config_dir}/${f} ${target_dir}/${f}"
	cp "${config_dir}/${f}" "${target_dir}/${f}"
    elif [ -f "${default_dir}/${f}" ]
    then
	echo "cp ${default_dir}/${f} ${target_dir}/${f}"
	cp "${default_dir}/${f}" "${target_dir}/${f}"
    fi
    # set mode
    if [ -f "${target_dir}/${f}" ]
    then
	echo 'chmod u=rw,og=r ${target_dir}/${f}'
	chmod u=rw,og=r "${target_dir}/${f}"
    fi
done

