"""
    Solution for https://stepik.org/lesson/59290/step/6?unit=36810
"""
import numpy as np

def read():
    """
        Reads std input.
    """
    p_teleport = float(input())
    n_total = int(input())
    linklist = {}
    hashes = {}
    for _ in range(n_total):
        str_a, str_b = input().split(' ')
        for str_id in [str_a, str_b]:
            if str_id in hashes:
                int_id = hashes[str_id]
            else:
                int_id = len(hashes)
                hashes[str_id] = int_id
                linklist[int_id] = []

        linklist[hashes[str_a]] += [hashes[str_b]]

    return p_teleport, hashes, linklist


def transition(linklist):
    """
        Returns pure transition matrix of graph repr-ed by linklist.
    """
    n_total = len(linklist)
    mat = np.zeros((n_total, n_total), dtype=float)
    for source in linklist:
        if len(linklist[source]) == 0:
            # fix for dangling nodes
            mat[:, source] = [1. / n_total for _ in range(n_total)]
            continue

        transition_fraction = 1. / len(linklist[source])
        for target in linklist[source]:
            mat[target, source] = transition_fraction
    return mat


def iterate_over(mat):
    """
        It was boring to use np.linalg.solve or np.linalg.eigh,
        so i just iterated over.
    """
    n_total = mat.shape[0]
    vec = np.ones((n_total, 1)) * 1. / n_total
    prev = np.zeros((n_total, 1))
    while np.any(prev != vec):
        prev = vec
        vec = np.dot(mat, vec)
    return vec.reshape(n_total).tolist()


def main():
    """
        As for http://www.math.cornell.edu/~mec/Winter2009/RalucaRemus/Lecture3/lecture3.html
        Constructs Page-Brin matrix M = transition matrix * (1 - p) + [[1/n]] * p and finds it
        eigenvalue, which is converted into pageranks.
    """
    p_teleport, hashes, linklist = read()
    n_total = len(linklist)

    transition_mat = transition(linklist)
    ones = np.ones((n_total, n_total), dtype=float) * 1. / n_total
    page_brin_mat = transition_mat * (1. - p_teleport) + ones * p_teleport
    pageranks = iterate_over(page_brin_mat)

    for str_id, int_id in hashes.items():
        print('{} {}'.format(str_id, pageranks[int_id]))

if __name__ == '__main__':
    main()
