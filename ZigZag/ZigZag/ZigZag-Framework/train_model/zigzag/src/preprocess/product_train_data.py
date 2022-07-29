# -*- coding: utf-8 -*-
#
# datetime:2022/2/28 15:50

"""
description：This python file is used to split database into 80% train set and 20% test set,
                tranfer the original code into vector, creating input file of deap learning model.


 1.   generate  w2v； 2. Processing unified data shape; 3. Unified file name format
"""
import random
import pickle
import time
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from src.tools import utils
from src.preprocess.process_data import produce_val_data
from src.tools.utils import get_all_files


def write_vector():
    """
        2.change word to vector
    """
    for train_or_test in os.listdir(all_corpus):  # /corpus/expr_slices
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        p1 = os.path.join(all_corpus, train_or_test)
        origin_path_list = []
        tigress_path_list = []
        origin_vector_path = os.path.join(all_vector, train_or_test, 'origin')
        tigress_vector_path = os.path.join(
            all_vector, train_or_test, 'tigress')
        os.makedirs(origin_vector_path, exist_ok=True)
        os.makedirs(tigress_vector_path, exist_ok=True)
        for files_kinds in os.listdir(p1):
            p2 = os.path.join(p1, files_kinds)
            p3 = os.path.join(p2, 'origin')
            list1 = sorted(os.listdir(p3))
            # list2 = list1[::step_num]
            # list2 = list1
            for file_name in list1:
                origin_path_list.append(os.path.join(p3, file_name))
                print(os.path.join(p3, file_name))
            # tigress
            for i in range(8):
                tigress_file_name = 'tigressType' + str(i + 1)
                p3 = os.path.join(p2, tigress_file_name)
                for file_path in os.listdir(p3):
                    if file_path in list1:
                        p4 = os.path.join(p3, file_path)
                        tigress_path_list.append(p4)
                        print(p4)
        print(train_or_test, "origin file num", str(len(origin_path_list)))
        print(train_or_test, "tigress file num", str(len(tigress_path_list)))
        deal_input_sard(origin_path_list, origin_vector_path)
        deal_input_sard(tigress_path_list, tigress_vector_path)
        # Get the data in List2 in Tigress 1-8, process the tigress data and output it to vector_ path
        # vector_path = os.path.join(all_vector, train_or_test, 'tigress')


def deal_input_sard(list_select, vector_path):
    """
        list_select：
        file_len:
        vector_path:
    """
    data_batch = []
    i = 0
    for pkl_path in list_select:
        for pkl_file in os.listdir(pkl_path):
            p5 = os.path.join(pkl_path, pkl_file)
            if i < file_len:
                with open(p5, 'rb') as f:
                    data = pickle.load(f)  # A piece of data
                # 2.change word to vector
                data[0] = utils.generate_corpus(w2v_model, data[0])
                i += 1
                data_batch.append(data)
            else:
                pkl_name = utils.give_file_name(str(file_len))
                pkl_name = os.path.join(vector_path, pkl_name)
                print(pkl_name)
                utils.write2file(pkl_name, data_batch, max_len, vector_dim)
                data_batch = []
                i = 0
    # less than file_len end
    if i > 0:
        # More than half are reserved and less than half are discarded
        if len(data_batch) > file_len / 2:
            print(len(data_batch))
            # -Fill duplicate data
            data_batch.extend(random.sample(
                data_batch, file_len - len(data_batch)))
            pkl_name = utils.give_file_name(str(file_len))
            pkl_name = os.path.join(vector_path, pkl_name)
            print(pkl_name)
            utils.write2file(pkl_name, data_batch, max_len, vector_dim)


