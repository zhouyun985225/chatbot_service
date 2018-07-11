# coding=utf8
import werobot
import json
import requests
import time
import os

from QA_V5 import console
from console import Answer
from mysql_dao import *
from redis_dao import *
from environments import *

sql_dao = mysql_dao()
cache_dao = redis_dao()
Answerclass = Answer()

robot = werobot.WeRoBot(enable_session=False,
                        token=WECHAT_TOKEN,
                        APP_ID=WECHAT_APP_ID,
                        APP_SECRET=WECHAT_APP_SECRET)


client = robot.client


def log_dialog(userID, session_id, question, coreferenceQuestion, answer, ai_id):
    return sql_dao.insert_dialog(userID, session_id, question, coreferenceQuestion, answer, ai_id)


def log_ai_procedure(session_id, question, intention, ir_answer, comprehen_answer):
    return sql_dao.insert_ai_procedure(session_id, question, intention, ir_answer, comprehen_answer)


def handle_question_from_user(userID, serviceID, question):
    session_id = cache_dao.get_session_id(userID, serviceID)
    print ('session id', session_id)
    intention, scorevesus = Answerclass.getIntention(question)
    if intention == 'other':
        other_answer = Answerclass.getOtherAnswer(session_id, question)
        ai_id = log_ai_procedure(session_id, question, intention, None, other_answer)
        log_dialog(userID, session_id, question, question, other_answer, ai_id)
        cache_dao.cache_data(session_id, userID, serviceID, question, question, intention, other_answer)
        return other_answer
    else:
        ir_answer, coreference_question, result_json = Answerclass.getIRAnswer(session_id, question)
        ai_id = log_ai_procedure(session_id, question, intention, json.dumps(result_json, ensure_ascii=False), ir_answer)
        log_dialog(userID, session_id, question, coreference_question, ir_answer, ai_id)
        cache_dao.cache_data(session_id, userID, serviceID, question, coreference_question, intention, ir_answer)
        return ir_answer


@robot.text
def answerQuestion(message):
    source = message.source
    target = message.target
    question = message.content

    answer = handle_question_from_user(source, target, question)
    return answer


if __name__ == "__main__":
    question = "乳腺癌饮食该注意什么？"
    answer = handle_question_from_user("source", "target", question)
    print(answer)
