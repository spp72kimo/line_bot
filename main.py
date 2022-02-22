import os
import json
from getTemperature import getTemperature

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
    
    if msg == '測試':
        f = open('test_temp.json','r',encoding='utf-8')
        temp = json.load(f)
        f.close()
        line_bot_api.reply_message(reply_token, FlexSendMessage(alt_text='測試樣板',contents=temp))
    elif msg.isdigit() and int(msg) < 22 and int(msg) >= 0: 
        # 取得氣象資料
        temperature = getTemperature(int(msg))
        line_bot_api.reply_message(reply_token, FlexSendMessage(alt_text='天氣預報',contents=temperature))
    else:
        line_bot_api.push_message(user_id, TextSendMessage(text=f'您輸入錯誤：{msg}\n請輸入正確數字！'))
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

        line_bot_api.push_message(user_id, TextSendMessage(
            text=text,
            quick_reply=QuickReply(
                items=[
                    QuickReplyButton(
                        action=PostbackAction(label="Postback",data="回傳資料")
                        ),
                    QuickReplyButton(
                        action=MessageAction(label="台北市",text="0")
                        ),
                    QuickReplyButton(
                    action=MessageAction(label="新北市",text="1")
                    ),
                    QuickReplyButton(
                        action=MessageAction(label="桃園市",text="2")
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
    app.run()
    # port = int(os.environ.get('PORT', 80))
    # app.run(host='0.0.0.0', port=port)

    