import os.path
import pickle

from tools.utils import get_all_files, data2pkl

import random


def subset(alist, idxs):
    """
        用法：根据下标idxs取出列表alist的子集
        alist: list
        idxs: list
    """
    sub_list = []
    for idx in idxs:
        sub_list.append(alist[idx])

    return sub_list


def split_list(alist, group_num=4, shuffle=True, retain_left=False):
    """
        用法：将alist切分成group个子列表，每个子列表里面有len(alist)//group个元素
        shuffle: 表示是否要随机切分列表，默认为True
        retain_left: 若将列表alist分成group_num个子列表后还要剩余，是否将剩余的元素单独作为一组
    """

    index = list(range(len(alist)))  # 保留下标

    # 是否打乱列表
    if shuffle:
        random.shuffle(index)

    elem_num = len(alist) // group_num  # 每一个子列表所含有的元素数量
    sub_lists = {}

    # 取出每一个子列表所包含的元素，存入字典中
    for idx in range(group_num):
        start, end = idx * elem_num, (idx + 1) * elem_num
        sub_lists['set' + str(idx)] = subset(alist, index[start:end])

    # 是否将最后剩余的元素作为单独的一组
    # 列表元素数量未能整除子列表数，需要将最后那一部分元素单独作为新的列表
    if retain_left and group_num * elem_num != len(index):
        sub_lists['set' + str(idx + 1)] = subset(alist, index[end:])

    return sub_lists


if __name__ == '__main__':
    trainDatasetPath = "./dataset/zigzag/input-step-15/test/"
    write_path = './dataset/zigzag/test_case'
    # 1.获取所有文件列表pkl
    all_file_full_path_list = []
    all_file_name_list = []
    all_file_full_path_list, all_file_name_list = get_all_files(trainDatasetPath, all_file_full_path_list,
                                                                all_file_name_list)
    test_case = []
    for path1 in all_file_full_path_list:
        with open(path1, 'rb') as f:
            dataset, labels, focus, funcs_file, filenames_file = pickle.load(f)
        for file_name in filenames_file:
            # print(file_name)
            test_case.append(file_name.split(' ')[1])
            # print(file_name.split(' ')[1])
    print('test_case--', len(test_case))
    test_case_set = set(test_case)
    # print(test_case_set)
    print('test_case_set--', len(test_case_set))
    test_case_list = list(test_case_set)
    print("test_case_list", len(test_case_list))
    os.makedirs(write_path, exist_ok=True)
    # pkl_name = os.path.join(write_path, 'all_file.pkl')
    sub_lists = split_list(test_case_list, group_num=20, retain_left=False)
    for idx in range(20):
        file_name = 'set' + str(idx)
        # print(sub_lists[file_name])
        pkl_name = os.path.join(write_path, file_name + '.pkl')
        # data2pkl(sub_lists[file_name], pkl_name)
    #
    # test_case_name = './dataset/zigzag/input-step-15/test_case_set.csv'
    # with open(test_case_name, 'a+') as fwrite:
    #     fwrite.write(test_case_set)
