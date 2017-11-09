import sys
import numpy as np

RANDINT_SEED = 1543
RANDINT_HIGHER = 1000 * 1000 * 1000

def make_graph(edges, ns, seed):
	np.random.seed(seed)
	n1, n2 = ns
	mat = np.zeros(shape = (max(n1, n2), max(n1, n2)))
	for a, b in edges:
		mat[a, b] = np.random.randint(RANDINT_HIGHER)
	return mat


def find_pplc(edges, ns):
	np.seterr(all = 'ignore')
	mat = None
	iter_max = 10
	for _ in range(iter_max):
		mat = make_graph(edges, ns, seed = RANDINT_SEED)
		det = np.linalg.det(mat)
		if det != 0:
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

	if find_pplc(edges, [m_a + 1, m_b + 1]):
		print('yes')
	else:
		print('no')


if __name__ == '__main__':
	main()