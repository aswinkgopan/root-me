#!/usr/bin/python
# coding: utf-8

# Les bitmaps commencent par les caractères 'B' et 'M', et sont suivis de la taille en little endian.
clairConnu = ['B', 'M', '\xf6', '\x8f', '\x07', '\x00']
def make_key(ciph, cc):
	ret = []
	for j,c in enumerate(cc):
		i = 0
		while i^ord(ciph[j]) != ord(c):
			i+=1
		ret.append(i)
	return ret

def xor(ciph, key):
	n = len(key)
	start = 0
	end = start + n
	size = len(ciph)
	ret = []
	while end < size:
		for i,c in enumerate(ciph[start:end]):
			ret.append(ord(c)^key[i])
		start = end
		end += n
	return ret

with open('ch3.bmp', 'r') as f:
	s = f.read()

key = make_key(s, clairConnu)
print([chr(x) for x in key])
l = xor(s, key)
with open('clear.bmp', 'w') as clr:
	for c in l:
		clr.write(chr(c))
