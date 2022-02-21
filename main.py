import re
import os
import json
import requests

from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
    # MessageEvent, TextMessage, TextSendMessage,


app = Flask(__name__,static_url_path='/',static_folder='public')


line_bot_api = LineBotApi('P8Q73gxhooUHWCXs7boN9tQRwLUOvHDNaAj/8AjvOCTqY0RdOgpu9gsOhZGojAXMiBjhjwuxWlvl0BloHSo+F/5uImCWEi5WP7El5nWpKnkAz56Ouxf31zqFlrsHsgVzVmnnUjiEW+BjOHJx9gNHwAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('ece5707c637b53ed6820ca6073a11eb0')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
   
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    print('\n',body,'\n')
    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message_type = event.message.type
    user_id = event.source.user_id
    reply_token = event.reply_token
    msg = event.message.text
    
    # 取得氣象局的資料
    dataid='F-C0032-001'
    apikey = 'CWB-FE716C0D-A181-471C-B987-02279212628D'
    format = 'JSON'
    res = requests.get(f'https://opendata.cwb.gov.tw/fileapi/v1/opendataapi/{dataid}?Authorization={apikey}&format={format}')
    weather = json.loads(res.text)

    
    # location_index = {
    #     '台北市' : 0,
    #     '新北市' : 1,
    #     '桃園市' : 2,
    #     '台中市' : 3,
    #     '台南市' : 4,
    #     '高雄市' : 5,
    #     '基隆市' : 6,
    #     '新竹縣' : 7,
    #     '新竹市' : 8,
    #     '苗栗縣' : 9,
    #     '彰化縣' : 10,
    #     '南投縣' : 11,
    #     '雲林縣' : 12,
    #     '嘉義縣' : 13,
    #     '嘉義市' : 14,
    #     '屏東縣' : 15,
    #     '宜蘭縣' : 16,
    #     '花蓮縣' : 17,
    #     '台東縣' : 18,
    #     '澎湖縣' : 19,
    #     '金門縣' : 20,
    #     '連江縣' : 21
    # }
    # if msg not in location_index:
    #     line_bot_api.reply_message(reply_token, TextSendMessage(text='請重新輸入！'))



    # msgRex = re.compile(r'[0-21]')
    # msgRex.match(msg)
    if msg == '測試':
        f = open('test_temp.json','r',encoding='utf-8')
        temp = json.load(f)
        f.close()
        line_bot_api.reply_message(reply_token, FlexSendMessage(alt_text='測試樣板',contents=temp))
        

    msgRexp = re.compile(r'[0-21]')
    mo = msgRexp.match(msg)   
    print(mo) 
    if (mo == None):
         line_bot_api.push_message(user_id, TextSendMessage(text=f'您輸入錯誤：{msg}\n請輸入正確數字！'))
    if mo:
        # 讀取flex樣板格式
        f = open('template.json','r',encoding='utf-8')
        temp = json.load(f)
        f.close()
        contents = temp['contents']
        i = int(msg)
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

        # 傳送氣象資訊
        line_bot_api.reply_message(reply_token, FlexSendMessage(alt_text='天氣預報',contents=temp))
    else:
        text=f'''查詢氣象資料，請輸入數字...
        '台北市' : 0,
        '新北市' : 1,
        '桃園市' : 2,
        '台中市' : 3,
        '台南市' : 4,
        '高雄市' : 5,
        '基隆市' : 6,
        '新竹縣' : 7,
        '新竹市' : 8,
        '苗栗縣' : 9,
        '彰化縣' : 10,
        '南投縣' : 11,
        '雲林縣' : 12,
        '嘉義縣' : 13,
        '嘉義市' : 14,
        '屏東縣' : 15,
        '宜蘭縣' : 16,
        '花蓮縣' : 17,
        '台東縣' : 18,
        '澎湖縣' : 19,
        '金門縣' : 20,
        '連江縣' : 21'''

        line_bot_api.push_message(user_id, TextSendMessage(text=text,
        quick_reply=QuickReply(
        items=[
            QuickReplyButton(
                action=PostbackAction(label="Postback",data="回傳資料")
                ),
            QuickReplyButton(
                action=MessageAction(label="文字訊息",text="回傳文字")
                ),
            QuickReplyButton(
                action=DatetimePickerAction(label="時間選擇",data="時間選擇",mode='datetime')
                ),
            QuickReplyButton(
                action=CameraAction(label="拍照")
                ),
            QuickReplyButton(
                action=CameraRollAction(label="相簿")
                ),
            QuickReplyButton(
                action=LocationAction(label="傳送位置")
                )
            ]
        )
        )
        )



if __name__ == "__main__":
    # app.run()
    port = int(os.environ.get('PORT', 80))
    app.run(host='0.0.0.0', port=port)

    