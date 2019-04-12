# sqlite3 標準モジュールをインポート
import sqlite3
 
# データベースファイルのパス
dbpath = 'accident.sqlite'

# テーブル定義
DEF_TABLE = """
CREATE TABLE IF NOT EXISTS master (
id INTEGER PRIMARY KEY,
belongs TEXT,
blg_code TEXT,
contents TEXT,
date TEXT,
time TEXT,
day TEXT,
address TEXT,
city_code TEXT,
road TEXT,
accident TEXT,
a_type TEXT,
a_age TEXT,
a_damage TEXT,
b_type TEXT,
b_age TEXT,
b_damage TEXT,
route TEXT,
day_night TEXT,
weather TEXT,
death INTEGER DEFAULT 0,
serious INTEGER DEFAULT 0,
injury INTEGER DEFAULT 0,
latitude REAL DEFAULT 0.0,
longitude REAL DEFAULT 0.0)"""
 
# データベース接続とカーソル生成
connection = sqlite3.connect(dbpath)
# 自動コミットにする場合は下記を指定（コメントアウトを解除のこと）
# connection.isolation_level = None
cursor = connection.cursor()
 
# エラー処理（例外処理）
try:
    # CREATE
    cursor.execute("DROP TABLE IF EXISTS master")
    cursor.execute(DEF_TABLE)
except sqlite3.Error as e:
    print('sqlite3.Error occurred:', e.args[0])

# 保存を実行（忘れると保存されないので注意）
connection.commit()

# 接続を閉じる
connection.close()

