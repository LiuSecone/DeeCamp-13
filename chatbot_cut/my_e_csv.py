import re
import sys
import pickle
import csv
import numpy as np
from tqdm import tqdm

sys.path.append('..')

def main(limit=20, x_limit=3, y_limit=6):
    """执行程序
    Args:
        limit: 只输出句子长度小于limit的句子
    """
    from word_sequence import WordSequence

    print('load pretrained vec')
    word_vec = pickle.load(open('word_vec.pkl', 'rb'))

    print('extract lines')
    fp = open('zhihu.csv', 'r', errors='ignore',encoding='utf-8')
    x_data = []
    y_data = []
    i=0
    for line in tqdm(fp):
        #i+=1
        #if(i>10000):
        #    break
        line = line.replace('\n', '')
        x, y = line.split(',')
        x = x.split(' ')
        y = y.split(' ')
        x_data.append(x)
        y_data.append(y)

    print(len(x_data), len(y_data))
    for ask, answer in zip(x_data[:20], y_data[:20]):
        print(''.join(ask))
        print(''.join(answer))
        print('-' * 20)

    data = list(zip(x_data, y_data))
    data = [
        (x, y)
        for x, y in data
        if len(x) < limit \
        and len(y) < limit \
        and len(y) >= y_limit \
        and len(x) >= x_limit
    ]
    x_data, y_data = zip(*data)

    print('refine train data')

    train_data = x_data + y_data

    print('fit word_sequence')

    ws_input = WordSequence()

    ws_input.fit(train_data, max_features=100000)

    print('dump word_sequence')

    pickle.dump(
        (x_data, y_data, ws_input),
        open('chatbot.pkl', 'wb')
    )

    print('make embedding vecs')

    emb = np.zeros((len(ws_input), len(word_vec['</s>'])))

    np.random.seed(1)
    for word, ind in ws_input.dict.items():
        if word in word_vec:
            emb[ind] = word_vec[word]
        else:
            emb[ind] = np.random.random(size=(300,)) - 0.5

    print('dump emb')

    pickle.dump(
        emb,
        open('emb.pkl', 'wb')
    )

    print('done')


if __name__ == '__main__':
    main()
