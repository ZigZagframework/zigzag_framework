import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from scipy import stats

import seaborn as sns

plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

'''
路径和文件名中不要用中文，不然会报错
encoding用于指定文件的编码，因为读取的csv中有中文，所以指定文件编码为中文编码“GBK”
'''
list_zigzag = [0.71429, 0.69492, 0.69173, 0.81538, 0.68852, 0.77037, 0.77027, 0.75188, 0.7218,
               0.71212, 0.72581, 0.75188, 0.67826, 0.7027, 0.64122, 0.80916, 0.72857, 0.76563, 0.76923, 0.78431]
list_sys = [0.41096, 0.48, 0.28169, 0.32, 0.11765, 0.37838, 0.33333, 0.24615, 0.08219, 0.37037, 0.15789,
            0.18182, 0.36842, 0.33333, 0.28125, 0.26471, 0.41026, 0.36842, 0.46753, 0.32786]

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
