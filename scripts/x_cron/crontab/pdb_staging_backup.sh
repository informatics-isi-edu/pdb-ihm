#!/bin/bash                                                                                                                                                       

# --------
# Script to backup all local databases and the hatrac directory 
# to the apache-pdbdev-deposit-east.wwpdb.org
# To be use with a daily cron job. Only saves the latest daily dump of each  
# database.
# MUST edit the below variables below if not in the default locations
# rsync -arv -e "ssh -i /home/pdbihm/.ssh/id_ed25519" /var/lib/pgsql/14/backups/. ubuntu@apache-pdbdev-deposit-east.wwpdb.org:/mnt/vdb1/PDB-Dev-deriva-DHS/${REMOTE_DIR}/database/.
# rsync -arv -e "ssh -i /home/pdbihm/.ssh/id_ed25519" /var/www/hatrac/. ubuntu@apache-pdbdev-deposit-east.wwpdb.org:/mnt/vdb1/PDB-Dev-deriva-DHS/${REMOTE_DIR}/hatrac/.
# -------   

REMOTE_HOST=apache-pdbdev-deposit-east.wwpdb.org
REMOTE_USER=ubuntu
REMOTE_DIR=dev.pdb-dev.org
IDENTITY_FILE=/home/pdbihm/.ssh/id_ed25519
FROM_DATABASE_DIR=/var/lib/pgsql/14/backups/.
TO_DATABASE_DIR=/mnt/vdb1/PDB-Dev-deriva-DHS/${REMOTE_DIR}/var/lib/pgsql/14/backups/.
FROM_HATRAC_DIR=/var/www/hatrac/.
TO_HATRAC_DIR=/mnt/vdb1/PDB-Dev-deriva-DHS/${REMOTE_DIR}/var/www/hatrac/.

FROM_HOME=/home/pdbihm/pdb
FROM_CONFIG=${FROM_HOME}/config
FROM_CONFIG_DEV=${FROM_CONFIG}/dev/.
FROM_CONFIG_STAGING=${FROM_CONFIG}/staging/.
FROM_MAKE_MMCIF=${FROM_HOME}/make-mmCIF/make-mmcif.py
FROM_PY_RCSB_DB=${FROM_HOME}/py-rcsb_db/.
FROM_CPP_DICT_PACK=${FROM_HOME}/cpp-dict-pack/.
TO_HOME=/mnt/vdb1/PDB-Dev-deriva-DHS/${REMOTE_DIR}/home/pdbihm/pdb
TO_CONFIG=${TO_HOME}/config
TO_CONFIG_DEV=${TO_CONFIG}/dev/.
TO_CONFIG_STAGING=${TO_CONFIG}/staging/.
TO_MAKE_MMCIF=${TO_HOME}/make-mmCIF/make-mmcif.py
TO_PY_RCSB_DB=${TO_HOME}/py-rcsb_db/.
TO_CPP_DICT_PACK=${TO_HOME}/cpp-dict-pack/.


CURRENT_YEAR=$(date +'%Y')
BACKUP_LOGS_DIR=/home/pdbihm/backup_logs/${REMOTE_DIR}
BACKUP_LOG_FILE_NAME=backup_${CURRENT_YEAR}.log
BACKUP_LOG_FILE=${BACKUP_LOGS_DIR}/${BACKUP_LOG_FILE_NAME}
OUTPUT_FILE_NAME=output.log
ERROR_FILE_NAME=error.log
OUTPUT_LOG_FILE=${BACKUP_LOGS_DIR}/${OUTPUT_FILE_NAME}
ERROR_LOG_FILE=${BACKUP_LOGS_DIR}/${ERROR_FILE_NAME}


echo "$(date) : Database backup started." >> ${BACKUP_LOG_FILE}
echo "rsync -arv -e \"ssh -i ${IDENTITY_FILE}\" ${FROM_DATABASE_DIR} ${REMOTE_USER}@${REMOTE_HOST}:${TO_DATABASE_DIR}" >> ${BACKUP_LOG_FILE}
rsync -arv -e "ssh -i ${IDENTITY_FILE}" ${FROM_DATABASE_DIR} ${REMOTE_USER}@${REMOTE_HOST}:${TO_DATABASE_DIR} >${OUTPUT_LOG_FILE} 2>${ERROR_LOG_FILE}
echo "$(date) : Database backup ended." >> ${BACKUP_LOG_FILE}

