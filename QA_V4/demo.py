import sys
import os
import re
import jieba
from SKL import feature_selection

_curpath=os.path.normpath( os.path.join( os.getcwd(), os.path.dirname(__file__) ))
nb_path = os.path.join(_curpath, 'NaiveBayes')
skl_path = os.path.join(_curpath, 'SKL')
res_path = os.path.join(_curpath, 'resource')
sys.path.append(_curpath)
sys.path.append(nb_path)
sys.path.append(skl_path)
sys.path.append(res_path)


def tokenization(question, featureIDF, featureIndex, stopWordsList, sysnonymDict):
    pattern = r'[?？!！，,。、~\-@#￥%……&*\s+\.\\/_$^*\(\+\"\'\)\]+\|\[+【】“”（）]+|[0-9]+'
    text = re.sub(pattern, '', question)
    tokenList = list(jieba.cut(text.replace('\n', '')))
    seg_text0 = removeStopWords(list(tokenList), stopWordsList)
    seg_text1 = replaceSynonym(seg_text0, sysnonymDict)
    features = list(featureIDF.keys())
    vector = dict()
    featureCount = dict()
    for token in seg_text1:
        if token in features:
            if token in featureCount:
            # if featureIndex[token] in featureCount:
                featureCount[token] += 1
            else:
                featureCount[token] = 1
    featureTfidf = dict()
    for feature, count in featureCount.items():
        tf = count / len(tokenList)
        tfidf = float(featureIDF[feature]) * tf
        # vector[feature] = tfidf
        vector[featureIndex[feature]] = tfidf
        featureTfidf[feature] = tfidf
    return vector, featureTfidf


def removeStopWords(tokenList, stopWordsList):
    newTokenList = list()
    for token in tokenList:
        if token not in stopWordsList:
            newTokenList.append(token)
    return newTokenList

def replaceSynonym(tokenList, sysnonymDict):
    newTokenList = list()
    sysnonymList = sysnonymDict.keys()
    for token in tokenList:
        if token == '肚子':
            continue
        if token in sysnonymList:
            newTokenList.append(sysnonymDict[token])
        else:
            newTokenList.append(token)
    return newTokenList