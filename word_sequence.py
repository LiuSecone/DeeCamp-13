# encoding=utf-8
"""
WordSequence类

维护一个字典，把一个list（或者字符串）编码化，或者反向恢复

"""


import numpy as np
import os
import pickle

class WordSequence(object):
    """一个可以把句子编码化（index）的类
    """

    PAD_TAG = '<pad>'
    UNK_TAG = '<unk>'
    START_TAG = '<s>'
    END_TAG = '</s>'
    PAD = 0
    UNK = 1
    START = 2
    END = 3


    def __init__(self):
        """初始化基本的dict
        """
        if os.path.exists('dict.txt'):
            f = open('dict.txt', 'rb')
            self.dict = pickle.load(f)
            f.close()
        else:
            self.dict = {
                WordSequence.PAD_TAG: WordSequence.PAD,
                WordSequence.UNK_TAG: WordSequence.UNK,
                WordSequence.START_TAG: WordSequence.START,
                WordSequence.END_TAG: WordSequence.END,
            }
        self.fited = False



    def to_index(self, word):
        """把一个单字转换为index
        """
        assert self.fited, 'WordSequence 尚未 fit'
        if word in self.dict:
            return self.dict[word]
        return WordSequence.UNK


    def to_word(self, index):
        """把一个index转换为单字
        """
        assert self.fited, 'WordSequence 尚未 fit'
        for k, v in self.dict.items():
            if v == index:
                return k
        return WordSequence.UNK_TAG


    def size(self):
        """返回字典大小
        """
        assert self.fited, 'WordSequence 尚未 fit'
        return len(self.dict) + 1

    def __len__(self):
        """返回字典大小
        """
        return self.size()


    def fit(self, sentences, min_count=3, max_count=None, max_features=None):
        """训练 WordSequence
        Args:
            min_count 最小出现次数
            max_count 最大出现次数
            max_features 最大特征数

        ws = WordSequence()
        ws.fit([['hello', 'world']])
        """
        assert not self.fited, 'WordSequence 只能 fit 一次'

        count = {}
        for sentence in sentences:
            arr = list(sentence)
            for a in arr:
                if a not in count:
                    count[a] = 0
                count[a] += 1

        if min_count is not None:
            count = {k: v for k, v in count.items() if v >= min_count}

        if max_count is not None:
            count = {k: v for k, v in count.items() if v <= max_count}

        print('word len',len(count))

        # self.dict = {
        #     WordSequence.PAD_TAG: WordSequence.PAD,
        #     WordSequence.UNK_TAG: WordSequence.UNK,
        #     WordSequence.START_TAG: WordSequence.START,
        #     WordSequence.END_TAG: WordSequence.END,
        # }

        if isinstance(max_features, int):
            count = sorted(list(count.items()), key=lambda x: x[1])
            # 增量建词典这里其实是有点问题的，总词数超过max_features需要排掉出现次数最少的那些词
            # 增量建没有统计全部的词频，但应该不会到10w个词那么多
            if max_features is not None and len(count) > max_features:
                count = count[-int(max_features):]
            for w, _ in count:
                if w in self.dict:
                    continue
                self.dict[w] = len(self.dict)
        else:
            for w in sorted(count.keys()):
                if w in self.dict:
                    continue
                self.dict[w] = len(self.dict)

        f = open('dict.txt', 'wb')
        pickle.dump(self.dict, f)
        f.close()
        self.fited = True


    def transform(self,
                  sentence, max_len=None):
        """把句子转换为向量
        例如输入 ['a', 'b', 'c']
        输出 [1, 2, 3] 这个数字是字典里的编号，顺序没有意义
        """
        assert self.fited, 'WordSequence 尚未 fit'

        # if max_len is not None:
        #     r = [self.PAD] * max_len
        # else:
        #     r = [self.PAD] * len(sentence)

        if max_len is not None:
            r = [self.PAD] * max_len
        else:
            r = [self.PAD] * len(sentence)

        for index, a in enumerate(sentence):
            if max_len is not None and index >= len(r):
                break
            r[index] = self.to_index(a)

        return np.array(r)


    def inverse_transform(self, indices,
                          ignore_pad=False, ignore_unk=False,
                          ignore_start=False, ignore_end=False):
        """把向量转换为句子，和上面的相反
        """
        ret = []
        for i in indices:
            word = self.to_word(i)
            if word == WordSequence.PAD_TAG and ignore_pad:
                continue
            if word == WordSequence.UNK_TAG and ignore_unk:
                continue
            if word == WordSequence.START_TAG and ignore_start:
                continue
            if word == WordSequence.END_TAG and ignore_end:
                continue
            ret.append(word)

        return ret


def test():
    """测试
    """
    ws = WordSequence()
    ws.fit([
        ['第', '一', '句', '话'],
        ['第', '二', '句', '话']
    ],min_count=1)

    indice = ws.transform(['第', '三'])
    print(indice)

    back = ws.inverse_transform(indice)
    print(back)

if __name__ == '__main__':
    test()
