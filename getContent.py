from ssl import ALERT_DESCRIPTION_UNKNOWN_PSK_IDENTITY
import requests
import json



dataid='F-C0032-001'
apikey = 'CWB-FE716C0D-A181-471C-B987-02279212628D'
format = 'JSON'
res = requests.get(f'https://opendata.cwb.gov.tw/fileapi/v1/opendataapi/{dataid}?Authorization={apikey}&format={format}')

with open(f'{dataid}.json','w',encoding='utf-8') as f:
    f.write(res.text)

meta = json.loads(res.text)
# print(res.text)