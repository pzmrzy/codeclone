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

files = ls('csharplog')
for f in files:
	if f == "csharplog/.DS_Store":
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
	while True:
		
		while (flag):
			l = fin.readline()
			if l[:10] == "diff --git":
				fname = l
				flag = False
				break
			elif l == '':
				break
			else:
				comment.append(l)
				continue

		l = fin.readline()
		
		
		if l[:10] == "diff --git":
			dic[num] = {"cid":cid, "author":author, "authordate":authordate, "comment": comment, "fname": fname, "code":code}
			code = []
			num += 1
			fname = l
			continue
		code.append(l)
		if l == '':
			fin.close()
			dic[num] = {"cid":cid, "author":author, "authordate":authordate, "comment": comment, "fname": fname, "code":code}
			code = []
			num += 1
			
			break
print len(dic)
newdic = {}
for key in dic:
	if dic[key]["fname"].strip().split('.')[-1] == "cs":
		newdic[key] = dic[key]
print len(newdic)

print json.dumps(newdic, sort_keys=True, indent=4, separators=(',', ': '))
