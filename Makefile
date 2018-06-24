all: test

test:
	gcc test.c -o test -lm -Wall -Wextra

clean:
	rm test

run:
	clean
	test
