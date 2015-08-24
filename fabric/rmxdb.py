#!/usr/bin/fab -f

import os
import sys
import time
import re
import ConfigParser
from contextlib import nested
from fabric.api import *

ini = ConfigParser.ConfigParser()
ini.optionxform = str
ini.read('/root/rmxdb/rmxdb.ini')
db_hosts = ini.get('db', 'hosts').strip().split(',')
db_user = ini.get('db', 'user').strip()
db_pass = ini.get('db', 'pass').strip()
db_backup_dir = ini.get('db', 'backup_dir').strip()
db_backup_days = int(ini.get('db', 'backup_days'))

env.hosts = db_hosts
env.remote_interrupt = True

print 'db_hosts=' + str(env.hosts)
#print sys.argv

cfg = {}
cfg['db_user'] = db_user
cfg['db_pass'] = db_pass
cfg['db_backup_dir'] = db_backup_dir
cfg['db_backup_dir_keep_latest'] = 86400 * db_backup_days

def sql_cmd(cmd):
	return "mysql --user='%s' --password='%s' -e '%s'" % (cfg['db_user'], cfg['db_pass'], cmd)

@task
@runs_once
def check_synced():
	cmd = 'show status like "wsrep_local_state_comment";'
	result = execute(is_synced, hosts=env.hosts)
	print result
	return result
	pass

@task
@parallel
def is_synced():
	#print env.host_string
	cmd = 'show status like "wsrep_local_state_comment";'
	with quiet():
		out = run(sql_cmd(cmd))
		#print out
		match = re.search('(Synced)', out, re.I | re.M)
		result = True if match else False
		#print result
		return result
	pass

@task
def full_backup_db(file='db_backup'):
	base_dir = '/tmp'
	tmp_dir = 'backup'
	
	with cd(base_dir):
		# clean up temp dir
		run("rm -rf %s" % tmp_dir)

		# xtrabackup commands
		run("innobackupex --user='%s' --password='%s' --no-timestamp %s" % (cfg['db_user'], cfg['db_pass'], tmp_dir))
		run("innobackupex --apply-log %s" % tmp_dir)

		# transfer backup file from remote to local
		file = run("date +rmxdb_%Y-%m-%d") + ".tar.gz"
		run("tar -zcf %s %s" % (file, tmp_dir))
		get("%s" % file, cfg['db_backup_dir'])

		# clean up temp dir
		run("rm -rf %s" % tmp_dir)
	pass

@task
@runs_once
def purge_expired_files(dir, expired_in_sec=86400*7):
	with lcd(dir):
		now = time.time()
		d = os.listdir(dir)
		for entry in d:
			path = dir + os.sep + entry
			match = re.search('(\d\d\d\d)-(\d\d)-(\d\d)', entry)
			if match:
				t = time.mktime((int(match.group(1)), int(match.group(2)), int(match.group(3)), 0, 0, 0, 0, 0, -1))
				if now - t > expired_in_sec:
					local("rm -rf %s" % path)
	pass

@task
@runs_once
def full_backup():
	db_synced = check_synced()
	host_synced = None
	for host in db_synced:
		if  db_synced[host]:
			host_synced = host
			break
	
	if host_synced is None:
		print 'No synced host found! backup failed'
		return False

	print host_synced
	execute(full_backup_db, hosts=[host_synced])
	purge_expired_files(cfg['db_backup_dir'], cfg['db_backup_dir_keep_latest'])
	pass

@task(default=True)
def cmd(command='echo 0'):
	run(command)

