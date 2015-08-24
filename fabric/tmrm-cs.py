#!/usr/bin/fab -f

import sys
from fabric.api import *

#env.hosts = ['host1', 'host2']
env.hosts = [
        'tmrm-cs01.sjc1',
        'tmrm-cs02.sjc1'
	]
env.remote_interrupt = True
env.command_timeout = None
env.timeout = None
env.warn_only = True

#print sys.argv

@task(default=True)
#@parallel(pool_size=5)
def cmd(command):
    run(command)

