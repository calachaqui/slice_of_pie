#!/home/slice/berryconda3/bin/python
import sqlite3,sys
from sqlite3 import Error

conn = sqlite3.connect("/home/slice/compute/speedtest.db")
cur = conn.cursor()

stmnt = "SELECT test_time,round(download/1000000,2) FROM isp_speed_log;"
cur.execute(stmnt)

rows = cur.fetchall()
downloads = {}
for row in rows:
	downloads[row[0]]= row[1]

print(downloads)

#lists = sorted(downloads.items())
#x,y = zip(*lists)
#p

