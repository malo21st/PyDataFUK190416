#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
make_near_list.pyで出力したデータから、指定した距離で抽出した交通事故の
発生場所を地図上にプロットし、ＨＴＭＬ形式で出力する。
"""
import pickle
import pandas as pd
import networkx as nx
import folium
import sqlite3

FILE_NAME = 'near_list_50m.pkl' # 入力データのファイル名
DIS = 30    # 抽出条件の距離[m]
TOP = 20    # プロットさせるグループ数（グラフの数）

Fukuoka_city_hall = [33.58974488,130.401803]    # 福岡市役所の緯度・経度
# マップオブジェクトの生成
plot_map = folium.Map(location=Fukuoka_city_hall, zoom_start=9)

def get_near_df(pkl_name, distance):
    """
    make_near_list.pyで出力したデータを読み込んで、指定した距離(distance)
    以下のデータのみ抽出し、データフレーム形式で出力。 
    データフレームのカラム名は、a, b:ＤＢのid, distance:距離
    """
    with open(pkl_name, 'rb') as f:
        near_list = pickle.load(f)
    df = pd.DataFrame(near_list)
    df.columns=["a","b","distance"]
    df_distance = df.query('distance <= ' + str(distance))
    
    return df_distance

def get_top_list(df_distance):
    """
    データフレーム形式のデータを networkX の Graphオブジェクトに格納。
    格納の際、networkXが自動的に近いも同士を１つの１つのグラフで管理
    してくれる。（グラフは、ノードとエッジから構成される）
    各グラフに納められたノードの数で多い順に並び替えて出力。
    """
    G = nx.Graph()
    for index, row in df_distance.iterrows():
        G.add_edges_from([(row["a"], row["b"])])
        G.edges[row["a"], row["b"]]['distance'] = row["distance"]
        
    top_list = []
    for component in nx.connected_components(G):
        top_list.append([len(component), component])
    top_list.sort(reverse=True)
    
    return top_list


def set_maker(pos, msg):
    """
    地図にマーカーを設定する。
    popup  :マーカーをクリックするとメッセージを表示
    tooltip:マーカーの上にカーソルが来るとメッセージ表示
    """
    MONTH = 24 # データは２年分

    MESSAGE = "発生数：{}件　月平均：{:.1f}件<br>死亡：{}　重傷：{}　軽傷：{}"
    folium.CircleMarker(
        location=[pos[0], pos[1]],
        tooltip=MESSAGE.format(msg[0], msg[0]/MONTH, msg[1], msg[2], msg[3]),
        radius=10,
        color=None,
        fill_color='red'
    ).add_to(plot_map)


df_m = get_near_df(FILE_NAME, DIS)
top_list = get_top_list(df_m)

dbpath = 'DB/accident.sqlite'
connection = sqlite3.connect(dbpath)
cursor = connection.cursor()

for top in top_list[:TOP]:
    list_pos = []
    sum_death = 0   # 死者数の合計
    sum_serious = 0 # 重傷者の合計
    sum_injury = 0  # 軽傷者の合計
    for idx in top[1]:
        sql = "SELECT latitude,longitude,death,serious,injury  \
               FROM master WHERE id = " + str(idx)
        cursor.execute(sql)
        data = cursor.fetchall()
        list_pos.append([data[0][0], data[0][1]])
        sum_death += data[0][2]
        sum_serious += data[0][3]
        sum_injury += data[0][4]

    for pos in list_pos:
        set_maker([pos[0], pos[1]], 
                  [top[0], sum_death, sum_serious, sum_injury]
                  )

connection.close()

plot_map.save('hot_spot_' + str(DIS) + 'm.html')

