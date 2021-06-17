#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" 用于绘制初始解与最终解的甘特图 """

import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import numpy as np
import seaborn
import functionm as fm

# ax = plt.gca()
# [ax.spines[i].set_visible(False) for i in ["top", "right"]]    # 将图做成二维坐标系的样子

flights_initsol = list()


def initial_solution_gantt_parameter(_flights_initsol):
    global flights_initsol
    flights_initsol = _flights_initsol


def initial_final_draw_gantt(num_gates, flights, L0, LNP1):
    """
    绘制甘特图：
        以每个停机位作为标的，在禁忌搜索算法结束后，得到每个停机位下将会停放的航班列表；
        如果列表为空则说明此停机位没有飞机需要停放，故无需绘制在甘特图中；如果列表不空，
        则说明此停机位有飞机需要停放，则将它们分别绘制在甘特图中。每个航班的颜色与它们
        在列表中的顺序决定，即所有停机位的第 0 个停放的航班均为一个颜色，所有停机位的
        第 1 个停放的航班均为一个颜色，以此类推..."""
    plt.figure(num=1, figsize=(14, 8))
    ax1 = plt.gca()
    [ax1.spines[i].set_visible(False) for i in ["top", "right"]]  # 将图做成二维坐标系的样子
    barh_height = 0.7  # 甘特图内，“航班条” 的高度，考虑到 y 轴停机位为间隔为 1 的整数，故取此值
    text_yoffset = 0.15  # 写在 “航班条” 内的 “航班号” 距离 “航班条” 顶部的距离
    # color_list = ['powderblue', 'lightgreen', 'beige', 'peachpuff', 'thistle', 'gainsboro']
    color_list = [seaborn.xkcd_rgb['manilla'], seaborn.xkcd_rgb['yellowy green'], seaborn.xkcd_rgb['light blue'],
                  seaborn.xkcd_rgb['light lavender'], seaborn.xkcd_rgb['blush pink'], seaborn.xkcd_rgb['sunflower'],
                  seaborn.xkcd_rgb['light khaki'], seaborn.xkcd_rgb['hospital green'], seaborn.xkcd_rgb['light cyan'],
                  seaborn.xkcd_rgb['light rose'], seaborn.xkcd_rgb['light peach'], seaborn.xkcd_rgb['sandy'],
                  'beige', 'gainsboro']
    for gate in range(num_gates):
        flights_on_gate = fm.flights_assigned(gate, flights_initsol)
        if flights_on_gate:  # 若循环得到的停机位gate，里面有航班停放
            for flight in flights_on_gate:  # 遍历某个停机位里需要停放的航班号
                flight_index = flights_on_gate.index(flight)
                plt.barh(y=gate,  # y坐标，对应该航班停在哪个停机位
                         width=flight.departure_time - flight.arrival_time,  # 宽度，对应该航班的停放时长
                         left=flight.arrival_time,  # 起始 x 坐标，对应该航班的到港时间
                         height=barh_height,  # 高度，使甘特图协调
                         color=color_list[flight_index],  # 填充颜色，用于区分
                         # edgecolor='darkgrey'  # 边框颜色，均为浅黑灰色
                         )
                plt.text(x=flight.arrival_time,
                         y=gate - text_yoffset,
                         s=flight.number,
                         color="dimgrey",
                         size=8  # 写入航班标号
                         )
                # if flight_index == 0:
                #     plt.barh(y=gate,    # y坐标，对应该航班停在哪个停机位
                #              width=flight.departure_time - flight.arrival_time,    # 宽度，对应该航班的停放时长
                #              left=flight.arrival_time,    # 起始 x 坐标，对应该航班的到港时间
                #              height=height,    # 高度，使甘特图协调
                #              color='powderblue')    # 颜色，用于区分
                #     plt.text(flight.arrival_time, gate, flight.number, color="dimgrey", size=8)    # 为航班标号
                # elif flight_index == 1:
                #     plt.barh(y=gate,
                #              width=flight.departure_time - flight.arrival_time,
                #              left=flight.arrival_time,
                #              height=height,
                #              color='lightgreen')
                #     plt.text(flight.arrival_time, gate, flight.number, color="dimgrey", size=8)
                # elif flight_index == 2:
                #     plt.barh(y=gate,
                #              width=flight.departure_time - flight.arrival_time,
                #              left=flight.arrival_time,
                #              height=height,
                #              color='beige')
                #     plt.text(flight.arrival_time, gate, flight.number, color="dimgrey", size=8)
                # elif flight_index == 3:
                #     plt.barh(y=gate,
                #              width=flight.departure_time - flight.arrival_time,
                #              left=flight.arrival_time,
                #              height=height,
                #              color='peachpuff')
                #     plt.text(flight.arrival_time, gate, flight.number, color="dimgrey", size=8)
                # elif flight_index == 4:
                #     plt.barh(y=gate,
                #              width=flight.departure_time - flight.arrival_time,
                #              left=flight.arrival_time,
                #              height=height,
                #              color='thistle')
                #     plt.text(flight.arrival_time, gate, flight.number, color="dimgrey", size=8)
                # elif flight_index > 4:
                #     plt.barh(y=gate,
                #              width=flight.departure_time - flight.arrival_time,
                #              left=flight.arrival_time,
                #              height=height,
                #              color='gainsboro')
                #     plt.text(flight.arrival_time, gate, flight.number, color="dimgrey", size=8)

    conversion = [x for x in range(L0, LNP1 + 1, 12)]  # 更改前的横坐标列表（此时横坐标是由 “时” 换算成的数值）
    hour = list()  # 更改后的横坐标列表
    for i in range(len(conversion)):
        hour.append(str(int(conversion[i] / 12)) + ':00')  # 将横坐标的数值转换回 “时”，如：96 --> 8:00
    plt.xticks(conversion, hour)  # 将横坐标的数值转换回 “时”，如：96 --> 8:00
    plt.yticks(np.arange(num_gates), np.arange(num_gates))  # 纵坐标显示所有停机位的编号

    # 设置横纵坐标的名称以及对应字体格式
    font_xylabel = {'family': 'Times New Roman',
                    'style': 'italic',  # 设置横纵坐标文本为斜体
                    'weight': 'normal',
                    'size': 13,
                    }
    font_set = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=12)
    plt.xlabel(xlabel='time', fontdict=font_xylabel)
    plt.ylabel(ylabel='gates', fontdict=font_xylabel)
    plt.title(label='停机位分配初始解', fontproperties=font_set)

    plt.get_current_fig_manager().window.state('zoomed')
    plt.savefig("./test/picture/停机位分配初始解.png")

    plt.figure(num=2, figsize=(14, 8))
    ax2 = plt.gca()
    [ax2.spines[i].set_visible(False) for i in ["top", "right"]]  # 将图做成二维坐标系的样子
    barh_height = 0.7  # 甘特图内，“航班条” 的高度，考虑到 y 轴停机位为间隔为 1 的整数，故取此值
    text_yoffset = 0.15  # 写在 “航班条” 内的 “航班号” 距离 “航班条” 顶部的距离
    # color_list = ['powderblue', 'lightgreen', 'beige', 'peachpuff', 'thistle', 'gainsboro']
    color_list = [seaborn.xkcd_rgb['manilla'], seaborn.xkcd_rgb['yellowy green'], seaborn.xkcd_rgb['light blue'],
                  seaborn.xkcd_rgb['light lavender'], seaborn.xkcd_rgb['blush pink'], seaborn.xkcd_rgb['sunflower'],
                  seaborn.xkcd_rgb['light khaki'], seaborn.xkcd_rgb['hospital green'], seaborn.xkcd_rgb['light cyan'],
                  seaborn.xkcd_rgb['light rose'], seaborn.xkcd_rgb['light peach'], seaborn.xkcd_rgb['sandy'],
                  'beige', 'gainsboro']
    for gate in range(num_gates):
        flights_on_gate = fm.flights_assigned(gate, flights)
        if flights_on_gate:  # 若循环得到的停机位gate，里面有航班停放
            for flight in flights_on_gate:  # 遍历某个停机位里需要停放的航班号
                flight_index = flights_on_gate.index(flight)
                plt.barh(y=gate,  # y坐标，对应该航班停在哪个停机位
                         width=flight.departure_time - flight.arrival_time,  # 宽度，对应该航班的停放时长
                         left=flight.arrival_time,  # 起始 x 坐标，对应该航班的到港时间
                         height=barh_height,  # 高度，使甘特图协调
                         color=color_list[flight_index],  # 填充颜色，用于区分
                         # edgecolor='darkgrey'  # 边框颜色，均为浅黑灰色
                         )
                plt.text(x=flight.arrival_time,
                         y=gate - text_yoffset,
                         s=flight.number,
                         color="dimgrey",
                         size=8  # 写入航班标号
                         )
                # if flight_index == 0:
                #     plt.barh(y=gate,    # y坐标，对应该航班停在哪个停机位
                #              width=flight.departure_time - flight.arrival_time,    # 宽度，对应该航班的停放时长
                #              left=flight.arrival_time,    # 起始 x 坐标，对应该航班的到港时间
                #              height=height,    # 高度，使甘特图协调
                #              color='powderblue')    # 颜色，用于区分
                #     plt.text(flight.arrival_time, gate, flight.number, color="dimgrey", size=8)    # 为航班标号
                # elif flight_index == 1:
                #     plt.barh(y=gate,
                #              width=flight.departure_time - flight.arrival_time,
                #              left=flight.arrival_time,
                #              height=height,
                #              color='lightgreen')
                #     plt.text(flight.arrival_time, gate, flight.number, color="dimgrey", size=8)
                # elif flight_index == 2:
                #     plt.barh(y=gate,
                #              width=flight.departure_time - flight.arrival_time,
                #              left=flight.arrival_time,
                #              height=height,
                #              color='beige')
                #     plt.text(flight.arrival_time, gate, flight.number, color="dimgrey", size=8)
                # elif flight_index == 3:
                #     plt.barh(y=gate,
                #              width=flight.departure_time - flight.arrival_time,
                #              left=flight.arrival_time,
                #              height=height,
                #              color='peachpuff')
                #     plt.text(flight.arrival_time, gate, flight.number, color="dimgrey", size=8)
                # elif flight_index == 4:
                #     plt.barh(y=gate,
                #              width=flight.departure_time - flight.arrival_time,
                #              left=flight.arrival_time,
                #              height=height,
                #              color='thistle')
                #     plt.text(flight.arrival_time, gate, flight.number, color="dimgrey", size=8)
                # elif flight_index > 4:
                #     plt.barh(y=gate,
                #              width=flight.departure_time - flight.arrival_time,
                #              left=flight.arrival_time,
                #              height=height,
                #              color='gainsboro')
                #     plt.text(flight.arrival_time, gate, flight.number, color="dimgrey", size=8)

    conversion = [x for x in range(L0, LNP1 + 1, 12)]  # 更改前的横坐标列表（此时横坐标是由 “时” 换算成的数值）
    hour = list()  # 更改后的横坐标列表
    for i in range(len(conversion)):
        hour.append(str(int(conversion[i] / 12)) + ':00')  # 将横坐标的数值转换回 “时”，如：96 --> 8:00
    plt.xticks(conversion, hour)  # 将横坐标的数值转换回 “时”，如：96 --> 8:00
    plt.yticks(np.arange(num_gates), np.arange(num_gates))  # 纵坐标显示所有停机位的编号

    # 设置横纵坐标的名称以及对应字体格式
    font_xylabel = {'family': 'Times New Roman',
                    'style': 'italic',  # 设置横纵坐标文本为斜体
                    'weight': 'normal',
                    'size': 13,
                    }
    font_set = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=12)
    plt.xlabel(xlabel='time', fontdict=font_xylabel)
    plt.ylabel(ylabel='gates', fontdict=font_xylabel)
    plt.title(label='停机位分配最终解', fontproperties=font_set)

    plt.get_current_fig_manager().window.state('zoomed')
    plt.savefig("./test/picture/停机位分配最终解.png")
    plt.show()  # 出图



