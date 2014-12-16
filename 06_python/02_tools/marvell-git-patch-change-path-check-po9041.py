#!/usr/bin/python
# -*- coding: utf-8 -*-
#@File: marvell-git-patch-change-path-check-po9041.py
#@Author: xumingtao
'''
Change the filepath of patch from Marvell.
The project name is po9041 not pq9041. Check it!
Usage: marvell-git-patch-change-path-check-po9041 [option] arg1, arg2 ...
    -d arg1 is patch directory name, structure like these:
        9041_20141202
        ├── bootable
        │   └── bootloader
        │       ├── obm
        │       │   ├── 0001-OBM-enlarge-timeout-for-SWDConsole-download.patch
        │       └── uboot
        │           ├── 0001-Add-PO9041-board-file-support-in-uboot.patch
        
       arg2 is output directory name, like these:
        patch_all/
        ├── 0001-OBM-enlarge-timeout-for-SWDConsole-download.patch
        ├── 0001-Add-PO9041-board-file-support-in-uboot.patch

    -f arg1 is patch filename,like this:
         0001-OBM-enlarge-timeout-for-SWDConsole-download.patch
       arg2 is fixed path. we view this patch, this file Common/Download/ProtocolManager.h is in bootable/bootlaoder/obm.
        so the fixed path is bootable/bootlaoder/obm

./marvell-git-patch-change-path-check-po9041.py -d 9041_20141202 patch_all
./marvell-git-patch-change-path-check-po9041.py -f 0001-OBM-enlarge-timeout-for-SWDConsole-download.patch bootable/bootlaoder/obm
'''

import string
import os
import struct
import re
import fileinput
import fnmatch
import commands
import getopt
import sys

EXT = '*.patch'
ERROR_PROJECT_NAME = 'pq9041'
FIXED_PROJECT_NAME = 'po9041'

def check_path(fixedPath):
    if not fixedPath[-1] == '/':
        fixedPath += '/'
    return fixedPath

def get_git_change_files_list(patchName):
    git_cmd = 'git apply --numstat %s' % patchName
    output = commands.getoutput(git_cmd)
    return output.splitlines()

def replaceInFile(filename, strFrom, strTo):
    for line in fileinput.input(filename, inplace=True):
        if re.search(strFrom, line):
            line = line.replace(strFrom, strTo)
        print line,
        
def parse_file(filePath, fixedPath):
    git_changeList = get_git_change_files_list(filePath)
    for item in git_changeList:
        list = item.split('\t')
        #print list
        fixedPath = check_path(fixedPath)
        oldStr = list[-1]
        newStr = fixedPath + oldStr
        #print oldStr, newStr
        #print filePath
        replaceInFile(filePath, oldStr, newStr)
        replaceInFile(filePath, ERROR_PROJECT_NAME, FIXED_PROJECT_NAME)    

def do_file_parse(OrigPatchName, fixedPath):
    #step 0: remove '/'
    if OrigPatchName[-1] == '/':
        OrigPatchName = OrigPatchName[:-1]
    
    #step 1: check file path
    newPatchName = 'hipad-' + OrigPatchName
    if not os.path.exists(OrigPatchName):
        print '!!!Error!!!, please check your input ###%s### does not exist!' % OrigPatchName
        return None

    if os.path.exists(newPatchName):
        print '!!!Error!!!, please check ###%s### is exist and change your new patch name!' % newPatchName
        return None

    #step 2: copy orig file to new file
    open(newPatchName, 'wb').write(open(OrigPatchName, 'rb').read())

    #step 3: parse chang list files
    parse_file(OrigPatchName, fixedPath)

def walkDir(origDir, targetDir, ext='*.*', topdown=True):
    fileArray = []
    for root, dirs, files in os.walk(origDir, topdown):
        for name in files:
            if fnmatch.fnmatch(name, ext):
                #print root, name
                fixedPath = root[len(origDir):]
                targetFilePath = targetDir + name
                #print fixedPath, targetFilePath
                fileArray.append([fixedPath, targetFilePath])
    return fileArray

def copy_origDir_patches(origDir, targetDir):
    #step 1: check dir
    if not os.path.exists(targetDir):
        os.makedirs(targetDir)
    else:
        print '!!!Error!!!, please check ###%s### dir is existing and change your directory name!' % newPatchName
        return None

    #step 2: copy files
    sh_cmd = 'cp -rf `find %s -iname \"*.patch\"` %s' % (origDir, targetDir)
    print sh_cmd
    commands.getoutput(sh_cmd)
    return 0

def do_dir_parse(origDir, targetDir):
    #step 1: copy files
    result = copy_origDir_patches(origDir, targetDir)
    if result == None:
        return None
    
    #step 2: parse patch name and fixed path
    fileList = walkDir(origDir, targetDir, EXT)

    #step 3: parse file
    for fixedPath, filePath in fileList:
        #print fixedPath, filePath
        parse_file(filePath, fixedPath)

def Usage():
    print __doc__

def main(argv):
    arg1 = arg2 = None
    options = ['-d', '-f']
    
    print argv

    if not argv[1] in str(options):
        Usage()
        return

    arg1 = check_path(argv[2]);
    arg2 = check_path(argv[3]);
    
    print arg1, arg2

    if argv[1] == '-d':
        do_dir_parse(arg1, arg2)
    elif argv[1] == '-f':
        do_file_parse(arg1, arg2)
    else:
        Usage()

'''
    try:
        opts, args = getopt.getopt(argv[1:], 'df', ['arg1=', 'arg2='])
        print opts, args
    except getopt.GetoptError, err:
        print str(err)
        Usage()
        sys.exit(2)
'''


#    for o, a in opts:
#        print o, a

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print 'Usage: %s [option] arg1 arg2' % sys.argv[0]
        sys.exit(-1)
            
    main(sys.argv)
