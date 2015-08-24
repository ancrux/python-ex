#!/usr/bin/fab -f

import os
import sys
import time
import re
import ConfigParser
from contextlib import nested
from fabric.api import *

# configuration
path_latest_ext = '/tmp/tmc3.latest.ext'
path_project_admin = '/opt/trendmicro/tmscp/vhosts/tmc3/administrator'
deploy_description = 'daily-deploy ' + time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

def copy_latest_extensions():
#   local('rm -rf %s' % path_latest_ext)
#   local('mkdir -p %s' % path_latest_ext)
#   local('scp root@tmrm-dply01.trend.lava.tw:/home/build/output/TMRM/RMX.dev.latest/*.zip %s' % path_latest_ext)
    with lcd(path_latest_ext):
        local("unzip -q '*.zip'")
    pass

def install_extensions():
    local('cd %s; ./install_ext_from_dir.php %s;' % (path_project_admin, path_latest_ext))
    local('cd %s; chown -R apache:apache %s/..' % (path_project_admin, path_project_admin))
    with lcd(path_latest_ext):
        local("rm * -rf")
    pass

def deploy_appservers():
    local("cd %s; ./deploy.py 1 '%s';" % (path_project_admin, deploy_description))
    pass

def deploy_oneserver(target):
    # turn off L4
    with settings(host_string=target, warn_only=True):
        with cd("/opt/trendmicro/tmscp/vhosts"):
            result = run("mv index.html index.html.bak")
            if result.return_code == 0:
                time.sleep(1)
    
    # deploy to server
    local("cd %s; ./deploy.py 1 '%s' '%s';" % (path_project_admin, deploy_description, target))
    
    # turn on L4
    with settings(host_string=target, warn_only=True):
        with cd("/opt/trendmicro/tmscp/vhosts"):
            result = run("mv index.html.bak index.html")
            if result.return_code == 0:
                time.sleep(1)

    pass

def deploy_1by1():
    local("cd %s; ./deploy_1by1.php 1 '%s' '' no;" % (path_project_admin, deploy_description))
    pass

def deploy_1only(target):
    local("cd %s; ./deploy_1by1.php 1 '%s' '%s';" % (path_project_admin, deploy_description, target))
    pass

#@task(default=True)
def cmd(command='echo 0'):
    run(command)