echo "$(date) : Hatrac backup started." >> ${BACKUP_LOG_FILE}
echo "rsync -arv -e \"ssh -i ${IDENTITY_FILE}\" ${FROM_HATRAC_DIR} ${REMOTE_USER}@${REMOTE_HOST}:${TO_HATRAC_DIR}" >> ${BACKUP_LOG_FILE}
rsync -arv -e "ssh -i ${IDENTITY_FILE}" ${FROM_HATRAC_DIR} ${REMOTE_USER}@${REMOTE_HOST}:${TO_HATRAC_DIR} >>${OUTPUT_LOG_FILE} 2>>${ERROR_LOG_FILE}
echo "$(date) : Hatrac backup ended." >> ${BACKUP_LOG_FILE}

echo "$(date) : Home backup started." >> ${BACKUP_LOG_FILE}
echo "rsync -arv -e \"ssh -i ${IDENTITY_FILE}\" ${FROM_CONFIG_DEV} ${REMOTE_USER}@${REMOTE_HOST}:${TO_CONFIG_DEV}" >> ${BACKUP_LOG_FILE}
rsync -arv -e "ssh -i ${IDENTITY_FILE}" ${FROM_CONFIG_DEV} ${REMOTE_USER}@${REMOTE_HOST}:${TO_CONFIG_DEV} >>${OUTPUT_LOG_FILE} 2>>${ERROR_LOG_FILE}
echo "rsync -arv -e \"ssh -i ${IDENTITY_FILE}\" ${FROM_CONFIG_STAGING} ${REMOTE_USER}@${REMOTE_HOST}:${TO_CONFIG_STAGING}" >> ${BACKUP_LOG_FILE}
rsync -arv -e "ssh -i ${IDENTITY_FILE}" ${FROM_CONFIG_STAGING} ${REMOTE_USER}@${REMOTE_HOST}:${TO_CONFIG_STAGING} >>${OUTPUT_LOG_FILE} 2>>${ERROR_LOG_FILE}
echo "rsync -arv -e \"ssh -i ${IDENTITY_FILE}\" ${FROM_PY_RCSB_DB} ${REMOTE_USER}@${REMOTE_HOST}:${TO_PY_RCSB_DB}" >> ${BACKUP_LOG_FILE}
rsync -arv -e "ssh -i ${IDENTITY_FILE}" ${FROM_PY_RCSB_DB} ${REMOTE_USER}@${REMOTE_HOST}:${TO_PY_RCSB_DB} >>${OUTPUT_LOG_FILE} 2>>${ERROR_LOG_FILE}
echo "rsync -arv -e \"ssh -i ${IDENTITY_FILE}\" ${FROM_CPP_DICT_PACK} ${REMOTE_USER}@${REMOTE_HOST}:${TO_CPP_DICT_PACK}" >> ${BACKUP_LOG_FILE}
rsync -arv -e "ssh -i ${IDENTITY_FILE}" ${FROM_CPP_DICT_PACK} ${REMOTE_USER}@${REMOTE_HOST}:${TO_CPP_DICT_PACK} >>${OUTPUT_LOG_FILE} 2>>${ERROR_LOG_FILE}
echo "rsync -arv -e \"ssh -i ${IDENTITY_FILE}\" ${FROM_MAKE_MMCIF} ${REMOTE_USER}@${REMOTE_HOST}:${TO_MAKE_MMCIF}" >> ${BACKUP_LOG_FILE}
rsync -arv -e "ssh -i ${IDENTITY_FILE}" ${FROM_MAKE_MMCIF} ${REMOTE_USER}@${REMOTE_HOST}:${TO_MAKE_MMCIF} >>${OUTPUT_LOG_FILE} 2>>${ERROR_LOG_FILE}
echo "$(date) : Home backup ended." >> ${BACKUP_LOG_FILE}

echo "" >> ${BACKUP_LOG_FILE}
