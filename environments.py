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
TRUEVIEW_CHATBOT_MAX_DIALOG_COUNT = int(os.getenv('TRUEVIEW_CHATBOT_MAX_DIALOG_COUNT', '5'))

if ENVIRONMENT == 'development':
    CHATBOT_LISTENING_PORT = os.getenv("CHATBOT_LISTENING_PORT", "8080")
    WECHAT_TOKEN = os.getenv('WECHAT_TOKEN', 'trueai')
    WECHAT_APP_ID = os.getenv('WECHAT_APP_ID', 'wxc902464ae209ea6d')
    WECHAT_APP_SECRET = os.getenv('WECHAT_APP_SECRET', '22307f1b83958384510068ec450200f3')
    MYSQL_HOST = '127.0.0.1'
    MYSQL_USER = 'root'
    MYSQL_DATABASE_NAME = 'chatbot_service'
    MYSQL_PORT = 3306
    MYSQL_PASSWORD = 'Philips123'
    REDIS_HOST = '47.106.93.189'
    REDIS_PORT = 6379
    REDIS_PASSWORD = 'philips123'
    REDIS_EXPIRE_TIME = 7200
    IR_SERVICE_URL = os.getenv('IR_SERVICE_URL', 'http://localhost:9001/android')
   # CLASSIFY_URL = 'http://localhost:9000/android?q={0}&classify={1}'
    CLASSIFY_URL = os.getenv('CLASSIFY_URL', 'http://ec2-52-80-28-32.cn-north-1.compute.amazonaws.com.cn:9000/android?q={0}&classify={1}')
elif ENVIRONMENT == 'test':
    CHATBOT_LISTENING_PORT = os.getenv("CHATBOT_LISTENING_PORT", "8081")
    WECHAT_TOKEN = os.getenv('WECHAT_TOKEN', 'trueai')
    WECHAT_APP_ID = os.getenv('WECHAT_APP_ID', 'wxc902464ae209ea6d')
    WECHAT_APP_SECRET = os.getenv('WECHAT_APP_SECRET', '22307f1b83958384510068ec450200f3')
    MYSQL_HOST = os.getenv('MYSQL_HOST', 'ec2-52-80-28-32.cn-north-1.compute.amazonaws.com.cn')
    MYSQL_USER = os.getenv('MYSQL_USER','root')
    MYSQL_DATABASE_NAME = os.getenv('MYSQL_DATABASE_NAME', 'chatbot_service')
    MYSQL_PORT = int(os.getenv('MYSQL_PORT', '3306'))
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', 'Philips@123')
    REDIS_HOST = os.getenv('REDIS_HOST', 'ec2-52-80-28-32.cn-north-1.compute.amazonaws.com.cn')
    REDIS_PORT = int(os.getenv('REDIS_PORT', '6379'))
    REDIS_PASSWORD = os.getenv('REDIS_PASSWORD', '')
    REDIS_EXPIRE_TIME = int(os.getenv('REDIS_EXPIRE_TIME', '7200'))
    IR_SERVICE_URL = os.getenv('IR_SERVICE_URL', 'http://ec2-52-80-28-32.cn-north-1.compute.amazonaws.com.cn:9001/android')
    CLASSIFY_URL = os.getenv('CLASSIFY_URL', 'http://ec2-52-80-28-32.cn-north-1.compute.amazonaws.com.cn:9000/android?q={0}&classify={1}')
else:
    CHATBOT_LISTENING_PORT = os.getenv("CHATBOT_LISTENING_PORT", "8082")
    WECHAT_TOKEN = os.getenv('WECHAT_TOKEN', 'trueai')
    WECHAT_APP_ID = os.getenv('WECHAT_APP_ID', 'wx63efb6f9efadb72b')
    WECHAT_APP_SECRET = os.getenv('WECHAT_APP_SECRET', '45a4a1cdd8bd13e44e9ce26e763d931e')
    MYSQL_HOST = os.getenv('MYSQL_HOST', 'rm-uf6e87o934505d1162o.mysql.rds.aliyuncs.com')
    MYSQL_USER = os.getenv('MYSQL_USER', 'cdidev')
    MYSQL_DATABASE_NAME = os.getenv('MYSQL_DATABASE_NAME', 'chatbot_service')
    MYSQL_PORT = int(os.getenv('MYSQL_PORT', '3306'))
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', 'Philips123')
    REDIS_HOST = os.getenv('REDIS_HOST', 'r-uf6de3a867308ef4.redis.rds.aliyuncs.com')
    REDIS_PORT = int(os.getenv('REDIS_PORT', '6379'))
    REDIS_PASSWORD = os.getenv('REDIS_PASSWORD', '')
    REDIS_EXPIRE_TIME = int(os.getenv('REDIS_EXPIRE_TIME', '7200'))
    IR_SERVICE_URL = os.getenv('IR_SERVICE_URL', 'https://www.cdip.philips.com.cn/test/oncology-chatbot-ir/android')
    CLASSIFY_URL = os.getenv('CLASSIFY_URL', "https://www.cdip.philips.com.cn/test/oncology-chatbot-classify/android?q={0}&classify={1}")
