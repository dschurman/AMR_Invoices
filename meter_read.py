import sys
import json
import subprocess # command line utility
import time
import datetime
import requests

# adapted from https://billyoverton.com/2016/06/19/smart-meter-collecting-the-data.html
def meter_read(id_list):
	# NOTE: assumes an active rtl_tcp server (perhaps in another terminal window)
	proc = None
	# if no specified IDs, listen for all available meters
	if len(id_list) == 0:
		# start new rtlamr process
		proc = subprocess.Popen(['/home/pi/go/bin/rtlamr', '-format=json', '-unique=true'], stdout = subprocess.PIPE)
	else:
		# start new rtlamr process filtering by specified IDs
		id_str = ','.join(id_list)
		proc = subprocess.Popen(['/home/pi/go/bin/rtlamr', '-filterid=' + id_str, '-format=json', '-unique=true'], stdout = subprocess.PIPE)

	while True:
		# get line from stdout
	    line = proc.stdout.readline()
	    if not line:
	        break

	    # parse json object to retrieve data
	    data = json.loads(line.decode('utf-8'))
	    # format data in json-like object
	    message = [{"measurement":"consumption", "time": data['Time'], "tags": {"meter": data['Message']['ID'] }, "fields": {"value": data['Message']['Consumption']}}]
	    # print for clarity
	    print('***', message)
	    # send request to Flask app to insert into database
	    params = {'consumption':data['Message']['Consumption'], 'time':datetime.datetime.now(), 'id':data['Message']['ID']}
	    requests.get('http://dschurma.pythonanywhere.com/insert', params=params)
	    # repeat every 5 seconds
	    time.sleep(5)

def main():
	id_list = []
	for n in sys.argv[1:]:
		id_list.append(n)

	meter_read(id_list)

if __name__ == '__main__':
	main()