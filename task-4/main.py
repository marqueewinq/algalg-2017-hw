'''
    Solution for https://stepik.org/lesson/59290/step/4?unit=36810
'''

import numpy as np

#
# interfaces required to operate on $Z_2$ field
#
def z2(arr):
    return np.vectorize(lambda x: x % 2)(arr)


def dot(matA, matB):
    return np.dot(matA, matB) % 2


def inv(mat):
    return np.linalg.inv(mat) % 2


def grow_to_exp(mat, base):
    '''
        Expands the `mat` to size which matches the exp of base.
        Additional rows are identity rows.
    '''
    Y, X = mat.shape
    n = int(2 ** np.ceil(np.log(mat.shape[0]) / np.log(base)))
    result = np.diag([1.] * n)
    result[:Y, :X] = mat
    return result


def block_2x2(top_left, top_right, bot_left, bot_right):
    '''
    np.block was introduced in NumPy 1.13
    but it seems that Stepik still has NumPy<=1.12
    .
    .
    .
    What a shame
    '''
    top = np.concatenate([top_left, top_right], axis = 1)
    bot = np.concatenate([bot_left, bot_right], axis = 1)
    return np.concatenate([top, bot], axis = 0)


def read_matrix():
    mat = [list(map(int, input().split()))]
    n = len(mat[0])
    for _ in range(n - 1):
        row = list(map(int, input().split()))
        mat.append(row)
    return np.array(mat).astype(np.float32)


def get_permutation_mat(first, second, size = None):
    '''
        Returns permutation matrix, which swaps rows `first` and `second`
    '''
    if size is None:
        size = max(first, second)
    diag = np.diag([1.] * size).astype(np.float32)
    diag[[first, second]] = diag[[second, first]]
    return diag


def lup(mat):
    '''
        Returns LUP-decomposition

        Based on "Data Structures and Algorithms" by Aho et al.
    '''
    Y, X = mat.shape
    
    if Y == 1:
        left = np.array([1]).reshape(1, 1)
        first_nonzero_row_index = np.nonzero(np.any(mat, axis = 0))[0][0]
        perm = get_permutation_mat(0, first_nonzero_row_index, size = X)
        return left, dot(mat, perm), perm # as inverse(perm) == perm

    low = mat[:Y // 2, :]
    high = mat[Y // 2:, :]

    left_1, mid_1, right_1 = lup(low)

    # frankly i don't know how to name those matrices according to their meaning
    # so i will just call them arbitrarily to increase verbosity
    dirac = dot(high, inv(right_1))
    einstein = mid_1[:, :Y // 2]
    faraday = dirac[:, :Y // 2]
    
    godel = dirac - dot(dot(faraday, inv(einstein)), mid_1)
    columns_we_need = X - Y // 2
    gauss = godel[:, godel.shape[1] - columns_we_need:]
    left_2, mid_2, right_2 = lup(gauss)

    perm_3 = np.diag([1.] * X)
    perm_3[X - right_2.shape[0]:, X - right_2.shape[1]:] = right_2
    
    hilbert = dot(mid_1, inv(perm_3))

    zeros = np.zeros((Y // 2, Y // 2)).astype(np.float32)
    left = block_2x2(left_1, zeros, dot(faraday, inv(einstein)), left_2)
    assert left.shape == (Y, Y)
    hilbert_left = hilbert[:, :X // 2] 
    hilbert_right = hilbert[:, X // 2:]
    mid = block_2x2(hilbert_left, hilbert_right, zeros, mid_2)
    assert mid.shape == (Y, X)
    right = dot(perm_3, right_1)
    return left, mid, right


def print_format(mat):
    return "\n".join([" ".join(map(str, map(z2, map(int, row)))) for row in mat.tolist()])


def main():
    mat = read_matrix()
    assert mat.shape[0] == mat.shape[1]
    n = mat.shape[0]
    results = lup(grow_to_exp(mat, base = 2))
    for result in results:
        print(print_format(result[:n, :n]))

if __name__ == '__main__':
    main()

