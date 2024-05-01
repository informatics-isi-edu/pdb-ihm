#!/bin/bash

. /usr/local/sbin/pdb-software-lib.sh

job_tasks=(
    "derivapy_pull_checkout pdb-20240321.1"
    "pdb_www_pull_checkout pdb-20240321.1"
    "python_ihm_pull_checkout 1.0"
    "derivapy_install"
    "pdb_processing_install"
    "python_ihm_install"
    "python_ihm_validation 20240320"
)

cron_run "hourly-update" "${job_tasks[@]}"

