import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
# plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
data_list = [0.411, 0.48, 0.282, 0.32, 0.118, 0.378, 0.333, 0.246, 0.08219, 0.37037, 0.15789,
             0.182, 0.36842, 0.33333, 0.28125, 0.26471, 0.41026, 0.36842, 0.46753, 0.32786]


def check_distribution():
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
    print('sample_mean',sample_mean)

    """
        ● 零假设：zigzag模型不满足标准，F1<0.72
        ● 备选假设：zigzag模型满足标准，F1>=0.72
    """

    # 查看数据集分布
    sns.distplot(dataSer)
    plt.title('ZigZag-enabled SySeVR')
    plt.show()

    # 总体平均值
    pop_mean = 0.27

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
    print('样本平均值=', sample_mean, '单位：ppm')
    print('样本标准差=', sample_std, '单位：ppm')
    # 做出结论
    if t > 0 and p_one < alpha:
        # 右尾判断条件
        print(data_list)
        print('拒绝零假设，有统计显著，满足F1>=', pop_mean)
    else:
        print('接受零假设，没有统计显著，不满足F1>=', pop_mean)

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


if __name__ == '__main__':
    check_distribution()
