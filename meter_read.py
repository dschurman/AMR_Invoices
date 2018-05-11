# adapted from https://billyoverton.com/2016/06/19/smart-meter-collecting-the-data.html
import sys
import json
import subprocess
import time

def meter_read(id_list):
	proc = None
	if len(id_list) == 0:
		proc = subprocess.Popen(['$GOPATH/bin/rtlamr', '-format=json', '-unique=true'], stdout = subprocess.PIPE)
	else:
		id_str = '\"' + ','.join(id_list) + '\"'
		proc = subprocess.Popen(['$GOPATH/bin/rtlamr', '-filterid=' + id_str, '-format=json', '-unique=true'], stdout = subprocess.PIPE)

	while True:
	    line = proc.stdout.readline()
	    if not line:
	        break

	    data = json.loads(line)
	    message = [{"measurement":"consumption", "time": data['Time'], "tags": {"meter": data['Message']['ID'] }, "fields": {"value": data['Message']['Consumption']}}]
	    print(message)
	    time.sleep(1)

def main():
	id_list = []
	for n in sys.argv[1:]:
		id_list.append(int(n))
	
	'''
	if len(id_list) == 0:
		print('Usage: python3 meter_read.py [ID1 ID2 ID3 ... IDn]')
		return 1
	'''

	meter_read(id_list)

if __name__ == '__main__':
	main()