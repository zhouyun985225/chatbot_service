# coding=utf8
from tools import *
import mysql.connector
import os
import json
import redis
from environments import *


@singleton
class MySqlDAO:

    def getConnection(self):
        cnx = None
        if ENVIRONMENT == 'development':
            cnx = mysql.connector.connect(user='root', password='Philips@123',
                                          host='localhost', database='chatbot_service')
        else:
            cnx = mysql.connector.connect(user='cdidev', password='Philips@123',
                                          host='rm-uf6e87o934505d1162o.mysql.rds.aliyuncs.com',
                                          database='chatbot_service')
        return cnx

    def insert_dialog(self, userid, sessionid, question, coreference_question, answer, ai_id, disease_type, disease, topic, dialog_status):
        if userid is None or question is None or answer is None:
            raise ValueError('some param is none')
        cnx = self.getConnection()
        cursor = cnx.cursor()

        cursor.callproc("insert_dialog_manage", (None, userid, sessionid, question, coreference_question, disease_type, disease, topic, dialog_status))
        cursor.execute("SELECT LAST_INSERT_ID();")
        dialog_manage_id = cursor.fetchone()

        cursor.callproc("insert_dialog", (userid, sessionid, question, answer, ai_id, dialog_manage_id[0], None))
        cursor.execute("SELECT LAST_INSERT_ID();")
        dialog_id = cursor.fetchone()

        cursor.execute("UPDATE `dialog_manage` SET `Dialog_id` = %s WHERE `Id` = %s;",
                       (dialog_id[0], dialog_manage_id[0]))

        cnx.commit()
        cursor.close()
        cnx.close()
        return dialog_id[0]

    def insert_ai_procedure(self, sessionid, question, intention, ir_answer, comprehen_answer):
        if question is None:
            raise ValueError('some param is none')
        cnx = self.getConnection()
        cursor = cnx.cursor()
        cursor.callproc("insert_ai_procedure", (sessionid, question, intention, ir_answer, None, None, comprehen_answer, None, 0, None))
        cursor.execute("SELECT LAST_INSERT_ID();")
        ai_procedure_id = cursor.fetchone()
        cnx.commit()
        cursor.close()
        cnx.close()
        return ai_procedure_id[0]

    def insert(self, sql):
        cnx = self.getConnection()
        cursor = cnx.cursor()

        try:
            cursor.execute(sql)
            cnx.commit()
        except:
            cnx.rollback()
        cursor.close()
        cnx.close()

    def query(self, sql):
        cnx = self.getConnection()
        cursor = cnx.cursor()

        try:
            cursor.execute(sql)
            results = cursor.fetchall()
            cnx.commit()
            return results
        except:
            print
            "Error: unable to fecth data"
        cursor.close()
        cnx.close()
