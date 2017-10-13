#!/usr/bin/python

carre =[
	['','','','',''],
	['','','','',''],
	['','','','',''],
	['','','','',''],
	['','','','','']
]

def fill_carre(mdp):
	key = []
	for c in mdp:
		if c not in key:
			key.append(c)

	line = 0
	k = 0
	abc = 'abcdefghijklmnopqrstuvxyz'
	c = 0
	while line < len(carre):
		column = 0
		while column < len(carre[line]):
			if k < len(key):
				carre[line][column] = key[k]
				k+=1
			else:
				while abc[c] in key and c < len(abc):
					c += 1
				carre[line][column] = abc[c]
				c += 1
			column += 1
		line += 1

f = open('ch12.txt','r')
fill_carre('tjeozrhcmxqgblvsidnypfaku')

s = f.read()
s = s.replace('a','0')
s = s.replace('b','1')
s = s.replace('c','2')
s = s.replace('d','3')
s = s.replace('e','4')

def lookup(char):
	for i,l in enumerate(carre):
		for j,c in enumerate(l):
			if char == c:
				return i,j

ret = ''
i = 0
while i < len(s) -1:
	if s[i] not in '01234':
		ret += s[i]
		i+=1
		continue
	line,col = int(s[i]),int(s[i+1])-1
	ret += carre[line][col]
	i+=2

print(ret)

