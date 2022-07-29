# -*- coding: utf-8 -*-
#
# datetime:2022/3/14 15:55

"""
description：预处理数据阶段的数据操作，批量删除数据、复制数据、移动数据、处理数据格式
"""

import os
import re
import random
import pickle
import shutil

from src.tools.utils import get_all_files


def mv_data(from_path, to_path):
    order_mv = 'mv' + '  ' + from_path + '  ' + to_path
    os.system(order_mv)


def mv_train_test():
    order_s = 'mv'
    corpus_path = '/data1/yjy/dataset/SARD/corpus/'
    file_list = ['array_slices', 'api_slices', 'pointer_slices', 'expr_slices']
    for corpus_files in file_list:
        p1 = os.path.join(corpus_path, corpus_files)
        # dir_p1=
        for train_or_test in os.listdir(p1):
            if train_or_test == 'Train':
                p22 = os.path.join(corpus_path, 'train', corpus_files)
            else:
                p22 = os.path.join(corpus_path, 'test', corpus_files)

            p2 = os.path.join(p1, train_or_test)
            for origin_or_tigress in os.listdir(p2):
                if origin_or_tigress == 'Origin':
                    to_path = os.path.join(p22, 'origin')
                else:
                    to_path = os.path.join(p22, origin_or_tigress)

                from_file = os.path.join(p2, origin_or_tigress, '*')

                # re_file_name = origin_or_tigress + '-' + file_name
                # re_file_name = os.path.join(p3, re_file_name)

                # order_rename = 'mv' + '  ' + from_file + '  ' + re_file_name
                os.makedirs(to_path, exist_ok=True)
                order_mv = 'mv' + '  ' + from_file + '  ' + to_path
                print(order_mv)
                print(os.system(order_mv))
                # print(os.system(order_mv))


def move_fuc2testcase():
    # CWE78_OS_Command_Injection__wchar_t_console_system_68b.c
    cp_path = '/data1/yjy/dataset/SARD/corpus/'
    direct_path = '/data1/yjy/dataset/zigzag220712/SARD'
    for train_or_test in os.listdir(cp_path):
        p1 = os.path.join(cp_path, train_or_test)
        direct_path1 = os.path.join(direct_path, train_or_test)
        for bug_kind in os.listdir(p1):
            p2 = os.path.join(p1, bug_kind)
            direct_path2 = os.path.join(direct_path1, bug_kind)
            for tigress_kind in os.listdir(p2):
                p3 = os.path.join(p2, tigress_kind)
                direct_path3 = os.path.join(direct_path2, tigress_kind)
                for cve_kind in os.listdir(p3):
                    print(cve_kind)
                    tail_name = cve_kind.split('_')[-1].split('.')[0]
                    print(tail_name)
                    cve_file_name = cve_kind.strip(cve_kind.split('_')[-1])
                    file_tail = re.sub("\D", "", tail_name)
                    cve_file_name = cve_file_name + file_tail
                    print(cve_file_name)
                    p4 = os.path.join(p3, cve_kind)
                    cve_file_path = os.path.join(direct_path3, cve_file_name)
                    print(cve_file_path)
                    os.makedirs(cve_file_path, exist_ok=True)
                    cp_command = 'cp -r -f ' + p4 + '/*   ' + cve_file_path + '/'
                    print(cp_command)
                    os.system(cp_command)


def subset(alist, idxs):
    sub_list = []
    for _idx in idxs:
        sub_list.append(alist[_idx])

    return sub_list


def split_list(alist, group_num=4, shuffle=True, retain_left=False):
    index = list(range(len(alist)))
    if shuffle:
        random.shuffle(index)
    elem_num = len(alist) // group_num
    _sub_lists = {}
    for _idx in range(group_num):
        start, end = _idx * elem_num, (_idx + 1) * elem_num
        _sub_lists['set' + str(_idx)] = subset(alist, index[start:end])
    if retain_left and group_num * elem_num != len(index):  #
        _sub_lists['set' + str(_idx + 1)] = subset(alist, index[end:])
    return _sub_lists


def get_test_case():
    """
        获取统计学实验的测试样本
    """
    trainDatasetPath = "/data1/yjy/dataset/zigzag/input-step-15/test/"
    write_path = '/data1/yjy/dataset/zigzag/test_case'
    all_file_full_path_list = []
    all_file_name_list = []
    all_file_full_path_list, all_file_name_list = get_all_files(trainDatasetPath, all_file_full_path_list,
                                                                all_file_name_list)
    test_case = []
    for path1 in all_file_full_path_list:
        with open(path1, 'rb') as f:
            dataset, labels, focus, funcs_file, filenames_file = pickle.load(f)
        for file_name in filenames_file:
            test_case.append(file_name.split(' ')[1])
    print('test_case--', len(test_case))
    test_case_set = set(test_case)
    print('test_case_set--', len(test_case_set))
    test_case_list = list(test_case_set)
    print("test_case_list", len(test_case_list))
    os.makedirs(write_path, exist_ok=True)
    sub_lists = split_list(test_case_list, group_num=20, retain_left=False)
    for idx in range(20):
        file_name = 'set' + str(idx)
        # print(sub_lists[file_name])
        pkl_name = os.path.join(write_path, file_name + '.pkl')


