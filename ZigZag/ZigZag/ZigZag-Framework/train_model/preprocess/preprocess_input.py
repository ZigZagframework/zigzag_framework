# -*- coding: utf-8 -*-
#
# datetime:2022/3/14 15:55

"""
description：
"""

import pickle
import numpy as np

from tools import utils

np.random.seed(1337)  # for reproducibility


def multi_labels_to_two(label):
    """
       All tags are mapped to 0 or 1, binary in the article
    """
    if label in [0, 1]:
        return label
    if 1 in label:
        return 1
    else:
        return 0


def multi_labels_to_onehot(label):
    """
             All tags are mapped to [0,1] or [1,0], binary in the article
        """
    if label == 1:
        return [0, 1]
    else:
        return [1, 0]


def mislabels(list_labels, threshold):
    # Label confusion
    label_sum = len(list_labels)
    mispart = int(label_sum * threshold)  # Confusion ratio

    i = 0
    while i < label_sum:
        if i > mispart:
            i += 1
            continue
        if list_labels[i] == 0:
            list_labels[i] = 1
            i += 1
        elif list_labels[i] == 1:
            list_labels[i] = 0
            i += 1

        else:
            print("error")
            exit()

    return list_labels


def x_fold_cross_validation_binary(dataset, labels, batch_size, folder=5):
    # X-fold cross validation method for binary classification
    len_dataset = len(dataset)
    if len(dataset) % folder == 0:
        snippet_width = len_dataset / folder
    else:
        snippet_width = len_dataset / folder + 1

    list_snippet_dataset = []
    list_snippet_labels = []
    for i in range(0, folder):
        if i != folder - 1:
            list_snippet_dataset.append(
                dataset[i * snippet_width:(i + 1) * snippet_width])
            list_snippet_labels.append(
                labels[i * snippet_width:(i + 1) * snippet_width])
        else:
            list_snippet_dataset.append(dataset[i * snippet_width:])
            list_snippet_labels.append(labels[i * snippet_width:])

    # list_dataset_all = []
    list_dataset_all = [[[], [], [], []], [[], [], [], []], [
        [], [], [], []], [[], [], [], []], [[], [], [], []]]
    # Construct the data set of cross validation method
    for i in range(0, len(list_snippet_dataset)):
        list_train_dataset = []
        list_train_labels = []
        train_dataset = []
        train_labels = []
        test_dataset = []
        test_labels = []

        for j in range(0, len(list_snippet_dataset)):
            if j == i:
                continue
            else:
                list_train_dataset += list_snippet_dataset[j]

                # For the connection between arrays, DL input only accepts numpy type data structures, and does not support lists
                list_train_labels += list_snippet_labels[j]

        train_data_num = len(list_train_dataset)
        train_remain = train_data_num % batch_size

        if train_remain != 0:
            train_dataset = list_train_dataset[:train_data_num - train_remain]
            train_labels = list_train_labels[:train_data_num - train_remain]
        else:
            train_dataset = list_train_dataset
            train_labels = list_train_labels

        test_data_num = len(list_snippet_dataset[i])
        test_remain = test_data_num % batch_size

        if test_remain != 0:
            test_dataset = list_snippet_dataset[i][:test_data_num - test_remain]
            test_labels = list_snippet_labels[i][:test_data_num - test_remain]
        else:
            test_dataset = list_snippet_dataset[i]
            test_labels = list_snippet_labels[i]
        # print("test", len(test_dataset), test_labels.shape)

        # test_dataset = list_snippet_dataset[i]
        # test_labels = list_snippet_labels[i]
        list_dataset_all[i][0] = train_dataset
        list_dataset_all[i][1] = train_labels
        list_dataset_all[i][2] = test_dataset
        list_dataset_all[i][3] = test_labels
        # list_dataset_all.append((train_dataset, train_labels, test_dataset, test_labels))

    return list_dataset_all


def load_data_binary(dataset_path, batch_size, max_len=None, vector_dim=40, seed=113):
    # Load data
    f1 = open(dataset_path, 'rb')
    X, labels, focuspointers = pickle.load(f1)
    f1.close()

    cut_count = 0
    fill_0_count = 0
    no_change_count = 0
    fill_0 = [0] * vector_dim
    if max_len:
        new_X = []
        new_labels = []
        for x, y, focus in zip(X, labels, focuspointers):
            if len(x) > 1000:  # If the data is too long, it will be discarded directly
                pass
            if len(x) < max_len:  # Fill 0
                x = x + [fill_0] * (max_len - len(x))
                new_X.append(x)
                # y = multi_labels_to_two(y)
                new_labels.append(y)
                fill_0_count += 1

            elif len(x) == max_len:
                new_X.append(x)
                # y = multi_labels_to_two(y)
                new_labels.append(y)
                no_change_count += 1

            else:  # data len, Between maxlen and 1000, the cutting is carried out by cutting the head and tail
                startpoint = int(focus - round(max_len / 2.0))
                endpoint = int(startpoint + max_len)
                if startpoint < 0:
                    startpoint = 0
                    endpoint = max_len
                if endpoint >= len(x):
                    startpoint = -max_len
                    endpoint = None
                new_X.append(x[startpoint:endpoint])
                # y = multi_labels_to_two(y)
                new_labels.append(y)
                cut_count += 1

        X = new_X
        labels = new_labels

    num = len(X)
    remain = num % batch_size

    if remain != 0:
        dataset = X[:num - remain]
        _labels = labels[:num - remain]
    else:
        dataset = X
        _labels = labels

    return dataset, _labels


def generator_of_data(data, labels, batch_size, max_len, vector_dim):
    """
    generate data
    返回通过 yield batched_input, batched_labels
      lenyield
    """
    iter_num = int(len(data) / batch_size)
    i = 0
    while iter_num:
        # A batch of data represented by digital vectors
        batch_data = data[i:i + batch_size]
        batched_input = utils.process_sequences_shape(
            batch_data, max_len=max_len, vector_dim=vector_dim)
        batched_labels = labels[i:i + batch_size]
        yield batched_input, batched_labels
        i = i + batch_size
        iter_num -= 1
        if iter_num == 0:
            iter_num = int(len(data) / batch_size)
            i = 0
