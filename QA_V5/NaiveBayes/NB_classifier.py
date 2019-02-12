#coding:utf8
import numpy as np
import os
import json
import re
import jieba
import csv
import codecs


idx_lbl = 'idx'
tfreq_lbl = "textfreq"
classes = ['tumor', 'other']
model_path = os.path.normpath(os.path.join( os.getcwd(), os.path.dirname(__file__) ))

def createDictionary(data):
    token_pool = {}
    for cl in classes:
        token_pool[cl] = []
    fr = open(data, 'r', encoding='utf8')
    for line in fr.readlines():
        cl = line.split("\t")[1].replace("__label__", "").strip()
        token_pool[cl].append(line.split("\t")[0].split(' '))
    token_dict = {}
    idx = 0
    for cl in classes:
        for token_list in token_pool[cl]:
            for token in token_list:
                if token in token_dict:
                    if cl in token_dict[token]:
                        token_dict[token][cl] += 1
                    else:
                        token_dict[token][cl] = 1
                else:
                    token_dict[token] = {}
                    token_dict[token][idx_lbl] = idx
                    idx += 1
                    token_dict[token][cl] = 1
    return token_dict


def saveDictToFile(tdict, filename):
    w = csv.writer(open(filename, "w", encoding='utf8', newline=''))
    for key, val in tdict.items():
        row = []
        row.append(key)
        row.append(val[idx_lbl])
        for cl in classes:
            if cl in val:
                row.append(cl + ':' + str(val[cl]))
            else:
                row.append(cl + ':' + '0')
        w.writerow(row)


def readFileToDict(filename):
    tdict = {}
    for row in csv.reader(codecs.open(filename, 'r', encoding='utf8')):
        try:
            tdict[row[0]] = {}
            tdict[row[0]][idx_lbl] = int(row[1])
            for i in range(2, len(row)):
                lbl, cnt = row[i].split(':')
                tdict[row[0]][lbl] = int(cnt)
        except:
            continue
    return tdict


class NaiveBayes:
    def __init__(self, class_labels, tdict):
        self.k = len(class_labels)
        self.priors = np.zeros((self.k, 1))             #prior probabilities for each class
        self.cctermp = np.zeros((len(tdict), self.k))   #class conditional term probabilities
        self.ctermcnt = np.zeros((self.k, 1))           # total number of terms in a class
        self.lbl_dict = dict(zip(class_labels, range(self.k)))
        self.class_labels = class_labels
        self.tdict = tdict


    def train(self, class_counts, tfidf_but_smoothing = True):
        # First learn the prior probabilities
        if len(class_counts) != len(self.priors):
            print ("error! number of classes don't match")
            return None
        for i in range(len(class_counts)):
            self.priors[i, 0] = class_counts[0] * 1.0 / sum(class_counts)

        # now learn the class conditional probabilities for each term
        for term, data in self.tdict.items():
            idx = data[idx_lbl]
            for cl in self.lbl_dict.keys():
                if cl in data:
                    self.cctermp[idx, self.lbl_dict[cl]] += data[cl]
                    self.ctermcnt[self.lbl_dict[cl], 0] += data[cl]

        # print self.cctermp
        if not tfidf_but_smoothing:
            for i in range(len(self.tdict)):
                for j in range(self.k):
                    self.cctermp[i,j] = (self.cctermp[i,j] + 1) * 1.0 / (self.ctermcnt[j] + len(self.tdict))
        else:
            for i in range(len(self.tdict)):
                for j in range(self.k):
                    if self.cctermp[i,j] > 0:
                        self.cctermp[i,j] = (self.cctermp[i,j] + 1) * np.log(self.ctermcnt[j] * 1.0 / self.cctermp[i,j])
        params = {}
        params['k'] = self.k
        params['cctermp'] = self.cctermp.tolist()
        params['priors'] = self.priors.tolist()
        with open("params.json", 'w', encoding='utf-8') as json_file:
            json.dump(params, json_file, ensure_ascii=False)


    def predict(self, tokens_list):
        text_vec = self.__createVectorRepresentation(tokens_list)
        class_score = [0] * self.k
        for i in range(self.k):
            log_class_conditional = np.log(self.cctermp[:,i] + 1e-14)
            class_score[i] = log_class_conditional.transpose().dot(text_vec)[0] + np.log(self.priors[i,0])
        transform_score = [(100+score) for score in class_score]
        score_rate = [score/sum(transform_score) for score in transform_score]
        if score_rate[0] > 0.5:
            preindex = 0
        else:
            preindex = 1
        return self.class_labels[preindex], score_rate
        # return self.class_labels[class_score.index(max(class_score))], score_rate


    def __createVectorRepresentation(self, tokens_list):
        vec = np.zeros((len(self.tdict), 1), dtype=np.int8)
        for token in tokens_list:
            if token in self.tdict:
                vec[self.tdict[token][idx_lbl], 0] += 1
        return vec


