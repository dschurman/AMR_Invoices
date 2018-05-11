# adapted from class example
import requests, json
from flask import Flask, Response,request
import MySQLdb
#import time
import datetime
from dateutil.relativedelta import relativedelta

ID_TO_NAME = {61497317:"Jack_Roswell", 52548934:"Alex_Zhuk", 61041183:"Rashid_Zia", 52554278:"Elizabeth_Austin"}

db = MySQLdb.connect(
    host='dschurma.mysql.pythonanywhere-services.com',
    user='dschurma',
    passwd='jackroswell',
    db='dschurma$Meter_Readings',
    use_unicode=True,
    charset='UTF8')

c = db.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS tenants
    (id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(128) NOT NULL,
    time_stamp VARCHAR(128) NOT NULL,
    meter_ID VARCHAR(128),
    consumption VARCHAR(128) NOT NULL,
    PRIMARY KEY (id))''')

db.commit()

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'It is late at night and David is tired.'

@app.route('/insert')
def add_consumption(term=''):
	if 'time' in request.args and 'id' in request.args and 'consumption' in request.args:
		time_stamp = request.args['time']
		meter_ID = int(request.args['id'])
		consumption = int(request.args['consumption'])
		name = ID_TO_NAME[meter_ID]
		c.execute('''INSERT INTO tenants (name, time_stamp, meter_ID, consumption) VALUES (%s, %s, %s, %s) ''', (name, time_stamp, meter_ID, consumption))
		db.commit()
		return "success"
	else:
		return 'Invalid parameters - need \"time\", \"id\", and \"consumption\"'

@app.route('/query_by_tenant')
def query_by_tenant_name():
	if 'name' in request.args:
		name = request.args['name']
		now = datetime.datetime.now()
		past_lower = now + relativedelta(months = -1)
		past_upper = past_lower + relativedelta(days = +1)
		c.execute("SELECT * FROM tenants WHERE time_stamp >= %s AND time_stamp < %s AND name = %s", (str(past_lower), str(past_upper), name))
		data_past = c.fetchmany(10)

		now_lower = now + relativedelta(days = -1)
		c.execute("SELECT * FROM tenants WHERE time_stamp >= %s AND time_stamp < %s AND name = %s", (str(now_lower), str(now), name))
		data_now = c.fetchmany(10)

		if len(data_past) == 0:
		    consumption_past = 0
		else:
		    consumption_past = data_past[0][-1]

		consumption_now = data_now[-1][-1]
		#return str(past_lower) + '<br>' + str(past_upper) + '<br>' + str(now_lower) + '<br>' + str(now) + '<br>' + str(data_past) + '<br>' + str(data_now) + '<br>' + str(int(consumption_now) - int(consumption_past)
		return str(int(consumption_now) - int(consumption_past))
	else:
		return 'Invalid parameters - need \"name\"'
