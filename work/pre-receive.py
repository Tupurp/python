#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys
import os
import fileinput
import subprocess
import re

#失败信息
checkFailedMessage = '''##############################################################################
##                                                                          ##
## Commit message style check failed!                                       ##
##                                                                          ##
## Commit message style must satisfy this regular:                          ##
##   ^(?:fixup!\s*)?(\w*)(\(([\w\$\.\*/-].*)\))?\: (. *)|^Merge\ branch(.*) ##
##                                                                          ##
## Example:                                                                 ##
##   feat(test): test commit style check.                                   ##
##                                                                          ##
##############################################################################'''



#日志匹配正则
commitMessagePattern = '^(feat|fix|hotfix|docs|style|refactor|perf|test|chore|revert)(\([^\s]*?\))?(\:\s|\：){1}[^\s]{10,}|^Merge\ branch(.*)'

#获取提交日志列表
def getMsgs(old,new):
    commitmsg = subprocess.check_output(['git','log', oldrev+'..'+newrev, '--pretty=format:%s'],
        universal_newlines=True)
    msgs = commitmsg.split('\n')
    return msgs	 


#读取STDIN信息，并写入变量
oldrev,newrev,refname = sys.stdin.readline().strip().split(' ')


if newrev == '0000000000000000000000000000000000000000':
   sys.exit(0)

if oldrev == '0000000000000000000000000000000000000000':
   sys.exit(0)


#获取推送的branch分支
branch = refname.split('/')[-1]


try:
  # 得到当前提供的 branch 下的最新提交信息
  msgs = getMsgs(oldrev,newrev)
  #正则匹配提交日志是否合乎规范
  for msg in msgs:  
	  flag = re.match(commitMessagePattern,msg)
	  if flag:
	     print(msg+" is meet the requirement")
	  else:
	     print(msg+" is not meet the requirement\n")
	    print(checkFailedMessage)
	    sys.exit(1)
except subprocess.CalledProcessError as err:
    print('======= %s %s ERROR ======='%(branch,err.output))
    sys.exit(1)

  
sys.exit(0)