def calculateMetrics(right_label, pred_label):
    metrics = {}
    tp = 0
    tn = 0
    fp = 0
    fn = 0
    if len(right_label) != len(pred_label):
        print ('Number error')
        return None
    for i in range(len(right_label)):
        if pred_label[i] == 'tumor':
            if right_label[i] == pred_label[i]:
                tp += 1
            else:
                fp += 1
        elif pred_label[i] == 'other':
            if right_label[i] == pred_label[i]:
                tn += 1
            else:
                fn += 1
    metrics["tp"] = tp
    metrics["tn"] = tn
    metrics["fp"] = fp
    metrics["fn"] = fn
    return metrics


def test(retrain = True):
    root_path = r'C:\Work\Project\QA\NaiveBayes'
    training_data = os.path.join(root_path, 'train.txt')
    class_count = [2086, 2086]
    dictionary_path = os.path.join(os.getcwd(), 'dictionary.csv')
    # if not os.path.isfile(dictionary_path):
    if retrain == True:
        tdict = createDictionary(training_data)
        saveDictToFile(tdict, dictionary_path)
    else:
        tdict = readFileToDict(dictionary_path)

    dumbBayes = NaiveBayes(classes, tdict)
    if retrain == True:
        dumbBayes.train(class_count, False)
    else:
        with open("params.json", 'r', encoding='utf-8') as json_file:
            params = json.load(json_file)
        dumbBayes.k = params['k']
        dumbBayes.cctermp = np.array(params['cctermp'], dtype=float)
        dumbBayes.priors = np.array(params['priors'], dtype=float)

    right_label = []
    pred_label = []
    test_data = os.path.join(root_path, 'train.txt')
    fr = open(test_data, 'r', encoding='utf8')
    for line in fr.readlines():
        cl = line.split("\t")[1].replace("__label__", "").strip()
        right_label.append(cl)
        tokens_list = line.split("\t")[0].split(' ')
        pred_cl, score = dumbBayes.predict(tokens_list)
        pred_label.append(pred_cl)

    matric = calculateMetrics(right_label, pred_label)
    recall = matric['tp'] / (matric['tp'] + matric['fn'])
    precision = matric['tp'] / (matric['tp'] + matric['fp'])
    f1 = 2 * recall * precision / (recall + precision)
    accuracy = (matric['tp'] + matric['tn']) / (matric['tp'] + matric['tn'] + matric['fp'] + matric['fn'])
    print(matric)
    print ('recall', recall, 'precision', precision, 'f1', f1, 'accuracy', accuracy)


# def classifier(question, usrinfo, path = model_path):
def classifier(question, path = model_path):
    pattern = r'[?？!！，,。、~\-@#￥%……&*\s+\.\\/_$^*\(\+\"\'\)\]+\|\[+【】“”（）]+|[0-9]+'
    text = re.sub(pattern, '', question)
    seg_text = list(jieba.cut(text.replace('\n', '')))
    params_path = os.path.join(model_path, 'params.json')
    with open(params_path, 'r', encoding='utf-8') as json_file:
        params = json.load(json_file)
    dictionary_path = os.path.join(model_path, 'dictionary.csv')
    tdict = readFileToDict(dictionary_path)
    dumbBayes = NaiveBayes(classes, tdict)
    dumbBayes.k = params['k']
    dumbBayes.cctermp = np.array(params['cctermp'], dtype=float)
    dumbBayes.priors = np.array(params['priors'], dtype=float)
    prediction, classscore = dumbBayes.predict(seg_text)
    return (prediction, classscore)


if __name__ == "__main__":
    # test()
    Q = '上海'
    # # Q = '这是鼻息肉吗有东西刺激到鼻子就打喷嚏'
    # usrinfo = {}
    # # text = Q.encode('')
    cl = classifier(Q, model_path)
    print (cl)
    # test(retrain=False)