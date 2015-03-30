#!/bin/sh 

# mysql database restore script.
#----------------------------------------------------

# (1) set up all the mysqldump variables
PATH=/data/backups/db/
DBSERVER=127.0.0.1
USER=root
PASS=XXXXXX

for DATABASE in db_name1 db_name2
do
  FILE=${PATH}${DATABASE}.sql.`/bin/date +"%Y%m%d"`

  /bin/gunzip -c ${FILE}.gz > ${FILE}

  /usr/bin/mysql --user=${USER} --password=${PASS} ${DATABASE} < ${FILE}

  /bin/rm ${FILE}
done
