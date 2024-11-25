#!/bin/bash

/home/isrddev/pdb-ihm/scripts/cron/crontab/pdb_archive_zip.sh

CURRENT_DATE=$(date +"%Y-%m-%d")
RSYNC_DIR=/mnt/vdb1/archive/log/uploaded_pdb_ihm

OUTPUT_LOG_FILE=${RSYNC_DIR}/${CURRENT_DATE}_rsync_output.log
ERROR_LOG_FILE=${RSYNC_DIR}/${CURRENT_DATE}_rsync_error.log

rsync -av --password-file=/home/pdbihm/.secrets/pdb-archive/ihm__user --delete --port=8730  /mnt/vdb1/archive/pdb_ihm/ ihm__user@ihm-exch.rcsb.rutgers.edu::pdb_ihm >${OUTPUT_LOG_FILE} 2>${ERROR_LOG_FILE}

if [ -s ${ERROR_LOG_FILE} ] ;
then
	python3 -m pdb_dev.tools.send_email_notification --config /home/pdbihm/.secrets/mail.json -s "Error rsync archive" -b ${ERROR_LOG_FILE}
else
	python3 -m pdb_dev.tools.send_email_notification --config /home/pdbihm/.secrets/mail.json -s "Successfully rsync archive" -b ""
fi
