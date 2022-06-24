import os.path

import numpy as np
import pickle

from model.bgru_generator_model import generator_eva_model
from model.evaluation_model import evaluation_with_predict, evaluation_stat
from preprocess.load_data import concat_x_and_y
from preprocess.statistics_tool import gen_f1
from tools import utils
from tools.utils import get_all_files
from tensorflow.keras.models import load_model
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

os.environ["CUDA_VISIBLE_DEVICES"] = "2"

if __name__ == '__main__':
    fromData = "./dataset/zigzag/input-step-15/test/"
    model_path = "./dataset/zigzag/model/static_f1/model-3.1.h5"
    metricsName = "model-3.21.csv"
    metricsFile = "./dataset/zigzag/model/static_f1/" + metricsName
    model = load_model(model_path)
    model_metrics, c2_model = generator_eva_model(model)
    f1_log = './dataset/zigzag/statistics_success/f1_log.csv'
    toData = './dataset/zigzag/statistics_success/success_200_15/statistics_find/'
    f1_list = gen_f1(metricsFile, toData, model_metrics)
