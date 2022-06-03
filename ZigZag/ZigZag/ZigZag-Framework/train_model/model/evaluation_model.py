# -*- coding: utf-8 -*-
#
# datetime:2022/2/19 15:58

"""
description：model  eval 
"""

import math
from sklearn.metrics import *
from preprocess.process_data import *
from preprocess.load_data import *
from tools.oth_tools import *
from model.bgru_generator_model import *


def save_metrics(result_data, samples_num, result_path, classifier_name):
    """
        写入 eval  result 到文件
        classifier_name:分类器名称
    """
    score, TP, FP, FN, precision, recall, f_score = result_data[0]
    TN = samples_num - TP - FP - FN
    mkdir(result_path)
    with open(result_path + '/metrocs.txt', 'a+') as fwrite:
        fwrite.write(classifier_name + 'Metrics recode' + '\n')
        fwrite.write('cdg_ddg: ' + ' ' + str(samples_num) + '\n')
        fwrite.write("TP:" + str(TP) + ' FP:' + str(FP) +
                     ' FN:' + str(FN) + ' TN:' + str(TN) + '\n')
        FPR = float(FP) / (FP + TN)
        fwrite.write('FPR: ' + str(FPR) + '\n')
        FNR = float(FN) / (TP + FN)
        fwrite.write('FNR: ' + str(FNR) + '\n')
        Accuracy = float(TP + TN) / samples_num
        fwrite.write('Accuracy: ' + str(Accuracy) + '\n')
        precision = float(TP) / (TP + FP)
        fwrite.write('precision: ' + str(precision) + '\n')
        recall = float(TP) / (TP + FN)
        fwrite.write('recall: ' + str(recall) + '\n')
        f_score = (2 * precision * recall) / (precision + recall)
        fwrite.write('fbeta_score: ' + str(f_score) + '\n')
        fwrite.write('--------------------\n')


def testcase2func(result_data, test_cases, result_path, funcs_file):
    dict_testcase2func = {}
    for i in test_cases:
        if i not in dict_testcase2func:
            dict_testcase2func[i] = {}
    TP_index = result_data[1]
    for i in TP_index:
        if not funcs_file[i]:
            continue
        for func in funcs_file[i]:
            if func in dict_testcase2func[test_cases[i]].keys():
                dict_testcase2func[test_cases[i]][func].append("TP")
            else:
                dict_testcase2func[test_cases[i]][func] = ["TP"]
    FP_index = result_data[2]
    for i in FP_index:
        if not funcs_file[i]:
            continue
        for func in funcs_file[i]:
            if func in dict_testcase2func[test_cases[i]].keys():
                dict_testcase2func[test_cases[i]][func].append("FP")
            else:
                dict_testcase2func[test_cases[i]][func] = ["FP"]
    with open(result_path + "/dict_testcase2func_flatten.pkl", 'wb') as f:
        pickle.dump(dict_testcase2func, f)


def evaluation_with_generator(test_dataset_path, batch_size, max_len, vector_dim, model_path, result_path):
    print("evaluation begin ... ")
    # 1.加载model
    c1_model, c2_model = generator_eva_model(model_path)

    # 2.读数据
    dataset, labels, test_cases, funcs_file = load_test_data(test_dataset_path)

    test_generator = generator_of_data(
        dataset, labels, batch_size, max_len, vector_dim)
    samples_num = len(dataset)
    steps_epoch = int(math.ceil(samples_num / batch_size))

    result_data = c1_model.evaluate_generator(
        test_generator, steps=steps_epoch)
    classifier_name = 'classifier1--evaluation_with_generator'
    save_metrics(result_data, samples_num, result_path, classifier_name)
    testcase2func(result_data, test_cases, result_path, funcs_file)

    result_data = c2_model.evaluate_generator(
        test_generator, steps=steps_epoch)
    classifier_name = 'classifier2--evaluation_with_generator'
    save_metrics(result_data, samples_num, result_path, classifier_name)
    testcase2func(result_data, test_cases, result_path, funcs_file)


