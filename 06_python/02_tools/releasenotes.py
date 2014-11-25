#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, sys, re, xml.dom.minidom
import urllib2

TEMP_PATH = ".temp"
FILENAME_SVN_LOG = "svn_log.xml"
BUGZILLA_NOT_FIX_INFO = 'bugzilla_not_fix_info.xml'
BUGZILLA_FIXED_INFO = 'bugzilla_fixed_info.xml'
BUGZILLA_STATUS = ('UNCONFIRMED', 'NEW', 'ASSIGNED', 'REOPENED', 'RESOLVED', 'CLOSED')
BUGZILLA_RESOLUTION = ('FIXED', 'Not%20a%bug', 'Won\'t%20Fix', 'DUPLICATE', 'Unable%20to%20Reproduce', 'By%20Design', 'Postponed')

reload(sys)
sys.setdefaultencoding('utf-8')

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

class SvnLogParser:
	def loadXml(self, pathname):
		dom = xml.dom.minidom.parse(pathname)
		if dom == None:
			return False

		self.mRootElement = dom.documentElement
		return True

	def getLogEntrys(self):
		return self.mRootElement.getElementsByTagName("logentry")

class SvnLogEntry:
	def __init__(self, element):
		self.mRootElement = element

	def getRevesion(self):
		return self.mRootElement.getAttribute("revision")

	def getAuthor(self):
		return getFirstElementData(self.mRootElement, "author")

	def getDate(self):
		return getFirstElementData(self.mRootElement, "date")

	def getMessage(self):
		return getFirstElementData(self.mRootElement, "msg")

class BugzillaInfo:	
	def __init__(self, project):
		self.mNotFixFile = os.path.join(TEMP_PATH, BUGZILLA_NOT_FIX_INFO)
		self.mFixedFile = os.path.join(TEMP_PATH, BUGZILLA_FIXED_INFO)
		#self.mProject = project
		self.mNotFixUrl = ('http://10.1.1.252/api_get_bug.php?product_name=%s&status[]=%s&resolution[]=%s&resolution[]=%s&resolution[]=%s&resolution[]=%s'
						% (project, BUGZILLA_STATUS[4], BUGZILLA_RESOLUTION[1], BUGZILLA_RESOLUTION[2], BUGZILLA_RESOLUTION[4], BUGZILLA_RESOLUTION[5]))
		self.mFixedUrl = ('http://10.1.1.252/api_get_bug.php?product_name=%s&status[]=%s&resolution[]=%s&resolution[]=%s'
						% (project, BUGZILLA_STATUS[4], BUGZILLA_RESOLUTION[0], BUGZILLA_RESOLUTION[3]))
		
	'''
	def genNotFixInfoFile(self):
		#url = 'http://10.1.1.252/api_get_unfix_bug.php?product_name=' + self.mProject
		url = 'http://10.1.1.252/api_get_bug.php?product_name=ho9021&status[]=RESOLVED&resolution[]=Not\%20a\%20Bug&resolution[]=Won\'t\%20Fix' 
		url = self.mNotFixUrl
		data = urllib2.urlopen(url).read()
		fp = open(self.mInfoFile, 'w')
		if not fp:
			return False
		
		fp.write(data)
		fp.close()
		return True
	'''
	
	def genInfoEntrys(self, infoFileName):
		dom = xml.dom.minidom.parse(infoFileName)
		if dom == None:
			return None
		
		return dom.documentElement.getElementsByTagName("bug")

	def genBugInfoFile(self, url, infoFileName):
		#url = 'http://10.1.1.252/api_get_unfix_bug.php?product_name=' + self.mProject
		data = urllib2.urlopen(url).read()
		fp = open(infoFileName, 'w')
		if not fp:
			return False
		
		fp.write(data)
		fp.close()
		return True

	def getBugList(self, url, infoFileName):
		bugListInfo = []
		#step 1: gen xml file.
		if self.genBugInfoFile(url, infoFileName) == False:
			return None
		
		#step 2: gen info entrys
		entrys = self.genInfoEntrys(infoFileName)
		if entrys is None:
			return None
		
		for node in entrys:
			#step 3: parse email, author, bugid, title
			email = getFirstElementData(node, "bug_assigned_to")
			author = email.split('@')[0].strip()
			id = "[Bug:" + getFirstElementData(node, "bug_id") + "]"
			title = id + getFirstElementData(node, "bug_title")
			bugListInfo.append(('%s: %s') % (author, title))
		
		return bugListInfo
	
	def getNotFixList(self):
		return self.getBugList(self.mNotFixUrl, self.mNotFixFile)
	
	def getFixedList(self):
		return self.getBugList(self.mFixedUrl, self.mFixedFile)

	'''				
	def getNotFixList(self):
		listNotFixInfo = []
		#step 1: gen xml file.
		if self.genNotFixInfoFile() == False:
			return None		
		
		#step 2: gen info entrys
		entrys = self.genInfoEntrys()
		if entrys is None:
			return None
		
		for node in entrys:
			#step 3: parse email, author, bugid, title
			email = getFirstElementData(node, "bug_assigned_to")
			author = email.split('@')[0].strip()
			id = "[Bug:" + getFirstElementData(node, "bug_id") + "]"
			title = id + getFirstElementData(node, "bug_title")
			listNotFixInfo.append(('%s: %s') % (author, title))
		
		return listNotFixInfo
	'''

