import numpy as np
import logging


def filling_data(data):
    """ Функция filling_data принимает на вход массив считанных входных данных data из файла json
     и считает матрицу расстояний между точками
     при этом в нулевых строках и столбцах лежат id точек"""
    logging.info("Началось заполнение матрицы расстояний")
    len_axes = len(data) + 1
    res = np.ones((len_axes, len_axes))
    np.fill_diagonal(res, np.inf)
    """Заполнение главной диагонали матрицы значением бесконечности"""

    for row in range(len_axes):
        for column in range(row + 1, len_axes):
            if row == 0:
                """Заполнение id точек"""
                id = (data[column - 1]).get('id')
                res[0][column] = id
                res[column][0] = id
            else:
                x1 = (data[row - 1]).get('x')
                x2 = (data[column - 1]).get('x')
                y1 = (data[row - 1]).get('y')
                y2 = (data[column - 1]).get('y')
                value = np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
                res[row][column] = value
                res[column][row] = value
            """Заполнение матрицы расстояний симметрично относительно главной диагонали, 
            при чем value рассчитана заранее лишь один раз"""

    logging.info("Матрица расстояний получена")
    return res

def air_corridor(data_corridor, matrix):
    """Функция air_corridor принимает на вход список словарей data_corridor
    с КТ, между которыми запрещен пролет и меняет расстояние в матрице расстояний
    matrix между этими КТ на значение бесконечности"""
    len_axes = len(matrix)
    for group_id in range(len(data_corridor)):
        """Пробегаемся по id КТ, между которыми запрещен пролет"""
        id_1 = (data_corridor[group_id]).get('id1')
        id_2 = (data_corridor[group_id]).get('id2')
        for elem_in_row in range(1, len_axes):
            """Ищем совпадение с id1 в строке с idшниками"""
            if matrix[0][elem_in_row] == id_1:
                for elem_in_column in range(1, len_axes):
                    """Ищем совпадение с id2 в столбце с idшниками"""
                    if matrix[elem_in_column][0] == id_2:
                        matrix[elem_in_column][elem_in_row] = np.inf
                        matrix[elem_in_row][elem_in_column] = np.inf
                        break
                    if elem_in_column == len_axes - 1:
                        msg = f'This id2 = {id_2} is not found'
                        raise RuntimeError(msg)
                break

            if elem_in_row == len_axes - 1:
                msg = f'This id1 = {id_1} is not found'
                raise RuntimeError(msg)
    """Прописаны исключения на случай того, что в данных для воздушных коридоров
     будет указана точка, которой не было в data_points"""
    return matrix



