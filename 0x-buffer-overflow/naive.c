#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <stdbool.h>

#define BUF_SIZE 8

static __attribute__((noinline)) bool read_password(FILE *fp, char *ptr) {
    int c;
    for (c = fgetc(fp); c != '\n' && c != EOF; c = fgetc(fp)) {
        *(ptr++) = c;
    }
    *ptr = '\0';
    return c == EOF;
}

int main(int argc, const char **argv) {
    char input[BUF_SIZE];
    char expected[BUF_SIZE];

    const char *passwd_filepath = argc >= 2
        ? argv[1]
        : "password.txt";

    FILE *passwd = fopen(passwd_filepath, "r");
    if (passwd == NULL) {
        perror("Failed to open password file");
        return EXIT_FAILURE;
    }
    read_password(passwd, expected);
    fclose(passwd);

    for (int run = true; run;) {
        printf("Password: ");
        run = !read_password(stdin, input);

        if (strncmp(input, expected, BUF_SIZE) == 0) {
            printf("Secret!\n");
            run = false;
        } else if (*input) {
            printf("Access denied!\n");
        }
    }
    return EXIT_SUCCESS;
}
