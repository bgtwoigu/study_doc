#!/usr/bin/python

#@author: xumingtao
#@date: 2014/12/9

import os
import sys
import commands
import fileinput
import fnmatch
import re
import shutil
import time

TRUNK_PATH = '/home/xumingtao/share/Marvell/04_Repository/02_PXA1908/01_git/PO9041/01_trunk/po9041_trunk'
BRANCH_PATH = '/home/xumingtao/share/Marvell/04_Repository/02_PXA1908/01_git/PO9041/02_branches/po9041_AndroidULC_KK44Beta1'
SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__)) 
SUBJECT_STR = 'Subject:'
ENCODER = '?UTF-8?q?'
LOG_FILE = SCRIPT_PATH + '/copy_trunk_to_branches.log'
COMMIT_ID_FILE = SCRIPT_PATH + '/begin_commit_id.file'
BACKUP_PATCHES_DIR = SCRIPT_PATH + '/backup_patches'
GIT_LOG_INFO_FILENAME = 'git_log_info.txt'

def do_git_cmd(git_project_path, git_cmd):
    #step 1: change dir path
    os.chdir(git_project_path)

    #step 2: gen log info 
    output = commands.getoutput(git_cmd)

    #step 3: back to script path
    os.chdir(SCRIPT_PATH)

    return output

def get_git_log_info(git_project_path, begin_commit_id, end_commit_id=''):
    git_cmd = 'git log --pretty=format:"%H | %an" ' + begin_commit_id + '..' + end_commit_id
    #print git_cmd
    return do_git_cmd(git_project_path, git_cmd)

def gen_git_format_patch(git_project_path, commit_id, dirctory):
    git_cmd = 'git format-patch -1 %s -o %s' %(commit_id, dirctory)
    #print git_cmd
    return do_git_cmd(git_project_path, git_cmd)

def apply_git_format_patch(git_project_path, patch_name):
    git_cmd = 'git am --ignore-whitespace %s' % patch_name
    text = do_git_cmd(git_project_path, git_cmd)
    #print output
    
    save_log('########save apply git format patch#####')
    save_log(text)
    save_log('########apply end#######################')

    isGitAmAbort = False
    if text.find('git am --abort') > 0:
        isGitAmAbort = True

    return isGitAmAbort   

def rebase_trunk():
    git_cmd = 'git svn rebase'
    do_git_cmd(TRUNK_PATH, git_cmd)
   
def dcommit_branch():
    git_cmd = 'git svn rebase'
    do_git_cmd(BRANCH_PATH, git_cmd)
    git_cmd = 'git svn dcommit'
    do_git_cmd(BRANCH_PATH, git_cmd)

def replaceInFile(filename, author):
    for line in fileinput.input(filename, inplace=True):
    #for line in fileinput.input(filename):
        newLine = line
        if re.search(SUBJECT_STR, line):
            #print line
            split_index = 0
            encoder_index = line.find(ENCODER)
            if encoder_index > 0:
                split_index = encoder_index + len(ENCODER)
            else:
                split_index = line.find(']') + 1
            newLine = line[0:split_index] + author + line[split_index:]
            #print newLine
        print newLine,

def get_begin_commit_id():
    if not os.path.exists(COMMIT_ID_FILE):
        save_log('copy_trunk_to_branches.log is not exist')
        return None
    
    fp = open(COMMIT_ID_FILE)
    commit_id = fp.read()[:-1]
    save_log('get begin commit id = ' + commit_id)
    fp.close()
    return commit_id

def save_commitid_in_file(commit_id):
    fp = open(COMMIT_ID_FILE, 'w')
    fp.write(commit_id)
    save_log('set last commit id = ' + commit_id)
    fp.close()

def save_log(text):
    date = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    fp = open(LOG_FILE, 'a')
    text = date + ' ' + text + '\r\n'
    fp.write(text)
    fp.close()

def save_git_log_file(backup_dir, loginfoList):
    filepath = backup_dir + '/' + GIT_LOG_INFO_FILENAME
    fp = open(filepath, 'w')
    fp.write(str(loginfoList))
    fp.close()
    save_log('save log info list in filepath = ' + filepath)

def exit_with_log(text):
    save_log(text)
    exit(1)

def gen_backup_dir(begin, end):
    #if not os.path.exist(BACKUP_PATCHES_DIR):
    #    os.makedirs(BACKUP_PATCHES_DIR)
    
    date = time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
    dirPath = '%s/%s_%s_%s' % (BACKUP_PATCHES_DIR, date, begin, end)
    if not os.path.exists(dirPath):
        save_log('make dir: ' + dirPath)
        os.makedirs(dirPath)
    else:
        save_log(dirPath + ' removed!')
        shutil.rmtree(dirPath, True)
    return dirPath

def main():
    save_log('\r\n**********Begin backup all log...!********')

    #step 1. get begin commit id
    begin_commit_id = get_begin_commit_id()
    if begin_commit_id == None:
        exit_with_log('begin commit id is none, exit!')

    #step 2: trunk code rebase from svn repository
    rebase_trunk()

    #step 3: get git log info from trunk
    #end_commit_id = '02b06284db95580573e3debfbea72a84817e5da0'
    #git_log_info = get_git_log_info(TRUNK_PATH, begin_commit_id, end_commit_id)
    git_log_info = get_git_log_info(TRUNK_PATH, begin_commit_id)
    git_log_infoList = git_log_info.splitlines()
    if len(git_log_infoList) <= 0:
        exit_with_log('Thers is no git log info!It is already sync!')

    #last_commit_id = git_log_infoList[-1][0].strip()
    #if begin_commit_id == last_commit_id:
    #    exit_with_log('It is already sync, bengin_commit_id = last_commit_id = ' + last_commit_id)

    #step 4: generate backup directory, save patch files and log info list
    backup_dir = gen_backup_dir(begin_commit_id[0:4], git_log_infoList[-1][0:4])
    save_git_log_file(backup_dir, git_log_info)

    #print git_log_infoList
    for item in git_log_infoList[::-1]:
        info = item.split('|')
        commit_id = info[0].strip()
        author = info[1].strip() + ':'
        #print info
        #print 'commit: ' + commit_id
        #print 'author: ' + author

        #step 6: generate git format patch from trunk.
        filepath = gen_git_format_patch(TRUNK_PATH, commit_id, backup_dir)
        #print filepath

        #step 7: add commit author to subject in patch
        replaceInFile(filepath, author)

        #step 8: apply this format patch to branch
        if apply_git_format_patch(BRANCH_PATH, filepath):
            exit_with_log('branch git am abort! please fix it!')
    
    #step 9: save last commit id in file.
    save_commitid_in_file(commit_id)

    #step 10: dcommit all patch to svn repository.
    dcommit_branch()

    save_log('*********Backup end!!!**********\r\n')

if __name__ == '__main__':
    main()
