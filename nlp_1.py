import jieba
import math
import re

class TraversalFun():

    # 初始化 处理文本
    def __init__(self, rootDir):
        self.rootDir = rootDir

    def TraversalDir(self):
        return TraversalFun.getCorpus(self, self.rootDir)

    def getCorpus(self, rootDir):
        corpus = []
        count=0
        with open(rootDir, "r", encoding='ansi') as file:
            filecontext = file.read()
            filecontext = re.sub(r'[(，)(。)(, )(\u3000)(：“)(“)(”)(》)(《)(’)(”)(？)(（)(）)(！)(.)(cr173)(www)(com)(txt)(、)(‘)(·)(、)]', '', filecontext)
            filecontext = filecontext.replace("\n", '')
            filecontext = filecontext.replace(" ", '')
            filecontext = filecontext.replace("本书来自www.cr173.com免费txt小说下载站\n更多更新免费电子书请关注www.cr173.com", '')
            seg_list = jieba.cut(filecontext, cut_all=True)
            corpus += seg_list
          #  print(corpus)
            count += len(filecontext)
            corpus.append(filecontext)
        return corpus,count

def cal_unigram(corpus,count):
    split_words = []
    words_len = 0
    line_count = 0
    words_tf = {}
    for line in corpus:
        for x in jieba.cut(line):
            split_words.append(x)
            words_len += 1
        get_tf(words_tf, split_words)
        split_words = []
        line_count += 1

    print("小说字数:", count)
    print("分词个数:", words_len)
    print("平均词长:", round(count / words_len, 5))
    entropy = []
    for uni_word in words_tf.items():
        entropy.append(-(uni_word[1] / words_len) * math.log(uni_word[1] / words_len, 2))
    print("一元模型中文信息熵为:", round(sum(entropy), 5), "比特/词")

def cal_bigram(corpus):

        split_words = []
        words_len = 0
        line_count = 0
        words_tf = {}
        bigram_tf = {}

        for line in corpus:
            for x in jieba.cut(line):
                split_words.append(x)
                words_len += 1

            get_tf(words_tf, split_words)
            get_bigram_tf(bigram_tf, split_words)

            split_words = []
            line_count += 1


        bigram_len = sum([dic[1] for dic in bigram_tf.items()])
        print("二元模型长度:", bigram_len)

        entropy = []
        for bi_word in bigram_tf.items():
            jp_xy = bi_word[1] / bigram_len  # 计算联合概率p(x,y)
            cp_xy = bi_word[1] / words_tf[bi_word[0][0]]  # 计算条件概率p(x|y)
            entropy.append(-jp_xy * math.log(cp_xy, 2))  # 计算二元模型的信息熵
        print("二元模型的中文信息熵为:", round(sum(entropy), 5), "比特/词")



def cal_trigram(corpus):
        split_words = []
        words_len = 0
        line_count = 0
        words_tf = {}
        trigram_tf = {}

        for line in corpus:
            for x in jieba.cut(line):
                split_words.append(x)
                words_len += 1

            get_bigram_tf(words_tf, split_words)
            get_trigram_tf(trigram_tf, split_words)

            split_words = []
            line_count += 1


        trigram_len = sum([dic[1] for dic in trigram_tf.items()])
        print("三元模型长度:", trigram_len)

        entropy = []
        for tri_word in trigram_tf.items():
            jp_xy = tri_word[1] / trigram_len  # 计算联合概率p(x,y)
            cp_xy = tri_word[1] / words_tf[tri_word[0][0]]  # 计算条件概率p(x|y)
            entropy.append(-jp_xy * math.log(cp_xy, 2))  # 计算三元模型的信息熵
        print("三元模型的中文信息熵为:", round(sum(entropy), 5), "比特/词")






# 词频统计，方便计算信息熵
def get_tf(tf_dic, words):

    for i in range(len(words)-1):
        tf_dic[words[i]] = tf_dic.get(words[i], 0) + 1

def get_bigram_tf(tf_dic, words):
    for i in range(len(words)-1):
        tf_dic[(words[i], words[i+1])] = tf_dic.get((words[i], words[i+1]), 0) + 1

def get_trigram_tf(tf_dic, words):
    for i in range(len(words)-2):
        tf_dic[((words[i], words[i+1]), words[i+2])] = tf_dic.get(((words[i], words[i+1]), words[i+2]), 0) + 1



if __name__ == '__main__':
    tra = TraversalFun("./data/鹿鼎记.txt")
    corpus,count = tra.TraversalDir()
    cal_unigram(corpus,count)
    cal_bigram(corpus)
    cal_trigram(corpus)