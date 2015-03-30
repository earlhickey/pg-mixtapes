#!/bin/sh

# mysql database backup script.
#----------------------------------------------------

# (1) set up all the mysqldump variables
PATH=/data/backups/db/
DBSERVER=127.0.0.1
USER=root
PASS=XXXXXX

for DATABASE in db_name1 db_name2
do
  FILE=${PATH}${DATABASE}.sql.`/bin/date +"%Y%m%d"`
  # (2) in case you run this more than once a day, remove the previous version of the file
  /bin/rm ${FILE}     2> /dev/null
  /bin/rm ${FILE}.gz  2> /dev/null

  # (3) do the mysql database backup (dump)

  # use this command for a database server on a separate host:
  #/usr/bin/mysqldump --opt --protocol=TCP --user=${USER} --password=${PASS} --host=${DBSERVER} ${DATABASE} > ${FILE}

  # use this command for a database server on localhost. add other options if need be.
  /usr/bin/mysqldump --opt --user=${USER} --password=${PASS} ${DATABASE} > ${FILE}

  # (4) gzip the mysql database dump file
  /bin/gzip $FILE

  # (5) show the user the result
  echo "${FILE}.gz was created:"
  /bin/ls -l ${FILE}.gz
done
