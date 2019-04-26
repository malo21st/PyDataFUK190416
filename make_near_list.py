#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ＤＢに納めた交通事故の発生場所（緯度・経度）の各データの距離を
総当りで計算し、５０ｍ以内のデータをpickle形式で出力
"""
import sqlite3
import pandas as pd
import math
import pickle


DIS_DEG = 0.00045   # 約50mに相当する緯度・経度
DIS_M =  50         # 距離[m]

FILE_NAME = 'near_list_' + str(DIS_M) + 'm.pkl'
SQM = DIS_DEG * DIS_DEG

conn = sqlite3.connect('DB/accident.sqlite')
query = "select id,latitude,longitude from master;"
data = pd.read_sql_query(query, conn)

temp = list(data.values)
near_list = []

while temp:
    pos_a = temp.pop(0)
    if not(pos_a[0] % 1000):
        print(int(pos_a[0]), end=" ")
    for pos_b in temp:
        lat = abs(pos_a[1] - pos_b[1])
        lon = abs(pos_a[2] - pos_b[2])
        if lat > DIS_DEG:
            continue
        if lon > DIS_DEG:
            continue
        sq_dis_deg = lat * lat + lon * lon
        if sq_dis_deg < SQM:
            near_list.append([int(pos_a[0]), 
                              int(pos_b[0]), 
                              math.sqrt(sq_dis_deg) / DIS_DEG * DIS_M
                            ])            

with open(FILE_NAME, mode='wb') as f:
    pickle.dump(near_list, f)