def deal_input(list_select, tot, tog):
    """
        list_select：
        file_len:
        vector_path:
    """
    data_batch = []
    i = 0
    vector_path = os.path.join(all_vector, tot, tog)
    os.makedirs(vector_path, exist_ok=True)
    for pkl_file in list_select:
        if i < file_len:
            with open(pkl_file, 'rb') as f:
                data = pickle.load(f)  # A piece of data
            # 2.change word to vector
            data[0] = utils.generate_corpus(w2v_model, data[0])
            i += 1
            data_batch.append(data)
        else:
            pkl_name = utils.give_file_name(str(file_len))
            pkl_name = os.path.join(vector_path, pkl_name)
            print(pkl_name)

            utils.write2file(pkl_name, data_batch, max_len, vector_dim)
            data_batch = []
            i = 0
    # less than file_len end
    if i > 0:
        # More than half are reserved and less than half are discarded
        if len(data_batch) > file_len / 2:
            print(len(data_batch))
            # Fill duplicate data
            data_batch.extend(random.sample(
                data_batch, file_len - len(data_batch)))
            pkl_name = utils.give_file_name(str(file_len))
            pkl_name = os.path.join(vector_path, pkl_name)
            print(pkl_name)

            utils.write2file(pkl_name, data_batch, max_len, vector_dim)


def write_vector_nvd_sard():
    # 获取全路径列表 all_corpus
    all_file_full_path_list = []
    all_file_name_list = []
    dataset_path_list, *_ = get_all_files(all_corpus, all_file_full_path_list,
                                          all_file_name_list)
    # 太蠢了
    print(len(dataset_path_list))
    nvd_train_origin = []
    nvd_train_tigress = []
    sard_train_origin = []
    sard_train_tigress = []
    sard_test_origin = []
    sard_test_tigress = []
    for pkl_file in dataset_path_list:
        if pkl_file.split('/')[5] == 'NVD':
            if pkl_file.split('/')[7] == 'Origin':

                nvd_train_origin.append(pkl_file)
            else:
                nvd_train_tigress.append(pkl_file)
        else:
            if pkl_file.split('/')[6] == 'train':
                if pkl_file.split('/')[8] == 'origin':

                    sard_train_origin.append(pkl_file)
                else:
                    sard_train_tigress.append(pkl_file)
            else:
                if pkl_file.split('/')[8] == 'origin':
                    sard_test_origin.append(pkl_file)
                else:
                    sard_test_tigress.append(pkl_file)
    # print(len(nvd_train_origin)+len(nvd_train_tigress)+len(sard_train_origin)+len(sard_train_tigress)+len(sard_test_origin)+len(sard_test_tigress))
    deal_input(nvd_train_origin, 'train', 'origin')
    deal_input(nvd_train_tigress, 'train', 'tigress')
    deal_input(sard_train_origin, 'train', 'origin')
    deal_input(sard_train_tigress, 'train', 'tigress')
    deal_input(sard_test_origin, 'test', 'origin')
    deal_input(sard_test_tigress, 'test', 'tigress')
    produce_val_data(all_vector, file_len)


def main():
    print('begin data loading  ......')
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    write_vector()
    print("w2v over...")
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    produce_val_data(all_vector, file_len)


if __name__ == "__main__":
    # generate  300 pieces of data to test the feasibility of the initial code
    # generate  About 2000 data tests show whether the train loss can be reduced to close to 0 after several epochs.
    # Verify the model performance on the small s example set of 10000 or 100000 levels, and analyze the sensitivity of super parameters.
    # cd /home/***/code/keras/zigzag-master/preprocess/
    # sudo nohup python -u product_train_data.py > product_train_data.txt 2>&1
    vector_dim = 40
    max_len = 500
    # step_num = 5
    file_len = 320  # Single file  len
    all_corpus = "/data1/yjy/dataset/zigzag220712"
    all_vector = "/data1/yjy/dataset/zigzag_vector_220720"
    w2v_model_path = "/data1/yjy/model/w2v_model/"
    os.makedirs(all_vector, exist_ok=True)
    w2v_model_name = 'w2v-all-20220712.model'
    w2v_model = os.path.join(w2v_model_path, w2v_model_name)
    write_vector_nvd_sard()
    #  main()
    print("---------------------------end------------------------------------")
