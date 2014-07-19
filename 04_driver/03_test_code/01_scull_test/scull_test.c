/*
 * scull_test.c
 *
 *  Created on: Jul 11, 2014
 *      Author: xumingtao
 */

#include <unistd.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <stdlib.h>
#include <stdio.h>

int main() {
	char buffer1[20] = { 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
			16, 17, 18, 19 };
	char buffer2[20] = { 0 };
	int sculltest, code, i;

	sculltest = open("/dev/scullxmt", O_WRONLY);

	for (i = 20; i > 0; i -= code) {
		if ((code = write(sculltest, &buffer1[20 - i], i)) != i)
			printf("write error! code = %d\n", code);
		else
			printf("read ok! code = %d\n", code);

	}

	for (i = 0; i < 20; i += 5) {
		printf(
				"buf[%d] = %d, buf[%d] = %d, buf[%d] = %d, buf[%d] = %d, buf[%d] = %d\n",
				i, buffer2[i], i + 1, buffer2[i + 1], i + 2, buffer2[i + 2],
				i + 3, buffer2[i + 3], i + 4, buffer2[i + 4]);
	}

	printf("OK!\n");

	close(sculltest);
	exit(0);
}
