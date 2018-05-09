from sklearn import svm, datasets, metrics
from sklearn.externals import joblib
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import SGDClassifier
from sklearn.neighbors import KNeighborsClassifier
import os
import demo
# from sklearn.feature_extraction import DictVectorizer
from scipy.sparse import coo_matrix


data_path = 'trainVector.svm'
testPath = 'testVector.svm'
model_path = os.path.normpath(os.path.join(os.getcwd(), os.path.dirname(__file__) ))
res_path = os.path.join(os.path.dirname(model_path), 'resource')
K = 5000

def train():
    clf_svm = svm.SVC(probability=True)
    clf_NB = MultinomialNB()
    clf_lr = LogisticRegression()
    clf_rlr = SGDClassifier(penalty='elasticnet')
    clf_knn = KNeighborsClassifier()
    x_train, y_train = datasets.load_svmlight_file(data_path)
    clf_svm.fit(x_train,y_train)
    clf_NB.fit(x_train,y_train)
    clf_lr.fit(x_train,y_train)
    clf_knn.fit(x_train,y_train)
    clf_rlr.fit(x_train, y_train)
    joblib.dump(clf_svm, 'train_model.svm')
    joblib.dump(clf_NB, "train_model.nb")
    joblib.dump(clf_lr, 'train_model.lr')
    joblib.dump(clf_knn, 'train_model.knn')
    joblib.dump(clf_rlr, 'train_model.rlr')

def test():
    x_test, y_test = datasets.load_svmlight_file(testPath)
    x_train, y_train = datasets.load_svmlight_file(data_path)
    clf_svm = joblib.load("train_model.svm")
    clf_nb = joblib.load("train_model.nb")
    clf_lr = joblib.load("train_model.lr")
    clf_knn = joblib.load("train_model.knn")
    clf_rlr = joblib.load("train_model.rlr")
    # y_pre = clf_svm.predict(x_train)
    # y_pre = clf_nb.predict(x_train)
    # y_pre = clf_lr.predict(x_train)
    # y_pre = clf_knn.predict(x_train)
    y_pre = clf_rlr.predict(x_train)
    # class_probabilities = clf_rlr.predict_proba(x_train)
    print('Confusion Matrix: ',metrics.confusion_matrix(y_train, y_pre), sep = '\n')
    print('Accuracy Score: ',metrics.accuracy_score(y_train,y_pre)*100,'%',sep='')
    print('F1 Score: ',metrics.f1_score(y_train,y_pre)*100,'%',sep='')

def predict(question, clf_rlr):
    classmap = {1:'tumor', 0:'other'}
    vector, featureCount = demo.tokenization(question)
    # Multi class
    # vec = DictVectorizer()
    # vector = vec.fit_transform(vector).toarray()
    # LabelBinarizer().fit_transform(y)
    value = []
    row = []
    col = []
    # print (vector)
    for key, val in vector.items():
        row.append(eval(key)-1)
        value.append(val)
        col.append(0)
    coo = coo_matrix((value, (col, row)),shape=(1,K+1))
    pre = clf_lr.predict(coo)
    # class_probabilities = clf_lr.predict_proba(coo).tolist()[0]
    # pre = class_probabilities.index(max(class_probabilities))
    cl = classmap[pre[0]]
    # return cl, class_probabilities
    return (cl)


if __name__ == '__main__':
    train()
    # test()
    Q = '放疗'
    # Q = '上海明天天气怎么样？'
    cl = predict(Q)
    print (cl)