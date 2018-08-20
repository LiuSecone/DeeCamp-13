#encoding=utf-8
from sentenceSimilarity import SentenceSimilarity
from cutWords import *
class Chatbot_port2(object):
    def __init__(self):
        # 分词工具，基于jieba分词，并去除停用词
        seg = Seg()
        self.ss = SentenceSimilarity(seg)
        self.ss.restore_model()
        with open("dataset/answer.txt", 'r', encoding='utf-8') as file_answer:
            self.line = file_answer.readlines()

    def chat(self,question):
        question = question.strip()
        top_10 = self.ss.similarity(question)

        answer_index = top_10[0][0]
        answer = self.line[answer_index]
        return answer,top_10[0][1]

if __name__ == '__main__':
    chatbot = Chatbot_port2()
    answer = chatbot.chat('你好。')
    print(answer)
    answer = chatbot.chat('请问，你来自哪里？')
    print(answer)
