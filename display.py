import curses

class Display:
	@staticmethod
	def display_grid(stdscr, grid, cursor_row=-1, cursor_col=-1):
		"""
		Отображение сетки на экране с подсветкой курсора.
		"""
		stdscr.clear()
		for row_idx, row in enumerate(grid):
			for col_idx, cell in enumerate(row):
				# Подсветка ячейки под курсором
				if row_idx == cursor_row and col_idx == cursor_col:
					stdscr.attron(curses.A_REVERSE)

				# Отображение содержимого ячейки (с учетом символа "X")
				if cell == "X":
					stdscr.addstr(row_idx, col_idx * 2, str(cell), curses.A_BOLD | curses.A_REVERSE if row_idx == cursor_row and col_idx == cursor_col else curses.A_BOLD)
				else:
					stdscr.addstr(row_idx, col_idx * 2, str(cell))

				# Выключение подсветки
				if row_idx == cursor_row and col_idx == cursor_col:
					stdscr.attroff(curses.A_REVERSE)
		stdscr.refresh()

	@staticmethod
	def toggle_cell(grid, original_grid, row, col):
		"""
		Закрашивает или снимает закраску с ячейки.
		"""
		if grid[row][col] == "X":
			grid[row][col] = original_grid[row][col]
		else:
			grid[row][col] = "X"