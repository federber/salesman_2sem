import numpy as np

"""
    Функция принимает три кортежа с координатами трех точек, лежащих на одной прямой: p1, p2, p3
    возвращает bool флаг: True - p2 лежит на отрезке p1p3
    False - во всех иных случаях
"""


def on_segment(p1: tuple[float, float], p2: tuple[float, float], p3: tuple[float, float]) -> bool:
    p1_x = p1[0]
    p1_y = p1[1]
    p2_x = p2[0]
    p2_y = p2[1]
    p3_x = p3[0]
    p3_y = p3[1]
    if ((p2_x <= max(p1_x, p3_x)) and (p2_x >= min(p1_x, p3_x)) and
            (p2_y <= max(p1_y, p3_y)) and (p2_y >= min(p1_y, p3_y))):
        return True
    return False


"""
    Функция принимает три кортежа с координатами трех точек: 
    возвращает строку с ориентаций этих точек на плоскости: 
    "counterclockwise" - точки расположены против часовой стрелки;
    "clockwise" - точки расположены по часовой стрелке;
    "collinear" - точки лежат на одной прямой

"""


def orientation(p1: tuple[float, float], p2: tuple[float, float], p3: tuple[float, float]) -> str:
    p1_x = p1[0]
    p1_y = p1[1]
    p2_x = p2[0]
    p2_y = p2[1]
    p3_x = p3[0]
    p3_y = p3[1]
    val = ((p2_y - p1_y) * (p3_x - p2_x)) - ((p2_x - p1_x) * (p3_y - p2_y))
    if val > 0:
        return "clockwise"
    elif val < 0:
        return "counterclockwise"
    else:
        return "collinear"


"""
    Функция принимает четыре кортежа с координатами четырех точек: 
    p1, q1 - концы первого отрезка
    p2, q2 - концы первого отрезка
    возвращает bool флаг: True - есть пересечение между отрезками,
    False - нет общих точек (т.е. нет пересечения)
"""


def intersection_segments(p1: tuple[float, float], q1: tuple[float, float],
                          p2: tuple[float, float], q2: tuple[float, float]) -> bool:
    o1 = orientation(p1, q1, p2)
    o2 = orientation(p1, q1, q2)
    o3 = orientation(p2, q2, p1)
    o4 = orientation(p2, q2, q1)
    """Общий случай"""
    if (o1 != o2) and (o3 != o4):
        return True

    """ p1 , q1 и p2 лежат на одной прямой и p2 лежит на прямой p1q1 """
    if (o1 == "collinear") and on_segment(p1, p2, q1):
        return True

    """ p1 , q1 и q2 лежат на одной прямой и q2 лежит на прямой p1q1 """
    if (o2 == "collinear") and on_segment(p1, q2, q1):
        return True

    """ p2 , q2 и p1 лежат на одной прямой и p1 лежит на прямой p2q2 """
    if (o3 == "collinear") and on_segment(p2, p1, q2):
        return True

    """ p2 , q2 и q1 лежат на одной прямой и q1 лежит на прямой p2q2 """
    if (o4 == "collinear") and on_segment(p2, q1, q2):
        return True

    return False


"""
    Функция принимает список ассоциированных списков с координатами точек многоугольника
    и точки отрезка, с которым надо проверить взаимное расположение: 
    возвращает bool флаг: True - есть одна или две общих точки,
    False - нет общих точек (т.е. нет пересечения)
"""


def polygons_and_segment(polygon: list[dict], point_a: tuple[float, float], point_b: tuple[float, float]) -> bool:
    """Проверяем с каждым отрезком, составляющим многоугольник"""
    for i in range(len(polygon) - 1):
        p2 = (polygon[i].get('x'), polygon[i].get('y'))
        q2 = (polygon[i + 1].get('x'), polygon[i + 1].get('y'))
        if intersection_segments(point_a, point_b, p2, q2):
            return True
    return False


"""
    Функция принимает две точки: кортежи с координатами концов вектора;
    Сначала аргументом подается начало вектора, затем конец;
    Возвращает кортеж с координатами вектора, составленного на этих точках
"""


