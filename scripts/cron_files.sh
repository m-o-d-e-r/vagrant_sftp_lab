#!/bin/bash

CREATED_FILE_NAME=`date +"%Y-%m-%d__%H-%M-%S"`

echo "$CREATED_FILE_NAME file will be created localy..."
echo -e "`date`\nfrom\n`ip -br a | grep UP | awk '{print $3}'`" > $CREATED_FILE_NAME

for sftp_ip in `cat ./vms_ip`
do
sftp -o StrictHostKeyChecking=no -i .ssh/id_rsa_$sftp_ip sftp@$sftp_ip << EOF > /dev/null
cd data
put $CREATED_FILE_NAME
EOF
done

echo "Deleting $CREATED_FILE_NAME file..."
rm $CREATED_FILE_NAME
