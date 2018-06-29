import os

ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')

CHATBOT_LISTENING_PORT = ''
if ENVIRONMENT == 'development':
    CHATBOT_LISTENING_PORT = os.getenv("CHATBOT_LISTENING_PORT", "80")
else:
    CHATBOT_LISTENING_PORT = os.getenv("CHATBOT_LISTENING_PORT", "8082")

TULING_KEY = os.getenv('TULING_KEY', '302e70feb15347a9a497dc1d5d405bec')
TULING_URL = os.getenv('TULING_URL', 'http://www.tuling123.com/openapi/api')

IR_SERVICE_URL = os.getenv(
    'IR_SERVICE_URL', 'https://trueview.natappvip.cc/android?q=')

TULING_ENABLE = os.getenv('TULING_ENABLE', 'True')

WECHAT_TOKEN = ''
WECHAT_APP_ID = ''
WECHAT_APP_SECRET = ''
if ENVIRONMENT == 'development':
    WECHAT_TOKEN = os.getenv('WECHAT_TOKEN', 'yelin1597532')
    WECHAT_APP_ID = os.getenv('WECHAT_APP_ID', 'wx13fe1f4594768ce8')
    WECHAT_APP_SECRET = os.getenv(
        'WECHAT_APP_SECRET', '3a6b21f513146fda56d5f61d48361e43')
else:
    WECHAT_TOKEN = os.getenv('WECHAT_TOKEN', 'trueai')
    WECHAT_APP_ID = os.getenv('WECHAT_APP_ID', 'wx63efb6f9efadb72b')
    WECHAT_APP_SECRET = os.getenv(
        'WECHAT_APP_SECRET', '45a4a1cdd8bd13e44e9ce26e763d931e')

REDIS_EXPIRE_TIME = int(os.getenv('REDIS_EXPIRE_TIME', '60'))
TRUEVIEW_CHATBOT_MAX_DIALOG_COUNT = int(os.getenv('TRUEVIEW_CHATBOT_MAX_DIALOG_COUNT'),'5')