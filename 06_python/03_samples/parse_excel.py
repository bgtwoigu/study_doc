#!/usr/bin/python
# -*- coding:utf-8 -*-

import sys
import csv

PROJECT_LIST = ['lj50v00', 'zq9077', 'po9041', 'yo9083']
HIPAD_LIST = ['xumingtao', 'wuzhenyuan', 'liuyanfeng', 'zouyuanfei', 'dengzhilong', 'shenyuanqing', 'hesiming', 'hanhao', 'zhuyifei', 'zhangling', 'luoruifeng', 'zhouguangcheng', 'xiaotiaoyun', 'wangyongxian', 'zhangjiyou', 'xiangsheng', 'chenzili', 'shenyong', 'liaoye']

def getProjectAndHipad(title):
    curProj = 'N/A'
    curHipad = 'N/A'

    for project in PROJECT_LIST:
        if title.upper().find(project.upper()) > 0:
            if project == 'lj50v00' or project == 'zq9077':
                curProj = 'lj50v00'
            elif project == 'po9041' or project == 'yo9083':
                curProj = 'yo9083'            

    for hipad in HIPAD_LIST:
        if title.upper().find(hipad.upper()) > 0:
            curHipad = hipad

    return [curProj, curHipad]

def parse_excel(filename):
    newFilename = 'parse_' + filename
    print 'filename: %s, newFilename: %s' % (filename, newFilename)
    parseLists = []

    with open(filename, 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            #print row[1]
            project, hipad = getProjectAndHipad(row[1])
            row.append(project)
            row.append(hipad)
            #print row
            parseLists.append(row)

    with open(newFilename, 'wb') as csvfile:
        spamwriter = csv.writer(csvfile,dialect='excel')
        for row in parseLists:
            spamwriter.writerow(row)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print '%s :please input filename!' % sys.argv[0]
        sys.exit(-1)

    parse_excel(sys.argv[1])
    
