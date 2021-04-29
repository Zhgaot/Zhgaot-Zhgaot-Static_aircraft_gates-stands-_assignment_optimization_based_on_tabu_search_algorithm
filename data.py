#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import os
import flight

flights = list()
pb_data = dict()    # 创建包含（记录）航班数 N 和停机位数 M 的字典

''' 对file、line的测试（不必在意）：'''
# filename = "data/GAP5_25"
# with open(filename + '.txt', 'r') as file:
# 	all_data = file.read()
# 	print(all_data)
# line = all_data.split("\n")
# print(line)
# temp = line[0].split(" ")
# print(temp)
# pb_data[temp[0]] = temp[1]
# print(pb_data)


def read_instance(filename):
    """ 读取文件中的信息 """

    """ ========== 变量初始化 ========== """
    A = list()
    A_h = list()
    A_m = list()
    D = list()
    D_h = list()
    D_m = list()
    # L0 = 0
    # LNP1 = 0
    P = dict()
    n = 0

    """ ========== 获取文件中的数据 ========== """
    # ====== 阅读数据文件 ======
    with open(filename, 'r') as file:
        all_data = file.read()  # 得到了txt文件中的数据

    """ ========== 数据规范化 ========== """
    line = all_data.split("\n")                # 把 all_data 的每一行都变成字符串，然后存入新生成的列表 line 中；即 line 中的每个元素对应于数据文件的每一行

    for i in range(len(line)):                 # 对 line 的每一项根据索引来进行循环
        if i == 0 or i == 1:                   # 因为 line 列表中的前两项为：'Gates 5', 'Flights 25'
            temp = line[i].split(" ")          # 以空格为标识符，把 line[i] 内的内容分割字符串，然后存入新生成的列表 temp 中
            pb_data[temp[0]] = temp[1]         # 把 temp 列表的内容变成字典，比如：['Gates', '5'] --> {'Gates': '5'}
        else:                                  # 列表 A、D 和字典 P 的构造
            temp = line[i].split(" ")          # 以空格为标识符，把 line[i] 内的内容分割字符串，然后存入新生成的列表 temp 中，比如：['#00:', '08:20', '10:45', '0', '1', '2', '3', '4', '']
            if len(temp) > 1:                  # 比1大，表明是有航班需要停放进停机场的
                A.append(temp[1])              # 将 “到港时间” 存入列表 A 中
                D.append(temp[2])              # 将 “离港时间” 存入列表 D 中
                P[n] = []                      # P是字典，n的初值是0，在字典 P 中加入 “键为n、值为[]” 的元素
                for j in range(3, len(temp) - 1):
                    P[n].append(int(temp[j]))  # 把停机位的编号存到字典P中键n对应的值里，这个值是一个列表
                n = n + 1                      # n服务于字典 P，主要是为了作为字典 P 的一个标杆

    """ ========== 到、离港时间的数值化换算 ========== """
    for i in range(len(A)):
        A_split = str(A[i]).split(":")         # A_split 为一个存放每次到港时和分的中间值，其中的元素是字符形式
        D_split = str(D[i]).split(":")         # D_split 为一个存放每次离港时和分的中间值，其中的元素是字符形式
        A_h.append(A_split[0])                 # A_h存放每次到港的“时”
        A_m.append(A_split[1])                 # A_h存放每次到港的“分”
        D_h.append(D_split[0])                 # D_h存放每次离港的“时”
        D_m.append(D_split[1])                 # D_h存放每次离港的“分”
        A[i] = int(A_h[i]) * 12 + int(int(A_m[i]) / 5)  # 比如，把原本存放的到港时间8:20，量化成了数字100
        D[i] = int(D_h[i]) * 12 + int(int(D_m[i]) / 5)

    # 记录到港时间的最早的 “时” ，以及离港时间的最晚的 “时”
    L0 = int(A_h[0]) * 12
    LNP1 = (int(D_h[len(D) - 1]) + 1) * 12

    """ ========== 航班对象创建 ========== """
    for i in range(int(pb_data["Flights"])):  # pb_data = {'Gates': '5', 'Flights': '25'}，这里取25，即航班数量，有多少个航班就创建多少个航班对象
        flights.append(flight.Flight())
        flights[i].number = i
        flights[i].arrival_time = A[i]
        flights[i].departure_time = D[i]
        flights[i].compatible_gates = P[i]

    return flights, P, L0, LNP1


def display_data(flights):
    print("*** 航班 ***")
    for i in range(len(flights)):
        print("飞机航班 ", flights[i].number,
              " --- 到港时间 = ", flights[i].arrival_time,
              " --- 离港时间 = ", flights[i].departure_time,
              " --- 飞机兼容的停机位 = ", flights[i].compatible_gates,
              " --- 分配给该航班的停机位 = ", flights[i].gate, sep="")


""" 用于测试模块 “data” （不必在意）： """
# flights, P, L0, LNP1 = read_instance(filename)
# display_data(flights)