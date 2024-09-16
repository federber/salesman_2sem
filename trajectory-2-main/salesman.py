import copy
import numpy as np
import logging
from utils_salesman import Matrix, Plan, Path_and_H, create_path, find_min_in_cutted, Edge, normalize, min_wtht_ind


def salesman(start_matrix, numb_of_salesmen):
    """Реализует решение задачи Комивояжера"""
    start_matrix = copy.deepcopy(start_matrix)
    start_matrix = np.delete(start_matrix, 0, 1)
    nums_to_ind = {}
    nums_to_name = {}
    for i in range(len(start_matrix[0])):
        nums_to_ind[i] = i
        nums_to_name[i] = int(start_matrix[0][i])

    start_matrix = np.delete(start_matrix, 0, 0)
    logging.basicConfig(filename='example.log', level=logging.DEBUG, filemode='w')
    start_matrix = Matrix(np.array(start_matrix, np.float64))
    nums_to_ind_2 = {}

    if numb_of_salesmen != 1:
        for i in range(2 * numb_of_salesmen):
            nums_to_ind_2[i] = nums_to_ind[0]

        for i in range(2 * numb_of_salesmen + 1, 1 + 2 * numb_of_salesmen + len(start_matrix) - 1, 1):
            nums_to_ind_2[i - 1] = nums_to_ind[i - 2 * numb_of_salesmen]

        start_matrix.replace_by_numb_of_salesmen(numb_of_salesmen)

    cut_branches = []
    """ Н - полная длина пути. Во всех ветвях хранится именно ПОЛНАЯ длина пути
        (длина пути без этой ветви + длина пути по ветви)"""
    act_plan = Plan(matrix=start_matrix)
    while True:
        matrix = copy.deepcopy(act_plan.matrix)

        dh = matrix.reduct()
        names = matrix.zero_pow()
        inc_matrix = copy.deepcopy(matrix)
        not_matrix = copy.deepcopy(matrix)
        not_matrix.make_inf(names)

        inc_matrix.make_inf(names[::-1])
        inc_matrix.delete_by_name(names)

        i_dH = inc_matrix.reduct()
        n_dH = not_matrix.reduct()

        inc_plan = copy.deepcopy(act_plan)
        inc_plan.add_edge(Edge(names, True, dh + i_dH))
        inc_plan.matrix = inc_matrix

        not_plan = copy.deepcopy(act_plan)
        not_plan.add_edge(Edge(names, False, dh + n_dH))
        not_plan.matrix = not_matrix

        if i_dH <= n_dH:
            """Выбираем меньшую ветвь(ту из двух ветвей, длина пути по которой меньше)
             Добавляем эту ветвь в результат, а большую - в список оборванных ветвей"""
            logging.info(f'edge {names} included')
            cut_branches.append(copy.deepcopy(not_plan))
            act_plan = inc_plan
        else:
            logging.info(f'edge {names} excluded')
            cut_branches.append(copy.deepcopy(inc_plan))
            act_plan = not_plan

        min_in_cut = find_min_in_cutted(cut_branches)
        """Находим наименьшую из оборванных ветвей. Если текущая длина пути меньше длины пути через найденную оборванную ветвь,
        добавляем ветвь из оборванных в результат, а текущую ветвь в список оборванных"""

        if act_plan.H >= min_in_cut.H:
            logging.info(f'take plan from cut branches')
            cut_branches.append(copy.deepcopy(act_plan))
            cut_branches.remove(min_in_cut)
            act_plan = min_in_cut

        if len(act_plan.matrix) == 1:
            logging.info(f'last edge')

            act_plan.add_edge(Edge([act_plan.matrix.rows_names[0], act_plan.matrix.cols_names[0]], True,
                                   act_plan.matrix.matrix[0, 0]))

            if numb_of_salesmen > 1:
                pairs = [res.names for res in act_plan.prev_branches if res.is_inc == True]

                for pair in pairs:
                    pair[0] = nums_to_ind_2[pair[0]]
                    pair[1] = nums_to_ind_2[pair[1]]
            if len(create_path(act_plan)) != numb_of_salesmen:
                logging.info(f'looping detected')
                for i in range(len(cut_branches) - 1, 0, -1):
                    if len(cut_branches[i].matrix) > len(act_plan.matrix):
                        act_plan = cut_branches[i]
                        logging.info(f'find previous without looping')
                        cut_branches.pop(i)

            else:
                break

    res = create_path(act_plan)
    for path in res:
        for i in range(len(path)):
            path[i] = nums_to_name[path[i]]

    return normalize(res)
