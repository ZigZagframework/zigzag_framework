# -*- coding: utf-8 -*-
#
# datetime:2022/3/12 16:49

"""
description：整理 path，分为train 、test
"""
import os


def mv_1():
    order_s = 'mv'
    corpus_path = './code/keras/zigzag-master/data/corpus-vector/'
    file_list = ['array_slices', 'api_slices', 'pointer_slices', 'expr_slices']
    for corpus_files in file_list:
        p1 = os.path.join(corpus_path, corpus_files)
        for train_or_test in os.listdir(p1):
            if train_or_test == 'Train':
                p22 = os.path.join(corpus_path, 'train')
            else:
                p22 = os.path.join(corpus_path, 'test')

            p2 = os.path.join(p1, train_or_test)
            for origin_or_tigress in os.listdir(p2):
                if origin_or_tigress == 'Origin':
                    to_path = os.path.join(p22, 'origin')
                else:
                    to_path = os.path.join(p22, 'tigress')
                p3 = os.path.join(p2, origin_or_tigress)
                for file_name in os.listdir(p3):
                    # re_file_name = origin_or_tigress + '-' + file_name
                    # re_file_name = os.path.join(p3, re_file_name)
                    from_file = os.path.join(p3, file_name)

                    # order_rename = 'mv' + '  ' + from_file + '  ' + re_file_name
                    os.makedirs(to_path, exist_ok=True)
                    order_mv = 'mv' + '  ' + from_file + '  ' + to_path
                    print(order_mv)
                    # print(os.system(order_rename))
                    print(os.system(order_mv))


# from_file = "./code/keras/zigzag-master/data/corpus-vector/train/origin/data-1537.pkl"
#
# to_path = './code/keras/zigzag-master/data/corpus-vector/train/origin/origin-data-1537.pkl'
# order_s = 'mv' + '  ' + from_file + '  ' + to_path
# print(order_s)

def mv_train_test():
    order_s = 'mv'
    corpus_path = './dataset/SARD/corpus/'
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


def file_len():
    order_s = 'mv'
    corpus_path = './dataset/SARD/corpus/'
    file_list = ['array_slices', 'api_slices', 'pointer_slices', 'expr_slices']
    for corpus_files in file_list:
        p1 = os.path.join(corpus_path, corpus_files)
        for train_or_test in os.listdir(p1):

            p2 = os.path.join(p1, train_or_test)
            for origin_or_tigress in os.listdir(p2):
                p3 = os.path.join(p2, origin_or_tigress)

                print(len(os.listdir(p3)))


def main():
    file_len()


if __name__ == "__main__":
    main()
