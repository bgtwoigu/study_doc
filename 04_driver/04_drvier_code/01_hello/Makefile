obj-m := hello.o 
KERNELDR := /home/xumingtao/share/git/linux_kernel/kernel_2.6/linux-2.6.34.14 
PWD := $(shell pwd)
modules: 
	$(MAKE) -C $(KERNELDR) M=$(PWD) modules
modules_install:
	$(MAKE) -C $(KERNELDR) M=$(PWD) modules_install
clean:
	rm -rf *.o *~core .depend .*.cmd *.ko *.mod.c .tmp_versions
