#################################
#libtest.so之前需要指定当前路径
#否则会提示无法找到so文件
#################################
hellolibso: libtest.so hellolibso.c
	gcc hellolibso.c -o hellolibso ./libtest.so

libtest.so: test.c test.h
	gcc -shared -fPIC -o libtest.so test.c

clean:
	rm -rf hellolibso
	rm -rf *.so
