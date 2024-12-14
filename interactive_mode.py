import curses
from grid_generator import HitoriGenerator
from display import Display
from solver import HitoriSolver

class InteractiveMode:
	@staticmethod
	def interactive_mode(stdscr, is_extended, height, width):
		try:
			if is_extended:
				grid = HitoriGenerator.generate_hitori_grid(width, height, is_extended)
			else:
				grid = HitoriGenerator.generate_hitori_grid(width, width, is_extended)
		except Exception as e:
			stdscr.addstr(1, 0, f"Ошибка генерации сетки: {str(e)}")
			stdscr.refresh()
			stdscr.getch()
			return False

		original_grid = [row[:] for row in grid]
		cursor_row, cursor_col = 0, 0

		while True:
			Display.display_grid(stdscr, grid, cursor_row, cursor_col)
			stdscr.addstr(
				len(grid) + 1,
				0,
				"Используйте стрелки для перемещения, пробел для закрашивания/отмены, q для выхода в меню.",
			)
			stdscr.refresh()

			key = stdscr.getch()
			if key == curses.KEY_UP and cursor_row > 0:
				cursor_row -= 1
			elif key == curses.KEY_DOWN and cursor_row < len(grid) - 1:
				cursor_row += 1
			elif key == curses.KEY_LEFT and cursor_col > 0:
				cursor_col -= 1
			elif key == curses.KEY_RIGHT and cursor_col < len(grid[0]) - 1:
				cursor_col += 1
			elif key == ord(" "):
				Display.toggle_cell(grid, original_grid, cursor_row, cursor_col)
			elif key in (ord("q"), ord("Q"), ord("й"), ord("Й")):
				return True

			if HitoriSolver.is_valid(grid, is_extended) and HitoriSolver.is_connected(grid, is_extended):
				Display.display_grid(stdscr, grid, cursor_row, cursor_col)
				stdscr.addstr(len(grid) + 2, 0, "Поздравляем! Вы решили головоломку!")
				stdscr.refresh()
				stdscr.getch()
				return True