def del_ep(contents):
    # isdir用于判断路径是否为目录，是目录的话需要进一步的循环读取
    if os.path.isdir(contents):
        for i in os.listdir(contents):
            # 含多层级文件目录，所以需要不停的更新
            del_ep(os.path.join(contents, i))
    # 如果rmdir得到的路径是非空文件夹，会抛出异常
    try:
        if not os.listdir(contents):
            # 删除
            os.rmdir(contents)
            print('已删除空文件夹: ', contents)
    except Exception as e:
        print(e)


def del_after_2017():
    # 全路径
    all_file_full_path_list = []
    all_file_name_list = []
    dataset_path_list, *_ = get_all_files(dataSetPath,
                                          all_file_full_path_list,
                                          all_file_name_list)
    for pkl_file in dataset_path_list:
        if 'CVE-2020' in pkl_file:
            print(pkl_file)


def deal_nvd():
    path_list = []
    del_str = 'rm -rf '
    for path1 in os.listdir(dataSetPath):  # api_slices/
        path_list1 = os.path.join(dataSetPath, path1)
        # print(path_list1)
        for path2 in os.listdir(path_list1):  # api_slices/tigressType1/
            path_list2 = os.path.join(path_list1, path2)
            # NVD/api_slices/tigressType1/ffmpeg/
            for path3 in os.listdir(path_list2):
                print(path3)
                path_list3 = os.path.join(path_list2, path3)
                if path3 == 'linux_kernel':
                    print(del_str + path_list3)
                    os.system(del_str + path_list3)
                    continue
                # NVD/api_slices/tigressType1/ffmpeg/ffmpeg-0.10.14_vul/
                for path4 in os.listdir(path_list3):
                    path_list4 = os.path.join(path_list3, path4)
                    # /data1/yjy/dataset/zigzag220712/NVD/api_slices/tigressType1/ffmpeg/ffmpeg-0.10.14_vul/CVE-2012-2797/
                    for path5 in os.listdir(path_list4):
                        path_list5 = os.path.join(path_list4, path5)
                        # 删除大于2017的所有文件.split(',')
                        years = path5.split('-')[1]
                        if int(years) > 2016:
                            print(del_str + path_list5)
                            os.system(del_str + path_list5)
                            continue
                        # /data1/yjy/dataset/zigzag220712/NVD/api_slices/tigressType1/ffmpeg/ffmpeg-0.10.14_vul/CVE-2012-2797/CVE-2012-2797_NVD-CWE-noinfo_libavcodec_mpegaudiodec.c_1.1_OLD.c#decode_frame_mp3on4#.c/
                        for path6 in os.listdir(path_list5):
                            path_list6 = os.path.join(path_list5, path6)
                            # print(len(os.listdir(path_list6)))
                            if len(os.listdir(path_list6)) == 0:
                                print(len(path_list6))
                                # os.system(del_str + path_list6)


def del_linux_kernel():
    # 全路径
    all_file_full_path_list = []
    all_file_name_list = []
    dataset_path_list, *_ = get_all_files(dataSetPath,
                                          all_file_full_path_list,
                                          all_file_name_list)
    for pkl_file in dataset_path_list:
        print(pkl_file)
        if 'linux_kernel' in pkl_file:
            print(pkl_file)


def sum_sard_pkl_num():
    path1 = '/data1/yjy/dataset/zigzag220712/SARD/train/'
    all_file_full_path_list = []
    all_file_name_list = []
    dataset_path_list, file_name_list = get_all_files(path1,
                                                      all_file_full_path_list,
                                                      all_file_name_list)
    print('test_pkl_num--', len(file_name_list))


def sum_sard_testcase():
    path1 = '/data1/yjy/dataset/zigzag220712/SARD/train/'
    all_file_full_path_list = []
    all_file_name_list = []
    dataset_path_list, file_name_list = get_all_files(path1,
                                                      all_file_full_path_list,
                                                      all_file_name_list)
    # /data1/yjy/dataset/zigzag220712/SARD/train/pointer_slices/origin/
    # 读
    print('dataset_path_list长度--', len(dataset_path_list))
    path_set = set()
    for i, path_str in enumerate(dataset_path_list):
        pkl_name = path_str.split('/')[9]
        path_set.add(pkl_name)
    print(len(path_set))
    testcase_path_list = list(path_set)
    return testcase_path_list


def del_testcase():
    del_num = 4829
    path1 = '/data1/yjy/dataset/zigzag220712/SARD/train/'
    testcase_path_list = sum_sard_testcase()
    del_path = random.sample(testcase_path_list, del_num)
    print('dataset_path_list长度--', len(testcase_path_list))
    print('dir_path-长度--', len(del_path))
    for slice_path in os.listdir(path1):
        slice_paths = os.path.join(path1, slice_path)
        for tog in os.listdir(slice_paths):
            p2 = os.path.join(slice_paths, tog)  # tigress
            for testcase_path in del_path:
                dir_path = os.path.join(p2, testcase_path)
                del_file_command = 'rm -rf ' + dir_path
                if os.path.isdir(dir_path):
                    print(del_file_command)
                    shutil.rmtree(dir_path)


if __name__ == '__main__':
    dataSetPath = '/data1/yjy/dataset/zigzag220712/'
    sum_sard_testcase()
