#!/usr/bin/fab -f

from fabric.api import *
from contextlib import nested

env.disable_known_hosts = True
env.command_prefixes += ['date']

@task(default=True)
def main():
	root_pub_key = '/root/.ssh/id_rsa.pub'
	remote_tmp_key = '/tmp/tmp.pub'

	with nested(prefix('pwd'), settings(hide('warnings'), warn_only=True)):
		put(root_pub_key, remote_tmp_key)
		sudo('test ! -d /root/.ssh && ssh-keygen -N \'\' -f /root/.ssh/id_rsa')
		sudo('cat ' + remote_tmp_key + ' >> /root/.ssh/authorized_keys;rm -f ' + remote_tmp_key + ';')
