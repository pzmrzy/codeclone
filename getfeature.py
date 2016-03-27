#!/usr/bin/python
import json

with open('./preprocess/antlr3_java.json') as data_file:
    data = json.load(data_file)

print data
