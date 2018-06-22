# coding=utf8
import werobot
import json
import requests
import time
import os

from QA_V5 import console
from console import Answer
from mysql_dao import mysql_dao

sql_dao = mysql_dao()
Answerclass = Answer()

robot = None
if os.getenv('ENVIRONMENT','development') == 'development':
    robot = werobot.WeRoBot(enable_session=False,
                        token=os.getenv('WECHAT_TOKEN', 'yelin1597532'),
                        APP_ID=os.getenv(
                            'WECHAT_APP_ID', 'wx13fe1f4594768ce8'),
                        APP_SECRET=os.getenv('WECHAT_APP_SECRET', '3a6b21f513146fda56d5f61d48361e43'))
else:
    robot = werobot.WeRoBot(enable_session=False,
                        token=os.getenv('WECHAT_TOKEN', 'trueai'),
                        APP_ID=os.getenv(
                            'WECHAT_APP_ID', 'wx63efb6f9efadb72b'),
                        APP_SECRET=os.getenv('WECHAT_APP_SECRET', '45a4a1cdd8bd13e44e9ce26e763d931e'))

client = robot.client


def log_dialog(userID, question, coreferenceQuestion, answer, ai_id):
    return sql_dao.insert_dialog(userID, question, coreferenceQuestion, answer, ai_id)


def log_ai_procedure(question, intention, ir_answer, comprehen_answer):
    return sql_dao.insert_ai_procedure(question, intention, ir_answer, comprehen_answer)


def handle_question_from_user(userID, question):
    intention, scorevesus = Answerclass.getIntention(question)
    print(intention)
    if intention == 'other':
        other_answer = Answerclass.getOtherAnswer(question)
        ai_id = log_ai_procedure(question, intention, None, other_answer)
        log_dialog(userID, question, question, other_answer, ai_id)
        return other_answer
    else:
        ir_answer, coreference_question, result_json = Answerclass.getIRAnswer(
            question)
        ai_id = log_ai_procedure(question, intention, json.dumps(
            result_json, ensure_ascii=False), ir_answer)
        log_dialog(userID, question, coreference_question, ir_answer, ai_id)
        return ir_answer


@robot.text
def answerQuestion(message):  
    source = message.source
    target = message.target
    question = message.content
    
    answer = handle_question_from_user(source, question)
    return answer


if __name__ == "__main__":
    question = "乳腺癌饮食该注意什么？"
    answer = handle_question_from_user("source", question)
    print(answer)
