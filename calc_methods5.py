from scipy.integrate import quad
from math import sin
from numpy import arange

left = 0
right = 1
step = 0.05

def legendre(n):
	if n == 0:
		return lambda x: 1
	elif n == 1:
		return lambda x : x
	return lambda x: (((2*n - 1) * x * legendre(n - 1)(x) - (n-1) * legendre(n - 2)(x)) / n)
# def legendre(x, n):
	# if n == 0:
		# return 1
	# elif n == 1:
		# return x
	# return (((2*n - 1) * x * legendre(x, n - 1) - (n-1) * legendre(x, n - 2)) / n)

def f(x):
	return sin(x)

print((right + left) / 2)
print((right - left) / 2)

# def integrand(x, n):

	# t = (right + left) / 2 + (right - left) / 2 * x
	

	# t = (2*x-(right+left))/(right-left)
	# return f(t) * legendre(t, n)
	

# def get_Ck(k):
	# return (2*k + 1) / 2 * quad(integrand, -1, 1, args=k)[0]

def scale(x):
	return (2*x-(right+left))/(right-left)
	# return (2*x-(right+left))/(right-left)

import matplotlib.pyplot as plt
xs = list(arange(left,right,step))
ys = list()
nodes_len = len(xs)
for i in xs:
	ys.append(f(i))

scaled_xs = list()
for i in xs:
	scaled_xs.append(scale(i))

lambdas = [legendre(i) for i in range(nodes_len)]
print("LAMBDAS")
# pre_cs = list()
# for i in range(len(scaled_xs)):
	# pre_cs.append(lambdas[i](scaled_xs[i]))

def integ(x, ind):
	t1 = (right + left) / 2 + (right - left) / 2 * x
	t2 = (2*x-(right+left))/(right-left)
	return f(t2) * lambdas[i](t1)

cs = list()
for i in range(nodes_len):
	el = (2*i + 1) / 2 * quad(integ, -1, 1, args=i)[0]
	cs.append(el)
print("QUADS")

csy = list()

def calc_pol(x):
	res = 0
	t1 = (right + left) / 2 + (right - left) / 2 * x
	t2 = (2*x-(right+left))/(right-left)
	for i in range(nodes_len):
		res += cs[i] * lambdas[i](t1)
	return res

for i in xs:
	ty = calc_pol(i)
	# csy.append((right+left)/2+(right-left)/2*ty)
	# csy.append((2*ty-(right+left))/(right-left))
	csy.append(ty)

print("DONE")

plt.plot(xs, ys, 'ro', xs, csy, 'b--')
plt.axis([left, right, -1, 1])
plt.show()


# a = 2
# b = 1
# I = quad(integrand, 0, 1, args=(a,b))
# print(I)