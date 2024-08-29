#!/bin/bash

chown -R admin:admin /home/admin
chown -R sftp:sftp /var/sftp/.ssh

systemctl restart cron.service
systemctl restart sshd.service

rkhunter --check --skip-keypress
