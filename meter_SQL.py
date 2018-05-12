# adapted from class example
import json
from flask import Flask, request
import MySQLdb
import datetime # formatting dates and times
from dateutil.relativedelta import relativedelta # date offsets

# assigns meter IDs to corresponding tenant names
ID_TO_NAME = {61497317:"Jack_Roswell", 52548934:"Alex_Zhuk", 61041183:"Rashid_Zia", 52554278:"Elizabeth_Austin"}

# connect to database
db = MySQLdb.connect(
    host='dschurma.mysql.pythonanywhere-services.com',
    user='dschurma',
    passwd='jackroswell',
    db='dschurma$Meter_Readings',
    use_unicode=True,
    charset='UTF8')

c = db.cursor()

# create tenants table
c.execute('''CREATE TABLE IF NOT EXISTS tenants
    (id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(128),
    time_stamp VARCHAR(128) NOT NULL,
    meter_ID VARCHAR(128) NOT NULL,
    consumption VARCHAR(128) NOT NULL,
    PRIMARY KEY (id))''')

db.commit()

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'It is late at night and David is tired.'

# used for adding to database
@app.route('/insert')
def add_consumption(term=''):
    # check required fields
	if 'time' in request.args and 'id' in request.args and 'consumption' in request.args:
		# get data values from request
		time_stamp = request.args['time']
		meter_ID = int(request.args['id'])
		consumption = int(request.args['consumption'])
		name = ID_TO_NAME[meter_ID]
		# try to insert into database - if error caught, then must reconnect to database
		# (pinging would also work, but this is the solution provided by pythonanywhere documentation)
		try:
		    c.execute('''INSERT INTO tenants (name, time_stamp, meter_ID, consumption) VALUES (%s, %s, %s, %s) ''', (name, time_stamp, meter_ID, consumption))
		except:
		    db = MySQLdb.connect(host='dschurma.mysql.pythonanywhere-services.com', user='dschurma', passwd='jackroswell', db='dschurma$Meter_Readings', use_unicode=True, charset='UTF8')
		    c = db.cursor()
		    c.execute('''INSERT INTO tenants (name, time_stamp, meter_ID, consumption) VALUES (%s, %s, %s, %s) ''', (name, time_stamp, meter_ID, consumption))
		db.commit()
		return "success"
	else:
		return 'Invalid parameters - need \"time\", \"id\", and \"consumption\"'

# used for querying power usage by name
@app.route('/query_by_tenant')
def query_by_tenant_name():
    # check required field
	if 'name' in request.args:
	    # get data from request
		name = request.args['name']
		# get time search ranges
		now = datetime.datetime.now()
		past_lower = now + relativedelta(months = -1)
		past_upper = past_lower + relativedelta(days = +1)
		# try to query database by one month ago date range - if error caught, then must reconnect to database
		# (pinging would also work, but this is the solution provided by pythonanywhere documentation)
		try:
		    c.execute("SELECT * FROM tenants WHERE time_stamp >= %s AND time_stamp < %s AND name = %s", (str(past_lower), str(past_upper), name))
		except:
		    db = MySQLdb.connect(host='dschurma.mysql.pythonanywhere-services.com', user='dschurma', passwd='jackroswell', db='dschurma$Meter_Readings', use_unicode=True, charset='UTF8')
		    c = db.cursor()
		    c.execute("SELECT * FROM tenants WHERE time_stamp >= %s AND time_stamp < %s AND name = %s", (str(past_lower), str(past_upper), name))
		data_past = c.fetchmany(10)

		# repeat for current time range
		now_lower = now + relativedelta(days = -1)
		try:
		    c.execute("SELECT * FROM tenants WHERE time_stamp >= %s AND time_stamp < %s AND name = %s", (str(now_lower), str(now), name))
		except:
		    db = MySQLdb.connect(host='dschurma.mysql.pythonanywhere-services.com', user='dschurma', passwd='jackroswell', db='dschurma$Meter_Readings', use_unicode=True, charset='UTF8')
		    c = db.cursor()
		data_now = c.fetchmany(10)

		# get latest meter reading
		consumption_now = data_now[-1][-1]
		# if no past data found, then data has not been propagated for an entire month - then, treat total usage as 0
		if len(data_past) == 0:
		    consumption_past = consumption_now
		else:
		    consumption_past = data_past[0][-1]

	    # return a json object of last month's reading, the current reading, and the difference (past month's usage)
		return json.dumps({'current_month':consumption_now, 'past_month':consumption_past, 'change':str(int(consumption_now) - int(consumption_past))})
	else:
		return 'Invalid parameters - need \"name\"'
