# coding:utf8
from NaiveBayes import NB_classifier
import requests
import os
import weatherJudge
import re
import jieba
import demo
from SKL import SKL_clf
from SKL import feature_selection
import datetime
import polling
from sklearn.externals import joblib

import json
import requests
import traceback


apiKey= '302e70feb15347a9a497dc1d5d405bec'
apiUrl= 'http://www.tuling123.com/openapi/api'
confidence_threshold=0.66

class TulingAutoReply:
    def __init__(self, tuling_key, tuling_url):
        self.key = tuling_key
        self.url = tuling_url

    def reply(self, unicode_str):
        body = {'key': self.key, 'info': unicode_str.encode('utf-8')}
        r = requests.post(self.url, data=body)
        r.encoding = 'utf-8'
        resp = r.text
        if resp is None or len(resp) == 0:
            return None
        try:
            js = json.loads(resp)
            if js['code'] == 100000:
                # return js['text'].replace('', 'n')
                return js['text']
            elif js['code'] == 200000:
                return js['url']
            else:
                return None
        except Exception:
            traceback.print_exc()
            return None

auto_reply = TulingAutoReply(apiKey, apiUrl) # key和url从图灵机器人网站上申请得到


class Answer:
    def __init__(self):
        self.confidence_cutoff = confidence_threshold
        # self.IR_url = 'http://161.92.141.209:9000/android?q='
        # self.IR_url = 'http://127.0.0.1:9000/android?q='
        # self.IR_url = 'http://rmcdf8.natappfree.cc/android?q='
        # self.IR_url = os.getenv('IR_SERVICE_PROTOCOL','https')+'://'+os.getenv('IR_SERVICE_IP','trueview.natappvip.cc')+':'+os.getenv('IR_SERVICE_PORT','443')+'/android?q='
        self.IR_url = os.getenv('IR_SERVICE_PROTOCOL','http')+'://'+os.getenv('IR_SERVICE_IP','106.15.162.17')+':'+os.getenv('IR_SERVICE_PORT','9000')+'/android?q='
        self.commonInformation = {
            'location': None,
            'hospital': None,
            'date': datetime.date.today().strftime('%Y-%m-%d'),
            'disease': None
        }
        self.cur_path = os.path.normpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
        self.res_path = os.path.join(self.cur_path, 'resource')

        # It is so slow to load the dictionary
        jieba.load_userdict(os.path.join(self.res_path, 'userdict.txt'))
        self.loadFeature()
        self.loadStopword()
        self.loadSynonym()
        self.loadCityName()


    def loadFeature(self):
        featurePath = os.path.join(demo.skl_path, 'feature.csv')
        self.featureDic, self.featureIDF, self.featureIndex = feature_selection.readFeature(featurePath)

    def loadStopword(self):
        stopwordspath = os.path.join(demo.res_path, 'stopwords.txt')
        self.stopWordsList = list()
        with open(stopwordspath, 'r', encoding='utf8') as swf:
            for line in swf.readlines():
                self.stopWordsList.append(line.strip())
        swf.close()

    def loadSynonym(self):
        synonympath = os.path.join(demo.res_path, 'synonym.txt')
        self.sysnonymDict = dict()
        with open(synonympath, 'r', encoding='utf8') as snf:
            lines = snf.readlines()
            for i in range(len(lines)):
                if lines[i].startswith('#'):
                    seedWord = lines[i].strip().strip('#')
                    self.sysnonymDict[seedWord] = list()
                    continue
                if lines[i] != '\n':
                    self.sysnonymDict[lines[i].strip()] = seedWord
                else:
                    continue
        snf.close()

    def loadCityName(self):
        cityFilePath = os.path.join(demo.res_path, 'city_name.txt')
        cityfile = open(cityFilePath, 'r', encoding='utf8')
        raw_city_list = cityfile.read().split('\t')
        namefix = r'(市|特别行政区|州|地区|林区|县)$'
        self.cityList = [re.sub(namefix, '', city) for city in raw_city_list]

    def loadClfModel(self):
        rlr_model_path = os.path.join(demo.skl_path, 'train_model.rlr')
        self.clf_rlr = joblib.load(rlr_model_path)

    def getIntention(self, question):
        intention, scorevesus = NB_classifier.classifier(question)
        return intention, scorevesus

    def getOtherAnswer(self, question):
        rep = auto_reply.reply(question) + '[非肿瘤相关问题,回答仅供参考]'
        return rep

    def getIRAnswer(self, question):
        header = {'content-type': 'application/json'}
        url = self.IR_url + question

        r = requests.get(url, headers=header).json()
        print (r)
        if r == {}:
            return '此问题请咨询专业人士[肿瘤相关问题, No Replay]', question, None
        else:
            result = r['result'][0]
        answer = result['answer']
        original_question = result['question']
        confidence = result['score']

        if confidence > self.confidence_cutoff:
            rep = answer + '[肿瘤相关问题,回答仅供参考]'
            return rep, original_question, result
        else:
            return '此问题请咨询专业人士[肿瘤相关问题, Low confidence score]',original_question, result

            
    def getanswer(self, question):
        
        # weatherAnswer, commonInformation = weatherJudge.answerWeather(question, self.commonInformation, self.cityList)
        # if weatherAnswer != None:
        #    return weatherAnswer
        # else:
        intention, scorevesus = NB_classifier.classifier(question)
         # intention = SKL_clf.predict(self.question, self.clf_rlr)
        # print (intention)
        if intention == 'other':
            # return 'Call chat buddy'   # to tuling Chatbot
            # print('flag')
            rep = auto_reply.reply(question) + '[非肿瘤相关问题,回答仅供参考]'
            return rep, question, intention
        else:
            # body = {
            #     "question": question,
            #     "usrinfo": [usrinfo]
            #     }
            header = {'content-type': 'application/json'}
            url = self.IR_url + question
            # url = 'url"Q"'.format(url = IR_url, Q = question)
            # r = requests.post(IR_url, headers=header, data=json.dumps(body))
            # r = requests.get(url, headers=header).text

            r = requests.get(url, headers=header).json()
            print (r)

            if r == {}:
                # return 'Professionnal answer required (No answer)'  # manual service required
                return '此问题请咨询专业人士[肿瘤相关问题, No Replay]', question, intention
            else:
                result = r['result'][0]
            answer = result['answer']
            original_question = result['question']
            confidence = result['score']

            # Todo: Compare answers from different sources

            if confidence > self.confidence_cutoff:
                rep = answer + '[肿瘤相关问题,回答仅供参考]'
                # validationScore, validList = self.validifyAnswer(question,original_question)
                # validationScore, validList = self.validifyAnswer(question,answer)
                # if validationScore == 0.5:
                    # answer = '{answer}【回答仅供参考】'.format(answer = answer)
                #    answer = answer
                #elif validationScore == 1:
                #    answer = answer
                # else:
                    # return 'Professionnal answer required (validation failed)'
                #    return '此问题请咨询专业人士(Validation failed)'
                return rep, original_question, intention
            else:
                return '此问题请咨询专业人士[肿瘤相关问题, Low confidence score]',original_question, intention
                # return 'Professionnal answer required (Low confidence score)'


    def validifyAnswer(self, question, answer):
        pattern = r'[?？!！，,。、~\-@#￥%……&*\s+\.\\/_$^*\(\+\"\'\)\]+\|\[+【】“”（）]+|[0-9]+'
        vector, featureTfidf = demo.tokenization(question, self.featureIDF, self.featureIndex, self.stopWordsList, self.sysnonymDict)
        scores = list(vector.values())
        feature_word = list()
        if len(vector) == 0:
            return 0, []
        if len(scores) > 1:
            max_score = max(scores)
            scores.remove(max_score)
            secondMax_score = max(scores)
            for key, val in featureTfidf.items():
            # for key, val in vector.items():
                if float(val) == max_score:
                    if len(feature_word) == 0:
                        feature_word.append(key)
                    elif len(feature_word) == 2:
                        feature_word[0] = key
                if float(val) == secondMax_score:
                    if len(feature_word) == 0:
                        feature_word.extend([key, key])
                    elif len(feature_word) == 1:
                        feature_word.append(key)
        else:
            feature_word.append(list(featureTfidf.keys())[0])
            # feature_word.append(list(vector.keys())[0])
        answerText = re.sub(pattern, '', answer)
        answerTokenList = list(jieba.cut(answerText.replace('\n', '')))
        validationScore = 0
        validList = list()
        for feature in feature_word:
            if feature in answerTokenList:
                validationScore += 0.5
                validList.append(feature)
        return validationScore, validList

def main():
    while True:
        usrinfo = {}
        Answerclass = Answer()
        try:
            question = polling.poll(
                lambda: input(),
                ignore_exceptions=(IOError,),
                timeout=10,
                step=0.1)
            if question:
                answer = Answerclass.getanswer(question)
                print (answer)
        except:
            raise
            pass


if __name__ == '__main__':
    Q = '放疗导致的味觉迟钝怎样处理?'
    # Q = '胃癌吃饭应该注意什么？'
    # Q = '肿瘤克星精准放疗'
    # Q = '在哪里'
    # Q = '2018年世界杯足球赛'
    # Q = '你好 你是谁'
     # Q = '上海明天天气怎么样？'
    # Q = '这是鼻息肉吗有东西刺激到鼻子就打喷嚏'
    # usrinfo = {}
    Answerclass = Answer()
    answer = Answerclass.getanswer(Q)
    print(answer)
    # main()