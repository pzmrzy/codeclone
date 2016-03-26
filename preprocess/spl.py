#!/usr/bin/python
fin = open('csharp.log')
data = fin.readlines()
fin.close()
i = 0
logs = []
cid = '0'
for l in data:
	tmp = l.strip()
	#print tmp
	if (tmp[:7] == "commit "):
		fout = open('./csharplog/%s' % cid, 'w')
		for t in logs:
			fout.write("%s\n" % t)
		fout.close()
		logs=[]
		cid = tmp.split(' ')[1]
		logs.append(tmp)
	else:
		logs.append(tmp)
