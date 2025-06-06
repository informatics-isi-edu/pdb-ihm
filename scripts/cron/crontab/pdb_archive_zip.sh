#!/bin/bash

CURRENT_DATE=$(date +"%Y-%m-%d")
UPLOADED_ZIP_DIR=/mnt/vdb1/archive/log/uploaded_pdb_ihm

OUTPUT_LOG_FILE=${UPLOADED_ZIP_DIR}/${CURRENT_DATE}_zip_output.log
ERROR_LOG_FILE=${UPLOADED_ZIP_DIR}/${CURRENT_DATE}_zip_error.log

ZIP_FILE=${CURRENT_DATE}.tar.gz
cd /mnt/vdb1/archive
tar -czvf ${ZIP_FILE} pdb_ihm >${OUTPUT_LOG_FILE} 2>${ERROR_LOG_FILE}
rm -f ${UPLOADED_ZIP_DIR}/${ZIP_FILE}
mv ${ZIP_FILE} ${UPLOADED_ZIP_DIR}/
chown -R pdbihm:root ${UPLOADED_ZIP_DIR}

if [ -s ${ERROR_LOG_FILE} ] ;
then
	python3 -m pdb_dev.tools.send_email_notification --config /home/pdbihm/.secrets/mail.json -s "Error zipping the archive" -b ${ERROR_LOG_FILE}
else
	python3 -m pdb_dev.tools.send_email_notification --config /home/pdbihm/.secrets/mail.json -s "Successfully zipped the archive" -b ""
fi
