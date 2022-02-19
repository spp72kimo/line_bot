from linebot import LineBotApi

line_bot_api = LineBotApi('P8Q73gxhooUHWCXs7boN9tQRwLUOvHDNaAj/8AjvOCTqY0RdOgpu9gsOhZGojAXMiBjhjwuxWlvl0BloHSo+F/5uImCWEi5WP7El5nWpKnkAz56Ouxf31zqFlrsHsgVzVmnnUjiEW+BjOHJx9gNHwAdB04t89/1O/w1cDnyilFU=')

message_content = line_bot_api.get_message_content('15616365313132')
with open('pic', 'wb') as fd:
    for chunk in message_content.iter_content():
        fd.write(chunk)