def single_draw_gantt(num_gates, flights, L0, LNP1, is_final):
    """
    绘制甘特图：
        以每个停机位作为标的，在禁忌搜索算法结束后，得到每个停机位下将会停放的航班列表；
        如果列表为空则说明此停机位没有飞机需要停放，故无需绘制在甘特图中；如果列表不空，
        则说明此停机位有飞机需要停放，则将它们分别绘制在甘特图中。每个航班的颜色与它们
        在列表中的顺序决定，即所有停机位的第 0 个停放的航班均为一个颜色，所有停机位的
        第 1 个停放的航班均为一个颜色，以此类推..."""
    ax = plt.gca()
    [ax.spines[i].set_visible(False) for i in ["top", "right"]]  # 将图做成二维坐标系的样子
    barh_height = 0.7  # 甘特图内，“航班条” 的高度，考虑到 y 轴停机位为间隔为 1 的整数，故取此值
    text_yoffset = 0.15  # 写在 “航班条” 内的 “航班号” 距离 “航班条” 顶部的距离
    # color_list = ['powderblue', 'lightgreen', 'beige', 'peachpuff', 'thistle', 'gainsboro']
    color_list = [seaborn.xkcd_rgb['manilla'], seaborn.xkcd_rgb['yellowy green'], seaborn.xkcd_rgb['light blue'],
                  seaborn.xkcd_rgb['light lavender'], seaborn.xkcd_rgb['blush pink'], seaborn.xkcd_rgb['sunflower'],
                  seaborn.xkcd_rgb['light khaki'], seaborn.xkcd_rgb['hospital green'], seaborn.xkcd_rgb['light cyan'],
                  seaborn.xkcd_rgb['light rose'], seaborn.xkcd_rgb['light peach'], seaborn.xkcd_rgb['sandy'],
                  'beige', 'gainsboro']
    for gate in range(num_gates):
        flights_on_gate = fm.flights_assigned(gate, flights)
        if flights_on_gate:  # 若循环得到的停机位gate，里面有航班停放
            for flight in flights_on_gate:  # 遍历某个停机位里需要停放的航班号
                flight_index = flights_on_gate.index(flight)
                plt.barh(y=gate,  # y坐标，对应该航班停在哪个停机位
                         width=flight.departure_time - flight.arrival_time,  # 宽度，对应该航班的停放时长
                         left=flight.arrival_time,  # 起始 x 坐标，对应该航班的到港时间
                         height=barh_height,  # 高度，使甘特图协调
                         color=color_list[flight_index],  # 填充颜色，用于区分
                         # edgecolor='darkgrey'  # 边框颜色，均为浅黑灰色
                         )
                plt.text(x=flight.arrival_time,
                         y=gate - text_yoffset,
                         s=flight.number,
                         color="dimgrey",
                         size=8  # 写入航班标号
                         )
                # if flight_index == 0:
                #     plt.barh(y=gate,    # y坐标，对应该航班停在哪个停机位
                #              width=flight.departure_time - flight.arrival_time,    # 宽度，对应该航班的停放时长
                #              left=flight.arrival_time,    # 起始 x 坐标，对应该航班的到港时间
                #              height=height,    # 高度，使甘特图协调
                #              color='powderblue')    # 颜色，用于区分
                #     plt.text(flight.arrival_time, gate, flight.number, color="dimgrey", size=8)    # 为航班标号
                # elif flight_index == 1:
                #     plt.barh(y=gate,
                #              width=flight.departure_time - flight.arrival_time,
                #              left=flight.arrival_time,
                #              height=height,
                #              color='lightgreen')
                #     plt.text(flight.arrival_time, gate, flight.number, color="dimgrey", size=8)
                # elif flight_index == 2:
                #     plt.barh(y=gate,
                #              width=flight.departure_time - flight.arrival_time,
                #              left=flight.arrival_time,
                #              height=height,
                #              color='beige')
                #     plt.text(flight.arrival_time, gate, flight.number, color="dimgrey", size=8)
                # elif flight_index == 3:
                #     plt.barh(y=gate,
                #              width=flight.departure_time - flight.arrival_time,
                #              left=flight.arrival_time,
                #              height=height,
                #              color='peachpuff')
                #     plt.text(flight.arrival_time, gate, flight.number, color="dimgrey", size=8)
                # elif flight_index == 4:
                #     plt.barh(y=gate,
                #              width=flight.departure_time - flight.arrival_time,
                #              left=flight.arrival_time,
                #              height=height,
                #              color='thistle')
                #     plt.text(flight.arrival_time, gate, flight.number, color="dimgrey", size=8)
                # elif flight_index > 4:
                #     plt.barh(y=gate,
                #              width=flight.departure_time - flight.arrival_time,
                #              left=flight.arrival_time,
                #              height=height,
                #              color='gainsboro')
                #     plt.text(flight.arrival_time, gate, flight.number, color="dimgrey", size=8)

    conversion = [x for x in range(L0, LNP1 + 1, 12)]  # 更改前的横坐标列表（此时横坐标是由 “时” 换算成的数值）
    hour = list()  # 更改后的横坐标列表
    for i in range(len(conversion)):
        hour.append(str(int(conversion[i] / 12)) + ':00')  # 将横坐标的数值转换回 “时”，如：96 --> 8:00
    plt.xticks(conversion, hour)  # 将横坐标的数值转换回 “时”，如：96 --> 8:00
    plt.yticks(np.arange(num_gates), np.arange(num_gates))  # 纵坐标显示所有停机位的编号

    # 设置横纵坐标的名称以及对应字体格式
    font_xylabel = {'family': 'Times New Roman',
                    'style': 'italic',  # 设置横纵坐标文本为斜体
                    'weight': 'normal',
                    'size': 13,
                    }
    font_set = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=12)
    plt.xlabel(xlabel='time', fontdict=font_xylabel)
    plt.ylabel(ylabel='gates', fontdict=font_xylabel)
    if is_final:
        plt.title(label='停机位分配最终解', fontproperties=font_set)
    elif not is_final:
        plt.title(label='停机位分配初始解', fontproperties=font_set)

    plt.show()  # 出图
