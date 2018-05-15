#coding=utf8
import werobot
import json
import requests
import time

from QA_V4 import console
from console import Answer
from mysql_dao import mysql_dao

sql_dao = mysql_dao()
Answerclass = Answer()

robot = werobot.WeRoBot(enable_session=False,
                        token='yelin1597532',
                        APP_ID='wx13fe1f4594768ce8',
                        APP_SECRET='1ac3c38ec9be75a1216bd3502f89bb50')
client = robot.client

@robot.handler
def answerQuestion(message):
    source = message.source
    target = message.target
    print("Source is : ",source)
    print("Target is : ",target)
    input = message.content
    answer = Answerclass.getanswer(input)

    sql_dao.insert_dialog(source,input,answer)
    print("Input Q : ",input)
    print("Answer A is : ",answer)
    print("Answer Type is : ",type(answer))
    return (answer)

# 让服务器监听在 0.0.0.0:8082
# robot.config['HOST'] = '0.0.0.0'
# robot.config['PORT'] = 8082
# robot.run()
