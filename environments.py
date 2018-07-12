import os

ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')

CHATBOT_LISTENING_PORT = ''
WECHAT_TOKEN = ''
WECHAT_APP_ID = ''
WECHAT_APP_SECRET = ''

TULING_ENABLE = os.getenv('TULING_ENABLE', 'True')
TULING_KEY = os.getenv('TULING_KEY', '302e70feb15347a9a497dc1d5d405bec')
TULING_URL = os.getenv('TULING_URL', 'http://www.tuling123.com/openapi/api')

REDIS_HOST = ''
REDIS_PORT = 6379
REDIS_PASSWORD = ''
REDIS_EXPIRE_TIME = 0
TRUEVIEW_CHATBOT_MAX_DIALOG_COUNT = int(os.getenv('TRUEVIEW_CHATBOT_MAX_DIALOG_COUNT','5'))
# IR_SERVICE_URL = os.getenv('IR_SERVICE_URL', 'http://139.224.76.93:9001/android')
IR_SERVICE_URL = os.getenv('IR_SERVICE_URL', 'http://139.224.76.93:9001/android')
    # self.IR_url = 'http://161.92.141.209:9000/android?q='
    # self.IR_url = 'http://127.0.0.1:9000/android?q='
    # self.IR_url = 'http://rmcdf8.natappfree.cc/android?q='
    # self.IR_url = 'https://trueview.natappvip.cc/android?q='
    # self.IR_url = 'http://trueview2.s1.natapp.cc/android?q='


if ENVIRONMENT == 'development':
    CHATBOT_LISTENING_PORT = os.getenv("CHATBOT_LISTENING_PORT", "80")
    WECHAT_TOKEN = os.getenv('WECHAT_TOKEN', 'yelin1597532')
    WECHAT_APP_ID = os.getenv('WECHAT_APP_ID', 'wx13fe1f4594768ce8')
    WECHAT_APP_SECRET = os.getenv('WECHAT_APP_SECRET', '3a6b21f513146fda56d5f61d48361e43')
    REDIS_HOST = '47.106.93.189'
    REDIS_PORT = 6379
    REDIS_PASSWORD = 'philips123'
    REDIS_EXPIRE_TIME = 5
else:
    CHATBOT_LISTENING_PORT = os.getenv("CHATBOT_LISTENING_PORT", "8082")
    WECHAT_TOKEN = os.getenv('WECHAT_TOKEN', 'trueai')
    WECHAT_APP_ID = os.getenv('WECHAT_APP_ID', 'wx63efb6f9efadb72b')
    WECHAT_APP_SECRET = os.getenv('WECHAT_APP_SECRET', '45a4a1cdd8bd13e44e9ce26e763d931e')
    REDIS_HOST = os.getenv('REDIS_HOST', 'r-uf6de3a867308ef4.redis.rds.aliyuncs.com')
    REDIS_PORT = int(os.getenv('REDIS_PORT', '6379'))
    REDIS_PASSWORD = os.getenv('REDIS_PASSWORD', '')
    REDIS_EXPIRE_TIME = int(os.getenv('REDIS_EXPIRE_TIME', '7200'))
