#!/usr/bin/python
import json
from nltk.tokenize import RegexpTokenizer
from gensim import corpora
import re
import time
import datetime

REauthor = re.compile(r'<(.*?)>')
REdate = re.compile(r'AuthorDate: (.*?) (.*?) (.*?) (.*?):(.*?):(.*?) (.*?) (.*?)')
tokenizer = RegexpTokenizer(r'\w+')

def getauthor(aut):
    return re.findall(REauthor, aut)[0]

def getdate(dat):
    def ch(s):
        if s == 'Jan':
            return 1
        elif s == 'Feb':
            return 2
        elif s == 'Mar':
            return 3
        elif s == 'Apr':
            return 4
        elif s == 'May':
            return 5
        elif s == 'Jun':
            return 6
        elif s == 'Jul':
            return 7
        elif s == 'Aug':
            return 8
        elif s == 'Sep':
            return 9
        elif s == 'Oct':
            return 10
        elif s == 'Nov':
            return 11
        elif s == 'Dec':
            return 12
        else:
            return 'false'

    tmp = re.findall(REdate, dat)[0]
    date = tmp[0]
    month = ch(tmp[1])
    day = int(tmp[2])
    hour = int(tmp[3])
    minute = int(tmp[4])
    second = int(tmp[5])
    year = int(tmp[6])
    dt = datetime.datetime(year, month, day, hour, minute, second)
    ts = time.mktime(dt.timetuple())
    return int(ts)

def getfname(fn):
    return fn.split('/')[-1].split('.')[0]

def getcommentbow(com):
    doc = []
    for l in com:
        tmp = tokenizer.tokenize(l.lower().strip())
        doc += tmp
    return tmp

def trainbow(docs):
    dictionary = corpora.Dictionary(docs)
    return dictionary

with open('./preprocess/antlr3_java.json') as data_file:
    javadata = dict(json.load(data_file))

with open('./preprocess/antlr3_csharp.json') as data_file:
    csdata = dict(json.load(data_file))

feature = {}
author = []
docs = []

for key in javadata:
    author.append(getauthor(javadata[key]['author']))
    docs.append(getcommentbow(javadata[key]['comment']))

for key in csdata:
    author.append(getauthor(csdata[key]['author']))
    docs.append(getcommentbow(csdata[key]['comment']))

author = list(set(author))
dictionary = trainbow(docs)

dic = {}
for key in javadata:
    tauthor = getauthor(javadata[key]['author'])
    timestamp = getdate(javadata[key]['authordate'])
    fname = getfname(javadata[key]['fname'])
    comment = dictionary.doc2bow(getcommentbow(javadata[key]['comment']))
    tkey = 'java_'+key
    dic[tkey] = {'author':tauthor, 'timestamp':timestamp, 'fname':fname, 'comment':comment}

for key in csdata:
    tauthor = getauthor(csdata[key]['author'])
    timestamp = getdate(csdata[key]['authordate'])
    fname = getfname(csdata[key]['fname'])
    comment = dictionary.doc2bow(getcommentbow(csdata[key]['comment']))
    tkey = 'cs_'+key
    dic[tkey] = {'author':tauthor, 'timestamp':timestamp, 'fname':fname, 'comment':comment}

print json.dumps(dic, sort_keys=True, indent=4, separators=(',', ': '))
