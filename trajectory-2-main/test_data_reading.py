import data_reading
import numpy as np


def test_filling_data():
    """Тесты проводятся на значениях точек из разных числовых множеств: вещественные, целые, иррациональные и нули"""
    arr1 = [{'id': 1, 'x': 1.4, 'y': 6.7}, {'id': 2, 'x': 2.8, 'y': 3.33}]
    arr2 = [{'id': 1, 'x': 0.0, 'y': 0.0}, {'id': 2, 'x': 10.0, 'y': 10.0}, {'id': 3, 'x': 17.0, 'y': 7.0}]
    arr3 = [{'id': 1, 'x': 0.0, 'y': 0.0}, {'id': 2, 'x': 0.0, 'y': 0.0}, {'id': 3, 'x': 0.0, 'y': 0.0}]
    arr4 = [{'id': 1, 'x': (np.sqrt(2)), 'y': (np.sqrt(3))}, {'id': 2, 'x': (np.sqrt(4)), 'y': (np.sqrt(5))},
            {'id': 3, 'x': (np.sqrt(6)), 'y': (np.sqrt(7))}]

    matrix1 = [[np.inf, 1, 2],
               [1, np.inf, np.sqrt(49 / 25 + (337 / 100) ** 2)],
               [2, np.sqrt(49 / 25 + (337 / 100) ** 2), np.inf]]
    matrix2 = [[np.inf, 1, 2, 3],
               [1, np.inf, 10 * np.sqrt(2), 13 * np.sqrt(2)],
               [2, 10 * np.sqrt(2), np.inf, np.sqrt(58)],
               [3, 13 * np.sqrt(2), np.sqrt(58), np.inf]]
    matrix3 = [[np.inf, 1, 2, 3],
               [1, np.inf, 0, 0],
               [2, 0, np.inf, 0],
               [3, 0, 0, np.inf]]
    matrix4 = [[np.inf, 1, 2, 3],
               [1, np.inf, np.sqrt(14 - 4 * np.sqrt(2) - 2 * np.sqrt(15)),
                np.sqrt(18 - 4 * np.sqrt(3) - 2 * np.sqrt(21))],
               [2, np.sqrt(14 - 4 * np.sqrt(2) - 2 * np.sqrt(15)), np.inf,
                np.sqrt(22 - 4 * np.sqrt(6) - 2 * np.sqrt(35))],
               [3, np.sqrt(18 - 4 * np.sqrt(3) - 2 * np.sqrt(21)),
                np.sqrt(22 - 4 * np.sqrt(6) - 2 * np.sqrt(35)), np.inf]]
    accuracy = 0.000001
    """задаем точность accuracy (параметр atol в методе allclose),
    с которой будут сравниваться элементы матриц"""
    assert np.allclose(data_reading.filling_data(arr1), matrix1, atol=accuracy) == True  # noqa: E712
    assert np.allclose(data_reading.filling_data(arr2), matrix2, atol=accuracy) == True  # noqa: E712
    assert np.allclose(data_reading.filling_data(arr3), matrix3, atol=accuracy) == True  # noqa: E712
    assert np.allclose(data_reading.filling_data(arr4), matrix4, atol=accuracy) == True  # noqa: E712
