import math
import numpy as np

"""
   Принимает координаты отрезка, координаты центра и радиус окружности,
   возвращает bool флаг: True - есть одна или две общих точки (касание или пересечение),
   False - нет общих точек (т.е. нет пересечения)

   A_x, A_y - координаты первого конца отрезка (в километрах)
   B_x, B_y - координаты второго конца отрезка (в километрах)
   C_x, C_y - координаты центра окружности (в километрах)
   R - радиус окружности (в метрах)
"""


def circle_and_segment(a_x, a_y, b_x, b_y, c_x, c_y, r):
    """Сдвиг отрезка и окружности"""
    a_x -= c_x
    a_y -= c_y
    b_x -= c_x
    b_y -= c_y
    """Решим квадратное уравнение, чтобы определить взаимное расположение окружности и отрезка"""
    a = (b_x - a_x) ** 2 + (b_y - a_y) ** 2
    b = 2 * ((b_x - a_x) * a_x + (b_y - a_y) * a_y)
    c = a_x ** 2 + a_y ** 2 - r ** 2
    d = b ** 2 - 4 * a * c
    if d < 0:
        return False
    else:
        t_1 = (-b + d ** 0.5) / (2 * a)
        t_2 = (-b - d ** 0.5) / (2 * a)
        if 0 <= t_1 <= 1 and 0 <= t_2 <= 1:
            return True


"""
   Принимает координаты точки А, координаты центра окружности С и радиус R;
   Возвращает список из двух точек касания между прямой, 
   проведенной через точку А, и окружностью С;
"""


def tangent(a_x, a_y, c_x, c_y, r):
    l_x = c_x - a_x
    l_y = c_y - a_y
    le = (l_x ** 2 + l_y ** 2) ** 0.5
    """Получение точек касания между окружностью и прямой, проведенной из точки A(A_x, A_y)"""
    t1_x = r * math.sin(math.atan2(l_y, l_x) - math.asin(r / le)) + c_x
    t1_y = r * (-math.cos(math.atan2(l_y, l_x) - math.asin(r / le))) + c_y
    t2_x = r * (-math.sin(math.atan2(l_y, l_x) + math.asin(r / le))) + c_x
    t2_y = r * math.cos(math.atan2(l_y, l_x) + math.asin(r / le)) + c_y
    """Получаем массив с координатами двух точек касания"""
    res = [(t1_x, t1_y), (t2_x, t2_y)]
    return res


"""
   Функция принимает два кортежа с координатами двух точек;
   возвращает длину отрезка, заключенного между этими точками
"""


def segment_length(tuple_1, tuple_2):
    x1 = tuple_1[0]
    y1 = tuple_1[1]
    x2 = tuple_2[0]
    y2 = tuple_2[1]
    res = ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
    return res


"""
   Функция принимает два кортежа с координатами двух точек и радиус окружности;
   Возвращает меньший центральный угол дуги окружности, заключенной между точками A и B
"""


def tetha(tuple_1, tuple_2, c_y, r):
    y1 = tuple_1[1]
    y2 = tuple_2[1]
    le = segment_length(tuple_1, tuple_2)
    if ((y1 - c_y) < 0 and (y2 - c_y) >= 0) or ((y1 - c_y) >= 0 and (y2 - c_y) < 0):
        alpha = (2 * np.pi - (math.acos(1 - (le ** 2) / (2 * (r ** 2))))) * (180 / np.pi)
    else:
        alpha = (math.acos(1 - (le ** 2) / (2 * (r ** 2)))) * (180 / np.pi)
    return alpha


"""
   Функция принимает два кортежа с координатами двух точек и радиус окружности;
   Возвращает меньшую длину дуги окружности, заключенную между точками A и B
"""


def arc_length(tuple_1, tuple_2, r):
    le = segment_length(tuple_1, tuple_2)
    alpha = math.acos(1 - (le ** 2) / (2 * (r ** 2)))
    res = alpha * r
    return res


"""
    Имеем отрезок AB, пересекающий окружность C.
    Тогда будут следующие точки касания для конца А: t_1  и t_2;
    Тогда будут следующие точки касания для конца B: t_3  и t_4;
    Эти четыре точки касания лежат в списке tangents.
    Значит существует 4 маршрута по дугам, из которых определим оптимальный:
    route[0]: A - t_1 - t_3 - B
    route[1]: A - t_1 - t_4 - B
    route[2]: A - t_2 - t_3 - B
    route[3]: A - t_2 - t_4 - B
    Тогда каждый маршрут можно разбить на 3 куска: касательная, дуга и касательная;
    begin0: A - t_1
    begin1: A - t_2
    end0: t_3 - B
    end1: t_4 - B
    Кусок дуги обозначим middle
"""


