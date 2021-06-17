#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" 存放了一些辅助函数和评价函数 """

interval_value_max, conflict_max = 1, 1
interval_value_min = 0


def maximum(_interval_value_max, _conflict_max):
    global interval_value_max, conflict_max
    interval_value_max = _interval_value_max
    conflict_max = _conflict_max


def flights_assigned(gate, flights):
    """
    该函数返回一个参数FlightsOnGate，是指在同一个停机位上，随时间推移，停放的航班列表"""
    flights_on_gate = []
    for i in range(len(flights)):  # 航班数量，让 i 遍历
        if flights[i].gate == gate:  # 只要某个航班的停机位编号（就是传进来的gate）与某些航班的停机位编号相同
            flights_on_gate.append(flights[i])  # 就把这些航班的Flight对象存进FlightsOnGate中，就是说找到哪些航班的停机位重复了
    return flights_on_gate


def position_flight_gate(flight_i, gate_j, flights):
    """
    该函数用于找到，从函数flights_assigned中得到的 “在同一个停机位上停放的航班列表” 中的，
    与gate_j相对应的航班flight_i在 “在同一个停机位上停放的航班列表” 中的坐标index"""
    FlightsOnGate_j = flights_assigned(gate_j, flights)
    index = 0
    for k in range(len(FlightsOnGate_j)):
        if FlightsOnGate_j[k] == flight_i:
            index = k
    return index


def contribution(flight_i, flights, L0):
    """随着flight_i的遍历，该函数用于获得每个航班到港时刻，与L0，或与前一个航班的离港时刻的差的平方"""
    front_delta = 0
    first_delta = 0
    gate_j = flight_i.gate  # 航班 i 此时匹配的停机位
    # print(gate_j)
    FlightsOnGate = flights_assigned(gate_j, flights)
    index = position_flight_gate(flight_i, gate_j, flights)  # 这个下标是FlightsOnGate列表里对上flight_i的下标，和i没有关系。另外，直接传FlightsOnGate就不用再算一次了吧？？？改一下试试看有什么问题
    # print(index)
    if index == 0:  # index==0 表示flight_i是在FlightsOnGate列表里的第0个，说明是最先到该停机位的那个航班，前面还没有航班停靠过
        front_delta = (flight_i.arrival_time - L0) ** 2
        first_delta = front_delta

    flight_avant_i = FlightsOnGate[index - 1]
    # print(flight_avant_i.number)
    # print(flight_avant_i.departure_time)
    if flight_avant_i.departure_time + 8 <= flight_i.arrival_time:  # 看上一个停在这个停机位上的航班走没走，这个地方应在左侧加一个停机位安全间隙
        front_delta = (flight_i.arrival_time - flight_avant_i.departure_time - 8) ** 2  # 这个公式也应该再减去一个停机位安全间隙
    return front_delta, first_delta


def contribution_fin_gate(gate_i, flights, LNP1):
    """随着gate_i的遍历，该函数用于获得了每个停机位，最后一个航班的离开时间与LNP1的差的平方"""
    delta = 0
    FlightsOnGate = flights_assigned(gate_i, flights)  # 获取都想停到gate_i这个停机位的航班的一个列表
    if len(FlightsOnGate) != 0:
        last_flight = FlightsOnGate[len(FlightsOnGate) - 1]  # 获取上述列表的最后一架航班（这获取的是一个Flight类的对象）
        # print(last_flight.number)
        delta = (LNP1 - last_flight.departure_time) ** 2
        return delta
    elif len(FlightsOnGate) == 0:
        delta = 0
        return delta


def contribution_total(flights, n_gates, L0, LNP1):
    """这是评价函数之一：用于计算所有航班，在每个停机位上的，空闲时间间隔，的平方，的和"""
    b = 0
    c = 0
    d = 0
    for i in range(len(flights)):  # 有几个航班，就有几个i
        front_delta, first_delta = contribution(flights[i], flights, L0)
        b = b + first_delta
        c = c + front_delta
        # c = c + contribution(flights[i], flights, L0)
    for gate in range(n_gates):
        d = d + contribution_fin_gate(gate, flights, LNP1)
    interval = (c + d) / interval_value_max
    global interval_value_min
    interval_value_min = b + d
    # return c + d
    return interval


def conflit(flight_i, flight_j):
    """该函数用于判定每次传入的两个航班是否存在时间上的冲突"""
    c = 1
    # 但凡有一个航班的离港时间，比另一个航班的到港时间提前，那就让：c = 0，说明没冲突；否则：c = 1，说明有冲突
    # 有问题！！！这里也没有加入安全事件间隙，需要改进
    if flight_i.departure_time + 8 <= flight_j.arrival_time:
        c = 0
    # if flight_j.departure_time + 8 <= flight_i.arrival_time:  # 因为 j > i，所以此项不可能出现，故注释
    #     c = 0
    return c


