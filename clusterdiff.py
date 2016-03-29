#!/usr/bin/python
import json
import numpy as np
import sklearn
from sklearn.cluster import DBSCAN
from sklearn import metrics
import editdistance
import math
data = []

def dist(it1, it2):
    v1 = data[it1]
    v2 = data[it2]
    def L1dis(l1, l2):
        dic = {}
        for k in l1:
            dic[k[0]] = k[1]
        for k in l2:
            if k[0] in dic.keys():
                dic[k[0]] = math.abs(dic[k[0]] - k[1])
            else:
                dic[k[0]] = k[1]
        res = 0
        for k in dic:
            res += dic[k]
        return res

    timedf = v1[2] - v2[2] / 86400
    #if v1[4] == v2[4]:
    #    audf = 0
    #else:
    #    audf = 1
    #fndf = int(editdistance.eval(v1[3], v2[3]))
    #comdf = L1dis(v1[1], v2[1])
    #return timedf + audf + fndf + comdf
    return timedf


with open('feature.json') as data_file:
    jsdata = dict(json.load(data_file))

datanum = []
k = 0
for key in jsdata:
    comment = jsdata[key]['comment']
    ts = jsdata[key]['timestamp']
    fname = jsdata[key]['fname']
    author = jsdata[key]['author']
    data.append([key, comment, ts, fname, author])
    datanum.append([k])
    k += 1

npdata = np.array(datanum, dtype=int)
db = DBSCAN(eps=5, min_samples=5, metric = dist, algorithm = 'ball_tree').fit(npdata)

print db,labels_
