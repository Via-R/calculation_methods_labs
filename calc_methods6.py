import numpy as np
from typing import Callable
from matplotlib import pyplot as plt

def dot(a: float, b: float, f: Callable[[float], float], phi: Callable[[float], float], n: int = 200) -> float:
    h = (b - a) / n
    nodes = [a + i * h for i in range(n)]
    products = [f(nodes[i] - h / 2) * phi(nodes[i] - h / 2) for i in range(n)]
    return sum(products) * h

def function_rescale(f: Callable[[float], float], old_a: float, old_b: float, new_a: float, new_b: float) -> Callable[[float], float]:
    return lambda x: f((old_b - old_a) / (new_b - new_a) * (x - new_a) + old_a)

class LegendreApproximation:
    def __init__(self, a: float, b: float, f: Callable[[float], float]):
        self._a = a
        self._b = b
        self._approx = f
        self._legendre = None

    def get_legendre_approximation_continuous(self, n: int = 5):
        a0 = -1
        b0 = 1
        self._approx = function_rescale(self._approx, self._a, self._b, a0, b0)
        c = np.array([dot(a0, b0, self._approx, self._get_legendre_polynom(i))*(2 * i + 1) / 2 for i in range(n+1)])

        self._legendre = lambda x: np.dot(c, np.array([self._get_legendre_polynom(k)(x) for k in range(n+1)]))

        self._approx = function_rescale(self._approx, a0, b0, self._a, self._b)
        self._legendre = function_rescale(self._legendre, a0, b0, self._a, self._b)

        self._delta()

        return self._legendre

    def _get_legendre_polynom(self, k: int):
        if k == 0:
            return lambda x: 1
        if k == 1:
            return lambda x: x

        return lambda x: (2 * k - 1) / k * x * self._get_legendre_polynom(k - 1)(x) - (k - 1) / k * self._get_legendre_polynom(k - 2)(x)

    def _delta(self):
        print("||f-Qn||^2 = ", dot(self._a, self._b, lambda x: self._approx(x) - self._legendre(x), lambda x: self._approx(x) - self._legendre(x)))


def func(x, A = 10, w = 1.2):
    return np.sin(x)


def plot_approximation(a, b, title: str, f: Callable[[float], float], phi: Callable[[float], float]):
    x = np.linspace(a, b, 200)
    y = [phi(node) for node in x ]
    plt.title(title)
    plt.plot(x, f(x), 'g-', label='True function')
    plt.plot(x, y, color="red", linestyle='-.', label='Approximation function')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.legend()
    plt.show()

if __name__ == "__main__":
    a = 0
    b = 4
    try:
        n = int(input("Введите степень полинома: "))
    except ValueError:
        n = 5
        print("Ошибка ввода, используем стандартное значение")
    legendre = LegendreApproximation(a, b, func)
    Qn_legendre = legendre.get_legendre_approximation_continuous(n)
    title = "Legendre continuous approximation"
    plot_approximation(a, b, title, f=func, phi=Qn_legendre)
    quit()