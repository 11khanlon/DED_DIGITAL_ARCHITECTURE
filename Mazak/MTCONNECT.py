import requests
import time
import xmltodict
import json
 
#MTConnect = requests.get('http://192.168.0.30:5000/current')
#xml = MTConnect._content
file = open('MTConnect_reports.txt', 'w')
#file.write(xml)
i = 0
while i<5:
    MTConnect = requests.get('http://192.168.0.30:5000/current')
    xml = MTConnect._content
    dict_report = xmltodict.parse(xml.decode('utf-8'))
    json_out = json.dumps(dict_report, separators=(',',':'))
    file.write(json_out)
    i+=1
    time.sleep(1)
