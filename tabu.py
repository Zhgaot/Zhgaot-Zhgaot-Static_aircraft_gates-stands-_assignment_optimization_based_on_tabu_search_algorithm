#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
import time
import copy
from collections import Counter
import neighborhood as nbhd
import tabu_list as tls
import functionm as fm
import draw


class Tabu:
    """ 定义禁忌搜索算法类及其内部属性和内部函数 """

    def __init__(self, n_flights, n_gates, compatibilities, flights, L0, LNP1):
        # self.optimal_sol = dict()
        # self.optimal_value = 0.0
        self.n_flights = n_flights
        self.n_gates = n_gates
        self.compatibilities = compatibilities
        self.flights = flights    # 定义一个存有航班类的列表
        self.L0 = L0
        self.LNP1 = LNP1

    def start_search(self, SWAP, RANDOM, KMAX, TABU_LENGTH, TIME, start_time, NUM_REPEAT, max_value_looptime, initsol_looptime):
        """  禁忌搜索算法函数 """

        """ ========== 0- 创建邻域类 ========== """
        self.nb = nbhd.Neighborhood(self.n_flights, self.n_gates, self.compatibilities)

        """ ========== 1- 得到各个目标函数的近似最大值，用于对各个目标函数进行归一化 ========== """
        # fm.maximum(1, 1)    # 当需要多次运行代码进行测试时，除第0次外的运行时需要对 functionm 中的 max 值进行还原
        # interval_value_max, conflict_max = self.loop_for_max(max_value_looptime)
        # fm.maximum(interval_value_max, conflict_max)    # 注意：这里得到的是间隙（而不是总评价函数）最大值和冲突次数最大值
        fm.maximum(130000, 89)  # 同一文件，测试时，提前运行一次找到相对最大的最大值，后面就不用再运行loop了，直接赋值就好

        print("\n 开始禁忌搜索......")

        """ ========== 2- 生成初始解决方案，并将初始解放入 self.flights 中以对其进行更新 ========== """
        if not RANDOM:                                       # 如果RANDOM==False，也就是初始解决方案是固定的时候
            sol = self.initial_solution_fixe()               # 从一个固定的初始解决方案开始
        else:                                                # 如果RANDOM==True，也就是初始解决方案是随机的时候
            sol = self.initial_solution()                    # 从一个随机的初始解决方案开始
            sol = self.min_conflict_initial_solution(initsol_looptime)  # 在多次循环中，尽量找到一个冲突次数小的随机初始解决方案
            print("随机分配的初始解为：", sol)
        self.flights = self.dict_sol_to_vect_flights(sol)    # 将生成的初始方案 sol 加到 self.flights 中
        flights_initsol = copy.deepcopy(self.flights)        # 用于生成 ”初始解甘特图“

        """ ========== 3- 计算初始解决方案中的总评价函数值和冲突次数 ========== """
        value, conflict = self.objective_function(sol)

        """ ========== 4- 将初始解决方案暂时作为最佳解决方案，并展示 ========== """
        self.optimal_sol = sol
        self.optimal_value = value
        self.optimal_conflict = conflict

        print("初始解决方案：")
        self.display_solution(self.flights)    # 显示初始解决方案
        print("初始总评价函数值：", self.optimal_value, )
        print("初始冲突次数：", self.optimal_conflict, "\n")

        """ ========== 5- 创建禁忌列表 ========== """
        self.tabu_list = tls.Tabu_list(TABU_LENGTH)    # 创建禁忌列表，并传入禁忌长度 TABU_LENGTH
        self.iteration = 0    # 当前迭代次数，设其初始值为 0

        value_list = list()
        """ ========== 6- 开始禁忌搜索直到达到终止条件 ========== """
        while self.iteration < KMAX:  # 当未达到最大迭代次数时可进入循环执行禁忌搜索算法
            print("迭代次数：", self.iteration)

            """ 6.1- 计算当前解决方案的非禁忌邻域（候选）集合 """
            self.nb.init_params(sol, self.tabu_list, self.iteration)  # 向 self.nb 里继续传参
            candidates = self.nb.generate_candidates(SWAP)            # 调用nb对象的函数以得到候选集合（传入的参数是SWAP，即邻域动作是否基于交换）
            # print("通过邻域动作，本次选定 ", len(candidates), " 个候选解")

            """ 6.2- 寻找邻域(候选)集合中的最佳更改（/交换）方案（以最小化总评价函数为筛选标准）"""
            # 返回候选集中最佳总评价函数值、最佳更改（交换）方案（即候选解）、该候选解的冲突次数：
            best_value, best_candidate, best_conf = self.best_solution(candidates)
            # print("最佳邻域(候选)解：", best_candidate.neighbor)
            # print("最佳邻域(候选)解的评价函数值：", best_value)
            # print("本次最佳邻域(候选)解参与更改的航班为：", best_candidate.f1, " 参与交换的停机位：", best_candidate.old_gate_f1, " --> ", best_candidate.new_gate_f1)

            """ 6.3- 更新禁忌表 """
            # if best_value > value:
            if best_value > self.optimal_value:
                self.add_tabu(best_candidate, SWAP)
            print("禁忌表：", self.tabu_list.tabu_list)

            """ 6.4- 更新最佳解决方案、最佳评价函数值、最佳冲突次数 """
            if best_value < self.optimal_value:
                self.optimal_sol = best_candidate.neighbor
                self.optimal_value = best_value
                self.optimal_conflict = best_conf
            # print("迄今为止的最佳评价函数值是：", self.optimal_value)

            """ 6.5- 更新当前解决方案 """
            sol = best_candidate.neighbor
            value = best_value
            conflict = best_conf
            print("当前解决方案评价函数值：", value)
            print("当前解决方案冲突次数：", conflict)

            """ 6.6- 若已搜索到最终解但还未达到最大迭代次数时，提前结束循环 """
            # 参考：https: // www.cnblogs.com / royfans / p / 8316060.html
            value_list.append(value)
            value_dict = Counter(value_list)
            if max(value_dict.values()) == NUM_REPEAT:
                break

            """ 6.7- 切换到下一次迭代"""
            self.iteration = self.iteration + 1

        print("搜索终止(FIN RECHERCHE)\n")

        """ ========== 7- 展示禁忌搜索得到的最佳解决方案、总评价函数值、冲突次数 ========== """
        self.flights = self.dict_sol_to_vect_flights(self.optimal_sol)  # 将最佳方案加入航班类列表中（在此将optim_sol_flights换成了self.flights）
        self.display_solution(self.flights)
        print("最佳评价函数值：", self.optimal_value)
        print("冲突次数：", self.optimal_conflict)

        """ ========== 8- 展示禁忌搜索算法总运行时间 ========== """
        if TIME:
            end_time = time.time()
            total_time = end_time - start_time
            print("算法运行总时间(second)：", total_time, "\n\n")

        """ ========== 9- 禁忌搜索算法结束时警报提示（若运行测试时可注释掉） ========== """
        # duration = 1800  # millisecond
        # freq = 550       # Hz
        # winsound.Beep(freq, duration)

        """ ========== 10- 生成初始解、最终解的甘特图（若运行测试时可注释掉，循环测试时先不用生成图） ========== """
        draw.initial_solution_gantt_parameter(flights_initsol)  # 传入初始解
        draw.initial_final_draw_gantt(self.n_gates, self.flights, self.L0, self.LNP1)  # 同时绘制初始解、最终解甘特图
        # draw.final_draw_gantt(self.n_gates, self.flights, self.L0, self.LNP1, True)  # 单单绘制最终解甘特图

    def loop_for_max(self, max_value_looptime):
        """
        一个循环，用于找到 ”空闲间隔“、”冲突次数“ 的相对最大值，以更好地对评价函数进行归一化；
        循环的次数越多，归一化就越精确 """
        count = 0
        loop_time = 0
        loop_start = time.time()
        loop_interval_value_list = list()
        loop_conflict_list = list()
        while loop_time < max_value_looptime:
            loop_sol = self.initial_solution()
            loop_flights = self.dict_sol_to_vect_flights(loop_sol)
            loop_interval_value, loop_conflict = fm.fonction_objectif_return_value(loop_flights, self.n_gates, self.L0, self.LNP1)
            loop_interval_value_list.append(loop_interval_value)
            loop_conflict_list.append(loop_conflict)
            count = count + 1
            loop_end = time.time()
            loop_time = loop_end - loop_start
        loop_interval_value_max = max(loop_interval_value_list)
        loop_conflict_max = max(loop_conflict_list)
        print("在循环", count, "次后得到的最大值为：")
        print("loop_value_max =", loop_interval_value_max)
        print("loop_conflict_max =", loop_conflict_max)
        return loop_interval_value_max, loop_conflict_max

    def min_conflict_initial_solution(self, initsol_looptime):
        """ 经过多次循环，找到一个 ”冲突次数“ 相对较低的随机初始解 """
        loop_time = 0
        loop_start = time.time()
        min_cft_sol = self.initial_solution()
        flights_0 = self.dict_sol_to_vect_flights(min_cft_sol)
        interval_value_0, min_conflict = fm.fonction_objectif_return_value(flights_0, self.n_gates, self.L0, self.LNP1)
        while loop_time < initsol_looptime:
            loop_sol = self.initial_solution()
            loop_flights = self.dict_sol_to_vect_flights(loop_sol)
            loop_interval_value, loop_conflict = fm.fonction_objectif_return_value(loop_flights, self.n_gates, self.L0,self.LNP1)
            if loop_conflict < min_conflict:
                min_conflict = loop_conflict
                min_cft_sol = loop_sol
            loop_end = time.time()
            loop_time = loop_end - loop_start
        return min_cft_sol

    def initial_solution(self):
        """ 为每个航班随机分配停机位，可保证分配到的停机位一定与该航班兼容 """
        solution = dict()
        for flight in range(self.n_flights):
            random_gate = random.randint(0, self.n_gates - 1)
            while not self.nb.is_gate_compatible(random_gate, flight):  # 若随机分配给某个航班的停机位与该航班不兼容，
                random_gate = random.randint(0, self.n_gates - 1)       # 则需要重新分配，直到兼容为止
            solution[flight] = random_gate
        # print("随机分配的初始解为：", solution)
        return solution

    def initial_solution_fixe(self):
        """ 为每个航班分配固定的停机位，这需要人为手动提供一个初始方案 """
        flights = dict()  # 函数里的局部变量
        '''flights[0] = 4
        flights[1] = 2
        flights[2] = 20
        flights[3] = 9
        flights[4] = 23
        flights[5] = 0
        flights[6] = 5
        flights[7] = 13
        flights[8] = 11
        flights[9] = 24
        flights[10] = 2
        flights[11] = 22
        flights[12] = 10
        flights[13] = 3
        flights[14] = 18
        flights[15] = 20
        flights[16] = 12
        flights[17] = 21
        flights[18] = 9
        flights[19] = 6
        flights[20] = 14
        flights[21] = 1
        flights[22] = 15
        flights[23] = 8
        flights[24] = 19
        flights[25] = 4
        flights[26] = 18
        flights[27] = 17
        flights[28] = 22
        flights[29] = 11
        flights[30] = 16
        flights[31] = 2
        flights[32] = 10
        flights[33] = 15
        flights[34] = 0
        flights[35] = 13
        flights[36] = 23
        flights[37] = 7
        flights[38] = 3
        flights[39] = 19
        flights[40] = 17
        flights[41] = 8
        flights[42] = 12
        flights[43] = 10
        flights[44] = 7
        flights[45] = 5
        flights[46] = 7
        flights[47] = 21
        flights[48] = 21
        flights[49] = 14
        flights[50] = 3
        flights[51] = 9
        flights[52] = 17
        flights[53] = 24
        flights[54] = 1
        flights[55] = 6
        flights[56] = 13
        flights[57] = 16
        flights[58] = 5
        flights[59] = 23'''

        '''flights[0] = 14
        flights[1] = 2
        flights[2] = 1
        flights[3] = 9
        flights[4] = 23
        flights[5] = 0
        flights[6] = 5
        flights[7] = 13
        flights[8] = 11
        flights[9] = 15
        flights[10] = 2
        flights[11] = 22
        flights[12] = 10
        flights[13] = 3
        flights[14] = 18
        flights[15] = 20
        flights[16] = 12
        flights[17] = 21
        flights[18] = 9
        flights[19] = 6
        flights[20] = 14
        flights[21] = 1
        flights[22] = 15
        flights[23] = 8
        flights[24] = 19
        flights[25] = 0
        flights[26] = 18
        flights[27] = 17
        flights[28] = 22
        flights[29] = 11
        flights[30] = 16
        flights[31] = 2
        flights[32] = 10
        flights[33] = 15
        flights[34] = 0
        flights[35] = 13
        flights[36] = 23
        flights[37] = 7
        flights[38] = 3
        flights[39] = 19
        flights[40] = 17
        flights[41] = 8
        flights[42] = 12
        flights[43] = 10
        flights[44] = 7
        flights[45] = 5
        flights[46] = 7
        flights[47] = 21
        flights[48] = 21
        flights[49] = 14
        flights[50] = 3
        flights[51] = 9
        flights[52] = 17
        flights[53] = 23
        flights[54] = 1
        flights[55] = 6
        flights[56] = 13
        flights[57] = 16
        flights[58] = 5
        flights[59] = 23'''

        flights[0] = 2
        flights[1] = 4
        flights[2] = 9
        flights[3] = 8
        flights[4] = 21
        flights[5] = 13
        flights[6] = 3
        flights[7] = 3
        flights[8] = 10
        flights[9] = 3
        flights[10] = 0
        flights[11] = 17
        flights[12] = 5
        flights[13] = 11
        flights[14] = 6
        flights[15] = 4
        flights[16] = 4
        flights[17] = 16
        flights[18] = 0
        flights[19] = 11
        flights[20] = 12
        flights[21] = 29
        flights[22] = 7
        flights[23] = 14
        flights[24] = 25
        flights[25] = 5
        flights[26] = 15
        flights[27] = 5
        flights[28] = 8
        flights[29] = 28
        flights[30] = 19
        flights[31] = 16
        flights[32] = 24
        flights[33] = 9
        flights[34] = 20
        flights[35] = 13
        flights[36] = 17
        flights[37] = 11
        flights[38] = 7
        flights[39] = 13
        flights[40] = 1
        flights[41] = 8
        flights[42] = 1
        flights[43] = 3
        flights[44] = 3
        flights[45] = 15
        flights[46] = 12
        flights[47] = 22
        flights[48] = 14
        flights[49] = 6
        flights[50] = 13
        flights[51] = 0
        flights[52] = 6
        flights[53] = 20
        flights[54] = 27
        flights[55] = 10
        flights[56] = 11
        flights[57] = 16
        flights[58] = 4
        flights[59] = 24
        flights[60] = 21
        flights[61] = 3
        flights[62] = 7
        flights[63] = 8
        flights[64] = 1

        num_incompatible = 0
        flight_incompatible = list()
        for flight in range(len(flights)):
            if not self.nb.is_gate_compatible(flights[flight], flight):
                num_incompatible = num_incompatible + 1
                flight_incompatible.append(flight)
                while not self.nb.is_gate_compatible(flights[flight], flight):  # 若上述固定分配给某个航班的停机位与该航班不兼容，
                    flights[flight] = random.randint(0, self.n_gates - 1)
        if num_incompatible:
            print("由于固定写入的初始解存在", num_incompatible, "个 “航班与停机位不兼容” 的情况，出现不兼容问题的航班如下：",
                  flight_incompatible, "，故将此些航班分配的初始停机位进行修改...")
            print("修改后的固定初始解为：", flights)
        else:
            print("固定初始解：", flights)

        return flights

    """ ** Pour afficher une solution de format [Flight] (vecteur d'instances Flight) ** """
    """ ** 显示航班格式解决方案的步骤 ** """

    def display_solution(self, sol_flights):
        """
        该函数用于：展示解决方案。
        对于此时传入的、根据到港时间排列的航班列表，分别列举它们各自都放在了哪些停机位中，
        并展示它们的航班序号、到港时间、离港时间 """
        for g in range(self.n_gates):
            print("位于停机位", g, ":")
            for f in fm.flights_assigned(g, sol_flights):  # 返回在同一个停机位 g 上，随时间推移，停放的航班列表，f遍历列表内元素；随着 g 的遍历，将会得到所有停机位上的航班列表
                print("航班 ", f.number, ": 到港时间 ", f.arrival_time, " 离港时间 ", f.departure_time)

    """ ****** Fonctions internes ****** """

    """ ** Fonction qui calcule la fonction objectif ou coût d'une solution donnée.
        Elle retourne la valeur objectif et le nombre de conflicts trouvés entre les vols. ** """

    def objective_function(self, sol):
        """ 该函数用于：调用 fm.fonction_objectif，以计算解决方案中的目标函数值和冲突次数 """
        # 转换解决方案格式，convertir format de solution
        flights = self.dict_sol_to_vect_flights(sol)  # 这里不明白为什么不直接传入self.flights？？？因为该函数不止一个地方要用到，要具有普遍性
        # 计算目标值，calculer sa valeur objectif
        obj_value, conflict = fm.fonction_objectif(flights, self.n_gates, self.L0, self.LNP1)
        return obj_value, conflict

    """ ** Fonction qui calcule la meilleur solution minimisant la fonction objectif sur un ensemble de solutions.
        Notamment pour calculer le meilleur voisin d'un voisinage. ** """

    def best_solution(self, sols):  # sols est une liste de classes Neighbor
        """
        该函数用于：寻找到一组解决方案（邻域/候选解）中最小化目标函数的最佳解决方案。
        其实最终，就是在上述这一群邻域解中，只会寻找到某一个航班的更改（交换）方案，
        因为这个航班的这个方案，比其他所有航班的所有方案都最小化了目标函数。"""
        i = 0
        result0, conflict0 = self.objective_function(sols[i].neighbor)
        best_sol = sols[i].neighbor  # 这个是否没有用处，应该可以省略
        best_pos = i
        while i < len(sols) - 1:
            i = i + 1
            new_res, new_conf = self.objective_function(sols[i].neighbor)
            if new_res < result0:
            # if new_res < result0 or new_conf < conflict0:
            # if new_conf < conflict0:
                best_sol = sols[i].neighbor  # 这个是否没有用处，应该可以省略
                result0 = new_res
                conflict0 = new_conf
                best_pos = i

        return result0, sols[best_pos], conflict0

    """ ** Fonction qui ajoute un mouvement à la liste tabou. Elle prend un voisin comme paramètre et interdit le mouvement qui a généré ce 		voisin. Par exemple, si un voisin est généré en changeant dans la solution originale la porte du vol 3 de porte 1 à 2,
        donc on dit que le mouvement qui a généré ce voisin est (vol 3, porte 1, porte 2). ** """

    def add_tabu(self, neighbor_ins, SWAP):
        self.tabu_list.insert_movement(neighbor_ins.f1, neighbor_ins.old_gate_f1, neighbor_ins.new_gate_f1,
                                       self.iteration)
        # print("Nouveau mouvement tabou ajouté: (Vol ",neighbor_ins.f1,": porte ",neighbor_ins.old_gate_f1,"=> porte ",neighbor_ins.new_gate_f1,")")
        if SWAP:  # si la méthode de voisinage de swap est activée, on interdit aussi le mouvement du second vol (vol de swap)
            self.tabu_list.insert_movement(neighbor_ins.f2, neighbor_ins.old_gate_f2, neighbor_ins.new_gate_f2,
                                           self.iteration)
            print("Nouveau mouvement tabou ajouté: (Vol ", neighbor_ins.f2, ": porte ", neighbor_ins.old_gate_f2,
                  "=> porte ", neighbor_ins.new_gate_f2, ")")

    """ ** Fonctions de support ** """

    # def get_iteration(self):
    #	return self.iteration

    # def get_tabu_length(self):
    #	return TABU_LENGTH

    # def get_tabu_list_length(self):
    #	return TABU_LIST_SIZE

    """ ** Fonction de conversion de format d'une solution (de dict() à vecteur de Flights) ** """

    def dict_sol_to_vect_flights(self, sol_dict):
        """ 该函数用于：将一个新的 “停机位分配方案” 放入一个，新生成的、元素全为 Flight 类的，列表当中 """
        # sol_flights = self.flights.copy()  # 复制flights，它是一个内部全是Flight对象的列表，每个对象都对应一个航班复制后给sol_flights
        sol_flights = copy.deepcopy(self.flights)
        for i in range(self.n_flights):
            sol_flights[i].gate = sol_dict[i]  # 在sol_flights中的每个对象中，将传入这个函数的解决方案分别放进各个对象（航班）的gate里
        return sol_flights