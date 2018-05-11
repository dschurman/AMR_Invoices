# adapted from https://billyoverton.com/2016/06/19/smart-meter-collecting-the-data.html
import sys
import json
import subprocess
import time
import datetime
import requests

def meter_read(id_list):
	proc = None
	if len(id_list) == 0:
		proc = subprocess.Popen(['/home/pi/go/bin/rtlamr', '-format=json', '-unique=true'], stdout = subprocess.PIPE)
	else:
		id_str = ','.join(id_list)
		proc = subprocess.Popen(['/home/pi/go/bin/rtlamr', '-filterid=' + id_str, '-format=json', '-unique=true'], stdout = subprocess.PIPE)

	while True:
	    line = proc.stdout.readline()
	    #print('***', line)
	    if not line:
	        break

	    data = json.loads(line.decode('utf-8'))
	    message = [{"measurement":"consumption", "time": data['Time'], "tags": {"meter": data['Message']['ID'] }, "fields": {"value": data['Message']['Consumption']}}]
	    print('***', message)
	    params = {'consumption':data['Message']['Consumption'], 'time':datetime.datetime.now(), 'id':data['Message']['ID']}
	    requests.get('http://dschurma.pythonanywhere.com/insert', params=params)
	    time.sleep(5)

def main():
	id_list = []
	for n in sys.argv[1:]:
		id_list.append(n)
	
	'''
	if len(id_list) == 0:
		print('Usage: python3 meter_read.py [ID1 ID2 ID3 ... IDn]')
		return 1
	'''

	meter_read(id_list)

if __name__ == '__main__':
	main()