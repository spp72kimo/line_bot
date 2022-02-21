import json
import os

from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

template=ButtonsTemplate(
    thumbnail_image_url='https://example.com/image.jpg',
    title='Menu',
    text='Please select',
    actions=[
        PostbackAction(
            label='postback',
            display_text='postback text',
            data='action=buy&itemid=1'
        ),
        MessageAction(
            label='message',
            text='message text'
        ),
        URIAction(
            label='uri',
            uri='http://example.com/'
        )
    ]   
)

buttons_template_message = TemplateSendMessage(
    alt_text='Buttons template',
    template=template
    )

json_obj = json.dumps(template)
with open('button.json','w',encoding='utf-8') as f:
    f.write(json.loads(json_obj))
