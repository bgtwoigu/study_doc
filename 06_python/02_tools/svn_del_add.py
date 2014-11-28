#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import commands
import sys
import string
import urllib

is_effective = True #True False
#0 is changelist filename.
IGNORE_FILENAME = ('changeList.txt', 'gen_patch_directory.py', 'gen_pac.sh')
#
MOD = 100

def get_output(cmd):
    system = sys.platform
    if system == 'win32':
        #windowns
        r = os.popen(cmd)
        output = r.read()
        r.close()
    else:
        #linux
        status, output = commands.getstatusoutput(cmd)
        #print status
    return output

def do_svn_op(cmd_str, op_list):
    blankStr = ' '
    svn_cmd = cmd_str + ' %s' % blankStr.join(op_list)
    commands.getoutput(svn_cmd)
    
def prase_list(cmd_str, files_list):
    length = len(files_list)
    count = length / MOD

    i = start = end = 0
    while count > i:
        start = i * MOD
        end = (i + 1) * MOD
        list = files_list[start:end]
        do_svn_op(cmd_str, list)
        i += 1
    else:
        list = files_list[end:-1]
        do_svn_op(cmd_str, list)

def svn_add_files(add_files_list):
    #blankStr = ' '
    #svn_cmd = 'svn add --force --no-ignore %s' % blankStr.join(add_files_list)
    #commands.getoutput(svn_cmd)
    prase_list('svn add --force --no-ignore ', add_files_list)
    
def svn_delete_files(delete_files_list):
    #blankStr = ' '
    #svn_cmd = 'svn delete --force %s' % blankStr.join(delete_files_list)
    #commands.getoutput(svn_cmd)
    prase_list('svn delete --force ', delete_files_list)

def gen_changeListFile(changeList):
    toast = '#################changelist#################\r\n'
    # decode the URL that contains Chinese characters
    de = urllib.unquote
    changeList = de(changeList)
    # print changeList
    changeList = changeList.replace('\n', '\r\n') + '\r\n'
    readme = toast + changeList + toast
    cmd = 'echo "%s" > %s' % (readme, IGNORE_FILENAME[0])
    # print cmd
    os.system(cmd)

def gen_svn_status_list():
    svn_cmd = 'svn st --no-ignore'
    output = get_output(svn_cmd)
    gen_changeListFile(output)    
    changeList = output.splitlines()
            
    add_files_list = []
    delete_files_list = []
    ignoreFilesList = getIgnoreFilesList()
    
    for item in changeList:
        #print item
        fileList = item.split(' ')

        #step 1: is it need to ignore?
        ignore = False
        for ignoreFileName in ignoreFilesList:
            if ignoreFileName == fileList[-1]:
                ignore = True
                break
        
        #step 2: add this file to list
        if not ignore:
            if fileList[0] == '?' or fileList[0] == 'I': 
                add_files_list.append(fileList[-1])
            elif fileList[0] == '!':
                delete_files_list.append(fileList[-1])
    
    return [add_files_list, delete_files_list]
        
def getIgnoreFilesList():
    realpath = os.path.realpath(__file__)
    currentPyFileName = os.path.basename(realpath)
    #print currentPyFileName
    
    ignoreFilesList = list(IGNORE_FILENAME)
    ignoreFilesList.append(currentPyFileName)
    return ignoreFilesList

def main():
    print '########BEGINNING...########'
    print '###01_gen_svn_status_list###'
    #0 is add files, 1 is delete files
    add_delete_files_list = gen_svn_status_list()
    
    print '###02_svn_add_files#########'
    svn_add_files(add_delete_files_list[0])

    print '###03_svn_delete_files######'
    svn_delete_files(add_delete_files_list[1])
    print '############OK!!!###########'

if __name__=='__main__':
    main()


