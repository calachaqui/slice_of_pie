#!/usr/bin/python3

import datetime,os,subprocess,sys

log = '%s'%(datetime.datetime.now()) +'running speedtest-cli\n'
with open('/home/slice/compute/run_log.txt','a+') as l:
	l.write(log)


#run the speedtest-cli and get output, date, metadata
speed = subprocess.check_output(['/usr/local/bin/speedtest-cli','--csv'])
print(speed)

log = '%s'%(datetime.datetime.now())+'finished speedtest, running insert\n'
with open('/home/slice/compute/run_log.txt','a+') as l:
	l.write(log)

cleanput = speed.decode('utf-8')

values = ''
quote = False
for char in cleanput:
	if char == '"':
		if quote == False:
			quote = True
		else:
			quote = False
	if char != ',':
		values = values + char
	elif quote == False:
		values = values + char
values = values.replace('"','')
outlist = values.split(',')
v1 = outlist[0]
v2 = outlist[1]
v3 = outlist[2]
v4 = outlist[3]
v5 = outlist[4]
v6 = outlist[5]
v7 = outlist[6]
v8 = outlist[7]
v9 = outlist[8]
v10 = outlist[9].replace('''
''','')

vals = ','.join(map(str,[v1,v2,v3,v4,v5,v6,v7,v8,v9,v10]))
with open('/home/slice/compute/run_log.txt','a+') as l:
	l.write("%s\n"%vals)

#load data to the sqlite database
import sqlite3
from sqlite3 import Error
try: #create db file or connect to existing file
	conn = sqlite3.connect('/home/slice/compute/speedtest.db')
except Error as e:
	print(e)
	log = "could not connect to database error: %s" % (e)
	with open('/home/slice/compute/run_log.txt','a+') as l:
		l.write("%s\n" % log)
	sys.exit("sqlite insert failed")

c = conn.cursor()
# create table if not exists
stmnt = """CREATE TABLE IF NOT EXISTS isp_speed_log (
	server_id INT,
	sponser VARCHAR(20),
	server_name VARCHAR(20),
	test_time datetime PRIMARY KEY,
	distance float,
	ping float,
	download float,
	upload float,
	ip_address VARCHAR(15)
	);"""
try:
	c.execute(stmnt)
	conn.commit()
except Error as e:
	print(e)
	log = "could not run createif not exists statement: %s\n" % e
	with open('/home/slice/compute/run_log.txt','a+') as l:
		l.write("%s\n"%stmnt)
	sys.exit("sqlite create table failed")
# insert speed log data into database table
stmnt = """INSERT INTO isp_speed_log (
          server_id,
          sponser,
          server_name,
          test_time,
          distance,
          ping,
          download,
          upload,
          ip_address)
              VALUES (
              {sid},
              '{spon}',
              '{snm}',
              '{tt}',
              {dist},
              {ping},
              {down},
              {up},
              '{ip}');""".format(
              sid=v1,spon=v2,snm=v3,tt=v4,dist=v5,ping=6,down=v7,up=v8,ip=v10)
try:
	c.execute(stmnt)
	conn.commit()
except:
	log = "data could not be added to the database"
	with open('/home/slice/compute/run_log.txt','a+') as l:
	        l.write("%s\n"%log)
	sys.exit("sqlite insert failed")

log = "data was inserted to the sqlite database"
with open('/home/slice/compute/run_log.txt','a+') as l:
	l.write("%s\n"%log)
# remove data older than three months
#stmnt = """DELETE FROM isp_speed_log WHERE date(test_time,'%Y-%m-%dT%H:%M:%S.%fZ') < date('now','-90 day');"""

try:
	c.execute(stmnt)
	conn.commit()
except Error as e:
	log = "data could not be deleted from table: %s" % e
	print(log)



