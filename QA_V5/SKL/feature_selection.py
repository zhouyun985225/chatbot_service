import codecs
import math
import csv
import os
from collections import OrderedDict
import random
import demo

n_doc = 5938
classes = ['tumor', 'other']
classmap = {'tumor':1, 'other':0}
K = 5000
model_path = os.path.normpath( os.path.join(os.getcwd(), os.path.dirname(__file__) ))


def buildTokenPool(dataPath):
    tokenPool = {}
    for cl in classes:
        tokenPool[cl] = []
    fr = open(dataPath, 'r', encoding='utf8')
    for line in fr.readlines():
        cl = line.split("\t")[1].replace("__label__", "").strip()
        tokenPool[cl].append(line.split("\t")[0].split(' '))
    return tokenPool

# Build dictionary for IDF statistics
def createDictionary(dataPath):
    tokenPool = buildTokenPool(dataPath)
    idfDict = {}

    for cl in classes:
        for tokenList in tokenPool[cl]:
            seg_text0 = demo.removeStopWords(list(tokenList))
            seg_text1 = demo.replaceSynonym(seg_text0)
            for token in list(set(list(seg_text1))):
                if token in idfDict:
                    if cl in idfDict[token]:
                        idfDict[token][cl] += 1
                    else:
                        idfDict[token][cl] = 1
                else:
                    idfDict[token] = {}
                    idfDict[token][cl] = 1
    return idfDict

# Calculate the chi-square value
def ChiCalc(a, b, c, d):
    result = float(pow((a*d - b*c), 2)) /float((a+c) * (a+b) * (b+d) * (c+d))
    return result


def featureSelection(termDic, K):
    chisquareDic = dict()
    for term in termDic:
        if classes[0] in termDic[term]:
            a = termDic[term][classes[0]]  # 在这个分类下包含这个词的文档数量
            c = n_doc/2 - a  # 在这个分类下不包含这个词的文档数量
        else:
            a = 0
            c = n_doc/2
        if classes[1] in termDic[term]:
            b = termDic[term][classes[1]]  # 不在该分类下包含这个词的文档数量
            d = n_doc/2 - b  # 不在该分类下，且不包含这个词的文档数量
        else:
            b = 0
            d = n_doc/2
        chisquare = ChiCalc(a, b, c, d)
        chisquareDic[term] = chisquare
    sortedChisquareDic = sorted(chisquareDic.items(), key=lambda d: d[1], reverse=True)
    print (sortedChisquareDic)
    featureDic = OrderedDict()
    for i in range(K):
        featureDic[sortedChisquareDic[i][0]] = sortedChisquareDic[i][1]
    print (featureDic)
    return featureDic


# def featureSelectionEX(termDic, K):
#     classTermCountDic = dict()
#     for cl in classes:
#         for term in termDic:
#             if len(termDic[term]) == 2:
#                 for term_cl in termDic[term]:
#                     if cl == term_cl:
#                         # print(cl, termDic[term])
#                         another_cl = classes[1 - classes.index(term_cl)]
#                         a = termDic[term][term_cl]  # 在这个分类下包含这个词的文档数量
#                         c = n_doc - a  # 在这个分类下不包含这个词的文档数量
#                     else:
#                         b = termDic[term][term_cl]  # 不在该分类下包含这个词的文档数量
#                         d = n_doc - b  # 不在该分类下，且不包含这个词的文档数量
#             else:
#                 if cl in termDic[term]:
#                     a = termDic[term][cl] # 在这个分类下包含这个词的文档数量
#                     c = n_doc - termDic[term][cl] # 在这个分类下不包含这个词的文档数量
#                     b = 0
#                     d = n_doc
#                 else:
#                     a = 0
#                     c = n_doc
#                     b = list(termDic[term].values())[0]
#                     d = n_doc - b
#
#             termCount = ChiCalc(a, b, c, d)
#             print(cl, term, termCount, a, b,c,d)
#             classTermCountDic[term] = termCount
#         sortedClassTermCountDic = sorted(classTermCountDic.items(), key=lambda d: d[1], reverse=True)
#         termCountDic = dict()
#         subDic = dict()
#         for i in range(K):
#             subDic[sortedClassTermCountDic[i][0]] = sortedClassTermCountDic[i][1]
#         print (cl)
#         print (sortedClassTermCountDic)
#
#         termCountDic[cl] = subDic
#     return termCountDic


