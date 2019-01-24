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
stmnt = """SELECT strftime('%d %H',test_time,'localtime'),round(download/1000000,2)
	FROM isp_speed_log ORDER BY test_time DESC LIMIT 48;"""
cur.execute(stmnt)
rows = cur.fetchall()
downloads = {}
for row in rows:
        downloads[row[0]]= row[1]

# avg speed by day
stmnt = """SELECT strftime('%w',test_time,'localtime'),round(avg(download/1000000),2)
	FROM isp_speed_log GROUP BY strftime('%w',test_time,'localtime');"""
cur.execute(stmnt)
rows = cur.fetchall()
dow = {}
for row in rows:
	dow[row[0]]= row[1]

# avg speed by hour of the day
stmnt = """SELECT strftime('%H',test_time,'localtime'), round(avg(download/1000000),2)
	FROM isp_speed_log GROUP BY strftime('%H',test_time,'localtime');"""
cur.execute(stmnt)
rows = cur.fetchall()
hod = {}
for row in rows:
	hod[row[0]]= row[1]

# count and speed by source
stmnt = """SELECT sponser,count(*),round(avg(download/1000000),2)
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

#print(dow)
#print(hod)
#print(scount)
#print(sspeed)
#print(ip)

#########plotting the data##########
# setup data for 48 hours
lists = sorted(downloads.items())
x,y = zip(*lists)
figa = plt.figure()
ax = figa.add_subplot(111)
ax.plot(x,y)
ax.set_ylim(ymin=0)
ax.set(xlabel='datetime',ylabel='Mbps isp speed',
	title='internet speeds over 48 hours')
plt.xticks(fontsize=6, rotation=315)
ax.grid()
figa.savefig("/home/slice/compute/slice_of_pie/graphs/two_days.png")

# setup for avg speed by day
lists = sorted(dow.items())
x,y = zip(*lists)
figb = plt.figure()
plt.bar(x,y)
plt.xlabel('day of week')
plt.ylabel('avg speed')
plt.title('Avg Download Speed By Day')
plt.xticks(x)
figb.savefig("/home/slice/compute/slice_of_pie/graphs/weekday.png")

# setup for avg speed by hour
lists = sorted(hod.items())
x,y = zip(*lists)
figc = plt.figure()
plt.bar(x,y)
plt.xlabel('hour of day')
plt.ylabel('avg speed')
plt.title('Avg Download Speed By Hour')
plt.xticks(x)
plt.xticks(rotation=45)
figc.savefig("/home/slice/compute/slice_of_pie/graphs/hourly.png")

# setup for count by source
lists = sorted(scount.items())
x,y = zip(*lists)
figd = plt.figure()
plt.bar(x,y)
plt.xlabel('source of service')
plt.ylabel('count of usage')
plt.title('Count of Usage by Internet Source')
plt.xticks(x)
plt.xticks(rotation=45)
#plt.xticks(rotation=315)
figd.savefig("/home/slice/compute/slice_of_pie/graphs/source_count.png")

# setup for speed by source
lists = sorted(sspeed.items())
x,y = zip(*lists)
fige = plt.figure()
plt.bar(x,y)
plt.xlabel('source of service')
plt.ylabel('avg speed')
plt.title('Avg Speed by Internet Source')
plt.xticks(x)
plt.xticks(rotation=45)
fige.savefig("/home/slice/compute/slice_of_pie/graphs/source_speed.png")

## find a way to display ip address dates

