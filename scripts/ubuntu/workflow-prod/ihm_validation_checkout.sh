#!/bin/bash

. /usr/local/sbin/pdb-software-lib.sh

job_tasks=(
    "python_ihm_validation 20240320"
)

cron_run "hourly-update" "${job_tasks[@]}"

