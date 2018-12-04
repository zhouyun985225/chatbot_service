# coding=utf8
import werobot
import json
import requests
import time
import os
from random import choice

from QA_V5 import console
from QA_V5.console import Answer
from MySqlDAO import *
from RedisDAO import *
from environments import *
from environments import *

from User import *

answer_class = Answer()


class RobotService():
    def __init__(self, service_id):
        self.service_id = service_id
        self.sql_dao = MySqlDAO()
        self.cache_dao = RedisDAO()
        self.header = {'content-type': 'application/json'}
        self.number_list = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13']

    def dialog_manage(self, userID, session_id, question, coreferenceQuestion, intention, result_json, answer, disease_type, disease, topic, dialog_status):
        ai_id = self.sql_dao.insert_ai_procedure(session_id, question, intention, json.dumps(result_json, ensure_ascii=False), answer)
        self.sql_dao.insert_dialog(userID, session_id, question, coreferenceQuestion, answer, ai_id, disease_type, disease, topic, dialog_status)
        self.cache_dao.cache_data(session_id, userID, self.service_id, question, coreferenceQuestion, intention, answer)

    def handle_question_from_user(self, userID, question):
        session_id = self.cache_dao.get_session_id(userID, self.service_id)
        results = self.sql_dao.query("SELECT * FROM dialog_manage WHERE Session_id={0}".format(session_id))
        item = {"id": None, "dialog_id": None, "userinfo_id": None, "session_id": None, "question": None, "coreference_question": None, "gmt_time": None, "disease_type": None, "disease": None, "topic": None, "dialog_status": None}
        if results:
            res = results[-1]
            item['id'] = res[0]
            item['dialog_id'] = res[1]
            item['userinfo_id'] = res[2]
            item['session_id'] = res[3]
            item['question'] = res[4]
            item['coreference_question'] = res[5]
            item['gmt_time'] = res[6]
            item['disease_type'] = res[7]
            item['disease'] = res[8]
            item['topic'] = res[9]
            item['dialog_status'] = res[10]

        if item['disease_type'] == None:
            '''handle when question type is number'''
            question = self.disease_type_name(question)
        elif item['disease'] == None:
            question = self.disease_name(question)

        '''0. goto tumor calssify'''
        intention, scorevesus = answer_class.getIntention(question)

        '''1. get disease_type'''
        disease_type = self.disease_type_analysis(item, question)
        if disease_type == None or disease_type == 'other':
            if intention == 'other':
                dialog_status =  None
            else:
                dialog_status = question

            answer = "小主，为了更精准的为您解疑答惑，请告诉小谱您正在接受放射治疗（放疗）还是化学药物治疗（化疗）？\n请选择: 1 放疗  2 化疗"
            self.dialog_manage(userID, session_id, question, None, None, None, answer, None, None, None, dialog_status)
            return answer

        '''2. get disease name'''
        disease_name = self.disease_name_analysis(item, question)
        if disease_name == None or disease_name == 'other':
            answer = "小主，为了更精准的为您解疑答惑，请告诉小谱想咨询的肿瘤类型是：\n 1. 鼻腔肿瘤\n 2. 骨转移\n 3. 会阴癌\n 4. 面颈部肿瘤\n 5. 脑部恶心肿瘤\n 6. 盆腔癌\n 7. 前列腺癌\n 8. 四肢放疗\n 9. 直肠癌\n 10. 乳腺癌"
            self.dialog_manage(userID, session_id, question, None, None, None, answer, disease_type, None, None, item['dialog_status'])
            return answer
        else:
            if item['disease'] == None and item['dialog_status'] == None:
                answer = "小主，小谱已经了解您的情况了，请小主开始咨询{0}的问题吧".format(disease_name)
                self.dialog_manage(userID, session_id, question, None, None, None, answer, disease_type, disease_name, None, None)
                return answer
            elif item['dialog_status']:
                question = item['dialog_status']

        '''3. get topic name'''
        topic_name = self.topic_name_analysis(item, question, disease_type)

        '''4. goto IR'''
        if intention == 'other':
            answer = "对不起小主，小谱还在成长中，现在暂时只能回答「16病区放化疗宣教手冊」和[就医流程]问题。"
            self.dialog_manage(userID, session_id, question, None, 'other', None, answer, disease_type, disease_name, topic_name, None)
        else:
            if item['topic'] == None:
                lasttopic = ''
            else:
                lasttopic = item['topic']
            answer, coreference_question, result_json = answer_class.getIRAnswer(session_id, question, disease_type, disease_name, lasttopic, topic_name)
            self.dialog_manage(userID, session_id, question, coreference_question, 'tumor', result_json, answer, disease_type, disease_name, topic_name, None)

        return answer

    def disease_type_analysis(self, item, question):

        question = self.disease_type_name(question)

        '''1. get disease_type by DB'''
        type_db = item['disease_type']

        '''2. get disease_type by classifier'''
        type_classification = self.classifier(question, '类型')

        '''3. compare disease_type'''
        if type_classification == 'other' or type_classification == None:
            if type_db:
                return type_db
            else:
                return None
        elif type_classification == '放疗/化疗':
            if type_db:
                return type_db
            else:
                return None
        else:
            return type_classification

    def disease_name_analysis(self, item, question):

        question = self.disease_name(question)

        disease_db = item['disease']

        disease_classification = self.classifier(question, '疾病')

        if disease_classification == 'other' or disease_classification == None:
            if disease_db:
                return disease_db
            else:
                return None
        else:
            return disease_classification

    def topic_name_analysis(self, item, question, disease_type):
        question = self.topic_name(item['disease_type'], question)

        topic_db = item['topic']

        topic_classification = self.classifier(question, disease_type)

        if topic_classification == 'other' or topic_classification == None:
            if topic_db:
                return topic_db
            else:
                return None
        else:
            return topic_classification

    def disease_type_name(self, type_name):
        try:
            index = self.number_list.index(type_name)
            type_list = ['放疗', '化疗']
            return type_list[index]
        except:
            return type_name

    def disease_name(self, disease_name):
        try:
            index = self.number_list.index(disease_name)
            disease_name_list = ['鼻腔肿瘤', '骨转移', '会阴癌', '面颈部肿瘤', '脑部恶心肿瘤', '盆腔癌', '前列腺癌', '四肢放疗', '直肠癌', '乳腺癌']
            return disease_name_list[index]
        except:
            return disease_name

    def topic_name(self, type, topic_name):
        try:
            index = self.number_list.index(topic_name)
            if type == '放疗':
                '''放疗 radiotherapy'''
                type_set = ['癌症常见问题', '鼻腔肿瘤', '骨转移', '会阴癌', '面颈部肿瘤', '脑部恶心肿瘤', '盆腔癌', '前列腺癌', '四肢放疗', '直肠癌', '饮食护理', '疼痛', '营养']
            else:
                '''化疗 chemotherapy'''
                type_set = ['picc', '肝功能', '骨髓抑制', '化疗泵', '静脉', '皮肤护理', '四肢或躯体护理', '消化道', '饮食护理', '疼痛', '营养']
            return type_set[index]
        except:
            return topic_name

    def classifier(self, question, classify):
        response = requests.get(CLASSIFY_URL.format(question, classify), headers=self.header).json()
        if response:
            result = response['result']
        else:
            result = None
        return result


if __name__ == "__main__":
    question = "乳腺癌饮食该注意什么？"
    question = "复旦肿瘤医院的就医流程"
    user = User("Source")
    robot = RobotService("target")
    # answer = user.send_message_to_robot(question, robot)
    # print(answer)
    robot.dialog_manage('1', '1', 'hello', 'hi', 'other', None, 'world', 'fangliao', 'zhichangai', 'zhichangai', None)
    # item= {"disease_type":"放疗"}
    #
    # print(robot.disease_type_analysis(item,'化疗'))
