#!/usr/bin/python

ciphertext = 'Wnb.r.ietoeh Fo"lKutrts"znl cc hi ee ekOtggsnkidy hini cna neea civo lh'
k = 8
n = 1

def encrypt(plain, k, n):
	parts = []
	for i in range(k):
		parts.append('')

	i = n-1
	d = 1
	for c in plain:
		parts[i] += c
		if i == k-1:
			d = -1
		elif i == 0:
			d = 1
		i += d

	crypt = ''
	for p in parts:
		crypt += p
	return crypt

def decrypt(ciphertext, k, n):
	parts = []
	for i in range(k):
		parts.append([])

	l = 0
	for j,p in enumerate(parts):
		i = n-1
		d = 1
		for c in ciphertext:
			if i == j:
				parts[j].append(ciphertext[l])
				l += 1
			if i == k-1:
				d = -1
			elif i == 0:
				d = 1
			i += d

	i = n-1
	d = 1
	plain = ''
	for c in ciphertext:
		plain += parts[i].pop(0)

		if i == k-1:
			d = -1
		elif i == 0:
			d = 1
		i += d

	return plain

print(decrypt(ciphertext, k, n))
