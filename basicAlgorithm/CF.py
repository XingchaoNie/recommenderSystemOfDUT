# 基于物品的协同过滤推荐算法实现
import pandas as pd
import numpy as np


def readData():         # 通用数据导入函数
    io = r'E:\Python_space\大创项目2.1\basicAlgorithm\basicData\user_data.xlsx'
    user_data = pd.read_excel(io, sheet_name=0, header=None)
    user_data = np.array(user_data)
    return user_data


def show(grade):
    print('*' * 5 + "基于物品的协同过滤推荐算法展示前四位用户推荐结果前两甲及评分" + '*' * 5)
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
    # 基于物品协同过滤-生成物品相似度矩阵(修正后余弦相似度计算)
    v_s = np.zeros([c, c])
    x_i = []
    x_j = []
    x_average = []
    for i in range(c):
        for j in range(c):
            if i <= j:
                v_s[i, j] = 1
            else:
                for k in range(r):
                    if user_data[k+1, i+1] != 0 and user_data[k+1, j+1] != 0:
                        x_i.append(user_data[k+1, i+1])
                        x_j.append(user_data[k+1, j+1])
                        x_average.append(np.sum(user_data[k+1, 1:])/np.sum(user_data[k+1, 1:] != 0))
                x_x_average = np.array(x_average)
                x_x_i = np.array(x_i)-x_x_average
                x_x_j = np.array(x_j)-x_x_average
                v_s[i, j] = np.sum(x_x_i * x_x_j) / ((sum(x_x_i ** 2) ** 0.5) * (sum(x_x_j ** 2) ** 0.5))
                v_s[j, i] = v_s[i, j]
            x_j.clear()
            x_i.clear()
            x_average.clear()
    # 基于物品协同过滤-用户未评分物品的预测评分
    grade = []
    for i in range(r):
        grade.append([])
        for j in range(c):
            if user_data[i+1, j+1] == 0:
                z_sum = 0
                m_sum = 0
                for k in range(c):
                    if user_data[i+1, k+1] != 0:
                        z_sum = z_sum + v_s[j, k] * user_data[i + 1, k + 1]
                        m_sum = m_sum + v_s[j, k]
                p_u_j = z_sum/m_sum
                grade[i].append([j+1, p_u_j])
        grade[i].sort(key=lambda x: x[1], reverse=True)
    show(grade)


if __name__ == '__main__':
    main()
