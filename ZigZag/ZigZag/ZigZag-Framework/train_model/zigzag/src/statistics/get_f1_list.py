import os.path

from src.model import generator_eva_model
from src.statistics.statistics_tool import gen_f1
from tensorflow.keras.models import load_model

os.environ["CUDA_VISIBLE_DEVICES"] = "2"

if __name__ == '__main__':
    fromData = "/data1/yjy/dataset/zigzag/input-step-15/test/"
    model_path = "/data1/yjy/dataset/zigzag/model/static_f1/model-3.1.h5"
    metricsName = "model-3.21.csv"
    metricsFile = "/data1/yjy/dataset/zigzag/model/static_f1/" + metricsName
    model = load_model(model_path)
    model_metrics, c2_model = generator_eva_model(model)
    f1_log = '/data1/yjy/dataset/zigzag/statistics_success/f1_log.csv'
    toData = '/data1/yjy/dataset/zigzag/statistics_success/success_200_15/statistics_find/'
    f1_list = gen_f1(metricsFile, toData, model_metrics)
