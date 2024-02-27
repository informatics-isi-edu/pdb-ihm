#!/bin/bash

. /usr/local/sbin/isrd-software-lib.sh

job_tasks=(
    "derivapy_pull_checkout pdb-20231127.1"
    "pdb_www_pull_checkout pdb-20231127.1"
    "derivapy_install"
    "pdb_processing_install"
    "require /home/isrddev/protein-database/scripts/deploy/config_update.sh"
    "require service pdb_www_processing_worker restart"
)

cron_run "hourly-update" "${job_tasks[@]}"

