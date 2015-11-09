#!/usr/bin/python
#
# @Author: xmt
# @Date: 2015/05/04

import os
import commands
import sys
import xlwt
import xml.dom.minidom
from xml.dom.minidom import parse
from xml.dom.minicompat import NodeList

SHELL_CMD_FIND = 'find device/qcom/ packages/ frameworks/ vendor/ -iname strings.xml'
CN_EN_FR_VALUES = ['/values/', '/values-zh-rCN/', '/values-fr/']
#WORK_DIR_PATH = '/home/xumingtao/share/Qualcomm/ZTE/ZC2501/ZTE_INTERNAL_MP/android'


TAG_STRING = 'string'
TAG_STRING_ARRAY = 'string-array'
TAG_PLURALS = 'plurals'
TAG_ITEM = 'item'
ATTR_NAME = 'name'
ATTR_QUANTITY = 'quantity'

SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))

reload(sys)
sys.setdefaultencoding('utf-8')

class ParseStringXml:
        
    def parse(self, WORK_DIR_PATH, path, index, sheetValues):
        #print path
        path = WORK_DIR_PATH + '/' + path
        
        DOMTree = xml.dom.minidom.parse(path)
        resource = DOMTree.documentElement    
        all_strings = resource.getElementsByTagName('*')
        
        first_import = (len(sheetValues) < 1)
        #print first_import
        if first_import:
            filepath_key, rows = self.get_rows_info('0', '', path[len(WORK_DIR_PATH) + 1:], '', ['', '', ''])
            sheetValues[filepath_key] = rows      
            title_key, rows = self.get_rows_info('0', 'TYPE', 'KEY', 'ORDER', ['CONTENT-EN', 'CONTENT-CN', 'CONTENT-FR'])            
            sheetValues[title_key] = rows            
            
        lineNo = 1
        
        for name in all_strings:
            
            if not name.hasAttribute(ATTR_NAME):
                continue
            
            rows = []
            contents = [None, None, None]
            typeTag = name.nodeName
            key = name.getAttribute(ATTR_NAME)
            
            if typeTag == TAG_STRING:
                self.update_sheetValues(sheetValues, index, first_import, name.childNodes, lineNo, typeTag, key)
                lineNo += 1 
                    
            elif typeTag == TAG_STRING_ARRAY:
                #print TAG_STRING_ARRAY
                i = 0
                for node in name.getElementsByTagName(TAG_ITEM):           
                    self.update_sheetValues(sheetValues, index, first_import, node.childNodes, lineNo, typeTag, key, i)
                    lineNo += 1 
                    i += 1
            
            elif typeTag == TAG_PLURALS:
                #print TAG_PLURALS
                for item_node in name.getElementsByTagName(TAG_ITEM):
                    self.update_sheetValues(sheetValues, index, first_import, item_node.childNodes, lineNo, typeTag, key, item_node.getAttribute(ATTR_QUANTITY))
                    lineNo += 1                    
            
            
        #for item in sheet_values:
        #    print item, sheet_values[item]
        return sheetValues
    
    def update_sheetValues(self, sheetValues, index, first_import, NodeList, lineNo, typeTag, key, order=None):
        contents = [None, None, None]
        values = self.get_values_from_xliff(NodeList)
        contents[index] = values
        dict_key, rows = self.get_rows_info(lineNo, typeTag, key, order, contents)
        #print rows
        if not first_import:
            for temp_dict_key in sheetValues:
                if temp_dict_key.find(dict_key[5:]) > 0:
                    dict_key = temp_dict_key
                    break
                
            if sheetValues.has_key(dict_key):
                rows = sheetValues[dict_key]
                rows[3 + index] = values
        sheetValues[dict_key] = rows        
    
    def get_values_from_xliff(self, NodeList):
        values = ''
        for node in NodeList:
            text = node.nodeValue
            if text == None:
                text = '%s'
            values += text
        
        if values == '%s':
            values = None

        return values
        
    def get_rows_info(self, lineNo, type, key, order, contents):
        rows = []
        dict_key = str(str(lineNo).zfill(5)  +  str(type) + str(key) + str(order))
        #dict_key = str(str(type) + str(key) + str(order))
        #rows.append(dict_key)
        rows.append(str(type))
        rows.append(str(key))
        rows.append(str(order))
        rows.append(str(contents[0]))
        rows.append(str(contents[1]))
        rows.append(str(contents[2]))
        #print dict_key
        return [dict_key, rows]    
    
def get_find_result(WORK_DIR_PATH):
    os.chdir(WORK_DIR_PATH)
    find_result = commands.getoutput(SHELL_CMD_FIND)
    os.chdir(SCRIPT_PATH)
    return find_result.splitlines();

def get_cn_en_fr_filelist(WORK_DIR_PATH, excel_filename):
    cn_en_fr_dict = {}
    find_result = get_find_result(WORK_DIR_PATH)
    for path in find_result:
        #print path
        i = 0
        for value in CN_EN_FR_VALUES:
            if path.find(value) > 0:
                key = parse_key_from_path(path)
                if cn_en_fr_dict.has_key(key):
                    cn_en_fr_dict[key][i] = path
                else:
                    values = [None, None, None]
                    values[i] = path
                    cn_en_fr_dict[key] = values
                break;
            i += 1
    
    #print cn_en_fr_dict
    book = xlwt.Workbook(encoding='utf-8', style_compression=0)
    
    #cn_en_fr_dict = sorted(cn_en_fr_dict.iteritems(), key = lambda asd:asd[1])
    
    #for key in cn_en_fr_dict:
    for item_dict in sorted(cn_en_fr_dict.iteritems(), key = lambda asd:asd[1]):
        key = item_dict[0]
        #print key
        
        sheet = book.add_sheet(key, cell_overwrite_ok=True)
        pathList = cn_en_fr_dict[key]
        values = [None, None, None, None, None, None]
        
        stringParse = ParseStringXml()
        sheetValues = {}
        index = 0
        for path in pathList:
            if not path == None:
                #print path                 
                stringParse.parse(WORK_DIR_PATH, path, index, sheetValues)
                #print sheetValues
                #print len(sheetValues), len(sheetValues[0])
            #else:
            #    print '1'
            index += 1
        
        row = 0
        #for item in sheetValues:
        for item_sheet in sorted(sheetValues.iteritems(), key = lambda asd:asd[1]):
            sheet_key = item_sheet[0]

            content_values = sheetValues[sheet_key][-3:]
            #print content_values
            if (not content_values[0] == 'None') and (not content_values[2] == 'None') and (row > 1):
                continue
            
            #print sheet_key
            column = 0
            #print item, sheetValues[item]
            for info in sheetValues[sheet_key]:
                if info == 'None':
                    info = ''
                    
                sheet.write(row, column, info)
                column += 1
            row += 1
        
        #break
    book.save(excel_filename + '.xls')

def parse_key_from_path(path):
    key = ''
    index = path.find('/res/values')
    keylist = path[:index].split('/')
    for item in keylist[:-3]:
        key += item[0]
    
    for item in keylist[-3:-1]:
        key += item[:2]

    key = key + '_' + keylist[-1]
    #print key, path

    if len(key) > 31:
        key = key[0:31]

    return key

def main(WORK_DIR_PATH, excel_filename):
    print WORK_DIR_PATH, SCRIPT_PATH
    get_cn_en_fr_filelist(WORK_DIR_PATH, excel_filename)
    

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print 'Usage: %s android_code_path filename' % sys.argv[0]
        sys.exit(-1)
    main(sys.argv[1], sys.argv[2])
