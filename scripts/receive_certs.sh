#!/bin/bash

echo "Receiving certs..."

apt install -y jq

interface_name=eth1
current_ip=$(ip -br a | grep $interface_name | awk '{print $3}' | awk -F'/' '{print $1}')
cert_provider_ip=192.10.0.2
cert_provider_port=8080

echo "" > /home/admin/.ssh/authorized_keys
echo "" > /var/sftp/.ssh/authorized_keys

for sftp_ip in `cat /home/admin/vms_ip`
do
response=$(curl -s -X POST http://$cert_provider_ip:$cert_provider_port/certs \
   -H "Content-Type: application/json" \
   -d "{\"ip\": \"$sftp_ip\"}")

echo "$response" | jq -r '.private_key' > /home/admin/.ssh/id_rsa_$sftp_ip
echo "$response" | jq -r '.private_key' > /var/sftp/.ssh/id_rsa_$sftp_ip

chmod 600 /home/admin/.ssh/id_rsa_$sftp_ip
chmod 600 /var/sftp/.ssh/id_rsa_$sftp_ip
done

response=$(curl -s -X POST http://$cert_provider_ip:$cert_provider_port/certs \
   -H "Content-Type: application/json" \
   -d "{\"ip\": \"$current_ip\"}")

echo "$response" | jq -r '.public_key' >> /home/admin/.ssh/authorized_keys
echo "$response" | jq -r '.public_key' >> /var/sftp/.ssh/authorized_keys
