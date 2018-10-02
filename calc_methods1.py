from math import log, log2, ceil
from fractions import Fraction as Q

eps = 10e-4
equation = "x^5 + x - 3 = 0"

class Approximator:
	"""Зберігає загальні методи, що використовуються усіма унаслідуваними класами."""

	def __init__(self):
		self.log = ""
		self.n = -1
		self.name = ""

	def _add_entry(self, text, newline=True):
		"""Записує отриманий в параметрі текст до змінної, що зберігає увесь текст розв'язку поточним методом."""

		self.log += text + "\n" + "\n" * newline

	def _eval_iterations(self):
		"""Виконує розрахунок асимптотичної оцінки кільькості ітерацій."""

		pass

	def _iter(self):
		"""Виконує одну ітерацію розв'язку."""

		pass

	def _solve(self):
		"""Виконує ітерації та записує описову інформацію."""

		# Перевіривши потрібні умови, можна зробити висновок, що всі сталі обрані вірно
		# Можна починати процес ітерацій, перед цим розрахувавши апріорну асимптотичну оцінку кількості ітерацій
		self._eval_iterations()
		self._add_entry("Поточний метод наближеного розв`язку рівняння ({}): {}".format(equation, self.name))
		self._add_entry("Апріорна оцінка кількості ітерацій: {}".format(self.n))
		self._add_entry("x[0] = {}".format(float(self.x0)), False)
		x_main = self._iter(self.x0)
		iterations = 1
		x_old = self.x0
		while abs(x_main - x_old) > eps:
			self._add_entry("x[{}] = {}".format(iterations, x_main), False)
			x_old, x_main = x_main, self._iter(x_main)
			iterations += 1
		self._add_entry("\nРозраховане наближення кореня заданого рівняння: {}\nАпостеріорна оцінка кількості ітерацій: {}".format(format(float(x_main), ".4g"), iterations))
		self._add_entry(">----------------------------<", False)

	def get_log(self):
		"""Ініціює початок розв'язання та повертає отриманий текст розв'язку."""

		self._solve()
		return self.log

class IterationsAprx(Approximator):
	"""Проводить розрахунки для методу простих ітерацій."""

	def __init__(self):
		super().__init__()
		# Корінь знаходиться на проміжку [1, 2], перша похідна функції x = (3-x)^(1/5) на заданому проміжку має максимум 1/5, в якості першого наближення обираємо лівий край проміжку
		self.a = 1
		self.b = 2
		self.x0 = 1
		self.q = Q(1, 5)
		self.name = "Метод простих ітерацій"

	def _eval_iterations(self):
		"""Виконує розрахунок асимптотичної оцінки кільькості ітерацій."""

		self.n = ceil(log((self.b - self.a) / (eps * (1 - self.q))) / log(1 / self.q))

	def _iter(self, x):
		"""Виконує одну ітерацію розв'язку."""

		return (3 - x) ** Q(1, 5)

class NewtonAprx(Approximator):
	"""Проводить розрахунки для методу Н'ютона."""

	def __init__(self):
		super().__init__()
		# Корінь знаходиться на проміжку [1, 6/5], m[1] = 6, M[2] = 864/25
		self.a = 1
		self.b = Q(6, 5)
		self.x0 = Q(6, 5)
		self.q = Q(72, 125)
		self.name = "Метод Н`ютона"

	def _eval_iterations(self):
		"""Виконує розрахунок асимптотичної оцінки кільькості ітерацій."""

		self.n = ceil(log2((log(1 / (5 * eps))) / (log(1 / self.q)) + 1) + 1)

	def _iter(self, x):
		"""Виконує одну ітерацію розв'язку."""

		return float(x - (x**5 + x - 3)/(5 * x**4 + 1))


if __name__ == "__main__":
	solver = IterationsAprx()
	print(solver.get_log())

	solver = NewtonAprx()
	print(solver.get_log())
	