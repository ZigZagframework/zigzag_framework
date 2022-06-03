import random

import numpy as np
import os

from preprocess.get_test_case import split_list

all_file_full_path_list = []
all_file_name_list = []

if __name__ == '__main__':
    sub_lists = split_list(range(1400), group_num=20, retain_left=False)
    for i in range(1000):
        num = 0
        for idx in range(20):
            file_name = 'set' + str(idx)
            # print(sub_lists[file_name])
            # print(sub_lists[file_name])
            list1 = sub_lists[file_name]
            # print("list1---", len(list1))
            list1_set = set(list1)
            # print("list1_set---", len(list1_set))
            if len(list1) != len(list1_set):
                print('有重复数据')
                num = num + 1
