#!/usr/bin/python
import json
#from nltk.tokenize import RegexpTokenizer
#from gensim import models
import re

REauthor = re.compile(r'<(.*?)>')

def getauthor(aut):
    return re.findall(REauthor, aut)[0]

def getdate():
    pass

def getcommentbow():
    pass

def trainbow():
    pass


with open('./preprocess/antlr3_java.json') as data_file:
    data = dict(json.load(data_file))

feature = {}
author = []
"""
for key in data:
    author.append(getauthor(data[key]['author']))

    exit()
"""
for key in data:
    tauthor = getauthor(data[key]['author'])
    
