import numpy as np
np.set_printoptions(precision=4, suppress=True)


def read_edges():
    """
        Reads edges as declared in task
    """
    n_edges = int(input())
    edges = []
    names = []
    for _ in range(n_edges):
        src, dst = map(int, input().split())
        if src not in names:
            names.append(src)
        if dst not in names:
            names.append(dst)
        edges.append([names.index(src), names.index(dst)])
    return edges, names


def count_degrees(edges):
    degs = {}
    max_edge_index = 0
    for edge in edges:
        src, dst = edge
        max_edge_index = max(max_edge_index, src, dst)
        degs[src] = degs.get(src, 0) + 1
        degs[dst] = degs.get(dst, 0) + 1
    return [value for vtx, value in degs.items()]


def get_laplacian(edges, degs):
    lapl = np.diag(degs)
    for edge in edges:
        src, dst = edge
        lapl[src][dst] = -1
        lapl[dst][src] = -1
    return lapl.astype(int)


def get_cut_density(cut, edges, n_vtx):
    interlace_count = 0
    for edge in edges:
        src, dst = edge
        if bool(src in cut) != bool(dst in cut):
            interlace_count += 1

    return interlace_count * n_vtx * 1. / len(cut) / (n_vtx - len(cut))


def repr(names, keys):
    return " ".join(map(str, sorted(np.array(names)[keys])))


def main():
    edges, names = read_edges()
    print ("edges: {}".format(edges))
    print ("names: {}".format(names))
    degs = count_degrees(edges)
    print ("degrees: {}".format(degs))

    lapl = get_laplacian(edges, degs)
    print ("laplacian: \n{}".format(lapl))
    print ("lapl det: {}".format(np.linalg.det(lapl)))

    values, vectors = np.linalg.eigh(lapl)
    print ("values: {}".format(values))
    print ("vectors: \n{}".format(vectors))

    fiedler_arg = np.argsort(values)[1]
    print ("fiedler value: {}".format(values[fiedler_arg]))
    fielder_argsorted = np.argsort(-vectors[:, fiedler_arg])
    print ("fielder_argsorted: {}".format(fielder_argsorted))
    densities = []
    for k_count in range(len(fielder_argsorted) - 1):
        cut = fielder_argsorted[:k_count + 1]
        densities.append(get_cut_density(cut, edges, len(fielder_argsorted)))

    print ("densities: {}".format(densities))
    min_density = np.min(densities)
    keys = None
    for k_count in range(len(densities)):
        if densities[k_count] == min_density:
            new_keys = fielder_argsorted[:k_count + 1]
            if keys is None or (len(keys) >= len(new_keys) and repr(names, keys) > repr(names, new_keys)):
                keys = new_keys
    return repr(names, keys)


if __name__ == '__main__':
    print(main())