def writeFeatureToFile(termCountDic, fileName):
    featureList = list()
    for key in termCountDic:
        featureList.append(key)
    count = 1
    file = open(fileName, 'w')
    for feature in featureList:
        if len(feature) > 0 and feature != " " :
            file.write(str(count)+" " +feature+"\n")
            count = count + 1
    file.close()

def featureWeight(data_path, featureDic):
    token_pool = buildTokenPool(data_path)
    featureIDF = dict()
    features = list(featureDic.keys())
    for feature in features:
        featureDocCount = 0
        totalDocCount = n_doc
        for cl in token_pool:
            for token_list in token_pool[cl]:
                if feature in token_list:
                    featureDocCount += 1
        idf = math.log(float(totalDocCount)/(featureDocCount+1))
        featureIDF[feature] = idf
    # featureTFIDF = dict()
    # for cl in token_pool:
    #     for token_list in token_pool[cl]:
    #         for i in range(len(features)):
    #             if features[i] in token_list:
    #                 featurecount = token_list.count(features[i])
    #                 tf = float(featurecount) / (len(token_list))
    #                 tfidf = featureIDF[features[i]] * tf
    #                 featureTFIDF[features[i]] = tfidf
    return featureIDF

def saveFeature(featurePath, featureDic, featureIDF):
    featureFile = csv.writer(open(featurePath, 'w', encoding='utf8', newline=''))
    index = 0
    header = ['Index', 'Term', 'Chi-square', 'IDF']
    featureFile.writerow(header)
    for feature, chisquare in featureDic.items():
        index += 1
        row = [index, feature, chisquare, featureIDF[feature]]
        featureFile.writerow(row)

def readFeature(featurePath):
    featurePath = os.path.join(model_path,'feature.csv')
    featureFile = csv.reader(codecs.open(featurePath, 'r', encoding='utf8'))
    featureDic = dict()
    featureIDF = dict()
    featureIndex = dict()
    for row in featureFile:
        try:
            featureDic[row[1]] = row[2]
            featureIDF[row[1]] = row[3]
            featureIndex[row[1]] = row[0]
        except:
            continue
    return featureDic, featureIDF, featureIndex


def buildVectorFile(dataPath, featurePath, vectorFilePath):
    vectorFile = open(vectorFilePath, 'w', encoding='utf8')
    tokenPool = buildTokenPool(dataPath)
    featureDic, featureIDF, featureIndex = readFeature(featurePath)
    features = list(featureIDF.keys())
    vectorList = []
    for cl in tokenPool:
        for tokenList in tokenPool[cl]:
            # vectorFile.write(str(classmap[cl]) + " ")
            seg_text0 = demo.removeStopWords(list(tokenList))
            seg_text1 = demo.replaceSynonym(seg_text0)
            vector = []
            vector.append(str(classmap[cl]))
            for i in range(1, len(features)):
                if features[i] in seg_text1:
                    featureCount = seg_text1.count(features[i])
                    tf = float(featureCount) / (len(tokenList))
                    tfidf = float(featureIDF[features[i]]) * tf
                    # vectorFile.write(str(i + 1) + ":" + str(tfidf) + " ")
                    # vector.append(features[i] + ":" + str(tfidf))
                    vector.append(str(i + 1) + ":" + str(tfidf))
            vectorList.append(vector)
            # vectorFile.write("\n")
    shuffleList = list(range(len(vectorList)))
    random.seed(12345)
    random.shuffle(shuffleList)

    for i in shuffleList:
        vectorFile.write(' '.join(vectorList[i]))
        vectorFile.write('\n')
    vectorFile.close()


if __name__ == '__main__':
    dataPath = os.path.join(os.getcwd(), 'train.txt')
    testData = os.path.join(os.getcwd(), 'test.txt')
    featurePath = 'feature.csv'
    trainVectorFilePath = 'trainVector.svm'
    testVectorFilePath = 'testVector.svm'
    termDic = createDictionary(dataPath)
    featureDic = featureSelection(termDic, K)
    featureIDF = featureWeight(dataPath, featureDic)
    saveFeature(featurePath, featureDic, featureIDF)
    buildVectorFile(dataPath, featurePath, trainVectorFilePath)
    buildVectorFile(testData, featurePath, testVectorFilePath)