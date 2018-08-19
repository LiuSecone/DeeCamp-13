#encoding=utf-8
import sys
import jieba
import codecs
import os
class Seg(object):
    stopwords = []
    synonym_dict = {}
    stopword_filepath="dataset/stopword.txt"

    def __init__(self):
        self.read_in_stopword()
        self.load_synonym_dict()
        jieba.load_userdict('dataset/dictionary.txt')

    def read_in_stopword(self):#读入停用词
        print(os.getcwd())
        file_obj = codecs.open(self.stopword_filepath,'r','utf-8')
        while True:
            line = file_obj.readline()
            line=line.strip()
            if not line:
                break
            self.stopwords.append(line)
            # print(line)
        self.stopwords.append(' ')
        file_obj.close()

    def cut(self,sentence,stopword=True):
        for exp in self.synonym_dict:
            if exp in sentence:
                sentence = sentence.replace(exp,self.synonym_dict[exp])
        seg_list = jieba.cut(sentence)#切词

        results = []
        for seg in seg_list:
            if seg in self.stopwords and stopword:
                continue#去除停用词
            results.append(seg)
        return results
            
    def cut_for_search(self,sentence):
        for exp in self.synonym_dict:
            if exp in sentence:
                sentence = sentence.replace(exp,self.synonym_dict[exp])

        seg_list = jieba.cut_for_search(sentence)
        results = []
        for seg in seg_list:
            if seg in self.stopwords:
                continue
            results.append(seg)

        return results

    def load_synonym_dict(self,synonym_dict_path='dataset/synonym_dictionaries.txt'):
        # loading synonym dict
        with open(synonym_dict_path, 'r',encoding = 'utf-8') as f:
            lines = f.readlines()
            for line in lines:
                line = line.strip()
                uniform_exp = line.split(":")[0]
                other_exp = line.split(":")[1].split(',')
                for exp in other_exp:
                    self.synonym_dict[exp] = uniform_exp
        for word in self.synonym_dict:
            print(word, self.synonym_dict[word])