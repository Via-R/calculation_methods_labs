import numpy as np
from fractions import Fraction as Q

eps = 10e-4

def prvect(v):
	print("( ", end="")
	for i in v:
		print(format(float(i), ".4f"), end=" ")
	print(")")

def prmatr(m):
	print("[")
	for i in m:
		prvect(i)	
	print("]")


def swap_rows(A, x, y):
	if x == y: return A
	temp = A[x].copy()
	A[x] = A[y]
	A[y] = temp
	return(A)

def make_m(main, ind):
	m = np.eye(3, dtype=Q)
	temp = main[ind, ind]
	for i in range(ind, 3):
		m[i, ind] = - main[i, ind] / temp if i != ind else 1 / temp
	return m

def make_rational(a):
	temp = np.zeros(shape=(3, 4), dtype=Q)
	for i in range(0, 3):
		for j in range(0, 4):
			temp[i, j] = Q(a[i, j])
	return temp

def count_cordinality_num(m):
	# det = m[0, 0] * m[1, 1] * m[2, 2] + m[2, 0] * m[0, 1] * m[1, 2] + m[0, 2] * m[1, 0] * m[2, 1] - m[0, 2] * m[1, 1] * m[2, 0] -  m[1, 0] * m[0, 1] * m[2, 2] - m[2, 1] * m[1, 2] * m[0, 0]
	inv = np.linalg.inv(raw_main_matrix)
	return np.linalg.norm(inv, np.inf) * np.linalg.norm(raw_main_matrix, np.inf)

def is_correct():
	print("DET = {}".format(format(np.linalg.det(raw_main_matrix), ".4g")))
	print("DET > 0: ", np.linalg.det(raw_main_matrix) > 0)
	if np.linalg.det(raw_main_matrix) == 0:
		print("ERROR, INCORRECT MATRIX")
		return False
	print("\nA = A^T: ", np.array_equal(raw_main_matrix, raw_main_matrix.T))
	print("DIAGONAL PRIORITY: ", check_diagonal_priority(raw_main_matrix))
	print()
	return True

def check_diagonal_priority(m):
	for i in range(len(m)):
		sum_n = 0
		for j in range(len(m[i])):
			if i != j:
				sum_n += abs(m[i][j])
		if sum_n > m[i][i]:
			return False
	return True

def solve_Gauss(matr, const):

	P_arr = []
	M_arr = []

	for k in range(0, 3):
		abs_max_indexes = np.absolute(matr).argmax(0)
		P = np.eye(3, dtype=Q)
		P = swap_rows(P, abs_max_indexes[k], k)
		print("\nP{}: ".format(k))
		prmatr(P)
		P_arr.append(P)
		matr = P.dot(matr)
		const = P.dot(const)
		M = make_m(matr, k)
		print("\nM{}: ".format(k))
		prmatr(M)
		M_arr.append(M)
		matr = M.dot(matr)
		const = M.dot(const)
		print("\nA{}:".format(k))
		prmatr(matr)
		print("\nCONST:", end="")
		prvect(const)
		print("\n>------------------------------<\n")

	x = [0] * 3
	x[2] = const[2]
	x[1] = const[1] - matr[1,2] * x[2]
	x[0] = const[0] - matr[0,2] * x[2] - matr[0,1] * x[1]
	print("X: ", x)

	E_arr = [np.eye(3, dtype=Q)]
	for k in range(0, 3):
		E = M_arr[k].dot(P_arr[k]).dot(E_arr[k])
		print("\nE{}: ".format(k+1))
		prmatr(E)
		E_arr.append(E)
	
	E_f = E_arr[3]

	a33 = E_f[2, 2]
	a32 = E_f[2, 1]
	a31 = E_f[2, 0]
	a21 = E_f[1, 0] - matr[1, 2] * a31
	a22 = E_f[1, 1] - matr[1, 2] * a32
	a23 = E_f[1, 2] - matr[1, 2] * a33
	a11 = E_f[0, 0] - matr[0, 1] * a21 - matr[0, 2] * a31
	a12 = E_f[0, 1] - matr[0, 1] * a22 - matr[0, 2] * a32
	a13 = E_f[0, 2] - matr[0, 1] * a23 - matr[0, 2] * a33

	final = np.array([
		[a11, a12, a13],
		[a21, a22, a23],
		[a31, a32, a33]
	])
	print("\nFINAL EQUALITY: ")
	prmatr(matr)
	print("*")
	prmatr(final)
	print("=")
	prmatr(E_f)
	print("\nEQUALS?: ")
	print(np.array_equal(matr.dot(final), E_f))

def check_stop(x1, x2):
	if abs(x1[0] - x2[0]) < eps or abs(x1[1] - x2[1]) < eps or abs(x1[2] - x2[2]) < eps:
		return True
	return False

def solve_Jacobi(matr, const):
	const[0] = const[0] / matr[0, 0]
	matr[0] /= matr[0, 0]
	const[1] /= matr[1, 1]
	matr[1] /= matr[1, 1]
	const[2] /= matr[2, 2]
	matr[2] /= matr[2, 2]
	X = np.array([Q(0)] * 3)
	X_prev = const.copy()
	X[0] = - matr[0, 1] * X_prev[1] - matr[0, 2] * X_prev[2] + const[0]
	X[1] = - matr[1, 0] * X_prev[0] - matr[1, 2] * X_prev[2] + const[1]
	X[2] = - matr[2, 0] * X_prev[0] - matr[2, 1] * X_prev[1] + const[2]
	i = 1
	print("X0 = ", end="")
	prvect(X_prev)
	print("X1 = ", end="")
	prvect(X)
	while np.linalg.norm(X_prev - X, np.inf) > eps:
		X_prev = X.copy()
		i+=1
		X[0] = - matr[0, 1] * X_prev[1] - matr[0, 2] * X_prev[2] + const[0]
		X[1] = - matr[1, 0] * X_prev[0] - matr[1, 2] * X_prev[2] + const[1]
		X[2] = - matr[2, 0] * X_prev[0] - matr[2, 1] * X_prev[1] + const[2]
		print("X{} = ".format(i), end="")
		prvect(X)

	print("RESULT X: ", end="")
	prvect(X)

if __name__ == "__main__":
	raw = np.loadtxt('matrix.txt')
	raw_main_matrix = raw[:,:-1]
	raw = make_rational(raw)
	main_matrix = raw[:,:-1]
	constants = raw[:,-1]
	if is_correct():
		print("Cond number:")
		print(count_cordinality_num(main_matrix))
		print("\nGauss method:")
		solve_Gauss(main_matrix.copy(), constants.copy())
		print("\n>------------------------------<\n\n>------------------------------<\n\nJacobi method:\n")
		solve_Jacobi(main_matrix.copy(), constants.copy())
