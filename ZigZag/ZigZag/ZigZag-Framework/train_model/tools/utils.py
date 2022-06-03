# -*- coding: utf-8 -*-
#
# datetime:2022/4/27 9:22

"""
description：工具类
能重复利用的类
解耦
"""
import pickle
import sys
import string
import time
import os
import random
import numpy as np
from gensim.models.word2vec import Word2Vec


def give_file_name(file_len):
    ran_str = ''.join(random.sample(string.ascii_letters + string.digits, 4))
    file_name = ran_str + '-' + str(file_len) + '.pkl'
    return file_name


def write2file(pkl_name, data_batch, max_len, vector_dim):
    data, label, focus, funcs, filenames = del_word_len(
        data_batch, max_len, vector_dim)
    data2pkl([data, label, focus, funcs, filenames], pkl_name)


def data2pkl(parm_list, pkl_name):
    with open(pkl_name, 'wb') as f_vector:
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        pickle.dump(parm_list, f_vector, protocol=4)
        print(pkl_name, "write  input success...")


def process_sequences_shape(sequences, max_len, vector_dim):
    """
        数据格式处理
        将数据统一为 max_len*vector_dim
    """
    samples_len = len(sequences)
    nb_samples = np.zeros((samples_len, max_len, vector_dim))
    i = 0
    for sequence in sequences:
        m = 0
        for vectors in sequence:
            n = 0
            if m <= max_len:
                for values in vectors:
                    nb_samples[i][m][n] += values
                    n += 1
                m += 1
        i += 1
    return nb_samples


def process_input_shape(sequence, max_len, vector_dim):
    """
        数据格式处理
        将数据统一为 max_len*vector_dim
    """
    nb_samples = np.zeros((max_len, vector_dim))
    m = 0
    for vectors in sequence:
        n = 0
        if m <= max_len:
            for values in vectors:
                nb_samples[m][n] += values
                n += 1
            m += 1
    return nb_samples


def generate_corpus(w2v_model_path, samples):
    """
        This function is used to create input of deep learning model
        Arguments
        w2v_model_path: the path saves word2vec model
        samples: the list of sample
        create vector
    """
    model = Word2Vec.load(w2v_model_path)
    dl_corpus = [[model.wv[word] for word in sample] for sample in samples]
    return dl_corpus


def get_all_files(path, all_file_full_path_list, all_file_name_list):
    """
    all_file_full_path_list:For multi-level directories, all files have full paths;
    all_file_name_list:All file names under multi-level directories
    获取指定路径下多层目录内的所有文件全路径及文件名称
    Obtain the full path and file name of all files in the multi-level directory under the specified path
    :param path: 需获取文件的指定路径 To get the specified path of the file
    :return: 结果1 类型：list<str> ：多层目录下的，全部文件全路径；结果2 类型：list<str> ：多层目录下的，全部文件名称

    """
    all_file_list = os.listdir(path)
    # 遍历该文件夹下的所有目录或文件
    for file in all_file_list:
        file_path = os.path.join(path, file)
        # 如果是文件夹，递归调用当前函数
        if os.path.isdir(file_path):
            get_all_files(file_path, all_file_full_path_list, all_file_name_list)
        # 如果不是文件夹，保存文件路径及文件名
        elif os.path.isfile(file_path):
            all_file_full_path_list.append(file_path)
            all_file_name_list.append(file)
    return all_file_full_path_list, all_file_name_list


def del_word_len(data_list, max_len, vector_dim):
    """
        3.Unified data shape maxLen * vectorDim
    """
    X = []
    Y = []
    focus_points = []
    funcs = []
    filenames = []
    for data in data_list:
        x, y, focus_point, func, file_name = data[0][0], data[1][0], data[2][0], data[3][0], data[4][0]
        if len(x) < max_len:
            x = process_input_shape(x, max_len=max_len, vector_dim=vector_dim)
            X.append(x)
            focus_points.append(focus_point)
        elif len(x) == max_len:
            X.append(x)
            focus_points.append(focus_point)
        else:
            startpoint = int(focus_point - round(max_len / 2.0))
            endpoint = int(startpoint + max_len)
            if startpoint < 0:
                startpoint = 0
                endpoint = max_len
            if endpoint >= len(x):
                startpoint = -max_len
                endpoint = None
            focus_point = focus_point - startpoint
            focus_points.append(focus_point)
            X.append(x[startpoint:endpoint])
        Y.append(y)
        funcs.append(func)
        filenames.append(file_name)
    # 4.change list to ndarray
    X = np.asarray(X)
    Y = np.asarray(Y)
    return X, Y, focus_points, funcs, filenames
