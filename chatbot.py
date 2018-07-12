# coding=utf8
import werobot
import json
import requests
import time
import os

from QA_V5 import console
from console import Answer
from MySqlDAO import *
from RedisDAO import *
from environments import *

from User import *

class RobotService():
    def __init__(self, service_id):
        self.service_id = service_id
        self.sql_dao = MySqlDAO()
        self.cache_dao = RedisDAO()
        self.answer_class = Answer()

    def log_dialog(self, userID, session_id, question, coreferenceQuestion, answer, ai_id):
        return self.sql_dao.insert_dialog(userID, session_id, question, coreferenceQuestion, answer, ai_id)


    def log_ai_procedure(self, session_id, question, intention, ir_answer, comprehen_answer):
        return self.sql_dao.insert_ai_procedure(session_id, question, intention, ir_answer, comprehen_answer)


    def handle_question_from_user(self, userID, question):
        session_id = self.cache_dao.get_session_id(userID, self.service_id)
        print('session id', session_id)
        intention, scorevesus = self.answer_class.getIntention(question)
        if intention == 'other':
            other_answer = self.answer_class.getOtherAnswer(session_id, question)
            ai_id = self.log_ai_procedure(session_id, question,
                                    intention, None, other_answer)
            self.log_dialog(userID, session_id, question, question, other_answer, ai_id)
            self.cache_dao.cache_data(session_id, userID, self.service_id,
                                question, question, intention, other_answer)
            return other_answer
        else:
            ir_answer, coreference_question, result_json = self.answer_class.getIRAnswer(
                session_id, question)
            ai_id = self.log_ai_procedure(session_id, question, intention, json.dumps(
                result_json, ensure_ascii=False), ir_answer)
            self.log_dialog(userID, session_id, question,
                    coreference_question, ir_answer, ai_id)
            self.cache_dao.cache_data(session_id, userID, self.service_id,
                                question, coreference_question, intention, ir_answer)
            return ir_answer




if __name__ == "__main__":
    question = "乳腺癌饮食该注意什么？"
    user = User("Source")
    robot = RobotService("target")
    questions="question1"
    question_array = compose_question_array(questions)
    for question in question_array:
        user.send_message_to_robot(question, robot)
