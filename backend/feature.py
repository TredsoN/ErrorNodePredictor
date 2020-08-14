'''
***********************
与特征提取相关的所有函数
***********************
'''

import re
import numpy as np
import networkx as nx
import backend.topology as tp

from collections import Counter
from backend.utils import read_file
from datetime import datetime, timedelta

## (第一步)获取节点错误总数
def step1_get_increase_average_per_minute(file):
    node_vec = [0] * 30
    reader = file
    
    for row in reader:
        node_tag = row[3].split(' ')[0].split('_')[1]
        for node_tag2 in range(30):
            if int(node_tag) in tp.Combined_Node[node_tag2]:
                com_node = node_tag2
                break
        node_vec[com_node] += 1
    
    return node_vec

## (第一步)找到告警数最大的前6个节点
def step1_get_max(target, data_analysis, increase_var_per_minute):
    first_row = 0
    result_row = []
    result_node = []
    res = []

    for i in range(len(increase_var_per_minute)):
        node_tag = i
        temp = float(increase_var_per_minute[i])
        data_analysis.append(increase_var_per_minute[i])
        if first_row == 0:
            first_row = -1
            result_row.append(temp)
            result_node.append(node_tag)
            continue
        for ii in range(len(result_row)):
            if temp > result_row[ii]:
                result_row.insert(ii, temp)
                result_node.insert(ii, node_tag)
                break
            else:
                if ii == (len(result_row) - 1):
                    result_row.append(temp)
                    result_node.append(node_tag)
                    break
    for i in range(target):
        res.append(result_node[i])

    return res

## (第一步)往下探寻连接节点
def step1_step_in(node_tag, deep, node_list, res_list):
    # nodeTag是当前的节点
    # deep是当前递归的深度，递归3层就退出
    # nodeList 是传入一条点名线路
    # resList 是返回的参数
    temp_list = [-1] * 4
    for i in range(4):
        temp_list[i] = node_list[i]
    temp_list[deep] = node_tag
    if deep == 3:
        for i in range(4):
            temp_list[i] += 1
        row = [node_list[0] + 1, temp_list]
        if row not in res_list:
            res_list.append(row)
        return res_list
    for i in range(30):
        if tp.Combined_Graph[node_tag][i] == 1:
            res_list = step1_step_in(i, deep + 1, temp_list, res_list)
    return res_list

## (第一步)找到最大两个数及其对应节点
def step1_get_top2(namingList, nodeVector):
    res = []
    # nodeVector = [0] * 30
    for i in range(len(namingList)):
        for x in range(len(namingList[i])):
            for node in namingList[i][x][1]:
                nodeVector[int(node) - 1] += 1
    step1_cutdown(namingList, nodeVector)
    nodeVector = [0] * 30
    for i in range(len(namingList)):
        for x in range(len(namingList[i])):
            for node in namingList[i][x][1]:
                nodeVector[int(node) - 1] += 1

    for i in range(len(namingList)):
        node = int(namingList[i][0][0]) - 1
        if len(namingList[i]) > 1:
            node_List1 = namingList[i][0][1]
            node_List2 = namingList[i][1][1]
            if nodeVector[int(node_List1[1]) - 1] == nodeVector[int(node_List2[1]) - 1]:
                nodeVector[int(node_List1[0]) - 1] -= 1

    top1 = 0
    for i in range(len(nodeVector)):
        if nodeVector[top1] < nodeVector[i]:
            top1 = i
    res.append(top1 + 1)

    top = nodeVector[top1]
    nodeVector[top1] = 0
    top2 = 0
    top2s = []
    for i in range(len(nodeVector)):
        if nodeVector[top2] < nodeVector[i]:
            top2 = i
    for i in range(len(nodeVector)):
        if nodeVector[top2] == nodeVector[i]:
            top2s.append(i)

    for second in top2s:
        if tp.Combined_Graph[top1][second] == 1:
            res.append(second + 1)
        if tp.Combined_Graph[second][top1] == 1:
            res.append(second + 1)
    if len(res) == 1:
        res.append(top2 + 1)


    return res

## (第一步)剪枝
def step1_cutdown(namingList, nodeVector):
    for i in range(len(namingList)):
        node = int(namingList[i][0][0]) - 1
        if np.sum(tp.Combined_Graph[node]) > 1:
            node_List1 = namingList[i][0][1]
            node_List2 = namingList[i][1][1]
            if nodeVector[int(node_List1[1]) - 1] < nodeVector[int(node_List2[1]) - 1]:
                namingList[i].pop(0)
            if nodeVector[int(node_List1[1]) - 1] > nodeVector[int(node_List2[1]) - 1]:
                namingList[i].pop(1)

## (第一步)获取基于点名次数剪枝的点名方差
def step1_get_naming_var(IncreaseVarPerMinute):
    data_analysis = []
    node_vec = [0] * 30
    max6 = step1_get_max(6, data_analysis, IncreaseVarPerMinute)  # 取得最大的前6个结点
    node_list = [-1] * 4
    naming_list = []
    list4null = []

    for i in range(6):
        naming_list.append(step1_step_in(int(max6[i]), 0, node_list, list4null))
        list4null = []

    top_2 = step1_get_top2(naming_list, node_vec)

    return np.var(node_vec)