def vector(point_a: tuple[float, float], point_b: tuple[float, float]) -> tuple:
    a_x = point_a[0]
    a_y = point_a[1]
    b_x = point_b[0]
    b_y = point_b[1]
    c_x = b_x - a_x
    c_y = b_y - a_y
    c = (c_x, c_y)
    return c


"""
    Функция принимает кортеж с координатами вектора; 
    возвращает кортеж с координатами вектора ортогонального данному
"""


def normal_vector(vector_a: tuple[float, float]) -> tuple:
    a_x = vector_a[0]
    a_y = vector_a[1]
    if a_x == 0:
        vector_b = (1, 0)
        return vector_b
    b_x = -(a_y / a_x)
    b_y = 1.0
    vector_b = (b_x, b_y)
    return vector_b


"""
    Принимает кортеж с координатами вектора; 
    Возвращает длину вектора
"""


def length_vector(vec: tuple[float, float]) -> float:
    return np.sqrt(vec[0] ** 2 + vec[1] ** 2)


"""
    Функция принимает кортежи с координатами трех векторов: v, a и b 
    Возвращает bool флаг: False - векторы a и b лежат по разные стороны от вектора v;
    True - во всех остальных случаях (один из векторов коллинеарен вектору v, 
    другой лежит по любую сторону от вектора v; оба вектора лежат по одну сторону от вектора v) 
"""


def orientation_vectors(v: tuple[float, float], a: tuple[float, float], b: tuple[float, float]) -> bool:
    normal = normal_vector(v)
    len_a = length_vector(a)
    len_b = length_vector(b)
    len_norm = length_vector(normal)
    cos_1 = (normal[0] * a[0] + normal[1] * a[1]) / (len_norm * len_a)
    cos_2 = (normal[0] * b[0] + normal[1] * b[1]) / (len_norm * len_b)
    if (cos_1 * cos_2) < 0:
        return False
    return True


"""
    Функция принимает список ассоциированных списков с координатами точек многоугольника
    и кортеж с координатами точки, через которую проходит касательная к многоугольнику; 
    Возвращает кортеж с id двух точек касания (вершины многоугольника) или id двух  вершин, 
    составляющих ребро, через которое проходит касательная
"""


def tangent(polygon: list[dict], point: tuple[float, float]) -> tuple:
    flag = 0
    tangents = [0, 0]
    for i in range(len(polygon)):
        if flag == 2:
            break
        if i == len(polygon) - 1:
            begin = (polygon[i].get('x'), polygon[i].get('y'))
            end_1 = (polygon[0].get('x'), polygon[0].get('y'))
            end_2 = (polygon[i - 1].get('x'), polygon[i - 1].get('y'))

        else:
            begin = (polygon[i].get('x'), polygon[i].get('y'))
            end_1 = (polygon[i + 1].get('x'), polygon[i + 1].get('y'))
            end_2 = (polygon[i - 1].get('x'), polygon[i - 1].get('y'))

        vector_v = vector(point, begin)
        vector_a = vector(begin, end_1)
        vector_b = vector(begin, end_2)
        if orientation_vectors(vector_v, vector_a, vector_b):
            tangents[flag] = polygon[i].get('id')
            flag += 1
    tangents = tuple(tangents)
    return tangents


"""
    Функция принимает незамкнутый маршрут в виде списка из кортежей с координатами точек 
    и возвращает длину этого маршрута
"""


def length_route(route: list) -> float:
    length = 0
    for i in range(len(route) - 1):
        point1 = route[i]
        point2 = route[i + 1]
        vec = vector(point1, point2)
        length += length_vector(vec)
    return length


"""
    Функция принимает список ассоциированных списков с координатами вершин многоугольника, 
    координаты точек отрезка ab, пересекающего многоугольник и пару точек касания p и q;
    p - id точки касания для точки a, q - id точки касания для точки b;
    Возвращает для данных точек касания минимальный маршрут route (список с кортежами точек прохода)
"""


