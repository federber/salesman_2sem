import copy
import numpy as np
import logging


class Path_and_H:
    """Класс, включающий в себя список вершин, образующих путь,
    а также длину данного пути"""

    def __init__(self, path, H):
        self.H = H
        self.path = path

    def __eq__(self, other):
        return self.H == other.H and self.path == other.path

    def __repr__(self):
        return f'{self.path} {self.H}'


class Edge:
    """Описывает ребро графа"""

    def __init__(self, names, is_inc, weight):
        self.names = copy.deepcopy(names)
        self.is_inc = is_inc
        self.weight = weight


class Plan:
    """Тип данных, описывающий ветвь траектории. Поля класса: индексы ребра,
    включением/исключением которой в траекторию получена ветвь,
    флаг(включена/исключена вершина), матрица расстояний, список предыдущих ребер"""

    def __init__(self, H=None, names=None, is_included=None, matrix=None, prev_branches=None):
        if isinstance(names, type(None)):
            self.names = []
            self.is_inc = False
            self.H = 0
        else:
            self.names = copy.deepcopy(names)
            self.is_inc = is_included
            self.H = H

        if isinstance(matrix, type(None)):
            self.matrix = Matrix()
        else:
            self.matrix = copy.deepcopy(matrix)
        if isinstance(prev_branches, type(None)):
            self.prev_branches = []
        else:
            self.prev_branches = copy.deepcopy(prev_branches)

    def add_edge(self, edge=None):
        """Добавляет ребро в план"""
        if isinstance(edge, type(None)):
            raise RuntimeError
        else:
            self.prev_branches.append(copy.deepcopy(edge))
            self.H = sum([el.weight for el in self.prev_branches])

    def __eq__(self, other):
        """Равными считаются два объекты класса, у которых равны все соответсвующие элементы.
        Такая реализация необходима для нахождения совпадающих ветвей."""
        return all([self.H == other.H,
                    self.is_inc == other.is_inc,
                    self.names == other.names,
                    self.matrix == other.matrix])

    """Более короткой считается ветвь с наименьшей длиной пути.
    Такая реализация необходима для нахождения пути с наименьшей длиной."""

    def __lt__(self, other):
        return self.H < other.H

    def __gt__(self, other):
        return self.H > other.H

    def __repr__(self):
        st = ''
        for el in self.prev_branches:
            if el.is_inc:
                st = st + f'{el.names}' + f'{el.is_inc}'
        return st + f'{self.names} {self.is_inc}'


