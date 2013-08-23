#!/bin/bash
curl --remote-name https://raw.github.com/jpmontez/replicate/master/provisioning/files/public_keys 
rsync --checksum --perms --no-o --no-g /root/public_keys /root/.ssh/authorized_keys
rm -rf /root/public_keys
