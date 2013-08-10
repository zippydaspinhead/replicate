#!/usr/bin/env python

"""Build Cloud Server(s).

Usage:
  build_srv.py <name> [--flavor=<size>] [--image=<name>] [--public_key=<key>]
                      [--region=<name>] [--username=<name>] 
  build_srv.py (-h | --help)

Arguments:
  <name>              Name of the server.

Options:
  -h --help           Show this screen.
  --flavor=<size>     Size of the instance. [default: 512MB]
  --image=<name>      Name of an image to use. [default: CentOS 6.4]
  --public_key=<key>  Path to your SSH public key. [default: ~/.ssh/id_rsa.pub]
  --region=<name>     Region to build in. [default: DFW]
  --username=<name>   Keyring username for authentication.

"""
from docopt import docopt
from os.path import expanduser
import pyrax

args = docopt(__doc__, help = True)

pyrax.set_setting('identity_type', 'rackspace')
pyrax.keyring_auth(args['--username'])
cs = pyrax.connect_to_cloudservers(region = args['--region'])

full_path =  ''.join([expanduser('~') if x == '~' else x \
                     for x in list(args['--public_key'])])

public_key = {'/root/.ssh/authorized_keys': open(full_path)}

image = next(img for img in cs.images.list() if args['--image'] in img.name)
flavor = next(flv for flv in cs.flavors.list() if args['--flavor'] in flv.name)

request = cs.servers.create(args['<name>'], image.id, flavor.id,
  files = public_key)
build = pyrax.utils.wait_until(request, "status", ["ACTIVE", "ERROR"], attempts = 0,
  interval = 30, verbose = True)
server = cs.servers.get(build.id)

public_ipv4 = next(addr for addr in server.networks['public'] if '.' in addr)

print "--"
print "Public IPv4 address: ", public_ipv4
