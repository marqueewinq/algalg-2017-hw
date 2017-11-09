import sys
import numpy as np

RANDINT_SEED = 1543
RANDINT_HIGHER = 1000 * 1000 * 1000
MOD = 1e9 + 7


def det(matrix, mul = 1):
	width = len(matrix)
	if width == 1:
		return mul * matrix[0][0]

	sign = -1
	answer = 0
	for i in range(width):
		m = []
		for j in range(1, width):
			minor = []
			for k in range(width):
				if k != i:
					minor.append(matrix[j][k])
			m.append(minor)

		sign *= -1
		answer += mul * solve(m, sign * matrix[0][i])

	return answer % MOD

#matrix = [[1,-2,3],[0,-3,-4],[0,0,-3]]
#print(solve(matrix, 1))


def make_graph(edges, ns):
	n1, n2 = ns
	mat = np.zeros(shape = (max(n1, n2), max(n1, n2)))
	for a, b in edges:
		mat[a, b] = np.random.randint(RANDINT_HIGHER)
	return mat


def find_pplc(edges, ns):
	np.seterr(all = 'ignore')
	np.random.seed(seed = RANDINT_SEED)
	mat = None
	iter_max = 10
	for _ in range(iter_max):
		mat = make_graph(edges, ns)
		det = np.linalg.det(mat)
		#print (det)
		#print (mat)
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

	if n == 0 or find_pplc(edges, [m_a + 1, m_b + 1]):
		print('yes')
	else:
		print('no')


if __name__ == '__main__':
	main()
