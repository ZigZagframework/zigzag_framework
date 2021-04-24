## -*- coding: utf-8 -*-
'''
This python file is used to train four class focus data in blstm model
===============================================================
'''

from keras.preprocessing import sequence
from keras.optimizers import SGD, RMSprop, Adagrad, Adam, Adadelta
from keras.models import Sequential, load_model, Model
from keras.layers import Input
from keras.layers.core import Masking, Dense, Dropout, Activation
from keras.layers.recurrent import LSTM,GRU
from preprocess_dl_Input_sard_0528 import *
from keras.layers.wrappers import Bidirectional
from collections import Counter
import numpy as np
import pickle
import random
import time
import math
import os

RANDOMSEED = 2018  # for reproducibility
os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"] = "1"

class LossHistory(keras.callbacks.Callback):
    def on_train_begin(self, logs={}):
        self.losses = []
 
    def on_batch_end(self, batch, logs={}):
        self.losses.append(logs.get('loss'))


def generator_model(maxlen, vector_dim, layers, dropout):
    
    inputs = Input(shape=(maxlen, vector_dim))
    mask_1 = Masking(mask_value=0.0, name='mask_1')(inputs)
    bgru_1 = Bidirectional(GRU(units=256, activation='tanh', recurrent_activation='hard_sigmoid', return_sequences=True), name='bgru_1')(mask_1)
    dropout_1 = Dropout(dropout, name='dropout_1')(bgru_1)
    bgru_2 = Bidirectional(GRU(units=256, activation='tanh', recurrent_activation='hard_sigmoid', return_sequences=True), name='bgru_2')(dropout_1)
    dropout_2 = Dropout(dropout, name='dropout_2')(bgru_2)
	
    g = Model(inputs= inputs,outputs=dropout_2)
    g.summary()
    
    return g,dropout_2


def classifier_model(dropout_2):
    
    classifier_1 = Dense((1,activation='sigmoid'),name='classifier_1')(dropout_2)
    classifier_2 = Dense((1,activation='sigmoid'),name='classifier_2')(dropout_2)

    c1 = Model(inputs=dropout_2,outputs=classifier_1)
    c2 = Model(inputs=dropout_2,outputs=classifier_2)
    c1.summary()
    c2.summary()
    return c1,c2,classifier_1,classifier_2

def build_model(g,c1,c2,inputs,classifier_1,classifier_2):

    g.trainable = True
    c1.trainable = True
    c2.trainable = True

    print("begin compile")    
	
    c1.compile(loss='binary_crossentropy', optimizer='adamax', metrics=['TP_count', 'FP_count', 'FN_count', 'precision', 'recall', 'fbeta_score'])
    c2.compile(loss='binary_crossentropy', optimizer='adamax', metrics=['TP_count', 'FP_count', 'FN_count', 'precision', 'recall', 'fbeta_score'])

    return g,c1,c2,classifier_1,classifier_2


