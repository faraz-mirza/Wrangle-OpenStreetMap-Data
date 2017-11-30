import pandas as pd
import sqlite3
import csv

# Loading the data in Database

conn = sqlite3.connect("SanFrancisco.db")
c = conn.cursor()

df = pd.read_csv("nodes_tags.csv")
df.to_sql("nodes_tags", conn, if_exists='append', index=False)

c.close()
conn.close()

conn = sqlite3.connect("SanFrancisco.db")
c = conn.cursor()

# nodes
c.execute("CREATE TABLE IF NOT EXISTS nodes (id, lat, lon, user, uid, version, changeset, timestamp)")

with open('nodes.csv', 'r') as fin:
    dr = csv.DictReader(fin)
    to_db = [(i['id'], i['lat'], i['lon'], i['user'], i['uid'], i['version'], i['changeset'], i['timestamp']) for i in
             dr]

c.executemany(
    "INSERT INTO nodes (id, lat, lon, user, uid, version, changeset, timestamp) VALUES (?, ?, ?, ?, ?, ?, ?, ?);",
    to_db)
conn.commit()

# ways
c.execute("CREATE TABLE IF NOT EXISTS ways (id, user, uid, version, changeset, timestamp)")

with open('ways.csv', 'r') as fin:
    dr = csv.DictReader(fin)
    to_db = [(i['id'], i['user'], i['uid'], i['version'], i['changeset'], i['timestamp']) for i in dr]

c.executemany("INSERT INTO ways (id, user, uid, version, changeset, timestamp) VALUES (?, ?, ?, ?, ?, ?);", to_db)
conn.commit()

# ways_nodes
c.execute("CREATE TABLE IF NOT EXISTS ways_nodes (id, node_id, position)")

with open('ways_nodes.csv', 'r') as fin:
    dr = csv.DictReader(fin)
    to_db = [(i['id'], i['node_id'], i['position']) for i in dr]

c.executemany("INSERT INTO ways_nodes (id, node_id, position) VALUES (?, ?, ?);", to_db)
conn.commit()

# ways_tags
c.execute("CREATE TABLE IF NOT EXISTS ways_tags (id, key, value, type)")

with open('ways_tags.csv', 'r') as fin:
    dr = csv.DictReader(fin)
    to_db = [(i['id'], i['key'], i['value'], i['type']) for i in dr]

c.executemany("INSERT INTO ways_tags (id, key, value, type) VALUES (?, ?, ?, ?);", to_db)
conn.commit()

c.close()
conn.close()