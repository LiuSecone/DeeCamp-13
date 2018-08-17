# encoding=utf-8
from gensim import corpora, models, similarities
from sentence import Sentence
from collections import defaultdict


class SentenceSimilarity():

    def __init__(self, seg):
        self.seg = seg

    def set_sentences(self, sentences):
        self.sentences = []

        for i in range(0, len(sentences)):
            self.sentences.append(Sentence(sentences[i], self.seg, i))

    # 获取切过词的句子
    def get_cuted_sentences(self):
        cuted_sentences = []
        #         i = 220
        for sentence in self.sentences:
            #             print(sentence.get_cuted_sentence())
            cuted_sentences.append(sentence.get_cuted_sentence())

        with open('dataset/question_cuted.txt', mode='w', encoding="utf-8") as output_f:
            for cut in cuted_sentences:
                output_f.write(' '.join(cut))

        return cuted_sentences

    # 构建其他复杂模型前需要的简单模型
    def simple_model(self, min_frequency=3):
        self.texts = self.get_cuted_sentences()

        # 删除低频词
        frequency = defaultdict(int)
        for text in self.texts:
            for token in text:
                frequency[token] += 1

        self.texts = [[token for token in text if frequency[token] > min_frequency] for text in self.texts]

        self.dictionary = corpora.Dictionary(self.texts)
        self.corpus_simple = [self.dictionary.doc2bow(text) for text in self.texts]

    # tfidf模型
    def TfidfModel(self):
        self.simple_model()

        # 转换模型
        self.model = models.TfidfModel(self.corpus_simple)
        self.corpus = self.model[self.corpus_simple]

        # 创建相似度矩阵
        self.index = similarities.MatrixSimilarity(self.corpus)

    def LsiModel(self):
        print('dict len:',len(self.dictionary))
        # 使用LSI模型进行相似度计算
        self.lsi_model = models.LsiModel(self.corpus, id2word=self.dictionary, num_topics=200)
        self.corpus_lsi = self.lsi_model[self.corpus]
        # 获取最重要的topic;num_topics选取的topic个数，num_words每个topic包含的单词个数
        print(self.lsi_model.show_topics(num_topics=20, num_words=10))
        self.similarity_lsi = similarities.Similarity('Similarity-LSI-index', self.corpus_lsi, num_features=len(self.dictionary), num_best=5)

    def sentence2vec(self, sentence):
        sentence = Sentence(sentence, self.seg)
        # print(sentence.get_origin_sentence())
        # print(sentence.get_cuted_sentence())
        vec_bow = self.dictionary.doc2bow(sentence.get_cuted_sentence())
        return self.model[vec_bow]

    # 求最相似的句子
    def similarity(self, sentence):
        sentence_vec = self.sentence2vec(sentence)
        sims = self.index[sentence_vec]

        # 按相似度降序排序
        sim_sort = sorted(list(enumerate(sims)), key=lambda item: item[1], reverse=True)
        top_10 = sim_sort[0:10]
        return top_10

    def lsi_similarity(self,sentence):
        sentence = Sentence(sentence, self.seg)
        vec_bow = self.dictionary.doc2bow(sentence.get_cuted_sentence())
        sims = self.similarity_lsi[self.lsi_model[vec_bow]]
        return sims


    def save_model(self):
        self.dictionary.save('model/model_dic.txt')
        corpora.MmCorpus.serialize('model/corpus_simple.txt', self.corpus_simple)
        corpora.MmCorpus.serialize('model/corpus_tfidf.txt', self.corpus)
        self.model.save('model/tfidf_model.txt')
        self.index.save('model/matrixSimilarity.txt')

    def restore_model(self):
        self.dictionary = corpora.Dictionary.load('model/model_dic.txt')
        self.corpus_simple = corpora.MmCorpus('model/corpus_simple.txt')
        self.corpus = corpora.MmCorpus('model/corpus_tfidf.txt')
        self.model = models.TfidfModel.load('model/tfidf_model.txt')
        self.index = similarities.MatrixSimilarity.load('model/matrixSimilarity.txt')

    def save_lsi_model(self):
        self.lsi_model.save('model/lsi_model.txt')
        corpora.MmCorpus.serialize('model/corpus_lsi.txt', self.corpus_lsi)
        self.similarity_lsi.save('model/sim_lsi.txt')

    def restore_lsi_model(self):
        self.similarity_lsi = similarities.Similarity.load('model/sim_lsi.txt')
        self.lsi_model = models.LsiModel.load('model/lsi_model.txt')
        self.corpus_lsi = corpora.MmCorpus('model/corpus_lsi.txt')