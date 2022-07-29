# -*- coding: utf-8 -*-
#
# datetime:2022/3/6 20:42

"""
description：bgru model
"""

from tensorflow.keras.layers import Input
from tensorflow.keras.layers import Masking, Dense, Dropout
from tensorflow.keras.layers import GRU
from tensorflow.keras.layers import Bidirectional
from tensorflow.keras.models import Model
from tensorflow.keras import optimizers

from src.model.zigzag_loss import *


def generator_eva_model(model_last):
    """
          generate  trainmodel 
          eval 
      """
    print('loading eva model')
    model_eva = model_last
    print("building model ...")
    inputs = model_eva.get_layer('inputs').output
    classifier1 = model_eva.get_layer('classifier1').output
    classifier2 = model_eva.get_layer('classifier2').output
    c1 = Model(inputs=inputs, outputs=classifier1)
    c2 = Model(inputs=inputs, outputs=classifier2)
    return c1, c2


def generator_print_mid(model_last):
    """
          generate  trainmodel 
          eval 
         laye
      """
    print('loading eva model')
    model_eva = model_last
    print("building model ...")
    inputs = model_eva.get_layer('inputs').output
    classifier1 = model_eva.get_layer('classifier1').output
    classifier2 = model_eva.get_layer('classifier2').output
    c1 = Model(inputs=inputs, outputs=classifier1)
    c2 = Model(inputs=inputs, outputs=classifier2)
    merge_pred = model_eva.get_layer('merge_pred').output
    # 1 originX
    merge_data = Model(inputs=inputs, outputs=merge_pred)
    return c1, c2, merge_data


