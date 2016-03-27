#!/usr/bin/python
import re
import os
import json

def ls(rootDir):
	list_dirs = os.walk(rootDir)
	tmp = []
	for root, dirs, files in list_dirs:
		for f in files:
			if (f[:2] == '._'):
				continue
			tmp.append( os.path.join(root, f) )

	return tmp
dic = {}
num = 0

files = ls('javalog')
for f in files:
	if f == "javalog/.DS_Store":
		continue
	fin = open(f)
	cid = fin.readline().strip()
	author = fin.readline().strip()
	authordate = fin.readline().strip()
	commit = fin.readline().strip()
	commitdate = fin.readline().strip()
	comment = []
	l = ""
	flag = True
	fname = ""
	code = []
	fcode = False
	fat = False
	while True:
		l = fin.readline()
		if l[:10] == "diff --git":
			fname = l.strip()
			flag = False
			fat = False
			continue
		elif l == '':
			break
		else:
			if flag:
				if len(l.strip()) > 0:
					comment.append(l.strip())
				continue
		
		if (l[:3] == "@@ "):
			fat = True
			if len(code) == 0:
				continue
			dic[num] = {"cid":cid, "author":author, "authordate":authordate, "comment": comment, "fname": fname, "code":code}
			code = []
			num += 1
			continue

		if fat:
			code.append(l.strip())
		if l == '':
			fin.close()
			dic[num] = {"cid":cid, "author":author, "authordate":authordate, "comment": comment, "fname": fname, "code":code}
			code = []
			num += 1
			
			break
	
	
#print len(dic)
newdic = {}
for key in dic:
	if dic[key]["fname"].strip().split('.')[-1] == "cs":
		newdic[key] = dic[key]
#print len(newdic)

print json.dumps(newdic, sort_keys=True, indent=4, separators=(',', ': '))
