# 基础CB推荐算法的实现
import numpy as np
import pandas as pd


def show(grade):                        # 通用推荐结果输出函数
    print('*' * 5 + "基础CB推荐算法展示前四位用户推荐结果前两甲及评分" + '*' * 5)
    for i in range(len(grade)):
        if i < 4:
            print('*'*5 + "第{:d}位用户".format(i + 1) + '*'*5)
            for j in range(len(grade[i])):
                if j < 2:
                    print("电影编号:{:d}".format(int(grade[i][j][0])))
                    print("推荐评分:{:.4f}".format(grade[i][j][1]))
    return


def main():
    io = r'E:\Python_space\大创项目2.1\basicAlgorithm\basicData\CB_data.xlsx'
    mv_data = pd.read_excel(io, sheet_name=0, header=None)
    user_data = pd.read_excel(io, sheet_name=1, header=None)
    mv_data = np.array(mv_data)
    [r_1, c_1] = np.shape(mv_data) - np.array([1, 1])
    user_data = np.array(user_data)
    [r_2, c_2] = np.shape(user_data) - np.array([1, 1])
    personal = []
    # 构建用户画像
    for i in range(r_2):        # 基础CB推荐-构建用户画像
        personal.append([[], [], [], [], []])          # 画像维度索引值 0:导演  1:演员  2:电影类型  3:制片地区  4:上映时间编号
        for k in range(c_1):
            progress = dict()
            for j in range(c_2):
                pro = mv_data[user_data[i + 1, j + 1], k + 1]
                if k == 1:
                    pro = pro.split('\\')
                    for x in pro:
                        if x in progress:
                            progress[x] = progress[x] + 1
                        else:
                            progress[x] = 1
                else:
                    if pro in progress:
                        progress[pro] = progress[pro]+1
                    else:
                        progress[pro] = 1
            for key in progress.keys():
                if progress[key] > 1:
                    personal[i][k].append(key)
            if not personal[i][k]:
                personal[i][k].append(0)
    # 用户画像构建完毕
    # 基础CB算法-根据算法公式打分
    grade = list()
    for i in range(r_2):
        grade.append([])
        for p in range(r_1):
            if p+1 not in user_data[i+1, 1:]:
                pro_grade = 0
                for q in range(c_1):
                    pro = mv_data[p+1, q+1]
                    if q == 1:
                        pro = pro.split('\\')
                        lv = 0
                        for x in pro:
                            if x in personal[i][q]:
                                lv = lv+1
                        # 基础CB推荐算法
                        lv = 2*lv/(len(pro)+len(personal[i][1]))
                        pro_grade = pro_grade+lv*0.2
                    else:
                        if pro in personal[i][q]:
                            pro_grade = pro_grade+0.2
                grade[i].append([p + 1, pro_grade].copy())
        grade[i].sort(key=lambda y: y[1], reverse=True)
    show(grade)


if __name__ == '__main__':
    main()


