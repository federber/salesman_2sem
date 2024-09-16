import matplotlib.patches
import matplotlib.path
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D


def getting_cords(points, read_data):
    """получает список из id точек, полученных методом Литтла;
    возвращает кортеж из двух списков с координатами точек(x, y)"""
    id1 = points[0]
    id2 = points[1]
    for i in range(len(read_data)):
        if (read_data[i]).get('id') == id1:
            x1 = (read_data[i]).get('x')
            y1 = (read_data[i]).get('y')
        if (read_data[i]).get('id') == id2:
            x2 = (read_data[i]).get('x')
            y2 = (read_data[i]).get('y')
    res = (x1, y1, x2, y2)
    return res


def getting_air_cords(data_corridor, read_data):
    """Получает список data_corridor из id КТ для воздушных коридоров
    и сопоставляет им координаты из списка с данными точек read_data,
    возвращает кортеж из двух списков с координатами точек(x, y) """
    x_cords = []
    y_cords = []
    i = 0
    while i < len(data_corridor):
        for j in range(len(read_data)):
            if (read_data[j]).get('id') == (data_corridor[i]).get('id1'):
                x_cords.append((read_data[j]).get('x'))
                y_cords.append((read_data[j]).get('y'))
            if (read_data[j]).get('id') == (data_corridor[i]).get('id2'):
                x_cords.append((read_data[j]).get('x'))
                y_cords.append((read_data[j]).get('y'))
        i += 1
    return x_cords, y_cords


"""
    Функция рисует прямую между двумя точками, заданными кортежем tuples(x0, y0, x1, y1)
"""


def draw_line(axes, tuples, color):
    x0 = tuples[0]
    y0 = tuples[1]

    x1 = tuples[2]
    y1 = tuples[3]

    line = Line2D([x0, x1], [y0, y1], color=color, linewidth=2)
    axes.add_line(line)


"""
    Функция рисует меньшую дугу окружности между двумя точками на этой окружности 
    дуга задается кортежем tuple ((c_x, c_y), r, r, tetha_1, tetha_2)
"""


def draw_arc(axes, tuples, color):
    arc_cords = tuples[0]
    """
        Умножаем tuples[1] и tuples[2], т.е. радиусы, на 2, 
        потому что функция задается удвоенными большой и малой полуосью
    """
    arc_width = tuples[1] * 2
    arc_height = tuples[2] * 2
    arc_theta1 = tuples[3]
    arc_theta2 = tuples[4]

    arc = matplotlib.patches.Arc(arc_cords,
                                 arc_width,
                                 arc_height,
                                 theta1=arc_theta1,
                                 theta2=arc_theta2,
                                 color=color,
                                 linewidth=2)
    axes.add_patch(arc)


"""
    Функция рисует окружность(в нашем случае ЗД ПВО);
    каждая окружность задается кортежем, состоящем из координат центра и радиуса(в км)
"""


def draw_circle(axes, tuples):
    c_x = tuples[0]
    c_y = tuples[1]
    r = tuples[2]
    circle = matplotlib.patches.Circle((c_x, c_y),
                                       radius=r,
                                       fill=True,
                                       color='r')
    axes.add_patch(circle)


def draw_polygons(axes, route: list):
    polygon = matplotlib.patches.Polygon(route,
                                         color='r')
    axes.add_patch(polygon)


"""
    Функция рисует кратчайший обходной маршрут между двумя точками через многоугольник 
    с непреодолимым рельефом, маршрут задается списком из кортежей координат точек
"""


def draw_path_on_polygon(axes, route: list, color):
    polygon = matplotlib.patches.Polygon(route,
                                         fill=False,
                                         closed=False,
                                         color=color,
                                         linewidth=2)
    axes.add_patch(polygon)


"""Отрисовка воздушных коридоров"""


def visualisation_air_corridors(data_corridor, read_data):
    cords_air_corridor = getting_air_cords(data_corridor, read_data.get('data_points'))
    for line in range(0, len(cords_air_corridor[0]), 2):
        """Последовательно рисуем воздушные коридоры между парами КТ"""
        plt.plot(cords_air_corridor[0][line:line + 2], cords_air_corridor[1][line:line + 2], color='red', linewidth=2)


"""Отрисовка красными кругами ЗД ПВО"""


def visualisation_pvo(axes, data_pvo):
    for i in range(len(data_pvo)):
        x = data_pvo[i].get('x')
        y = data_pvo[i].get('y')
        r = data_pvo[i].get('r')
        draw_circle(axes, (x, y, r / 1000))


"""Отрисовка красными многоугольниками неприемлемого рельефа"""


def visualisation_relief(axes, data_relief):
    for i in range(len(data_relief)):
        relief = data_relief[i]
        route = []
        for j in range(len(relief)):
            x = relief[j].get('x')
            y = relief[j].get('y')
            point = (x, y)
            route.append(point)
        draw_polygons(axes, route)


"""
    Функция visualisation отрисовывает путь, 
    включая обходные маршруты, конкретного коммивояжера
"""


def visualisation(axes, optimal_way, read_data, detour_routes_circle, detour_routes_relief, color):
    plt.xlim(0, 10)
    plt.ylim(0, 10)
    plt.grid()  # отрисовка сетки

    """Отрисовка маршрута коммивояжера"""
    for i in range(len(optimal_way) - 1):
        point_1 = optimal_way[i]
        point_2 = optimal_way[i + 1]
        points = (point_1, point_2)
        if points in detour_routes_circle:
            """рисуем касательную, дугу, касательную"""
            current_route = detour_routes_circle.get(points)
            line_1 = current_route.get('line_1')
            line_2 = current_route.get('line_2')
            arc = current_route.get('arc')
            draw_line(axes, line_1, color)
            draw_line(axes, line_2, color)
            draw_arc(axes, arc, color)
        elif points in detour_routes_relief:
            current_route = detour_routes_relief.get(points)
            draw_path_on_polygon(axes, current_route, color)
        else:
            cords = getting_cords(points, read_data)
            draw_line(axes, cords, color)
