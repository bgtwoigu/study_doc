#!/usr/bin/python
# -*- coding: utf-8 -*-
#@Author: xmt
#@Date: 2015/7/21

import os, sys, xml.dom.minidom
import urllib2
import xlwt

#reload(sys)
#sys.setdefaultencoding('utf-8')

TEMP_PATH = ".temp"
FILE_BUGZILLA_INFO = 'bugzilla_info.xml'
FILE_EXCEL_BUGLIST = 'Q05_buglist.excel'
URL_Q05 = 'http://10.1.6.33/api_get_bug.php?product_name=ZX55Q05%EF%BC%88%E8%81%94%E9%80%9AA%E5%BA%93%EF%BC%89&assigned_to=\
dengzhilong@hipad.com,zouyuanfei@hipad.com,fengertong@hipad.com,liaoye@hipad.com,linxingyu@hipad.com,madejin@hipad.com,\
maxiaohui@hipad.com,wangkai@hipad.com,wangyongxian@hipad.com,xiangsheng@hipad.com,xiaotiaoyun@hipad.com,yuyuanjiang@hipad.com,\
zhangjiyou@hipad.com,zhangling@hipad.com,zhangyuan@hipad.com,zhouguangcheng@hipad.com'

def getFirstElement(parent, name):
    tags = parent.getElementsByTagName(name)
    if not tags or len(tags) < 1:
        return None
    return tags[0]

def getFirstElementData(parent, name):
    tag = getFirstElement(parent, name)
    if tag == None:
        return None
    node = tag.firstChild
    if not node or node.nodeType != node.TEXT_NODE:
        return None
    return node.data

class XmlInfoParser:
    def loadXml(self, pathname):
        f = open(pathname)
        self.Txt = f.read()
        f.close()
        return True

    def getInfoEntrys(self):
        infoEntrys = self.Txt.split('</bug>')
        return infoEntrys

class InfoEntry:
    def __init__(self, info):
        self.mInfo = info
    
    def getAttribute(self, tag):
        start = self.mInfo.find('<' + tag + '>')
        end = self.mInfo.find('</' + tag + '>')
        
        if start < 0 or end < 0:
            return ''        
        
        start =  start + len(tag) + 2
        return self.mInfo[start:end]
    
    def getBugId(self):
        return self.getAttribute("bug_id")

    def getAuthor(self):
        return self.getAttribute("bug_assigned_to")

    def getTitle(self):
        return self.getAttribute("bug_title")

    def getSeverity(self):
        return self.getAttribute("bug_severity")
    
    def getStatus(self):
        return self.getAttribute("bug_status")
    
    def getResolution(self):
        return self.getAttribute("bug_resolution")

    def getLongdescs(self):
        longdescs = self.getAttribute("bug_longdescs")
        if longdescs == '':
            return ''
      
        descs = ''
        for node in longdescs.split('</descs>')[::-1]:
            if node == '':
                continue
            
            start = node.find('<descs>')
            if start < 0:
                continue
            
            start += len('<descs>')            
            desc = node[start:].strip()
            
            if not desc == '':
                descs += desc + '\n'
        
        return descs

class BugInfoGenerator:
    def __init__(self):
        self.mBugInfoFile = os.path.join(TEMP_PATH, FILE_BUGZILLA_INFO)
        
        if not os.path.isdir(TEMP_PATH):
            os.makedirs(TEMP_PATH)

        print 'BugInfoGenerator init.'
        
    def genBugInfo(self):
        if self.genBugInfoFile() == False:
            print 'gen Buginfo error'
            return False
        
        parser = XmlInfoParser()
        if parser.loadXml(self.mBugInfoFile) == False:
            return False

        book = xlwt.Workbook(encoding='utf-8', style_compression=0)
        sheet = book.add_sheet(FILE_EXCEL_BUGLIST, cell_overwrite_ok=True)
        
        # gen title
        sheet.write(0, 0, 'BugId')
        sheet.write(0, 1, '责任人')
        sheet.write(0, 2, '优先级')
        sheet.write(0, 3, '状态')
        sheet.write(0, 4, '标题')
        sheet.write(0, 5, '解决方案')
        sheet.write(0, 6, '注释')        
        
        row = 1
        for node in parser.getInfoEntrys():
            entry = InfoEntry(node)
            bugId = entry.getBugId()
            author = entry.getAuthor().split('@')[0]
            title = entry.getTitle()
            serverity = entry.getSeverity()
            status = entry.getStatus()
            resolution = entry.getResolution()
            longdescs = entry.getLongdescs()
            #print bugId, author, title, serverity, status
            #print resolution
            #print longdescs
            sheet.write(row, 0, bugId)
            sheet.write(row, 1, author)
            sheet.write(row, 2, serverity)
            sheet.write(row, 3, status)
            sheet.write(row, 4, title)
            sheet.write(row, 5, resolution)
            sheet.write(row, 6, longdescs)
            row += 1
            #break
                
        book.save(FILE_EXCEL_BUGLIST + '.xls')    
        print 'done'
        return True

    def genBugInfoFile(self):
        #print URL_Q05
        data = urllib2.urlopen(URL_Q05).read()
        fp = open(self.mBugInfoFile, 'w')
        if not fp:
            return False
        
        fp.write(data)
        fp.close()
        return True

if __name__ == "__main__":
    # if len(sys.argv) < 6:
    #    print "Usage: %s project url start end filepath" % sys.argv[0]
    #    sys.exit(-1)

    # generator = BugInfoGenerator(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    generator = BugInfoGenerator()
    if generator.genBugInfo() == False:
        print "Error"
        sys.exit(-1)

    print "OK"
