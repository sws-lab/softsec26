#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>
#include <assert.h>

static char BUFFER[1024] = {0};
static char ALPHABET[] = "0123456789";
static char ALPHABET2[] = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";

int main(int argc, const char **argv) {
	char chr;
	size_t i, count;
	int offset;
	
	if (argc < 2) {
		printf("Usage: %s LENGTH [OFFSET]\n", argv[0]);
		return -1;
	}
	count = strtoul(argv[1], NULL, 10);
	if (count >= sizeof(BUFFER)) {
		printf("Buffer overflow with %zu\n", count);
		return -1;
	}
	if (argc >= 3) {
		offset = strtod(argv[2], NULL);
	} else {
		offset = 0;
	}
	for (i = 0; i < count; i++) {
		if (i % 2 == 0) {
			size_t alphabetIdx = rand() % (sizeof(ALPHABET) - 1);
			chr = ALPHABET[alphabetIdx];
			BUFFER[i] = chr;
		} else {
			size_t alphabetIdx = rand() % (sizeof(ALPHABET2) - 1);
			chr = ALPHABET2[alphabetIdx];
			BUFFER[i] = chr;
		}
		BUFFER[i] += offset;
	}
	printf("%s\n", BUFFER);
	return 0;
}
