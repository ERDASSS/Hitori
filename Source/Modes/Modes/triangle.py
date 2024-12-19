from __future__ import annotations
from Source.Modes.mode import Mode
from Source.Helpers.reader import Reader

class Triangle(Mode):
	NAME = "Triangle"

	@staticmethod
	def read_grid_info(screen) -> None | tuple[int, int]:
		screen.addstr(0, 0, "Введите размер поля [3;6]: ")
		screen.refresh()

		size_input = Reader.get_user_input(screen, 0, "Введите размер поля [3;6]: ")
		if size_input is None:
			return None

		try:
			size = int(size_input)
			if size < 3 or size > 6:
				raise ValueError("Размер поля должен быть в пределах [3;6]")
		except ValueError as e:
			screen.addstr(1, 0, f"Ошибка: {str(e)}")
			screen.refresh()
			screen.getch()
			return None

		return size, size

	@staticmethod
	def display_input_info(screen):
		screen.addstr(0, 0, "Введите головоломку строка за строкой, разделяя числа пробелами:")

	@staticmethod
	def validate_grid(grid: list[list[int]]):
		max_allowed = len(grid[-1])
		for row in grid:
			Mode.validate_row(row)
			for num in row:
				if num > max_allowed:
					raise ValueError(f"Число {num} превышает финальное допустимое значение {max_allowed}.")