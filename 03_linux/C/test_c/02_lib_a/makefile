helloliba: helloliba.c libtest.a
	gcc helloliba.c -o helloliba libtest.a

libtest.a: test.o
	ar rc libtest.a test.o

test.o: test.c test.h
	gcc -c test.c

clean:
	rm -rf libtest.a helloliba
	rm -rf *.o
