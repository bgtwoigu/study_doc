all: Stack Queue

Stack: LinkStack.c TestStack.c
	gcc -o Stack TestStack.c LinkStack.c -g

Queue: CycleQueue.c TestQueue.c
	gcc -o Queue CycleQueue.c TestQueue.c -g

clean:
	rm -rf Stack Queue
	rm -rf *.o
