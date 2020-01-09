import psycopg2
import urllib.parse as urlparse
import os
import json

a = open("babelli-copypasta.json", mode="r")
babelli = json.load(a)

url = urlparse.urlparse(postgresql://oaflopean:99burning944@104.154.59.220:5432/data001)
dbname = url.path[1:]
user = url.username
password = url.password
host = url.hostname
port = url.port

conn = psycopg2.connect(
    dbname=dbname,
    user=user,
    password=password,
    host=host,
    port=port
)
con = conn.cursor()
conn.autocommit=True

con.execute('CREATE DATABASE {};'.format(dbname))
book_id_keys = list(babelli.keys())
for id in book_id_keys:
    a = babelli[id]["id"]
    b = babelli[id]["title"]
    c = babelli[id]["author"]
    d = " ".join(babelli[id]["subjects"])
    con.execute("INSERT INTO fiction (book_id, title, author, subjects) VALUES (%s, %s, %s, %s)",
                (str(a), b, c, d))
    print(id + " added")
print("query done")
