#!/usr/bin/fab -f

import sys
from fabric.api import *

#env.hosts = ['host1', 'host2']
env.hosts = ['tmscp-ps-ap01.sjc1', 'tmscp-ps-ap02.sjc1']
env.remote_interrupt = True
env.warn_only = True

#print sys.argv

@task(default=True)
def cmd(command):
    run(command)

