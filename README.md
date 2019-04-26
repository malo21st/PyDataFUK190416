# PyDataFUK190416
PyData.Fukuoka Meetup #3 - LINE Fukuoka会場

# ＬＴ資料
福岡県の交通事故を見える化してみた（地図編）.pdf

# ファイルの説明と処理の流れ
DB（データベースフォルダ）交通事故データ<BR>
　　　　↓<BR>
make_near_list.py（処理）50m以内で発生した事故の抽出<BR>
　　　　↓<BR>
near_list_50m.pkl（データ）a:id, b:id, distance:距離<BR>
　　　　↓<BR>
地図に交通事故の発生場所をプロット.ipynb（処理）<BR>
create_map.py（上と同じ処理）JupyterNotebookが使えない方はこちら<BR>
　　　　↓<BR>
plot_map_tooltip10m.html　（出力）危険な交差点<BR>
plot_map_tooltip50m.html　（出力）危険なエリア<BR>
plot_map_MDP.html　（出力）最も危険なポイント<BR>
