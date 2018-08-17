
import sys
import random
import pickle
import os
import numpy as np
import tensorflow as tf
import jieba
from data_utils import batch_flow
sys.path.append('..')
from sequence_to_sequence import SequenceToSequence



class chatbot_port(object):
    def __init__(self):
        self.cell_type = 'lstm'
        self.depth = 2
        self.bidirectional = True
        self.attention_type = 'Bahdanau'
        self.use_residual = False
        self.use_dropout = False
        print("!!!!")
        self.time_major = False
        self.hidden_units = 512
        random.seed(0)
        np.random.seed(0)
        tf.set_random_seed(0)
        self.x_data, self._, self.ws = pickle.load(open('chatbot_cut/chatbot.pkl', 'rb'))
        self.config = tf.ConfigProto(
            device_count={'CPU': 1, 'GPU': 0},
            allow_soft_placement=True,
            log_device_placement=False
        )
        self.save_path = 'chatbot_cut/s2ss_chatbot_anti.ckpt'
        tf.reset_default_graph()
        self.model_pred = SequenceToSequence(
            input_vocab_size=len(self.ws),
            target_vocab_size=len(self.ws),
            batch_size=1,
            mode='decode',
            beam_width=64,
            bidirectional=self.bidirectional,
            cell_type=self.cell_type,
            depth=self.depth,
            attention_type=self.attention_type,
            use_residual=self.use_residual,
            use_dropout=self.use_dropout,
            parallel_iterations=1,
            time_major=self.time_major,
            hidden_units=self.hidden_units,
            share_embedding=True,
            pretrained_embedding=True
        )
        self.init = tf.global_variables_initializer()
        #sess.run(self.init)
        print("!!!!")
    def chat(self,user_text):
        with tf.Session(config=self.config) as sess:
            self.model_pred.load(sess, self.save_path)
            x_test = [jieba.lcut(user_text.lower())]
            bar = batch_flow([x_test], self.ws, 1)
            x, xl = next(bar)
            x = np.flip(x, axis=1)
            pred = self.model_pred.predict(
                sess,
                np.array(x),
                np.array(xl)
            )
            return ''.join(self.ws.inverse_transform(pred))

