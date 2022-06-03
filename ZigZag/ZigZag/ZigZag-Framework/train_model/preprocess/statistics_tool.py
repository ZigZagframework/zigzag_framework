import os.path

import numpy as np
import pickle

from model.bgru_generator_model import generator_eva_model
from model.evaluation_model import evaluation_with_predict, evaluation_stat
from preprocess.load_data import concat_x_and_y
from tools import utils
from tools.utils import get_all_files
from tensorflow.keras.models import load_model
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

os.environ["CUDA_VISIBLE_DEVICES"] = "3"


def gen_statistics_data(from_data, to_data, step):
    """
        从所有test数据中随机获取step*20条数据
        Randomly obtain step*20 pieces of data from all test data
    """
    os.makedirs(to_data, exist_ok=True)
    all_file_full_path_list = []
    all_file_name_list = []
    all_file_full_path_list, all_file_name_list = get_all_files(from_data, all_file_full_path_list,
                                                                all_file_name_list)

    dataset, labels = load_file_list(all_file_full_path_list)
    for index in range(20):
        start = index * step
        end = (index + 1) * step
        print(start, end)
        select_dataset = dataset[start:end]
        select_labels = labels[start:end]
        pkl_name = 'set' + str(index)
        os.makedirs(os.path.join(to_data, pkl_name), exist_ok=True)
        utils.data2pkl([select_dataset, select_labels], os.path.join(to_data, pkl_name, 'data.pkl'))


def gen_statistics_data_sep(from_data, to_data, step):
    """
        从所有test数据中随机获取20*step条数据
        Randomly obtain step*20 pieces of data from all test data
    """
    os.makedirs(to_data, exist_ok=True)
    origin_from_data = os.path.join(from_data, 'origin')
    all_file_full_path_list = []
    all_file_name_list = []
    origin_list, all_file_name_list = get_all_files(origin_from_data, all_file_full_path_list,
                                                    all_file_name_list)
    origin_len = len(origin_list)
    tigress_from_data = os.path.join(from_data, 'tigress')
    all_file_full_path_list = []
    all_file_name_list = []
    tigress_list, all_file_name_list = get_all_files(tigress_from_data, all_file_full_path_list,
                                                     all_file_name_list)
    tigress_len = len(tigress_list)
    all_len = origin_len + tigress_len
    origin_step = int(step * origin_len / all_len)
    print('step----', step)
    print('origin_step----', origin_step)
    tigress_step = step - origin_step
    print('tigress_step----', tigress_step)
    origin_dataset, origin_labels = load_file_list(origin_list)
    tigress_dataset, tigress_labels = load_file_list(tigress_list)

    for index in range(20):
        origin_start = index * origin_step
        origin_end = (index + 1) * origin_step
        tigress_start = index * tigress_step
        tigress_end = (index + 1) * tigress_step
        origin_select_dataset = origin_dataset[origin_start:origin_end]
        origin_select_labels = origin_labels[origin_start:origin_end]
        tigress_select_dataset = tigress_dataset[tigress_start:tigress_end]
        tigress_select_labels = tigress_labels[tigress_start:tigress_end]
        pkl_name = 'set' + str(index)
        select_dataset = np.concatenate([origin_select_dataset, tigress_select_dataset], axis=0)
        select_labels = np.hstack([origin_select_labels, tigress_select_labels])
        os.makedirs(os.path.join(to_data, pkl_name), exist_ok=True)
        utils.data2pkl([select_dataset, select_labels], os.path.join(to_data, pkl_name, 'data.pkl'))


def gen_f1(metrics_file, test_data,model_metrics):
    # 生成20组F1
    f_score_list = []
    with open(metrics_file, 'a+') as f_write:
        f_write.write(f"model_name,acc,precision,recall,F1,tn,tp,fp,fn,fpr,fnr\n")
    for index in range(20):
        model_name = 'set' + str(index)
        acc, f_score = evaluation_stat(os.path.join(test_data, model_name), model_metrics, metrics_file, 0.4, model_name)
        f_score_list.append(round(f_score, 5))
    print(f_score_list)
    return f_score_list


