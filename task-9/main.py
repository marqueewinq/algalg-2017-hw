"""
    Solution for https://stepik.org/lesson/59290/step/9?unit=36810
"""
import numpy as np

def generate_legendre(prime):
    """
        Generates legendre symbol for given prime
    """
    legendre = [-1] * prime
    legendre[0] = 0
    for i in range(1, prime // 2 + 1):
        legendre[i * i % prime] = 1
    return legendre

def hadamard(n_dim):
    """
        Construct hadamar matrice under cetrain conditions on n_dim
    """
    legendre = generate_legendre(n_dim - 1)

    t_dashed = []
    for index_a in range(n_dim - 1):
        row = []
        for index_b in range(n_dim - 1):
            row.append(legendre[index_a - index_b])
        t_dashed.append(row)

    for diag_i in range(n_dim - 1):
        t_dashed[diag_i][diag_i] = -1

    result = [[1] * n_dim]
    for index in range(n_dim - 1):
        result.append([1] + t_dashed[index])
    return np.array(result)

def solve_bsh_codes(n_dim):
    """
        Returns Bose-Shrikhande code (n, 2n, n/2) for a given n
    """
    hadamard_1 = hadamard(n_dim)
    hadamard_1[hadamard_1 == -1] = 0
    hadamard_2 = (hadamard_1 + 1) % 2
    return np.concatenate([[hadamard_1], [hadamard_2]])

def main():
    """
        Solves the task
    """
    n_dim = int(input())
    codes = solve_bsh_codes(n_dim)
    output = []
    for row in codes.reshape(-1, n_dim):
        output.append("".join(map(str, row)))
    for out in sorted(output):
        print(out)

if __name__ == '__main__':
    main()
