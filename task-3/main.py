"""
    Solution for https://stepik.org/lesson/59290/step/3?unit=36810
"""
import sys
import numpy as np

def read_edges():
    """
        Reads the graph from input into linklist
        Returns:
            `list` : graph's repr as a linklist
    """
    with sys.stdin as f:
        n = int(f.readline())
        edges = []

        sz = 0
        for _ in range(n):
            a, b = map(int, f.readline().split(' '))
            sz = max(sz, a, b)
            edges.append((a, b,))

        linklist = [[] for _ in range(sz + 1)]
        for a, b in edges:
            linklist[a].append(b)
            linklist[b].append(a)
    return linklist


def collect_cycle(linklist):
    """
        Basically a pretty interface for dfs.
        Args:
            linklist : `list of lists` : a graph repr
        Returns:
            `bool` : Is there a cycle?
            `list` : Arbitrary cycle as a list of vertex indices
    """
    found, cycle = _walks_until_cycle(0, linklist, [False for _ in range(len(linklist))])
    return found > 0, cycle


def _walks_until_cycle(v, linklist, used, prev = None):
    """
        Dfs itself.
        Args:
            v : `int` : current vertex
            linklist : `list of lists` : a graph repr
            used : `list of bool` : list for marking visited vertices
            prev : `int` : current vertex's predecessor
        Returns:
            _found : `int` : one of:
                0 if there is no cycle forward
                1 if there is cycle, and we are on it
                2 if we have found the cycle, stored it in _cycle,
                  so we just need to return it straight to the top
            _cycle : `list` : cycle (or it's tail) as a list of vertex indices

    """
    if used[v]:
        return 1, [v,]
    used[v] = True

    for nxt in linklist[v]:
        if prev is not None and nxt == prev:
            continue
        found, collected = _walks_until_cycle(nxt, linklist, used, prev = v)
        if found == 1:
            # walk detected, that we are on a cycle; tracing it backwards
            if v in collected:
                # found snake's head end!
                return 2, collected
            else:
                # collect cycle, go backwards
                return 1, collected + [v,]
        elif found == 2:
            # found cycle, return it straight to the top
            return 2, collected
    return 0, None


def force_planarity(linklist, fixed_vtx, field):
    """
        Solves linear system for graph's embedding.
        Args:
            linklist : `list of lists` : a graph repr
            fixed_vtx : `list` : list of vertices with fixed coordinates
            field : `dict` : map of vertex -> (x, y) coordinates
        Returns:
            `list` : solution, list of (x, y) coordinates
    """
    n = len(linklist)
    free_vtx = [i for i in range(n) if i not in fixed_vtx]

    def value(i, j):
        """
            Provider of matrice values
        """
        if i in fixed_vtx:
            if j in fixed_vtx:
                return float(i == j)
        else:
            if i == j:
                return -float(len(linklist[i]))
            if j in linklist[i]:
                return 1.
        return 0.

    mat = [[value(i, j) for j in range(n)] for i in range(n)]

    b_x = [0. for _ in range(n)]
    b_y = [0. for _ in range(n)]
    for fi in fixed_vtx:
        b_x[fi], b_y[fi] = field[fi]

    return np.linalg.solve(mat, b_x), np.linalg.solve(mat, b_y)

def main():
    # read graph
    linklist = read_edges()

    # find arbitrary cycle
    found_cycle, collected_cycle = collect_cycle(linklist = linklist)
    assert found_cycle, 'graph is a tree'

    # embed it
    field = {}
    for i, vtx in enumerate(collected_cycle):
        if i < len(collected_cycle) // 2:
            y = 0.
        else:
            y = 1.
        x = float(i % (len(collected_cycle) // 2 + 1))
        field[vtx] = (x, y,)

    # embed everything else
    xs, ys = force_planarity(linklist, collected_cycle, field)
    for i, (x, y) in enumerate(zip(xs, ys)):
        if i not in field:
            field[i] = [x, y]

    for vtx, (x, y) in field.items():
        print("{vtx} {x:.4f} {y:.4f}".format(vtx = vtx, x = x, y = y))


if __name__ == '__main__':
    main()
