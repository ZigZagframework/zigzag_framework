'''
Author: your name
Date: 2022-02-09 17:40:38
LastEditTime: 2022-04-06 19:37:55
LastEditors: Please set LastEditors
Description:
'''
import os
import pickle

import numpy as np
from numpy.random import shuffle
from tensorflow.keras.models import load_model

from src.tools.utils import get_all_files

RANDOMSEED = 2018


def return_last_count(file_name, model_path, model_name_list):
    cycle_num = 0
    if not os.path.exists(file_name):
        with open(file_name, 'a+') as fwrite:
            fwrite.write(
                f"model_name,acc,precision,recall,F1,tn,tp,fp,fn,fpr,fnr\n")
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
        if state_list[0] == '':
            cycle_num = 0
        else:
            cycle_num = int(state_list[0]) - 1
    if cycle_num == 0:
        model_name = os.path.join(model_path, model_name_list[0])
        return load_model(model_name), cycle_num
    model_name = os.path.join(model_path, str(cycle_num) + model_name_list[3])
    return load_model(model_name), cycle_num


def load_data_once(dataset_path):
    """

        Read all data under the path at one time and put it into memory
    """
    all_file_full_path_list = []
    all_file_name_list = []
    all_file_full_path_list, * \
        _ = get_all_files(
        dataset_path, all_file_full_path_list, all_file_name_list)
    dataset, labels = load_file_list(all_file_full_path_list)
    return dataset, labels


def load_file(file_path):
    """
        read data
    """
    with open(file_path, "rb") as f:
        dataset, labels, *_ = pickle.load(f)  # **drop。
    np.random.seed(RANDOMSEED)
    np.random.shuffle(dataset)  # x  # shuffle
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
            x, y, *_ = pickle.load(f)  # **drop。
        dataset, labels = concat_x_and_y(dataset, labels, x, y, file_path)
    np.random.seed(RANDOMSEED)
    np.random.shuffle(dataset)  # x  # shuffle
    np.random.seed(RANDOMSEED)
    np.random.shuffle(labels)  # y
    return dataset, labels


def concat_x_and_y(dataset, labels, x, y, file_path):
    """
       data and label
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
#     trainDatasetPath = "/data1/yjy/dataset/zigzag/test_case/"  #save path
#     validationDatasetPath = "/data1/yjy/dataset/zigzag/pass_hp/validation/"
#     testDataSetPath = "/data1/yjy/dataset/zigzag/pass_hp/test/"
#     serialNumber = 'mcd0428'  #
#     modelKind = 'BGRU'  # select model
#     predThreshold = 0.5  # Threshold
#     modelPath = "/data1/yjy/dataset/zigzag/model"  # model save pathsav path-/
#     resultPath = '/data1/yjy/dataset/zigzag/result'  # result save path
#     all_file_full_path_list = []
#     all_file_name_list = []
#     all_file_full_path_list, all_file_name_list = get_all_files(trainDatasetPath, all_file_full_path_list,
#                                                                 all_file_name_list)
#     for file_name in all_file_full_path_list:
#         with open(file_name, 'rb') as f:
#             dataset = pickle.load(f)
#         print(dataset)
