/*
 *      * specific ld opts: -lcrypt
 *           */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <crypt.h>
#include <sys/types.h>
#include <unistd.h>

int main (int argc, char *argv[]) {
	if (argc != 2)
		return 0;

	printf("'%s'\n",crypt(argv[1], "$1$awesome"));

	return 0;
}
