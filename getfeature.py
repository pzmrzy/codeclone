#!/usr/bin/python
import json
from nltk.tokenize import RegexpTokenizer
from gensim import corpora
import re

REauthor = re.compile(r'<(.*?)>')
REdate = re.compile(r'AuthorDate: (.*?) (.*?) (.*?) (.*?):(.*?):(.*?) (.*?) (.*?)')
tokenizer = RegexpTokenizer(r'\w+')

def getauthor(aut):
    return re.findall(REauthor, aut)[0]

def getdate(dat):
    tmp = re.findall(REdate, dat)[0]
    date = tmp[0]
    month = tmp[1]
    day = tmp[2]
    hour = tmp[3]
    year = tmp[6]
    return (date, year, month, day, hour)

def getfname(fn):
    return fn.split('/')[-1].split('.')[0]

def getcommentbow(com):
    doc = []
    for l in com:
        tmp = tokenizer.tokenize(l.strip())
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
    docs.append(getcommentbow(javadata[key]['comment']))

author = list(set(author))
dictionary = trainbow(docs)

for key in javadata:
    tauthor = getauthor(javadata[key]['author'])
    dat = getdate(javadata[key]['authordate'])
    fname = getfname(javadata[key]['fname'])
    comment = dictionary.doc2bow(getcommentbow(javadata[key]['comment']))

    print key
    print tauthor
    print dat
    print comment
    exit()
