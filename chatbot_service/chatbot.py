#coding=utf8
import werobot
import json
import requests
import time

from QA_V4 import console
from console import Answer

robot = werobot.WeRoBot(enable_session=False,
                        token='yelin1597532',
                        # test account
                        # APP_ID='wx7a4560f95a2cee84',
                        # APP_SECRET='97ee7e0e015eb4c5b9b8eaf2c7f561b6')
                        APP_ID='wx13fe1f4594768ce8',
                        APP_SECRET='1ac3c38ec9be75a1216bd3502f89bb50')
# Answerclass = Answer()
client = robot.client

@robot.handler
def answerQuestion(message):
    source = message.source
    target = message.target
    print("Source is : ",source)
    print("Target is : ",target)
    input = message.content
    answer = Answerclass.getanswer(input)
    print("Input Q : ",input)
    print("Answer A is : ",answer)
    print("Answer Type is : ",type(answer))
    return (answer)

# 让服务器监听在 0.0.0.0:8082
# robot.config['HOST'] = '0.0.0.0'
# robot.config['PORT'] = 8082
# robot.run()
