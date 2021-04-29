#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class Tabu_list:
    """ 禁忌表类 """

    def tabu_list_creation(self):
        """创建禁忌表"""
        self.tabu_list = dict()

    def insert_movement(self, plane, gate1, gate2, i):
        """更新禁忌表：没有该方案则添加并存入禁忌值，有该方案则存入禁忌值，不到禁忌值不能出去"""
        self.tabu_list[(plane, gate1, gate2)] = i + self.duration

    def del_movement(self, plane, gate1, gate2):
        """
        在其他函数确认禁忌表中 “某航班的停机位交换方案” 在禁忌表中待的迭代次数超过了禁忌长度时，
        本函数即可将此 “某航班的停机位交换方案” 从禁忌表中剔除"""
        del self.tabu_list[(plane, gate1, gate2)]

    def is_tabu(self, plane, gate1, gate2, i):
        """
        本函数用于判断 “某航班的停机位更改方案” 是否还在禁忌中，即：
        1. 是否还在禁忌表中； 2. 如果在禁忌表中，其在禁忌表中待的迭代次数是否超过了禁忌长度；
        若在禁忌表中，且未超过禁忌长度，则返回True；若在禁忌表中，但已超过禁忌长度，或根本不在禁忌表中，则返回False"""
        if (plane, gate1, gate2) in self.tabu_list.keys() and i <= self.tabu_list[(plane, gate1, gate2)]:    # 依然在禁忌范围内
            return True
        else:
            if (plane, gate1, gate2) in self.tabu_list.keys() and i > self.tabu_list[(plane, gate1, gate2)]:    # 已经不在禁忌范围内
                self.del_movement(plane, gate1, gate2)
            return False

    def tabu_cleaning(self, i):
        tabu_to_clean = [movements for movements in self.tabu_list.keys()]
        for movements in tabu_to_clean:
            if i > self.tabu_list[movements]:
                self.del_movement(movements[0], movements[1], movements[2])


    def __init__(self, d):
        """__init__函数在创建该类的时候，将会默认执行该函数内的语句"""
        self.tabu_list_creation()    # 由于__init__函数会在该类创建的时候被执行，则这条调用函数的语句也会在创建该类的时候自动执行
        self.duration = d
