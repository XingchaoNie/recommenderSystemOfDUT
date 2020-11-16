# 关联推荐算法的实现
import numpy as np
import pandas as pd


def allSubsets(s):      # 关联推荐算法-递归算法求集合所有子集（含空集）
    if len(s) == 0:
        return [[]]
    return allSubsets(s[1:]) + [[s[0]] + r for r in allSubsets(s[1:])]


def demo_show(grade):
    # 随机数生成的数据集输入对关联推荐算法的输出有巨大影响
    for item in grade:
        print(item)
    return


def show(grade):
    print('*' * 5 + "关联推荐算法展示前四位用户推荐结果前两甲及评分" + '*' * 5)
    for i in range(len(grade)):
        if i < 4:
            print('*'*5 + "第{:d}位用户".format(i + 1) + '*'*5)
            for j in range(len(grade[i])):
                if j < 2:
                    print("电影编号:{:d}".format(int(grade[i][j][0])))
                    print("推荐评分:{:.4f}".format(grade[i][j][1]))
    return


def main():
    io = r'E:\Python_space\大创项目2.1\basicAlgorithm\basicData\RR_data.xlsx'
    rr_data = pd.read_excel(io, sheet_name=0, header=None)
    rr_data = np.array(rr_data)
    [r, c] = np.shape(rr_data)-np.array([1, 1])
    link = []
    progress = (np.array(range(20))+1).tolist()
    progress = [str(i) for i in progress]
    progress = allSubsets(progress)
    for i in range(r):
        pro = list(set(rr_data[i+1, 1].split('\\')))
        link.append(allSubsets(pro))
    i = 0  # 控制while循环
    grade = []
    while len(progress[i]) <= len(rr_data[1, 1].split('\\')):       # 关联推荐算法-生成关联规则
        if len(progress[i]) != 0:
            lv = 0
            for j in range(r):
                if set(progress[i]) in [set(i) for i in link[j]]:
                    lv = lv+1
            lv = lv/r
            progress[i].insert(0, lv)
            if lv >= 0.1:
                grade.append(progress[i])
        i = i + 1
    grade.sort(key=lambda x: x[0], reverse=True)
    max_grade = grade[0]
    for i in range(len(grade)):                     # 关联推荐算法-选取最优关联规则
        if grade[i][0] == max_grade[0] or len(grade[i])>len(max_grade):
            max_grade = grade[i]
    print(max_grade)
    end_grade = []
    grade_progress = []
    for i in range(len(grade)):
        grade_progress.append(set(grade[i][1:]).copy())
    max_grade_progress = allSubsets(max_grade[1:])
    for item in max_grade_progress:
        if len(item) == 1:
            lv = grade[grade_progress.index(set(item))][0]
            for items in max_grade_progress:
                if item[0] in items and item != items:
                    end_lv = grade[grade_progress.index(set(items))][0]/lv
                    end_grade.append([item, items, end_lv].copy())
    end_grade.sort(key=lambda x: x[2], reverse=True)
    # 根据关联规则进行推荐
    fin_grade = []
    for i in range(r):
        fin_grade.append([])
        for item in max_grade[1:]:
            if item in rr_data[i+1, 1].split('\\'):
                sig = 0
                for j in range(len(end_grade)):
                    if end_grade[j][0][0] == item and sig == 0:
                        sig = 1
                        for items in end_grade[j][1]:
                            if items != item and items not in fin_grade[i] and items not in rr_data[i+1, 1].split('\\'):
                                fin_grade[i].append(items)
    demo_show(fin_grade)


if __name__ == '__main__':
    main()
