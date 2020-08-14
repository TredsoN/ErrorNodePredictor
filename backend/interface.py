'''
***********************
给前端提供的接口
***********************
'''

import csv
import joblib

from sklearn import tree
from backend.utils import read_file
from backend.feature import step1_get_decision_tree_features, step2_get_increase_var_per_minute, step3_get_statistical_data
from backend.procedure import step1, step2, step3

clf = joblib.load('backend/model/decision_tree.model')

## 寻找根因节点
def get_node(path):
    # 读取文件
    file = read_file(path)

    # 第一步
    feature1 = step1_get_decision_tree_features(file)
    if step1(clf, feature1) == False:
        return -1

    # 第二步
    feature2 = step2_get_increase_var_per_minute(file)
    suspect = step2(feature2)
    
    #第三步
    feature3 = step3_get_statistical_data([file],[[set(suspect)]])
    return step3(feature3)

## 获取根因节点详细信息
def get_information(path, num):
    # 读取CSV文件，然后判断节点号是否等于num，如果等于则停止，并且返回告警信息
    with open(path, 'r', encoding="utf-8") as f:
        reader = csv.reader(f)
        firstline = 1
        for row in reader:
            if firstline == 1:
                firstline = 0
                continue
            x = row[3].split(" ")[0].split("_")[1]
            if int(x) == num:
                return row[3]