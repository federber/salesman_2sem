import matplotlib.pyplot as plt
import data_reading
import visualisation
import logging
import json
import forbidden_zone
import salesman
import polygons

logging.basicConfig(level=logging.INFO, filename='trajectory_log.log', filemode='w')

logging.info("Началось считывание данных из файла")
with open('data2.json', 'r', encoding='utf-8') as f:
    read_data = json.load(f)
logging.info("Завершилось считывание данных из файла")
data_points = read_data.get('data_points')
air_corridor = read_data.get('air_corridor')
data_pvo = read_data.get('forbidden_zone')
data_relief = read_data.get('relief')

""" Получение матрицы расстояний """
matrix = data_reading.air_corridor(air_corridor, data_reading.filling_data(data_points))

"""Получение обходных маршрутов с учетом ЗД ПВО"""
detour_routes_circle = forbidden_zone.forbidden_zone(data_points, data_pvo, matrix)
"""Получение обходных маршрутов с учетом рельефа"""
detour_routes_relief = polygons.relief(data_points, data_relief, matrix)

""" 
    Функция salesman принимает матрицу расстояний и количество БПЛА;
    Возвращает массив ways из id точек, полученных методом Литтла; 
    
"""
ways = salesman.salesman(start_matrix=matrix, numb_of_salesmen=3)
print(ways)
"""Словарь с кодами цветов формата RGB для разных БПЛА"""
colors = {0: '#0000FF', 1: '#FFBB00', 2: '#00FFFF', 3: '#FF00FF', 4: '#808000',
          5: '#191970', 6: '#800080', 7: '#8B4513', 8: '#000000', 9: '#FFA500'}

""" Визуализация траектории и получение файла формата png """
axes = plt.gca()
axes.set_aspect("equal")
visualisation.visualisation_pvo(axes, data_pvo)
visualisation.visualisation_air_corridors(air_corridor, read_data)
visualisation.visualisation_relief(axes, data_relief)

for i in range(len(ways)):
    color = colors.get(i)
    visualisation.visualisation(axes, ways[i], data_points, detour_routes_circle, detour_routes_relief, color)

plt.show()
plt.savefig('trajectory.png')