class BugInfoGenerator:
	def __init__(self, project, url, start, end):
		self.mProject = project.upper()
		self.mUrl = url
		self.mStartRevision = int(start)
		self.mLastRevistion = int(end)

		if self.mStartRevision > self.mLastRevistion:
			temp = self.mStartRevision
			self.mStartRevision = self.mLastRevistion
			self.mLastRevistion = temp

		if not os.path.isdir(TEMP_PATH):
			os.makedirs(TEMP_PATH)

		self.mPattern = re.compile('^\s*\[([^\]]+)\]\s*(\[([^\]]+)\].*)')

	def genSvnLog(self, pathname):
		return os.system("svn log --xml -r %d:%d %s > %s" % (self.mStartRevision, self.mLastRevistion, self.mUrl, pathname)) == 0

	def writeTitle(self, title):
		self.mFileOutput.write("========================================================\r\n")
		self.mFileOutput.write(title)
		self.mFileOutput.write("\r\n========================================================\r\n\r\n")

	def writeLogList(self, title, logList, prefix = "", last = False):
		if len(logList) < 1:
			return

		self.mFileOutput.write(title)
		self.mFileOutput.write(":\r\n")
		index = 1
		for log in logList:
			self.mFileOutput.write("%s%d. %s\r\n" % (prefix, index, log))
			index = index + 1

		if not last:
			self.mFileOutput.write("\r\n")

	def genBugInfo(self, pathname):
		fileSvnLog = os.path.join(TEMP_PATH, FILENAME_SVN_LOG)
		if self.genSvnLog(fileSvnLog) == False:
			return False
		
		parser = SvnLogParser()
		if parser.loadXml(fileSvnLog) == False:
			return False

		listBug = []
		listPatch = []
		listDevelop = []
		listCustomize = []
		listVendor = []
		listMerge = []
		listOther = []
		listUnknown = []

		for node in parser.getLogEntrys():
			entry = SvnLogEntry(node)
			message = entry.getMessage()
			if not message:
				continue
			message = message.replace('\n', ' ').strip()
			match = self.mPattern.match(message)
			if not match:
				listUnknown.append("%s: %s" % (entry.getAuthor(), message))
				continue

			if match.group(1).upper().find(self.mProject) < 0:
				listOther.append(message)
				continue

			action = match.group(3).strip().lower()
			comment = match.group(2).strip()
			if action.startswith("bug"):
				listBug.append(comment)
			elif action.startswith("patch"):
				listPatch.append(comment)
			elif action.startswith("dev"):
				listDevelop.append(comment)
			elif action.startswith("cus"):
				listCustomize.append(comment)
			elif action.startswith("vendor"):
				listVendor.append(comment)
			elif action.startswith("merge"):
				listMerge.append(comment)
			else:
				listOther.append(message)

		bugzillaInfo = BugzillaInfo(self.mProject)		
		listNotFixInfo = bugzillaInfo.getNotFixList()
		listFixedInfo = bugzillaInfo.getFixedList()

		fp = open(pathname, "w")
		if not fp:
			return False

		self.mFileOutput = fp

		self.writeTitle("项目名称： %s\r\nsvn版本号: 从 %d 到 %d" % (self.mProject, self.mStartRevision, self.mLastRevistion))
		self.writeLogList("修改bug", listBug)
		self.writeLogList("合入patch", listPatch)
		self.writeLogList("增加功能", listDevelop)
		self.writeLogList("客制化修改", listCustomize)
		self.writeLogList("原产代码", listVendor)
		self.writeLogList("merge代码", listMerge)
		self.writeLogList("其他项目的修改", listOther)
		self.writeLogList("无法识别的", listUnknown)
		self.writeLogList('当前项目中状态为RESLOVED的bug', listFixedInfo)
		self.writeLogList('当前项目中不做修改的bug', listNotFixInfo, last = True)

		fp.close()

		return True

if __name__ == "__main__":
	if len(sys.argv) < 6:
		print "Usage: %s project url start end filepath" % sys.argv[0]
		sys.exit(-1)

	generator = BugInfoGenerator(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
	if generator.genBugInfo(sys.argv[5]) == False:
		print "Error"
		sys.exit(-1)

	print "OK"
