'''
***********************
预测的三个主要步骤
***********************
'''

import backend.topology as tp

from backend.feature import *

## 步骤一：判断是否有根因，有则返回true，无则返回false
def step1(clf, feature1):
  r = clf.predict([feature1])
  if r[0] == '1':
    return True
  return False

## 步骤二：确定根因范围，返回包含根因的list
def step2(feature2):
  data_analysis = []
  node_vec = [0]*30
  max6 = step1_get_max(6, data_analysis, feature2)  # 取得最大的前6个结点
  node_list = [-1] * 4
  naming_list = []
  list4null = []
  suspected = []

  for i in range(6):
    naming_list.append(step1_step_in(int(max6[i]), 0, node_list, list4null))
    list4null = []

  top_2 = step1_get_top2(naming_list, node_vec)

  for i in range(len(top_2)):
    suspected.append(top_2[i]-1)
  
  for i in range(30):
    for jj in range(len(top_2)):
      if tp.Combined_Graph[top_2[jj]-1][i] == 1:
        suspected.append(i)

  return list(set(suspected))

## 步骤三：确定根因，返回根因id
def step3(feature3):
  Row = []
  i = feature3

  avrg_top2 = step3_get_top2(i, 3)

  if i[avrg_top2[0]][2]-i[avrg_top2[1]][2] > 0.26:
    Row.append([i[avrg_top2[0]][-1], i[avrg_top2[0]][1], i[avrg_top2[0]][-3], "R"])
    return Row[0][0]

  if i[avrg_top2[1]][2]-i[avrg_top2[0]][2] > 0.26:
    Row.append([i[avrg_top2[1]][-1], i[avrg_top2[1]][1], i[avrg_top2[1]][-3], "R"])
    return Row[0][0]

  attention = -1
  for x in i:
    if x[-2] == 1:
      attention = x[0]
      break

  if attention != -1 and tp.Combined_Graph[i[avrg_top2[0]][0]][attention] == 1:
    Row.append([x[-1], x[1], x[-3], "T2"])
    return Row[0][0]
  else:
    for k in i:
      if k[2] < 0.45:
        i.remove(k)
    k = step3_get_top2(i, 3)
    Row.append([i[k[0]][-1], i[k[0]][1], i[k[0]][-3], "T", "无"])

  return Row[0][0]