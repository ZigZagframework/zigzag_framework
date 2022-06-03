import os


def mkdir(path):
    """
        如果无文件夹则创建文件夹
    """
    folder = os.path.exists(path)
    if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs(path)  # makedirs 创建文件时如果路径不存在会创建这个路径
        print(path + "文件夹已创建成功")