def main(traindataSet_path, testdataSet_path, realtestpath, weightpath, resultpath, batch_size, maxlen, vector_dim, layers, dropout):
    print("Loading data...")
    
    g,c1,c2,outputs_1,outputs_2 = build_model(maxlen, vector_dim, layers, dropout)
    print(outputs_1,outputs_2)
    
    #model.load_weights(weightpath)
    
    print("Train...")
    dataset_raw = []
    labels_raw = []
    testcases_raw = []
    filenames_raw = []
    for folder in os.listdir(traindataSet_path):
        for filename in os.listdir(os.path.join(traindataSet_path,folder)):
            if(filename.endswith("raw.pkl") is False):
                continue
            print(filename)
            f = open(os.path.join(traindataSet_path, folder, filename),"rb")
            dataset_file,labels_file,funcs_file,filenames_file,testcases_file = pickle.load(f)
            f.close()
            dataset_raw += dataset_file
            labels_raw += labels_file
            testcases_raw += testcases_file
            #filenames += filenames_file			
    print(len(dataset_raw), len(labels_raw), len(testcases_raw))
    
    bin_labels = []
    for label in labels_raw:
        bin_labels.append(multi_labels_to_two(label))
    labels_raw = bin_labels
    #print(labels)
    
       
    np.random.seed(RANDOMSEED)
    np.random.shuffle(dataset_raw)
    np.random.seed(RANDOMSEED)
    np.random.shuffle(labels_raw)

    dataset_con = []
    labels_con = []
    testcases_con = []
    filenames_con = []
    for folder in os.listdir(traindataSet_path):
        for filename in os.listdir(os.path.join(traindataSet_path,folder)):
            if(filename.endswith("raw.pkl") is True):
                continue
            print(filename)
            f = open(os.path.join(traindataSet_path, folder, filename),"rb")
            dataset_file,labels_file,funcs_file,filenames_file,testcases_file = pickle.load(f)
            f.close()
            dataset_con += dataset_file
            labels_con += labels_file
            testcases_con += testcases_file
            #filenames += filenames_file			
    print(len(dataset_con), len(labels_con), len(testcases_con))
    
    bin_labels = []
    for label in labels_con:
        bin_labels.append(multi_labels_to_two(label))
    labels_con = bin_labels
    #print(labels)
    
       
    np.random.seed(RANDOMSEED)
    np.random.shuffle(dataset_con)
    np.random.seed(RANDOMSEED)
    np.random.shuffle(labels_con)

    #c1.compile(loss='binary_crossentropy', optimizer='adamax', metrics=['TP_count', 'FP_count', 'FN_count', 'precision', 'recall', 'fbeta_score'])
    #c2.compile(loss='binary_crossentropy', optimizer='adamax', metrics=['TP_count', 'FP_count', 'FN_count', 'precision', 'recall', 'fbeta_score'])
    #c1_c2_on_g_1.compile(loss = 'binary_crossentropy', optimizer='adamax', metrics=['TP_count', 'FP_count', 'FN_count', 'precision', 'recall', 'fbeta_score'])

    t1 = time.time()
    for epoch in range(4):
        print("Epoch is:",epoch)
        train_generator = generator_of_data(dataset_raw, labels_raw, batch_size, maxlen, vector_dim)    
        all_train_samples = len(dataset_raw)
        steps_epoch = int(all_train_samples / batch_size)
        print("Number of batches:",steps_epoch)	
		
        c1.fit_generator(train_generator, steps_per_epoch=steps_epoch,epochs=1,callbacks=[history])
        history = LossHistory()
        loss_1 = history.losses

        c2.fit_generator(train_generator, steps_per_epoch=steps_epoch,epochs=1,callbacks=[history])
        history = LossHistory()
        loss_2 = history.losses	

        loss_s = loss_1 + loss_2
        #c1_c2_on_g.compile(loss=loss_s, optimizer='adamax', metrics=['TP_count', 'FP_count', 'FN_count', 'precision', 'recall', 'fbeta_score'])
		
        train_generator = generator_of_data(dataset_raw, labels_raw, batch_size, maxlen, vector_dim)    
        all_train_samples = len(dataset_raw)
        steps_epoch = int(all_train_samples / batch_size)
        print("Number of batches:",steps_epoch)	
		
		g.trainable = False
        c1.fit_generator(train_generator, steps_per_epoch=steps_epoch,epochs=1,callbacks=[history])
        history = LossHistory()
        loss_1 = history.losses

        c2.fit_generator(train_generator, steps_per_epoch=steps_epoch,epochs=1,callbacks=[history])
        history = LossHistory()
        loss_2 = history.losses	

        loss_s = loss_1 + loss_2
        #c1_c2_on_g.compile(loss=loss_s, optimizer='adamax', metrics=['TP_count', 'FP_count', 'FN_count', 'precision', 'recall', 'fbeta_score'])
		
        train_generator = generator_of_data(dataset_con, labels_con, batch_size, maxlen, vector_dim)    
        all_train_samples = len(dataset_con)
        steps_epoch = int(all_train_samples / batch_size)
        print("Number of batches:",steps_epoch)	
		
        c1.fit_generator(train_generator, steps_per_epoch=steps_epoch,epochs=1,callbacks=[history])
        history = LossHistory()
        loss_1 = history.losses

        c2.fit_generator(train_generator, steps_per_epoch=steps_epoch,epochs=1,callbacks=[history])
        history = LossHistory()
        loss_2 = history.losses	

        print(outputs_1,outputs_2)
        loss_dis = np.mean(np.abs(outputs_1 - outputs_2))
        loss = loss_s + (-loss_dis)
        #c1_c2_on_g.compile(loss=loss_s, optimizer='adamax', metrics=['TP_count', 'FP_count', 'FN_count', 'precision', 'recall', 'fbeta_score'])
		
		c1.trainable = False
        c2.trainable = False
		
        train_generator = generator_of_data(dataset_con, labels_con, batch_size, maxlen, vector_dim)    
        all_train_samples = len(dataset_con)
        steps_epoch = int(all_train_samples / batch_size)
        print("Number of batches:",steps_epoch)	
		
        c1.fit_generator(train_generator, steps_per_epoch=steps_epoch,epochs=1,callbacks=[history])
        history = LossHistory()
        loss_1 = history.losses

        c2.fit_generator(train_generator, steps_per_epoch=steps_epoch,epochs=1,callbacks=[history])
        history = LossHistory()
        loss_2 = history.losses	

        print(outputs_1,outputs_2)
        loss_dis = np.mean(np.abs(outputs_1 - outputs_2))
        #c1_c2_on_g.compile(loss=loss_s, optimizer='adamax', metrics=['TP_count', 'FP_count', 'FN_count', 'precision', 'recall', 'fbeta_score'])
        		

        g.save_weights(weightpath_g, True)
        c1.save_weights(weightpath_c1, True)	
        c2.save_weights(weightpath_c2, True)			

    t2 = time.time()       		
    train_time = t2 - t1
    
    c1.load_weights(weightpath_c1)
    c2.load_weights(weightpath_c2)
    g.load_weights(weightpath_g)

    print("Test...")
    dataset = []
    labels = []
    testcases = []
    filenames = []
    funcs = []
    for folder in os.listdir(testdataSet_path):
        for filename in os.listdir(os.path.join(testdataSet_path,folder)):
            if(filename.endswith("flatten.pkl") is False):
                continue
            #if "NVD" in filename:
                #continue
            print(filename)
            f = open(os.path.join(testdataSet_path, folder, filename),"rb")
            datasetfile,labelsfile,funcsfile,filenamesfile,testcasesfile = pickle.load(f)
            f.close()
            dataset += datasetfile
            labels += labelsfile
            testcases += testcasesfile
            filenames += filenamesfile
            funcs += funcsfile
    print(len(dataset), len(labels), len(funcs), len(filenames), len(testcases))
    
    bin_labels = []
    for label in labels:
        bin_labels.append(multi_labels_to_two(label))
    labels = bin_labels
    #print(labels)
    
    #index = -1
    batch_size = 64
    test_generator = generator_of_data(dataset, labels, batch_size, maxlen, vector_dim)
    all_test_samples = len(dataset)
    steps_epoch = int(math.ceil(all_test_samples / batch_size))

    t1 = time.time()
    result = c1.evaluate_generator(test_generator, steps=steps_epoch)
    t2 = time.time()
    test_time = t2 - t1
    #print(result)
    score, TP, FP, FN, precision, recall, f_score= result[0]
    #f = open("TP_index_bgru_flatten_split0726.pkl",'wb')
    #pickle.dump(result[1], f)
    #f.close()
    
    TN = all_test_samples - TP - FP - FN
    fwrite = open(resultpath, 'a')
    fwrite.write('cdg_ddg: ' + ' ' + str(all_test_samples) + '\n')
    fwrite.write("TP:" + str(TP) + ' FP:' + str(FP) + ' FN:' + str(FN) + ' TN:' + str(TN) +'\n')
    FPR = float(FP) / (FP + TN)
    fwrite.write('FPR: ' + str(FPR) + '\n')
    FNR = float(FN) / (TP + FN)
    fwrite.write('FNR: ' + str(FNR) + '\n')
    Accuracy = float(TP + TN) / (all_test_samples)
    fwrite.write('Accuracy: ' + str(Accuracy) + '\n')
    precision = float(TP) / (TP + FP)
    fwrite.write('precision: ' + str(precision) + '\n')
    recall = float(TP) / (TP + FN)
    fwrite.write('recall: ' + str(recall) + '\n')
    f_score = (2 * precision * recall) / (precision + recall)
    fwrite.write('fbeta_score: ' + str(f_score) + '\n')
    #fwrite.write('train_time:' + str(train_time) +'  ' + 'test_time:' + str(test_time) + '\n')
    fwrite.write('--------------------\n')
    fwrite.close()
    
    
    dict_testcase2func = {}
    for i in testcases:
        if not i in dict_testcase2func:
            dict_testcase2func[i] = {}
    TP_indexs = result[1]
    for i in TP_indexs:
        if funcs[i] == []:
            continue
        for func in funcs[i]:
            if func in dict_testcase2func[testcases[i]].keys():
                dict_testcase2func[testcases[i]][func].append("TP")
            else:
                dict_testcase2func[testcases[i]][func] = ["TP"]
    FP_indexs = result[2]
    for i in FP_indexs:
        if funcs[i] == []:
            continue
        for func in funcs[i]:
            if func in dict_testcase2func[testcases[i]].keys():
                dict_testcase2func[testcases[i]][func].append("FP")
            else:
                dict_testcase2func[testcases[i]][func] = ["FP"]
    f = open(resultpath+"_dict_testcase2func_0929_flatten.pkl",'wb')
    #pickle.dump(dict_testcase2func, f)
    pickle.dump(dict_testcase2func, f)
    f.close()
    
	

