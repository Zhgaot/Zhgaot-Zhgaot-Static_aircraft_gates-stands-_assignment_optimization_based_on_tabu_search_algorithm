#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" 邻域动作的实现（封装），通过邻域动作，来生成邻域(候选)解 """

import neighbor as nb
import random


class Neighborhood:
    """
    Neighborhood类定义了一个与给定解决方案相邻的解决方案集（邻域解集）。
    -解决方案是一个字典，其键是航班，其值是分配给这些航班的停机位（例如，solution{1:2，2:1}）
    -邻域解集是一个邻域列表（Neighbor class），其中每个邻域都由字典（Neighbor solution）和生成该邻域的运动定义
    """

    def __init__(self, num_flights, num_gates, compatibilities):
        self.num_flights = num_flights
        self.num_gates = num_gates
        self.compatibilities = compatibilities

    def init_params(self, sol, tabu_list, iteration):
        self.current_solution = sol
        self.neighborhood = list()  # 存储候选（邻域）解，里面的每个元素都是一个nb.Neighbor类
        self.tabu_list = tabu_list
        self.iteration = iteration

    def generate_neighborhood_one(self):
        """
        邻域动作1：考虑停机位与航班的兼容性，为每一个航班分配一个新的停机位。并只记录下不禁忌的邻域解。邻域解全部存储在内部变量 “self.neighborhood” 中。
        两层for循环作用：采用2层循环以遍历所有航班与停机位。
        if语句作用：1. 在循环遍历到的航班 f 中，循环遍历到的 g 是否与 f 当前搭配的停机位不同（相同就没必要换了）；
        		  2. 判断此时循环遍历到的 g 是否与此时循环遍历到的 f 在机型上匹配（兼容性）；
        		  3. 判断遍历到的 f 和 g 所组成的 “某航班 f 的停机位交换方案” 是否还在禁忌中；
        		  只有：是、是、否，方可将此时遍历到的停机位 g 对此时遍历到的航班 f 的原本的停机位进行更改 """
        for f in range(self.num_flights):
            # for g in range(self.num_gates):
            # for g in [random.randint(0, self.num_gates) for _ in range(int(self.num_gates / 2))]:
            for g in random.sample([_ for _ in range(self.num_gates)], int(self.num_gates / 2)):
                if (self.current_solution[f] is not g) \
                        and (self.is_gate_compatible(g, f)) \
                        and (not self.tabu_list.is_tabu(f, self.current_solution[f], g,
                                                        self.iteration)):  # 此句传入了：遍历到的航班f、f此时对应的停机位号、遍历到的停机位g、当前迭代次数
                    neighbor_dict = self.current_solution.copy()  # 没必要使用deepcopy，copy()够用
                    neighbor_dict[f] = g  # 将进入判断语句的 g 写入遍历到的 f 的对应停机位
                    # 一旦产生相邻的解决方案，就存储产生该解决方案的动作
                    neighbor_ins = nb.Neighbor(neighbor_dict, f, self.current_solution[f], g)
                    self.neighborhood.append(neighbor_ins)

    def gen_neighborhood_compatible_swap(self):
        """
        邻域动作2：考虑停机位与航班的兼容性，以当前的 “停机位分配方案” 为基础，满足交换条件后，交换该方案中的两个航班原本对应的停机位，
        将每一个交换动作作为一个邻域解，记录进内部变量 “self.neighborhood” 中。
        """

        for f1 in range(self.num_flights):
            for f2 in range(self.num_flights):
                if (f2 > f1) \
                        and (self.current_solution[f1] is not self.current_solution[f2]) \
                        and self.are_flights_compatible(self.current_solution, f1, f2) \
                        and (
                        not self.tabu_list.is_tabu(f1, self.current_solution[f1], self.current_solution[f2],
                                                   self.iteration)) \
                        and (
                        not self.tabu_list.is_tabu(f2, self.current_solution[f2], self.current_solution[f1],
                                                   self.iteration)):
                    neighbor_dict = self.current_solution.copy()
                    neighbor_ins = self.swap_flights(neighbor_dict, f1, f2)
                    self.neighborhood.append(neighbor_ins)

    def reset_neighborhood(self):
        self.neighborhood = list()

    def swap_flights(self, solution, f1, f2):
        old_gf1 = solution[f1]
        solution[f1] = solution[f2]
        solution[f2] = old_gf1
        neighbor_ins = nb.Neighbor(solution, f1, old_gf1, solution[f1])
        neighbor_ins.add_swap(f2, solution[f1], old_gf1)

        return neighbor_ins

    def is_gate_compatible(self, gate, flight):
        """检验传入的 停机位号(gate) 和 航班号(flight)，是否兼容，这就需要通过从文件中获取的 “兼容性” 来判断"""
        # 挨个遍历self.compatibilities内的每个键，然后把他们的值放到一个列表中，这个列表中包含有 “航班总数量” 个元素，每个元素都是一个列表：
        comp_vals = [c for c in self.compatibilities.values()]
        if gate in comp_vals[flight]:
            return True
        return False

    def are_flights_compatible(self, solution, f1, f2):
        """ 检验需要交换的两个航班各自本来对应的停机位号，是否与对方的航班兼容 """
        gate_f1 = solution[f1]
        gate_f2 = solution[f2]
        if self.is_gate_compatible(gate_f1, f2) and self.is_gate_compatible(gate_f2, f1):
            return True
        return False

    def generate_candidates(self, swap):
        """通过SWAP决定的某种方法，来生成候选（邻域）集合，即self.neighborhood"""
        if not swap:  # 如果不基于交换：SWAP --> swap == False
            self.generate_neighborhood_one()
        else:  # 如果基于交换：SWAP --> swap == True
            self.gen_neighborhood_compatible_swap()

        return self.neighborhood
