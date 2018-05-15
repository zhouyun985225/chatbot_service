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
    def __init__(self):
        self.cnx = mysql.connector.connect(user='cdidev', password='Philips@123',host='rm-uf6e87o934505d1162o.mysql.rds.aliyuncs.com',database='trueview_chatbot')
        self.cursor = self.cnx.cursor()
        print("server info: %s",self.cnx.connection_id)

    def insert_dialog(self, userid, question, answer):
        self.cursor.callproc('insert_dialog',(userid, null, question, answer, null, null, null))
        