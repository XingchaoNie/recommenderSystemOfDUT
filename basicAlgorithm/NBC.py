# 朴素贝叶斯推荐算法的实现
import pandas as pd
import numpy as np


def show(grade):
    print('*' * 5 + "朴素贝叶斯推荐算法展示前四位用户推荐结果前两甲及评分" + '*' * 5)
    for i in range(len(grade)):
        if i < 4:
            print('*'*5 + "第{:d}位用户".format(i + 1) + '*'*5)
            for j in range(len(grade[i])):
                if j < 2:
                    print("电影编号:{:d}".format(int(grade[i][j][0])))
                    print("推荐评分:{:.4f}".format(grade[i][j][1]))
    return


def main():
    # 用户行为日志导入（模拟为用户-物品-评分矩阵，0表示用户尚未评分）（数据为随机生成）
    io = r'E:\Python_space\大创项目2.1\basicAlgorithm\basicData\user_data.xlsx'
    user_data = pd.read_excel(io, sheet_name=0, header=None)
    user_data = np.array(user_data)
    [r, c] = np.shape(user_data)-np.array([1, 1])
    grade = []
    for i in range(r):              # 朴素贝叶斯-列表嵌套形式逐个遍历用户信息进行打分
        grade.append([])
        for j in range(c):
            if user_data[i+1, j+1] == 0:
                progress = []
                for k in range(5):
                    progress.append([])
                    for p in range(r):
                        if user_data[p+1, j+1] == k+1:
                            progress[k].append(user_data[p+1, 1:])
                link = list()
                for k in range(5):
                    _pro_ = np.array(progress[k])
                    if not progress[k]:
                        link.append(0)
                    else:
                        _pro_ = np.array(progress[k])
                        lv = 1
                        for p in range(c):
                            if p != j:
                                lv = lv*(np.sum(_pro_[:, p] == user_data[i + 1, p + 1]) / np.shape(_pro_)[0])
                        link.append(lv)
                grade[i].append([j + 1, link.index(max(link)) + 1])
        grade[i].sort(key=lambda x: x[1], reverse=True)
    show(grade)


if __name__ == '__main__':
    main()
