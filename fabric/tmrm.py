#!/usr/bin/fab -f

import sys
from fabric.api import *

#env.hosts = ['host1', 'host2']
env.hosts = [
	'sco-ap01.sjc1',
	'sco-ap02.sjc1',
	'sco-ap03.sjc1',
	'sco-ap04.sjc1',
        'sco-ap05.sjc1',
        'sco-ap06.sjc1',
        'sco-ap07.sjc1',
        'sco-ap08.sjc1',
        'sco-ap09.sjc1',
        'sco-ap10.sjc1',
	'tmrm-rp01.sjc1',
	'tmrm-rp02.sjc1',
	'tmrm-mq01.sjc1',
	'tmrm-mq02.sjc1',
	'tmrm-psa01.sjc1',
	'tmrm-psa02.sjc1',
	'tmrm-cs01.sjc1',
	'tmrm-cs02.sjc1',
	'tmrm-db01.sjc1',
	'tmrm-db02.sjc1'
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

