import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from scipy import stats

import seaborn as sns
import statsmodels.stats.weightstats as st

plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

'''
路径和文件名中不要用中文，不然会报错
encoding用于指定文件的编码，因为读取的csv中有中文，所以指定文件编码为中文编码“GBK”
'''
list_zigzag = [0.71429, 0.69492, 0.69173, 0.81538, 0.68852, 0.77037, 0.77027, 0.75188, 0.7218,
               0.71212, 0.72581, 0.75188, 0.67826, 0.7027, 0.64122, 0.80916, 0.72857, 0.76563, 0.76923, 0.78431]
list_checkmarks = [0.41096, 0.48, 0.28169, 0.32, 0.11765, 0.37838, 0.33333, 0.24615, 0.08219, 0.37037, 0.15789,
                   0.18182, 0.36842, 0.33333, 0.28125, 0.26471, 0.41026, 0.36842, 0.46753, 0.32786]

if __name__ == '__main__':
    dataSer_z = pd.Series(list_zigzag)
    dataSer_s = pd.Series(list_checkmarks)
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
    第2组数据：checkmarks
    '''
    # 第二组数据均值
    checkmarks_mean = dataSer_s.mean()
    # 第二组数据标准差
    checkmarks_std = dataSer_s.std()

    print('zigzag_std样本大小20，样本标准差=', zigzag_std)
    print('checkmarks_std样本大小20，样本标准差=', checkmarks_std)

    # 查看数据集分布
    sns.distplot(dataSer_z)
    plt.title('zigzag dataset')
    plt.show()

    sns.distplot(dataSer_s)
    plt.title('checkmarks dataset')
    plt.show()

    # 导入统计模块
    '''
    Scipy的双独立样本t检验不能返回自由度，对于后面计算置信区间不方便。所以我们使用另一个统计包（statsmodels）

    需要先在navigator中安装统计包（statsmodels），
    如果还不知道如何安装包，可以看第1关的教程：https://www.zhihu.com/question/58033789/answer/254673663

    双独立（independent）样本t检验（ttest_ind）
    statsmodels.stats.weightstats.ttest_ind
    官网使用文档http://www.statsmodels.org/dev/generated/statsmodels.stats.weightstats.ttest_ind.html
    '''

    '''
    ttest_ind：独立双样本t检验，
    usevar='unequal'两个总体方差不一样
    返回的第1个值t是假设检验计算出的（t值），
    第2个p_two是双尾检验的p值
    第3个df是独立双样本的自由度
    '''
    t, p_two, df = st.ttest_ind(dataSer_z, dataSer_s,
                                usevar='unequal')

    # 自由度一般只保留整数部分
    print('t=', t, 'p_two=', p_two, ',df=', df)

    # 单尾检验的p 值
    p_oneTail = p_two / 2
    print('单尾检验的p值=', p_oneTail)

    # 判断标准（显著水平）使用alpha=5%
    alpha = 0.05

    '''
    在课程中《章节33：独立双样本检验第4步：做出结论》有误，修正为下面最新的代码和对应文档《课程错误更正.doc》：
    双尾判断条件：
    p_two（双尾检验的p值） < 判断标准（显著水平）alpha 时，
    拒绝零假设，有统计显著，也就是有显著差异
    '''
    # 做出结论
    if t > 0 and p_oneTail < alpha:
        print('拒绝零假设，有统计显著，也就是接受备选假设')
        print('备选假设：A版本和B版本有差异')
    else:
        print('接受零假设，没有统计显著')
        print('零假设：A版本和B版本没有差异')

    '''
    效应量：差异指标Cohen's d
    这里的标准差，因为是双独立样本，需要用合并标准差（pooled standard deviations）代替
    '''
    zigzag_n = len(list_zigzag)
    checkmarks_n = len(list_checkmarks)

    # 合并标准差
    sp = np.sqrt(((zigzag_n - 1) * np.square(zigzag_std) + (checkmarks_n - 1) * np.square(zigzag_std)) / (
                zigzag_n + checkmarks_n - 2))
    # 效应量Cohen's d
    d = (zigzag_mean - checkmarks_mean) / sp

    print('d=', d)