class GeneratorModel(object):
    def __init__(self, max_len, vector_dim, dropout, pred_threshold, model_path, learning_rate):
        self.max_len = max_len
        self.vector_dim = vector_dim
        self.dropout = dropout
        self.pred_threshold = pred_threshold
        self.model_path = model_path
        self.learning_rate = learning_rate
        self.class_layer = ['classifier1', 'classifier2', 'classifier2_c', 'classifier1_c', 'c1_layer', 'c2_layer',
                            'c1_layer_c', 'c2_layer_c', 'c1_dense', 'c2_dense', 'c1_dense_c', 'c2_dense_c']

    def generator_model_3_1(self):
        """
             origin  sample X
            generate  
        """
        inputs = Input(shape=(self.max_len, self.vector_dim), name='inputs')
        mask_1 = Masking(mask_value=0.0, name='mask_1')(inputs)
        bgru_1 = Bidirectional(
            GRU(units=256, activation='tanh',
                recurrent_activation='hard_sigmoid', return_sequences=True),
            name='bgru_1')(mask_1)
        dropout_1 = Dropout(self.dropout, name='dropout_1')(bgru_1)
        bgru_2 = Bidirectional(
            GRU(units=256, activation='tanh', recurrent_activation='hard_sigmoid'), name='bgru_2')(
            dropout_1)
        dropout_2 = Dropout(self.dropout, name='f_out')(bgru_2)
        # classifier layer
        c1_layer = Dense(512, activation='relu', name='c1_layer')(dropout_2)
        c2_layer = Dense(512, activation='relu', name='c2_layer')(dropout_2)
        # c1_norm = BatchNormalization()(c1_layer)
        # c2_norm = BatchNormalization()(c2_layer)
        # c1_dense = Dense(512, activation='relu', name='c1_dense')(c1_norm)
        # c2_dense = Dense(512, activation='relu', name='c2_dense')(c2_norm)

        classifier1 = Dense(1, activation='sigmoid',
                            name='classifier1')(c1_layer)
        classifier2 = Dense(1, activation='sigmoid',
                            name='classifier2')(c2_layer)
        model_3_1 = Model(inputs=inputs, outputs=[classifier1, classifier2])
        losses_c1_c2 = {'classifier1': 'binary_crossentropy',
                        'classifier2': 'binary_crossentropy'}
        adam_o = optimizers.Adam(lr=self.learning_rate[0], decay=0.005)
        model_3_1.compile(loss=losses_c1_c2, optimizer=adam_o,
                          metrics=['binary_accuracy'])
        model_3_1.summary()
        return model_3_1

    def generator_model_3_2_1(self, model_last):
        print('loading 3.21 model')
        model_3_1 = model_last
        print("building model 3.2_1 ...")
        inputs = model_3_1.get_layer('inputs').output
        classifier1 = model_3_1.get_layer('classifier1').output
        classifier2 = model_3_1.get_layer('classifier2').output
        model_3_1 = Model(inputs=inputs, outputs=[classifier1, classifier2])

        losses_c1_c2 = {'classifier1': 'binary_crossentropy',
                        'classifier2': 'binary_crossentropy'}
        adam_o = optimizers.Adam(lr=self.learning_rate[1], decay=0.005)
        model_3_1.compile(loss=losses_c1_c2, optimizer=adam_o,
                          metrics=['binary_accuracy'])
        model_3_1.summary()
        return model_3_1

    def generator_model_3_2_2(self, model_last, model_last2):
        """
           sampl originsample,hard
        """
        print('loading 3.21 model')
        model_3_1 = model_last
        model_3_1_copy = model_last2
        for layer in model_3_1_copy.layers:
            layer_name = layer.name
            layer_rename = layer.name + "_c"
            model_3_1_copy.get_layer(layer_name)._name = layer_rename

        print("building model 3.2...")
        inputs1 = model_3_1.get_layer('inputs').output  # inputs
        classifier1 = model_3_1.get_layer('classifier1').output
        classifier2 = model_3_1.get_layer('classifier2').output

        inputs2 = model_3_1_copy.get_layer('inputs_c').output

        classifier_x1 = model_3_1_copy.get_layer('classifier1_c').output
        classifier_x2 = model_3_1_copy.get_layer('classifier2_c').output
        # 1.load X'
        model_3_2 = Model(inputs=[inputs1, inputs2], outputs=[
            classifier1, classifier2, classifier_x1, classifier_x2])

        losses_c1_c2 = {'classifier1': max_f1(classifier2, classifier_x1, classifier_x2),
                        'classifier2': max_f1(classifier1, classifier_x1, classifier_x2),
                        'classifier1_c': max_f2(classifier1, classifier2, classifier_x2),
                        'classifier2_c': max_f2(classifier1, classifier2, classifier_x2)
                        }
        # lock
        for layer in model_3_2.layers:
            if layer.name not in self.class_layer:
                layer.trainable = False
            else:
                layer.trainable = True
            print(layer.name + '--------' + str(layer.trainable))

        adam_o = optimizers.Adam(lr=self.learning_rate[2], decay=0.005)
        model_3_2.compile(loss=losses_c1_c2, optimizer=adam_o,
                          metrics=['binary_accuracy'])
        model_3_2.summary()
        return model_3_2

    def generator_model_3_3(self, model_last):
        print('loading 3.22 model')
        model_3_3 = model_last
        print("building model 3.3...")
        inputs = model_3_3.get_layer('inputs').output
        classifier1 = model_3_3.get_layer('classifier1').output
        classifier2 = model_3_3.get_layer('classifier2').output
        model_3_3 = Model(inputs=inputs, outputs=[classifier1, classifier2])
        # Frozen layer
        for layer in model_3_3.layers:
            if layer.name in self.class_layer:
                layer.trainable = False
            else:
                layer.trainable = True
            print(layer.name + '--------' + str(layer.trainable))
        losses_c1_c2 = {'classifier1': min_f(classifier2),
                        'classifier2': min_f(classifier1)}
        adam_o = optimizers.Adam(lr=self.learning_rate[3], decay=0.005)
        model_3_3.compile(loss=losses_c1_c2, optimizer=adam_o)
        model_3_3.summary()
        return model_3_3
