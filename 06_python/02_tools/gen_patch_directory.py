#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import commands
import sys
import urllib

PATCH_TYPE = ('before', 'after')
FILE_TYPE = ('file', 'directory')
CHANGE_TYPE = ('M', 'A', 'D')
    
class PatchGenerator:
    def __init__(self, url, start, end, patchName):
        self.mUrl = url
        self.mStartRevision = int(start)
        self.mLastRevistion = int(end)
        self.mPatchName = patchName

        if self.mStartRevision > self.mLastRevistion:
            temp = self.mStartRevision
            self.mStartRevision = self.mLastRevistion
            self.mLastRevistion = temp
        
        #url end with '/'
        if self.mUrl[-1] != '/':
            self.mUrl = self.mUrl + '/'

    def getChangeList(self):
        svn_changeList_cmd = 'svn diff -r %d:%d --summarize %s' % (self.mStartRevision, self.mLastRevistion, self.mUrl)
        #print svn_changeList_cmd
        status, output = commands.getstatusoutput(svn_changeList_cmd)
        #print status
        #print output
        if status != 0:
            print output
            return None
        else:
            self.genReadme(output)
            return output.splitlines()
            
    def getFileType(self, svn_vevision, http_full_path):
        svn_cmd = 'svn info -r %d %s' % (svn_vevision, http_full_path) + ' | grep "Node Kind"'
        output = commands.getoutput(svn_cmd)
        type = output.split(':')[-1].strip()
        if type == FILE_TYPE[1]:
            #directory
            return FILE_TYPE[1]
        else:
            #file
            return FILE_TYPE[0]
        
    def genSvnFileAndDir(self, svn_vevision, http_full_path, patch_type):
        filePath = self.mPatchName + '/' + patch_type + '/' + http_full_path[len(self.mUrl):]
        file_tpye = self.getFileType(svn_vevision, http_full_path)
        if file_tpye == FILE_TYPE[1]:
            if not os.path.exists(filePath):
                os.makedirs(filePath)
        else:
            folderPath = os.path.dirname(filePath)
            if not os.path.exists(folderPath):
                os.makedirs(folderPath)
            svn_cmd = 'svn export -r %d %s %s' % (svn_vevision, http_full_path, folderPath)
            commands.getoutput(svn_cmd)
        
    def genBeforeDir(self, http_full_path):
        self.genSvnFileAndDir(self.mStartRevision, http_full_path, PATCH_TYPE[0])
        
    def genAfterDir(self, http_full_path):
        self.genSvnFileAndDir(self.mLastRevistion, http_full_path, PATCH_TYPE[1])
        
    def getValidNameAndPath(self, http_full_path):
        status = -1
        basename = os.path.basename(http_full_path)        
        validHttpPath = http_full_path
        while status != 0:
            svn_cmd = 'svn info -r %d %s' % (self.mStartRevision, validHttpPath)
            status, output = commands.getstatusoutput(svn_cmd)
            #print status
            if status != 0:
                basename = os.path.basename(validHttpPath)
                validHttpPath = os.path.dirname(validHttpPath)
                #print validHttpPath
                #print basename
        
        return [basename, validHttpPath]
        
    def genDeleteSvnFileAndDir(self, http_full_path):
        nameAndPath = self.getValidNameAndPath(http_full_path)
        deleteFolderPath = self.mPatchName + '/' + PATCH_TYPE[0] + '/' + nameAndPath[1][len(self.mUrl):]
        #print deleteFolderPath
        if not os.path.exists(deleteFolderPath):
            #step 1: check out empty folder.
            svn_cmd = 'svn co -r %d %s --depth empty %s' % (self.mStartRevision, nameAndPath[1], deleteFolderPath)
            commands.getoutput(svn_cmd)
            
            #step 2: update folder and file.
            deleteDirName = deleteFolderPath + '/' + nameAndPath[0]
            #print deleteDirName
            svn_cmd = 'svn up -r %d %s --set-depth infinity' % (self.mStartRevision, deleteDirName)
            commands.getoutput(svn_cmd)
            
            #step 3: delete .svn folder
            delete_svn_cmd = 'find %s -iname .svn | xargs rm -rf' % deleteFolderPath
            commands.getoutput(delete_svn_cmd)
    
    def genDir(self, changType, http_full_path):
        #modify 'M' 
        if changType == CHANGE_TYPE[0]:
            self.genBeforeDir(http_full_path)
            self.genAfterDir(http_full_path)
        #add 'A'
        elif changType == CHANGE_TYPE[1]:
            self.genAfterDir(http_full_path)
        #delete 'D'
        elif changType == CHANGE_TYPE[2]:
            self.genDeleteSvnFileAndDir(http_full_path)
            
    def genPatchFile(self):
        patchFilePath = self.mPatchName + '/' + self.mPatchName + '.patch'
        svn_cmd = 'svn diff -r %d:%d --force %s > %s' %(self.mStartRevision, self.mLastRevistion, self.mUrl, patchFilePath)
        #print svn_cmd
        os.system(svn_cmd)
        
    def genReadme(self, changeList):
        toast = '#################changelist#################\r\n'
        #decode the URL that contains Chinese characters
        de = urllib.unquote
        changeList = de(changeList)
        #print changeList
        changeList = changeList.replace('\n', '\r\n') + '\r\n'
        readme = toast + changeList + toast
        cmd = 'echo "%s" > %s' %(readme, self.mPatchName + '/readme.txt')
        #print cmd
        os.system(cmd)
                
    def genPatchDirectory(self):
        print 'begining...'
        
        if not os.path.exists(self.mPatchName):
            os.makedirs(self.mPatchName)
        else:
            print "Patch Name: ***%s*** is exists, please change it!\n" % self.mPatchName
            return False
        
        svn_changeList = self.getChangeList()        
        if svn_changeList == None:
            return False
        
        for item in svn_changeList:
            list = item.split(' ')
            #print list
            self.genDir(list[0], list[-1])
        
        self.genPatchFile()
        
        return True
        
if __name__ == "__main__":
    if len(sys.argv) < 5:
        print 'Usage: %s url start end patchname' % sys.argv[0]
        sys.exit(-1)

    generator = PatchGenerator(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    if generator.genPatchDirectory() == False:
        print "Error"
        sys.exit(-1)

    print "OK"

