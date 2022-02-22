import requests
import json


def getTemperature(i=0):

    # 取得氣象局的資料
    dataid='F-C0032-001'
    apikey = 'CWB-FE716C0D-A181-471C-B987-02279212628D'
    format = 'JSON'
    res = requests.get(f'https://opendata.cwb.gov.tw/fileapi/v1/opendataapi/{dataid}?Authorization={apikey}&format={format}')
    weather = json.loads(res.text)
    
    # 讀取flex樣板格式
    f = open('temperature.json','r',encoding='utf-8')
    temp = json.load(f)
    f.close()
    contents = temp['contents']

    # 設定氣象資料到變數
    for j in range(3):
        # i = location_index[msg]
        locationName = weather['cwbopendata']['dataset']['location'][i]['locationName']
        startTime = weather['cwbopendata']['dataset']['location'][i]['weatherElement'][0]['time'][j]['startTime'][5:16]
        endTime = weather['cwbopendata']['dataset']['location'][i]['weatherElement'][0]['time'][j]['endTime'][5:16]
        startTime = startTime.replace('T',' ')
        endTime = endTime.replace('T',' ')
        condition = weather['cwbopendata']['dataset']['location'][i]['weatherElement'][0]['time'][j]['parameter']['parameterName']
        temperature_now = weather['cwbopendata']['dataset']['location'][i]['weatherElement'][0]['time'][j]['parameter']['parameterValue']
        temperature_Max = weather['cwbopendata']['dataset']['location'][i]['weatherElement'][1]['time'][j]['parameter']['parameterName']
        temperature_Min = weather['cwbopendata']['dataset']['location'][i]['weatherElement'][2]['time'][j]['parameter']['parameterName']
        comfort = weather['cwbopendata']['dataset']['location'][i]['weatherElement'][3]['time'][j]['parameter']['parameterName']
        rain = weather['cwbopendata']['dataset']['location'][i]['weatherElement'][4]['time'][j]['parameter']['parameterName']

        # 設定氣象資料到flex
        contents[j]['body']['contents'][0]['text'] = f'{locationName}：{temperature_now}°C '
        contents[j]['body']['contents'][1]['text'] = f'{condition} {comfort}'
        contents[j]['body']['contents'][2]['text'] = f'{startTime} ~ {endTime}'
        contents[j]['body']['contents'][3]['text'] = f'{temperature_Min}°C ~ {temperature_Max}°C'
        contents[j]['body']['contents'][4]['text'] = f'降雨機率：{rain}%'

    return temp