'''
***********************
工具函数
***********************
'''

import csv

## 读取csv文件
def read_file(path):
  rows = []

  with open(path, 'r', encoding="UTF-8") as file:
    reader = csv.reader(file)
    next(reader)
    for row in reader:
      rows.append(row)
    
  return rows