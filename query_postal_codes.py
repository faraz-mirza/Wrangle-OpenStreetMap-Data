import sqlite3
import pandas as pd

conn = sqlite3.connect("SanFrancisco.db")

c = conn.cursor()

c.execute("SELECT tags.value, COUNT(*) as count FROM (SELECT * FROM nodes_tags 	  UNION ALL SELECT * FROM ways_tags) \
tags WHERE tags.key='postcode'GROUP BY tags.value ORDER BY count DESC;")

conn.commit()

rows = c.fetchall()

df = pd.DataFrame(rows, columns=['Postal Codes', 'Count'])

print (df)
