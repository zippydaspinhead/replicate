name             'base'
maintainer       'Julian Montez'
maintainer_email 'julian.montez@rackspace.com'
license          'All rights reserved'
description      'Installs/Configures base'
long_description IO.read(File.join(File.dirname(__FILE__), 'README.md'))
version          '0.1.0'

depends 'apt'
depends 'git'
depends 'mysql'
depends 'networking_basic'
