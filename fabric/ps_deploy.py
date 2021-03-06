#!/usr/bin/fab -f

import os
import sys
import time
import re
import ConfigParser
from contextlib import nested
from fabric.api import *

# configuration
path_latest_ext = '/tmp/tmrm.latest.ext'
path_project_admin = '/opt/trendmicro/tmscp/vhosts/tmrm/administrator'
deploy_description = 'daily-deploy ' + time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

def copy_latest_extensions():
	local('rm -rf %s' % path_latest_ext)
	local('mkdir -p %s' % path_latest_ext)
	local('scp root@bs-dply01.trend.lava.tw:/root/output/TMRM/RMX.dev.latest/*.zip %s' % path_latest_ext)
	with lcd(path_latest_ext):
		local("unzip '*.zip'")
	pass

def install_extensions():
	local('cd %s; ./install_ext_from_dir.php %s;' % (path_project_admin, path_latest_ext))
	local('cd %s; chown -R apache:apache %s/..' % (path_project_admin, path_project_admin))
	pass

def deploy_appservers():
	local("cd %s; ./deploy.py 1 '%s';" % (path_project_admin, deploy_description))
	pass

#@task(default=True)
def cmd(command='echo 0'):
	run(command)

