import pandas as pd
import os
import numpy as np
import xml.etree.ElementTree as ET

def GetExtraX(data,xml):
    # 解析XML文件
    print(xml)
    tree = ET.parse(xml)
    root = tree.getroot()
    
    for newX in root.findall('newX'):
        name = newX.find('name').text  # 获取新列的名称
        operands = []  # 用于存储操作数的列表

        # 获取操作数
        for operand_tag in newX:
            if operand_tag.tag != 'name' and operand_tag.tag != 'Formula':
                operands.append(data[operand_tag.text])

        formula = newX.find('Formula').text  # 获取计算公式

        # 构建动态的计算字典
        eval_dict = {f'operand{i}': operand for i, operand in enumerate(operands, 1)}

        # 计算新列的值
        result = eval(formula, eval_dict)
        data[name] = result
        
    return data