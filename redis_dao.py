# coding=utf8
from tools import *
from environments import *
import json
import redis
import os

session_id_manage_key = 'TRUEVIEW_CHATBOT_SESSION_ID'
session_id_key_temp = 'TRUEVIEW_CHATBOT_SESSION_ID_{0}_{1}'

@singleton
class redis_dao:
    def get_connection(self):
        r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, charset='utf-8')
        return r

    def generate_new_session_id(self):
        r = self.get_connection()
        id = str(r.incr(session_id_manage_key))
        return id
        
    def get_session_id(self, user_id=None, service_id=None):
        session_id_key = session_id_key_temp.format(user_id, service_id)
        r = self.get_connection()
        with r.pipeline() as pipe:
            pipe.watch(session_id_key)
            session_id = pipe.get(session_id_key)
            if session_id == None:
                session_id = self.generate_new_session_id()
                pipe.multi()
                pipe.set(session_id_key, session_id)
            else:
                # simple number get from redis will be treated as bytes
                session_id = session_id.decode('utf-8')
            pipe.expire(session_id_key, REDIS_EXPIRE_TIME)
            pipe.execute()
            return session_id
        
    def cache_data(self, session_id=None, user_id=None, service_id=None, question=None, coreference=None, intention=None, answer=None):
        if coreference == None:
            coreference = question
        session_id = str(self.get_session_id(user_id, service_id))
        r = self.get_connection()
        with r.pipeline() as pipe:
            pipe.watch(session_id)
            dataStr = pipe.get(session_id)
            data = {}
            if dataStr != None:
                data = json.loads(dataStr,encoding='utf-8')
            dialogs = []
            if 'dialogs' not in data or data['dialogs'] == None:
                data = {'session_id':session_id, 'user_id':user_id, 'dialogs':[]}
            dialogs = data['dialogs']
            lastDialogNumber = 0
            if len(dialogs) > 0:
                lastDialogNumber = dialogs[len(dialogs)-1]['dialog_number']
            if len(dialogs) >= TRUEVIEW_CHATBOT_MAX_DIALOG_COUNT:
                del dialogs[0]
            insertObject = {'dialog_number': lastDialogNumber+1, 'question':question, 'coreference':coreference,'intention':intention,'answer':answer}
            dialogs.append(insertObject)
            data['dialogs'] = dialogs
            string = json.dumps(data, ensure_ascii=False)
            pipe.multi()
            pipe.set(session_id, string)
            pipe.expire(session_id, REDIS_EXPIRE_TIME)
            pipe.execute()
            return session_id

    def get_cached_data(session_id=None):
        r = self.get_connection()
        dataStr = r.get(session_id)
        data = {}
        if dataStr != None:
            data = json.loads(dataStr,encoding='utf-8')
        return data

if __name__ == "__main__":
    redisDAO=redis_dao()
    userID='123456'
    serviceID='654321'
    session_id=redisDAO.get_session_id(user_id=userID,service_id=serviceID)
    redisDAO.cache_data(session_id=session_id,user_id=userID,service_id=serviceID,question='什么是洗鼻？',coreference='啥是洗鼻？',intention='tumor',answer='概念：主要是借用一定压力（或吸、或用重力、或用机械压力）将生理盐水送入鼻孔，流经鼻前庭（露在头部外面的部分）、鼻窦、鼻道绕经鼻咽部，或从一侧鼻孔排出，或从口部排出。通过以上路径，借助于生理盐水自身的杀菌作用及水流的冲击力，将鼻腔内己聚集的致病及污湄排出，从而使鼻腔恢复正常的生理环境，恢复鼻腔的自我排毒功能，达到保护鼻腔的目的。适应人群：鼻腔肿瘤化疗后，放疗期间和治疗结束以后，鼻腔手术患者，过敏性鼻炎、鼻窦炎，，长期在粉尘等严重环境中的工作者。目的：鼻腔肿瘤放疗过程中鼻腔、鼻窦和鼻咽颅底不可避免地受到照射后引起充血肿胀，出现与口腔黏膜相似的鼻腔黏膜反应，鼻咽癌患者常有鼻黏膜干燥、鼻塞、鼻腔分泌物增多、黏稠。有效预防鼻腔粘连，以清除鼻咽腔黏膜表面的分泌物，减轻放疗反应，增加癌细胞对放射线的敏感度。')
