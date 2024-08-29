#!/bin/bash

echo "nameserver 8.8.8.8" > /etc/resolv.conf

apt-get update
DEBIAN_FRONTEND=noninteractive apt-get install -y rkhunter

rkhunter --update

useradd -U -m -d /var/sftp -s /bin/bash sftp
useradd -U -m -d /home/admin -s /bin/bash admin

mkdir /home/admin/.ssh
chown -R admin:admin /home/admin/.ssh

mkdir /var/sftp/data
mkdir /var/sftp/.ssh

chown root:root /var/sftp
chown sftp:sftp /var/sftp/data
chmod 755 /var/sftp

if ! grep -q "Match Group sftp" /etc/ssh/sshd_config; then
    echo "Match Group sftp
        ChrootDirectory /var/sftp/
        X11Forwarding no
        AllowTcpForwarding no
        PasswordAuthentication no
        ForceCommand internal-sftp
    " >> /etc/ssh/sshd_config
fi

echo "* * * * * bash /home/admin/cron_files.sh" > /var/spool/cron/crontabs/admin
chown admin:crontab /var/spool/cron/crontabs/admin
chmod 0600 /var/spool/cron/crontabs/admin
