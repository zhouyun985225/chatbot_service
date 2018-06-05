# -*- coding: utf-8 -*-
import mysql.connector

def singleton(cls, *args, **kw):  
    instances = {}  
    def _singleton():  
        if cls not in instances:  
            instances[cls] = cls(*args, **kw)  
        return instances[cls]  
    return _singleton

@singleton
class mysql_dao:

    def insert_dialog(self, userid, question, coreference_question, answer):
        if userid is None or question is None or coreference_question is None or answer is None:
            raise ValueError('some param is none')
        cnx = mysql.connector.connect(user='cdidev', password='Philips@123',host='rm-uf6e87o934505d1162o.mysql.rds.aliyuncs.com',database='trueview_chatbot')
        cursor = cnx.cursor()

        cursor.callproc("insert_dialog_manage",(None,userid, None, question,coreference_question))
        cursor.execute("SELECT LAST_INSERT_ID();")
        dialog_manage_id=cursor.fetchone()

        cursor.callproc("insert_dialog",(userid,None, question, answer,None,dialog_manage_id[0],None))
        cursor.execute("SELECT LAST_INSERT_ID();")
        dialog_id=cursor.fetchone()

        cursor.execute("UPDATE `dialog_manage` SET `Dialog_id` = %s WHERE `Id` = %s;",(dialog_id[0],dialog_manage_id[0]))

        cnx.commit()
        cursor.close();
        cnx.close();
        return dialog_id[0];