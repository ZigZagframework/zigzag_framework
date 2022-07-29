import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from scipy import stats

import seaborn as sns

# plt.rcParams['font.sans-serif'] = ['SimHei']  #
# plt.rcParams['axes.unicode_minus'] = False  #

'''

encodincs“GBK”
'''
list_zigzag = [81.4, 79.5, 79.2, 91.5, 79.9, 87.0, 87.0, 85.2, 82.2, 81.2,
               82.6, 85.2, 77.8, 80.3, 74.1, 90.9, 82.9, 86.6, 87.9, 88.4]
list_sys = [41.1, 48, 28.2, 32, 11.8, 37.8, 33.3, 24.6, 8.2, 37.0,
            15.8, 18.2, 36.8, 33.3, 28.1, 26.5, 41, 36.8, 46.8, 32.8]
# list_zigzag = [0.814, 0.795, 0.792, 0.915, 0.799, 0.870, 0.870, 0.852, 0.822, 0.812, 0.826, 0.852, 0.778, 0.803, 0.741, 0.909, 0.829,
#                0.866, 0.879, 0.884]
# list_sys = [0.296, 0.254, 0.318, 0.357, 0.416, 0.333, 0.330, 0.349, 0.262, 0.366, 0.30, 0.190, 0.32, 0.410, 0.293, 0.378, 0.233, 0.317,
#             0.427, 0.264]
if __name__ == '__main__':
    dataSer_z = pd.Series(list_zigzag)
    dataSer_s = pd.Series(list_sys)
    dataSer_z.describe()
    dataSer_s.describe()
    '''
    第一组数据：zigzag
    '''
    # 第一组数据均值
    zigzag_mean = dataSer_z.mean()
    # 第一组数据标准差
    zigzag_std = dataSer_z.std()

    '''
    第2组数据：sys
    '''
    # 第二组数据均值
    sys_mean = dataSer_s.mean()
    # 第二组数据标准差
    sys_std = dataSer_s.std()

    # 导入统计模块

    """
        ttest_rel ： 相关配对检验
        返回的t 是假设检验中计算的t值
        返回的p 是双尾检验的p值（p_twoTail）
    """
    t, p_twoTail = stats.ttest_rel(dataSer_z, dataSer_s)  # 内部计算是差值数据集的t 值和p 值
    print('t值=', t, '双尾检验的p值=', p_twoTail)

    # 单尾检验的p 值
    p_oneTail = p_twoTail / 2
    print('单尾检验的p值=', p_oneTail)

    # 显著水平使用alpha=5%
    alpha = 0.05

    # 决策
    if t > 0 and p_oneTail < alpha:
        print('拒绝零假设，有统计显著')
        print('也就是接受备选假设：zigzag模型存在提升作用')
    else:
        print('接受备选假设，没有统计显著，也就是zigzag模型不存在提升作用')

        # data.plot(kind='bar', ax=ax)

    '''
    效应量：差异指标Cohen's d
    '''
    # 差值数据集对应的总体平均值是0
    list_zigzag.sort()
    list_sys.sort()
    c = [list_zigzag[i] - list_sys[i] for i in range(0, len(list_zigzag))]
    print(c)
    dataSer_c = pd.Series(c)
    # 查看数据集分布
    sns.distplot(dataSer_c)
    plt.title('Difference data set distribution')
    plt.show()
    '''
    效应量：差异指标Cohen's d
    '''
    # 差值数据集对应的总体平均值0.71-0.31
    pop_mean = 0.37
    # 差值数据集的标准差
    sample_std = dataSer_c.std()
    sample_mean = dataSer_c.mean()
    d = (sample_mean - pop_mean) / sample_std

    print('d=', d)