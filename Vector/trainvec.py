
from gensim.models import word2vec
import logging

# 主程序
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
sentences = word2vec.Text8Corpus(u"D:\chatbot org data\orgqaforvec.txt")  # 加载语料
model = word2vec.Word2Vec(sentences, size=200)  # 默认window=5

# 计算两个词的相似度/相关程度
y1 = model.similarity(u"腹泻", u"肚子疼")
print(u"【腹泻】和【肚子疼】的相似度为：", y1)
print("--------\n");

# 计算某个词的相关词列表
y2 = model.most_similar(u"疼", topn=20)  # 20个最相关的
print("和【疼】最相关的词有：\n")
for item in y2:
    print(item[0], item[1])
print( "--------\n")

# 保存模型，以便重用
model.save(u"书评.model")
# 对应的加载方式
# model_2 = word2vec.Word2Vec.load("text8.model")

# 以一种C语言可以解析的形式存储词向量
model.save_word2vec_format(u"书评.model.bin", binary=True)
# 对应的加载方式
# model_3 = word2vec.Word2Vec.load_word2vec_format("text8.model.bin", binary=True)

if __name__ == "__main__":
    pass
