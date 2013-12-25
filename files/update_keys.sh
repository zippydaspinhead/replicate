#!/bin/bash
curl --remote-name https://raw.github.com/jpmontez/replicate/master/files/public_keys
rsync /root/public_keys /root/.ssh/authorized_keys
rm -rf /root/public_keys
