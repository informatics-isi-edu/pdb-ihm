#!/bin/bash

. /usr/local/sbin/pdb-software-lib.sh

job_tasks=(
    "derivapy_pull_checkout"
    "pdb_www_pull_checkout"
    "python_ihm_pull_checkout 1.0"
    "derivapy_install"
    "pdb_processing_install"
    "python_ihm_install"
    "python_ihm_validation origin/dev_2.0"
)

cron_run "hourly-update" "${job_tasks[@]}"