def metrics_p(y_pred, pred_threshold, y_true, result_file, model_name):
    y_pred[y_pred >= pred_threshold] = 1
    y_pred[y_pred < pred_threshold] = 0
    y_pred = y_pred.flatten()
    # print(classification_report(y_true, y_pred))
    acc = accuracy_score(y_true, y_pred)
    precision = precision_score(y_true, y_pred)
    recall = recall_score(y_true, y_pred)
    f_score = f1_score(y_true, y_pred)
    fpr = 1 - precision
    fnr = 1 - recall
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
    # print(f"""----------------------------\n
    # >>> Result: \n
    # >>> Accuracy: {acc} \n
    # >>> Precision: {precision}\n
    # >>> Recall: {recall}\n
    # >>> F1: {f_score}\n
    # >>> tn:{tn}--fp:{fp}--fn:{fn}--tp:{tp}\n""")
    # 误报率=1-精确率（查准率）
    # fpr=1-precision
    # 漏报率=1-召回率（查全率）
    # fnr=1-recall

    with open(result_file, 'a+') as fwrite:
        # fwrite.write(f"model_name,acc,precision,recall,F1,tn,tp,fp,fn\n")
        fwrite.write(
            f"{model_name},{acc:.5f},{precision:.5f},{recall:.5f},{f_score:.5f},{tn},{tp},{fp},{fn},{fpr:.5f},{fnr:.5f}\n")

    return acc, f_score


def print_mid(test_dataset_path, model_last):
    c1_model, c2_model, merge_model = generator_print_mid(model_last)
    test_dataset, y_true = load_data_once(test_dataset_path)
    y1_pred = c1_model.predict(test_dataset)[0:10]
    y2_pred = c2_model.predict(test_dataset)[0:10]
    merge_pred = merge_model.predict(test_dataset)[0:10]
    print('y1_pred-----shape', y1_pred.shape)
    print(y1_pred)
    print('y2_pred-----shape', y2_pred.shape)
    print(y2_pred)
    print('merge_pred-----shape', y2_pred.shape)
    print(merge_pred)


def evaluation_with_predict(test_dataset_path, model_last, result_file, pred_threshold, train_step):
    c1_model, c2_model = generator_eva_model(model_last)
    test_dataset, y_true = load_data_once(test_dataset_path)
    y1_pred = c1_model.predict(test_dataset)
    y2_pred = c2_model.predict(test_dataset)

    y_true.reshape(-1, 1)
    acc1, f_score1 = metrics_p(y1_pred, pred_threshold, y_true, result_file, train_step)
    acc2, f_score2 = metrics_p(y2_pred, pred_threshold, y_true, result_file, train_step)

    return max(acc1, acc2), max(f_score1, f_score2)


def evaluation_stat(test_dataset_path, model_last, result_file, pred_threshold, train_step):
    test_dataset, y_true = load_data_once(test_dataset_path)
    y1_pred = model_last.predict(test_dataset)

    y_true.reshape(-1, 1)
    acc1, f_score1 = metrics_p(y1_pred, pred_threshold, y_true, result_file, train_step)

    return acc1, f_score1


def evaluation_origin_data():
    pass

# if __name__ == "__main__":
#     batchSize = 64
#     vectorDim = 40
#     maxLen = 500
#     dropout = 0.2
#     trainDatasetPath = "/data1/yjy/dataset/zigzag/pass_hp/train/"  # 数据save path
#     validationDatasetPath = "/data1/yjy/dataset/zigzag/pass_hp/validation/"
#     testDataSetPath = "/data1/yjy/dataset/zigzag/pass_hp/test/"
#     serialNumber = '20220407-1'  # 日期
#     modelKind = 'BGRU'  #  select model
#     predThreshold = 0.5  # 分类正确的 Threshold
#     modelPath = "/home/yjy/code/zigzag/data/model"  # model save path，需要save用户 path-
#     resultPath = 'data/result'  #  result save path
#     modelPath = os.path.join(modelPath, modelKind, serialNumber)
#     resultPath = os.path.join(resultPath, modelKind, serialNumber)
#     os.makedirs(modelPath, exist_ok=True)
#     os.makedirs(resultPath, exist_ok=True)
#     # model_file = os.path.join(modelPath, '20220407-1-3.1.h5')
#     model_path = os.path.join(modelPath, 'model3.1-15-0.07991-0.95752-val.h5')
#     model_file = "/home/yjy/code/zigzag/data/model/BGRU/20220407-1/20220407-1-3.1.h5"
#     print(model_file)
#     for file in os.listdir('/home/yjy/code/zigzag/data/model/BGRU/20220407-1/'):
#         print(file)
#     evaluation_with_predict(testDataSetPath, batchSize, maxLen, vectorDim, modelPath, model_file, predThreshold)
#
#     print(modelPath)