## 提取第一步用到的特征
def step1_get_decision_tree_features(file):
    result = []
    reader = file
    error_node_list = []
    root_node = 0

    # 提取错误节点
    for row in reader:
        node = int(row[3].split('_')[1].split(' ')[0])
        error_node_list.append(int(node))

    error_node_list = np.array(error_node_list)

    # 将错误节点转化为合并节点
    for i in range(0,len(error_node_list)):
        for j in range(0,len(tp.node_orinode_relation)):
            if error_node_list[i] in tp.node_orinode_relation[j]:
                error_node_list[i] = j+1
                break

    # 将合并节点转化为系统
    for i in range(0,len(error_node_list)):
        for j in range(0,len(tp.sys_node_relation)):
            if error_node_list[i] in tp.sys_node_relation[j]:
                error_node_list[i] = j+1
                break

    # 特征1：统计错误次数
    data = np.array(Counter(error_node_list).most_common())[:,1]
    result.append(np.std(data))

    # 统计错误最多的前三个系统
    top3 = np.array(Counter(error_node_list).most_common(3))[:,0]

    # 创建合并后节点的图
    G = nx.DiGraph()
    G.add_edges_from(tp.sys_edges)

    # 特征2：计算最小距离平均值
    shortest1 = min(nx.shortest_path_length(G,top3[0],top3[1]),nx.shortest_path_length(G,top3[1],top3[0]))
    shortest2 = min(nx.shortest_path_length(G,top3[1],top3[2]),nx.shortest_path_length(G,top3[2],top3[1]))
    shortest3 = min(nx.shortest_path_length(G,top3[0],top3[2]),nx.shortest_path_length(G,top3[2],top3[0]))
    result.append((shortest1+shortest2+shortest3)/3)
    
    # 特征3：计算点名方差
    features_node = step1_get_increase_average_per_minute(file)
    result.append(step1_get_naming_var(features_node))

    return result

## 提取第二步中用到的特征
def step2_get_increase_var_per_minute(file):
    reader = file
    # 循环统计每个合并后节点的告警总数
    features_node = []

    for node_tag2 in range(30):
        n_time = []
        n_time_int = []

        for row in reader:
            node_time = row[2]
            node_time = datetime.strptime(node_time, "%Y-%m-%d %H:%M:%S")
            node_tag = row[3].split(' ')[0].split('_')[1]
            if int(node_tag) not in tp.Combined_Node[node_tag2]:
                continue
            n_time.append(node_time)

        if len(n_time) == 0:
            features_node.append(0)
            continue

        for i in range(len(n_time)-1, -1, -1):
            n_time[i] -= n_time[0]
            n_time_int.append(n_time[i].total_seconds())

        error_split = [0]*(1 + int(n_time_int[0]/60))
        
        for i in range(len(n_time)):
            error_split[int(n_time_int[i]/60)] += 1

        features_node.append(np.sum(error_split))

    return features_node

## (第三步)第三步中找到最大的前两项
def step3_get_top2(row_temp, condition):
    the_max = row_temp[0][condition]
    index = 0
    res = []
    for i in range(len(row_temp)):
        if row_temp[i][condition] > the_max:
            the_max = row_temp[i][condition]
            index = i
    res.append(index)
    the_max = 0
    index2 = 0
    for i in range(len(row_temp)):
        if i == index:
            continue
        if row_temp[i][condition] > the_max:
            the_max = row_temp[i][condition]
            index2 = i
    res.append(index2)
    return res

## 提取第三步用到的特征
def step3_get_statistical_data(file, suspect):
    contained = [":80", "端口80", "端口80"]
    files = []

    for file_tag in range(len(file)):
        area = []
        sus = suspect[0]
        for comNode in sus[0]:  # 从可疑节点中选择合并后节点，大大减小循环次数
            combined_node = []
            reader = file[file_tag]
            first_row = 0
            for row in reader:
                if first_row == 0:
                    first_row = 1
                    continue
                node_tag = row[3].split(' ')[0].split('_')[1]
                node_tag = int(node_tag)
                if node_tag not in tp.Combined_Node[comNode]:
                    continue
                row[0] = node_tag
                combined_node.append(row)
            area.append(combined_node)
        files.append(area)

    res = []
    for file_tag in range(len(file)):
        for comArea in files[file_tag]:
            if len(comArea) == 0:
                continue
            node_type = []
            for i in range(len(comArea)):
                if comArea[i][0] not in node_type:
                    node_type.append(comArea[i][0])

            # 统计各个节点的告警数量
            error_sum = [0]*len(node_type)
            error80 = [0]*len(node_type)
            for i in range(len(comArea)):
                for j in range(len(node_type)):
                    if comArea[i][0] == node_type[j]:
                        error_sum[j] += 1
                        if error80[j] != 1:
                            for pat in contained:
                                m = re.search(pat, comArea[i][3])
                                if m is not None:
                                    error80[j] = 1

            # 找到告警数量最大的节点
            max_error = 0
            for X in range(len(error_sum)):
                if error_sum[X] > error_sum[max_error]:
                    max_error = X
            max_error_node = node_type[max_error]
            total = np.sum(error_sum)
            rate = error_sum[max_error]/total
            avrg = np.average(error_sum)
            for comNode in sus[0]:
                if max_error_node in tp.Combined_Node[comNode]:
                    break
            row_tempt = [comNode, -1, rate, avrg, -1, file_tag, error80[max_error], max_error_node]
            res.append(row_tempt)

    return res