class Matrix:
    def __init__(self, matr=None):
        if isinstance(matr, type(None)):
            self.matrix = np.array([[]], np.float64)
        else:
            self.matrix = copy.deepcopy(np.array(matr, np.float64))
        logging.info("New matrix created")

        """ self.matrix - матрица расстояний
        self.cols_names - массив с индексами(номерами) столбцов в начальной матрице
        self.rows_names - массив с индексами(номерами) строк в начальной матрице
        (индексы могут отличаться от индексов элементов в массиве)"""
        self.make_diag_inf()
        self.cols_names = [i for i in range(0, len(self.matrix))]
        self.rows_names = [i for i in range(0, len(self.matrix))]

    def name_of_min_in_row(self, row_name):
        return self.cols_names.index(min(self.matrix[self.rows_names[row_name]]))

    def replace_by_numb_of_salesmen(self, numb_of_sal):
        """Изменяет матрицу для решения задачи нескольких комивояжеров"""

        # это нужно переписать нормально на numpy, просто надо было проверить

        a_x0 = np.delete(self.matrix[:, 0], 0, 0)
        x0_a = np.delete(self.matrix[0], 0, 0)
        self.matrix = np.delete(self.matrix, 0, 0)
        self.matrix = np.delete(self.matrix, 0, 1)

        for i in range(numb_of_sal):
            self.matrix = np.insert(self.matrix, 0, a_x0, axis=1)
        for i in range(numb_of_sal):
            self.matrix = np.insert(self.matrix, 0, [float('inf')] * len(self.matrix), axis=1)

        ins_line = []
        for i in range(numb_of_sal):
            ins_line.append(0)
        for i in range(numb_of_sal + len(self.matrix)):
            ins_line.append(float('inf'))
        for i in range(numb_of_sal):
            self.matrix = np.insert(self.matrix, 0, ins_line, axis=0)
        ins_line = []
        for i in range(2 * numb_of_sal):
            ins_line.append(float('inf'))
        ins_line = np.concatenate((ins_line, x0_a), axis=0)
        for i in range(numb_of_sal):
            self.matrix = np.insert(self.matrix, 0, ins_line, axis=0)

        self.cols_names = [i for i in range(0, len(self.matrix))]
        self.rows_names = [i for i in range(0, len(self.matrix))]

    def __eq__(self, other):
        return all([np.all(self.matrix == other.matrix),
                    self.cols_names == other.cols_names,
                    self.rows_names == other.rows_names])

    def __len__(self):
        return len(self.matrix)

    def make_diag_inf(self):
        """Функция заменяет на float('inf') диагональные элементы матрицы"""
        self.matrix += np.where(np.eye(self.matrix.shape[0]) > 0, float('inf'), 0)
        logging.info("Change matrix diagonal to INF")

    def delete_by_name(self, names):
        """names[0] - номер удаляемой строки
            names[1] - номер удаляемого столбца
            (номер, который имели строка/столбец в первоначальной матрице)
            Удаляет пару строка+столбец соответствующую names"""
        c_i = self.cols_names.index(names[1])
        r_i = self.rows_names.index(names[0])
        self.matrix = np.delete(self.matrix, c_i, axis=1)
        self.matrix = np.delete(self.matrix, r_i, axis=0)
        self.cols_names.pop(c_i)
        self.rows_names.pop(r_i)

    def reduct(self):
        """Функция, производящая редуцирование матрицы по строкам и столбцам"""

        H = 0
        length = len(self.matrix)
        for i in range(length):  # По строкам
            element = min(self.matrix[i])
            H += element
            if element != np.inf:
                for j in range(length):
                    self.matrix[i][j] -= element
        for i in range(length):  # По столбцам
            element = min(row[i] for row in self.matrix)
            H += element
            for j in range(length):
                if element != np.inf:
                    self.matrix[j][i] -= element
        return H

    def zero_pow(self):
        """Определяет нулевой элемент матрицы "с минимальной степенью",
        т.е. для каждого нуля ищет второй минимум в строке и столбце,
        складывает их. Возвращает индексы нуля с минимальной такой суммой"""
        max_zero_pow = 0
        index1 = 0
        index2 = 0
        for i in range(self.matrix.shape[0]):
            for j in range(self.matrix.shape[1]):
                if self.matrix[i][j] == 0:
                    tmp = min_wtht_ind(self.matrix[i], j) + min_wtht_ind([row[j] for row in self.matrix], i)
                    if tmp >= max_zero_pow:
                        max_zero_pow = tmp
                        index1 = i
                        index2 = j
        logging.info('degrees of zeros are determined')
        return [self.rows_names[index1], self.cols_names[index2]]

    def make_inf(self, names):
        """Превращает элемент с индексами names в float('inf')"""
        if names[0] in self.rows_names and names[1] in self.cols_names:
            self.matrix[self.rows_names.index(names[0])][self.cols_names.index(names[1])] = float('inf')

            logging.info(f'change element {names} to INF')
        else:
            logging.info(f'can not find element {names}')

    def __repr__(self):
        outstr = ''
        for i in range(len(self.matrix)):
            outstr += str(self.rows_names[i]) + ' | ' + str(self.matrix[i]) + '\n'
        outstr += '-------------------\n'

        return '    ' + str(self.cols_names) + '\n     ---------------\n' + outstr


def normalize(arr):
    """Функция, приводящая путь к стандартному виду
    (начальная точка пути - точка с наименьшим индексом)"""
    arr = copy.deepcopy(arr)
    for path in arr:
        path.pop()

        for i in range(path.index(min(path))):
            path.append(path[0])
            path.pop(0)
        path.append(path[0])
    return arr


def min_wtht_ind(lst, pass_index):
    """находит минимальный элемент lst, исключая
     элемент с индексом pass_index"""
    return min(np.delete(copy.deepcopy(lst), pass_index))


def find_min_in_cutted(cut_branches):
    """Находит в списке оборванных ветвей ветвь с минимальной длиной пути"""
    logging.info('element with minimal H in cutted branches was founded')
    return min(cut_branches)


def create_path(inp_plan):
    """Создает путь из массива пар вершин, между которыми необходимо пролететь."""
    plan = copy.deepcopy(inp_plan)
    pairs = [res.names for res in plan.prev_branches if res.is_inc == True]

    path_arr = []
    d = dict(copy.deepcopy(pairs))
    path = []
    prev_point = list(d.keys())[0]
    while len(d.keys()) > 0:

        path.append(prev_point)
        try:
            d[prev_point]
        except KeyError:
            if path[len(path) - 1] != path[0]:
                path.append(path[0])
            prev_point = list(d.keys())[0]
            path_arr.append(copy.deepcopy(path))
            path = []

        else:
            tmp = prev_point
            prev_point = d[prev_point]
            d.pop(tmp)

    path.append(prev_point)
    if path[len(path) - 1] != path[0]:
        path.append(path[0])

    path_arr.append(path)
    logging.info(f'path created: {path_arr} from inp arr {pairs})')
    return path_arr
