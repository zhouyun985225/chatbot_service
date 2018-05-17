#coding=utf8
import werobot
import json
import requests
import time
import os

from QA_V4 import console
from console import Answer
from mysql_dao import mysql_dao

sql_dao = mysql_dao()
Answerclass = Answer()

robot = werobot.WeRoBot(enable_session=False,
                        token=os.getenv('WECHAT_TOKEN','trueai'),
                        APP_ID=os.getenv('WECHAT_APP_ID','wx63efb6f9efadb72b'),
                        APP_SECRET=os.getenv('WECHAT_APP_SECRET','45a4a1cdd8bd13e44e9ce26e763d931e'))
client = robot.client

@robot.handler
def answerQuestion(message):
    source = message.source
    target = message.target
    print("Source is : ",source)
    print("Target is : ",target)
    question = message.content
    answer, coreference_answer = Answerclass.getanswer(question)

    sql_dao.insert_dialog(source,question,coreference_answer,answer)
    print("Input Q : ",question)
    print("Answer A is : ",answer)
    print("Answer Type is : ",type(answer))
    return (answer)

# 让服务器监听在 0.0.0.0:8082
# robot.config['HOST'] = '0.0.0.0'
# robot.config['PORT'] = 8082
# robot.run()
