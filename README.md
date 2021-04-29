# Zhgaot-Zhgaot-Static_aircraft_gates-stands-_assignment_optimization_based_on_tabu_search_algorithm
基于禁忌搜索算法的静态停机位分配

/* 文件说明 */
1. data目录：用于存放待读取的实验数据，内部文件的命名为"GAP##_**.txt"；##表示停机位总个数，**表示航班总个数
2. test目录：test/picture文件夹内部用于存放每次运行结束后生成的初始解/最终解甘特图
3. main.py：主函数（运行入口）
4. data.py：用于data目录中读取数据
5. flight.py：航班（飞机）类的实现
6. neighbor.py：neighbor类的实现，用于定义邻域解决方案
7. tabu_list.py：禁忌表类的实现
8. neighborhood.py：邻域动作的实现（封装），通过邻域动作，来生成邻域(候选)解
9. tabu.py：禁忌搜索的实现（封装）
10. functionm.py：存放了一些辅助函数和评价函数
11. draw.py：用于绘制初始解与最终解的甘特图
