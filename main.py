from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
    # MessageEvent, TextMessage, TextSendMessage,
import json

app = Flask(__name__)

line_bot_api = LineBotApi('P8Q73gxhooUHWCXs7boN9tQRwLUOvHDNaAj/8AjvOCTqY0RdOgpu9gsOhZGojAXMiBjhjwuxWlvl0BloHSo+F/5uImCWEi5WP7El5nWpKnkAz56Ouxf31zqFlrsHsgVzVmnnUjiEW+BjOHJx9gNHwAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('ece5707c637b53ed6820ca6073a11eb0')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    print('這是訊息資訊： ', body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message_type = event.message.type
    user_id = event.source.user_id
    reply_token = event.reply_token
    msg = event.message.text
    if msg == '地點':
        reply =  LocationSendMessage(
            title='HAMA Boutique Outlet',
            address='台北市內湖區民善街215號1樓(HAMA專櫃)',
            latitude=25.064432222106895,
            longitude=121.5745863441039
            )
    else:
        buttons_template_message = TemplateSendMessage(
            alt_text='Buttons template',
            template=ButtonsTemplate(
                thumbnail_image_url='https://free.com.tw/blog/wp-content/uploads/2014/08/Placekitten480.jpg',
                image_aspect_ratio='rectangle',
                image_size='contain',
                image_background_color='#FFFFFF',
                title='Menu',
                text='Please select',
                default_action=URIAction(
                    label='view detail',
                    uri='http://example.com/page/123'
                ),
                actions=[
                    PostbackAction(
                        label='postback',
                        display_text='postback text',
                        data='action=buy&itemid=1'
                    ),
                    LocationAction(
                        label='location'
                    ),
                    DatetimePickerAction(
                        label='Select date',
                        data='storeId=12345',
                        mode='datetime',
                        initial="2018-12-25T00:00",
                        min='2017-01-24T23:59',
                        max='2018-12-25T00:00'
                    )
                ]
            )
        )
    

    
    line_bot_api.reply_message(
        event.reply_token,buttons_template_message
        )


# import os

if __name__ == "__main__":
    app.run()
    # port = int(os.environ.get('PORT', 80))
    # app.run(host='0.0.0.0', port=port)

    