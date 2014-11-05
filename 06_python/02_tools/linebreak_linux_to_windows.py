#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys

class LineBreakConvertor:
    def __init__(self, oldFile, newFile):
        self.mOldFile = oldFile
        self.mNewFile = newFile
                
    def convertLinuxIntoWindows(self):
        print 'begining...'
        
        if os.path.exists(self.mNewFile):
            print "File Name: ***%s*** is exists, please change it!\n" % self.mNewFile
            return False
        
        #step 1: read text
        oldFp = open(self.mOldFile)
        if not oldFp:
            return False
        all_the_text = oldFp.read()
        oldFp.close()
        
        #step 2: convert '\n' into '\r\n'
        all_the_text = all_the_text.replace('\n', '\r\n')
        
        #step 3: save to new file
        newFp = open(self.mNewFile, 'w')
        if not newFp:
            return False
        newFp.write(all_the_text)
        newFp.close()
        
        return True
        
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print 'Usage: %s url oldfile newfile' % sys.argv[0]
        sys.exit(-1)

    convertor = LineBreakConvertor(sys.argv[1], sys.argv[2])
    if convertor.convertLinuxIntoWindows() == False:
        print "Error"
        sys.exit(-1)

    print "OK"

