#!/usr/bin/python
import time

print time.time()
print time.localtime(time.time())
print time.strftime('%Y-%m-%d',time.localtime(time.time()))

print 

myTuple = time.localtime(time.time())
print myTuple[0], myTuple[1], myTuple[2]
print myTuple.tm_year, myTuple.tm_mon, myTuple.tm_mday

