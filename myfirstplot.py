#!/home/slice/berryconda3/bin/python

import matplotlib
# Force matplotlib to not use any Xwindows backend.
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

###############getting data section################
# Data for plotting
import sqlite3,sys
from sqlite3 import Error

# 48 hour download speeds
conn = sqlite3.connect("/home/slice/compute/speedtest.db")
cur = conn.cursor()
stmnt = """SELECT datetime(test_time,'localtime'),round(download/1000000,2)
	FROM isp_speed_log ORDER BY test_time DESC LIMIT 48;"""
cur.execute(stmnt)
rows = cur.fetchall()
downloads = {}
for row in rows:
        downloads[row[0]]= row[1]

# avg speed by day
stmnt = """SELECT strftime('%w',test_time,'locatime'),avg(round(download/1000000,2))
	FROM isp_speed_log GROUP BY strftime('%w',test_time,'localtime');"""
cur.execute(stmnt)
rows = cur.fetchall()
dow = {}
for row in rows:
	dow[row[0]]= row[1]

# avg speed by hour of the day
stmnt = """SELECT strftime('%H',test_time,'localtime'), avg(round(download/1000000,2))
	FROM isp_speed_log GROUP BY strftime('%H',test_time,'localtime');"""
cur.execute(stmnt)
rows = cur.fetchall()
hod = {}
for row in rows:
	hod[row[0]]= row[1]

# count and speed by source
stmnt = """SELECT sponser,count(*),round(avg(download/1000000,2)
	FROM isp_speed_log GROUP BY sponser;"""
cur.execute(stmnt)
rows = cur.fetchall()
scount = {}
sspeed = {}
for row in rows:
	scount[row[0]]= row[1]
	sspeed[row[0]]= row[2]

# min date for ip address
stmnt = """SELECT min(datetime(test_time,'localtime')),ip_address
	FROM isp_speed_log GROUP BY ip_address;"""
cur.execute(stmnt)
rows = cur.fetchall()
ip = {}
for row in rows:
	ip[row[0]]= row[1]

#########plotting the data##########
# setup data for 48 hours
lists = sorted(downloads.items())
x,y = zip(*lists)
fig, ax = plt.subplots()
ax.plot(x,y)
ax.set_ylim(ymin=0)

ax.set(xlabel='datetime',ylabel='Mbps isp speed',
	title='internet speeds over 48 hours')
ax.grid()
fig.savefig("/home/slice/compute/slice_of_pi/graphs/two_days.png")

# setup data for avg speed by day
lists = sorted(dow.items())
x,y = zip(*lists)
fig, ax = plt.subplots()
ax.plot(x,y)
ax.set_ylim(ymin=0)
ax.set(xlabel='day of week',ylabel='avg isp speed',
	title='avg internet speed by day of week')
ax.grid()
fig.savefig("/home/slice/compute/slice_of_pi/graphs/weekday.png")

# setup for avg speed by hour
lists = sorted(hod.items())
x,y = zip(*lists)
fig, ax = plt.subplots()
ax.set_ylim(ymin=0)
ax.set(xlabel='hour of day',ylabel='avg isp speed',
	title='avg internet speed by hour of day')
ax.grid()
fig.savefig("/home/slice/compute/slice_of_pi/graphs/hourly.png")

# setup for count by source
lists = sorted(scount.items())
x,y = zip(*lists)
fig, ax = plt.subplots()
ax.set_ylim(ymin=0)
ax.set(xlabel='source of service',ylabel='count of usage',
        title='count of usage of internet sources')
ax.grid()
fig.savefig("/home/slice/compute/slice_of_pi/graphs/source_count.png")

# setup for speed by source
lists = sorted(sspeed.items())
x,y = zip(*lists)
fig, ax = plt.subplots()
ax.set_ylim(ymin=0)
ax.set(xlabel='source of service',ylabel='avg speed',
        title='average speed of download by source')
ax.grid()
fig.savefig("/home/slice/compute/slice_of_pi/graphs/source_speed.png")

# find a way to display ip address dates