def testrealdata(realtestpath, weightpath, batch_size, maxlen, vector_dim, layers, dropout):
    model = build_model(maxlen, vector_dim, layers, dropout)
    model.load_weights(weightpath)
    
    print("Loading data...")
    for filename in os.listdir(realtestpath):
        print(filename)
        f = open(realtestpath+filename, "rb")
        realdata = pickle.load(f,encoding="latin1")
        f.close()
    
        labels = model.predict(x = realdata[0],batch_size = 1)
        for i in range(len(labels)):
            if labels[i][0] >= 0.5:
                print(realdata[1][i])


if __name__ == "__main__":
    batchSize = 64
    vectorDim = 40
    maxLen = 500 
    layers = 1
    dropout = 0.2
    traindataSetPath = "./data/dl_input_shuffle_w2v/train/"
    testdataSetPath = "./data/dl_input_shuffle_w2v/test/"
    #testdataSetPath2 = "./dl_input_shuffle/cdg_ddg_apart/test/SARD/"
    #testdataSetPath3 = "./dl_input_shuffle/cdg_ddg_apart/test/NVD/"
    realtestdataSetPath = "data/"
    weightPath = './model/BGRU_0929_flatten'
    resultPath = "./result/BGRU_0929_flatten"
    #dealrawdata(raw_traindataSetPath, raw_testdataSetPath, traindataSetPath, testdataSetPath, batchSize, maxLen, vectorDim)
    main(traindataSetPath, testdataSetPath, realtestdataSetPath, weightPath, resultPath, batchSize, maxLen, vectorDim, layers, dropout)
    #testrealdata(realtestdataSetPath, weightPath, batchSize, maxLen, vectorDim, layers, dropout)
