import os
import re
import jieba
import datetime

cur_path = os.path.normpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
res_path = os.path.join(cur_path, 'resource')

def calDatetime(n):
    today = datetime.date.today()
    timeDelta = datetime.timedelta(days=n)
    return today + timeDelta

dateList = {
       '大前天': calDatetime(-3),
       '前天': calDatetime(-2),
       '昨天': calDatetime(-1),
       '今天': calDatetime(0),
       '明天': calDatetime(1),
       '后天': calDatetime(2),
       '大后天': calDatetime(3)
}

def containDate(tokenList):
    indicator = None
    day = None
    for token in tokenList:
        if token in dateList.keys():
            day = dateList[token]
            indicator = token
    return indicator, day

def containCity(tokenList, cityList):
    city = None
    for token in tokenList:
        if token in cityList:
            city = token
    return city

def weatherWord(tokenList):
    isWeatherQ = False
    seedWords = r'天气|风|雨|太阳|云'
    for token in tokenList:
        if re.search(seedWords, token):
            isWeatherQ = True
    return isWeatherQ

def answerWeather(question, commonInfo, cityList):
    answer = None
    tokenList = list(jieba.cut(question))
    isWeatherQ = weatherWord(tokenList)
    city = containCity(tokenList, cityList)
    indicator, day = containDate(tokenList)
    if city == None:
        city = commonInfo['location']
    else:
        commonInfo['location'] = city
    if day != None:
        commonInfo['date'] = day
    else:
        indicator = '今天'
        day = datetime.date.today()
    if isWeatherQ and city:
        answer = '{city}{day}天气晴朗，微风，温度17摄氏度'.format(city = city, day = indicator)
    return answer, commonInfo