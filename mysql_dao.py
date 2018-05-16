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


if __name__ == "__main__":
    dao = mysql_dao()
    result=dao.insert_dialog('asdfkjc','缺点','放疗的缺点？','①放射治疗设备昂贵，治疗费用较高；②放射治疗工作人员要求全面和熟练，包括合格的放射治疗医生、放射物理、放射生物和熟练的放射技术人员；③放射治疗周期长，一般需1～2个月；④放射并发症较多，甚至引起部分功能丧失；⑤有些肿瘤，尤其是晚期肿瘤患者，放射治疗效果并不完好。')
    print (result)