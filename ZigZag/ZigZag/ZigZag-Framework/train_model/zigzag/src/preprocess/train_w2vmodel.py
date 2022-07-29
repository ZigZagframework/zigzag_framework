# -*- coding: utf-8 -*-
"""
Description: This python file is used to train word2vec model , and save the word2vec model under the path 'w2v_model'.
Date: 2022-02-28 10:59:32
LastEditTime: 2022-03-06 12:24:40
"""
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from gensim.models.word2vec import Word2Vec
import pickle
from src.tools.utils import get_all_files
import gc
import time


class DirOfCorpus(object):
    """
        This class is used to make a generator to produce sentence for word2vec training
        dirname: The src of corpus files
    """

    def __init__(self, corpus_path):
        self.dirname = os.listdir(corpus_path)
        self.corpus_path = corpus_path

    def __iter__(self):
        path = self.corpus_path
        all_file_full_path_list = []
        all_file_name_list = []
        all_file_full_path_list, all_file_name_list = get_all_files(path, all_file_full_path_list, all_file_name_list)
        for file_full_path_list in all_file_full_path_list:
            samples = pickle.load(open(file_full_path_list, 'rb'))[0]
            for sample in samples:
                yield sample
            del samples
            gc.collect()

    """ # old read pkl method
       def __iter__(self):
           for class_name in self.dirname:
               print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
               p1 = os.path.join(self.corpus_path, class_name)
               for train_or_test in os.listdir(p1):
                   print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
                   p2 = os.path.join(p1, train_or_test)
                   for files_path in os.listdir(p2):
                       print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
                       p3 = os.path.join(p2, files_path)
                       for file_path in os.listdir(p3):
                           p4 = os.path.join(p3, file_path)
                           for file_name in os.listdir(p4):
                               samples = pickle.load(
                                   open(os.path.join(p4, file_name), 'rb'))[0]
                               for sample in samples:
                                   yield sample
                               del samples
                               gc.collect()
           """


def generate_w2v_model(dec_token_flaw_path, w2v_model):
    """
        This function is used to learning vectors from corpus, and save the model
        # Arguments
        dec_token_flaw_path: String type, the src of corpus file
        w2v_model_path: String type, the src of model file
    """
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    print("training...")
    model = Word2Vec(sentences=DirOfCorpus(dec_token_flaw_path), vector_size=40, alpha=0.01, window=15,
                     min_count=0,
                     max_vocab_size=None, sample=0.001, seed=1, workers=16, min_alpha=0.0001, sg=1, hs=0,
                     negative=10,
                     epochs=5)
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    # binary=False
    model.save(w2v_model)


def evaluate_w2v_model(w2v_model):
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    print("\n evaluating...")
    model = Word2Vec.load(w2v_model)
    for sign in ['(', '+', '-', '*', 'main', 'char', 'for']:  # for-while;break-con
        print(sign, ":")
        print(model.wv.most_similar(sign, topn=10))


def main():
    corpus_path = '/data1/yjy/dataset/zigzag220712/'
    w2v_model_path = "/data1/yjy/model/w2v_model/"
    date_s = '20220712'
    os.makedirs(w2v_model_path, exist_ok=True)
    w2v_model = 'w2v-all-' + date_s + '.model'
    w2v_model = os.path.join(w2v_model_path, w2v_model)
    generate_w2v_model(corpus_path, w2v_model)
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    evaluate_w2v_model(w2v_model)
    print("train word2vec model success!")
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))


# /home/yjy/code/keras/zigzag-master/preprocess/
# /data1/yjy/dataset/SARD/corpus/expr_slices/
#   export PYTHONHASHSEED=0
#
# nohup python -u train_w2vmodel.py > w2v_modle-all-20220311.txt 2>&1

if __name__ == "__main__":
    main()
