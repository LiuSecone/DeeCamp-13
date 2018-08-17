# encoding=utf-8

from cutWords import *
from sentenceSimilarity import SentenceSimilarity
train = True
if __name__ == '__main__':

    with open("dataset/question.txt",'r',encoding='utf-8') as rf :
        train_sentences = rf.readlines()

    # 读入测试集
    with open('dataset/test_input.txt','r',encoding='utf-8') as rf:
        raw_test_sentences = rf.readlines()
    test_sentences = []
    for sen in raw_test_sentences:
        test_sentences.append(sen.strip())

    for sen in test_sentences:
        print(sen)
    # 分词工具，基于jieba分词，并去除停用词
    seg = Seg()

    # 训练模型
    ss = SentenceSimilarity(seg)
    if train:
        ss.set_sentences(train_sentences)
        ss.TfidfModel()  # tfidf模型
        ss.save_model()
    else:
        ss.restore_model()

    # 测试集
    right_count = 0

    file_result = open('dataset/test_output.txt', 'w')

    with open("dataset/answer.txt", 'r', encoding='utf-8') as file_answer:
        line = file_answer.readlines()

    for i in range(0, len(test_sentences)):
        top_10 = ss.similarity(test_sentences[i])

        answer_index = top_10[0][0]
        answer = line[answer_index]
        file_result.write(test_sentences[i]+'\t')
        print(str(top_10[0][1]) + '\t' + str(answer))
        file_result.write(str(answer))

    file_result.close()