import numpy as np
from sympy import symbols, simplify
from math import cos, pi

print("Function: 8^x")
print("\nNewton:")
func = "8 ** {}"
dots = [0, 1, 2]
f_dots = []
for i in dots:
	f_dots.append(eval(func.format(i)))
table = [dots, f_dots, [], 0]
table[2].append((f_dots[1] - f_dots[0])/(dots[1]-dots[0]))
table[2].append((f_dots[2] - f_dots[1])/(dots[2]-dots[1]))
table[3] = (table[2][1] - table[2][0])/(dots[2]-dots[0])
print("\nTable: ")
print(table)
x = symbols('x')

print()
answ1 = simplify(table[1][0] + (x - table[0][0]) * table[2][0] + (x - table[0][0]) * (x - table[0][1]) * table[3])
print(answ1)

def get_ch_zero(a, b, k):
	return (b+a)/2+(b-a)/2*cos((2*k+1)*pi/6)

print("\nChebyshev:")
a = 0
b = 2
x0 = get_ch_zero(a, b, 0)
x1 = get_ch_zero(a, b, 1)
x2 = get_ch_zero(a, b, 2)
dots = [x0, x1, x2]
f_dots = []
for i in dots:
	f_dots.append(eval(func.format(i)))
table = [dots, f_dots, [], 0]
table[2].append((f_dots[1] - f_dots[0])/(dots[1]-dots[0]))
table[2].append((f_dots[2] - f_dots[1])/(dots[2]-dots[1]))
table[3] = (table[2][1] - table[2][0])/(dots[2]-dots[0])
print("\nTable: ")
print(table)
x = symbols('x')

print()
answ2 = simplify(table[1][0] + (x - table[0][0]) * table[2][0] + (x - table[0][0]) * (x - table[0][1]) * table[3])
print(answ2)
