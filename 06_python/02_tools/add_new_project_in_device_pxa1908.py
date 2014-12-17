#!/usr/bin/python

#@Date: 2014/12/17
#@Author: xmt

'''
add new project in marvell 1908.
'''
import os
import sys
import shutil
import re
import fileinput

def checkDirIsValid(source, target):
    if not os.path.exists(source) or not os.path.isdir(source):
        print '###Your input ***%s*** project is not present, please check it!###' % source
        return False

    if os.path.exists(target):
        print '###Your input ***%s*** project is exists, please change name!###' % target
        return False

    return True

def copyProject(source, target):
    shutil.copytree(source, target)

def rename(oldName, source, target):
    #print oldName, source, target
    if oldName.find(source) > 0 :
        newName = oldName.replace(source, target)
        #print newName, oldName
        os.rename(oldName, newName)

def replaceInFile(filePath, source, target):
    for line in fileinput.input(filePath, inplace=True):
        if re.search(source, line):
            line = line.replace(source, target)
        print line,

def replaceProjectName(source, target):
    for dirpath, dirnames, filenames in os.walk(target):
        for eachFile in filenames:
            filePath = os.path.join(dirpath, eachFile)
            #print 'filePath = %s' % filePath
            replaceInFile(filePath, source, target)
            rename(filePath, source, target)
            
        for eachDir in dirnames:
            dirFullPath = os.path.join(dirpath, eachDir)
            rename(dirFullPath, source, target)

def main(source, target):
    #print source, target
    
    if not checkDirIsValid(source, target):
        sys.exit(-1)

    copyProject(source, target)
    
    replaceProjectName(source, target)    
    print 'It is OK!'

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print 'Usage: %s source target' % sys.argv[0]
        sys.exit(-1)
    main(sys.argv[1], sys.argv[2])