def processing_route(polygon: list[dict], a: tuple[float, float],
                     b: tuple[float, float], p: int, q: int) -> list:
    route1 = []
    route2 = []
    route1.append(a)
    route2.append(a)
    """Продублируем список с координатами, чтобы проход по вершинам многоугольника был возможен и по часовой и против"""
    new_polygon = polygon * 2
    for i in range(len(new_polygon) - 1, -1, -1):
        if new_polygon[i].get('id') == p and p == q:
            point = (new_polygon[i].get('x'), new_polygon[i].get('y'))
            route1.append(point)
            break
        if new_polygon[i].get('id') == p and p != q:
            point = (new_polygon[i].get('x'), new_polygon[i].get('y'))
            route1.append(point)
            if new_polygon[i].get('id') == q:
                break

    for i in range(0, len(new_polygon), 1):
        if new_polygon[i].get('id') == p and p == q:
            point = (new_polygon[i].get('x'), new_polygon[i].get('y'))
            route2.append(point)
            break
        if new_polygon[i].get('id') == p and p != q:
            point = (new_polygon[i].get('x'), new_polygon[i].get('y'))
            route2.append(point)
            if new_polygon[i].get('id') == q:
                break
    route1.append(b)
    route2.append(b)
    if length_route(route1) >= length_route(route2):
        return route2
    else:
        return route1


"""
    Функция принимает список ассоцированных списков из координат вершин многоугольника, 
    id вершин tangents, через которые проходят касательные и концы отрезка ab, пересекающего многоугольник; 
    Возвращает список из кортежей координат точек, по которым длина обходного маршрута минимальна и длину этого маршута; 
"""


def shortest_route(polygon: list[dict], tangents: tuple, a: tuple[float, float], b: tuple[float, float]) -> tuple:
    route = [0, 0, 0, 0]
    route[0] = processing_route(polygon, a, b, tangents[0], tangents[2])
    route[1] = processing_route(polygon, a, b, tangents[0], tangents[3])
    route[2] = processing_route(polygon, a, b, tangents[1], tangents[2])
    route[3] = processing_route(polygon, a, b, tangents[1], tangents[3])
    min_route = route[0]
    min_len = length_route(route[0])
    for i in range(1, len(route)):
        leng = length_route(route[i])
        if leng < min_len:
            min_len = leng
            min_route = route[i]
    res = (min_route, min_len)
    return res


"""
    Функция принимает данные всех точек, данные о неприемлемом рельефе и матрицу расстояний matrix;
    в ходе работы преобразует матрицу расстояний между точками исходя из рельефа;
    возвращает словарь с обходными маршрутами detour_routes:
    detour_routes = {key: value, ...]
    key: кортеж из id двух точек, между которыми имеется неприемлемый рельеф,
    value: список с данными для обходного маршрута из точек, по которым нужно пройтись
"""


def relief(data_points, data_polygons, matrix):
    detour_routes = {}
    for k in range(len(data_polygons)):
        for i in range(1, len(data_points) + 1):
            for j in range(i + 1, len(data_points) + 1):
                a_id = (data_points[i - 1]).get('id')
                a_x = (data_points[i - 1]).get('x')
                a_y = (data_points[i - 1]).get('y')
                b_id = (data_points[j - 1]).get('id')
                b_x = (data_points[j - 1]).get('x')
                b_y = (data_points[j - 1]).get('y')
                """Проверка на общие точки между отрезком и многоугольником"""
                if polygons_and_segment(data_polygons[k], (a_x, a_y), (b_x, b_y)):
                    """Получение двух точек касания для каждого из обоих концов отрезка"""
                    tangents = tangent(data_polygons[k], (a_x, a_y)) + tangent(data_polygons[k], (b_x, b_y))
                    """Определяем длину наименьшего пути и способ прохода по дуге окружности"""
                    data_route = shortest_route(data_polygons[k], tangents, (a_x, a_y), (b_x, b_y))
                    route = data_route[0]
                    len_route = data_route[1]
                    matrix[i][j] = len_route
                    matrix[j][i] = len_route
                    detour_routes[(a_id, b_id)] = route
                    detour_routes[(b_id, a_id)] = route
    return detour_routes
