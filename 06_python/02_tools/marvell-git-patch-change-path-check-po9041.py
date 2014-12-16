#!/usr/bin/python
import string
import os
import struct
import re
import fileinput
import fnmatch
import commands

DIR = 'po9041_20141202/'
EXT = '*.patch'
ERROR_PROJECT_NAME = 'pq9041'
FIXED_PROJECT_NAME = 'po9041'

def walkDir(directory, ext='*.*', topdown=True):
    fileArray = []
    for root, dirs, files in os.walk(directory, topdown):
        for name in files:
            if fnmatch.fnmatch(name, ext):
                #print root, name
                fixedPath = root[len(DIR):]
                #print fixedPath
                fileArray.append([fixedPath, os.path.abspath(os.path.join(root, name))])
    return fileArray

def replaceInFile(filename, strFrom, strTo):
    for line in fileinput.input(filename, inplace=True):
        if re.search(strFrom, line):
            line = line.replace(strFrom, strTo)
        print line,

def check_path(fixedPath):
    if not fixedPath[-1] == '/':
        fixedPath += '/'
    return fixedPath

def get_git_change_files_list(patchName):
    git_cmd = 'git apply --numstat %s' % patchName
    output = commands.getoutput(git_cmd)
    return output.splitlines()

def main():
    fileList = walkDir(DIR, EXT)

    for fixedPath, filePath in fileList:
        fileName = os.path.basename(filePath)
        fixedPath = check_path(fixedPath)
        #print fixedPath, fileName

        git_changeList = get_git_change_files_list(filePath)
        for item in git_changeList:
            list = item.split('\t')
            #print list
            oldStr = list[-1]
            newStr = fixedPath + oldStr
            #print oldStr, newStr
            #print filePath
            replaceInFile(filePath, oldStr, newStr)
            replaceInFile(filePath, ERROR_PROJECT_NAME, FIXED_PROJECT_NAME)

if __name__ == '__main__':
    main()
