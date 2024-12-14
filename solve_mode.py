import curses
import logging
from solver import HitoriSolver

class SolveMode:
	@staticmethod
	def display_instructions(stdscr, is_extended):
		"""
		Отображает инструкции для ввода головоломки.
		"""
		stdscr.clear()
		if is_extended:
			stdscr.addstr(0, 0,
						  "Введите головоломку строка за строкой, разделяя числа пробелами. Для завершения введите пустую строку:")
		else:
			stdscr.addstr(0, 0, "Введите головоломку строка за строкой, разделяя числа пробелами:")
		stdscr.refresh()

	@staticmethod
	def get_row_input(stdscr, row_number):
		"""
		Получает ввод строки от пользователя.
		"""
		stdscr.addstr(row_number + 1, 0, f"Строка {row_number + 1}: ")
		stdscr.refresh()

		row_input = ""
		cursor_pos = len(f"Строка {row_number + 1}: ")
		while True:
			key = stdscr.getch()
			if key in (10, 13):  # Enter
				break
			elif key in (8, 127, curses.KEY_BACKSPACE):  # Backspace
				if cursor_pos > len(f"Строка {row_number + 1}: "):
					row_input = row_input[:-1]
					cursor_pos -= 1
					stdscr.addstr(row_number + 1, cursor_pos, " ")
					stdscr.refresh()
			elif 48 <= key <= 57 or key == ord(" "):  # Цифры и пробелы
				row_input += chr(key)
				cursor_pos += 1
			stdscr.addstr(row_number + 1, len(f"Строка {row_number + 1}: "), row_input)
			stdscr.refresh()

		return row_input

	@staticmethod
	def validate_row(grid, row, is_extended):
		"""
		Проверяет корректность введенной строки.
		"""
		row = list(map(int, row.split()))
		logging.debug(f"num_count {len(row)}")

		if grid and len(row) != len(grid[0]):
			raise ValueError("Все строки должны быть одной длины.")
		for num in row:
			if num > len(row) and not is_extended:
				raise ValueError("Числа не должны превышать размер квадрата")
			if not is_extended and num <= 0:
				raise ValueError("Числа должны быть больше 0")

		return row

	@staticmethod
	def validate_grid(grid, is_extended):
		"""
		Проверяет корректность всей сетки.
		"""
		if is_extended:
			max_width = len(grid[0])
			max_height = len(grid)
			max_allowed = max(max_width, max_height)
			for row in grid:
				for num in row:
					if num > max_allowed:
						raise ValueError(f"Число {num} превышает финальное допустимое значение {max_allowed}.")

	@staticmethod
	def display_solutions(stdscr, grid, solutions, is_extended):
		"""
		Отображает решения головоломки.
		"""
		solution_index = 0
		while True:
			solution = solutions[solution_index]

			# Очищаем экран от предыдущего решения
			stdscr.clear()
			stdscr.addstr(0, 0, "Введенная головоломка:")
			for row_idx, row in enumerate(grid):
				stdscr.addstr(row_idx + 1, 0, " ".join(map(str, row)))

			stdscr.addstr(len(grid) + 2, 0, f"Решение {solution_index + 1} из {len(solutions)}:")

			for row_idx, row in enumerate(solution):
				stdscr.addstr(len(grid) + 3 + row_idx, 0, " ".join(map(str, row)))

			stdscr.addstr(len(grid) + 3 + len(solution), 0, "Нажмите стрелки для навигации, q для выхода в меню.")
			stdscr.refresh()

			key = stdscr.getch()
			if key in (ord("q"), ord("Q"), ord("й"), ord("Й")):
				return True  # Возвращаем True, чтобы указать, что пользователь вышел в меню
			elif key == curses.KEY_LEFT:  # Стрелка влево
				solution_index = max(0, solution_index - 1)
			elif key == curses.KEY_RIGHT:  # Стрелка вправо
				solution_index = min(len(solutions) - 1, solution_index + 1)

	@staticmethod
	def solve_mode(stdscr, is_extended):
		SolveMode.display_instructions(stdscr, is_extended)

		grid = []
		while True:
			row_input = SolveMode.get_row_input(stdscr, len(grid))
			if is_extended and row_input == "":
				break

			try:
				row = SolveMode.validate_row(grid, row_input, is_extended)
				grid.append(row)
			except ValueError as e:
				stdscr.addstr(len(grid) + 2, 0, f"Ошибка ввода: {str(e)}")
				stdscr.refresh()
				stdscr.getch()
				return False  # Возвращаем False, чтобы указать, что режим завершился с ошибкой

			if len(grid) + 1 == len(row) + 1 and not is_extended:
				break

		try:
			SolveMode.validate_grid(grid, is_extended)
			solutions = HitoriSolver.solve(grid, is_extended)
		except Exception as e:
			stdscr.addstr(len(grid) + 3, 0, f"Ошибка решения: {str(e)}")
			stdscr.refresh()
			stdscr.getch()
			return False  # Возвращаем False, чтобы указать, что режим завершился с ошибкой

		if len(solutions) == 0:
			stdscr.clear()
			stdscr.addstr(0, 0, "Введенная головоломка:")
			for row_idx, row in enumerate(grid):
				stdscr.addstr(row_idx + 1, 0, " ".join(map(str, row)))

			stdscr.addstr(len(grid) + 2, 0, "Решений нет. Нажмите любую клавишу для выхода.")
			stdscr.refresh()
			stdscr.getch()
			return False  # Возвращаем False, чтобы указать, что режим завершился с ошибкой

		return SolveMode.display_solutions(stdscr, grid, solutions, is_extended)