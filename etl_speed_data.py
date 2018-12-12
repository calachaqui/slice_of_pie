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
try:
	#load data to the sqlite database
	import sqlite3
	conn = sqlite3.connect('/home/slice/compute/speedtest.db')
	c = conn.cursor()
	
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
	c.execute(stmnt)
	conn.commit()
except:
	stmnt = "data could not be added to the database"
	with open('/home/slice/compute/run_log.txt','a+') as l:
	        l.write("%s\n"%stmnt)
	sys.exit("sqlite insert failed")
stmnt = "data was inserted to the sqlite database"
with open('/home/slice/compute/run_log.txt','a+') as l:
	l.write("%s\n"%stmnt)

