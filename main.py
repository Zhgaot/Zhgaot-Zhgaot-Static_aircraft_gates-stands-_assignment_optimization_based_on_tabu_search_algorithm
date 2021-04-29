#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''Original Author: Mathilde GARRIGUES, Abderrafie MOUNADIM, Rime RAISSOUNI;
The author of the optimized content: Zhang Gaotian'''

import time
import data
import tabu
import winsound

""" 1-写入需要分配的 “航班及停机位文件”，并写入对应的航班数量、停机位数量 """
filename = "data/GAP30_65.txt"  # 填写文件路径（请勿忘记加上文件扩展名）
n_flights = 65  # 需要分配的航班数量
n_gates = 30  # 可参与分配的停机位数量

""" 2-选择邻域动作启动算法，可选择True(邻域动作基于交换) 或 False(邻域动作不基于交换) """
# SWAP = True
SWAP = False  # 是否基于交换

""" 3-选择最初的解决方案是随机的(True)还是固定的(False) """
# RANDOM = True
RANDOM = False  # 如果初始解决方案是固定的(False)，则需要在 tabu 类中的 initial_solution_fixe 函数下手动输入初始解
max_value_looptime = 120
initsol_looptime = 5

""" 4-设置禁忌长度 """
TABU_LENGTH = 30

""" 5-设置迭代相关系数 """
KMAX = 100  # 最大迭代次数
NUM_REPEAT = 10  # 控制提前退出迭代的当前解重复次数

""" 6-选择是否需要计算运行时间 """
start_time = time.time()
TIME = True

""" 阅读实例的数据 """
flights, compatibilities, L0, LNP1 = data.read_instance(filename)
# flights：航班列表（里面每个元素都是一个 “航班类”，详见模块 “flight”）； compatibilities：每个航班可兼容的停机位
# L0：最早航班的到港时间的前推整点的量化； LNP1：最晚航班的离港时间的后推整点的量化

""" 创建 Tabu 对象 """
tabu_ins = tabu.Tabu(n_flights, n_gates, compatibilities, flights, L0, LNP1)

""" 启动禁忌搜索算法 """
loop_num = 1
for loop_i in range(loop_num):
    print("================================================== 第", loop_i, "次循环 ==================================================")
    tabu_ins.start_search(SWAP, RANDOM, KMAX, TABU_LENGTH, TIME, start_time, NUM_REPEAT, max_value_looptime, initsol_looptime)
duration = 1800  # millisecond
freq = 550  # Hz
winsound.Beep(freq, duration)