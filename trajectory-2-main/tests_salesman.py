import salesman as sm

M = float('inf')


def test_salesman():
    assert_matr = [[0, 1, 2, 3, 4, 5],
                   [1, 0, 20, 18, 12, 8],
                   [2, 5, 0, 14, 7, 11],
                   [3, 12, 18, 0, 6, 11],
                   [4, 11, 17, 11, 0, 12],
                   [5, 5, 5, 5, 5, 0]]
    assert sm.salesman(assert_matr, 1) == [[1, 5, 3, 4, 2, 1]]
    assert_matr = [[0, 1, 2, 3, 4],
                   [1, 0, 8, 4, 10],
                   [2, 8, 0, 7, 5],
                   [3, 4, 7, 0, 3],
                   [4, 10, 5, 3, 0]]
    assert sm.salesman(assert_matr, 1) == [[1, 3, 4, 2, 1]]

    assert_matr = [[0, 1, 2, 3, 4, 5, 6],
                   [1, 0, 10, 5, 9, 16, 8],
                   [2, 6, 0, 11, 8, 18, 19],
                   [3, 7, 13, 0, 3, 4, 14],
                   [4, 5, 9, 6, 0, 12, 17],
                   [5, 5, 4, 11, 6, 0, 14],
                   [6, 17, 7, 12, 13, 16, 0]]
    assert sm.salesman(assert_matr, 1) == [[1, 3, 5, 6, 2, 4, 1]] or sm.salesman(assert_matr, 1) == [
        [1, 6, 2, 4, 3, 5, 1]]

    sq = 2 * 3 ** 0.5
    assert_matr = [[0, 7, 8, 9, 10],
                   [7, 0, 2, 2, 2],
                   [8, 2, 0, sq, sq],
                   [9, 2, sq, 0, sq],
                   [10, 2, sq, sq, 0]]
    assert sm.salesman(assert_matr, 3) == [[7, 10, 7], [7, 9, 7], [7, 8, 7]]
    assert sm.salesman(assert_matr, 1) == [[7, 8, 10, 9, 7]]
    assert sm.salesman(assert_matr, 2) == [[7, 8, 10, 7], [7, 9, 7]]


def test_reduct():
    assert_matr = [[0, 20, 18, 12, 8],
                   [5, 0, 14, 7, 11],
                   [12, 18, 0, 6, 11],
                   [11, 17, 11, 0, 12],
                   [5, 5, 5, 5, 0]]
    assert sm.Matrix(assert_matr).reduct() == 35
    assert_matr = [[0, 8, 4, 10],
                   [8, 0, 7, 5],
                   [4, 7, 0, 3],
                   [10, 5, 3, 0]]
    assert sm.Matrix(assert_matr).reduct() == 18


def test_zero_pow():
    assert_matr = [[M, 12, 10, 4, 0],
                   [0, M, 9, 2, 6],
                   [6, 12, M, 0, 5],
                   [0, 6, 0, M, 1],
                   [0, 0, 0, 0, M]]
    assert sm.Matrix(assert_matr).zero_pow() == [4, 1]


def test_delete_by_name():
    assert_matr = [[M, 12, 10, 4, 0],
                   [0, M, 9, 2, 6],
                   [6, 12, M, 0, 5],
                   [0, 6, 0, M, 1],
                   [0, 0, 0, 0, M]]
    matrix = sm.Matrix(assert_matr)
    matrix.delete_by_name([1, 3])
    assert matrix.rows_names == [0, 2, 3, 4] and matrix.cols_names == [0, 1, 2, 4]
    matrix.delete_by_name([2, 4])
    assert matrix.rows_names == [0, 3, 4] and matrix.cols_names == [0, 1, 2]


def test_make_inf():
    assert_matr = [[M, 12, 10, 4, 0],
                   [0, M, 9, 2, 6],
                   [6, 12, M, 0, 5],
                   [0, 6, 0, M, 1],
                   [0, 0, 0, 0, M]]
    matr = sm.Matrix(assert_matr)
    matr.make_inf([2, 3])
    assert matr.matrix[2][3] == M


def test_find_min_in_cutted():
    branches = [sm.Plan(2, [1, 2], 1, []), sm.Plan(3, [1, 2], 1, []), sm.Plan(1, [100, 100], 1, [1, 2])]
    assert sm.find_min_in_cutted(branches) == sm.Plan(1, [100, 100], 1, [1, 2])


def test_create_path():
    prev_branches = []
    prev_branches.append(sm.Edge([1, 2], True, 1))
    prev_branches.append(sm.Edge([5, 3], True, 2))
    prev_branches.append(sm.Edge([3, 1], True, 3))
    prev_branches.append(sm.Edge([2, 4], True, 4))
    prev_branches.append(sm.Edge([4, 5], True, 5))
    prev_branches.append(sm.Edge([1, 4], False, 6))

    plan = sm.Plan(prev_branches=prev_branches)
    assert sm.create_path(plan) == [[1, 2, 4, 5, 3, 1]]


def test_normalize():
    assert sm.normalize([[5, 4, 3, 2, 1, 5]]) == [[1, 5, 4, 3, 2, 1]]
    assert sm.normalize([[3, 5, 1, 3], [6, 2, 1, 6], [4, 1, 4]]) == [[1, 3, 5, 1], [1, 6, 2, 1], [1, 4, 1]]


def test_min_wtht_ind():
    assert sm.min_wtht_ind([3, 4, 0, 1, 3], 2) == 1


def test_make_diag_inf():
    assert_matr = [[0, 12, 10, 4, 0],
                   [0, 0, 9, 2, 6],
                   [6, 12, 0, 0, 5],
                   [0, 6, 0, 0, 1],
                   [0, 0, 0, 0, 0]]
    expected_res = [[M, 12, 10, 4, 0],
                    [0, M, 9, 2, 6],
                    [6, 12, M, 0, 5],
                    [0, 6, 0, M, 1],
                    [0, 0, 0, 0, M]]
    assert_matrix = sm.Matrix(assert_matr)
    assert_matrix.make_diag_inf()
    exp_matrix = sm.Matrix(expected_res)
    assert assert_matrix == exp_matrix
