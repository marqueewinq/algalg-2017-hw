import sys
import numpy as np

RANDINT_SEED = 1543
RANDINT_HIGHER = 100
EPS = 1e-9

def det(mat):
	width = len(mat)
	answer = 1
	for i in range(width):
		k = i
		for j in range(i + 1, width):
			if abs(mat[j][i]) > abs(mat[k][i]):
				k = j

		if abs(mat[k][i]) < EPS:
			return 0

		mat[i], mat[k] = mat[k], mat[i]
		if i != k:
			answer = -answer

		answer *= mat[i][i]
		for j in range(i + 1, width):
			mat[i][j] /= mat[i][i]

		for j in range(width):
			if j != i and abs(mat[j][i]) > EPS:
				for k in range(i + 1, width):
					mat[j][k] -= mat[i][k] * mat[j][i]
	return answer


def throw_dice():
	cruel_random = 0
	while cruel_random < EPS:
		cruel_random = np.random.random() * RANDINT_HIGHER
	return cruel_random


def make_graph(edges, ns):
	n1, n2 = ns
	mat = np.zeros(shape = (max(n1, n2), max(n1, n2)))
	for a, b in edges:
		mat[a, b] = throw_dice()
	return mat


def find_pplc(edges, ns):
	np.seterr(all = 'ignore')
	np.random.seed(seed = RANDINT_SEED)
	mat = None
	iter_max = 10
	for _ in range(iter_max):
		mat = make_graph(edges, ns)
		d = det(mat.tolist())
		if d != 0:
			return True
	return False


def main():
	edges = []
	m_a = m_b = 0
	with sys.stdin as f:
		n = int(f.readline())
		for _ in range(n):
			a, b = list(map(int, f.readline().split()))
			m_a = max(m_a, a)
			m_b = max(m_b, b)
			edges.append([a, b])

	if n == 0 or find_pplc(edges, [m_a + 1, m_b + 1]):
		print('yes')
	else:
		print('no')


if __name__ == '__main__':
	main()
