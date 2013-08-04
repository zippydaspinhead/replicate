#!/usr/bin/env python

"""Build Cloud Server(s).

Usage:
  build_srv.py <name> [--flavor=<size>] [--image=<name>] [--username=<name>]
                      [--public_key=<key>] [--region=<name>]
  build_srv.py (-h | --help)

Arguments:
  <name>              Name of the server.

Options:
  -h --help           Show this screen.
  --flavor=<size>     Size of the instance. [default: 512MB]
  --image=<name>      Name of an image to use. [default: Ubuntu 13.04]
  --username=<name>   Keyring username for authentication.
  --public_key=<key>  Path to your SSH public key.
  --region=<name>     Region to build in. [default: DFW]

"""
from docopt import docopt
import pyrax

args = docopt(__doc__, help = True)

pyrax.set_setting('identity_type', 'rackspace')
pyrax.keyring_auth(args['--username'])
cs = pyrax.connect_to_cloudservers(region=args['--region'])

key = open(args['--public_key'])
public_key = {'/root/.ssh/authorized_keys': key}

image = next(img for img in cs.images.list() if args['--image'] in img.name)
flavor = next(flav for flav in cs.flavors.list() if args['--flavor'] in flav.name)

build = cs.servers.create(args['<name>'], image.id,
		            flavor.id, files = public_key)
srv = pyrax.utils.wait_until(build, "status", ["ACTIVE", "ERROR"],
                attempts = 0, interval = 20, verbose = True)

srv = cs.servers.get(srv.id)

print "--"
print "Public IP address: ", srv.networks['public'][0]