def conflit_same_gate(flight_i, flight_j):
    """该函数用于判定每次传进来的两个航班：是否相同、是否抢占同一停机位，
    若都是，则通过函数 conflit 来判定它们是否存在冲突"""
    d = 0
    # c = conflit(flight_i, flight_j)
    # if flight_i != flight_j:
    #     if flight_i.gate == flight_j.gate:
    #         c = conflit(flight_i, flight_j)    # 将此句放在这里应该可以缩短程序运行时间
    #         d = c
    if flight_i.gate == flight_j.gate:
        c = conflit(flight_i, flight_j)
        d = c
    return d


def conflit_total(flights):
    """
    该函数为评价函数之二，用于计算 “整个机场中，同一停机位下的不同航班产生的冲突次数”，
    并且在d中加入了一个kc的权重，以尽量接近c的量纲"""
    a = 0
    # kc = 1500  # kc应该是加在 “冲突次数” 上的权重，这里设为1500可能是为了尽量获得与 “整个机场中，同一停机位下航班之间的时间间隔” 相同的量纲
    for i in range(len(flights)):
        for j in range(len(flights)):
            if j > i:
                a = a + conflit_same_gate(flights[i], flights[j])
            # a = a + conflit_same_gate(flights[i], flights[j])  # 每出现 1 个冲突，a 就会加 1，最终的 a 可以看出出现了几次冲突
    # 上述的两个循环有两个问题：1. 航班可能相同，即：i == j，但这个在conflit_same_gate已解决；
    #                         2. 当j小于i时，会出现与之前组合重复的情况，所以下面返回的a除以了一个2，这里可以进行修改，进而缩短程序运行时间
    # return kc * (a / 2)
    return a / conflict_max


def fonction_objectif(flights, n_gates, L0, LNP1):
    """
    该函数用于计算评价函数，这里包含了c、d两个评价函数，
    c得到的评价函数是 “整个机场中，同一停机位下航班之间的时间间隔”，
    d得到的评价函数是 “整个机场中，同一停机位下的不同航班产生的冲突次数”，
    该函数最终返回评价函数总值、冲突次数 """
    # kc = 1500  # kc应该是加在 “冲突次数” 上的权重，这里设为1500可能是为了尽量获得与 “整个机场中，同一停机位下航班之间的时间间隔” 相同的量纲
    w1, w2 = 0.45, 0.55
    b = contribution_total(flights, n_gates, L0, LNP1)
    c = ((b * interval_value_max) - interval_value_min) / (interval_value_max - interval_value_min)
    d = conflit_total(flights)
    res = ((w1 * c) + (w2 * d)) * 10000
    # return res, d / kc
    return res, int(d * conflict_max)


def fonction_objectif_return_value(flights, n_gates, L0, LNP1):
    """
    该函数用于分别返回评价函数各部分的值，两部分是c、d两个评价函数，
    c得到的评价函数是 “整个机场中，同一停机位下航班之间的时间间隔”，
    d得到的评价函数是 “整个机场中，同一停机位下的不同航班产生的冲突次数”，
    该函数最终返回 “时间间隔总值” 、“冲突次数” """
    # kc = 1500  # kc应该是加在 “冲突次数” 上的权重，这里设为1500可能是为了尽量获得与 “整个机场中，同一停机位下航班之间的时间间隔” 相同的量纲
    c = contribution_total(flights, n_gates, L0, LNP1)
    d = conflit_total(flights)
    # return res, d / kc
    return c, int(d * conflict_max)


def find_flights_conflit(flight_i, gate_j, flights):
    vecteur_flights_conflit = []
    FlightsOnGate = flights_assigned(gate_j, flights)
    for i in range(len(FlightsOnGate)):
        if conflit(flight_i, FlightsOnGate[i]) == 1:
            if flight_i != FlightsOnGate[i]:
                vecteur_flights_conflit.append(FlightsOnGate[i])
    return vecteur_flights_conflit


def partie_debut(flight_i, gate_j, flights):
    delta = 0
    flights_conflit = find_flights_conflit(flight_i, gate_j, flights)
    if len(flights_conflit) != 0:
        first_flight_conflit = flights_conflit[0]
        if flight_i.arrival_time < first_flight_conflit.arrival_time:
            delta = (first_flight_conflit.arrival_time - flight_i.arrival_time)
    return delta


def partie_fin(flight_i, gate_j, flights):
    delta = 0
    flights_conflit = find_flights_conflit(flight_i, gate_j, flights)
    if len(flights_conflit) != 0:
        last_flight_conflit = flights_conflit[len(flights_conflit) - 1]
        if flight_i.departure_time > last_flight_conflit.departure_time:
            delta = (flight_i.departure_time - last_flight_conflit.departure_time)
    return delta


def partie_milieu(flight_i, gate_j, flights):
    delta = 0
    flights_conflit = find_flights_conflit(flight_i, gate_j, flights)
    if len(flights_conflit) != 0:
        for i in range(len(flights_conflit) - 1):
            if conflit(flights_conflit[i], flights_conflit[i + 1]) == 0:
                gamma = flights_conflit[i + 1].arrival_time - flights_conflit[i].departure_time
                delta = delta + gamma ** 2
    return delta
