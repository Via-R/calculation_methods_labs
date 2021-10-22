from math import sin, cos, pi

int_function = lambda x: sin(8*x) * cos(2*x)

def trapezoid_rule(func, a, b, nseg):
    """Правило трапеций
       nseg - число отрезков, на которые разбивается [a;b]"""
    dx = 1.0 * (b - a) / nseg
    sum = 0.5 * (func(a) + func(b))
    for i in range(1, nseg):
        sum += func(a + i * dx)

    return sum * dx

def _rectangle_rule(func, a, b, nseg, frac):
    """Обобщённое правило прямоугольников."""
    dx = 1.0 * (b - a) / nseg
    sum = 0.0
    xstart = a + frac * dx # 0 <= frac <= 1 задаёт долю смещения точки, 
                           # в которой вычисляется функция,
                           # от левого края отрезка dx
    for i in range(nseg):
        sum += func(xstart + i * dx)

    return sum * dx

def left_rectangle_rule(func, a, b, nseg):
    """Правило левых прямоугольников"""
    return _rectangle_rule(func, a, b, nseg, 0.0)

def right_rectangle_rule(func, a, b, nseg):
    """Правило правых прямоугольников"""
    return _rectangle_rule(func, a, b, nseg, 1.0)

def midpoint_rectangle_rule(func, a, b, nseg):
    """Правило прямоугольников со средней точкой"""
    return _rectangle_rule(func, a, b, nseg, 0.5)


def runge(method, func, a, b, precision = 1e-8):
    nsegm = 42
    int_1 = method(func, a, b, int(nsegm / 2))
    int_2 = method(func, a, b, nsegm)
    safety_counter = 1
    while abs((int_1 - int_2) / 3) > precision and safety_counter < 1e5:
        nsegm *= 2
        int_1 = int_2
        int_2 = method(func, a, b, nsegm)
        safety_counter += 1

    return int_2, safety_counter

print("Розрахунок інтегралу від функції sin(8*x) * cos(2*x) на проміжку від 0 до П/2\n")
print("Метод трапецій, відрізок розбиваємо на 10000 частин")
print(trapezoid_rule(int_function, 0, pi / 2, 10000))
print("Метод середніх прямокутників, відрізок розбиваємо на 10000 частин")
print(midpoint_rectangle_rule(int_function, 0, pi / 2, 10000))
print("-" * 21)
print("Метод трапецій, точність 10^-8 за правилом Рунге")
print(runge(trapezoid_rule, int_function, 0, pi / 2))
print("Метод середніх прямокутників, точність 10^-8 за правилом Рунге")
print(runge(midpoint_rectangle_rule, int_function, 0, pi / 2))