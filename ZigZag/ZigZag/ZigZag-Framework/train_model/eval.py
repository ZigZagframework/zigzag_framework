# -*- coding: utf-8 -*-
#
# datetime:2022/3/6 20:42

"""
description：
"""
import os
import time
from tensorflow.keras.models import load_model

from model.evaluation_model import evaluation_with_predict


os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"] = "1"  # "1,2,3"
os.environ['KERAS_BACKEND'] = 'tensorflow'


def eval_3_1(model_path):
    model_path = os.path.join(model_path, '20220407-1-3.1.h5')
    print(model_path)
    model_last = load_model(model_path)
    evaluation_with_predict(testDataSetPath, model_last,
                            resultPath, predThreshold)


if __name__ == "__main__":
    batchSize = 64
    vectorDim = 40
    maxLen = 500
    dropout = 0.2
    trainDatasetPath = "/data1/yjy/dataset/zigzag/pass_hp/train/"  # 数据save path
    validationDatasetPath = "/data1/yjy/dataset/zigzag/pass_hp/validation/"
    testDataSetPath = "/data1/yjy/dataset/zigzag/pass_hp/test/"
    serialNumber = '20220407-1'  # 日期
    modelKind = 'BGRU'  # select model
    predThreshold = 0.5  # 分类正确的 Threshold
    modelPath = "/data1/yjy/dataset/zigzag/model"  # model save path，需要save用户 path-/
    resultPath = '/data1/yjy/dataset/zigzag/result'  # result save path
    epochTimes = [15, 4, 6, 3]  # 3.1-epochTimes[0]\3.21-1
    modelPath = os.path.join(modelPath, modelKind, serialNumber)
    resultPath = os.path.join(resultPath, modelKind, serialNumber)
    os.makedirs(modelPath, exist_ok=True)
    os.makedirs(resultPath, exist_ok=True)
    print(modelPath)
    eval_3_1(modelPath)
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
