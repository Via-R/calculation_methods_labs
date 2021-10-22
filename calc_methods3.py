import numpy as np
from math import sin, cos, atan, pi
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


x0 = np.array([0, 0])

F_str = ["{0}-1/2*sin(({0}-{1})/2)", "{1}-1/2*cos(({0}+{1})/2)"]


F = np.array([
	x0[0]-1/2*sin((x0[0]-x0[1])/2),
	x0[1]-1/2*cos((x0[0]+x0[1])/2)
])

A = np.array([
	[1 - 1/4*cos((x0[0]-x0[1])/2), 1/4*cos((x0[0]-x0[1])/2)],
	[1/4*sin((x0[0]+x0[1])/2), 1+1/4*sin((x0[0]+x0[1])/2)]
])

A1 = np.linalg.inv(A)

x = x0 - A1.dot(F)
x_p = x0.copy()

eps = 10e-8

i = 0

print("Modified Newton")
print(F_str[0].format("x", "y"), "= 0")
print(F_str[1].format("x", "y"), "= 0", end="\n")

print("\nA: ")
prmatr(A)

print("\nF'(x0):")
prvect(F)

print("\n")

while np.linalg.norm(x-x_p) > eps and i < 100:

	x_p = x.copy()
	F[0] = eval(F_str[0].format(x_p[0], x_p[1]))
	F[1] = eval(F_str[1].format(x_p[0], x_p[1]))
	x = x - A1.dot(F)
	i+=1

print("Answer:")
prvect(x)

print("Steps: ", i)

print("\n======================\n")

def find_absmax(A):
	temp = np.absolute(A)
	max_el = -1
	ind = (0, 1)
	for i in range(len(temp)):
		for j in range(len(temp[i])):
			if i == j: 
				continue
			if temp[i, j] > max_el:
				max_el = temp[i, j]
				ind = (i, j)
	return ind

def find_max(A):
	temp = np.absolute(A)
	max_el = -1
	for i in range(len(temp)):
		for j in range(len(temp[i])):
			if i == j: 
				continue
			if temp[i, j] > max_el:
				max_el = temp[i, j]
	return max_el

def count_non_d(A):
	res = 0
	for i in range(len(A)):
		for j in range(len(A[i])):
			if i == j: 
				continue
			res += A[i, j] ** 2
	return res

print("Jacobi\n")

print("A0:")

A = np.array([
	[5, -1, 1],
	[-1, 0, -2],
	[1, -2, 1]
])
prmatr(A)
count = 1
while count < 10000 and find_max(A) > eps:
	count+=1
	V = np.eye(3)

	i0, j0 = find_absmax(A)
	phi = 1/2*atan(2*A[i0, j0]/(A[i0, i0] - A[j0, j0])) if A[i0, i0] != A[j0, j0] else pi/4

	V[i0, i0] = cos(phi)
	V[i0, j0] = -sin(phi)
	V[j0, i0] = sin(phi)
	V[j0, j0] = cos(phi)

	A = V.T.dot(A.dot(V))
print("\nResult:")
prmatr(A)
print("\nSteps: ", count)