def processing_route(tangents, a_x, a_y, b_x, b_y, r):
    route = [0, 0, 0, 0]
    begin0 = segment_length((a_x, a_y), tangents[0])
    begin1 = segment_length((a_x, a_y), tangents[1])
    end0 = segment_length(tangents[2], (b_x, b_y))
    end1 = segment_length(tangents[3], (b_x, b_y))
    middle0 = arc_length(tangents[0], tangents[2], r)
    middle1 = arc_length(tangents[0], tangents[3], r)
    middle2 = arc_length(tangents[1], tangents[2], r)
    middle3 = arc_length(tangents[1], tangents[3], r)
    route[0] = begin0 + middle0 + end0
    route[1] = begin0 + middle1 + end1
    route[2] = begin1 + middle2 + end0
    route[3] = begin1 + middle3 + end1
    min_route = min(route)
    res = (route.index(min_route), min_route)
    return res


"""
    Функция по номеру обходного маршрута (указаны в функции processing_route) составляет словарь 
    с данными для построения касательной line_1, дуги arc и еще одной касательной line_2 
"""


def detour_route(number_route, a_x, a_y, b_x, b_y, c_x, c_y, r, tangents):
    if number_route == 0:
        line_1 = (a_x, a_y) + tangents[0]
        line_2 = tangents[2] + (b_x, b_y)
        alpha = tetha((c_x + r, c_y), tangents[0], c_y, r)
        beta = tetha((c_x + r, c_y), tangents[2], c_y, r)

    if number_route == 1:
        line_1 = (a_x, a_y) + tangents[0]
        line_2 = tangents[3] + (b_x, b_y)
        alpha = tetha((c_x + r, c_y), tangents[0], c_y, r)
        beta = tetha((c_x + r, c_y), tangents[3], c_y, r)

    if number_route == 2:
        line_1 = (a_x, a_y) + tangents[1]
        line_2 = tangents[2] + (b_x, b_y)
        alpha = tetha((c_x + r, c_y), tangents[1], c_y, r)
        beta = tetha((c_x + r, c_y), tangents[2], c_y, r)

    if number_route == 3:
        line_1 = (a_x, a_y) + tangents[1]
        line_2 = tangents[3] + (b_x, b_y)
        alpha = tetha((c_x + r, c_y), tangents[1], c_y, r)
        beta = tetha((c_x + r, c_y), tangents[3], c_y, r)
    if alpha == 0 and beta > 180:
        alpha += 360
    if beta == 0 and alpha > 180:
        beta += 360
    if alpha >= beta:
        tetha_1 = beta
        tetha_2 = alpha
        arc = ((c_x, c_y), r, r, tetha_1, tetha_2)
    if alpha < beta:
        tetha_1 = alpha
        tetha_2 = beta
        arc = ((c_x, c_y), r, r, tetha_1, tetha_2)

    res = {'line_1': line_1, 'arc': arc, 'line_2': line_2}
    return res


"""
    Функция принимает данные всех точек, данные о ЗД ПВО и матрицу расстояний matrix;
    в ходе работы преобразует матрицу расстояний между точками исходя из ЗД ПВО;
    возвращает словарь с обходными маршрутами detour_routes:
    detour_routes = {key: value, ...]
    key: кортеж из id двух точек, между которыми имеется ЗД ПВО,
    value: словарь с данными для построения касательной line_1, дуги arc и еще одной касательной line_2
"""


def forbidden_zone(data_points, data_pvo, matrix):
    detour_routes = {}
    for k in range(len(data_pvo)):
        for i in range(1, len(data_points) + 1):
            for j in range(i + 1, len(data_points) + 1):
                a_id = (data_points[i - 1]).get('id')
                a_x = (data_points[i - 1]).get('x')
                a_y = (data_points[i - 1]).get('y')
                b_id = (data_points[j - 1]).get('id')
                b_x = (data_points[j - 1]).get('x')
                b_y = (data_points[j - 1]).get('y')
                c_x = (data_pvo[k]).get('x')
                c_y = (data_pvo[k]).get('y')
                r = (data_pvo[k]).get('r')
                """приведение модуля радиуса r в километры"""
                r /= 1000
                """Проверка на общие точки между отрезком и окружностью"""
                if circle_and_segment(a_x, a_y, b_x, b_y, c_x, c_y, r):
                    """Получение двух точек касания для каждого из обоих концов отрезка"""
                    tangents = tangent(a_x, a_y, c_x, c_y, r) + tangent(b_x, b_y, c_x, c_y, r)
                    """Определяем длину наименьшего пути и способ прохода по дуге окружности"""
                    route = processing_route(tangents, a_x, a_y, b_x, b_y, r)
                    """Номера маршрутов прописаны в функции processing_route, число от 0 до 3"""
                    number_route = route[0]
                    len_route = route[1]
                    matrix[i][j] = len_route
                    matrix[j][i] = len_route
                    detour_routes[(a_id, b_id)] = detour_route(number_route, a_x, a_y, b_x, b_y, c_x, c_y, r, tangents)
                    detour_routes[(b_id, a_id)] = detour_route(number_route, a_x, a_y, b_x, b_y, c_x, c_y, r, tangents)
    return detour_routes
