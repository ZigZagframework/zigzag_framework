# -*- coding: utf-8 -*-
#
# datetime:2021/12/19 16:46

"""
description：Process data
"""
import random
import time

from src.preprocess.load_data import *
from src.tools import utils


def generator_of_data(data, labels, batch_size, max_len, vector_dim):
    """
    generate data
     yield batched_input, batched_labels
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


def get_file_path_list(dataset_path, secondary_directory, file_len):
    """
       file_le
        Fixed length, below file_len don't use
    """
    file_path_list = []
    al_data_len = 0
    for sec_dir in os.listdir(dataset_path):
        if sec_dir != secondary_directory:
            continue
        path1 = os.path.join(dataset_path, secondary_directory)
        for pkl_file in os.listdir(path1):
            file_path_list.append(os.path.join(
                dataset_path, sec_dir, pkl_file))
        al_data_len = file_len * len(file_path_list)
        print(dataset_path + 'data numbers-------' +
              str(al_data_len) + '\n -----file numbers---' + str(len(file_path_list)))
    return file_path_list, al_data_len


def get_data_len(pkl_file, batch_size):
    data_len = int(pkl_file[5:pkl_file.find('.')])
    data_len = int(data_len / batch_size) * batch_size
    return data_len


def get_hard_index(pred_threshold, y1_p, y2_p, input_label, data_set):
    x_list = []
    y_list = []
    y1_p = y1_p.flatten()
    y2_p = y2_p.flatten()
    a = (y1_p < pred_threshold) & (y2_p < pred_threshold) & (
            input_label < pred_threshold)  # all smaller then pred_threshold
    b = (y1_p > pred_threshold) & (y2_p > pred_threshold) & (
            input_label > pred_threshold)  # all bigger then pred_threshold
    c = a | b  # all bigger or all smaller mark true
    for i, flag in enumerate(c):
        if not flag:  # hard example is false
            x_list.append(data_set[i])
            y_list.append(input_label[i])
    print('x_list hard len ', len(x_list), 'y_list hard len', len(y_list))
    x_list = np.asarray(x_list)
    y_list = np.asarray(y_list)
    return x_list, y_list


def find_hard_examples(dataset_path, model_last, pred_threshold, file_len, hard_file_name):
    """
        find hard data
        save hard
    """
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    x_list = None
    y_list = None
    c1_model, c2_model = generator_eva_model(model_last)
    train_dataset_path = os.path.join(dataset_path, 'train')
    file_paths, all_data_len = get_file_path_list(
        train_dataset_path, 'tigress', file_len)
    for file_path in file_paths:
        data, y_true = load_file(file_path)
        y1_pred = c1_model.predict(data)
        y2_pred = c2_model.predict(data)
        x_1, y_1 = get_hard_index(
            pred_threshold, y1_pred, y2_pred, y_true, data)
        if y_1 is None or len(y_1) == 0:
            continue
        if y_list is None or len(y_list) == 0:
            x_list = x_1
            y_list = y_1
        elif len(y_list) != 0 and y_list is not None:
            print('x_list length ')
            print(len(x_list))
            try:
                x_list = np.concatenate([x_list, x_1], axis=0)
                y_list = np.hstack([y_list, y_1])
            except IOError:
                print(file_path)
                print("this file is none")
        if len(y_list) > file_len:
            x_list_out = x_list[:file_len]
            y_list_out = y_list[:file_len]
            pkl_name = utils.give_file_name(len(y_list_out))
            pkl_name = os.path.join(
                dataset_path, 'train', hard_file_name, pkl_name)
            utils.data2pkl([x_list_out, y_list_out], pkl_name)

            x_list = x_list[file_len:]
            y_list = y_list[file_len:]
            print('x_list1 len', len(x_list), 'y_list1  len', len(y_list))
    print("hard example find done")


def data_generator(file_path_list, batch_size):
    """
        generate data
        step_num:  select 
        1-3.1
        2-3.21、3.22、3.3
    """
    file_index = 0
    epoch_num = 1
    print(len(file_path_list))
    while file_index < len(file_path_list):
        data, labels = load_file(file_path_list[file_index])
        data = np.asarray(data)
        labels = np.asarray(labels)
        iter_num = int(len(data) / batch_size)  # loop  times
        i = 0
        while iter_num:  # iter_num==
            # A batch of data represented by digital vectors
            batch_data = data[i:i + batch_size]
            batched_labels = labels[i:i + batch_size]
            yield batch_data, [batched_labels, batched_labels]
            i = i + batch_size
            iter_num -= 1
        file_index += 1
        if file_index == len(file_path_list):
            print('\n')
            print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            print('--------------epoch: ' +
                  str(epoch_num) + '  train  end -------------------')
            epoch_num += 1
            file_index = 0


def get_gen_path_list(file_path_list, step_len, last_begin):
    """
        1 file list
    """
    file_path_list_len = len(file_path_list)
    if file_path_list_len <= step_len:
        return file_path_list, 0
    if file_path_list_len < last_begin + step_len:
        path_list = file_path_list[last_begin:]
        last_begin = last_begin + step_len - file_path_list_len
        path_list.extend(file_path_list[:last_begin])
    else:
        path_list = file_path_list[last_begin:last_begin + step_len]
        last_begin = last_begin + step_len
    return path_list, last_begin


def data_generator_from_list(file_path_list, batch_size, step_len):
    """
        generate data
        step_num:  select
        1-3.1
        2-3.21、3.22、3.3
    """
    # file_index = 0
    # epoch_num = 1
    print('file_path_list has :', len(file_path_list))
    # step_len = 10
    last_begin = 0
    while True:
        path_list, last_begin = get_gen_path_list(
            file_path_list, step_len, last_begin)
        data, labels = load_file_list(path_list)

        iter_num = int(len(data) / batch_size)  # loop  times
        i = 0
        while iter_num:  # iter_num==0 jump out
            # A batch of data represented by digital vectors
            batch_data = data[i:i + batch_size]
            batched_labels = labels[i:i + batch_size]
            yield batch_data, [batched_labels, batched_labels]
            i = i + batch_size
            iter_num -= 1


def data_generator_from_list_two(file_paths_list, batch_size, step_len):
    """
        generate data
         generate   origin  sample and hard sample
    """
    file_index = 0
    epoch_num = 1
    print(len(file_paths_list))
    origin_file_paths = file_paths_list[0]
    hard_file_paths = file_paths_list[1]
    max_file_num = max(len(origin_file_paths), len(hard_file_paths))
    # A = Y if X else Z
    if len(origin_file_paths) > len(hard_file_paths):
        hard_file_paths = fill_file(max_file_num, hard_file_paths)
    else:
        origin_file_paths = fill_file(max_file_num, origin_file_paths)
    last_begin_origin = 0
    last_begin_hard = 0
    while True:
        origin_path_list, last_begin_origin = get_gen_path_list(
            origin_file_paths, step_len, last_begin_origin)
        hard_path_list, last_begin_hard = get_gen_path_list(
            origin_file_paths, step_len, last_begin_hard)
        origin_data, origin_labels = load_file_list(origin_path_list)
        hard_data, hard_labels = load_file_list(hard_path_list)
        iter_num = int(len(origin_data) / batch_size)  # loop  times
        i = 0
        while iter_num:
            # A batch of data represented by digital vectors
            origin_batch_data = origin_data[i:i + batch_size]
            origin_batched_labels = origin_labels[i:i + batch_size]
            #
            hard_batch_data = hard_data[i:i + batch_size]
            yield [origin_batch_data, hard_batch_data], [
                origin_batched_labels, origin_batched_labels, origin_batched_labels, origin_batched_labels]
            i = i + batch_size
            iter_num -= 1


def data_generator_two(file_paths_list, batch_size):
    """
        generate data
         generate   origin  sample and hard sample
    """
    file_index = 0
    epoch_num = 1
    print(len(file_paths_list))
    origin_file_paths = file_paths_list[0]
    hard_file_paths = file_paths_list[1]
    max_file_num = max(len(origin_file_paths), len(hard_file_paths))
    # A = Y if X else Z
    if len(origin_file_paths) > len(hard_file_paths):
        hard_file_paths = fill_file(max_file_num, hard_file_paths)
    else:
        origin_file_paths = fill_file(max_file_num, origin_file_paths)
    while file_index < max_file_num:
        origin_data, origin_labels = load_file(origin_file_paths[file_index])
        hard_data, hard_labels = load_file(hard_file_paths[file_index])
        iter_num = int(len(origin_data) / batch_size)  # loop  times
        i = 0
        while iter_num:
            # A batch of data represented by digital vectors
            origin_batch_data = origin_data[i:i + batch_size]
            origin_batched_labels = origin_labels[i:i + batch_size]
            #
            hard_batch_data = hard_data[i:i + batch_size]
            yield [origin_batch_data, hard_batch_data], [
                origin_batched_labels, origin_batched_labels, origin_batched_labels, origin_batched_labels]
            i = i + batch_size
            iter_num -= 1
        file_index += 1
        if file_index == max_file_num:
            print('\n')
            print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            print('--------------epoch times:  ' +
                  str(epoch_num) + '  train  end -------------------')
            epoch_num += 1
            file_index = 0


def fill_file(max_file_num, file_paths):
    times = int(max_file_num / len(file_paths))
    tmp = file_paths[:]
    print(times)
    while times >= 2:
        times = times - 1
        file_paths.extend(tmp)
    file_paths.extend(random.sample(
        file_paths, max_file_num - len(file_paths)))
    return file_paths


def produce_val_data(all_vector, file_len):
    for tog in ['origin', 'tigress']:
        dataset_path_list, all_data_len = get_file_path_list(
            os.path.join(all_vector, 'test'), tog, file_len)
        val_data = None
        list_len = len(dataset_path_list)
        if list_len > 1:
            val_data = dataset_path_list[:int(list_len / 2)]
        path2 = os.path.join(all_vector, 'validation', tog)
        os.makedirs(path2, exist_ok=True)
        if val_data is not None:
            for pkl1 in val_data:
                com_str = 'mv  ' + pkl1 + '   ' + path2
                os.system(com_str)