def check_distribution(data_list):
    dataSer = pd.Series(data_list)
    # 样本平均值
    sample_mean = dataSer.mean()
    '''
        这里要区别：数据集的标准差，和样本标准差
        数据集的标准差公式除以的是n，样本标准差公式除以的是n-1。
        样本标准差，用途是用样本标准差估计出总体标准差
        pandas计算的标准差，默认除以的是n-1，也就是计算出的是样本标准差
        pandas标准差官网地址：https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.std.html
    '''
    # 样本标准差
    sample_std = dataSer.std()
    print('样本平均值=', sample_mean, '单位：ppm')
    print('样本标准差=', sample_std, '单位：ppm')

    """
        ● 零假设：zigzag模型不满足标准，F1<0.72
        ● 备选假设：zigzag模型满足标准，F1>=0.72
    """

    # 查看数据集分布
    sns.distplot(dataSer)
    plt.title('数据集分布')
    # plt.show()

    # 总体平均值
    pop_mean = 0.71

    '''
        ttest_1samp：单独样本t检验
        返回的第1个值t是假设检验计算出的（t值），
        第2个值p是双尾检验的p值
    '''
    t, p_two = stats.ttest_1samp(dataSer, pop_mean)

    print('t值=', t, '双尾检验的p值=', p_two)
    '''
    因为scipy计算出的是双尾检验的t值和p值，但是我们这里是左尾检验。
    根据对称性，双尾的p值是对应单尾p值的2倍
    '''
    # 单尾检验的p值
    p_one = p_two / 2

    print('单尾检验的p值=', p_one)
    # 判断标准（显著水平）使用alpha=5%
    alpha = 0.1

    '''
    左尾判断条件：t < 0 and  p_one < 判断标准（显著水平）alpha
    右尾判断条件：t > 0 and  p_one < 判断标准（显著水平）alpha
    '''
    # 做出结论
    if t > 0 and p_one < alpha:
        # 右尾判断条件
        print(data_list)
        print('拒绝零假设，有统计显著，满足F1>=', pop_mean)
        flag = True
    else:
        print('接受零假设，没有统计显著，不满足F1>=', pop_mean)
        del_file_command = 'rm -rf ' + toData
        os.system(del_file_command)
        flag = False

    '''
    效应量：差异指标Cohen's d
    '''
    d = (sample_mean - pop_mean) / sample_std
    '''
    效应量：相关度指标R2
    '''
    # 样本大小
    n = 20
    # 自由度
    df = n - 1
    R2 = (t * t) / (t * t + df)
    # 0.2，0.5，0.8分别代表小、中、大效应
    print('d=', d)
    print('R2=', R2)

    return flag, d, R2


def load_file_list(file_path_list):
    """
        read data
    """
    dataset = None
    labels = None
    for file_path in file_path_list:
        with open(file_path, "rb") as f:
            x, y, *_ = pickle.load(f)  # *_代表不用的变量返回值，可以为*drop，后接变量名无所谓。
        dataset, labels = concat_x_and_y(dataset, labels, x, y, file_path)
    np.random.seed(RANDOMSEED)
    np.random.shuffle(dataset)  # x  # 将数据集随机化 shuffle
    np.random.seed(RANDOMSEED)
    np.random.shuffle(labels)  # y
    return dataset, labels


if __name__ == '__main__':
    fromData = "/data1/yjy/dataset/zigzag/input-step-15/test/"
    model_path = "/data1/yjy/dataset/zigzag/model/static_f1/12model-3.21.h5"
    metricsName = "12model-3.21-step-sep.csv"
    metricsFile = "/data1/yjy/dataset/zigzag/model/static_f1/" + metricsName
    model = load_model(model_path)
    c1_model, c2_model = generator_eva_model(model)
    f1_log = '/data1/yjy/dataset/zigzag/statistics_success/f1_log.csv'
    with open(f1_log, 'a+') as fwrite:
        fwrite.write(f"index,step,F1_list,Cohensd,R2\n")
    # 1.找数据，20组，失败就覆盖，成功就break
    for idx in range(1000):
        RANDOMSEED = idx
        for sp in [100, 200, 300]:
            toData = os.path.join("/data1/yjy/dataset/zigzag/", 'statistics_find')
            gen_statistics_data_sep(fromData, toData, sp)
            f1_list = gen_f1(sp, toData)
            flag, d, R2 = check_distribution(f1_list)
            if flag:
                f1_list_f = [str(item) for item in f1_list]
                f1_list_str = ','.join(f1_list_f)
                with open(f1_log, 'a+') as fwrite:
                    fwrite.write(
                        f"{idx},{sp},{f1_list_str},{d:.5f},{R2:.5f}\n")
                print('RANDOMSEED', idx)
                savePlace = os.path.join("/data1/yjy/dataset/zigzag/", 'statistics_success',
                                         'success_' + str(sp) + '_' + str(idx))
                os.makedirs(savePlace, exist_ok=True)
                mv_file_command = 'mv  ' + toData + '  ' + savePlace
                os.system(mv_file_command)
