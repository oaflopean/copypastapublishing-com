import psycopg2
import urllib.parse as urlparse
import os
import json

a = open("babelli-copypasta.json", mode="r")
babelli = json.load(a)

url = urlparse.urlparse(os.environ['DATABASE_URL'])
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
#con.execute("CREATE TABLE fiction (id SERIAL PRIMARY KEY, book_id INTEGER, title +-VARCHAR(255), author VARCHAR(255), subjects VARCHAR(255));")
conn.autocommit=True

book_id_keys = list(babelli.keys())
for id in book_id_keys:
    a = babelli[id]["id"]
    b = babelli[id]["title"]
    c = babelli[id]["author"]
    d = " ".join(babelli[id]["subjects"])
    con.execute("INSERT INTO fiction [book_id, title, author, subjects] VALUES [%s, \"%s\", \"%s\", \"%s\"]",
                (str(a), b, c, d))
    print(id + " added")
print("query done")
os.sleep(100)
