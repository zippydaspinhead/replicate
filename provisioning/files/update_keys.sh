#!/bin/bash
rm -rf /root/replicate/
rm -rf /root/.ssh/
mkdir -p /root/.ssh/

git clone https://github.com/jpmontez/replicate.git
mv /root/replicate/provisioning/files/public_keys /root/.ssh/authorized_keys
chown root:root /root/.ssh/authorized_keys
chown root:root /root/.ssh/
chmod 600 /root/.ssh/authorized_keys
chmod 700 /root/.ssh/
