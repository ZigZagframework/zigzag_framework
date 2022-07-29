# -*- coding: utf-8 -*-
#
# datetime:2022/3/6 20:41

"""
description：train zigzag model start 
"""
import sys
import time
import os
from tensorflow.keras.models import load_model
import argparse
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from src.preprocess import load_data
from src.preprocess.process_data import find_hard_examples
from src.model.evaluation_model import evaluation_with_predict
from src.model.train_model import TranModel

os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"] = "0"  # "1,2,3"
os.environ['KERAS_BACKEND'] = 'tensorflow'

# Training settings
parser = argparse.ArgumentParser(description='tf zigzag')
parser.add_argument('--modelKind', type=str, default='BGRU',
                    help='modelKind')
parser.add_argument('--predThreshold', type=float, default=0.4,
                    help='Threshold')
parser.add_argument('--epochTimes', type=str, default='30,2,2,2',
                    help='step epochTimes')
parser.add_argument('--learningRate', type=str, default='0.0012, 0.001, 0.0003, 0.0001', help='learningRate')
parser.add_argument('--trainTimes', type=int, default=100,
                    help='evaluation only option')
args = parser.parse_args()


def train_begin(model_path, train_times):
    """
        train process and keep train 
        train_times:   loop train_times ： 3.2 origin -3.2 -3.3
    """
    if not os.path.exists(os.path.join(modelPath, model_name_list[0])):
        mv_model_command = 'cp ' + '  ' + os.path.join(modelPathAll, modelKind,
                                                       model_name_list[0]) + '  \"' + modelPath + '\"'
        os.system(mv_model_command)
        print(mv_model_command)
    max_acc = 0
    max_f_score = 0
    max_stop_step = 7
    stop_step = 0
    stop_flag = False
    model_last, i = load_data.return_last_count(
        metricsFile, model_path, model_name_list)
    if i == 0:
        model_name = str(i + 1) + model_name_list[0]
        evaluation_with_predict(
            testDataSetPath, model_last, metricsFile, predThreshold, model_name)
    if is_find_hard:
        hard_file_name = 'hard-' + serialNumber
        del_hard_file_command, hard_file_path = hard_name_and_path(
            datePath, hard_file_name)
    else:
        hard_file_name = 'tigress'
    while i < train_times:
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        print('----------- loop times :' + str(i + 1) +
              '---train  begin------------------')
        # 1
        model_name = str(i + 1) + model_name_list[1]
        model_last = trainModel.train_3_2_1(model_last, model_name)
        print('model3.21 eval result ---------------------------------')
        if is_find_hard:
            os.makedirs(hard_file_path, exist_ok=True)
            find_hard_examples(datePath, model_last,
                               predThreshold, fileLen, hard_file_name)
        acc, f_score = evaluation_with_predict(
            testDataSetPath, model_last, metricsFile, predThreshold, model_name)
        # stop early
        if not stop_flag and max_acc > 0.78 and max_f_score > 0.67:
            stop_flag = True
        if stop_flag and stop_step >= max_stop_step and i > 12:
            with open(metricsFile, 'a+') as fwrite:
                fwrite.write(
                    f"stop early,max_f_1,{max_f_score},max_acc,{max_acc}\n")
            break
        if stop_flag and max_f_score > f_score:
            stop_step = stop_step + 1
        elif max_f_score < f_score or max_acc < acc:
            stop_step = 0

        max_acc = max(max_acc, acc)
        max_f_score = max(max_f_score, f_score)

        # 2
        model_last2 = load_model(os.path.join(model_path, model_name))
        model_name = str(i + 1) + model_name_list[2]
        model_last = trainModel.train_3_2_2(
            model_last, model_last2, model_name, hard_file_name)
        print('model3.22 eval result')
        evaluation_with_predict(
            testDataSetPath, model_last, metricsFile, predThreshold, model_name)
        # 3
        model_name = str(i + 1) + model_name_list[3]
        model_last = trainModel.train_3_3(model_last, model_name)
        print('model3.3 eval result ')
        evaluation_with_predict(
            testDataSetPath, model_last, metricsFile, predThreshold, model_name)
        if is_find_hard:
            os.system(del_hard_file_command)
        i = i + 1
        print('----------- loop times: ' + str(i) +
              '--train  end ------------------')


def hard_name_and_path(date_path, hard_file_name):
    # rm -rf /data1/yjy/dataset/zigzag/data-step-20/hard/*
    hard_file_path = os.path.join(date_path, 'train', hard_file_name)
    del_hard_file_command = 'rm -rf ' + hard_file_path
    print(del_hard_file_command)
    return del_hard_file_command, hard_file_path


# /home/yjy/code/zigzag/zigzag03/zigzag/
# /data1/yjy/dataset/zigzag/model/
if __name__ == "__main__":
    batchSize = 64
    vectorDim = 40
    maxLen = 500
    dropout = 0.2
    dataFileName = 'zigzag_vector_220720'
    step_len = 40  # step_len
    datePath = os.path.join('/data1/yjy/dataset/', dataFileName)  # /data1/yjy/dataset/zigzag_vector_220720/
    modelPathAll = "/data1/yjy/dataset/zigzag/model"
    resultPath = '/data1/yjy/dataset/zigzag/result'  # result save path
    model_name_list = ['model-3.1.h5', 'model-3.21.h5',
                       'model-3.22.h5', 'model-3.3.h5']
    is_find_hard = False
    fileLen = 320
    modelKind = args.modelKind  # select model
    predThreshold = args.predThreshold  # Threshold
    epochTimes = [int(item) for item in args.epochTimes.split(',')]
    learningRate = [float(item) for item in args.learningRate.split(',')]
    trainTimes = args.trainTimes
    serialNumber = f'{dataFileName}-epochTimes-{epochTimes}-learningRate-{learningRate}-modelKind-{modelKind}-predThreshold-{predThreshold}-is_find_hard-{str(is_find_hard)}'
    modelPath = os.path.join(modelPathAll, modelKind, serialNumber)
    resultPath = os.path.join(resultPath, modelKind, serialNumber)
    os.makedirs(modelPath, exist_ok=True)
    os.makedirs(resultPath, exist_ok=True)
    testDataSetPath = os.path.join(datePath, 'test')
    metricsFileName = serialNumber + '.csv'
    metricsFile = os.path.join(resultPath, metricsFileName)
    print(modelPath)
    trainModel = TranModel(modelKind, datePath, modelPath, resultPath, batchSize, maxLen, vectorDim, dropout,
                           serialNumber, predThreshold, epochTimes, learningRate, fileLen, step_len)
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    modelLast = trainModel.train_3_1(model_name_list[0])
    # evaluation_with_predict(testDataSetPath, modelLast,
    #                         metricsFile, predThreshold, 'model-3.1.h5')
    # train_begin(modelPath, trainTimes)
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    print('-----------train  end -----------')
