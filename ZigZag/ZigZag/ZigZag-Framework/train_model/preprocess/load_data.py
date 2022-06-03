'''
Author: your name
Date: 2022-02-09 17:40:38
LastEditTime: 2022-04-06 19:37:55
LastEditors: Please set LastEditors
Description: 读取数据
'''
import os
import pickle

import numpy as np
from numpy.random import shuffle
from preprocess.process_data import *
from tensorflow.keras.models import load_model

from tools.utils import get_all_files

RANDOMSEED = 2018


def return_last_count(file_name, model_path, model_name_list):
    # TODO:精确到具体的步骤
    cycle_num = 0
    if not os.path.exists(file_name):
        with open(file_name, 'a+') as fwrite:
            fwrite.write(f"model_name,acc,precision,recall,F1,tn,tp,fp,fn,fpr,fnr\n")
        model_name = os.path.join(model_path, model_name_list[0])
        return load_model(model_name), cycle_num
    cnt = len(open(file_name, encoding="utf-8").readlines())
    if cnt <= 7:
        model_name = os.path.join(model_path, model_name_list[0])
        return load_model(model_name), cycle_num
    data = np.genfromtxt(file_name, dtype=str,
                         delimiter=",", skip_header=cnt - 1)
    state_list = [item for item in data[0].split('model-')]
    if state_list[1] == '3.3.h5':
        cycle_num = int(state_list[0])
    else:
        cycle_num = int(state_list[0]) - 1
    if cycle_num == 0:
        model_name = os.path.join(model_path, model_name_list[0])
        return load_model(model_name), cycle_num
    model_name = os.path.join(model_path, str(cycle_num) + model_name_list[3])
    return load_model(model_name), cycle_num


def load_data_once(dataset_path):
    """
        一次性读完路径下所有数据放入内存
        Read all data under the path at one time and put it into memory
    """
    all_file_full_path_list = []
    all_file_name_list = []
    all_file_full_path_list, *_ = get_all_files(dataset_path, all_file_full_path_list, all_file_name_list)
    dataset, labels = load_file_list(all_file_full_path_list)
    return dataset, labels


def load_file(file_path):
    """
        read data
    """
    with open(file_path, "rb") as f:
        dataset, labels, *_ = pickle.load(f)  # *_代表不用的变量返回值，可以为*drop，后接变量名无所谓。
    np.random.seed(RANDOMSEED)
    np.random.shuffle(dataset)  # x  # 将数据集随机化 shuffle
    np.random.seed(RANDOMSEED)
    np.random.shuffle(labels)  # y
    return dataset, labels


def load_file_list(file_path_list):
    """
        read data
    """
    dataset = None
    labels = None
    for file_path in file_path_list:
        with open(file_path, "rb") as f:
            x, y, *_ = pickle.load(f)  # *_代表不用的变量返回值，可以为*drop，后接变量名无所谓。
        dataset, labels = concat_x_and_y(dataset, labels, x, y, file_path)
    np.random.seed(RANDOMSEED)
    np.random.shuffle(dataset)  # x  # 将数据集随机化 shuffle
    np.random.seed(RANDOMSEED)
    np.random.shuffle(labels)  # y
    return dataset, labels


def concat_x_and_y(dataset, labels, x, y, file_path):
    """
        拼接data and label
        concat data and label
    """
    if y is None or len(y) == 0:
        return dataset, labels
    if labels is None or len(labels) == 0:
        dataset = x
        labels = y
    elif len(labels) != 0 and labels is not None:
        try:
            dataset = np.concatenate([dataset, x], axis=0)
            labels = np.hstack([labels, y])
        except IOError:
            print(file_path)
            print("this file has error")
    return dataset, labels


def load_one_file(file):
    with open(file, 'rb') as f:
        dataset, labels, focus, funcs_file, filenames_file = pickle.load(f)
    return dataset, (labels, labels)


def load_data_slices(train_dataset_path, is_change):
    """
        读取文件数据
        origin_or_tigress：是否变换过，origin指 origin 始数据，tigress指经过混淆后数据
    """
    filename_list = []
    for origin_or_tigress in os.listdir(train_dataset_path):
        if origin_or_tigress != is_change:
            continue
        path1 = os.path.join(train_dataset_path, origin_or_tigress)
        filename_list = os.listdir(path1)
    train_filename = []
    for filename in filename_list:
        filename = str(os.path.join(path1, filename))
        train_filename.append(filename)
    # train_filename = list(train_filename)

    return np.asarray(train_filename)
    # train_filename = tf.constant(train_filename)

    # return train_filename


def load_test_data(test_dataset_path):
    dataset = []
    labels = []
    testcases = []
    filenames = []
    funcs = []
    for filename in os.listdir(test_dataset_path):
        with open(os.path.join(test_dataset_path, filename), "rb") as f:
            dataset_file, labels_file, funcs_file, filenames_file, testcases_file = pickle.load(
                f)
        dataset += dataset_file
        labels += labels_file
        testcases += testcases_file
        filenames += filenames_file
        funcs += funcs_file
    print(len(dataset), len(labels), len(
        funcs), len(filenames), len(testcases))
    bin_labels = []
    for label in labels:
        bin_labels.append(label)
    dataset = np.asarray(dataset)
    bin_labels = np.asarray(bin_labels)
    testcases = np.asarray(testcases)
    funcs = np.asarray(funcs)
    return dataset, bin_labels, testcases, funcs


# if __name__ == "__main__":
#     batchSize = 64
#     vectorDim = 40
#     maxLen = 500
#     dropout = 0.2
#     trainDatasetPath = "/data1/yjy/dataset/zigzag/test_case/"  # 数据save path
#     validationDatasetPath = "/data1/yjy/dataset/zigzag/pass_hp/validation/"
#     testDataSetPath = "/data1/yjy/dataset/zigzag/pass_hp/test/"
#     serialNumber = 'mcd0428'  # 日期
#     modelKind = 'BGRU'  # select model
#     predThreshold = 0.5  # 分类正确的 Threshold
#     modelPath = "/data1/yjy/dataset/zigzag/model"  # model save path，需要save用户 path-/
#     resultPath = '/data1/yjy/dataset/zigzag/result'  # result save path
#     all_file_full_path_list = []
#     all_file_name_list = []
#     all_file_full_path_list, all_file_name_list = get_all_files(trainDatasetPath, all_file_full_path_list,
#                                                                 all_file_name_list)
#     for file_name in all_file_full_path_list:
#         with open(file_name, 'rb') as f:
#             dataset = pickle.load(f)
#         print(dataset)
