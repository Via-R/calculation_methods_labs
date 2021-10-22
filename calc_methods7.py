from sympy import *
x = symbols("x")
function = sin

func = function(x)
a = -1
b = 1

def zero_pow():
	func_diff = lambdify(x, diff(func), 'numpy')
	possible_points_raw = solve([Eq(func)], [x])
	possible_points = [a, b]
	for i in range(len(possible_points_raw)):
		if possible_points_raw[i][0] > a and possible_points_raw[i][0] < b:
			possible_points.append(possible_points_raw[i][0])
	possible_points.sort()
	m = possible_points[0]
	M = possible_points[-1]
	c0 = (M + m) / 2
	print("ZERO POWER: {}".format(c0))

def first_pow():
	c1 = (function(b) - function(a))/(b-a)
	ksi = solve([diff(func) - c1], [x])[0][0]
	c0 = (function(ksi) - c1 * ksi + function(a) - c1 * a) / 2
	print("FIRST POWER: {}x + {}".format(c1, c0))
	

def second_pow():
	pass


zero_pow()
first_pow()