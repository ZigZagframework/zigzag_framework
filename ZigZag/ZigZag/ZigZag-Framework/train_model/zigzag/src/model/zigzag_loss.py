# -*- coding: utf-8 -*-
#
from tensorflow.keras import losses
from tensorflow.keras import backend as K


def min_f(c_pred):
    def loss_abs(y_true, y_pred):
        return K.mean(K.abs(y_pred - c_pred))

    return loss_abs


def max_f1(c_pred, x1_pred, x2_pred):
    def max_fea(y_true, y_pred):
        return losses.binary_crossentropy(y_true, y_pred) + losses.binary_crossentropy(y_true, c_pred) - K.mean(
            K.abs(x1_pred - x2_pred))

    return max_fea


def max_f2(c1_pred, c2_pred, y2_pred):
    def max_fea(y_true, y1_pred):
        return losses.binary_crossentropy(y_true, c1_pred) + losses.binary_crossentropy(y_true, c2_pred) - K.mean(
            K.abs(y1_pred - y2_pred))

    return max_fea


def binary_c(c_pred):
    def binary_cross(y_true, y_pred):
        return losses.binary_crossentropy(y_true, y_pred) + losses.binary_crossentropy(y_true, c_pred)

    return binary_cross


def max_discrepancy(c_pred, x1_pred, x2_pred):
    """
         Prediction of original samples
         Prediction of countermeasure samples
    """

    def binary_cross(y_true, y_pred):
        return losses.binary_crossentropy(y_true, y_pred) + losses.binary_crossentropy(y_true, c_pred) - K.mean(
            K.abs(x1_pred - x2_pred))

    return binary_cross
