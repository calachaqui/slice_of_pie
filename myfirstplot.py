#!/home/slice/berryconda3/bin/python

import matplotlib
# Force matplotlib to not use any Xwindows backend.
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

# Data for platting
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

# setup data for plotting
lists = sorted(downloads.items())
x,y = zip(*lists)


fig, ax = plt.subplots()
ax.plot(x,y)

ax.set(xlabel='datetime',ylabel='Mbps isp speed',
	title='internet speeds of time')
ax.grid()
fig.savefig("/home/slice/compute/test_figure.png")

