#!/usr/bin/python
# -*- coding: utf-8 -*-

# @Date: 2014/12/19
# @Author: xmt

import commands
import os
import time

# SCRIPT_PATH = os.getcwd()
SCRIPT_PATH = '/home/xumingtao/daily_work/testall/02_Repository_Update'
LOG_FILEPATH = os.path.join(SCRIPT_PATH, 'repository_update.log')
CONFIG_FILEPATH = os.path.join(SCRIPT_PATH, 'repo_update.config')
SPLIT_OP_SVN = '#[svn]'
SPLIT_OP_GIT = '#[git]'
SPLIT_OP_GIT_SVN = '#[git-svn]'

def do_svn(repo):
    svn_cmd = 'svn update %s' % repo
    output = commands.getoutput(svn_cmd)
    save_log(svn_cmd)
    save_log(output)

def do_git(repo):
    # step 1: goto git repo
    os.chdir(repo)
    
    # step 2: update
    git_cmd = 'git pull'
    output = commands.getoutput(git_cmd)

    # step 3: goto script path
    os.chdir(SCRIPT_PATH)

    # step 4: save log
    save_log(git_cmd + repo)
    save_log(output)    
    
def do_git_svn(repo):
    # step 1: goto git repo
    os.chdir(repo)
    
    # step 2: update
    git_cmd = 'git svn rebase'
    output = commands.getoutput(git_cmd)

    # step 3: goto script path
    os.chdir(SCRIPT_PATH)

    # step 4: save log
    save_log(git_cmd + repo)
    save_log(output)

def parsePathList(pathList):
    repoList = []
    
    if len(pathList) <= 0:
        return repoList

    for path in pathList.split('\n'):
        if len(path) > 0 and not path.strip()[0] == '#':
            repoList.append(path)

    # if len(repoList) <= 0:
    #    repoList = pathList

    return repoList

# a:svn_index
# b:git_index
# c:git_svn_index
# return: end of SPLIT_OP_SVN
def getEndIndex(a, b, c, length):
    end = length
    
    if (a > b and a > c) or b == c:
        end = length
    elif a < b and a < c:
        end = (b < c) and b or c
    else:
        end = (b < c) and c or b
    
    return end

def getConfig():
    svn_repository = []
    git_repository = []
    git_svn_repository = []
    fp = open(CONFIG_FILEPATH)
    config = fp.read()
    fp.close()
    # print config
    svn_lists = git_lists = git_svn_lists = ''
    end = -1;
    
    svn_index = config.find(SPLIT_OP_SVN)
    git_index = config.find(SPLIT_OP_GIT)
    git_svn_index = config.find(SPLIT_OP_GIT_SVN)
    length = len(config)
    print svn_index, git_index, git_svn_index

#     if svn_index >= 0:
#         if (svn_index > git_index and svn_index > git_svn_index) or git_index == git_svn_index:
#             end = length
#         elif svn_index < git_index and svn_index < git_svn_index:
#             end = (git_index < git_svn_index) and git_index or git_svn_index
#         else:
#             end = (git_index < git_svn_index) and git_svn_index or git_index
#              
#         svn_lists = config[svn_index + len(SPLIT_OP_SVN):end]

    if svn_index >= 0:
        end = getEndIndex(svn_index, git_index, git_svn_index, length)
        svn_lists = config[svn_index + len(SPLIT_OP_SVN):end]

    if git_index >= 0:
        end = getEndIndex(git_index, svn_index, git_svn_index, length)            
        git_lists = config[git_index + len(SPLIT_OP_GIT):end]
        
    if git_svn_index >= 0:
        end = getEndIndex(git_svn_index, svn_index, git_index, length)            
        git_svn_lists = config[git_svn_index + len(SPLIT_OP_GIT_SVN):end]

#     print 'svnlists:%s ' % svn_lists
#     print 'git_lists:%s ' % git_lists
#     print 'git_svn_lists:%s ' % git_svn_lists
    svn_repository = parsePathList(svn_lists)
    git_repository = parsePathList(git_lists)
    git_svn_repository = parsePathList(git_svn_lists)

#     print svn_repository
#     print git_repository
#     print git_svn_repository

    return [svn_repository, git_repository, git_svn_repository]

def save_log(text):
    date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    fp = open(LOG_FILEPATH, 'a')
    text = date + '  ' + text + '\r\n'
    fp.write(text)
    fp.close()

def main():
    save_log('***Update Beginning...***')
    # step 1: get config info
    svn_repository, git_repository, git_svn_repository = getConfig()

    # step 2: update svn repo
    for repo in svn_repository:
        do_svn(repo)

    # step 3: update git repo
    for repo in git_repository:
        do_git(repo)
        
    # step 4: update git_svn repo
    for repo in git_svn_repository:
        do_git_svn(repo)        

    save_log('***Update OK!***')    

if __name__ == '__main__':
    main()
