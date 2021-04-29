import numpy as np
import os

class Flight:
    """定义航班类, 其内部属性如下 :
    - 此航班的编号
    - 此航班的到港时间
    - 此航班的离港时间
    - 此航班能够兼容的停机位
    - 此航班的评价函数值
    - 分配给此航班的停机位 """


    def __init__(self):
        self.number = 0
        self.arrival_time = int(0)
        self.departure_time = int(100)
        self.compatible_gates = []
        self.contribution = 0
        self.gate = int(9999)
        # self.assigned = False
